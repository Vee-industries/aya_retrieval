# Lane: Against
Recommendation: 6.37 seed 82 stays the model put forward; the case for C1 does not survive the record, so C1 goes in both papers as the tested candidate that failed one clause, with its numbers, and not as the shipped model.

Checked by me (05:30 ET, 15 Nov): R-178, R-191, R-240, R-276 to R-283, R-287, R-292 in `RECORDS.md`; git times; `results/s3/ship_rule.json`; per-seed N-hit counts from the S3 run files; my own chat-resampled interval for C1 minus base on N-hit (10,000 draws, seed 0): -3.1 to +5.7 points, matching the brief. Not checked: the claim that the scorers miss invented values.

## The case for C1, at its strongest

1. 6.37 fails clause (c) by far more than C1: its N-hit false answers are 286 of 708 (40.4%) against base's 14 of 236 (5.9%), and its copies 195 of 894 (21.8%) against base's 11 of 298 (3.7%). Keeping 6.37 keeps a model 34.5 points above base on the very line C1 misses by 1.3.
2. C1's 1.3-point miss has a 95% interval of -3.1 to +5.7: S3 cannot tell C1 from base on it. Seed 82, the seed that would ship (R-178), scores 11 of 236 (4.7%), under base. Only seed 83 (29 of 236) is above.
3. Kevin's aggregate ruling (R-278, commit 10:54) came before S3's first file (14:29). His point that he "made that call before seeing these results" is true of S3.

## Answers to questions 1 to 4

1. R-278 decided one thing: R-276's demo test is read as totals over Demo4 and Demo5 on seed 82, so C1 went on to seeds 83 and 94 and the pick (R-278: "Everything else in R-276 stands"). That chain decides which candidate enters S3 (R-191 item 3, R-192, R-194: "the dev pick names what to test; S3 is the measure"). The ship rule (R-178 item 5, R-191, R-281) decides what ships: all of (a), (b) and (c), else "6.37 seed 82 stays shipped". R-278 governs only the pick. R-280, written after R-278, restates the conjunctive ship rule at Kevin's "Yes, run S3". I could not check that Kevin read that restatement.

2. The aggregate call came before S3 but after both demo readings (R-278 discloses it; R-283 gives his reason). It was a ruling on the demo screen, which had already done its job. Using it now to put C1 forward means reading a new scope into it after the sealed result. That is a change to the ship rule, and rule 2 says "Rules are not loosened after results; any change of rule is the researcher's, made before the results it would decide". Kevin is the researcher, but the timing fails. Readings that would put C1 forward without a change: (i) "not above base's" read as "not significantly above". R-281 fixed the point-rate reading, naming it the stricter one, before any S3 file was read (commit 14:16, first S3 file 14:29). (ii) Seed 82 alone. R-178 and R-281 pool seeds 82, 83 and 94. (iii) An aggregate over S3 lines. R-178 says "All of (a), (b) and (c)". None of the three holds as written.

3. It is valid as an exploratory reading, disclosed as run after S3 and counted (rules 13, 38). It can decide nothing. 6.37 was never a pick candidate. The demos were screens, and S3 is the only ship test. If C1 beats 6.37 on the demos, (c) is still failed. If 6.37 wins, 6.37 is already shipped. The demos are small (6 older and 4 never-told questions each). K1.3 moved from 1 to 3 of 6 between them (R-257, R-277). Demo5 has been read twice and partly seen (R-277). It also costs GPU time before the 06:59 ET 16 Nov deadline at 97% weekly usage (R-292).

4. Put forward 6.37 seed 82. Both papers must say:
   - the ship rule and its registration dates (R-178, R-191, R-281), all before S3 opened;
   - C1 passed (a), (b) and two parts of (c), and failed "not above base's": 51 of 708 (7.2%) against 14 of 236 (5.9%), +1.3 points, interval -3.1 to +5.7, per seed 11, 29 and 11 of 236. That makes it a miss under the rule as written, not a measured difference;
   - base's 5.9% may be a floor, if the panel's finding on invented values holds;
   - C1 against 6.37, with counts: copies 5 against 195 of 894, N-hit 51 against 286 of 708, plain never-told 344 against 238 of 360, recall 364 against 347 of 1,242 (+1.4 points, -3.1 to +5.9);
   - 6.37's measured weakness: both fault rates are above base's;
   - R-276 and R-278 were set after the demo readings and decided only the pick;
   - K1 and K2.1 were report arms with two seeds and no coherence test, so no ship claim rests on them (R-292);
   - Kevin's view after S3 that the aggregate should win, given as his view and not applied. If he rules otherwise, the papers must call it a rule change after the sealed result (a deviation row, rule 26). They must not say C1 passed S3.

## The strongest point against my recommendation, and why it does not change it

Shipping 6.37 ships the model with the worse fault rates (40.4% N-hit against C1's 7.2%) because of a 1.3-point gap that S3 cannot resolve. On substance, C1 is the better model for users. That does not change the recommendation. R-178 chose this outcome in advance ("S3's numbers on 6.37 go in as its measured weakness"). Rule 2 makes a miss by one line a miss. Rule 8 lets the papers state C1's advantage in full without a ship claim. If the rule is loosened now, every earlier sealed verdict in the record loses its meaning.
