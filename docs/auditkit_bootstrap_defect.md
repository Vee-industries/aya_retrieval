# AuditKIT: `paired_bootstrap` does not centre its resamples

Found while building this project's AuditKIT evaluation (RECORDS R-031). Reported to Lexsi in the
hackathon submission, not posted publicly.

## Summary

`auditkit._bootstrap.paired_bootstrap` (1.1.3, commit `71316da`) never centres the resampled
differences under the null hypothesis of no difference. Every resampled mean sits around the observed
mean, so roughly half of them come out at least as large as it. Any real effect therefore reads as
p ≈ 0.5, and a gain on every pair reads as p = 1.0.

The function is shared by `ModelComparison.significance` (`model_compare.py:108`),
`ComparisonResult.significance` (`comparison.py:280`) and `Experiment.significance` (`experiment.py:99`),
so all three are affected.

## Reproduce

```python
from auditkit._bootstrap import paired_bootstrap

paired_bootstrap([(0.0, 1.0)] * 100)  # every pair improves
# {'delta': 1.0, 'p_value': 1.0, 'significant': False}

paired_bootstrap([(0.0, 1.0)] * 50 + [(1.0, 1.0)] * 50)  # half improve, none get worse
# {'delta': 0.5, 'p_value': 0.532468, 'significant': False}
```

On this project's data it reported p = 0.52 for 57% → 88% accuracy over 240 paired cases, where an
exact sign test on the discordant pairs gives p ≈ 6e-16.

## Cause

`_bootstrap.py`, line 67:

```python
if abs(sum(resample) / n) >= abs(observed):
```

This compares resampled means drawn around the observed mean with the observed mean itself. For a
test of "no difference", the resampled means should be shifted by the observed mean first.

## Suggested fix

```python
if abs(sum(resample) / n - observed) >= abs(observed):
```

With that one change, using the same seed and resample count:

| Pairs | Now | With the fix |
|---|---|---|
| 100 of 100 improve | 1.0 | 0.001 |
| 50 improve, 50 the same | 0.53 | 0.001 |
| no change | 1.0 | 1.0 |
| 20 improve, 20 get worse, 60 the same | not run | 1.0 |

A regression test with a known large effect, asserting p < 0.05, would catch this in future. This
project's `tests/test_stats.py` pins the defect, and `aya_retrieval.stats` holds the replacement used
here: an exact sign test and a centred paired bootstrap.
