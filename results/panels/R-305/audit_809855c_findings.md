# Audit of the write-up at commit 809855c (R-303) against the submit checklist and Kevin's requirements
Audited 2026-11-15 from about 09:20 to 10:10 Eastern. Findings only: nothing in the repo was changed (a scratch copy of 809855c was used to rebuild the documents).

Result: 2 HIGH, 6 MEDIUM, 6 LOW. No wrong count was found in any S3, first-sealed-test, outside-set or LongMemEval-S number I recomputed.

Read in full: ARTICLE.md (1,079 lines), HF_ARTICLE.md, ABSTRACT.md, MODEL_CARD.md, MODEL_CARD_C1.md, README.md (582 lines), PUBLISH.md, FIXLIST.md, RECORDS R-276 to R-279, R-294, R-295, R-298, R-302, R-303. Viewed the six figures R-303 or R-302 touched (s3_faults, s3_misses, never_told_slide, s3_recall, whole_chat_or_search, recall_out_of_view).

## Checks run (all passed unless a finding says otherwise)
- **Rebuild.** Extracted 809855c to scratch and ran `make_article.py` with the project venv: ARTICLE, HF_ARTICLE, ABSTRACT, MODEL_CARD and MODEL_CARD_C1 came out byte for byte the same as the committed files. So every filled number is what the templates and results files give.
- **S3 recomputed from the 15 run files** (`results/s3/s3_*.json`, 834 rows each), per arm and per seed: recall, in view, statement, plain never-told (by `variant`, as `score_s3.py` does), copies, N-hit false answers, right search decisions (682, 666, 670; code 714; C1 797, 789, 807), tag-question searches (7, 0, 5), found-fact counts (480 of 1,242; code 260 of 414), `older` alone by arm (30, 141, 253, 285, 292), re_ask (1, 17, 23, 6, 110), false claims corrected (1, 11, 4, 0, 32; K1 1, K2.1 4), wrong-recall stages (C1 661, 178, 39; 6.37 549, 192, 154), 59 of 347 right answers on rows not found (all `confirm`, true claim, no search), base's 28 of 59 (27 with no search), report arms by seed. Every one matches the papers and `ship_rule.json`.
- **The definition change (s3_qw_code_only).** Recomputed with "both searched": 6.37 seed 82: 88 (code found, seed missed), 22 (the reverse), p = 1.6e-10; C1 seed 82: 100 and 29, p = 2.5e-10. Grounding on the questions both found: 119 (65 against 84, p = 0.0026) and 154 (111 against 93, p = 0.038). All as printed. The text says "where both searched" in all three places (ARTICLE 823 to 826 and 1066 to 1070, HF_ARTICLE 186 to 188). See M5 for two wording problems that remain.
- **First sealed test** recomputed from `results/recall_eval/final_*`: pooled 426, 409, 434, 409, 434, 429, 434, 424 of 480; base 17, 15, 15, 14, 10, 11, 5, 8; seed 82 106, 107, 92, 91 against 32, 29, 21, 13; every seed's recall in Appendix A. All match.
- **Outside sets** (`blind_*`, `blind2_*`, seed 82 and base): older, confirm, in view, never told, statement all match the section 6.2 tables.
- **LongMemEval-S** against `results/analysis/R-170/scores.json`: 333, 238, 372 of 476 (p = 4.0e-4), gold in reply 51 and 63 of 411 (p = 0.20), searched 421 of 466, 309 of 460, 450 of 450, 21 of 30 unanswerable, clean first calls, seconds. All match. One denominator note in L1.
- **GPU hours** from the run files: 108.6 h over 186 training runs, 100.0 h over 849 evaluation runs, 7.9 h over 15 S3 runs (217 in all). Match.
- **C1 card** training line: 764 s + 770 s = 26 minutes, 1,137 rows, learning rate 0.0001, 1 epoch, batch 2. Match.
- **Records.** All R-ids cited in the six documents exist (R-001 to R-303, none missing). Spot-checked against their entries: R-276 to R-279 (commit times 10:40, 10:48, 10:54 give "six minutes later"), R-204, R-249, R-267 (106 of 117), R-298, R-156 (240 of 240), R-173, R-294, R-295, R-298, R-301, R-303 lane counts. First commit 2026-11-01 11:17 EST matches. The first demo-test change is described correctly in all seven places (after both of C1's readings and K1.3's Demo4 reading; ordered K1.3's Demo5 reading knowing C1's; the second after all four).
- **Voice.** 0 em dashes, 0 en dashes, 0 spaced hyphens or double hyphens, 0 "we/our/us", in all six documents. Marketing and hedge words: only in README, see L2.
- **Privacy** regex per document: 0, 0, 0, 0, 0, 0.
- **Co-author line:** 1,629 commits, 1,629 with it.
- **Abstracts:** ARTICLE Abstract 499 words, ABSTRACT.md 498 with the title (483 body). Both under 500 by whitespace count; see M1 for the margin.
- **Links.** Every local link and every image path in the six documents resolves. Every outbound URL returns 200 except the four in H1. The four Hugging Face repos are public and not gated.
- **Never opened:** `pools.py` past line 451, `data/heldout*`, `data/*independent*`, `results/longmemeval/`, `docs/demo5/`.

## b10eb2a findings: status now
| Finding | Now |
|---|---|
| H1 links and push | Still open, Kevin's call (H1 below). |
| H2 ARTICLE Abstract 515 words | Fixed (499). Margin is 1 word, see M1. |
| H3 README had no S3 table | Fixed (table at README 136 to 147, arms sentence). |
| M1 body length | Body is now 13,518 words (was about 11,800), file 16,229 (was 15,372). Kevin's call, L6. |
| M2 v3 not in the repo, five rules unstated | Partly fixed: section 11 says the rule numbers are v3, not in the repo; rows 21 and 22 cover rules 20, 21, 28, 30. Rules 23, 24, 34, 40, 41 still have no row, and README 153 still says STANDARD.md is the standard the repository is built to (M4). |
| M3 reopening wording | Fixed except the dates (M3). |
| M4 figures | Figure 5 band and line fixed; Figure 2 dots offset; point-count captions; Figure 8 no longer red and green; PDFs present. Figures 1 and 2 still have no interval (deviation 21, disclosed). |
| M5 first-use terms | Terms fixed in both abstracts. "Outside writers" without "Claude agents" still at first use (M2 below). |
| M6 PUBLISH.md | Fixed (current order, four repos, S3 upload). |
| M7 README 402 of 708 sentence | Fixed. |
| M8 section 6.2 p = 0.11 | Fixed. |
| L1 to L5 | Fixed (115,000 tokens gone; README stale lines fixed; heading says 12 to 15; the +50% and +96% sentence now names its comparison; HF_ARTICLE has the revision and a one-line claim). |
| L6 short paper length | 2,761 words, was 2,441 at R-299 (+13%). Kevin's call. |

## HIGH

**H1. The links in every document still point at copies that do not hold this write-up. Carried, Kevin's call; the form closes 06:59 Eastern on 16 November.**
Tested 2026-11-15 around 09:50 Eastern:
- `origin/main` is still 7b71a20 (10 November); 474 commits behind (`git ls-remote`).
- 404: `raw.githubusercontent.com/.../main/figures/s3_faults.png` and `.../demo_contamination.png`. HF_ARTICLE lines 157 and 173 show both, so the short paper's Figures 2 and 3 are broken until the push. Line 104 (recall_out_of_view.png) loads.
- 404: `github.com/.../blob/main/docs/demo.md` (ARTICLE 115 `demo.md`, README 232 and 276) and `.../main/notebooks/demo_6_37.ipynb` (README 193, ARTICLE 114: Colab opens but cannot load the notebook). `docs/MODEL_CARD_C1.md` also 404 on main.
- Hugging Face: `aya-retrieval-6.37` last modified 13 November (its README and `ARTICLE.md` are the old versions); both datasets 10 November (no `results/s3/`, no reopened training sets); `aya-retrieval-c1` modified today 10:41 UTC, before R-303 changed its card (33 lines), so it needs the R-303 card.
- ARTICLE 111 to 113 says `aya-retrieval-eval-logs` holds "every trajectory"; false for S3 until the upload.
Fix (PUBLISH.md steps 1 to 4, in order): privacy sweep over the 474 unpushed commits; push; the four Hugging Face uploads (6.37 card and article, C1 card, eval-logs with `results/s3/`, chats); recheck the links above logged out. Nothing else in the write-up can be finished before that.

**H2. README tells the reader to give the trained model the whole chat, and says it is "much better than base"; every other document says the opposite, and S3 contradicts it. README lines 310 to 313; MODEL_CARD.md lines 201 to 205.**
README 310 to 313: "the design this supports is to show the trained model the whole chat when it fits, and let it search when it does not: no measured loss against base when the chat fits, and much better than base once only part of the chat can be shown." Problems:
1. ARTICLE "Use this when", HF_ARTICLE "Use this when" and MODEL_CARD "Which to use when" say: if the chat fits, show base the whole chat with no adapter; if the faults matter, do not use 6.37.
2. "No measured loss against base" rests on the outside-writer sets only (R-165, one seed, 40 chats a kind), where README 308 to 310 itself says the test cannot show equality. 6.37 with the whole chat was never run on S3 or on the generated chats (MODEL_CARD 203 to 204 says so), so the two S3 faults are unmeasured in that configuration.
3. "Much better than base once only part of the chat can be shown" is about recall (27.9% against 14.3% on S3) and leaves out that on the same S3 chats 6.37 names its in-view wrong value on 21.8% against 3.7% and a listed value on 40.4% against 5.9% of N-hit questions. It is also a vague strong word the voice rule bans.
MODEL_CARD 201 to 202 ("show it the whole chat; the tool can stay in the prompt") has the same reading problem: "it" is the adapter.
Fix, README: replace lines 310 to 313 with "So when a chat fits, show base the whole chat and leave the adapter out. 6.37 with the whole chat was measured only on the outside-writer sets, where it shows no measured difference from base with the whole chat (one seed; the test cannot show equality); it was not run on S3, where 6.37 with the tool is worse than base on both faults. The whole-chat result holds on the outside-writer chats, not on this project's generated chats:" (then the existing sentence). MODEL_CARD 201: "When the chat is short enough to show whole, show base the whole chat; this adapter with the whole chat was measured only on the outside-writer chats (R-165)."

## MEDIUM

**M1. Both abstracts pass the 500-word limit by one or two words. ARTICLE lines 13 to 44 (499 by whitespace); ABSTRACT.md (498 with the title, 483 body).**
By whitespace they pass. A counter that splits on hyphens, slashes or the dot in "6.37" gives 512 to 544 for these two texts (ABSTRACT.md body 514 by `\w+` tokens). The form's counter is unknown, and the abstracts are number-dense. Cut about 30 words from each so any reasonable counter is under 500. Candidates: ARTICLE 43 to 44 and ABSTRACT.md 31 to 32 ("S3's flags see only listed values of the asked category; invented values and other stored facts pass unseen" is already in section 12 and the cards); the K1.3 clause in ARTICLE 42 to 43.

**M2. "Outside writers" is still unqualified at first use in four documents. ABSTRACT.md line 11; HF_ARTICLE lines 7 and 9 to 12; README lines 7 to 8; ARTICLE line 51.**
Read cold, "chats from outside writers" suggests people wrote them (Kevin's rule: never imply people wrote the Claude-agent chats). The agent fact comes later (ABSTRACT.md 20 "six blind writer agents", HF_ARTICLE 131, README 551, ARTICLE 245). Fix: "chats from outside writers (Claude agents)" at the first use in each of the four; ARTICLE line 51: "a second sealed test from outside writers (Claude agents)".

**M3. The reopening reason is stated with no dates, and the only record of the extension says the site still shows 15 November. ARTICLE 29, 204, 214, 502, 863; HF_ARTICLE 128; README 35; MODEL_CARD 52; ABSTRACT.md 19.**
R-173 records "the deadline was reported pushed (the site still says 15 November, 11:59 PM AoE)" and PUBLISH.md line 1 gives the same 15 November due date. A judge who opens the Lexsi page sees 15 November and no extension, so "the deadline extended" cannot be checked in the papers. Fix (needs Kevin or the Lexsi announcement): one clause, "the deadline moved from <date> to 15 November" in ARTICLE 502 and the declaration at 863, or say "reported extended (R-173)" at each place. Kevin's words use "the extra day"; the papers say "the extra time". Either is fine if the dates are given.

**M4. STANDARD.md is called "the standard this repository is built to" while the papers cite rules it does not contain; five v3 rules have no statement. README line 153; ARTICLE 708 to 710 and 734 to 735.**
README 153: "[`STANDARD.md`](STANDARD.md) is the standard this repository is built to." The file is the October version (12 rules); ARTICLE section 11 says so and says rule numbers above 12 are v3, not in the repository. README should say the same. Rules 23 (data manifest with bytes and SHA-256), 24 (fingerprint fields), 34 (source kind per number), 40 (time proof for the first sealed test) and 41 have no row in the deviations table and no sentence in Limits. Fix: README 153: "STANDARD.md is an earlier version of the author's research standard (rules 1 to 12); the rule numbers above 12 in the papers refer to version 3, which is not in this repository." Add one deviation row after row 22: "Rules 23, 24, 34, 40, 41 of STANDARD v3 | not applied as written: no per-file data manifest with hashes (only `results/freeze/sealed_manifest.json`), no fingerprint of every field, no source-kind check per number, time proof for S3 only (R-181) | not done | STANDARD v3 rules 23, 24, 34, 40, 41". Whether the project adopted v3 is Kevin's word.

**M5. Two wording problems on the query-writing counts after the definition change. ARTICLE lines 823 to 826 and 1066 to 1070; HF_ARTICLE 186 to 188.**
(a) "on 53 more seed 82 did not search (C1 seed 82: 100, 29 and 6)": seed 82 did not search on 67 recall questions (C1 seed 82: 11); the 53 (and 6) are those among them where code's search found the fact. The sentence reads as if 53 is all of them. Fix: "on 53 of the 67 questions seed 82 did not search, code's search found the fact (C1 seed 82: 100, 29, and 6 of 11)".
(b) ARTICLE 1070: "Both use the same keyword tool, so on the questions both searched the query made the difference." FIXLIST item 3 said to drop "the query made the difference". The counts show code found the fact where seed 82 did not on 88 questions and the reverse on 22; they do not isolate the query (code runs one search, the adapter up to three, and the adapter's reply is read separately). Fix: end the paragraph at "(sign test p = 1.6e-10)". The same causal sentence "Query writing is a measured cause" (ARTICLE 822 to 823, 828 to 829, 1065; HF_ARTICLE 185 to 186) could read "Query writing is the likeliest cause, measured as" to match; Kevin's call on how strong.

**M6. README "Results at a glance" gives the S3 recall and fault table but still has no coherence or report-arm numbers beside the rule, and the ship-rule table is only in the long paper. README lines 136 to 147.**
This is minor now (the S3 table and the arms sentence exist, which closes b10eb2a H3). What is still missing in README is the one fact a judge asks first: which clause C1 failed and by how much, in the table itself. It is in README 43 to 46 prose. Optional: add the seven lines of ARTICLE Appendix C "The lines" or one row "Ship rule: (a) pass, (b) pass, (c) fail by 1.3 points".

## LOW

**L1. LongMemEval-S "233 of 470" counts 10 failed runs as not declined; the table row does not say so. ARTICLE line 481 and Appendix A row at line 980; MODEL_CARD 95, 108, 233; README 91, 130, 350, 361; HF_ARTICLE 122; ABSTRACT.md 15 to 16.**
`scores.json` gives `refusal_on_answerable` for 6.37 as 233 of 460 completed questions (50.7%); the papers use all 470 answerable (49.6%), the registered convention (R-170 "failures_wrong"). Appendix A states the failure convention on the rows above and below but not on this row. Fix: Appendix A row label "Declines, 470 answerable (a failed run counts as no decline)". The 30 unanswerable row likewise (the file has 29 and 27 for base and code).

**L2. Voice: three prose hits in README. Lines 312, 324, 360.**
312 "much better than base" (in H2), 324 "far above code on recall", 360 "6.37 declines far more than base". The fix list rule was no "far". Use the counts: "above code on recall (seed 82 44 to 55 of 60 against 14 to 32)" and "6.37 declines on 233 of the 470 answerable questions against base's 22". (README 283 to 297 hold recorded model replies with "very", "really", "impressive", "significant": quotes, not prose.)

**L3. Changelog ranges and panel count. README 570 to 577; ARTICLE 888 to 902.**
"15 November (R-290 to R-303)": R-290 to R-293 are dated 14 November (commits 20:52 to 22:43); R-294 is the first of 15 November. HF_ARTICLE's table has it right (14 Nov to R-293, 15 Nov from R-294). README 570 "14 November (R-218 to R-289)" should end R-293. "two review panels (R-294, R-295, R-298)" names three records: R-294 is a three-lane panel, R-295 and R-298 are ten-lane rounds; README 50 says the rounds correctly ("two of ten ... two of thirteen").

**L4. C1 card does not say its coherence sample is seed 82. MODEL_CARD_C1.md lines 63 to 64.**
"Coherence (three blind Claude Sonnet judges; the first decides), out of 120 lines each: C1 97, base 95." The table above pools three seeds; the sample (R-284, R-286) is C1 seed 82 against base. ARTICLE 633 and Appendix C say so. Add "C1 seed 82 against base".

**L5. Figure 8 (`s3_misses`) uses two shades of one teal for "Right" and "Fact in its own search output, answered wrong".**
Red and green are gone (b10eb2a M4d fixed) and the legend names both, but dark and light teal read as two kinds of good at a glance. A hue apart from the gold and grey (for example the figures' orange or purple family kept for models, so a muted rose or blue) for "answered wrong" would separate them. Optional.

**L6. Length, Kevin's call.** ARTICLE body 13,518 words (to line 914) plus 2,711 in the appendices = 16,229; the short paper 2,761. R-302 and R-303 added about 860 words to the long paper after R-300 shortened it. Neither limit is in the submit rules; the short paper is the one Kevin wants short.

## Not checked
- R-number citations beyond existence and about 25 spot checks (each cited record's claim line by line).
- The judged tables in Appendix A (single-session 43, 26, 32 and so on) against `judged.json`; coherence mark counts against `results/s3/coherence/`.
- Template-typed numbers outside the section 15 list were not enumerated; the rebuild is identical, and the typed ones I sampled (R-175, R-176, R-204, R-249, R-267, R-298) match RECORDS.
- Every README command and the notebook (not run; no GPU use).
- The demo reply table in README 281 to 297 against `results/demo/`.
