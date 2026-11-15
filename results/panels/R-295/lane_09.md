# Lane 9: Against (hostile, the strongest case against submitting as is)
Verdict: do not submit as is; submit after fixes F1 to F4 (the rest can wait)

## Findings (most severe first)

F1. [BLOCKER] HF_ARTICLE.md sections 5 to 6; ARTICLE.md section 9 "Report arms": K1, the single candidate R-178 registered, and K2.1 meet every measured line of the ship rule on S3, and neither paper says so. The short paper never shows the report arms; the long paper lists them and moves on. A judge reading ARTICLE.md's S3 table sees K1's 12 of 472 false answers beside base's 14 of 236 and asks why the write-up says the reopening failed. It also shows the selection steps after K1 (pick recall 720 against 742, inside seed spread; then a demo rule changed after readings, decided by 1 question of 12 and 1 of 8) chose away from candidates that pass.
    Evidence: I applied score_s3.py's own `rate` and `lower_bound` to the report arms (script in scratchpad/panel/l09/k1_rule.py, read only). K1: recall 0.306 (bound 0.097), in view 0.883, statement 0.950, never told 0.983, copy 0.0017 (bound 0.166), N-hit 0.0254 (bound 0.318, below base's 0.0593). K2.1: N-hit 0.0297, every other line passes. Coherence and seed 94 were not run for them. ARTICLE.md:529 to 531 (K1 passed every screening line, pick recall 720); R-292.
    Fix: Say it in both papers and the abstract, in one or two sentences: "Two report arms, K1 and K2.1, meet every line measured for them (two seeds; no coherence run); they were not the pick, so the rule keeps 6.37. Development screening and the demos did not predict S3." Put K1 first in "Next".

F2. [BLOCKER] ABSTRACT.md lines 3 to 9, HF_ARTICLE.md "Result first": the headline is the one setting built by the author's own generator, where base with the tool is weakest. On every set from outside the generator, an untrained baseline matches or beats 6.37 on recall: outside-writer sets (whole chat 71/65 against 39/53; code tie), S3 (whole chat 66.2%, code 38.9%, against 27.9%), LongMemEval-S (code 40 against 53, p = 0.12). On S3, 6.37 does worse than base on three of four measures: copies 21.8% against 3.7%, N-hit false answers 40.4% against 5.9%, plain never-told declines 66.1% against 92.5%. That is the problem statement's "ignores distracting documents" clause. The abstract's "no adapter made more false retrievals than the untrained model" stands in paragraph 1; that 6.37 gives seven times base's false answers on S3 is never said directly.
    Evidence: ARTICLE.md:617 to 621 (S3 table), 395 to 413, 471 to 474.
    Fix: Add to paragraph 1 of the abstract and of "Result first": "On S3, written by outside writers, 6.37 named a value on 40.4% of never-told questions whose search returned text, against 5.9% for the untrained model, and its recall was below code that searches every turn." Name the first sealed test as "generator-built" wherever its result appears.

F3. [MAJOR] ABSTRACT.md:27 to 29: LongMemEval-S gives 53 against base's 34 but leaves out code (40, interval -0.8 to +11.3, p = 0.12) and the split where 6.37 ties code on the 233 answerable questions (40 against 40) and 11 of its 19-question lead over base comes from unanswerable questions. This is the only test whose chats really do not fit, which is the title's claim.
    Evidence: ARTICLE.md:470 to 474.
    Fix: Add "code that searches every turn: 40 (no measured difference)" to the abstract and to HF_ARTICLE.md:110 to 113.

F4. [MAJOR] ABSTRACT.md:29 to 30 "Every test was registered before it ran"; HF_ARTICLE.md:129 "fixed before S3 opened (R-178, R-191)": R-191 changed clause (a)'s standard from 6.37 to base after K1's development results were read (deviation 8). The S3 ship-rule scorer was written after S3 started (deviation 13). The demo pass line was changed after the readings (deviation 11). The short paper's disclosures list 11 and 12 but not 8 or 13.
    Evidence: ARTICLE.md:505 to 512, 728, 733; R-281 opening line.
    Fix: Change the abstract's sentence to "Every test was registered before it ran; three rules were changed after some readings, listed in the long paper's section 11." Add deviations 8 and 13 to HF_ARTICLE.md section 7.

F5. [MAJOR] Neither paper says that the never_told scorer passes a reply that invents a value outside the listed ones. So the never-told counts on the first sealed test and the outside-writer sets (37 and 36 of 40) are upper bounds.
    Evidence: src/aya_retrieval/scoring.py:60 to 61; docs/MODEL_CARD.md:205 to 207 (R-020); `grep -n -i "invent\|listed values"` over ARTICLE.md, HF_ARTICLE.md and ABSTRACT.md returns nothing.
    Fix: Add the model card's sentence to ARTICLE.md section 12 (construct validity) and to HF_ARTICLE.md section 7.

F6. [MAJOR] ARTICLE.md:50, the summary's headline table: base and trained are "of 120" and code is "14 to 32 of 60" in the same row, so code looks equal to base. On the same 120, code is 29 to 64 (A 64, B 61, C 37, D 29; ARTICLE.md:376 to 377), about double base.
    Fix: State code of 120: "29 to 64".

F7. [MAJOR] R-178 and R-281 registered "baselines first" when S3 is reported. Both papers put them after the trained models, "beside the rule", and the deviations table does not list this.
    Evidence: R-178 ruling 5; R-281 last bullet; HF_ARTICLE.md:188; ARTICLE.md:717 to 736.
    Fix: Move S3's code and whole-chat rows to the top of the S3 table, or add the change as deviation 16.

F8. [MINOR] Length and structure: the short paper runs about 3,100 words plus 6 figures and 4 tables, well over the asked 5 pages. Section 5 uses internal ids (K1 to K4.9, R2c, OP, C2, Demo2 to Demo5, "20 screening lines", "fixed older line"), and its scores have no denominator ("pick recall 742", "868", "775 against 742"; ARTICLE.md:527 gives no n either). More than half of the body is about a replacement that did not ship.
    Fix: Cut section 5 to four sentences (how many candidates, how the pick was chosen, the rule change, and the F1 fact), and give pick recall's n.

F9. [MINOR] HF_ARTICLE.md:34 "(the first sealed test, S3)" reads as if S3 is the first sealed test; ARTICLE.md:103 has the same text. HF_ARTICLE.md:225 to 226 "the plan (R-001) and the my chat engine LLE".
    Fix: "(the first sealed test and S3)"; "and my chat engine LLE".

Outside the documents: the brief gives the form deadline as 16 November 07:59 ET. R-178 and R-173 give 16 November 11:59 UTC (15 November 11:59 PM AoE), which is 06:59 ET (EST, UTC-5; checked with .NET TimeZoneInfo). Plan for 06:59.

## What holds up
- C1's S3 lines: my recomputation with score_s3.py's functions matches ship_rule.json (recall bound 0.091, copy bound 0.164, N-hit 0.0720 against base 0.0593).
- The demo rule change (R-276, R-278) and Demo5's double read are disclosed in both papers, with the reason (R-283).
- Seed 82 was named before most seeds existed, and the paper says it is the lowest of eight on `independent` (ARTICLE.md:366 to 368).
