"""Write a dial adapter from trained ones: one scaled toward base, or two blended (R-088).

Neither is a shippable model; each is scored to see where a trained adapter sits between two others.

Usage:
    python scripts/make_dial_adapter.py scale ADAPTER OUT --by 0.85
    python scripts/make_dial_adapter.py mix FIRST SECOND OUT --a 0.3

``scale`` multiplies every LoRA B matrix by ``by``, so the change to each weight is ``by`` times the
adapter's. ``mix`` stacks the two adapters' ranks: A matrices one above the other, B matrices
side by side, the first's scaled by ``a`` and the second's by ``1 - a``. With ``alpha / r`` kept,
the change to each weight is exactly ``a`` times the first's plus ``1 - a`` times the second's.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file

WEIGHTS = "adapter_model.safetensors"
CONFIG = "adapter_config.json"


def scaled(tensors: dict[str, torch.Tensor], by: float) -> dict[str, torch.Tensor]:
    """Return the adapter's tensors with every LoRA B matrix multiplied by ``by``."""
    return {k: v * by if ".lora_B." in k else v for k, v in tensors.items()}


def mixed(
    first: dict[str, torch.Tensor], second: dict[str, torch.Tensor], a: float
) -> dict[str, torch.Tensor]:
    """Return one adapter of twice the rank whose change is ``a`` first plus ``1 - a`` second."""
    if first.keys() != second.keys():
        raise ValueError("the two adapters train different modules")
    out = {}
    for key in first:
        if ".lora_A." in key:
            out[key] = torch.cat([first[key], second[key]], dim=0)
        elif ".lora_B." in key:
            out[key] = torch.cat([first[key] * a, second[key] * (1 - a)], dim=1)
        else:
            raise ValueError(f"unexpected tensor {key}")
    return out


def check_config(config: dict) -> None:
    if config.get("use_rslora") or config.get("use_dora") or config.get("rank_pattern"):
        raise ValueError("only plain LoRA with one rank is supported")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="mode", required=True)
    scale = sub.add_parser("scale")
    scale.add_argument("adapter", type=Path)
    scale.add_argument("out", type=Path)
    scale.add_argument("--by", type=float, required=True)
    mix = sub.add_parser("mix")
    mix.add_argument("adapter", type=Path)
    mix.add_argument("second", type=Path)
    mix.add_argument("out", type=Path)
    mix.add_argument("--a", type=float, required=True)
    args = parser.parse_args()

    config = json.loads((args.adapter / CONFIG).read_text(encoding="utf-8"))
    check_config(config)
    tensors = load_file(args.adapter / WEIGHTS)
    if args.mode == "scale":
        tensors, made = scaled(tensors, args.by), {"scale": args.by}
    else:
        other = json.loads((args.second / CONFIG).read_text(encoding="utf-8"))
        check_config(other)
        if (other["r"], other["lora_alpha"]) != (config["r"], config["lora_alpha"]):
            raise ValueError("the two adapters differ in rank or alpha")
        tensors = mixed(tensors, load_file(args.second / WEIGHTS), args.a)
        config = {**config, "r": 2 * config["r"], "lora_alpha": 2 * config["lora_alpha"]}
        made = {"mix": [args.adapter.as_posix(), args.second.as_posix()], "a": args.a}

    args.out.mkdir(parents=True, exist_ok=True)
    for name in args.adapter.iterdir():
        if name.name not in (WEIGHTS, CONFIG) and name.is_file():
            shutil.copy2(name, args.out / name.name)
    (args.out / CONFIG).write_text(json.dumps(config, indent=2), encoding="utf-8")
    save_file(tensors, args.out / WEIGHTS)
    (args.out / "dial.json").write_text(
        json.dumps({"from": args.adapter.as_posix(), **made}, indent=1), encoding="utf-8"
    )
    print(f"wrote {args.out}: {made}")


if __name__ == "__main__":
    main()
