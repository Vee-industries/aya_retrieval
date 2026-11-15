# Handoff

Created 2026-11-13 12:46 ET (R-216); updated 2026-11-15 (R-298, session 3fe62a52). Read this, then
`docs/PROJECT_MAP.md`, then `RECORDS.md` from R-227 (the stage tries) and closely R-273 to R-298, and `results/panels/R-294/`, `R-295/` and `R-298/`.

## State

- **State, 15 November (R-294 to R-297).** S3 is complete; 6.37 seed 82 stays the shipped model by the registered
  rule, and a panel Kevin asked for upheld it over his aggregate ruling (R-294; his view is stated in the papers, not
  applied). C1 seed 82 is published beside it, labelled as failing one clause:
  https://huggingface.co/KevinVaillancourt/aya-retrieval-c1 (R-296). A ten-reviewer panel on the write-up (R-295)
  listed fixes; R-297 applied them. A second round (R-298, Kevin: "send them to panel again") found more; R-298
  applied them: the short paper rewritten to 2,363 words, the abstract 465, both cards and the README in line. C1's
  card changed, so its Hugging Face copy waits for re-upload with 6.37's pages. Every decision is first person, Kevin's (R-291). **Form due 06:59 Eastern on 16 November** (15 November
  11:59 PM AoE, read on hackathon.lexsi.ai; earlier records said 07:59).
- **Waiting on Kevin.** (1) A push to the public GitHub repo, 465+ commits behind: the short paper's figures and links,
  the README and CI depend on it (run the privacy check with full output first). (2) Re-uploading 6.37's Hugging Face
  card and article, now older than the repo, and S3's run files to the eval-logs dataset. (3) Filing the form.
- **Not done (R-295 carried):** LoCoMo (Kevin: not needed), simpler baselines, a general-capability benchmark, a
  contamination probe; the short paper is about 3,950 words, over the 5 pages asked, because of the checklist items.
- **Pick before S3: C1** (`k13opc1_r263`; `decide_r191.py` 0 FAIL of 20, pick recall 775 against K1.3's 742, R-279).
  C1 is OP's stage run twice from K1.3 (1e-4 x 1 on OP's set, twice). It beat K1.3 by Kevin's rulings: a candidate must
  beat K1.3 (R-276), with the demos judged on their totals over Demo4 and Demo5 (R-278): older 5 of 12 against 4,
  never-told 6 of 8 against 5. S3 ran on Kevin's go (R-280). Before R-279 the pick was K1.3 (742); R2c
  (868) is not eligible (R-247, R-249; `NOT_ELIGIBLE` in `decide_r191.py`).
- **Demos (R-254, `docs/demos/WHY.md`):** Demo2 and Demo3 are retired (their answers were training values). Every try
  reads **Demo4** (screening) then **Demo5** (held out), both written fresh and checked clean by
  `scripts/records/demo_contamination.py`. K1.3 on Demo4: older 1 of 6, never-told 2 of 4 (R-257). Readings: Demo4 4
  (K1.3, C0, OP, C1), Demo5 2 (C1, K1.3: 3 of 6 / 3 of 4, R-277).
- **History of today's tries.** C1's try ran to the end and C1 became the pick (R-279). Earlier today: Kevin ruled (R-276) that a candidate must beat K1.3 on each demo line, not a fixed line. K1.3 on Demo5: 3 of 6 older, 3 of 4 never-told; C1 2 of 6, so C1 does not beat K1.3 (R-277). Demo5 has been seen by the orchestrator through a judge's marks (R-277). OPO (OPT from OP, C1 its control): the lane advised against it (R-273), Kevin said run it anyway (R-274), and it stopped by its rule with 0 answer rows, because OP gets every older and confirm item on the training templates right (48 and 48 of 48, R-275). By R-274 the day's tries end. Kevin said keep trying (R-271); C2 (C1 plus the same stage a third time) failed hard_dev, never_told 43 (R-272), so by R-271 OPT did not run. OP4 (R-267:
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
  `build_onpolicy_rows.py SEED [k13|t6|op|op4]`; `build_onpolicy_template.py SEED` (OPT, R-271, never run). `qtry6.sh` adds a C1 start adapter.

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

K1.3 46 / 2 / 52, Demo2 0 / 4, Demo4 1 / 2, Demo5 3 / 3 (R-277). K4.6 46 / 4 / 72, 2 / 4. T4 38 / 12 / 59, 3 / 3. T6 44 / 4 / 72, 2 / 4.
R2c 45 / 4 / 63, 3 / 4 (not eligible). C0 48 / 0 / 54, Demo4 2 / 2. OP 48 / 1 / 60, Demo4 2 / 3. OP4 33 / 5 (R-268). C1 46 / 0 / 68, Demo4 3 / 3, Demo5 2 / 3 (R-270); seed 83 48 / 2 / 66; pick recall 775 (R-279). C2 43 / 2 / 66 (R-272). Every other try in
R-227 to R-272 failed a gate or did not train.
