# Lane 2: Statistician and experimental designer (hostile)
Verdict: submit after fixes

Commit 8735c87. Recheck script: `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\3fe62a52-aba3-4a62-8744-fec0f4500b98\scratchpad\panel3\l02\recheck_s3.py`
(read-only, reads `results/s3/` only; chat-resampled, 10,000 draws, seed 0, as R-281). Every S3 count in the abstract,
the short paper and section 9 reproduces from the run files, including the new 6.37 seed 82 column, the per-seed rows,
the report arms, "confirm" searches 7, 0, 5 and 52, 37, 52 of 58, own-query finds 480 of 1,242 against code's 260 of
414, and C1 minus base on (c) +1.3 [-3.1, +5.7]. The 419-message counts (52, 52, 46, 44 against 32, 30, 17, 14) and
code of 120 (29 to 64) match `results/analysis/R-168/refs.json`.

## Round-1 findings: status
F1 fixed: ABSTRACT line 30 "Both sealed tests and their rules were registered before they ran; rules changed after some development readings are disclosed".
F2 partly: (c)'s interval is now in every document (HF 17-18, 207-209; ARTICLE 37, 659). The three (a) lines C1 "passed" still carry no interval; ARTICLE 684 "passed (a)'s statement line by 0.6 points", while C1 minus base on statement is -4.4 [-10.6, +1.7] (in_view +2.2 [-6.1, +11.1], plain never-told +3.1 [-2.5, +9.2]). The interval is given only where it softens a fail (new F3).
F3 fixed: HF 214-217, ARTICLE 707-711.
F4 partly: ARTICLE 661-671 has the shipped-seed table and "judges the recipe". The short paper gives only per-seed N-hit counts (HF 209-210); C1 seed 82's statement shortfall is absent from the short paper and the abstract (new F2).
F5 fixed: HF 132-137, "a stratified 248 of the 500", the split labelled post hoc. The abstract (line 16) still gives 53 of 248 without "stratified".
F6 partly: HF 43 and ARTICLE 120 still read "a sealed test opened once (the first sealed test and S3)".
F7 partly: "as well as" is gone from both papers but stays in README 113 and 324 ("recalls as well as 6.37", p = 0.76 and 0.45). README 74 still "under two seeds' spread"; HF 186 and ARTICLE 623 "inside the seed-to-seed spread" with no number. HF 178 and ARTICLE 594 still argue from overlapping intervals. C1 minus 6.37 recall +1.4 [-3.1, +5.9] is not printed.
F8 not fixed: ARTICLE 308-312 and 337 say nothing about rule 1's pooled sign test counting each base row eight times.
F9 partly: ARTICLE 684 says "120 sampled items"; neither paper says the coherence arm is C1 seed 82 only (R-286 "C1 seed 82"), not the pooled recipe the other lines judge. HF 202 has neither.

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md:11 ("When the chat fits, the untrained model shown the whole chat recalls more than either"), HF:57 ("The chat fits the context: show it whole, with no adapter"), ARTICLE.md:694 ("when the chat fits, show it whole"): these generalise past the evidence. On the first sealed test's 58-message chats (1,105 to 1,332 tokens, which fit), base with the whole chat recalls 33, 28, 21, 22 of 60 against seed 82's 54, 55, 46, 47, every p below 2e-5. The README states the opposite of the short paper.
    Evidence: `results/analysis/R-168/refs.json` (`whole_chat/sizes/58`); ARTICLE 393, 405-407; README 318-320 "holds on the outside-writer chats, not on this project's generated chats".
    Fix: "When the chat fits and was written outside the generator (two outside-writer sets and S3), show it whole; on the generator's 58-message chats seed 82 recalled 46 to 55 of 60 against the whole chat's 21 to 33."
F2. [MAJOR] HF_ARTICLE.md:19, 28, 59-60 and ABSTRACT.md:26-27 call the published C1 "labelled as failing that clause". The published adapter is seed 82. On its own it passes (c) (11 of 236, 4.7%, against base's 5.9%). It fails (a)'s statement line: 50 of 60 (83.3%) against the 91.7% line, C1 seed 82 minus base -13.3 points [-23.3, -3.3]. That is the only C1 shortfall against base whose interval excludes zero. The short paper and the abstract never say this. The C1 card (MODEL_CARD_C1.md:38, 51-52) and ARTICLE 671 do.
    Evidence: `recheck_s3.py` rows `C1_82`, interval `C1_82 - base statement`.
    Fix: in HF section 6 and its top paragraph: "The published C1 is seed 82, which on its own is under base on (c) and searches on 10 of 60 plain statements, below (a)'s line."
F3. [MAJOR] ARTICLE.md:684, HF_ARTICLE.md:202 ("Every other line passes"), section 9's PASS list: the papers report (c)'s interval to show that the fail is within noise, but they report none for (a)'s passes. Those passes are just as unresolved: statement -4.4 [-10.6, +1.7] reaches past the 5-point margin. Giving the interval on one side only favours C1.
    Evidence: `recheck_s3.py` intervals block.
    Fix: one line under the PASS list in ARTICLE section 9 and HF section 6 with the three (a) intervals: "S3 cannot show C1 within 5 points of base on statements either."
F4. [MINOR] HF_ARTICLE.md:187-188, ARTICLE.md:624-625: "so what ships did not depend on the change" rests on two of K1.3's three registered seeds. Pooled over three seeds, K1.3 passes "not above base's" if its third seed names a listed value on 5 or fewer of 236 (42 of 708 equals base's 5.93%). Its two seeds gave 9 and 28, so the claim very likely holds, but it is an inference. K1.3 minus base is +1.9 [-3.2, +7.0], the same "cannot tell" as C1.
    Fix: add "(a third seed would have needed 5 or fewer of 236; its two gave 9 and 28)".
F5. [MINOR] ARTICLE.md:707-711: the report-arm paragraph omits the one measured S3 difference among the candidates. At matched seeds 82 and 83, K1 (R-178's candidate, dev pick recall 720) is below C1 (775) on (c) by -5.9 points [-9.7, -2.5], with no measured recall difference (-0.7 [-5.2, +3.8]). The registered pick ranked them on a development lead the papers call inside seed spread.
    Fix: one sentence with these two intervals, labelled exploratory.
F6. [MINOR] README.md:107-120 ("For judges: one minute") gives no S3 rate for 6.37. R-297 says those rates are "stated in every document". The README gives 40.4% only at line 78 and never gives 21.8%.
    Fix: add the two S3 rates against base to the "Where it fails" bullet.

## What holds up
S3's counts, the per-seed rows and every interval the papers print reproduce exactly. The ship-rule verdict follows `ship_rule.json` as registered.
The LongMemEval split is internally consistent: 40 + 13 = 53, 32 + 2 = 34, 40 + 0 = 40, and 19 - 8 = 11.
The first sealed test's per-cell base rates (8.3 to 28.3%) and seed 82's 91 to 107 of 120 match R-162 and R-168.

Not checked: LongMemEval-S counts against their files (`results/longmemeval/` is closed to this panel); the figures' intervals; the abstract and short-paper word counts.
