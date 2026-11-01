"""Checks on a finished training run."""

from __future__ import annotations

from pathlib import Path

from safetensors.torch import load_file


def adapter_moved(adapter_path: Path) -> bool:
    """Return True if any LoRA update weight left its zero start, meaning training changed the model.

    PEFT starts every ``lora_B`` matrix at zero, so an adapter whose ``lora_B`` weights are all zero
    behaves exactly like the base model, however cleanly the run finished.

    Raises:
        ValueError: If the file holds no ``lora_B`` weights, so the check cannot be made.
    """
    update_weights = [
        tensor for name, tensor in load_file(adapter_path).items() if "lora_B" in name
    ]
    if not update_weights:
        raise ValueError(f"no lora_B weights in {adapter_path}")
    return any(bool(tensor.any()) for tensor in update_weights)
