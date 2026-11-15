# Lane 7: Research-standard auditor
Verdict: submit after fixes (no blocker; the long paper has the hypotheses, deviations, leakage, flow and limits sections, but rules 3, 15, 16, 18, 20, 21, 29 and 30 each have a gap a judge reading against STANDARD v3 can find)

Paths below: ARTICLE = docs/ARTICLE.md, HF = docs/submission/HF_ARTICLE.md. I read both in full, plus R-016, R-017, R-162/R-163 and `results/s3/`. I did not run `make_article.py` (it writes into the repo), so I did not check that the committed ARTICLE.md matches the results files.

## Findings (most severe first)

F1. [MAJOR] Rule 16, ARTICLE section 9 and HF section 6: the S3 rows for 6.37 and C1 are pooled over seeds 82, 83, 94 with no per-seed numbers, and the seeds are the ones used to pick C1 (R-191/R-279 pick recall is over 82, 83, 94), not fresh seeds. The pool hides the spread that decides clause (c). Per seed, from `results/s3/s3_*.json` rows: C1 N-hit false answers 11, 29, 11 of 236 (4.7%, 12.3%, 4.7%) against base 14 of 236 (5.9%); only seed 83 is above base. C1 recall 127, 132, 105 of 414. The shipped model alone (seed 82, not the pool): recall 99 of 414 (23.9%), copies 62 of 298, N-hit 100 of 236 (42.4%).
    Evidence: `results/s3/s3_fix17cs37_82/83/94.json`, `s3_k13opc1_r263_82/83/94.json` (kind, view, copy, n_hit, false_answer fields); ship_rule.json is pooled only.
    Fix: add a per-seed row for 6.37 and C1 to section 9 and say the S3 seeds are not fresh (rule 16). State the shipped seed's own S3 numbers.

F2. [MAJOR] Rule 3, ARTICLE sections 5, 6.1: no negative or positive control is reported for the sealed run or S3, and no sentence says why. R-016 registered an "adapter-moved control"; R-017 shows a `three_exchanges` control (0 of 24 on `older`) and a failed whole-chat control at 419 (the article says only "does not fit the 10 GB card", R-166). R-162/R-163 contain neither word "control" nor a three_exchanges arm. The only no-tool, three-exchange arm appears in LongMemEval-S (section 6.3). The second independent scorer (AuditKIT) "was not run on 6.37" (section 4); the only second marker covers 50 development lines. Rule 3: an absent control is not a passed one.
    Evidence: `grep -n control docs/ARTICLE.md` returns only candidate "controls" (C1, C0); R-017 "Controls" paragraph.
    Fix: add a controls table (arm, expected result, observed, gate passed), or a stated deviation with the reason each control could not run.

F3. [MAJOR] Rule 21, ARTICLE 6.1, 6.2, 5 (hypotheses table), HF sections 1 and 3: many differences are bare counts. 6.1 confirmatory rows give an interval but no sign-test p and n of pairs (R-163 has p = 3.4e-145 and the pair counts; the article drops them). The coherence and false-retrieval tables (6.1) have counts only, no denominators, no interval, no effect size (deviation 3 admits the coherence interval was "not computed"). 6.2's two tables give sign-test p only: no effect size, no interval. The hypotheses table's outcomes ("holds", "met") carry no number. No assumption-check output appears anywhere (`grep -i assumption` returns nothing); the sign tests' independence problem is stated (R-141, R-163) but no check is shown. HF's headline ("91 to 107 of 120 against 13 to 32", "85.2 to 90.4%") has no interval or test.
    Fix: put effect (points), 95% interval and method, n and p in each 6.2 row and in the hypotheses table; add false-retrieval denominators; one line naming the assumption record (or "none applies, because ...") per test.

F4. [MAJOR] Rule 18, ARTICLE section 3 leakage table and section 12: contamination of the pretrained model is "not probed". Rule 18 requires a probe (verbatim completion) and reports, never "ruled out". The table also says "every chat here was written after its release", which does not cover LongMemEval-S (public since 2024, Wu et al. 2025) and is the one set not written by the project. The duplicate row covers only `probe`/`hard_dev` (stop on a four-word run) and S3 (140 of 42,561); no duplicate or hash check against `heldout`, `independent` or the two outside-writer sets is stated. The temporal row covers S3 only.
    Fix: run or register the probe, or keep "not probed" and add LongMemEval-S as a named contamination risk; add duplicate-hash rows for the first sealed pools and outside sets (hashes, not reads of sealed text).

F5. [MAJOR] Rule 29, ARTICLE 6.2, 9, HF section 3: baselines were measured after the method and not on an equal tuning budget. The method had 40 + 24 candidate sets and eight seeds; base got "two fixed prompts" and "a search over prompts was not tried" (6.2). No baseline row has budget fields. The simple baseline that decides when to search (code searches only if the answer text is not in the last three exchanges, or only if the newest message is a question) was not run, yet the claim "training's gain is when to search" (abstract, HF 3) rests on comparing with code that searches every turn. Base with the tool matches 6.37 on `in_view` (set 1: 36 against 35), so the "leaves answers in view alone" gain is against code only.
    Fix: add a budget column (prompts tried, seeds, candidates) to the baseline tables and either run the gated-code baseline or reword the claim to "against always-search code".

F6. [MAJOR] Rule 30, ARTICLE section 3: the only flow table is S3's. The training set (how 1,094 rows were built and what was dropped), the first sealed test, the outside-writer sets and LongMemEval-S have none. LongMemEval-S's denominators move across rows (466, 460, 476, 411 read, 402, 389, 408, 441, 328, 472, 490, 484, 497 of 500) with failures in the last row but no exclusion-by-step table. S3's N-hit denominator is 236 for every arm including the no-search whole-chat arm: the scorer (`scripts/records/score_s3.py` lines 79 to 83, `run_s3_eval.py` n_hit) defines n_hit by a fixed canonical query, an item property, but the article defines it as "a never-told question whose search returned passages". Flow table lists 240 never-told items, not 236.
    Fix: add flow tables (at least LongMemEval-S and the first sealed test) and define n_hit as item-level, with the 4 missing items accounted for.

F7. [MAJOR] Rule 38, ARTICLE abstract, "Submission summary" headline table, contributions, 6.1, 9; HF opening paragraph, sections 4, 5, 6: not every claim carries a label. The abstract and headline table have none. HF's "Result first" mixes a confirmatory pass with exploratory baseline claims. Section 6.1 ("confirmatory") includes the late references and "Seed 82 is far above both references (largest p 3.2e-4)", which were not registered tests of that run. Section 9's "strongest baselines on S3" (code and whole chat recalling more than both trained models, 38.9% and 66.2% against 27.9% and 29.3%) is under the confirmatory heading with no label and no test; HF 6 the same. The abstract says "passed every rule" about 6.37, but R-016 rules 1 to 4 are pooled over adapters; seed 82's own pass is not a registered hypothesis. HF 4 (demo claims) and "Where recall is lost" are unlabelled and post hoc.
    Fix: label each abstract, summary and headline-table claim; move the late references and S3 baseline comparisons under "(exploratory)".

F8. [MAJOR] Rule 20, ARTICLE section 5 "Statistics": "reported unadjusted, as a family of exploratory results" gives no family size, no registered false-discovery level, no adjusted result. About 14 sign-test p-values appear in 6.2 alone. BH at q = 0.05 on those I counted (m = 14) keeps all p below 0.0051 and drops 0.047, so the stated claims survive; the paper does not show it.
    Fix: one line: family size, q, adjusted outcome (a script recomputing from the list).

F9. [MAJOR] Rule 13/28, ARTICLE sections 4, 8, 12: the candidate count is not given as one total. The first 40 candidate sets point to commit 7b71a20; the reopened 24 are listed, but 18 or more further tries (K2, K1.1, K1.2, K3, K3.1, K4, K3.2, K5, T2 to T6, lever 2, R2a/b/d, two blend grids, C0) are named without a count; the cap became a time cutoff (deviation 9) with no resulting total.
    Fix: state one total of candidates scored on development pools and the cap or cutoff it was measured against.

F10. [MINOR] Rule 26, ARTICLE section 11: no deviation rows for R-038/R-039/R-041 (amendments to R-016 before the run; described only in section 5 prose), and none for retiring Demo2 and Demo3 and replacing the gate with Demo4/Demo5 (R-254), after K4.x candidates were rejected on Demo2. Rows 3, 9 and 10 give no reason ("not computed", "my decision"). Hypotheses table row "LongMemEval-S H1 to H3" does not state H1 to H3.
    Fix: add the rows; state the reasons and the three hypotheses.

F11. [MINOR] Rule 8/21, ARTICLE abstract and 6.2 against section 9: "plain code recalls as well as 6.37" rests on a non-significant sign test (p = 0.76, 0.45), while section 9 says code recalls more than 6.37 on S3 with no test. "No measured difference" is not "as well as".
    Fix: use "no measured difference" in the abstract and give the S3 code against 6.37 test.

F12. [MINOR] Rule 15, ARTICLE 6.1 and 9: judge agreement is reported on development lines only (R-128, 13 of 576); no agreement counts for the sealed run or the S3 sample. S3 has no measure of over-declining on answerable items for C1, which trained to decline more (the LongMemEval-S table shows 6.37 declining 233 of 470).
    Fix: add pairwise judge agreement for the sealed and S3 sheets and C1's answerable-decline count.

F13. [MINOR] Rule 9, figures: captions often omit n and seeds (Figures 1, 5, 6, 7 give "60 chats" or "eight seeds" only in places); Figure 7 has no interval; outputs are SVG and PNG, not PDF (SVG is vector).
    Fix: add n and seeds to each caption.

F14. [MINOR] Short paper (HF): the author asked it to point to the long one, so it has no hypotheses, deviations, flow or leakage tables and its limits are one bullet list, not rule 22's headings. Its tables are bare counts (no interval or p) in sections 3 and 6; the labels exist only on four section headings (F7).

## What holds up
- Rule 4: figures in prose are filled from `{{...}}` slots in `docs/article_template.md`; I could not find a typed number among the ones I spot-checked (13 of 576, 959 of 960, 1.3 points, 233 of 470), and `make_article.py` stops on count mismatches.
- Rule 22 headings are all present in section 12 (population, internal, external, construct, probed not ruled out, second team, same-family judges, Kevin unblinded). Rule 26 has both tables; rule 2's one-judged-line miss is applied, not softened.
- Header numbers I rechecked match: abstract 91 to 107 against 13 to 32 (section 6.1 seed 82 rows), code 14 to 32 and seed 82 44 to 55 (HF 3), S3 flow 834 items, S3 totals in ship_rule.json.
