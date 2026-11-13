# Handoff

Created 2026-11-13 12:46 ET (R-216). Read this, then `docs/PROJECT_MAP.md`, then `RECORDS.md` from R-205.

## State

- **Shippable pick:** K1.3 (`decide_r191.py`, pick recall 742), provisional until Saturday 14 Nov 18:00 ET.
- **Running:** K4.7, queue `q215` (started 12:40), in the scratchpad of session 3f7d989b
  (`C:\Users\Gaming\scratch\claude\C--Users-Gaming--claude-spares-spare-wcSF8M\3f7d989b-d009-44ac-9f86-64e88058f022\scratchpad\`:
  `q215.sh`, `q215.log`, `q215_lock.py`). Seed 82 trains first (about 70 minutes), then Demo2.
- **Next on the queue's Demo2:** judge it (`demo2_judges.py` with `RUN`/`OUT` set to
  `results/demo2/branches_k4_7_r215_82.json` and `results/demo2/judge_k4_7_82`, `sheet()`, two fresh Sonnet judges each
  writing `marks_j1.txt` / `marks_j2.txt`, then `tally()`). A bomb: stop the queue (taskkill the lock python and the
  eval's outer timeout.exe) and start the next candidate at once. Not a bomb: let it run; then `decide_r191.py`.

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
K1.3 0 / 46, 2, 52 / 89; K4.1 4 / 34, 8, 65 / 122; K4.5 2 / 47, 2, 72 / not run; K4.6 2 / 46, 4, 72 / 132.
