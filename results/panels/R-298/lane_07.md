# Lane 7: Research-standard auditor (round 2)
Verdict: submit after fixes (no blocker; R-297 applied the leakage, deviation, limits and S3 per-seed fixes, but the rule 21, 20, 13/28 and 3 items from the R-295 synthesis group C are still missing, and one claim is stronger than the S3 data)

Paths: ARTICLE = docs/ARTICLE.md, HF = docs/submission/HF_ARTICLE.md, ABS = docs/submission/ABSTRACT.md. I read all three in full at commit 8735c87, STANDARD rules 2, 3, 13, 15, 16, 18 to 22, 26, 28 to 30 and 38, and ran read-only scoring code (`score_s3.load`, `by_chat`, `MEASURES`) on `results/s3/*.json`. Not run: `make_article.py` (writes into the repository), so I did not check the committed text against a fresh build.

## Round-1 findings: status
F1 (S3 pooled, no per seed) partly fixed: ARTICLE 9 now gives N-hit by seed (C1 11, 29, 11; 6.37 100, 79, 107 of 236) and a shipped-seed table (6.37 seed 82 99 of 414, 62 of 298, 100 of 236; C1 seed 82 50 of 60 statements). Still missing: per-seed recall (6.37 99, 120, 128; C1 127, 132, 105 of 414, from the run files) and no sentence that seeds 82, 83, 94 are the screening seeds, not fresh (rule 16).
F2 (controls) partly fixed: deviation row 16 states no control arm ran. See new F4 for what the row leaves out.
F3 (rule 21 numbers) not fixed: 6.2 rows still give a sign-test p only; no effect, interval, or pair count; hypotheses-table outcomes still bare; 6.1 still has no p. `results/analysis/R-162/A.json` holds the pair counts and p (25 and 604, p = 3.4e-145) and they are not in the article.
F4 (leakage, contamination) partly fixed: contamination row now names LongMemEval-S as predating the model and not probed; non-independence, illegitimate-features and demo rows added. No probe run; no duplicate-hash row for `heldout`, `independent` or the outside sets.
F5 (baselines) partly fixed: limits (ARTICLE 12, HF 7) now say one setting each against 40 trained sets and name the untested gated baselines. No budget column; ARTICLE 6.2 line 444 and contribution 2 (line 147) still say "training's gain is when to search" (new F1).
F6 (flow tables) partly fixed: N-hit is now defined as an item property, 236 of 240. Still no flow table for the training set, the first sealed test, the outside sets or LongMemEval-S (denominators 466, 460, 476, 411, 402 ... 497 of 500 unexplained); the 4 never-told items without a fixed-search passage are not accounted for.
F7 (labels) partly fixed: abstract, section 9 baselines and report arms are labelled. Still unlabelled: the headline table rows (the code column is exploratory next to confirmatory cells), the 6.1 late-references table and "Seed 82 is far above both references (largest p 3.2e-4)" (line 405) under the "(confirmatory)" heading, and "Where recall is lost" (line 696).
F8 (family size) not fixed: line 312 is unchanged ("reported unadjusted, as a family of exploratory results"); no family size, q or adjusted result.
F9 (candidate total) not fixed: ARTICLE lists 24 rows plus about 20 named further tries (line 571 to 573: K2, K1.1, K1.2, K3, K3.1, K4, K5, K3.2, T2 to T6, lever 2, R2a, R2b, R2d, two blend grids, C0) and 40 earlier sets; no total, and ABS says "Of 24 candidates".
F10 (deviation rows) mostly fixed: rows 16 to 19 added. Rows 3, 9, 10 still give "not computed" or "my decision" as reason; the hypotheses row "LongMemEval-S H1 to H3" (line 343) still does not state H1 to H3.
F11 (as well as) mostly fixed: "no measured difference" in abstract and 6.2. ARTICLE 9 still says code and whole chat recall "above" 6.37 and C1 with no test.
F12 (judge agreement) not fixed: pairwise agreement is still development-only (R-128, 13 of 576); no over-decline count for C1 on answerable S3 items.
F13 (captions) partly fixed: Figures 5 and 7 explain the report arms. Figures 1, 6, 7 still lack n or seeds; output is SVG and PNG, not PDF.
F14 (short paper) partly fixed: threat model, limits, labels on four headings added; its limits are one bullet list, its tables are bare counts, as the author chose for a 5-page paper.

## New findings (most severe first)
F1. [MAJOR] ARTICLE 1 contribution 2 (line 147), 6.2 line 444, HF 3 (line 123 to 125): "training's gain is when to search" is stronger than S3's own measure of it. The article defines "right search decisions" as the measure of clause "when" (line 137, 322) but never reports the number. From `results/s3` (`right_decision` field, 834 items a run): code 714 of 834 (85.6%); 6.37 682, 666, 670 (80.7% pooled, 2,018 of 2,502); C1 797, 789, 807 (95.6%); base with tool 201 (24.1%). So 6.37's total is below always-searching code. R-295 synthesis item A5 required this sentence; the "when" row (line 137) still lacks it.
    Evidence: `s3_always_search.json`, `s3_fix17cs37_82/83/94.json`, `s3_k13opc1_r263_*.json`, field `right_decision`.
    Fix: put the four rates in the "when" row and section 9; reword the claim to "on in-view and statement items".
F2. [MAJOR] ARTICLE 5, 11 row 16 and the hypotheses table: rule 21 and rule 20 numbers still absent (see F3, F8 above). One decision needed: add effect, interval, n and p to the 6.2 and hypotheses rows from A.json and the run files, and one line with family size, q and adjusted outcome, or add a deviation row saying these were not done.
F3. [MAJOR] ARTICLE abstract and sections 8, 12, ABS line 24, HF 5, 7: no single count of candidates scored on development pools (rule 13, 28). "Of 24 candidates" in ABS and the abstract understates the reopened search by roughly 20 further named tries.
    Fix: state one total, and the cap or cutoff it was measured against.
F4. [MINOR] ARTICLE 11 row 16: "Registered: a negative and a positive control" is not what R-016 registered; R-015 registered a `three_exchanges` control (at most 10% on `older`) and a `whole_chat` control (at least 50%), and R-014 and R-017 show whole chat at 419 failing it (1 of 20, 1 of 20, 0 of 12, peaks 11.22 and 11.62 GiB). The article gives only the memory-cap reason (R-166) and says (line 839) the whole chat at 419 "is not measured".
    Fix: one sentence in row 16 naming the R-015 controls and the failed 419 control.
F5. [MINOR] ABS line 30 and ARTICLE abstract: "Both sealed tests and their rules were registered before they ran" does not mention deviations 13 and 15 (S3's scorer and the coherence reading were fixed after S3 started, before any file was read). Fix: add "(section 11, rows 13, 15)".
F6. [MINOR] ARTICLE 9, "Shipped seed alone" table: the 6.37 cell for the plain-statement row is empty (6.37 seed 82 is 60 of 60 from the run file). Fix: fill it.

## What holds up
- Every S3 count I recomputed from the run files matches both papers: recall 347 and 364 of 1,242; copies 195 and 5 of 894; N-hit 286 and 51 of 708; per-seed N-hit 100, 79, 107 and 11, 29, 11; K1, K1.3, K2.1 sums 12, 37, 14 of 472; confirm searches 7, 0, 5 (6.37) and 52, 37, 52 (C1).
- 6.1 and the abstract's first-sealed-test numbers (91 to 107 against 13 to 32; code 29 to 64; seed 82 52, 52, 46, 44 of 60) match A.json and the table sums; rule 2 equals rule 1 in every condition.
- Rule 22 headings, rule 26 tables and the rule 2 "a miss by one line is a miss" handling are present and not softened.
