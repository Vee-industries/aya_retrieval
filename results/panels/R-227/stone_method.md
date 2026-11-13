RECOMMENDATION: Adopt with changes. Run it, but fix the rows, the single read and the try count before any seed starts, and check the two failing Demo2 items first (no training needed).

1. More likely than a fresh candidate?
Yes, modestly. My estimate for passing both gates on seed 82 is about 20%. For a new fresh candidate it is about 10%, and the lane found none above 50%.
- Strongest reason for: it is the one untried axis. K1.3 already holds hard_dev never_told 46 and false retrieval 2. The stage only has to add older-recall without undoing that. K4.6 at epoch 2 reached older 3 of 6, so that level is reachable when training is less finished. A one-epoch stage with linear decay to zero is a gentle dose. It also costs about 1.5 h of the 23.5 h left (three seeds, 25 to 30 min each), so a failure loses almost nothing.
- Strongest reason against: all eight fresh K4.x runs fail the same two Demo2 items at epoch 3, with different row counts. That points to a cause that more or different training rows do not change. One cause could be that the keyword search (OR, top 5) never returns those two facts. Another could be a flaw in those two items. A stone that starts from K1.3 and adds fewer natural-row epochs than the fresh runs got is more likely to land at 2 of 6 or lower than at 3.
- Change: before training, read the seed 82 Demo2 transcripts for those two items. Check whether the stored fact appears in the top 5 results. If it never does, no training fixes it. Say so and stop, instead of running the stone.

2. Rows, learning rate, epochs.
- Rows: use the whole set (template rows plus natural rows), not natural only. Natural-only rows shift the data away from the scripted chats that taught "not told", and that behaviour is what K1.3 holds at 46 and 2. Keeping the template rows in the stage rehearses it. It also makes the result comparable to K4.x, so the only thing that differs is the starting point.
- Which set: K4.8 bombed at both checkpoints, so first find out why (data or checkpoint). If the cause is its added rows, use the K4.x set with the best epoch-3 hard_dev result instead. State which set was used and why.
- Learning rate and epochs: 1 epoch, peak 1e-4, linear decay, same seed, adapter loaded from the same seed's K1.3, optimizer state not carried over. These come from the recorded earlier stage. Do not add a warmup or change anything else.
- Order: train seed 82 first. Seeds 83 and 94 follow only if seed 82 passes both gates. Time allows this: even with one declared second try on seed 82 (natural-only rows), the total is about 2 h.

3. Checkpoint and disclosure.
- Read the end-of-epoch-1 checkpoint only. Ignore any mid-epoch save. There is no choice of checkpoint to tune.
- Disclose:
  (a) K1.3, the pick, bombs Demo2 on older recall (0 of 6), so it fails the owner's gate as it stands.
  (b) Demo2 is one writer's chat of 10 questions. K1.3, eight K4.x runs, K4.8 and this stone have all been read against it. A pass is therefore weaker evidence than the gate implies. Give the count of candidates tried.
  (c) The stone was proposed after the fresh candidates failed.
  (d) The lineage is K1.3 plus a stage, so template rows are seen 3 epochs and then once more. The three seeds share a recipe, but each depends on that seed's K1.3.
  (e) Pooled recall must be compared with K1.3's pooled recall over seeds 82, 83 and 94.
  (f) If the second try on seed 82 is used, report both tries.

4. Prediction, seed 82.
- Demo2 older: 2 of 6. About 60% for 2, 20% for 3 or more, 20% for 1 or fewer.
- Demo2 never-told: 4 of 4. A result of 3 of 4 still passes.
- hard_dev never_told: about 45 of 48, range 43 to 47.
- hard_dev false retrieval: about 3, range 2 to 5.
- Recall: about 62, range 56 to 70. This sits between K1.3 at 52 and K4.x at about 72.
- Most likely outcome: it passes screening and fails Demo2 older by one item, as K4.x did.
