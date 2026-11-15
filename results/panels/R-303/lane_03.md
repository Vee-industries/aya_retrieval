# Lane 3: Evaluation and leakage specialist (hostile)
Verdict: submit after fixes

## Round-3 findings: status (one line each)
F1 fixed: ARTICLE.md:328, 724, 751-754 and HF_ARTICLE.md:197-199 name both markers (R-144, R-145).
F2 fixed: ARTICLE.md:730-731 and HF_ARTICLE.md:191 call 6.37's and C1's plain never-told rates ceilings.
F3 fixed: ARTICLE.md:732 "(counts for N-hit questions in Appendix C)".
F4 fixed: ARTICLE.md:266 cites R-003.
F5 fixed: README.md:89 and 402 "of wrong-view questions".

## New findings (most severe first)
F1. [MAJOR] ARTICLE.md:125, 210, 266 (leakage table, "Illegitimate features"); HF_ARTICLE.md:42: half of the `confirm` items put the right value in the question, so a reply that agrees is scored right with no memory. This is not disclosed for S3. On S3, 30 of 58 `confirm` items are true claims, and every one holds the answer string in the message (`older`: 0 of 356). Of base with the tool's 59 right recall answers, 28 are agreements with a true claim, 27 of them with no search. `older` alone: base 30/356, code 141/356, whole chat 253/356, 6.37 285/1,068, C1 292/1,068. Excluding the true claims flips no verdict, but the reported "recall" is partly agreement. S3's items are also "..., right?" tag questions, not "did I tell you...?".
    Evidence: `panel5/l03/confirm.py` on `results/s3/*.json` (fields `claim`, `answer`, `message`); `src/aya_retrieval/scoring.py:61`; the record has the point for the outside sets (RECORDS.md:5898, 6178; README.md:431).
    Fix: add the row to the leakage table and one sentence to section 12 with the counts above; define `confirm` as tag questions, half true claims.

F2. [MAJOR] ARTICLE.md section 9; HF_ARTICLE.md section 6: S3's false-claim result is missing, and it bears on the safety claim about not copying a wrong answer. 6.37 corrects 0 of 84 false claims (shipped seed 82: 0 of 28); base 1 of 28, code 11 of 28, whole chat 4 of 28, C1 32 of 84, K1 1 of 56, K2.1 4 of 56. Only the outside sets' 1 and 3 of 20 are reported (ARTICLE.md:439).
    Evidence: same script, `claim == "false"` rows.
    Fix: one line in section 9 and in the short paper's S3 table.

F3. [MINOR] ARTICLE.md:153: "59 of 347 of its right answers are on rows marked not found" reads as an instrument doubt. All 59 are agreements with a true claim made with no search.
    Fix: add "(all 59 agree with a true claim, no search)".

F4. [MINOR, carried from round 2] The rule is "names no listed value" but these places say "declined" or "declines": ARTICLE.md:342, 525 and 537 (Figure 4 caption), and the figure's y-axis (`scripts/make_figures.py:515`, which counts `correct`). MODEL_CARD.md:75 and 142 and README.md:316 say "never told" without the rule.
    Fix: "names no listed value" in each place.

F5. [MINOR, carried] ARTICLE.md:260, 741: the overlap count with the training text is given for 6.37 only. C1's set (K1.3 plus OP) has no count, and R-206's removal of six-word runs is not stated.
    Fix: give C1's count, or say it was not counted.

## What holds up
- Rerun on the run files: 6.37 searched on 7, 0 and 5 of 58 `confirm` items; right decisions 682, 666 and 670 (code 714; C1 797, 789 and 807) of 834.
- Every S3 count in the "every arm" table and the shipped-seed table matches.
- Not checked: 402 of 708 "other stored facts". It needs `data/heldout3`, which is out of bounds.
