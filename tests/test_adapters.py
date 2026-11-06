"""A step must start exactly from its parent's saved adapter, and refuse one that does not fit."""

import pytest
import torch
from peft import LoraConfig, get_peft_model
from transformers import LlamaConfig, LlamaForCausalLM

from aya_retrieval.adapters import load_lora_weights


def _model(r=4, targets=("q_proj", "v_proj")):
    torch.manual_seed(0)
    config = LlamaConfig(
        vocab_size=32,
        hidden_size=16,
        intermediate_size=32,
        num_hidden_layers=1,
        num_attention_heads=2,
        num_key_value_heads=2,
    )
    lora = LoraConfig(r=r, lora_alpha=2 * r, target_modules=list(targets), task_type="CAUSAL_LM")
    return get_peft_model(LlamaForCausalLM(config), lora)


def _trained(tmp_path):
    parent = _model()
    with torch.no_grad():
        for name, weight in parent.named_parameters():
            if "lora_B" in name:
                weight.fill_(0.5)
    parent.save_pretrained(str(tmp_path))
    return parent


def test_a_fresh_model_starts_from_the_saved_weights(tmp_path):
    parent = _trained(tmp_path)
    child = _model()
    assert load_lora_weights(child, tmp_path) == 4
    for (name, a), (_, b) in zip(parent.named_parameters(), child.named_parameters(), strict=True):
        if "lora_" in name:
            assert torch.equal(a, b)


def test_a_different_rank_is_refused(tmp_path):
    _trained(tmp_path)
    with pytest.raises(ValueError, match="configuration"):
        load_lora_weights(_model(r=8), tmp_path)


def test_different_target_modules_are_refused(tmp_path):
    _trained(tmp_path)
    with pytest.raises(ValueError, match="configuration"):
        load_lora_weights(_model(targets=("q_proj", "k_proj")), tmp_path)
