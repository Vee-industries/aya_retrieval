import pytest
from auditkit._bootstrap import paired_bootstrap as auditkit_paired_bootstrap

from aya_retrieval.stats import exact_sign_test, paired_bootstrap


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
