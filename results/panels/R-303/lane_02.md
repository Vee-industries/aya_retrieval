# Lane 2: Statistician and experimental designer (hostile)
Verdict: submit after fixes

Commit 125b902. Scripts (read-only, `results/s3/` only): `...\scratchpad\panel5\l02\recheck_s3.py`, `extra_s3.py`, `round4.py`. Every S3 count, interval and Appendix C split reproduces, as do the new numbers: search decisions 682/666/670, code 714, C1 797/789/807 of 834; 288 of 480, 158 of 260, 59 of 347; 141/22 and 106/29; README's recall intervals.

## Round-3 findings: status
F1 fixed: HF 11-12 "shows no measured difference".
F2 fixed: ARTICLE 427-429, README 303, MODEL_CARD 129-130 now say 22 points and "not powered to show equality".
F3 fixed: ARTICLE 436 "6.37 / base: 37 against 38" matches seed 82 first.
F4 fixed (ARTICLE 453). F5 fixed (ARTICLE 64).
Carried, not fixed and not recorded as declined in `results/panels/R-301/FIXLIST.md`: ARTICLE 135 and HF 33-34 "a sealed test opened once (the first sealed test and S3)"; no line says that rule 1's pooled sign test counts each base row eight times; ARTICLE 602-604 and Appendix C's coherence line do not say the 120 sampled items are C1 seed 82 only (`results/s3/coherence/key.json` holds arms `base` and `pick`; R-286 "C1 seed 82").

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md:71-72 and ARTICLE.md:154, "Grounds": "288 of 480 (60.0%) ... right, as often as base reading code's passages, 158 of 260 (60.8%)". "As often as" claims equality with no test (chat-resampled interval of the difference -11.2 to +9.1 points). The two rates are also over different questions, chosen by each arm's own search. On the questions both searches found, base on code's passages is right more often: seed 82 65 of 119 against code 84 (28 right only for code, 9 only for seed 82, sign test p = 0.0026); seeds 83 and 94 p = 0.096 and 0.89.
    Evidence: `round4.py results/s3`.
    Fix: "60.0% against 60.8%, over different questions; on the 119 questions both found, seed 82 65 and code 84 (p = 0.0026, exploratory)".
F2. [MINOR] HF_ARTICLE.md:47-48 defines "no measured difference" as "the 95% interval of the difference includes zero", but the outside-writer (p = 0.76, 0.45) and LongMemEval H2 (p = 0.2) uses rest on sign tests with no interval.
    Fix: "includes zero, or a sign test gives p of 0.05 or more".
F3. [MINOR] ARTICLE.md:438-439, tag questions "1 and 3 of 20 ... about as often as base" (base 1 and 0): equality on n = 20 with no test.
    Fix: "base 1 and 0; too few to compare".
F4. [MINOR] MODEL_CARD_C1.md:51-52, "This adapter, seed 82, is under base on that line": the gap is -1.3 points, 95% interval -5.9 to +3.4 (`recheck_s3.py`). This is the same size of gap the papers call unresolved when C1 is above base.
    Fix: add the interval.

## What holds up
All S3 rule lines and Appendix C counts reproduce from the 15 run files. The first sealed test's pooled range (85.2 to 90.4%) matches ARTICLE 378-381.
LongMemEval arithmetic is consistent (19-question lead: 8 answerable, 11 unanswerable).

Not checked: LongMemEval-S files (closed), the 372 against 333 of 476 and 63 against 51 of 411, figure intervals.
