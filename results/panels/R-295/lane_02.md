# Lane 2: Statistician and experimental designer (hostile)
Verdict: submit after fixes

Recompute script: `panel\l02\recompute_s3.py` (read-only, reads `results/s3/` only). Every S3 count in the three
documents and `ship_rule.json` reproduces exactly, including the recall bound 0.091.

## Findings (most severe first)

F1. [BLOCKER] docs/submission/ABSTRACT.md, last paragraph: "Every test was registered before it ran" is false. The
    scripted demo that caused the reopening was run before it was registered, and the demo pass rule was changed after
    both models' demo readings existed.
    Evidence: RECORDS.md R-175 title "The scripted demo for 6.37, run before it was registered"; R-276, R-278, R-283.
    Fix: "Both sealed tests and their rules were registered before they ran; the demo exceptions are disclosed in the
    long paper."

F2. [MAJOR] HF_ARTICLE.md section 6, ARTICLE.md section 9 and line 326 ("holds", confirmatory): the clause that decided
    the outcome, and (a)'s no-worse-than-base lines, are point comparisons, and no interval is reported for them. The
    1.3-point fail and the 0.6-point statement pass are both inside noise. Chat-resampled 95% intervals (10,000 draws,
    seed 0, same method as R-281), C1 pooled minus base: N-hit false answers +1.3 points [-3.1, +5.7]; statement -4.4
    [-10.6, +1.7]; in_view +2.2 [-6.1, +11.1]; plain never-told +3.1 [-2.5, +9.2]. Base's 14 N-hit false answers sit in
    10 of 60 chats. A candidate exactly as good as base fails "not above base's" about half the time on point estimates.
    The registered verdict stands, but "C1 failed by 1.3 points" without the interval reads as a measured difference,
    and "(a) holds" as shown no-worse, when S3 cannot show either at this size.
    Evidence: `recompute_s3.py` output; `scripts/records/score_s3.py` lines for in_view, statement, never_told_plain and
    (c)'s base part use no bound; ARTICLE.md lines 762 to 763 (no power calculation).
    Fix: add one sentence and the four intervals to section 6 of the short paper and section 9 of the long one: "The
    rule's point comparisons cannot tell C1 from base on these lines; C1 fails the rule as registered."

F3. [MAJOR] HF_ARTICLE.md section 6 (silent), ARTICLE.md line 672: the report arms are listed as raw counts, but
    neither paper says what they show. K1 (R-178's original single candidate) and K2.1 meet every line of the rule that
    can be scored without coherence, including the clause C1 failed: K1 N-hit false answers 12 of 472 (2.5%), K2.1 14
    of 472 (3.0%), base 14 of 236 (5.9%); recall bounds 0.097 and 0.088. K1.3 fails (c) like C1 (37 of 472, 7.8%).
    So the development pick, by recall alone over 24 candidates, chose an arm S3 ranks below the first candidate on
    the deciding clause. On development, C1 already had twice K1.3's T2 false answers (19 against 9) and K1 had 3; the
    screening line for this fault compared to 6.37 only, never to base (R-191 line 2, R-279). This is a selection
    result a judge needs, and S3 is now spent for choosing among these arms.
    Evidence: `recompute_s3.py` (report arms scored as if picked; two seeds, coherence not judged);
    `results/panels/R-279/decide_r191.txt` lines 20, 42.
    Fix: two sentences in both papers: what K1 and K2.1 show, that it is post hoc and two seeds, that no arm is
    swapped in, and that the pick criterion (dev recall) did not track clause (c).

F4. [MAJOR] HF_ARTICLE.md section 6, ARTICLE.md section 9: the rule pools three seeds, but one seed ships. C1 seed 82,
    the seed that would have shipped (R-178), fails (a)'s statement line on its own (50 of 60 left unsearched, 83.3%,
    against the 91.7% line) and passes (c) (11 of 236, 4.7%). Seed 83 alone carries the (c) fail (29 of 236, 12.3%);
    seed 94 has 11 of 236. Pooling is the registered reading (R-178 "pooled"), but the papers never give the shipped
    seed's own lines, and the seed spread on (c) (4.7% to 12.3%) is larger than the C1-base gap.
    Evidence: `recompute_s3.py`, per-seed rows `C1_82`, `C1_83`, `C1_94`.
    Fix: a per-seed row for C1 and 6.37 under the S3 table, and one sentence that the rule judges the recipe, not the
    shipped seed.

F5. [MAJOR] HF_ARTICLE.md section 3, LongMemEval paragraph: 53 against 34 and 40 of 248 is given without the long
    paper's split: on the 233 answerable judged questions 6.37 ties code (40 against 40, p = 1.0) and shows no measured
    difference from base (40 against 32, p = 0.29); 11 of the 19-point lead over base comes from 15 unanswerable
    questions. The 248 also mixes a 148-question type stratum with a 100-question random sample, so 53 of 248 is not a
    rate on LongMemEval-S.
    Evidence: ARTICLE.md lines 466 to 475.
    Fix: add the split (labelled post hoc, as the long paper does) and "on a stratified 248 of 500".

F6. [MINOR] HF_ARTICLE.md line 34 and ARTICLE.md line 102: "a sealed test opened once (the first sealed test, S3)"
    names two tests as one. Fix: "rest on the two sealed tests, each opened once: the first sealed test and S3".

F7. [MINOR] Interval wording. HF line 184 and ARTICLE line 649 "within each other's 95% intervals" uses overlap; the
    difference interval is the test: C1 minus 6.37 recall +1.4 points [-3.1, +5.9]. HF line 165 "a lead under two
    seeds' spread" is unclear: R-279 gives sd about 19 a seed, so a 3-seed sum has sd about 33 and the 33-point lead
    is under one sd of the difference. HF line 105 "Code recalls as well as 6.37" infers equality from p = 0.76 and
    0.45 with 120 items. Fix: give the difference interval; say "no measured difference" for code.

F8. [MINOR] Rule 1 of the first sealed test pools eight adapters into one sign test against a single base run, so each
    base row is counted eight times: 629 discordant pairs from 120 items, p = 3.4e-145. The pass does not depend on it
    (seed 82 alone p = 1.4e-19; chat-resampled gain +50.8 to +69.7). Not printed in the papers.
    Evidence: `results/analysis/R-162/A.json` `rule_1_recall.sign_test`; `scripts/records/score_r162.py` recall_rule.
    Fix: one line in ARTICLE section 5 that the pooled test overstates n and the seed-82 test and the interval carry it.

F9. [MINOR] HF line 179: "Coherence ... of 120" does not say it is C1 seed 82 only, one sample, no interval
    (97 against 95). Fix: add "seed 82, 120 sampled items".

## What holds up
S3's scorer and reading (R-281, R-282, commits a806741 and e98cc20 at 14:16 and 14:20) were committed before the first
S3 result file (bb4e12b, 14:29); every S3 count in the papers matches the run files.
First sealed test: seed 82's 91 to 107 of 120 and base's 13 to 32 match `results/analysis/R-162/*.json`; the 120 are
distinct facts (sizes 58 and 419 share 1 of 30 answers); code 14 to 32 and seed 82 44 to 55 of 60 match
`results/analysis/R-168/refs.json`; every adapter beats base on coherence under all three judges by over 30 lines.
R-191's change of the ship rule after K1's development results is disclosed (ARTICLE line 510, deviations row 8).
