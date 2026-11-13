# Panel question: a stepping stone on K1.3 instead of fresh training

Read only this file. Answer in under one page, written to the file named at the end. Plain words, no metaphors.

## Setting

A LoRA adapter on Tiny Aya Global (a small chat model) searches older chat history with a fixed keyword tool (OR
search, top 5) and must answer with the stored fact when told, and say "not told" when not told. Gates: (1)
**Demo2**, seed 82: one fresh writer's chat, 6 older and 4 never-told questions, two blind judges; bombs under 3 of 6
older or under 3 of 4 never-told (the owner keeps this gate). (2) **Screening**, seeds 82 and 83 each: hard_dev
never_told at least 44 of 48 (built with a same-type fact about another person), hard_dev false retrieval at most 4,
recall above base on several sets, and more lines. (3) Pick by pooled recall over seeds 82, 83, 94. Deadline: every
seed trained by Saturday 16:00 ET; it is Friday 16:30.

## Candidates so far (seed 82: Demo2 older of 6 / never-told of 4; hard_dev never_told, false retrieval, recall)

- **K1.3**, the pick: 722 template rows (scripted chats), trained fresh, 3 epochs. 0 / 4; 46, 2, 52. Passes all
  screening lines on seeds 82 and 83.
- K4.x line: K1.3's 722 rows plus about 1,000 to 1,750 natural rows (chats written by writer agents, with near-miss,
  wrong-person and contrast questions), each trained **fresh**, 3 epochs. Demo2 older 2 of 6 at epoch 3 on every one
  of eight (same two items); recall about 72; hard_dev never_told 46 to 47 where measured at epoch 3. At epoch 2
  (K4.6): older 3 of 6, never_told 39, false retrieval 10 (fails). K4.8, the latest, bombed at both checkpoints.
- A lane found no further fresh candidate more likely than not to pass both gates.

## The proposal

The trainer can start from an existing adapter (`--init-adapter`); the project's earlier shipped model was built
that way (a second stage of 1 epoch at a peak learning rate of 1e-4, linear decay, on top of the first stage's adapter,
same seed). Proposal: **K1.3 + one gentle epoch of the natural rows**: start from K1.3's adapter for each seed and
train one epoch on the latest natural rows (K4.8's set minus K1.3's 722 rows, about 1,765 rows; or K4.8's whole set),
peak 1e-4. About 25 to 30 minutes per seed. Every seed starts from the same seed's K1.3 adapter. Then the same gates.

## Questions

1. Is this more likely than a fresh candidate to pass both gates? Name the strongest reason for and against.
2. Which rows: natural rows only, or K4.8's whole set (template rows included, so the stage keeps rehearsing what
   K1.3 learned)? Which learning rate and epochs, taken only from the earlier recorded stage (1 epoch, 1e-4), not
   invented?
3. Which checkpoint is read (the stage has one epoch, so one checkpoint)? Anything that must be disclosed?
4. Your prediction, seed 82: Demo2 older of 6, never-told of 4; hard_dev never_told of 48 and recall.

## Output

Write to `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\OUTFILE`:
a recommendation line first (adopt, adopt with changes, reject), then the four answers. Reply with the
recommendation line only.
