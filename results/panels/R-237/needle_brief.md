# Against lane: two levers aimed at the Demo-versus-hard_dev trade

Read only this file. Answer in under one page, written to the file named at the end. Plain words, no metaphors.

## Setting

A LoRA adapter (rank 32, alpha 64) on Tiny Aya Global searches a chat's older history with a fixed keyword tool and
must name the stored fact when told and say "not told" when not. Gates: Demo2 (one writer's chat, read 17 times now;
pass at 3 of 6 older and 3 of 4 never-told), Demo3 (a second chat, read once), then screening per seed 82 and 83:
hard_dev never_told at least 44 of 48 (built with a same-type fact about another person), hard_dev false retrieval
at most 4, recall above base, more lines. Deadline: every seed trained by Saturday 16:00 ET (now Friday 19:00).

## The trade, measured (seed 82)

| Adapter | Demo2 older / never-told | Demo3 | hard_dev never_told / false retrieval / recall |
|---|---|---|---|
| K1.3 (the pick) | 0 / 4 | not run | 46 / 2 / 52 |
| T1: K1.3 + 1 epoch, 1e-4, K4.8 whole set | 2 / 4 | - | - |
| T4: K1.3 + 1 epoch, 3e-4, K4.8 natural rows only | 3 / 3 | 4 / 3 | 38 / 12 / 59 |
| K4.6 epoch 3 (fresh) | 2 / 4 | - | 46 / 4 / 72 |
| K4.6 epoch 2 | 3 / 4 | - | 39 / 10 / 75 |

Every candidate that reaches 3 Demo2 older items fails hard_dev never_told and false retrieval; every one that passes
hard_dev stays at 2 or fewer.

## The two levers

1. **Blend.** One adapter whose weight change is exactly (1 - w) x K1.3's change + w x T4's change, written as a
   rank-64 adapter (A stacked, B scaled side by side, alpha doubled; checked exact on every layer at w = 0 and 1, and
   a planted wrong weight shows a gap). Proposed w = 0.5, the midpoint, one try. No training; about 20 minutes to a
   Demo2 result. For seeds 83 and 94, T4's stage would first be trained on those seeds (about 25 minutes each).
2. **T4 plus K1.3's never-told rows.** T4's rows (K4.8's 1,393 natural rows) dropped every K1.3 row, including K1.3's
   160 never_told rows (scripted declines, some built for hard_dev's same-type trap in an earlier fix). Set: those
   1,393 plus the 160, unchanged. Stage on K1.3 at T4's setting (3e-4, 1 epoch). About 25 minutes to a Demo2 result.

## Questions

1. For each lever: more likely than not to pass both Demo gates and hard_dev? Strongest reason for, strongest against.
2. Blend: is w = 0.5 the honest single choice, or should more than one w be tried, and if so how many and which,
   without that becoming a search over a curve until one passes? What must be disclosed?
3. Order of the two, and against the remaining registered tries (T5 running, T6, then round 2's four).
4. Prediction, seed 82, for each: Demo2 older, never-told; hard_dev never_told, false retrieval.

## Output

Write to `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\needle_against.md`:
a recommendation line first, then the four answers. Reply with the recommendation line only.
