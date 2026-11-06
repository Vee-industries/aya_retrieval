"""Checks on a finished training run."""

from __future__ import annotations

from pathlib import Path

from safetensors.torch import load_file


def adapter_moved(adapter_path: Path) -> bool:
    """Return True if any LoRA update weight left its zero start, so training changed the model.

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


def adapter_changed(adapter_path: Path, start_path: Path) -> bool:
    """Return True if any LoRA weight differs from the adapter the run started from (R-103).

    A run that starts from a saved adapter has non-zero ``lora_B`` weights before it trains, so
    ``adapter_moved`` cannot tell whether it changed anything.
    """
    final, start = load_file(adapter_path), load_file(start_path)
    if set(final) != set(start):
        raise ValueError(f"{adapter_path} and {start_path} name different weights")
    return any(not bool((final[name] == start[name]).all()) for name in final)
