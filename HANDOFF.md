# Handoff

Created 2026-11-13 12:46 ET (R-216); updated 2026-11-14 (R-293, session 3fe62a52). Read this, then
`docs/PROJECT_MAP.md`, then `RECORDS.md` from R-227 (the stage tries) and closely R-273 to R-293.

## State

- **S3 is run and scored (R-287): C1 fails the ship rule on one clause, so 6.37 seed 82 stays shipped.** C1 passes (a)
  and (b) and two of (c)'s three parts; its N-hit false-answer rate, 51 of 708 (7.2%), is above base's 14 of 236
  (5.9%). Against 6.37 on S3: copies 195 to 5 of 894, N-hit false answers 286 to 51 of 708, plain never-told 238 to 344
  of 360, recall 347 to 364 of 1,242. Scored by `scripts/records/score_s3.py` (registered R-281, tested R-282);
  coherence by three judges (R-286). The queue (`qs3.sh`, scratchpad of session 77d169a0, log `qs3.log`) stopped
  after K1 seed 82 (R-288), was restarted on Kevin's word at 19:53 (R-289) and finished at 22:38: **S3 is complete**.
  `score_s3.py rule` rerun with the report arms: verdict and every line unchanged (R-292); the report arms' raw counts
  are in R-292 and section 9 (they enter no line). Nothing pushed (public repo: no push without Kevin's yes).
- **Write-up rebuilt (R-288), with the audit session `local_62a27534` checking it against the submit checklist.**
  Four documents now come from templates filled by `scripts/make_article.py` from results files: the long paper
  `docs/ARTICLE.md` (about 11,500 words, from about 20,800), the short paper `docs/submission/HF_ARTICLE.md` (about
  2,300 words, from about 8,400; template `docs/submission/hf_article_template.md`), the form abstract
  `docs/submission/ABSTRACT.md` (template `abstract_template.md`, refused over 500 words) and the model card. The long
  paper has a dated chronology (section 2), the reopening (7), the push to replace 6.37 then K1.3 with every candidate
  (8), S3 (9), and hypotheses, deviations, leakage, flow and limits tables. `scripts/make_figures.py` draws five new
  figures: S3 recall by arm, the two faults, S3 misses, the never-told slide and the demo contamination. Kevin's
  requirements (16:45): two complementary papers, the short one about 5 pages pointing to the long one, a chronology,
  "the dash to try to get a replacement" told well, every STANDARD v3 section, kv_voice_v2, figures from results.
  The audit's 15 findings on b1abc06 are fixed or answered (R-289). The papers state Kevin's decisions in his own first-person voice, no quotes (R-290,
  R-291). **Kevin's next ask (20:5x):** check both papers against kv_voice_v2, STANDARD v3 and the hackathon's submit
  rules, then a large adversarial panel on the write-up. Kevin (R-292): "i'll wait until tomorrow morning. i'll hit you
  up"; weekly usage resets at 05:00 ET on 15 November. **Left:** those checks and the panel, on his message. A voice
  scanner (shown catching a planted line) and its hits by line are in the notes folder
  `side-session-notes\local_f171c9ff-2a22-4e72-96cd-efd7d112faef\` (`voice_scan.py`, `voice_hits_27f6906.md`); none
  is judged or fixed yet. Form due 16 November 07:59 ET.
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
