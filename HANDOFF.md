# Handoff

Created 2026-11-13 12:46 ET (R-216); updated 21:10 (R-243). Read this, then `docs/PROJECT_MAP.md`, then
`RECORDS.md` from R-205 (the stage tries from R-227).

## State

- **Shippable pick:** K1.3 (`decide_r191.py`, pick recall 742), provisional until Saturday 14 Nov 22:00 ET.
- **Out:** K4.7, K4.8, K1.3s (T1), T2, T3, T5 bombed Demo2; K4.6e2, T4 (passed Demo2 and Demo3) and lever 2 failed
  seed 82's hard_dev (R-218 to R-239).
- **Running (scratchpad of session 77d169a0,**
  `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\`**):**
  T6 (`k13t6_r229.log`) on the card; `chain_r240.sh` (log `chain_r240.log`) then runs R2a, R2b, R2c, R2d (R-235),
  the blend grid (`qblend.sh`, R-237) and R3a (R-241), one at a time, each under its lock helper. R3b and R3c are
  conditional (R-241). `wake.sh` exits on any new gate event in the try logs.
- **Each try** (`qtry3.sh` from R-242; `scripts/records/queue/qtry.sh` is the record copy): trains seed 82, runs
  hard_dev and stops on a failed line (`hd_gate.py`), then Demo2, prints `DEMO2 READY` and waits for
  `LABEL_read2.txt` (`pass` or `bomb`); then Demo3 the same way (`LABEL_read3.txt`); then trains seeds 83 and 94,
  then the rest of screening. Judge each Demo with `demo2_judges.py` (`RUN` = `results/demo2/branches_LABEL_82_demoN.json`,
  `OUT` = `results/demo2/judge_LABEL_82_demoN`, `sheet()`, two fresh blind Sonnet judges, `tally()`); pass at 3 of 6
  older and 3 of 4 never-told. Readings so far: Demo2 18, Demo3 1.

## Rules in force

- Kevin (R-240): keep trying until a candidate beats K1.3 (every gate, then higher pick recall), then beat that one.
  Every lever is registered in `RECORDS.md` before it runs; new levers come from lanes.
- Schedule (R-243, Kevin pushed R-194 by 4 hours): every seed trained by Saturday 20:00 ET, pick by 22:00, S3 by 23:00.
  A try must clear seed 82's gates by Saturday 14:00 (R-242). S3 stays closed until then.
- Lexsi tries run at `--max-vram-fraction 0.85` (Kevin, R-232).
- The GitHub repo is public: no push without Kevin's yes. Privacy count on staged diffs exactly 0.
- Do not open `pools.py` past line 451, sealed or held-out data, or `results/longmemeval/`. Nobody reads Demo3's chat.
- SOP token rules 1 to 4 and 6 to 10 apply (the exemption is from the drain line only): fresh short-brief agents,
  Sonnet for writers and judges, commits as one `&&` chain.

## Seed 82 numbers so far

Demo2 older (of 6) / never-told (of 4); hard_dev never_told, false retrieval, recall:
K1.3 0 / 4; 46, 2, 52. K4.6 2 / 4; 46, 4, 72. K4.6e2 3 / 4; 39, 10, 75. T4 3 / 3 (Demo3 4 / 3); 38, 12, 59.
Lever 2 not read; 43, 5, 27. T1, T2, T3, T5 2 of 6 older (not screened).
