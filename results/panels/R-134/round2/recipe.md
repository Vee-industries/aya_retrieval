**Recipe expert, round 2**

**Claims I checked from the files**

Correct:
- **Data's rows.** The 28 ids are all `in_view` rows, and exactly 10 of them open "It sounds like". "a bit lost or confused" appears in 9 `hard_dev` misses.
- **Against's 6.34 group.** All 9 ids are in `build_r122.py`'s `sounds_like` group of 22. There are 57 correct `hard_dev` replies that open "It sounds like", against 32 misses that do. 6 targets open "You can". v6 misses 52 (188 of 240).
- **Stats.** R-097 does stop at probe in-view below 41 at 82 and 83, so in-view is gated there. The R-120/R-121 cost of 30 to 41 is correct, but 6.311 was trained on top of 6.31, so it is not a clean data effect.

Two corrections:
- **Dialogue's 44 rows** are its 22 deflection ids plus all 22 "It sounds like" rows. 12 of those 22 already give the value (for example 0001, 0012, 0033, 0049, 0096, 0127). Rewriting them is the 6.34 mistake at a smaller size: it changes good no-search examples.
- **Dialogue's "0 rows" claims** I did not recount.

**1. Final position: one fix, data's 28 rows with dialogue's target method**
- Change only the last assistant turn of data's 28 ids. 1,094 rows and 150 `in_view` rows stay.
- New target: base resampled with no tool, N fixed before the build. Keep the first candidate that:
  - passes the scorer;
  - fails dialogue's opener rules;
  - has no four-word run in common with the probe or `hard_dev`;
  - does not open "Your ...".
- If no candidate passes, use data's hand-written direct answer.
- One fresh blind judge vets all 28 changed targets.
- The recipe is 6.37's exactly:
  - `--loss-on chat_decision`, so the new targets get full loss. That loss is what the fix needs.
  - Rank 32, MLP plus attention, 3e-4, 3 epochs, from scratch.
  - The code's own checks must report `decision_rows` 222 and no row-key collisions.

My round 1 found that no recipe change helps. Masking the in-view words gives base's words back: 78% unsearched on `hard_dev`, against 6.37's 83%. Fewer epochs and a lower learning rate also did not help (`fix17e2`, `e2lr2`). So the targets must change, and their full loss then works in the fix's favour.

**2. Strongest objection: stats**

A clone of 6.37 passes the full gate about 3% of the time, and the fix moves only R-097. I accept the arithmetic. It does not argue against this fix in particular: 6.37 itself was such a draw and passed. The cost is one 52-minute run at 82 and 83, and the clock allows it.

Against's "every route was tried" is not right for this edit:
- Fix 12, fix 13, 6.311 and 6.32 rewrote or added targets in scripted or brief frames.
- 6.34 removed 12 good rows and kept 18 deflecting ones.
- None kept every row and replaced only the deflecting targets with base-voice answers.

**3. Probability**

About 7% for this fix. My 5% was for a recipe-only change. The rise comes from the verbatim copying: phrases found only in a few `in_view` rows reappear in the misses. That makes the cause specific. Recall risk (R-121's shape transfer) and seed noise keep the number low.

**4. Needed for my yes**
- The 28 ids and N are registered before the build. The target dictionary is frozen before training.
- No "Your {relation}" frame. No row is added or removed.
- 6.37's recipe byte for byte, recorded in the train report.
- Stats' same-seed protocol is registered first:
  - 6.37 is retrained at 97 to 99 from the identical set, queued first and alone on the card.
  - The reference at 82 and 83 is fixed now.
  - If 6.37's runs at 97 to 99 do not finish, the 7 fails.
- A stop rule: if `hard_dev` recall pooled at 82 and 83 falls below 157, the try ends with no judging.