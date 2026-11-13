# Design lane: round 2 of the stage tries

Read only this file and the files named under "Files you may read". Answer in one page or less, written to the file
named at the end. Plain words, no metaphors.

## The project

A LoRA adapter on Tiny Aya Global (a small chat model) sees only the last 3 exchanges of a chat and searches older
exchanges with a fixed keyword tool (SQLite FTS, each query word quoted, OR search, top 5 exchanges, at most 3 calls).
It must answer with the stored fact when told and say "not told" when not told. The tool, prompt and eval are fixed.

Gates: (1) **Demo2**, seed 82: one writer's chat, 6 older and 4 never-told questions, two blind judges; fails under 3
of 6 older or 3 of 4 never-told. (2) **Demo3**: a second, unseen writer's chat, same rules, read only for a try that
passes Demo2. (3) **Screening** per seed 82 and 83: hard_dev never_told at least 44 of 48 (built with a same-type
fact about another person), false retrieval at most 4, recall above base, more lines. (4) Pick by pooled recall over
seeds 82, 83, 94. Current pick **K1.3** (passes screening; Demo2 older 0 of 6). Deadline: every seed trained by
Saturday 16:00 ET; now Friday 18:20. A 1-epoch stage try takes about 30 minutes to a Demo2 result; a 3-epoch one
about 80.

## What has been tried (seed 82, Demo2 older of 6 / never-told of 4)

- Fresh adapters on the base model, 3 epochs, K1.3's 1,094 template rows plus 1,000 to 1,400 natural writer rows
  (near-miss, wrong-person, contrast, possessive-free queries, a second search on never-told, 64 more chats,
  never-told questions for them, 27 miss-then-hit rows): 2 of 6 at epoch 3 on every one of eight; 3 of 6 only at
  K4.6 epoch 2, which then failed hard_dev (never_told 39, false retrieval 10).
- Round 1, stages on K1.3's adapter: T1 1e-4 x 1 epoch, K4.8 whole set: 2 / 4. T2 3e-4 x 1, whole: 2 / 3. T3 1e-4 x 1,
  natural rows only: 2 / 3. T4 (3e-4 x 1, natural), T5 (1e-4 x 3, whole), T6 (3e-4 x 3, whole) to come.
- Every try answers the same 2 older items and misses the same 4. Of the 4: on every try, one is found by the search
  and declined; three are never returned by the model's searches, though K4.1's searches once returned all four
  (so the tool can find them; the model's queries do not).
- On outside-writer dev sets (K4.6): of 108 older misses, 65 searched once, got passages without the fact and
  stopped; 8 searched twice; 35 found the fact and declined or answered wrong.

## What the training rows teach (build_k3.py)

A natural fact row's first query uses only words from the question (writer `query`); if it misses, a second query of
1 to 3 category words (writer `second_query`); if both miss, the row declines. The decline/value balance step keeps
declines in proportion at each passage count. Template rows (K1.3) are scripted chats from a fixed pool.

## Questions

1. List up to 6 round-2 levers, ranked by chance of passing Demo2 and Demo3 and screening, each one plan line (one
   purpose), its cost in minutes, and its data or code need. A lever's numbers must come from the record (learning
   rates 1e-4 or 3e-4, epochs 1 or 3, existing row sets and builds, existing adapters K1.3, K4.5, K4.6) or a
   measurement, never invented. Candidates to judge, and add others: start a stage from K4.6's epoch-3 adapter (it
   passes hard_dev, recall 72) instead of K1.3's; stage data that teaches a different first query (for example the
   writer's `second_query` first, or a person-plus-category query); rows where the fact is found and a value is
   named, so fewer found-and-declined; stage data from the K5 third-search build or the K4.9 miss-then-hit rows.
2. What must not be done (tuning to Demo2's or Demo3's items, or to hard_dev or the outside-writer sets)?
3. If round 1 and round 2 both fail, what should the owner be told?

## Files you may read

- `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval\scripts\records\build_k3.py`
- `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval\docs\k3\WRITER_BRIEF.md`

## Output

Write to `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\round2_lane.md`:
the ranked list first, then answers 2 and 3. Reply with the top lever's plan line only.
