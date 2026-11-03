import contextlib

import pytest
import torch
import trl.trainer.sft_trainer as sft_trainer

from aya_retrieval.lean_loss import TRL_CHUNK, lean_chunk, use_lean_loss


def chunk_and_grads(chunk, h, w, lbl):
    h = h.clone().requires_grad_(True)
    w = w.clone().requires_grad_(True)
    loss, correct, entropy = chunk(h, w, None, lbl, 1.0, None)
    loss.backward()
    return loss, correct, entropy, h.grad, w.grad


@pytest.mark.parametrize(
    "dtype, autocast",
    [
        (torch.float32, False),
        (torch.bfloat16, False),
        (torch.bfloat16, True),
        (torch.float32, True),
    ],
)
def test_the_lean_chunk_gives_trl_values_exactly(dtype, autocast):
    gen = torch.Generator().manual_seed(0)
    h = torch.randn(5, 16, generator=gen).to(dtype)
    w = torch.randn(30, 16, generator=gen).to(dtype)
    lbl = torch.randint(0, 30, (5,), generator=gen)
    ctx = torch.autocast("cpu", dtype=torch.bfloat16) if autocast else contextlib.nullcontext()
    with ctx:
        ours = chunk_and_grads(lean_chunk, h, w, lbl)
    with ctx:
        theirs = chunk_and_grads(TRL_CHUNK, h, w, lbl)
    for a, b in zip(ours, theirs, strict=True):
        torch.testing.assert_close(a, b, rtol=0, atol=0)


def test_use_lean_loss_swaps_trl_chunk(monkeypatch):
    monkeypatch.setattr(sft_trainer, "_chunk", TRL_CHUNK)
    monkeypatch.setattr(sft_trainer, "_CHUNKED_LM_HEAD_CHUNK_SIZE", 256)
    settings = use_lean_loss()
    assert sft_trainer._chunk is lean_chunk
    assert sft_trainer._CHUNKED_LM_HEAD_CHUNK_SIZE == settings["loss_chunk_tokens"]
