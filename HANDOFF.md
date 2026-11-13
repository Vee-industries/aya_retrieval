# Handoff

Created 2026-11-13 12:46 ET (R-216). Read this, then `docs/PROJECT_MAP.md`, then `RECORDS.md` from R-205.

## State

- **Shippable pick:** K1.3 (`decide_r191.py`, pick recall 742), provisional until Saturday 14 Nov 18:00 ET.
- **Out:** K4.7 bombed Demo2 (R-218). K4.6e2 failed screening at seed 82 (R-221).
- **Running:** queue `q220b`, K4.8 (R-220, R-222), from 14:52; queue `q224`, K4.9 (R-224), waits behind it on the card
  lock and starts when q220b ends. Both in the scratchpad of session 77d169a0
  (`C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\`).
- **Checkpoint rule (R-222, panel):** each queue trains seed 82, runs Demo2 on epoch 3 and epoch 2, prints
  `DEMO2 READY` and waits for a read file beside it (`k48_read.txt`, `k49_read.txt`). Judge the run
  (`demo2_judges.py` with `RUN`/`OUT` set to `results/demo2/branches_k4_N_rNNN_82.json` and
  `results/demo2/judge_k4_N_82`, `sheet()`, two fresh Sonnet judges writing `marks_j1.txt` / `marks_j2.txt`, then
  `tally()`). Write `3` if epoch 3 passes, else `2` if epoch 2 passes, else `bomb`. The queue then reads that
  checkpoint for every seed, runs hard_dev first on seeds 82 and 83 (`hd_gate.py` beside it) and ends itself on a
  failed line; otherwise it screens 82, 83 and 94. Then `decide_r191.py`.

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
