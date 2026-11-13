**Recommendation: (c) with a fixed order and an early stop: Demo2 on both checkpoints, read epoch 3 if it passes, else epoch 2; if epoch 2 is read, screen seed 82 hard_dev first and drop K4.8 at once on a fail. Fix the rule before any K4.8 result exists, and expect K4.8 to fail.**

Against lane. Every row in the table fails at least one gate. Epoch 3 has never passed Demo2 older (0, 2, 2, 2 of 6). The one epoch 2 with a hard_dev result failed two screening lines. Choosing a checkpoint moves the model between answering more and declining more. It does not get it out of that trade-off. Only K4.8's new data can do that.

## 1. Which option, and why

- **Against (a), epoch 2 only.** It was registered on the premise that K4.6e2 was the better read, and that premise was set before K4.6e2's hard_dev result was in. That result: never_told 39 of 48 (needs 44) and false retrieval 10 (needs at most 4). Both lines fail by 5 or more items, so this is not a near miss. K4.5e2 also bombed Demo2 never-told (2 of 4). Of the two epoch 2 readings, one failed each gate.
- **Against (b), epoch 3 only.** Epoch 3 Demo2 older was 2 of 6 on K4.5, K4.6 and K4.7, one item under the line every time. K4.8's added data is never-told questions. Nothing in it should raise older recall, so (b) is a predicted Demo2 bomb.
- **Against (c), the option that looks best.** Going by the table, (c) almost always reads epoch 2, because epoch 3 does not pass Demo2 older. So in practice (c) is (a) plus a rare way out. It turns a 5-minute Demo2 bomb, which frees the slot at once, into a screening fail that shows up hours later. That is why I add the early stop: seed 82 hard_dev is the line epoch 2 is known to fail, so it runs first.
- **Single strongest piece of evidence:** K4.6 epoch 2 on hard_dev scored never_told 39 and false retrieval 10, where epoch 3 of the same candidate scored 46 and 4. The extra Demo2 item that epoch 2 bought cost 7 never-told items and 6 false retrievals.

## 2. Exact rule and how much it weakens Demo2

Rule, fixed before K4.8 seed 82 finishes. Run Demo2 on e2 and e3 of seed 82 with the same judges. A checkpoint passes if it gets at least 3 of 6 older and at least 3 of 4 never-told. If e3 passes, read e3. Else if e2 passes, read e2. Else bomb, and the next candidate starts. The read checkpoint is then used on every seed, with seed 82 screening first and a stop on the first failed line. Seeds 83 and 94 are never used to choose the checkpoint.

How much this weakens the gate: in the worst case (independent checkpoints, each with pass chance p) the chance of a lucky pass goes from p to 2p - p², which is close to double when p is small. In practice the two checkpoints share two of their three epochs. The observed pairs differed by at most 2 items on one count. So the realistic gain is the case where e2 sits exactly on the line at 3 older, one item over. Disclose it as "Demo2 had two tries (e2, e3); read = e3 unless only e2 passed".

## 3. Prediction for K4.8 seed 82

- e3: older 2 of 6, never-told 4 of 4, so it fails on older.
- e2: older 3 of 6, never-told 3 of 4, so it passes and is read.
- hard_dev never_told at e2: about 41 of 48 (39 from K4.6e2 plus a small gain from the wrong-person data). That fails the 44 line, with false retrieval about 7.
- Most likely outcome: K4.8 is dropped about 1.5 hours after Demo2, at seed 82 screening, and the remaining slot goes to the next candidate. K1.3 stays the pick. My rough chance that K4.8 passes everything: 1 in 4 or less.
