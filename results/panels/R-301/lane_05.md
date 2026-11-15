# Lane 5: AI safety and alignment reviewer (hostile), round 3
Verdict: submit after fixes (no blocker; two MAJOR, three MINOR)

## Round-2 findings: status (one line each)
F1 fixed: HF_ARTICLE.md:99-101 and 150-152, ARTICLE.md:692-695, Appendix C (ARTICLE.md:954), MODEL_CARD_C1.md:52-53 and 57-61 now say what the flag counts, both directions, with counts. `panel4/l05/offcat_wc.py` reproduces every count (base 17, 6.37 402 = 135+126+141, C1 99 = 25+48+26, K1 32, K2.1 37).
F2 partly: deviation row 20 added (ARTICLE.md:668), HF:152-154 and ARTICLE.md:118 say the scorer does not check for a decline. One label still says "declines" (new F2).
F3 fixed: MODEL_CARD_C1.md:27 now says "unrelated stored facts".
F4 not fixed: "instructions in retrieved passages not tested" is still only in the method text (HF:41-42, ARTICLE.md:207), not in HF section 7 or ARTICLE.md section 12's "Not probed" list.

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md:15 ("show it whole, with no adapter") and ARTICLE.md:592-593 ("show the chat whole"): the advice is made on recall alone. On S3 the whole chat names a listed value on 57 of 236 (24.2%) N-hit never-told questions, against base with the tool 14 (5.9%) and C1 51 of 708 (7.2%), and passes only 89 of 120 (74.2%) plain never-told questions against base's 111 (92.5%). No text in either paper gives these numbers; only Figure 5's dot shows 57/236. The text at ARTICLE.md:591 names code's fault rates but not the whole chat's. In a safety write-up, the first line of advice points to the arm with the second-worst never-told rate without saying so.
    Evidence: `results/s3/s3_whole_chat.json`, `panel4/l05/offcat_wc.py` (flagged 57 of 236; plain never-told right 89 of 120; copy 2 of 298); grep for "57 of 236" and "89 of 120" in ARTICLE.md, HF_ARTICLE.md, README.md, MODEL_CARD.md: 0 hits.
    Fix: HF:15, after "show it whole, with no adapter", add "(on S3 it then names a listed value on 57 of 236 never-told questions, base with the tool 14)". Add the same clause to ARTICLE.md:591-593.

F2. [MAJOR] ARTICLE.md:577: "Plain never-told declines: 238 of 360 (66.1%) to 344 of 360 (95.6%) (+45%)". These counts are replies naming no listed value; the scorer does not check for a decline (ARTICLE.md:118, deviation 20). My round-2 word-list count found 66 of C1's 344 with no decline word. The sentence states a measured decline rate that S3 did not measure.
    Evidence: ARTICLE.md:118, 668; `panel3/l05/nodecl.py`.
    Fix: "Plain never-told questions answered with no listed value: 238 of 360 ...".

F3. [MINOR] MODEL_CARD_C1.md:40: "-97% on the first fault and -82% on the second" makes the copy the first fault. HF_ARTICLE.md:100 and ARTICLE.md:693 call the never-told fault the first. A reader comparing documents reads -97% as the never-told cut.
    Fix: "-97% on copies and -82% on N-hit false answers".

F4. [MINOR] HF_ARTICLE.md section 7 and ARTICLE.md section 12: injection not listed as untested (round-2 F4), and neither paper has one sentence on why the faults matter for safety (HF:32-42 gives only the context-window use). Fix: one bullet: "Not tested: instructions hidden in retrieved passages. A value given as something the user said, when the user never said it, is a false memory the user may act on."

F5. [MINOR] ABSTRACT.md:24 calls C1 "The pick" with no sign that C1 became the pick only after the demo test was changed twice after both models' readings (HF:117-121, deviation 11); ABSTRACT.md:30-31 says only that changes are disclosed. 465 words, so room exists. Fix: "The pick, C1 (chosen after a demo rule changed once both models' readings existed), cut these ...".

## What holds up
Every S3 number in the papers' fault rows and the new other-stored-facts counts reproduces from `results/s3/`.
The demo-rule change is told in its two steps (HF:117-121), and C1 seed 82's own failure on (a)'s statement line is disclosed in every document that names it.
Appendix C holds what the body points to (the rule lines, the shipped seed's lines, `re_ask`, other stored facts, report arms per seed).
