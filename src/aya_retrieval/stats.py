"""Significance tests on paired outcomes: base and adapter on the same conversations."""

from __future__ import annotations

import random
from math import comb


def exact_sign_test(only_base: int, only_adapter: int) -> float:
    """Two-sided exact sign test on the discordant pairs; the test R-016 registered.

    Args:
        only_base: Conversations base got right and the adapter got wrong.
        only_adapter: Conversations the adapter got right and base got wrong.
    """
    n = only_base + only_adapter
    if n == 0:
        return 1.0
    tail = sum(comb(n, k) for k in range(min(only_base, only_adapter) + 1)) / 2**n
    return min(1.0, 2 * tail)


def paired_bootstrap(
    pairs: list[tuple[float, float]], n_resamples: int = 10_000, seed: int = 0
) -> dict:
    """Two-sided paired bootstrap of the mean difference, centred under no difference.

    The resampled means are shifted by the observed mean, so they show how far chance alone moves
    the mean; the p-value is the share of them at least as far from zero as the observed mean.
    """
    n = len(pairs)
    if n < 2:
        raise ValueError("need at least 2 pairs")
    diffs = [adapter - base for base, adapter in pairs]
    observed = sum(diffs) / n
    rng = random.Random(seed)
    extreme = sum(
        abs(sum(rng.choice(diffs) for _ in range(n)) / n - observed) >= abs(observed)
        for _ in range(n_resamples)
    )
    return {
        "n": n,
        "mean_base": sum(b for b, _ in pairs) / n,
        "mean_adapter": sum(a for _, a in pairs) / n,
        "delta": observed,
        "p_value": (extreme + 1) / (n_resamples + 1),
    }
