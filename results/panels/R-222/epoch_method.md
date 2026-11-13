Recommendation: (c), with the rule fixed now and disclosed: read epoch 3 if it passes Demo2, else epoch 2 if it passes Demo2, else K4.8 bombs and the next candidate starts. Do not use (a) alone.

## 1. Which option and why

(c). The registered "epoch 2 only" was set before K4.6 epoch 2's hard_dev result existed. That result is now known and it is the reason to drop (a).

Single strongest piece of evidence: K4.6 hard_dev on seed 82. Epoch 2 gives never_told 39 of 48 and false retrieval 10. That fails two screening lines (needs at least 44 and at most 4). Epoch 3 gives 46 and 4, which passes both. A candidate that fails screening cannot ship. Epoch 2's gain is one Demo2 older item (3 against 2 of 6) and 3 recall points. One item of six is within judge and sampling noise. The hard_dev change is 7 and 6 items out of 48, which is not noise. K4.5 points the same way: epoch 2 had 2 of 4 never-told on Demo2, epoch 3 had 4 of 4.

Why not (b) alone: epoch 3 has scored 2 of 6 older on every candidate (K4.5, K4.6, K4.7). The gate needs 3. So (b) will probably bomb K4.8 at Demo2 on one item of six. Only one checkpoint in the table (K4.6 epoch 2) has cleared the older line. Rule (c) lets the gate be passed by the checkpoint that clears it, while epoch 3 stays the default because it is the one that clears screening.

Why K4.8 does not repeat the K4.6 epoch 2 problem for sure: K4.8 adds near-miss and wrong-person never-told questions. Those target the exact failure (naming another person's value) that made K4.6 epoch 2 fail hard_dev. This is a reason to keep epoch 2 as a fallback. It is not a reason to make epoch 2 the only read.

Order of reading matters for method. The rule is fixed before any K4.8 result exists, so the choice cannot be fitted to K4.8 outcomes. The reason for changing from the registered rule (K4.6 epoch 2 hard_dev) comes from a different candidate. State both facts in the record.

## 2. The exact rule and how much it weakens Demo2

Rule, written before any K4.8 Demo2 run:
- Run Demo2 on K4.8 seed 82 at epoch 3 and at epoch 2, same judges, same questions, same prompt.
- Demo2 pass for a checkpoint = at least 3 of 6 older and at least 3 of 4 never-told (unchanged).
- If epoch 3 passes, the read is epoch 3, for all seeds (82, 83, 94). Epoch 2 is not looked at again.
- If epoch 3 bombs and epoch 2 passes, the read is epoch 2 for all seeds.
- If both bomb, K4.8 bombs and the next candidate starts at once. No third try.
- The checkpoint chosen on seed 82 is the one screened on 82, 83 and 94. Screening lines are not relaxed for epoch 2.
- Record the Demo2 numbers of both checkpoints, even the one not used.

Weakening: the gate gets two tries instead of one, but the two checkpoints come from one run and share most of their behaviour, so the tries are strongly correlated. Rough estimate: for an adapter whose true older rate is near 0.4 to 0.5, chance of passing the older line goes from about 35 to 50 percent at one try to about 45 to 60 percent with two. An adapter that is really below the line (true rate 0.25) passes about 17 percent at one try and about 25 percent at two. So false passes rise by roughly one third to one half. The gate is still 10 items with two judges and was already coarse. The harm is limited because Demo2 only decides who gets screened; shipping is decided by the screening lines and the pooled recall pick, and an epoch 2 read must still pass hard_dev (at least 44, at most 4), where K4.6 epoch 2 failed. Disclose in the report: two checkpoints tried at Demo2, rule fixed in advance, checkpoint order epoch 3 first.

## 3. Prediction for K4.8 seed 82

Under (c):
- Epoch 3: Demo2 older 2 of 6 (range 1 to 3), never-told 3 of 4 (range 2 to 4; the new near-miss data should fix some of K4.7's 2 of 4), hard_dev never_told 46 of 48 (range 44 to 47).
- Epoch 2 (the fallback): Demo2 older 3 of 6, never-told 3 of 4, hard_dev never_told about 42 of 48 (range 38 to 46), false retrieval about 6.

Most likely path: epoch 3 gets 2 of 6 older and bombs, epoch 2 passes Demo2, then epoch 2 fails or barely meets hard_dev. Probability K4.8 passes Demo2 and screening on seed 82: about 25 percent; on all three seeds: about 15 percent. Given that, plan the one remaining candidate slot assuming K4.8 may fail, and note that K1.3 stays the pick if so.
