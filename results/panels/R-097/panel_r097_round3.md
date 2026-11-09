# Fix C panel, round 3: the merged plan (accept, or name the smallest change)

1. **C1 = fix A's set minus 15 rows**: the 14 non-slip CuratorKIT rejections and A's one rejected rewrite
   (`older_0043`). Nothing new is written; A's other 26 rewrites stay; every `in_view`, `statement` and
   `never_told` row is byte-identical to 17m's; the 15 dropped rows are listed; `slip_shape` reads 0 on the set.
   [lane 2's round-2 plan; drop was lane 4's fallback; lane 3 accepted drop as a run; lane 1 objected that it
   moves the `older` count from 200 to 185]
   No CuratorKIT re-check is needed for C1, since no answer is new; the remaining 335 answers are the ones the
   R-096 judges already passed.
2. Seed 82, counts only: stop without judging if any R-086 count or slip-gate item fails, or probe `in_view` is
   below **41** (17m's at 82; A had 39). [lanes 1, 3, 4 at 41; lane 2 asked for 40]
3. Seed 83, counts and slips, same stop rule. Then R-086's judged sheets for C1 at 82 and 83, as registered
   (two-model sheets against base, judge 1 decides, judges 2 and 3 reported), read against A's R-095 sheets. A
   one-line miss is a miss.
4. If C1 passes: seeds 88, 89, 90 for R-076's rule and the pooled slip gate; seed 87 not run (A's 87 already
   reported the tail). If C1 passes there, it replaces v6 under Kevin's ruling; otherwise v6 stands.
5. **If C1 stops at step 2 or 3: C2** = A's set with the same 15 rows given the scripted "Your {relation}
   {person} ..." answer, built only after this pre-train acceptance test: a fresh three-judge CuratorKIT re-check
   on one blind sheet of the 15 new answers, the 22 original rejections as hidden controls and about 20 passing
   answers; go only if all 15 pass at 2 of 3 and at least 18 of the 22 controls are rejected (a failed control
   voids the sheet). Then steps 2 to 4. A second failure ends the track: v6 stands. [lanes 1, 3; lane 2 conceded
   scripted as the fallback]
6. Write-up: CuratorKIT is a data-quality audit and acceptance test on the training targets with Claude verdicts
   (saved and replayable), not an independent check of the model and not a pipeline stage; no claim that the
   faults cause the slips; every candidate-seed counted. The write-up work goes first if GPU time and it compete.
   [all four]

Reply in under 120 words: ACCEPT, or ACCEPT IF with the one smallest change and its reason.
