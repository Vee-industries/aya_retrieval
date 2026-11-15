# R-313: final editorial check of 6c9b656 (reviewer's report, as returned)

One fresh Opus reviewer agent, read only, brief from the orchestrator: an outside reviewer's final checklist (five
required checks, five editorial checks) and the R-309 and R-311 fixes. Its harness refused a report file, so the report
came back as text; this is it, with S = `docs/submission/HF_ARTICLE.md`, L = `docs/ARTICLE.md`, MC = `docs/MODEL_CARD.md`,
line numbers of the built files at 6c9b656.

## Checklist

| Check | Verdict | Where |
|---|---|---|
| 1. C1 against base | PASS | S 16-17, 175, 187; L 615-618; MC 59-60 (7.2% and 5.9%, 1.3 points, -3.1 to +5.7; nothing calls C1 statistically worse) |
| 2. S3 scoring limits | PASS (see M2) | S 26, S 210-212, S 188-189 (wider count, exploratory, R-298) |
| 3. Retrieval and grounding | PASS | S 75-79, 196-202; L 161-172, 1081-1093 (search comparison; 119 questions, 65 against 84, p = 0.0026) |
| 4. Report arms | PASS | S 202-205, 227; L 661-665, 834-841 |
| 5. Shipping decision | PASS | S 17-18, 190-191; L 616, 671-672 |
| Numbers sourced in L | PASS | every number in S found in L by script; spot checks in context |
| Labels kept | FAIL | S 195 (M1) |
| No-difference not made equivalence | PASS (see L6) | S 13, 30, 34, 127 |
| Disclosures and chronology | PASS | S 51-53, 155-161, 213-218, 236-239; L 587-589 |
| No real-world reliability claim | PASS | S 221-222 |

## Findings

- **M1.** S 195: S3's strongest baselines sit under section 6's "(confirmatory)" heading with no label; L 649 labels the
  same numbers exploratory. Older than R-309. Fix: "On S3 (exploratory, beside the rule, not part of it), ...".
- **M2.** R-311's L3 fix reached the term lines only; S 210, S 175 (row label) and L 783 name only the asked category,
  and L 140 "an invented value passes unseen" while a writer's listed wrong value is caught. Fix S 210-211, L 783,
  L 140 to name both sets.
- **L1.** The changelog (L 916-917) and stage tables (L 208, S 96) stop at R-309; "the whole chat at 419 messages named
  only where it ran" is unclear.
- **L2.** L 180-181 "so statements measure no gain over it" is unclear; code is 0 of 60 by construction.
- **L3.** L 592 "to pass" names no clause; only (c) is shown for a report arm.
- **L4.** L 669 "no measured change in recall": the defined term is "no measured difference".
- **L5.** L 836 and L 840 both say query writing is the likeliest cause; a repeat left by R-309's trim.
- **L6.** S 127, L 482 "6.37 ties code": equal counts after a post-result split; "ties" can read as shown equal.

Checked and right: section 9's paragraph against `ship_rule.json` (10 counts); `older` alone and N-hit counts
recomputed from `results/s3/`; the model card's R-311 fix against L 961-969; R-311's L2 wording; the added lines' voice.
Not checked: the LongMemEval-S split against its run files (not opened), the scorer's code.
