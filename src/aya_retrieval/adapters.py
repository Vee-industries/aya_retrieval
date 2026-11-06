"""Start a training run from a saved adapter, for a stepping stone's next step (R-103)."""

from __future__ import annotations

import json
from pathlib import Path

import torch
from peft import get_peft_model_state_dict, set_peft_model_state_dict
from safetensors.torch import load_file


def load_lora_weights(model, adapter_dir: Path) -> int:
    """Copy a saved adapter's LoRA weights into ``model``, a freshly wrapped PEFT model.

    The saved adapter must have the same rank, alpha and target modules as ``model``'s, and after
    loading every LoRA weight in ``model`` must equal the file's, so a step starts exactly where its
    parent ended.

    Returns:
        The number of weight tensors loaded.

    Raises:
        ValueError: If the configurations differ, or the weights do not match after loading.
    """
    saved = json.loads((adapter_dir / "adapter_config.json").read_text(encoding="utf-8"))
    config = model.peft_config["default"]
    if (saved["r"], saved["lora_alpha"], set(saved["target_modules"])) != (
        config.r,
        config.lora_alpha,
        set(config.target_modules),
    ):
        raise ValueError(f"{adapter_dir} has a different LoRA configuration from this run")
    weights = load_file(str(adapter_dir / "adapter_model.safetensors"))
    set_peft_model_state_dict(model, weights)
    loaded = get_peft_model_state_dict(model)
    if set(loaded) != set(weights):
        raise ValueError(f"{adapter_dir}'s weights do not name this model's LoRA modules")
    for name, tensor in weights.items():
        if not torch.equal(loaded[name].detach().cpu().to(tensor.dtype), tensor):
            raise ValueError(f"{name} differs from {adapter_dir} after loading")
    return len(weights)
