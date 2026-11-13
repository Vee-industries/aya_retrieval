# Against lane: the K4.8 training-set design

You are the against lane of a review panel. Your job is to argue with the design below and find what will make it
fail. Read only this file and the two files named under "Files you may read". Answer in one page or less, written to
the file named at the end. Plain words, no metaphors.

## The project

A LoRA adapter on a small chat model (Tiny Aya Global) that sees only the last 3 exchanges of a chat and searches
the older ones with a keyword tool (SQLite FTS, OR search, top 5 exchanges). It must answer with the stored fact when
it was told, and say it was not told when it was not, even when the search returns other text. Training rows are
whole chats ending in tool calls and a reply; loss is on the model's decisions.

Candidates are built on each other. Gates, in order: (1) Demo2: one fresh writer's chat, 6 "older" questions and 4
"never-told" questions, two blind judges; a candidate fails ("bombs") with fewer than 3 of 6 older or fewer than 3
of 4 never-told. The owner keeps this gate. (2) Screening over seeds 82 and 83: hard_dev never_told at least 44 of
48, false retrieval at most 6.37's plus 3, recall above base on several sets. (3) Pick by pooled recall over seeds
82, 83, 94. The registered shippable pick now is K1.3 (Demo2 older 0 of 6, pick recall 742). Deadline: every seed
trained by Saturday 16:00 ET; one seed trains in about 55 to 75 minutes.

## History, seed 82 (Demo2 older of 6 / never-told of 4; hard_dev never_told of 48, false retrieval, recall)

- K4.1 4 / - ; 34, 8, 65 (failed screening on never_told)
- K4.4 1 ; K4.5 2 / 4 ; 47, 2, 72
- K4.6 (K4.5 + never-told rows search a second time when the first returns text) 2 / 4 at epoch 3; 46, 4, 72;
  outside-writer recall 132 (K1.3 89)
- K4.6 read at its epoch-2 checkpoint ("K4.6e2", a checkpoint chosen after epoch 3 bombed, disclosed as a forking
  path): 3 / 4. It is now in screening as a candidate.
- K4.7 = K4.6 + 64 natural chats from 8 new writers (128 chats total): 2 / 2. Diagnosis: the 64 new chats added value
  rows but none of the near-miss and wrong-person never-told questions, which exist for the first 64 chats only; on
  Demo2 K4.7 named a value on both never-told items that share a word with a stored fact.

On the outside-writer sets, K4.6's misses are mostly facts its searches never return (39 and 34), then found and
declined (8 and 8). In 61 of 66 never-found misses (measured on K4.1) the model searched once, got passages without
the fact, and stopped.

## What the training data teaches after a search returns text (K4.7, counted on its 2,286 rows)

After a search output that holds passages, the next step is:

- natural fact rows (older, confirm): search again 42, reply 654
- natural never_told rows: search again 94, reply 264
- template rows (722 rows from K1.3): search again 0, reply 722

Of the natural rows that search again after text, by a rough phrase match on the reply: never_told decline 70, never_told
value 24 (the match is rough), older or confirm value 39, older or confirm decline 3. So most "search again after
text" rows end in a decline.

## The proposed K4.8

K4.7 whole, plus two additions:

A. **The never-told balance restored for the 64 new chats**: the near-miss brief (K4.1's) and the wrong-person brief
   (K4.4's), unchanged, run by 4 new writers over the new chats, built by the same steps and keep rules as before.
   This is the existing rule on more data.

B. **Miss-then-hit rows** (new). Writers read each chat and, for every older and check_true question (768
   questions over 128 chats), write a `miss_query`: 1 to 4 words taken from the question, no filler, not the
   question's own query, no word of the value, that should return other messages but not the source message. The
   build runs the real search: a row is kept only if the miss_query returns at least one passage and not the source
   message, and the writer's own `query` then returns the source message. Row: search(miss_query) -> passages
   without the fact; search(query) -> the fact; the writer's reply naming the value. Added as new rows beside the
   existing row for the same question (the existing row stays). Expected yield is unknown; it could be several
   hundred rows against the 42 that exist now.

Training as every K4.x: 3 epochs, epoch-2 checkpoint saved.

## Questions for you

1. Does B address the stated failure (search once, get text, stop), or does it teach something else? What would it
   do to never-told and false retrieval, given that never_told rows decline after a second text-returning search?
2. How many B rows, and where in the build: before or after the decline/value balance step (which equalises declines
   and value rows at each passage count of the last search)? Give a rule that does not invent a number, or say which
   number and why.
3. A and B stacked in one candidate: acceptable given the deadline, or split? If split, which first?
4. Which checkpoint is read for K4.8's Demo2 gate, decided now before training: epoch 3 only, epoch 2 only, or epoch
   3 then epoch 2 if 3 bombs (two tries at one gate)? Say what each choice costs.
5. Anything in the design that tunes to Demo2's or hard_dev's items, and should be removed?
6. Your prediction for K4.8 seed 82: Demo2 older of 6 and never-told of 4; hard_dev never_told of 48.

## Files you may read

- `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval\scripts\records\build_k3.py` (how rows are built)
- `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval\docs\k4_8\WRITER_BRIEF.md` (the draft brief for B)

## Output

Write your answer to
`C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\lane_against.md`:
a verdict first (adopt, adopt with changes, or reject), then one numbered answer per question. Reply with the
verdict line only.
