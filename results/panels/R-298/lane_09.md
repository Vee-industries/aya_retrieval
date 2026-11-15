# Lane 9: Against (hostile, the strongest case against submitting as is)
Verdict: submit after fixes (N1 to N4 are text only; do not submit with N1 or N2 standing)

## Round-1 findings: status
F1 fixed: ABSTRACT.md:27-28; HF_ARTICLE.md:214-217 ("did not predict S3 on that line"); ARTICLE.md:706-712; K1 named in HF "Not done" (255-257).
F2 partly: S3 faults against base now in ABSTRACT.md:22-24 and HF:13-16; first test named generator-built (ABSTRACT:5-6). Not fixed: neither the abstract nor HF "Result first" says code beats both trained models on S3 recall, and that gap is a measured difference (N1).
F3 partly: code (40, p = 0.12) added to ABSTRACT:15-16 and HF:10-11, 132-137. The abstract still leaves out the answerable split (40 against 40) and "stratified 248 of 500" that R-295 A8 asked for; 19 words of room remain (481).
F4 fixed in the abstract (30-31) and HF section 7 (243-244). It is not fixed in ARTICLE.md:148-149 or README.md:76 (N2).
F5 fixed in wording: HF:239-242, ARTICLE:801-804, ABSTRACT:28. Its size is not given (N3).
F6 fixed: ARTICLE.md:50 "code: 29 to 64 of 120".
F7 fixed as deviation 19 (ARTICLE:778). The row is now wrong the other way: the S3 "Every arm" table (ARTICLE:635-644) lists code and whole chat first (N5).
F8 partly: a names line was added (HF:89-90) and pick recall is defined (HF:185). "742", "775" and "868" still have no n; the short paper is 3,957 words (wc), with R-297 saying the checklist items exceed the 5 pages.
F9 fixed: HF:43 "(the first sealed test and S3)"; HF:266-267 "and my chat engine LLE"; no "first sealed test, S3" left in any document (grep).

## New findings (most severe first)

N1. [BLOCKER] ARTICLE.md:72-73 (summary, "For judges: one minute"): "code that searches every turn shows no measured difference from 6.37 and is faster. The same holds on S3." That is false. On S3, code 161 of 414 (38.9%) against 6.37 347 of 1,242 (27.9%) gives +11.0 points, chat-resampled 95% interval +3.5 to +18.6. Against C1 (29.3%) it gives +9.6, interval +2.4 to +16.6. ARTICLE:787 contradicts it the other way: "the whole chat and code beat the adapters on short written chats (sections 6.2 and 9)". Section 6.2 shows no measured difference from code (p = 0.76, 0.45). So on S3, the one sealed test from outside writers, both trained models lose on recall to a baseline that trains nothing. The papers say "both above" (HF:220, ARTICLE:684) but give no interval, and the abstract does not say it.
    Evidence: score_s3.py's own `lower_bound` and `rate` on results/s3 (script: scratchpad/panel3/l09/code_vs.py, read only).
    Fix: ARTICLE:73: "On S3 code recalls more than 6.37 and C1 (+11.0 and +9.6 points, 95% +3.5 to +18.6 and +2.4 to +16.6)." ARTICLE:787: "the whole chat beats the adapters on both; code ties them on the outside-writer sets and beats them on S3." Put the same clause in ABSTRACT paragraph 3 and HF "Result first", and the intervals in HF:220.

N2. [BLOCKER] ARTICLE.md:148-149 (contributions): "with the ship rule and its scorer fixed before it opened". README.md:76 says the same: "scored by a rule and scorer fixed before it opened". ARTICLE:628-630 and deviation 13 say that no scorer existed when S3 started. This is the round-1 F4 fault, still present in two places.
    Fix: "its ship rule fixed before it opened and its scorer fixed before any S3 file was read (deviation 13)".

N3. [MAJOR] HF:240-242, ARTICLE:801-804: "The untrained model invents many" is stated without a size, and the size changes how a reader takes every base comparison on never-told questions. Of base's 240 counted S3 never-told rows, 225 are scored right. I read 20 of those 225, drawn at random (seed 21). 14 are not declines: "Rhys loves pizza.", "Esperanza drives a Jeep.", "Bongani plays guitar.". A regex for any decline wording finds one in 79 of base's 240 rows, 82 of 6.37's 720 and 573 of C1's 720 (heuristic, my reading, after the results). Three consequences follow. Clause (c), which C1 failed by 1.3 points, compares C1 with a base that answers most never-told questions with invented values. "6.37 does worse than the untrained model on both faults" is true only for listed values. And C1 still gives the demo's fault, an unrelated stored fact ("is priya dealing with any health stuff" gets "Your wedding is in September."), on about 97 of the 669 rows scored right. The papers soften C1's comparison with base and say nothing of what C1 left unfixed.
    Evidence: scratchpad/panel3/l09/nt_decline.py, nt_invent.py; results/s3/s3_base_tool.json.
    Fix: one sentence with a hand count in HF section 7 and ARTICLE section 12. For example: "Read by hand, 14 of 20 randomly drawn base replies scored right on never-told name an invented value; C1 still gives an unrelated stored fact on some (exploratory, read after the result)."

N4. [MAJOR] HF:57-59, ARTICLE:79-81 "Use this when": "It does not fit: 6.37 ... recalls more than code on generated chats too long to show whole on this card". Those 419-message chats fit the model's 8,192-token window (ABSTRACT:8, R-166). A reader who goes by the box's first line ("fits the context: show it whole") should show them whole. The only chats that really do not fit the window are LongMemEval-S's, where 6.37 ties code on the answerable questions (40 against 40). The box gives a win for "does not fit" that no test of chats beyond the window supports.
    Fix: "Beyond the 8,192-token window (LongMemEval-S): no measured difference from code. Inside the window but too large for a 10 GB card (generated chats only): 6.37 above code."

N5. [MINOR] Deviation 19 (ARTICLE:778) says "Trained arms first in the tables", but the S3 table puts code and whole chat first. The deviation is in the text order (section 9 gives the rule and C1 before "The strongest baselines on S3").
    Fix: "Baselines first in the table; the text gives the rule and C1 before them."

N6. [MINOR] README.md was left out of R-297's fixes, though R-297 says the S3 weakness is "stated in every document" and that "as well as" was replaced. README:113 and :324 still say "recalls as well as". README:80 says "declines a plain never-told question rightly", which N3 shows is not what the measure counts. The README never gives 6.37's S3 copy rate against base (21.8% against 3.7%). README:113 says "best" where R-297 changed it to "most".
    Fix: apply A2, A9 and B of R-295 to the README.

N7. [MINOR] ABSTRACT:7 "Every registered rule of that test passed" carries no note that the never-told counts are upper bounds (HF:242 gives that note).
    Fix: add "(never-told counts are upper bounds)" if words allow, or drop it in favour of F3's split.

## What holds up
- Every S3 count I recomputed matches the papers: confirm searches 7, 0, 5 and C1's 52, 37, 52 of 58; found fact 141, 180, 159 (480 of 1,242), code 260 of 414; all arms' six measures.
- The first sealed test's numbers: code of 120 (64, 61, 37, 29), base 13 to 32, and seed 82's 52, 52, 46, 44 at 419 messages all match ARTICLE:393-401.
- The demo change in two steps, K1.3 failing (c) (37 of 472), and the per-seed lines are stated plainly in both papers.
