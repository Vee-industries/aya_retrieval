"""A lower-memory version of TRL's chunked cross-entropy, with the same arithmetic.

TRL's ``_chunk`` computes ``h.float() @ w.float().t()``. Under bf16 autocast, which training uses,
autocast casts both float32 copies back to bf16 before the product, so the result is the bf16
product of the original tensors, but the copies are still made: for Tiny Aya's 262,144 x 2,048
output layer that is 2 GiB in float32 plus 1 GiB in bf16 for every chunk of tokens, which pushes
training past a 10 GiB card. Here, when the tensors already have autocast's dtype, the product is
taken directly, which gives the same values without the copies. Outside autocast it is TRL's code.
"""

from __future__ import annotations

import torch
import torch.nn.functional as F
import trl.trainer.sft_trainer as sft_trainer

LOSS_CHUNK_TOKENS = 128
TRL_CHUNK = sft_trainer._chunk


def output_logits(h: torch.Tensor, w: torch.Tensor) -> torch.Tensor:
    """Return what ``h.float() @ w.float().t()`` returns, without float32 copies under autocast."""
    device = h.device.type
    if torch.is_autocast_enabled(device) and h.dtype == w.dtype == torch.get_autocast_dtype(device):
        return h @ w.t()
    return h.float() @ w.float().t()


def lean_chunk(h, w, b, lbl, logit_scale, final_logit_softcapping):
    """TRL's ``_chunk`` with ``output_logits`` in place of its float32 product."""
    logits = output_logits(h, w)
    if b is not None:
        logits = logits + b.float()
    if logit_scale != 1.0:
        logits = logits * logit_scale
    if final_logit_softcapping is not None:
        logits = final_logit_softcapping * torch.tanh(logits / final_logit_softcapping)
    log_p = F.log_softmax(logits, dim=-1)
    chunk_loss = F.nll_loss(log_p, lbl, reduction="sum")
    chunk_correct = (logits.argmax(dim=-1) == lbl).sum().float()
    chunk_entropy = -(log_p.exp() * log_p).sum(dim=-1).sum()
    return chunk_loss, chunk_correct, chunk_entropy


def use_lean_loss() -> dict:
    """Swap TRL's loss chunk for the lean one and shorten its chunks; return what was set."""
    sft_trainer._chunk = lean_chunk
    sft_trainer._CHUNKED_LM_HEAD_CHUNK_SIZE = LOSS_CHUNK_TOKENS
    return {"loss": "lean_loss.lean_chunk", "loss_chunk_tokens": LOSS_CHUNK_TOKENS}
