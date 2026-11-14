# Design lane: round 3 levers, for after round 2 and the blend

Read only this file and the files named under "Files you may read". Answer in one page or less, written to the file
named at the end. Plain words, no metaphors. Be against-minded: rank by honest odds.

## The project

A LoRA adapter (rank 32) on Tiny Aya Global (a small chat model) sees only the last 3 exchanges and searches older
ones with a fixed keyword tool (SQLite FTS, OR search, top 5 exchanges, at most 3 calls). It must name the stored fact
when told and say "not told" when not. Tool, prompt, eval and gates are fixed.

Gates, in order now: seed 82 hard_dev (never_told at least 44 of 48, built with a same-type fact about another
person; false retrieval at most 4); Demo2 (one writer's chat, 6 older and 4 never-told, pass at 3 and 3; read 18
times); Demo3 (a second chat, read once); full screening on seeds 82 and 83; pick by pooled recall over 82, 83, 94.
Current pick K1.3. The owner's standing order: keep trying until a candidate beats K1.3, then beat that, until
Saturday 16:00 ET (every seed trained); a try must clear seed 82 by about Saturday 10:00. Now Friday 20:50.

## Results, seed 82 (Demo2 older / never-told; hard_dev never_told / false retrieval / recall)

| Adapter | Demo2 | hard_dev |
|---|---|---|
| K1.3 (fresh, 1,094 template rows, 3 epochs, 3e-4) | 0 / 4 | 46 / 2 / 52 |
| K4.6 (fresh, templates + about 1,000 natural rows) epoch 3 | 2 / 4 | 46 / 4 / 72 |
| K4.6 epoch 2 | 3 / 4 | 39 / 10 / 75 |
| Stages on K1.3, 1 epoch unless said: T1 1e-4 whole K4.8 set | 2 / 4 | - |
| T2 3e-4 whole | 2 / 3 | - |
| T3 1e-4 natural only (1,393 rows) | 2 / 3 | - |
| T4 3e-4 natural only | 3 / 3 (Demo3 4 / 3) | 38 / 12 / 59 |
| T5 1e-4 whole, 3 epochs | 2 / 4 | - |
| Lever 2: T4's rows + K1.3's 160 never_told rows, 3e-4 | - | 43 / 5 / 27 |

Queued: T6 (3e-4 whole, 3 epochs), round 2 (merged first query; a stage from K4.6 epoch 3 on K1.3's set; third-search
rows; miss-then-hit rows), then a blend of K1.3 and T4 at w = 0.33, 0.5, 0.67.

Pattern: the adapters that reach 3 older (K4.6 epoch 2, T4) name another person's same-type fact on hard_dev; the
ones that pass hard_dev stay at 2 or fewer. Every adapter answers the same 2 Demo2 older items; of the other 4, three
are never returned by its searches (the tool can return them: K4.1's searches once returned all four) and one or two
are found and declined. On K4.6's outside-writer misses, 65 of 108 searched once, got passages without the fact and
stopped. Lever 2 shows that adding K1.3's scripted declines takes real facts too (recall 27).

## Questions

1. Up to 5 round-3 levers not already tried or queued, ranked, each one plan line (one purpose), cost in minutes,
   data or code need. Numbers only from the record (rates 1e-4 or 3e-4, epochs 1 or 3, existing sets, adapters,
   builds, briefs) or a measurement; nothing invented. The fixed tool, prompt, eval and gates are not levers.
2. Which result from the queued tries would change your ranking, and how?
3. Anything that must not be done.

## Files you may read

- `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval\scripts\records\build_k3.py`
- `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval\docs\k4_4\WRITER_BRIEF.md`

## Output

Write to `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\round3_lane.md`:
the ranked list first, then answers 2 and 3. Reply with the top lever's plan line only.
