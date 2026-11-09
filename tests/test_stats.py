import pytest
from auditkit._bootstrap import paired_bootstrap as auditkit_paired_bootstrap

from aya_retrieval.stats import (
    bootstrap_gain_interval,
    exact_sign_test,
    paired_bootstrap,
    wilson_interval,
)


def test_the_sign_test_matches_known_binomial_values():
    assert exact_sign_test(0, 0) == 1.0
    assert exact_sign_test(5, 5) == 1.0
    assert exact_sign_test(0, 10) == pytest.approx(2 / 2**10)
    assert exact_sign_test(2, 8) == pytest.approx(2 * (1 + 10 + 45) / 2**10)


def test_the_bootstrap_finds_a_clear_gain_and_no_gain_where_there_is_none():
    gain = paired_bootstrap([(0.0, 1.0)] * 30 + [(1.0, 1.0)] * 70, n_resamples=2000)
    assert gain["delta"] == pytest.approx(0.3)
    assert gain["p_value"] < 0.001
    same = paired_bootstrap(
        [(0.0, 1.0)] * 20 + [(1.0, 0.0)] * 20 + [(1.0, 1.0)] * 60, n_resamples=2000
    )
    assert same["p_value"] > 0.9


def test_auditkit_bootstrap_defect_is_still_present():
    """AuditKIT 1.1.3 does not centre its resamples, so a gain on every pair reads as p = 1.

    When this fails, AuditKIT has fixed it, and R-031's note about it needs updating.
    """
    assert auditkit_paired_bootstrap([(0.0, 1.0)] * 100)["p_value"] == 1.0


def test_the_wilson_interval_matches_a_published_value():
    low, high = wilson_interval(81, 263)  # Newcombe (1998), table I: 0.2553 to 0.3662
    assert low == pytest.approx(0.2553, abs=5e-4)
    assert high == pytest.approx(0.3662, abs=5e-4)
    assert wilson_interval(0, 10)[0] == 0.0


def test_the_gain_interval_brackets_the_observed_gain_and_excludes_zero_for_a_clear_one():
    base = [1] * 30 + [0] * 70
    adapters = [[1] * 80 + [0] * 20, [1] * 75 + [0] * 25]
    result = bootstrap_gain_interval(base, adapters, n_resamples=2000)
    observed, low, high = result["difference"]
    assert observed == pytest.approx(0.475)
    assert low < observed < high and low > 0
    gain, g_low, g_high = result["relative_gain"]
    assert gain == pytest.approx(0.775 / 0.3 - 1)
    assert g_low < gain < g_high


def test_the_gain_interval_without_clusters_is_unchanged_by_the_clusters_option():
    base = [1] * 30 + [0] * 70
    adapters = [[1] * 80 + [0] * 20]
    singletons = bootstrap_gain_interval(base, adapters, n_resamples=500, clusters=list(range(100)))
    assert singletons == bootstrap_gain_interval(base, adapters, n_resamples=500)


def test_clustered_resampling_widens_the_interval_when_groups_move_together():
    # Ten groups of ten: within a group every conversation has the same outcome, so there are
    # only ten independent units and the interval must be wider than the per-conversation one.
    base = [0] * 100
    adapters = [[1 if group % 2 else 0 for group in range(10) for _ in range(10)]]
    clusters = [group for group in range(10) for _ in range(10)]
    _, low, high = bootstrap_gain_interval(base, adapters, n_resamples=2000)["difference"]
    _, c_low, c_high = bootstrap_gain_interval(base, adapters, n_resamples=2000, clusters=clusters)[
        "difference"
    ]
    assert c_high - c_low > 2 * (high - low)


def test_the_gain_interval_spans_zero_when_there_is_no_gain():
    base = [1, 0] * 50
    adapters = [[0, 1] * 50]
    _, low, high = bootstrap_gain_interval(base, adapters, n_resamples=2000)["difference"]
    assert low < 0 < high
