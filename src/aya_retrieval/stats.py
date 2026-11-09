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


def wilson_interval(hits: int, total: int, z: float = 1.96) -> tuple[float, float]:
    """95% Wilson score interval for a proportion, as fractions."""
    if total == 0:
        return 0.0, 1.0
    p = hits / total
    centre = (p + z * z / (2 * total)) / (1 + z * z / total)
    half = z * ((p * (1 - p) / total + z * z / (4 * total * total)) ** 0.5) / (1 + z * z / total)
    return max(0.0, centre - half), min(1.0, centre + half)


def bootstrap_gain_interval(
    base: list[int],
    adapters: list[list[int]],
    n_resamples: int = 10_000,
    seed: int = 0,
    clusters: list[int] | None = None,
) -> dict:
    """95% percentile intervals for the adapters' gain over base, resampling conversations.

    ``base[i]`` and ``adapters[s][i]`` score the same conversation ``i`` (1 right, 0 wrong). Each
    resample draws conversations with replacement and keeps every model's answer on them, so the
    pairing holds. With ``clusters`` (a group id per conversation, such as its fact template), each
    resample draws whole groups instead, because conversations in one group are not independent
    (R-139); without it the draws are the same as before. Returned: the difference in rates
    (adapters pooled minus base) and the relative gain (adapters pooled over base, minus one), each
    with its observed value and interval.
    """
    n = len(base)
    if n < 2 or any(len(a) != n for a in adapters):
        raise ValueError("need at least 2 conversations, scored by every model")
    if clusters is not None and len(clusters) != n:
        raise ValueError("need one cluster id per conversation")
    groups: dict[int, list[int]] = {}
    for i, group in enumerate(clusters if clusters is not None else range(n)):
        groups.setdefault(group, []).append(i)
    members = list(groups.values())
    if len(members) < 2:
        raise ValueError("need at least 2 clusters")

    def rates(idx: list[int]) -> tuple[float, float]:
        b = sum(base[i] for i in idx) / len(idx)
        t = sum(a[i] for a in adapters for i in idx) / (len(idx) * len(adapters))
        return b, t

    rng = random.Random(seed)
    diffs, gains = [], []
    for _ in range(n_resamples):
        b, t = rates([i for _ in members for i in members[rng.randrange(len(members))]])
        diffs.append(t - b)
        gains.append(t / b - 1 if b else float("inf"))
    diffs.sort()
    gains.sort()
    lo, hi = int(0.025 * n_resamples), int(0.975 * n_resamples) - 1
    b, t = rates(list(range(n)))
    return {
        "difference": (t - b, diffs[lo], diffs[hi]),
        "relative_gain": (t / b - 1 if b else float("inf"), gains[lo], gains[hi]),
    }
