"""An adapter that never left its zero start must fail the training check."""

import pytest
import torch
from safetensors.torch import save_file

from aya_retrieval.training_checks import adapter_moved


def _adapter(tmp_path, **tensors):
    path = tmp_path / "adapter_model.safetensors"
    save_file(tensors, path)
    return path


def test_an_untrained_adapter_did_not_move(tmp_path):
    path = _adapter(tmp_path, lora_A=torch.ones(2, 2), lora_B=torch.zeros(2, 2))
    assert not adapter_moved(path)


def test_one_changed_update_weight_counts_as_moved(tmp_path):
    update = torch.zeros(2, 2)
    update[0, 1] = 1e-6
    assert adapter_moved(_adapter(tmp_path, lora_B=update))


def test_a_file_with_no_update_weights_is_an_error(tmp_path):
    with pytest.raises(ValueError, match="lora_B"):
        adapter_moved(_adapter(tmp_path, lora_A=torch.ones(2, 2)))
