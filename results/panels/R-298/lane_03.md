# Lane 3: Evaluation and leakage specialist (hostile)
Verdict: submit after fixes

## Round-1 findings: status
F1 partly: relabelled to "names a value listed for the chat" (ARTICLE.md:62, 636, 668; HF_ARTICLE.md:199; ABSTRACT.md:23-24), and the limits now say base's rates are floors (ARTICLE.md:801-804, HF_ARTICLE.md:239-242). The counts R-295 B asked for ("a limits paragraph with the counts") are not there. Unqualified wording remains: ARTICLE.md:76, 86, 326 ("answered with a value"), 693 ("names a value on 121 of 236"); HF_ARTICLE.md:59; MODEL_CARD.md:199.
F2 partly: tables say "names no listed value" (ARTICLE.md:636, 669; HF_ARTICLE.md:200; MODEL_CARD_C1.md:36); ARTICLE.md:189 fixed; the ceiling is stated (ARTICLE.md:803). Still "declines": ARTICLE.md:680 ("Plain never-told declines ... (+45%)"), ARTICLE.md:320, README.md:80 ("declines a plain never-told question rightly 344 times in 360 against 238"). See new F2.
F3 partly: copy now defined as naming the wrong value "when answering another question" (ARTICLE.md:115-116, HF_ARTICLE.md:87-88). No re_ask result is reported anywhere; `grep -n re_ask` finds only the definition and the item count (ARTICLE.md:116, 229). Recomputed (`l03/plain_nt.py`): re_ask right, base 1/60, whole chat 17/60, code 23/60, 6.37 6/180, C1 110/180, K1 61/120, K2.1 71/120.
F4 fixed: ARTICLE.md:242; "made by the same generator" in ABSTRACT.md:5-6, ARTICLE.md:15-16, HF_ARTICLE.md:6 and 105.
F5 fixed: ARTICLE.md:244 and 808-809; HF_ARTICLE.md:248. Tiny Aya's release date still not verified by me.
F6 fixed: ARTICLE.md:806.
F7 fixed: ARTICLE.md:239 ("found and reduced").
F8 fixed: ARTICLE.md:240.
F9 fixed: the coherence sentence is gone from ABSTRACT.md.
F10 fixed: ARTICLE.md:117-118, HF_ARTICLE.md:152-153.

## New findings (most severe first)
F1. [BLOCKER] ARTICLE.md:70-71 and README.md:110-111 ("Built: ... decline what it was never told"); ARTICLE.md:444-446 ("Training's gain is when to search ... `never_told` worse (p = 0.11 and 0.0042)"); MODEL_CARD.md:130-132 ("Training adds ... on facts never told 37 and 36 against 31 and 24"); README.md:327; the "Never told, of 40" rows at ARTICLE.md:421, 430, HF_ARTICLE.md:121, MODEL_CARD.md:71, README.md:136. The outside-writer never-told column uses the same lenient scorer (right = names no listed value), and the limits paragraph names only S3 and the first sealed test. On those sets the shipped seed almost never declines; its high count is fault 1 of R-177 (an unrelated stored fact), scored right.
    Evidence: `l03/blind_nt.py` on `results/recall_eval/{blind,blind2}_{base,fix17cs37_82}_seed_0.json` and `as_*`. 6.37 seed 82 scored right on 37 and 36 of 40. Only 3 and 5 hold a decline phrase. I read the other 65: 64 state another fact or invent one ("Your brother Wei bought a mustang." to "what does wei do for work"; "Your uncle Ming's car is a Bentley."; "Ingeborg works as a typer"), and 1 hedges. Base with the tool: right 34 and 32, decline phrase 12 and 11; base also invents ("Olumide is a software engineer."). Code: decline phrase 3 and 1. On S3 plain never-told, decline phrase: 6.37 29 of 360 (8.1%), base 33 of 120 (27.5%), C1 at least 257 of 360 (`l03/plain_nt.py`; 15 of 6.37's 209 no-phrase rows read, 0 declines). The regex is rough and I am one Claude reader, not blind to arm.
    Fix: drop "decline" from the "Built" line for 6.37, or say it was trained to decline and on outside chats does so on 8 of 80 never-told questions. Relabel the never-told rows "names no listed value". Replace "Training's gain ... `never_told` worse" with the decline counts above. Extend the limits sentence to the outside-writer sets and `hard_dev` (Figure 4's "declines", ARTICLE.md:604, HF_ARTICLE.md:177).

F2. [MAJOR] ARTICLE.md:680, ARTICLE.md:320, README.md:80, HF_ARTICLE.md:206-207: C1 against 6.37 on plain never-told, "+45%", is given as a change in declines. By decline phrase the change is 29 to at least 257 of 360. The registered line's reading stands, but the stated size does not.
    Evidence: as F1.
    Fix: say "names no listed value" at these lines. Add one sentence with the decline-phrase counts to the limits paragraph at ARTICLE.md:801-804 and HF_ARTICLE.md:239-242.

F3. [MINOR] ARTICLE.md:236-244 (leakage table): S3's text was used to build later candidates' training sets. R-206 dropped every row that shares a six-word run with S3 (K3.1 and later builds; check line 5), and four-word counts were read per candidate before the choice. The table says preprocessing on all data is "not present for the model" and gives only 6.37's overlap (140 of 42,561). C1's own set, K1.3's rows plus OP's corrections, has no stated overlap. R-206 gives K1.3 148 four-word runs. I found no count for C1's set (searched RECORDS.md past line 9600 for "with S3", "S3 shares" and "overlap_s3").
    Fix: add to the duplicates row: "later candidate sets dropped rows sharing a six-word run with S3, counts only (R-206); C1's set, K1.3's rows, shares 148 four-word runs".

F4. [MINOR] ARTICLE.md:243: "the sealed pools are generator-built" reads as covering S3, which is writer-built.
    Fix: "the first sealed test's pools are generator-built".

F5. [MINOR] ARTICLE.md:140 and MODEL_CARD_C1.md:27 say 6.37 names "values from passages" on never-told questions. The N-hit flag checks values listed for the chat, not what the passages held.
    Fix: "values listed for the chat".

F6. [MINOR] README.md:324 and MODEL_CARD.md:125-126 still say code "recalls as well as" 6.37. R-295 A9 changed this to "no measured difference" in the papers.
    Fix: the same words in both files.

## What holds up
- S3 table counts match the run files: copies 11/298, 195/894, 5/894; N-hit 14/236, 286/708, 51/708; plain never-told 111/120, 238/360, 344/360.
- The leakage table now states within-generator non-independence, LongMemEval-S predating the model, R-254's demo caveats and R-180's residual gap.
- The limits now say no person checked S3's flags and that base's listed-value rates are floors.
