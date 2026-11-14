# Against lane: round 4, or stop

Read only this file. Answer in under one page, written to the file named at the end. Plain words, no metaphors.

## Setting

A LoRA adapter on Tiny Aya Global searches older chat history with a fixed keyword tool and must name the stored
fact when told and say "not told" when not. Gates on seed 82, in order: hard_dev (never_told at least 44 of 48, false
retrieval at most 4), Demo2 (6 older and 4 never-told; pass at 3 and 3; read 21 times), Demo3 (a second chat, read
twice), then full screening on seeds 82, 83 and pick recall over 82, 83, 94 against the pick. The pick is **K1.3**
(pick recall 742). Owner's standing order: keep trying until a candidate beats the pick, until a try's seed 82 gates
are cleared by Saturday 14:00 ET (now 04:40); every seed trained by 20:00. Every lever is registered before it runs.

## Seed 82 results of the stage tries on K1.3 (hard_dev never_told / false retrieval / recall; Demo2 older / never-told)

| Try | hard_dev | Demo2 |
|---|---|---|
| K1.3 itself | 46 / 2 / 52 | 0 / 4 |
| T4: natural rows, 3e-4 x 1 | 38 / 12 / 59 | 3 / 3 (Demo3 4 / 3) |
| T6: K4.8 whole, 3e-4 x 3 | 44 / 4 / 72 | 2 / 4 |
| Lever 2: T4's rows + K1.3's 160 declines | 43 / 5 / 27 | - |
| R2a merged query | 42 / 6 / 68 | - |
| R2b from K4.6 on K1.3's set | 42 / 8 / 72 | - |
| **R2c: K5 third-search set, 1e-4 x 1** | **45 / 4 / 63** | **3 / 4 (Demo3 4 / 4)**; passed all 20 screening lines, pick recall 868; **not eligible**: its set failed one check line (user facts 32.9%, under a third) |
| R2cf: R2c on K5's set less 10 rows (fixed to pass) | 41 / 7 / 66 | - |
| R2d: K4.9 set | 42 / 6 | - |
| Blend K1.3 + T4, w 0.33 / 0.5 / 0.67 | 46 / 2; 44 / 5; 44 / 4 | 0.67: 2 / 3 |
| T1, T2, T3, T5 | not run | 2 of 6 |

Now running: a blend of T6 and T4 at w 0.33, 0.5, 0.67 (hard_dev first; the highest passing w reads Demo2 once).

Two findings: (1) hard_dev's lines sit inside its own variation: 10 rows fewer turned R2c's 45 / 4 into 41 / 7; the
K1.3 + T4 grid went pass, fail, pass as w rose. (2) Every try that answers a third Demo2 older item sits at or past
hard_dev's false retrieval line.

## Questions

1. Are further tries finding real gains, or mostly drawing again from the same variation until one lands on the right
   side of all the lines? Say which, plainly.
2. If any lever is worth the card before 14:00, list at most 3, ranked, each one plan line, cost, and why it is not a
   redraw. Numbers only from the record (rates 1e-4, 3e-4; epochs 1, 3; existing sets, adapters, builds).
3. What should the owner be told at 14:00 if nothing passes, and what is the one decision for him?

## Output

Write to `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\round4_against.md`:
an answer line first, then the three answers. Reply with the answer line only.
