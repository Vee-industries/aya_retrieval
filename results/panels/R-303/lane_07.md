# Lane 7: Research-standard auditor (round 4)
Verdict: submit after fixes (no blocker, no wrong count; rules 20, 21, 28 and 30 are still unmet but now disclosed in deviations 21 and 22; two minor labelling and figure gaps remain)

Read at 125b902: ARTICLE sections 1 to 15 and Appendices A to C, ABSTRACT line 34, STANDARD rules 2, 3, 4, 8, 9, 13, 15, 16, 18 to 22, 26, 29, 30, 38. Recomputed from `results/s3/*.json`: recall by seed, shipped-seed statement, N-hit and "other stored facts" counts (the R-298 function's logic). Did not run `make_article.py`; no network.

## Round-3 findings: status
F1 (rules 20, 21 numbers) partly fixed: deviation 21 (line 699) now says effect, interval, n on 6.2 rows and the hypotheses table, and the family size and adjusted result, were not computed. The numbers are still absent; the gap is disclosed, not closed.
F2 (labels on seed-82-vs-references sentence) fixed: lines 390 and 913 say "exploratory, run late".
F3 (headline table label) fixed: column header line 61 says "exploratory; ... run late".
F4 (per-seed S3 recall) fixed: Appendix C line 1007; I recounted 99, 120, 128 and 127, 132, 105.
F5 (ABS "registered before they ran") fixed: ABSTRACT.md line 34 says "after S3 started".
F6 (flow tables) partly fixed: deviation 22 discloses that only S3 has one; S3's table sums (476 right view plus 358 wrong view = 834).
F7 (single total of tries) partly fixed: deviation 22 discloses; the 40 is derivable from the 7b71a20 ledger (16 + 21 + 3), commit is on origin/main.

## New findings (most severe first)
F1. [MINOR] ARTICLE sections 7, 8, 10 (lines 459 to 560, 628 to 670): rule 38. Claims with no label: "6.37 answered 2 of its 4 questions", "repeated its own wrong answer on 6 of 8" (line 465), "C1 ... passed all 20 screening lines" (line 556), K1 and K1.3 on Demo2. By the article's own definition (line 135) these are exploratory.
    Evidence: label lines found by `grep -n -o -i "confirmatory\|exploratory"`: none between 459 and 525.
    Fix: one sentence under sections 7 and 8: "Every result in sections 7 and 8 is exploratory (development sets and demos), except S3's rule."
F2. [MINOR] Figures 1 and 2 (lines 385 to 387, 421 to 423): rule 9 asks every results figure to show uncertainty. Both captions say "no interval". Not covered by deviation 21.
    Evidence: captions; `make_figures.py` line 208 says "point counts, no intervals".
    Fix: add Wilson intervals as Figure 8 has, or add "figures 1 and 2" to deviation 21.
F3. [MINOR] Deviation 16 / rule 3: the rule allows a missing control only where the pre-registration says why and Kevin's quoted word allows it. The row gives a reason written afterwards and no quoted word.
    Evidence: lines 694 and 702 to 704.
    Fix: add the quoted word or the record that allows it, or say none exists.

## What holds up
- All appendix and section pointers resolve to what they name (6.1, 6.2, 6.3, 9, Appendices A to C); no sentence is broken where text was cut.
- Recomputed and matching: S3 recall 99/120/128 and 127/132/105; C1 seed 82 statement 50 of 60; N-hit flags 286, 51, 100, 11 and "other stored" counts 402/708, 99/708, 25/236, 17/236, 32/472, 37/472; Appendix A seed 82 miss counts (28, 29, 19, 20).
- Rule 22 headings (including who judged), rule 18 leakage table, rule 26 tables (22 deviations) and rule 29 baseline rows are present and plain.
