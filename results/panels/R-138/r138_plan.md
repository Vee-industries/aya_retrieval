# R-138 draft: break tests after the last try

## Kevin's word, 2026-11-08 ~19:00
"alright we're calling this the last try then we're going to start adding comparison tests so we can break it and if we find anything specific we can target that"

## Facts
- Project: LoRA on CohereLabs/tiny-aya-global so it searches an earlier chat for facts out of view (3 exchanges in view) and answers them, and does not search for facts in view, never-told facts or plain chat. Kinds: older, confirm (recall), in_view, never_told, statement.
- Shipping copy 6.37 (fix17cs37 seed 82). 6.38 (fix17cs38) is the last try, trained at 82 and 83 now, 97-99 overnight if its judged sheets pass. Model freeze Tue Nov 10; nothing starts after Mon Nov 9 12:00. Training is ~34 min a seed.
- Existing tests at seed 73157 (24 items a kind, chat sizes 58 and 419 messages, 1 decoy = a same-type fact about another person): plain probe and hard_dev; user-style typing; phone-style typing (held out of training); corrections (train and held-out wordings); asked-before. Existing gates (R-076, R-086, R-094, R-097, R-099, R-102) never move.
- Eval knobs that already exist and build on both pools (checked on CPU, 240 of 240 items each): `--decoys 3`, `--sizes 1000 2000`, and stress flags compose (phone + corrections + decoys 3). `--decoys 5` fails on probe (a fact type has too few values). Seeds 74xxx and 75xxx have never been used for any result.
- Base with no adapter is weak (probe recall 30 of 96 at 73157; hard_dev 20 of 96).

## Proposal
1. Discovery seed 74001, confirm seed 75001 (reserved, untouched until a targeted fix exists).
2. Conditions at 74001, probe and hard_dev, 24 items a kind, tool_loop arm:
   - plain (reference at this seed)
   - decoys3 (`--decoys 3`)
   - long (`--sizes 1000 2000`)
   - combo (`--phone-style --corrections --decoys 3`)
3. Models: base, 6.37 seed 82, 6.38 seed 82 (6.38 only if its judged sheets pass). 4 conditions x 2 pools x 3 models = 24 runs, ~10-15 min each, queued after 6.38's runs (~01:10 to ~07:00).
4. "Found something specific" = an adapter's score in a condition falls below its own plain score at 74001 by R-099's trigger (at least 8 of 192 on recall pooled over the two sizes, or 4 of 96 on any other kind), or below base in that condition on any kind. Then I read its misses and name the failure.
5. A targeted fix: training rows from the TRAIN pool only, never from probe/hard_dev items; trained from scratch at 82 and 83; must pass every existing gate unchanged against 6.37, and beat 6.37 in the broken condition at confirm seed 75001 (pooled over 82 and 83, ties fail). Must start before Mon 12:00. Otherwise 6.37 (or 6.38 if it wins) ships, and the break results go in the write-up as limits.
6. Reported per run with spread beside pooled counts (R-137).
