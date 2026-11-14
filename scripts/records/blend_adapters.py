"""R-237: an exact blend of two LoRA adapters on the same base, as one adapter of twice the rank.

Usage: python scripts/records/blend_adapters.py FIRST SECOND WEIGHT OUT

Each adapter changes a weight by s * B @ A (s = lora_alpha / r). The blend's change is
(1 - WEIGHT) * s * B1 @ A1 + WEIGHT * s * B2 @ A2, written exactly as one adapter of rank r1 + r2:
A = [A1; A2] stacked by rows, B = [(1 - WEIGHT) * B1, WEIGHT * B2] side by side, and lora_alpha
doubled so s stays the same. Both adapters must share the base, the target modules and s.
``--check`` instead confirms on every layer that weight 0 and 1 give back each adapter's own change.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file

WEIGHTS = "adapter_model.safetensors"
CONFIG = "adapter_config.json"


def load(path: Path) -> tuple[dict, dict]:
    return json.loads((path / CONFIG).read_text(encoding="utf-8")), load_file(str(path / WEIGHTS))


def pairs(tensors: dict) -> dict[str, tuple[torch.Tensor, torch.Tensor]]:
    """Each LoRA layer's (A, B), keyed by the name before ``.lora_A.weight``."""
    out = {}
    for key, a in tensors.items():
        if key.endswith(".lora_A.weight"):
            stem = key.removesuffix(".lora_A.weight")
            out[stem] = (a, tensors[f"{stem}.lora_B.weight"])
    if 2 * len(out) != len(tensors):
        raise ValueError("an adapter holds tensors other than LoRA A and B pairs")
    return out


def blend(first: Path, second: Path, weight: float) -> tuple[dict, dict]:
    (c1, t1), (c2, t2) = load(first), load(second)
    for field in ("base_model_name_or_path", "r", "lora_alpha"):
        if c1.get(field) != c2.get(field):
            raise ValueError(f"the adapters differ in {field}")
    if set(c1["target_modules"]) != set(c2["target_modules"]):
        raise ValueError("the adapters differ in target_modules")
    p1, p2 = pairs(t1), pairs(t2)
    if set(p1) != set(p2):
        raise ValueError("the adapters have different layers")
    out = {}
    for stem, (a1, b1) in p1.items():
        a2, b2 = p2[stem]
        out[f"{stem}.lora_A.weight"] = torch.cat([a1, a2], dim=0).contiguous()
        out[f"{stem}.lora_B.weight"] = torch.cat(
            [(1 - weight) * b1, weight * b2], dim=1
        ).contiguous()
    config = {**c1, "r": 2 * c1["r"], "lora_alpha": 2 * c1["lora_alpha"]}
    return config, out


def change(a: torch.Tensor, b: torch.Tensor, config: dict) -> torch.Tensor:
    return (config["lora_alpha"] / config["r"]) * (b.double() @ a.double())


def check(first: Path, second: Path) -> None:
    """Weight 0 gives the first adapter's change and weight 1 the second's, on every layer."""
    worst = 0.0
    for weight, source in ((0.0, first), (1.0, second)):
        config, tensors = blend(first, second, weight)
        own_config, own = load(source)
        for stem, (a, b) in pairs(tensors).items():
            a0, b0 = pairs(own)[stem]
            gap = (change(a, b, config) - change(a0, b0, own_config)).abs().max().item()
            worst = max(worst, gap)
    print(f"largest gap over all layers, weights 0 and 1: {worst:.3g}")
    if worst > 1e-6:
        raise SystemExit("FAIL: the blend does not give back the adapters")
    print("PASS")


def main() -> None:
    if sys.argv[1] == "--check":
        check(Path(sys.argv[2]), Path(sys.argv[3]))
        return
    first, second, weight, out = (
        Path(sys.argv[1]),
        Path(sys.argv[2]),
        float(sys.argv[3]),
        Path(sys.argv[4]),
    )
    config, tensors = blend(first, second, weight)
    out.mkdir(parents=True, exist_ok=True)
    for name in ("tokenizer.json", "tokenizer_config.json", "chat_template.jinja"):
        if (first / name).exists():
            shutil.copy(first / name, out / name)
    (out / CONFIG).write_text(json.dumps(config, indent=2), encoding="utf-8")
    save_file(tensors, str(out / WEIGHTS))
    print(
        f"{out}: rank {config['r']}, weight {weight} on {second.name}, {len(tensors) // 2} layers"
    )


if __name__ == "__main__":
    main()
