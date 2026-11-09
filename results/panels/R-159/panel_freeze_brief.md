# Panel brief: freeze 6.37 now, or use the time left for one more candidate

You are one lane of a three-lane panel. You read and may run light CPU-only Python to count things; you write nothing
to disk and change nothing. Your answer is your final message, under 700 words.

## Hard limits (break one and your answer is void)

- Never open `src/aya_retrieval/pool_independent.py`, anything under `docs/independent_pool/`, or line 452 onward of
  `src/aya_retrieval/pools.py` (sealed held-out material). When you search `pools.py`, limit the search to lines 1 to
  451 (for example `head -n 451 src/aya_retrieval/pools.py | grep ...`); never grep the whole file, and leave
  `pools.py` out of any search over several files. Never open a file whose name contains "token".
- Never open anything under `data/blind_dev2/` or any scratch folder named `indep2`. The second set's RESULTS files
  (`results/recall_eval/blind2_*`, `results/analysis/R-157/`) may be read: they are now a report (R-157).
- Training rows come only from the TRAIN pool (`pools.py` lines 1 to 451) or new material that shares no four-word run
  with the probe or `hard_dev` pools. Never from probe, `hard_dev`, either independent set, break-test items or
  held-out material. `phone_style` never enters training.

## Repo and context

`C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`. Read `README.md` (status and Known limits), then
`RECORDS.md` R-150 to R-158 (R-153 is 7's design and pass rule, R-155 its fail, R-156 7.1's design, R-157 7.1's fail
and the second independent set's report on 6.37, R-158 7.1's report on that set). Earlier records as needed (R-127
on probe pass rates, R-141 on templates, R-146 on the first independent set). Gate scripts as run:
`scripts/records/queue/`. Results: `results/recall_eval/`, `results/analysis/R-146/`, `results/analysis/R-157/`.

## The facts

- 6.37 (fix17cs37 seed 82) is the shipped model. Since R-093 seventeen-plus candidates were tried; each failed a
  registered line. The last two, 7 (tag-question rewordings) and 7.1 (7 without its 20 `in_view` tag rows), failed at
  seeds 82 and 83. R-156's registered reading of 7.1's result: no tag-question design before the freeze.
- Independent sets (writers blind to the generator): recall 6.37 seed 82 against base, 39 vs 26 of 120 (+50%) on the
  first, 53 vs 27 (+96%) on the second. 6.37 searches few tag questions there (`confirm` searched 12 of 40 on set 2).
- R-158's report on 7.1 (two seeds, second set): 7.1 searches tag questions 40 and 39 of 40 (6.37: 12 and 7) and every right `confirm` answer is found by search (18 and 18; 6.37: 6 and 4), but recall is not higher (51 and 52 against 6.37's 53 and 53): it corrects more false claims (7 and 5 of 20 against 3 and 1) and confirms fewer true ones (11 and 13 against 16 and 16). Read R-158's result section.
- Time now: Mon Nov 9, about 14:50 EST. Model freeze is Wed Nov 11 night (Kevin's date, R-151). Write-up Nov 12, demo
  Nov 13, submission by Nov 14. A candidate costs about 7 GPU hours to judge in full (82 and 83 scored, stress runs,
  judged sheets, seeds 94 to 96, five seeds on an independent set). There is no third unread independent set; one
  could be written by fresh blind writers in a few hours (R-152 took about that).
- After the freeze: `scripts/records/freeze_r154.py write` on the shipped adapter, then the sealed final run on the
  held-out pools, once, on Kevin's go.
- **Kevin's position:** he will freeze 6.37 if this panel agrees, and he says he is reluctant. Take his reluctance as a
  reason to make the case for continuing as strong as the facts allow, not as a reason to agree with him either way.

## The question

Freeze 6.37 now, or use the time to Wednesday night for one more candidate? If one more, name the design (rows
changed or added, how built, how many), the rule it must pass, what a fail would look like, the chance a copy with no
effect passes, and why it is worth the GPU and the write-up time it costs. Also say what each choice does to how a
hostile reviewer reads the final result (forking paths: how many candidates were tried, and against which sets).

## Your lane

{LANE}
