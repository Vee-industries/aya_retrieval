# Panel brief: a seed-average of 6.37 as a candidate ("7")

You are one lane of a two-lane panel. You read; you write nothing to disk and change nothing. Your answer is your
final message, under 500 words.

## Hard limits (break one and your answer is void)

- Never open `src/aya_retrieval/pool_independent.py`, anything under `docs/independent_pool/`, or line 452 onward of
  `src/aya_retrieval/pools.py`. Never open any file whose name contains "token".
- Never open a result file whose name contains `75002` (it is the judge seed) or anything under `data/blind_dev/`.

## Repo

`C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`; adapters in
`C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/adapters/screens/fix17cs37_{82,83,94,95,96,97,98,99}` (peft LoRA,
r 32, alpha 64, all attention and MLP projections, each trained from scratch on the same 1,094 rows with a different
seed). Read `RECORDS.md` R-141 and R-146 to R-150 for context.

## The proposal

6.37 (seed 82) is frozen. R-150's panel found the main remaining miss (found the line, answered without the asked
detail) is mostly a seed draw: 3 to 18 misses a seed with the same data, `hard_dev` recall 73 to 90 across the eight
seeds. Proposal: build one adapter whose weight change is the exact mean of the eight: delta W = (1/8) sum of
(alpha/r) B_i A_i. Stored losslessly as one LoRA of rank 256 (A = the eight A_i stacked, B = the eight B_i side by side
divided by 8, alpha set so the scaling stays alpha/r of the originals). CPU only, minutes, no training. It is then
scored as a candidate: every gate 6.37 passed, unchanged (probe and `hard_dev` recall pooled at 82 and 83 not below
192 and 163 is meaningless for one adapter, so the plan is: the averaged adapter's own scores must not be below 6.37
seed 82's on each counted line, and its `hard_dev` recall at fresh seed 75002 over `plain` and `long` must beat 6.37
seed 82's on the same items, ties failing), plus the stress runs and R-086's judged sheets. Any fail and 6.37 seed 82
ships.

## The question

Is this worth running, is the merge sound, and is the pass rule right? In particular: do independently initialised
LoRAs average into something useful, or does the mean of unrelated low-rank deltas shrink toward zero (toward base)?
Is "not below seed 82 on each line, then beat seed 82 at 75002" a fair and hard enough bar, given seed 82 is 6.37's
weakest seed on `hard_dev` (73) and on the independent set? Name a better bar if there is one.

## Your lane

METHOD. Check the merge and the plan as an engineer would. Read the adapter config and, if useful, the safetensors shapes (load with safetensors on CPU; do not run the model). Is the rank-256 stacking exact for peft LoRA (scaling, dropout at inference, module names)? Estimate, from the adapters themselves, how aligned the eight deltas are (for a few modules: cosine similarity of the flattened B_i A_i between seeds, and the norm of the mean against the mean norm), which tells how much the average shrinks toward base. Then say whether to run it and what bar to use.
