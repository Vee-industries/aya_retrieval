**Case against: 6.37 ships unchanged, and no 7 trains**

**1. Reading (all recounted from files)**

- **The in-view deflection is real, but the opener is not the fault.**
  - Over seeds 82, 83 and 94 to 96 in `results/recall_eval/hd_fix17cs37_*_seed_73157.json` (tool_loop, in_view), 6.37 misses 40 of 240. 32 of those 40 open "It sounds like", and only 4 of the 40 searched.
  - But 57 correct replies also open "It sounds like". The opener comes before right answers more often than wrong ones.
  - The 40 misses fall on 20 of the 48 items. 17 of them are on one `hard_dev` wording, "my head has lost ..." (`58_in_view_02` alone accounts for 5).
  - The base for comparison is already beaten. v6 misses 52 at the same seeds (fresh_r131.txt; R-120; R-128). Judged `hard_dev` Sheet B in_view is 129 against base 105 at 94 to 96 under judge 1 (R-130).
- **The lower-case gap is not significant.** In-view answers lost against gained, paired over 82 and 83 (`st_style_*` against plain), are 11 and 3 on the probe (two-sided sign test p = 0.057) and 8 and 3 on `hard_dev` (p = 0.23). R-099 item 7 also drops any messy-typing training try not started by Sunday 12:00. That time has passed.
- **What I found and cannot argue away.** `fix17cs37.jsonl` has 150 in_view rows. They get full loss: `chat_decision` masks only statement rows (`run_recall_train.py`, about lines 202 to 206). Several of these targets are the base model's deflections:
  - `in_view_0000` "It sounds like you're trying to remember what your aunt ran. Was it a 5k? A marathon?"
  - `in_view_0036` "Can you give me a hint?"
  - `in_view_0079` "Maybe you could try to remember the flavor"
  - `in_view_0103` "You can ask your cousin Ivan to tell you the name of his dog Waffles."

  6 in_view targets open "You can". This is the likely source of the failure, and the write-up should say so.

**2. Proposed fix: none.** Every route to that source has already been tried:

- **Removing the deflecting targets** is 6.34's `sounds_like` group. It contains `0000`, `0036`, `0079`, `0086`, `0088`, `0094`, `0122`, `0134` and `0136`. The opener vanished, but `hard_dev` in_view fell from 78 to 69, the misses becoming searches and denials (R-125, R-132). The model does not read the fact once the deflection is gone.
- **Rewriting them as direct answers** is fix 12 (R-063), fix 13 (R-064), 6.311 (R-120) and 6.32 (R-121). Each gained a few in-view answers and lost found-fact recall or detail, and 6.32 did not even raise `hard_dev` in_view (32 and 39).

That is 5 tries on the in-view rows and 5 trade-offs. A smaller subset (for example, removing only the 6 "You can" rows) is a new draw.

**3. The lines involved**

- **The target line is not a gate line.** `in_view` counts are reported, not gated. Beyond R-097's stop at 41 and the judged sheets against base, a 7 can gain nothing on the gate from fixing it; it can only fail other lines.
- **Lines where 6.37 itself passed with no margin** (R-128, R-130, R-131):
  - R-086 probe 51203 recall: 94, needs 94.
  - `hard_dev` Sheet B `statement` at 82 and 83: 44 against base 44 under judge 1.
  - Phone typing on the probe: 85 at seeds 95 and 96, on the line of 85.
- **Higher bar at 97 to 99.** Recall must match 6.37 at the same seeds. On the probe 6.37 sits at its ceiling (96 a seed), so a 7 can miss no probe recall question that 6.37 answers. Even a copy with no real defect misses one of the 96 in 11% to 20% of files (R-127).
- **The risk.** By the trade-off history, the line most at risk is `hard_dev` recall pooled, the asked detail on found facts. 6.37 is at 163 at 82 and 83 and 73 to 90 a seed.

**4. Probability that a 7 replaces 6.37: about 5%**

- **Base rate.** Since R-093, 1 of 16 candidates passed the full gate (6.37). 2 of 16 passed at 82 and 83 (6.2 and 6.37), and 6.2 then failed at fresh seed 92.
- **Fitting.** A fix aimed at "my head has lost" would be fitted to `hard_dev` items. Seeds 97 to 99 read those same items, so a pass there is not independent evidence of better in-view reading.
- **Cost to the write-up.**
  - A fail makes this candidate 17, with another disclosure.
  - A marginal pass replaces a copy that passed every judged item under all three judges with one designed after reading 94 to 96 and the battery.
- **Clock.** It is not the reason. R-132's schedule lane found a full gate would finish Monday morning.

**What I would do instead:** disclose the deflecting in-view targets as the probable cause, and list this as an open item in `docs/article_template.md`.

### Critical files for implementation
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/data/screens/fix17cs37.jsonl
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/run_recall_train.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/records/build_r122.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/RECORDS.md
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/docs/article_template.md