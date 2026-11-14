# Handoff

Created 2026-11-13 12:46 ET (R-216); updated 2026-11-14 09:16 ET (R-270, session b661dc83). Read this, then
`docs/PROJECT_MAP.md`, then `RECORDS.md` from R-227 (the stage tries) and closely R-247 to R-270.

## State

- **Shippable pick: K1.3** (`decide_r191.py`, pick recall 742). R2c beat it (868) but is not eligible: its set failed
  a check line (R-247); its fixed set failed hard_dev (R-249). `decide_r191.py` lists R2c in `NOT_ELIGIBLE`.
- **Demos (R-254, `docs/demos/WHY.md`):** Demo2 and Demo3 are retired (their answers were training values). Every try
  reads **Demo4** (screening) then **Demo5** (held out), both written fresh and checked clean by
  `scripts/records/demo_contamination.py`. K1.3 on Demo4: older 1 of 6, never-told 2 of 4 (R-257). Readings: Demo4 4
  (K1.3, C0, OP, C1), Demo5 1 (C1).
- **Nothing runs; the card is idle (09:15); no try is registered; reported to Kevin (R-270).** OP4 (R-267:
  on-policy second-search rows from OP) failed seed 82's hard_dev, 33 / 5 (R-268); its control C1 (OP's stage again on
  its own set) passed hard_dev 46 / 0 / recall 68 and Demo4 3 of 6 / 3 of 4, and bombed Demo5 older 2 of 6, never-told
  3 of 4 (R-269, R-270). By R-267, no smaller-dose retry today. The on-policy tries before it: C0 bombed Demo4
  (R-259); OP passed hard_dev (48 / 1 / 60) and bombed Demo4 older 2 of 6, never-told 3 of 4 (R-261, R-262); OP2 was
  stopped before training, its set held no corrections because T6 already gets its own training chats right (R-264);
  OP3 stopped by its rule, 0 new answer rows, since every reachable error OP has left is about someone else and its
  user-fact errors are ones its search does not reach (R-265).
- **Next step: Kevin's word.** K1.3 stays the pick. Facts for any further lever: OP's user-fact errors on its items
  are search misses (106 of 117, R-267); teaching a second search (OP4) made it keep searching on never-told
  questions (11 of 48 ran out of calls, R-268). C1's Demo5 older misses: two wrong with the source found, one out of
  calls, one decline with the source not found (R-270).
- **Queue scripts** (scratchpad of session 77d169a0,
  `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\`):
  `qtry5.sh` / `qtry5_lock.py` (a try with an optional start adapter `INIT` and a per-seed `PREP` script; `init`
  trains a missing K4.6, T6 or OP start adapter as it was), `op3_prep.sh` and `op4_prep.sh` (eval, build, stop rule,
  check), `chain8_r267.sh` (OP4 then C1), `wake.sh` (watcher; add a new try's log glob to its `logs=` line).
  `build_onpolicy_rows.py SEED [k13|t6|op|op4]`.

## How a try runs (`scripts/records/queue/qtry.sh`, run as `qtry3.sh` from the scratchpad)

Train seed 82 (a stage on the seed's start adapter, `INIT`, K1.3 unless named); seed 82 hard_dev with the early stop
(`hd_gate.py` in the scratchpad); Demo4, then it prints `DEMO2 READY` and waits for `LABEL_read2.txt`; Demo5 the same
with `DEMO3 READY` and `LABEL_read3.txt`; then trains seeds 83 and 94; then the rest of screening; then
`decide_r191.py`. **Judging a Demo:** `demo2_judges.py` with `RUN` = `results/demo2/branches_LABEL_82_demo4.json`
(or `_demo5`) and `OUT` = `results/demo2/judge_LABEL_82_demo4`, `sheet()`; two fresh blind Sonnet judges each read only
`sheet.md` and write `marks_j1.txt` / `marks_j2.txt`; `tally()`. Pass at 3 of 6 older and 3 of 4 never-told (with
search). Write `pass` or `bomb` into the read file; commit the record first (the queue waits for a clean tree).
`wake.sh` in the scratchpad exits on any new gate event, a 45-minute stall or 90 minutes with no event.

## Rules in force

- Kevin (R-240, R-252, 05:12): keep trying until a candidate beats K1.3 (every gate, every screening line, higher pick
  recall), then beat that. Every lever is registered in `RECORDS.md` before it runs.
- Schedule (R-243): a try clears seed 82 by Saturday 14:00 ET; every seed trained by 20:00; pick by 22:00; S3 by 23:00.
- Every training set passes `check_k3.py` with 0 FAIL before it trains (R-247's miss). No exception to a ruled line.
- Lexsi tries run at `--max-vram-fraction 0.85` (Kevin, R-232). One `&&` commit chain; `get_usage` before agents;
  corrections appended, never written over committed lines (R-258).
- The GitHub repo is public: no push without Kevin's yes. Do not open `pools.py` past line 451, sealed or held-out
  data, `results/longmemeval/`, or Demo5's chat.

## Seed 82 numbers (hard_dev never_told / false retrieval / recall; Demo2 older / never-told unless noted)

K1.3 46 / 2 / 52, Demo2 0 / 4, Demo4 1 / 2. K4.6 46 / 4 / 72, 2 / 4. T4 38 / 12 / 59, 3 / 3. T6 44 / 4 / 72, 2 / 4.
R2c 45 / 4 / 63, 3 / 4 (not eligible). C0 48 / 0 / 54, Demo4 2 / 2. OP 48 / 1 / 60, Demo4 2 / 3. OP4 33 / 5 (R-268). C1 46 / 0 / 68, Demo4 3 / 3, Demo5 2 / 3 (R-270). Every other try in
R-227 to R-270 failed a gate or did not train.
