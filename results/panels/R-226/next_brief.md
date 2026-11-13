# Design lane: the candidate after K4.9, or none

Read only this file and the files named under "Files you may read". Answer in one page or less, written to the file
named at the end. Plain words, no metaphors. You are the against lane: argue with what the owner wants to be true
(that one more candidate will pass), and say so if no candidate is justified.

## The project

A LoRA adapter on Tiny Aya Global (a small chat model) sees only the last 3 exchanges of a chat and searches older
exchanges with a keyword tool (SQLite FTS, each query word quoted, OR search, top 5 exchanges). It must answer with
the stored fact when told and say "not told" when not told. Training rows are whole chats ending in tool calls and a
reply; 3 epochs; the epoch-2 checkpoint is also saved. The tool and the prompt are fixed (the sealed test uses them).

Gates: (1) **Demo2**, seed 82: one fresh writer's chat, 6 older questions and 4 never-told (2 plain, 2 sharing a word
with a stored fact), two blind judges; bombs under 3 of 6 older or under 3 of 4 never-told. The owner keeps this gate
and has ruled twice that a bomb means the next candidate at once. (2) **Screening** per seed 82 and 83: hard_dev
never_told at least 44 of 48 (built with a same-type fact about another person), false retrieval at most 4, recall
above base on several sets. (3) Pick by pooled recall over seeds 82, 83, 94. Current pick **K1.3** (template rows
only; passes screening; Demo2 older 0 of 6). Deadline: every seed trained by Saturday 16:00 ET; it is Friday 16:20.
One seed trains in about 80 minutes; Demo2 comes about 85 minutes after a candidate starts. K4.9 is training now
(Demo2 about 17:40); it is K4.8 plus 27 rows and is expected within one item of K4.8.

## Results, seed 82 (Demo2 older of 6 / never-told of 4; hard_dev never_told, false retrieval, recall)

| Candidate | What it added | Demo2 | hard_dev |
|---|---|---|---|
| K1.3 | template rows (722), the pick | 0 / 4 | 46, 2, 52 |
| K3 | + natural writer chats (64) | 3 / 2 | - |
| K4.1 | + near-miss and contrast rows | 4 / - | 34, 8, 65 (fails) |
| K4.2 | + declines after two empty searches | 2 / - | 41, 7, 77 |
| K4.4 | + wrong-person rows | 1 / 3 | - |
| K4.5 | possessives out of every query | 2 / 4 | 47, 2, 72 |
| K4.6 | + never-told rows search twice | 2 / 4 | 46, 4, 72 |
| K4.6 epoch 2 | | 3 / 4 | 39, 10, 75 (fails) |
| K4.7 | + 64 more natural chats | 2 / 2 | - |
| K4.8 | + never-told questions for those chats | 2 / 3 (epoch 2: 2 / 2) | - |

On every K4 candidate the two older items answered are the same two; the misses are mostly facts never returned by
any search (the fact message uses words unlike the question) and one or two found and declined. On the outside-writer
dev sets (K4.6 seed 82), of 108 older and confirm misses, 65 searched once, got passages without the fact, and
stopped; 8 searched twice; 35 found the fact and answered wrong or declined. Training rows: after a search that returns
text, natural fact rows search again 69 times (K4.9) and never-told rows search again and decline 70 times. The
recall gain over K1.3 (52 to 72 on hard_dev) has held from K4.5 on; the Demo2 older line has not moved past 2 at
epoch 3 since K4.1.

## Questions

1. Is any next candidate more likely than not to pass both Demo2 and screening by the deadline? If none is, say so
   plainly, and say what the owner should be told.
2. If one is: describe it in one plan line (one purpose), what data or code it needs, how long to build, what it
   must not tune to (Demo2's items, hard_dev's items, the outside-writer sets are screening sets), and a prediction.
3. If K4.9 passes Demo2 at 17:40, does your answer change?

## Files you may read

- `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval\scripts\records\build_k3.py`
- `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval\docs\k3\WRITER_BRIEF.md`

## Output

Write to `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\next_against.md`:
an answer line first (a candidate, or none), then the three answers. Reply with the answer line only.
