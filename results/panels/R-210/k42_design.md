# R-210: K4.2 design (for the against lane)

## What failed

K4.1 (`data/screens/k4_1_r209.jsonl`, built by `scripts/records/build_k4_1.py`) failed 4 screening lines in
`scripts/records/decide_r191.py` (output `decide_r191.txt` here): hard_dev never_told 34 and 40 of 48 on seeds 82 and
83 (floor 44), hard_dev false retrieval 8 and 7 (ceiling 4 and 5). Pooled dev recall 577, against K1.3's 501.

`never_told_types.txt` here: over seeds 82, 83 and 94, K4.1's never_told misses are 22 (hard_dev) and 41 (probe)
rows that searched 4 times and ran out of calls, and 18 (hard_dev) that named a value. K1.3 searched once on every
never_told row and missed 2 and 3. Examples (hard_dev seed 82): queries "Lorcan uni", "degree studying", "course
major", reply "Lorcan is studying psychology" (the stored fact of another category); 4 queries then a fifth call.

## Diagnosis

Training rows by the number of searches and the reply (K4.1, natural rows):

| Searches | Reply names a value | Reply declines |
|---|---|---|
| 1 | 219 (older 74, check 112, contrast 33) | 147 (never_told 102, near_miss 45) |
| 2 | 104 (older 74, check_false 18, contrast 12) | 25 (older 16, check_false 5, never_told 4) |

Template rows (K1.3's 1,156) all search once. So after a second search the training reply names a value 104 times
in 129 (81%). The model has no row with a third search, and few rows that decline after a second one. On
never_told questions it searches again (as fact rows that missed do), then either names whatever the second search
brought back or keeps searching until it runs out of calls. A never_told row only does a second search when the
first returned no passages (`build_k3.chat_rows`), which is rare (4 rows).

## K4.2 (proposed)

Same writer files, same drops (`build_k4_1`), one change to how never_told and near_miss rows are built:

1. Natural never_told rows (K3 writers) and near_miss rows (K4 writers) run both queries, the first then
   `second_query`, every time, and decline (`TRAIN.unknown_replies`). Kept if either search returns a passage
   (R-020). A near_miss is kept only if one of the two outputs holds the stored message (was: the last output; with
   two searches both are in the context when the reply is written).
2. Balance at two searches: at each last-search passage count, two-search decline rows are cut in a hashed order to
   the number of two-search value rows there (one to one), so the second search ends in a value or a decline equally
   often. One-search rows keep R-205/R-208's balance as built. Then the 1,024-token limit.
3. Everything else as K4.1: K3.2's rows, contrast rows, statement rows, in_view rows, drops, check lines
   (`check_k3.py --set k4_2_r210`), queue (seed 82, Demo2 at once, bomb rule R-205, screening, seeds 83 and 94).

Prediction, registered before training: hard_dev never_told at least 44 of 48 on seeds 82 and 83, out-of-calls
never_told rows near 0, pooled dev recall below K4.1's 577 and above K1.3's 501.

## Questions for the lane

- Does the diagnosis follow from the counts, or is there a simpler cause (for example epoch 3 against epoch 2, or
  the contrast rows)?
- Does the change fix it without teaching the model to always search twice and decline found facts?
- Is the one-to-one cut at two searches the right size, or should two-search declines exceed values?
- Any rule of R-205 to R-209 it breaks?
