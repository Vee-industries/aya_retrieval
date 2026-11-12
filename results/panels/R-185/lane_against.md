# R-185 against lane (claude-opus-5-5; read only what brief.md allows; edited nothing, ran no model)

**1. Is a second candidate fair?** S3 is still opened once, by one candidate, so the ship rule stays clean. The
screening is where the damage is. K2's design comes from binning K1's hard_dev misses (`passages_r185.py` reads
`hd_*`). hard_dev and T2 are the same sets that decide K2, so a K2 pass on screening is weak evidence.

Must be disclosed: K2 was designed from K1's hard_dev rows; it is the sixth candidate after 6.37 (6.38, 6.39, 7, 7.1,
K1); the dev pools were reused (R-141, R-157). A skeptical judge would say: "six tries on reused pools; one passing by
noise is expected."

The stronger alternative, argued seriously: train no K2, and run S3 on 6.37, K1 as a report arm (not shippable), and
the baselines. K1 shows a measured trade on S3: wrong answers become declines (R-183: copies 368 to 68; R-184: 6.37
gave a wrong value or unrelated passage on 7 of 7). That is a clean, honest finding. A rule change, such as counting a
decline better than a wrong value, is the one move a judge would trust least after a fail. Reject it.

**2. Which gate fails first.** The binding gate is T2 other-facts recall: allowance 5 points (323 to 318, R-183), seed
noise about 20. The loss sits entirely in the hard_dev half: hard_dev older plus confirm went from 139 to 108, while
probe went from 184 to 188 (`st_of_*` files, my tally). So T2 recall and the hard_dev gate measure the same weakness.
K2 must recover 22 points on T2 and 29 on hard_dev (122 to 151).

- Option B (half dose), straight interpolation between 6.37 and K1: copies about 218 (gate at most 184); false
  answers about 28 (at most 26); T2 recall loss about 13.5 (allowance 5); hard_dev about 142 (at least 151). It fails
  all four. Nothing has been measured between the two doses, so this reading is a guess, the only one the data give.
- Option A (passage count kept) gives found rows 6.37's mean of 2.27 passages and keeps never_told at K1's 2.74
  (R-180). R-020's give-away then comes back reversed: more passages means decline. Decline share in training:

  | Passages | 6.37 | K1 | Option A |
  |---|---|---|---|
  | 4 | 4 of 54 | 30 of 167 | 30 of 80 (38%) |
  | 5 | 3 of 21 | 14 of 81 | 14 of 32 (44%) |

  Five passages is already K1's worst bin on hard_dev (21 right, 23 wrong). Even if K1's one-passage bin recovered to
  6.37's 87%, that adds about 18 and gives 140, still below 151.

**3. Flaws in the evidence table.**
- The "5 or more" bin is exactly 5, the search limit (`recall_tool.py` line 13, `TOP_K = 5`); no row goes above 5. It
  means "the search hit its limit", a different condition from "many passages".
- On hard_dev the passage count comes from each model's own query, so the columns hold different questions (6.37 78
  in the one-passage bin, K1 56). Per-bin rates are confounded with the question and the query written.
- K1 is worse in every bin with more than 10 questions; in the two-passage bin 62 of 70 against 52 of 53. So passage
  count is not the main cause. The habit of declining when passages are present (R-183, untested) fits better.
- Bins 3 and 4 hold 4 to 9 questions each and cannot be read.
- 6.37 has 22 never_told rows with an empty search; K1 has 0. K1 never trains declining on an empty result, and
  Option A leaves that unchanged.

**4. Register before the build.**
- The passage-count check as numbers: found and never_told mean passages differ by at most 0.37 either way (6.37's own
  gap, 2.27 against 1.90, R-180); each found bin within 10% of the 6.37 count A targets.
- One build only. If the check fails, no K2, no rebuild loop.
- Both seeds trained before any K2 result is read; `decide_r178.py` and the gates unchanged; no K2 hard_dev or stress
  row read before the decision.
- A prediction recorded first: K2's one-passage and five-passage right rates on hard_dev, and its decline count.
- No third candidate, whatever happens. S3 opened once, after K2's seeds and decision are committed.
- K2's training starts by Saturday 23:59 Eastern at the latest (R-182).

**Verdict:** neither as written; if one, A, on the condition that never_told passage counts are matched to found rows
(mean gap at most 0.37), checked before training, with one build and no rebuild.
