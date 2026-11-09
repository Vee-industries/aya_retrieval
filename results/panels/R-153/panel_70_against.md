# Panel brief: design 7

You are one lane of a three-lane panel. You read and may run light CPU-only Python to count things; you write nothing
to disk and change nothing. Your answer is your final message, under 700 words.

## Hard limits (break one and your answer is void)

- Never open `src/aya_retrieval/pool_independent.py`, anything under `docs/independent_pool/`, or line 452 onward of
  `src/aya_retrieval/pools.py` (sealed held-out material). Never open a file whose name contains "token".
- Never open anything under `C:/Users/Gaming/scratch/claude/C--Users-Gaming-Desktop-Claude-s-House/389594c2-8513-47d9-80f1-1a28b96837f7/scratchpad/indep2/`
  or `data/blind_dev2/` (the second independent set, which will judge 7), or any result whose name contains `75002`.
- Training rows come only from the TRAIN pool (`pools.py` lines 1 to 451) or new material written for 7 that shares
  no four-word run with the probe or `hard_dev` pools (`scripts/records/build_r110.py` `TEST_GRAMS`). Never from probe,
  `hard_dev`, either independent set, break-test items or held-out material. `phone_style` never enters training.

## Repo and context

`C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`. Read `RECORDS.md` R-138 to R-151 first, then as
needed earlier records (R-110, R-113, R-115, R-117 to R-128 explain how 6.37's set was built and what failed).
6.37's set: `data/screens/fix17cs37.jsonl` (1,094 rows). The original builder: `scripts/run_build_training_set.py`;
items: `src/aya_retrieval/conversations.py`; templates: `src/aya_retrieval/pools.py` (TRAIN only); the search tool:
`src/aya_retrieval/recall_tool.py`. The first independent set, now a development set (R-151): `data/blind_dev/chats/`,
6.37's results on it `results/recall_eval/blind_*_seed_0.json`, analysis `results/analysis/R-146/blind.json`.

## The goal

7 is a new training set, trained from scratch (6.37's recipe unless you argue otherwise), that keeps 6.37's strengths
(probe recall 96/96, `never_told` and `statement` near full, no slips, `in_view` 43 to 44 of 48) and fixes what costs
the most on chats the generator never made (R-146, 6.37 seed 82: 39 of 120 recall):
1. A "..., right?" tag question (`confirm`) rarely triggers a search (23 of 29 `confirm` misses never searched); the
   TRAIN `confirm` wordings are all "did i ever tell you about ..." forms.
2. Search queries reuse the TRAIN template's fixed `query` string ("{who} keeps animals yard") instead of words from
   the question, and miss.
3. A fact told with a pronoun ("he's out in Calgary now"), the person named in an earlier message, is not found.
4. Found but incomplete: the answer restates the line's first clause and leaves out the asked detail (R-144, R-148);
   R-110's rows made this worse three times (R-149); R-150 rejected value-first answers as untestable at 6.4's bar.

## Judging (fixed after your design, before training; for your planning)

Every 6.37 gate unchanged at seeds 82 and 83; then a win over 6.37 on the second independent set (recall, seeds 82
and 83 pooled against 6.37's 82 and 83); then 94 to 96. Training starts by Tue Nov 10 12:00 (it is Mon 09:20 now).
Building a set may use the base model on the GPU for a few hours if needed (6.37's set was built that way) and
scripted answers where the record supports them.

## The question

Design 7: what changes in the training data (and only if needed, the recipe), how each change is built and how many
rows, what the answers look like, and which of the four failures each change targets. Rank the changes by expected
gain against risk; say which to leave out. Say what result shows each change failed, and the single biggest risk.

## Your lane

AGAINST. Argue against the likely designs. For each obvious change (varied confirm wordings, queries from the question's words, pronoun facts, longer lines, a different answer shape, more rows), give the strongest record-based reason it will fail a gate or not move its failure, and say what the second independent set can and cannot show. If a design survives your case, name it and what would make it fail.
