"""Dial adapters change each weight by exactly the scaled or blended amount."""

import importlib.util
from pathlib import Path

import torch

SPEC = importlib.util.spec_from_file_location(
    "make_dial_adapter", Path(__file__).parents[1] / "scripts" / "make_dial_adapter.py"
)
dial = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(dial)

A, B = "m.lora_A.weight", "m.lora_B.weight"


def adapter(seed):
    gen = torch.Generator().manual_seed(seed)
    return {A: torch.randn(4, 6, generator=gen), B: torch.randn(5, 4, generator=gen)}


def delta(tensors):
    return tensors[B] @ tensors[A]


def test_scaling_scales_the_change():
    one = adapter(1)
    assert torch.allclose(delta(dial.scaled(one, 0.7)), 0.7 * delta(one))


def test_a_mix_is_the_exact_blend_of_the_two_changes():
    one, two = adapter(1), adapter(2)
    for a in (0.0, 0.3, 1.0):
        blend = a * delta(one) + (1 - a) * delta(two)
        out = dial.mixed(one, two, a)
        assert out[A].shape == (8, 6) and out[B].shape == (5, 8)
        assert torch.allclose(delta(out), blend, atol=1e-5)
