# Handoff

Created 2026-11-13 12:46 ET (R-216). Read this, then `docs/PROJECT_MAP.md`, then `RECORDS.md` from R-205.

## State

- **Shippable pick:** K1.3 (`decide_r191.py`, pick recall 742), provisional until Saturday 14 Nov 18:00 ET.
- **Running (R-219, R-220):** queue `q219`, K4.6e2 (K4.6's seeds read at epoch 2), started 14:16: seed 82 screening,
  then train and score 83, then 94. Queue `q220`, K4.8, waits behind it on the card lock: train seed 82, Demo2 on its
  epoch-2 checkpoint, then screening on epoch-2 checkpoints. Both in the scratchpad of session 77d169a0
  (`C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\`).
  K4.7 bombed Demo2 (R-218); its queue `q215` is stopped.
- **On K4.8's Demo2:** judge it (`demo2_judges.py` with `RUN`/`OUT` set to `results/demo2/branches_k4_8_r220_82.json`
  and `results/demo2/judge_k4_8_82`, `sheet()`, two fresh Sonnet judges each writing `marks_j1.txt` / `marks_j2.txt`,
  then `tally()`). A bomb: stop the queue (taskkill the lock python and the eval's outer timeout.exe) and start the
  next candidate at once. Not a bomb: let it run; then `decide_r191.py`.
- **Drawn, not built:** K4.9 = K4.8 plus "miss then hit" rows (R-220's B), only with a new loss mask that keeps the
  first search call out of the loss and `balance()` keyed on (searches, passages); draft brief
  `docs/k4_8/WRITER_BRIEF.md` (untracked).

## Rules in force

- Kevin keeps the Demo2 gate; a bomb means the next candidate at once. Never re-ask that.
- Schedule (R-194): every seed of a candidate trained by Saturday 16:00 ET (seed 82 of the last one starts by about
  09:00), pick by 18:00, S3 by 19:00. S3 stays closed until then.
- The GitHub repo is public: no push without Kevin's yes. Privacy count on staged diffs exactly 0.
- Do not open `pools.py` past line 451, sealed or held-out data, or `results/longmemeval/`.
- SOP token rules 1 to 4 and 6 to 10 apply (the exemption is from the drain line only): fresh short-brief agents,
  Sonnet for writers and judges, commits as one `&&` chain.

## Seed 82 numbers so far

Demo2 older (of 6) / hard_dev never_told, false retrieval, recall / outside-writer recall:
K1.3 0 / 46, 2, 52 / 89; K4.1 4 / 34, 8, 65 / 122; K4.5 2 / 47, 2, 72 / not run; K4.6 2 / 46, 4, 72 / 132;
K4.7 2 / not run; K4.6e2 (epoch 2) 3 / in screening (R-219).
