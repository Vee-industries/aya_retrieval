**Evaluation and statistics expert, round 2** (read-only; no forbidden file and no result for seeds 97 to 99 opened)

**Checks against the files**
- **Data expert: every number I checked is right.** All 28 ids exist as `in_view` rows, and 10 of them open "It sounds like". In the 66 in-view misses (both sets, five seeds), the five deflection phrases appear 10, 9, 14, 4 and 8 times. In the training targets they appear in 1, 1, 4, 4 and 4 rows. "a bit lost or confused" comes from one row (0122) and appears in 9 misses. This is the strongest evidence of a cause on the panel.
- **Recipe expert:** its 18 deflecting rows are a subset of the data expert's 28. One small error: at 82 and 83 the `hard_dev` misses open "It sounds like" 12 times of 14, not 11.
- **Dialogue expert: its 44 rows are chosen by the opening words, and that fails both ways.**
  - It includes 12 "It sounds like" targets that state the value ("...your cousin Nell is a loyal Yamaha owner").
  - It leaves out 6 clear deflections the data expert caught: 0027, 0058, 0060, 0064, 0099 and 0132. For example, 0058 is "Can you try to recall any details about Marble's name?".
  - 57 correct `hard_dev` replies also open "It sounds like", so filtering on the opener is the wrong test.
- **Retrieval expert:** 47 found-fact misses (19, 3, 14, 5, 6 by seed) is right. But its rows copy the shape of three `hard_dev` fact types. Seeds 97 to 99 read those same items, so a gain there would not be independent evidence.
- **Against expert:** the sign tests are right (p = 0.057 and 0.23). Its R-099 item 7 point is too broad: that cut-off applies to a messy-typing arm, not to rewriting in-view targets.
- **The 15% to 20% estimates** from the data, dialogue and retrieval experts all leave out two lines a 7 can fail on luck alone at 97 to 99. Even an exact copy of 6.37 passes the recall line against 6.37 only about 0.51 of the time on `hard_dev` and 0.74 on the probe, and the per-seed phone floor about 0.65.

**1. Final position: no 7, by expected value.** If the chair picks a fix, the only one I would vote yes on is the data expert's rewrite of the 28 targets.
- It leaves the row count, the kind mix, the no-search decisions and the user messages unchanged, and it uses no "Your ..." frame.
- I would merge in the dialogue expert's filters: drop any target sharing a four-word run with the probe or `hard_dev` pools, and require a blind-judge pass. A row that fails the judge keeps its old target.

**2. Strongest objection (against expert): five in-view edits, five trade-offs.** My answer: none of those edits rewrote only the deflecting targets in place. Still, the risk lands on the coin-flip `hard_dev` recall line, and R-120 and R-121 put that cost at 3 to 4 standard deviations.

**3. Probability.** It moves from about 3% to about 5%, given the copied-phrase evidence. To beat noise over five seeds, the fix must lift `hard_dev` in-view by about 3 per seed, removing about 40% of the 8 misses per seed. Of the gate lines, it reaches only R-097 (probe in-view at least 41).

**4. To vote yes, I need these registered before any row is built:**
- 6.37 retrained at 97, 98 and 99 from the byte-identical set and code, queued first, on a card it does not share.
- The recall comparison pooled over three seeds, ties passing. If 6.37's runs there do not finish, the 7 fails.
- The reference at 82 and 83 fixed now, preferably 6.37's 192 and 163.
- `hard_dev` in-view and lower-case in-view reported against 6.37's own seeds with this noise figure, and not claimed as gains below about +3 per seed.
- Disclosure that the targets were found by reading misses on items that 97 to 99 reuse.