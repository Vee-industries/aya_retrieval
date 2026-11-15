# Lane 3: Evaluation and leakage specialist (hostile)
Verdict: submit after fixes

## Round-2 findings: status (one line each)
F1 partly: fixed in ARTICLE.md:71-73, README.md:77-79, ARTICLE.md:415-417 (hand read of 8, R-298), HF_ARTICLE.md:94-96, README.md:107 (relabelled), and the limits (ARTICLE.md:696-697: first sealed test and outside sets are upper bounds). Not fixed: MODEL_CARD.md:71 ("Never told, of 40"), MODEL_CARD.md:130-134 and README.md:297-299 ("Training adds ... on facts never told 37 and 36 against 31 and 24"); Figure 4's caption, ARTICLE.md:503 and 515 ("declined", "never-told declines"), although `hard_dev` uses the same rule (`src/aya_retrieval/scoring.py:60-61`, `not names_forbidden`).
F2 partly: README.md:80 and HF_ARTICLE.md:133 now say "names no listed value". ARTICLE.md:576-577 still says "Plain never-told declines: 238 ... to 344 of 360 (+45%)". By decline phrase it is 29 to 257 of 360 (rerun of `panel4/l03/plain_nt.py`, same counts as round 2). ARTICLE.md:328 still says "a fact never told declined".
F3 not fixed: ARTICLE.md:246 and 704 give only 6.37's overlap (140 of 42,561) and say "counted, not removed"; R-206 (RECORDS.md:8358) removed six-word S3 runs from K3.1 and later builds; C1's set (K1.3 rows plus OP) has no stated count.
F4 fixed: ARTICLE.md:251.
F5 fixed: `grep "from passages\|values from"` finds nothing.
F6 fixed: `grep "as well as"` finds nothing in README or MODEL_CARD.

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md:160: "the only human marker is me" is false. R-145 (RECORDS.md:5536-5551) records an independent second person who marked the same 50 scorer lines blind (48 of 50 with the scorer, kappa 0.92). ARTICLE.md:712-713 says "The only human marker is me" and then names the second marker in the next clause, which contradicts itself.
    Evidence: R-145; ARTICLE.md:688 ("two human markers"); MODEL_CARD.md:217-219.
    Fix: HF_ARTICLE.md:160 and ARTICLE.md:712: "two people marked 50 development scorer lines: me, not blind to the hypotheses (47 of 50), and one independent marker (48 of 50, R-145)".

F2. [MAJOR] ARTICLE.md:695-697: the limits call base's plain never-told rate a ceiling and the first sealed test's and outside sets' never-told counts upper bounds, but leave out S3's adapter rows. 6.37's 238 and C1's 344 of 360 are also ceilings: 209 of 6.37's 238 and 87 of C1's 344 hold no decline phrase (`plain_nt.py`). With ARTICLE.md:577's "declines", this is the one S3 measure still read as declining.
    Fix: add "and S3's" to line 697's list; give the decline-phrase counts once (6.37 29 of 360, C1 257 of 360, base 33 of 120; rough regex, one Claude reader).

F3. [MINOR] ARTICLE.md:695: "(counts in Appendix C)" follows a sentence about both flags, but Appendix C (ARTICLE.md:948-949) counts other stored facts on N-hit questions only. No count is given for copy or plain never-told items.
    Fix: "(counts for N-hit questions in Appendix C)".

F4. [MINOR] ARTICLE.md:252: "the project's own chats were written after its release" has no source. The local cache shows the weights downloaded 2026-11-01 10:45 (R-003, `snapshots/af89d219...` mtime), so the release came before every chat, but the table cites nothing.
    Fix: cite R-003 (weights downloaded 1 November, before any chat was written).

F5. [MINOR] README.md:86: "names its in-view wrong value on 21.8% of questions" leaves out the denominator, the 298 wrong-view items of S3's 834.
    Fix: "on 21.8% of wrong-view questions".

## What holds up
- Rerun on the run files: outside never-told right 37/36 (6.37), 34/32 (base); S3 plain never-told 111/120, 238/360, 344/360; re_ask 1, 17, 23, 6, 110 (Appendix C matches).
- Report-arm sums in Appendix C match section 9 (K1 12, K2.1 14, K1.3 37 of 472).
- The leakage table now names within-generator non-independence, Claude-only writers, the demo keys and LongMemEval-S's date.
