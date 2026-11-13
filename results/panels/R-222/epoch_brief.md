# Panel question: which checkpoint of K4.8 is read

Read only this file. Answer in under one page, written to the file named at the end. Plain words, no metaphors.

## Setting

A LoRA adapter on a small chat model searches its own older chat history with a keyword tool and must answer with
the stored fact when told, and say "not told" when not told, even when the search returns another fact. Each
candidate trains 3 epochs (passes over the data) on a fixed learning-rate schedule; the adapter after epoch 2 is saved
too. Seeds 82, 83, 94 are trained for a candidate that keeps passing.

Gates, in order:
1. **Demo2** on seed 82, right after training: one writer's chat, 6 "older" questions (told long ago) and 4
   "never-told" questions, two blind judges. Fails ("bombs") under 3 of 6 older or under 3 of 4 never-told. The owner
   keeps this gate; a bomb means the next candidate at once.
2. **Screening** per seed (82 and 83), among others: hard_dev never_told at least 44 of 48 (hard_dev's never-told
   items are built with a same-type fact about another person in the chat); hard_dev false retrieval at most 4;
   recall above base on several sets. Any failed line means the candidate cannot ship.
3. **Pick** by pooled recall over seeds 82, 83, 94 among candidates passing everything. Current pick K1.3 (passes
   screening; Demo2 older 0 of 6).

Deadline: every seed trained by Saturday 16:00 ET (now Friday 14:55). A seed trains in about 80 minutes; a full
screening of one candidate (3 seeds) takes about 9 to 10 hours. There is time for about one more candidate after
this one.

## Evidence on the two checkpoints (seed 82 unless said)

| Candidate | Demo2 older / never-told | hard_dev never_told / false retrieval / recall |
|---|---|---|
| K4.5 epoch 3 | 2 / 4 | 47 / 2 / 72 |
| K4.5 epoch 2 | 2 / 2 | not run |
| K4.6 epoch 3 | 2 / 4 | 46 / 4 / 72 |
| K4.6 epoch 2 | 3 / 4 | 39 / 10 / 75 |
| K4.7 epoch 3 (K4.6 + 64 chats) | 2 / 2 | not run |
| K1.3 epoch 3 (pick) | 0 / 4 | 46 / 2 / 52 |

Reading: on K4.6, epoch 2 answers more (one more Demo2 older item, recall up 3) and names other people's facts more
(hard_dev never_told down 7, false retrieval up 6). Epoch 3 declines more. Demo2 has only 6 older items: 3 against 2
is one item.

## K4.8

K4.8 = K4.7 plus near-miss and wrong-person never-told questions for K4.7's 64 new chats (K4.7 lacked them and named
a value on 2 of 4 Demo2 never-told items). An earlier lane, before K4.6 epoch 2's hard_dev result was known, set
K4.8's read to **epoch 2 only**, to match K4.6e2. K4.8 seed 82 is training now; no K4.8 result exists. Both
checkpoints will be saved for every seed. A Demo2 run takes about 5 minutes per checkpoint; screening one seed at
one checkpoint takes about 1.5 hours.

## Options (you may propose another)

- (a) Epoch 2 only, as registered.
- (b) Epoch 3 only.
- (c) A rule fixed now that uses both, e.g. Demo2 on both; the checkpoint read is whichever passes Demo2, epoch 3
  if both pass. Cost: two tries at a 10-item gate, so the gate is weaker; must be disclosed.

## Questions

1. Which option, and why, given the table? Name the single strongest piece of evidence.
2. If (c) or similar: state the exact rule, and how much it weakens the Demo2 gate.
3. Your prediction for K4.8 seed 82 under your option: Demo2 older of 6, never-told of 4; hard_dev never_told of 48.

## Output

Write to `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\OUTFILE`:
a recommendation line first, then the three answers. Reply with the recommendation line only.
