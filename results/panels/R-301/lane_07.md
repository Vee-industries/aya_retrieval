# Lane 7: Research-standard auditor (round 3)
Verdict: submit after fixes (no blocker; the A5 claim, the control row and the shipped-seed cell are fixed and the appendix pointers all resolve; the rule 20, 21, 28 and 30 gaps carried from round 2 remain, none changes a claim)

Read at 48c6586: ARTICLE in full, ABS, HF in full, STANDARD rules 20, 21, 22, 28, 29, 30. Ran read-only counts on `results/s3/*.json` (fields `right_decision`, `kind`, `item_correct`); did not run `make_article.py`.

## Round-2 findings: status
F1 ("training's gain is when to search") fixed: contribution 2 (line 152 to 154) now says "leaving answers in view and plain statements unsearched"; the "when" row (line 143) gives right decisions. I recounted `right_decision`: 6.37 682, 666, 670; code 714; C1 797, 789, 807; base 201 of 834. All match.
F2 (rule 21 and 20 numbers) not fixed: see new F1.
F3 (candidate total) partly fixed: lines 482 to 484 name every untabled try, Appendix B holds the 24 rows (I counted 24, six with "every line read"). No single total, no cap statement beyond deviation 9.
F4 (row 16 control) fixed: names R-015's two controls and the 419-message memory failure.
F5 (abstract and deviations 13, 15) mostly fixed: the long abstract no longer makes the "registered before they ran" claim; ABS still does (new F5).
F6 (empty shipped-seed cell) fixed: Appendix C shows 60 of 60.
Round-1 items still open: flow tables other than S3's, per-seed recall (new F4), labels (new F3).

## New findings (most severe first)
F1. [MAJOR] ARTICLE 5 (line 316 to 321, 341 to 354) and 6.2 (lines 385 to 401): rules 21 and 20 not met. The 6.2 rows give a sign test p and counts only, with no effect, interval or n of pairs; the hypotheses outcomes ("holds", "met on set 1") are bare; the family line says "a family of exploratory results" with no size, q or adjusted result.
    Evidence: `results/analysis/R-162/A.json` holds the first-test pair counts; `grep -n "family\|adjust" docs/ARTICLE.md` returns lines 320 and 683 only (the latter is unrelated).
    Fix: add the gain, interval and n to the six 6.2 summary lines and hypotheses rows, plus one line with the family size and Benjamini-Hochberg result; or add a deviation row saying they were not computed.
F2. [MINOR] ARTICLE 6.1 line 374 to 377 and Appendix A lines 842 to 859: the "(confirmatory)" heading covers "Seed 82 is above both references (largest p 3.2e-4)". Those references ran late (exploratory, deviation 2). Appendix A repeats the sentence with no label. In Appendix C, "Where recall is lost" (line 957) and `re_ask` (line 951) carry none. Rule 15.
    Fix: add "(exploratory, run late)" to those sentences.
F3. [MINOR] Headline table (lines 57 to 63): the first row mixes confirmatory (6.37 vs base) and exploratory (code, whole chat) cells with no marker. Fix: one label on the baseline column.
F4. [MINOR] ARTICLE 9 and Appendix C: per-seed S3 recall is not given. From the run files: 6.37 seeds 82, 83, 94: 99, 120, 128 of 414; C1: 127, 132, 105. The shipped seed is 6.37's lowest, and the pooled 347 hides a 29-question range. Fix: one line in Appendix C with the six counts.
F5. [MINOR] ABS line 30 ("Both sealed tests and their rules were registered before they ran; S3's scorer was written before any S3 file was read") leaves out that the scorer was written after S3 started (deviation 13). Fix: add "after S3 started".
F6. [MINOR] Rule 30: a flow table exists for S3 only. The first sealed test, outside sets and LongMemEval-S show different denominators (466, 460, 476, 411, 402 in Appendix A) without a reason for each drop. Fix: one sentence each, or a deviation row.
F7. [MINOR] Rule 28: no single count of everything scored on development pools. ABS and the abstract say "24 candidates"; sections 4 and 8 add 40 earlier sets and about 20 named tries. Fix: one total with its cap or cutoff.

## What holds up
- Appendix and section pointers (6.1, 6.2, 6.3, 9, 12) each lead to the table or counts they claim; no sentence is broken where text was cut.
- S3 right-decision, recall (161, 274, 59) and shipped-seed counts recompute from the run files; the 6.37 seed 82 recall of 99 matches.
- Rule 22 headings, the leakage table and deviations 16 to 20 are present and plain; the 24-row ledger count is correct.
