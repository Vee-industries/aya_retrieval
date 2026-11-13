# Against lane: K1.3 + one epoch of the natural rows

**Recommendation: adopt with changes. Run seed 82 only first, on K4.8's whole set, 1 epoch at 1e-4. Read Demo2 and hard_dev before seeds 83 and 94 get any GPU time. Allow one try and no learning-rate variants. If it fails, report that no candidate passes Demo2 and stop.**

## 1. More likely than a fresh candidate?

Slightly more likely, and still more likely to fail than to pass. I put it at about 20 to 25%.

- **Strongest reason against.** The record already shows one trade-off: a model that answers more older questions also declines fewer never-told ones. K4.6 at epoch 2 got older 3 of 6, but never_told fell to 39 and false retrieval rose to 10. K1.3 sits at the other end: never-told 4 of 4, older 0 of 6. A short stage on natural rows, starting from K1.3, is one more point between these two ends. The two ways it fails:
  - It moves too little: older stays at 0 to 2.
  - It moves enough to reach 3 older, and hard_dev never_told then drops below 44, as it did for K4.6.
  
  Also, eight fresh K4.x runs, each with 3 full epochs on these rows, all stopped at older 2 of 6, on the same two items. One epoch at 1e-4 gives the model less of the natural rows than those runs did. Nothing in the brief says why the other four older items fail. If they fail at the search step (the keywords never pull up the fact in the top 5), more training on answer behaviour cannot fix them.
- **Strongest reason for.** This stage starts from a different place. K1.3 has already learned to decline, so a short stage could add answering on top of that without unlearning it. That is a different setup from the fresh mixes, all of which stopped at 2 of 6. The project's shipped model was also built this way.

## 2. Rows, learning rate, epochs

Use **K4.8's whole set**, with the template rows included. Training on natural rows only, starting from K1.3, takes away the rows that hold up never_told. That pushes the model toward the side of the trade-off that fails screening. The whole set is about 2,490 rows, so expect about 35 to 40 minutes per seed, not 25 to 30. Take the settings exactly as in the recorded stage: 1 epoch, peak 1e-4, linear decay, same seed, and the same warmup and other settings that stage used. Try no other values. A sweep of learning rates would be one more round of searching against the same 6 Demo2 items.

## 3. Checkpoint and disclosure

Read the single end-of-epoch checkpoint, and no other.

Disclose all of the following:
- It is a two-stage model: K1.3's 3 epochs, then 1 more on the whole set.
- The stage was chosen after K4.x failed Demo2.
- Demo2 seed 82 has now been used to choose among ten or more candidates, so it no longer counts as a held-out test. Give the number of candidates tried against it.
- Demo2 is one writer's chat with 6 older items. The pass line is 3, so one item flipping decides the result.

Check before training (no GPU needed): look at the tool calls on the four older items that fail every time. If the fact is not in the top 5, say so. In that case this stage is not expected to help, and the fault is in the search step.

## 4. Prediction, seed 82

| Measure | Prediction |
|---|---|
| Demo2 older | 1 of 6 (range 0 to 2) |
| Demo2 never-told | 4 of 4 |
| hard_dev never_told | 46 of 48 |
| hard_dev recall | about 60 (between K1.3's 52 and K4.x's 72) |

Result: passes screening on seed 82, bombs Demo2 on the older questions.
