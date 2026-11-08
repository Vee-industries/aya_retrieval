**Case against, round 2: still no 7, but I would vote yes on the data expert's 28-row rewrite, under the conditions in item 4**

**Checks on the other reports** (read from `fix17cs37.jsonl` and the 6.37 result files):

- **Data: confirmed.**
  - All 28 row ids exist.
  - Their targets average 31.9 words, against 19.5 for the other 122.
  - Over 66 in-view misses, its five phrases occur 10, 9, 14, 4 and 8 times. "a bit lost or confused" comes only from row `in_view_0122`.
  - The recipe expert's 18 rows are all among the data expert's 28.
- **Dialogue: its 44-row set is wrong for about a dozen rows.** It includes all 22 "It sounds like" rows, and many of those state the value:
  - `0001` (fantasy novels)
  - `0033` (geometry)
  - `0049` (surveyor)
  - `0096` (candle shop)
  - `0127` (chemistry teacher)

  These are among the good answers 6.34 removed. `hard_dev` in-view was 44 and 34 for 6.33 and 38 and 31 for 6.34 (78 to 69). So rewriting them repeats 6.34's risk.
- **Retrieval: fitted to `hard_dev`.** Its "event, then value" form was chosen from the three `hard_dev` fact types it then targets (45 of 47 misses), and seeds 97 to 99 score those same items. It also edits found-fact rows, which carry the line most at risk.
- **Recipe's audit note.** It reported a glob that matched a file with "token" in its name. Its transcript audit should record that.

**1. Final position.** On expected value, still no 7. If the chair picks a fix, the only one I would not block is the data expert's version:
- the 28 ids it lists, with only the final assistant turn changed;
- hand-written direct answers, with the value in the first sentence;
- no question, no feeling sentence, no "Your ..." opener;
- everything else byte for byte: 1,094 rows, `decision_rows` 222;
- 6.37's recipe, trained from scratch.

**2. Strongest objection to my position, and my answer.** The data and recipe reports trace the deflections to specific rows at full loss. I verified that, and it is the smallest in-view edit tried so far. A fail costs little: 6.37 keeps shipping, and the clock fits. I accept that. My remaining objection is the statistics expert's: the in-view lines are not gate lines. A copy exactly as good as 6.37 passes the full gate only about 3% of the time. A perfect in-view fix raises that by about one point, and a recall cost of 3 a seed lowers it.

**3. Probability.** For the data expert's fix, about 6% (the data expert says 20%). I lowered mine from 5% for "any 7" to a figure for this design. It is narrow and its cause is traced, but most of the gate risk is seed luck on lines it does not touch. The statistics expert's product, about 12% to 16% at 82 and 83 and about 18% at 97 to 99, is a fair reckoning; the data expert's 20% does not account for it.

**4. What the chair's design needs for my yes vote:**
1. **Exactly the 28 ids.** Not dialogue's 44: no rewrite of a target that already states the value.
2. **Vetting.** One fresh blind judge vets the 28. A rejected target is rewritten once; if it fails again, the old target stays. The number changed is reported.
3. **Same-seed floors at 82 and 83, registered before training.** Recall must not fall below 6.37's 192 (probe) and 163 (`hard_dev`), not v6's.
4. **Seeds 97 to 99.**
   - 6.37 is retrained from the byte-identical set, queued first, alone on the card.
   - The comparison is pooled sums, and ties pass.
   - If 6.37's runs at 97 to 99 do not finish, the 7 fails.
   - 6.37's own results there do not re-decide whether it ships.
5. **Stopping.**
   - Any fail stops the try, and there is no 6.39 after it.
   - Training at 82 and 83 starts by 22:00.
   - The write-up names it candidate 17 and gives the measured in-view result whatever it shows.