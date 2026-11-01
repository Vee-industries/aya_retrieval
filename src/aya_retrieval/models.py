"""The pinned model, loaded only from the local Hugging Face cache."""

from __future__ import annotations

import torch
from huggingface_hub import snapshot_download
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)

MODEL_ID = "CohereLabs/tiny-aya-global"
MODEL_REVISION = "af89d219b53ed9b13b8a4645f9c8028973510324"


def load_model() -> tuple[PreTrainedModel, PreTrainedTokenizerBase]:
    """Return Tiny Aya Global and its tokenizer on the GPU, in bfloat16 and evaluation mode.

    The lookup never touches the network, so a run cannot silently pick up new weights.
    """
    snapshot = snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(snapshot)
    model = AutoModelForCausalLM.from_pretrained(snapshot, dtype=torch.bfloat16, device_map={"": 0})
    model.eval()
    return model, tokenizer
