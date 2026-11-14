# Against lane brief: a second on-policy round (OP3), written 07:12 EST Sat 2026-11-14

You are the against lane. Argue with the preferred answer below; say plainly if it should not run. No metaphors. One
page. Use no tools except writing your answer to the output path given in the task. Read nothing else.

## Setting

A LoRA adapter on a small open model (Tiny Aya Global) answers questions about a user's earlier chat with a keyword
search tool, or says it was not told. The shipped pick is K1.3. A new candidate must beat K1.3 on every gate:
- seed 82 hard_dev: never_told at least 44 of 48, false retrieval at most 4;
- Demo4 (a fresh writer's chat, two blind judges): at least 3 of 6 older questions right AND at least 3 of 4
  never-told right, with search; then Demo5 (held out) at the same lines;
- then seeds 83 and 94 trained and full screening (20 lines), and higher pick recall over seeds 82, 83, 94.
Deadline: a try must clear seed 82's gates by 14:00 today; it is 07:12. Every try's training set must pass the set
checker with 0 FAIL first. Every lever is registered in the record before its result exists.

## What happened (counts)

- K1.3 seed 82: hard_dev never_told 46, false retrieval 2, recall 52. Demo4 with search: older 1 of 6, never-told 2
  of 4 (bombs).
- C0 (control: K1.3 + 1e-4 x 1 epoch on its own 1,094 rows): hard_dev 48 / 0 / recall 54. Demo4 older 2 of 6,
  never-told 2 of 4 (bombs).
- OP (round 1 on-policy): K1.3's seed adapter answered 375 items built from its own training chats (250 older, 125
  traps). Rows were built from its own turns: an older item it got wrong whose own search (queries cut to the
  first-query rule, search rerun) returned the source message gets the writer's answer; a trap where it named the
  stored value gets a decline; the decline side is filled with its own correct trap declines; both sides cut one to
  one by a hash; check_false rows added to the 15% line. Seed 82: 36 corrections (18 answer, 18 decline) plus 7
  check_false, beside K1.3's 1,094 rows; stage 1e-4 x 1 epoch from K1.3. Result: hard_dev never_told 48, false
  retrieval 1, recall 60. Demo4 older 2 of 6 (bombs), never-told 3 of 4 (meets the line). OP's four older misses: two
  declines after search, one "not stated" with no value, one reply that is only a search call. Seed 83's set had 18
  corrections, seed 94's 24.
- The earlier lane predicted OP: Demo older about 2, false retrieval 4 to 6, never_told down 1 to 3. Older held at
  2; false retrieval and never_told came out better than predicted.
- Of K1.3's 250 older items on seed 82, 178 were wrong; only 48 of those had the source in its own search results
  (130 never returned it). After query cutting and the checker's drops, 40 answer rows were built; the user-fact share
  cut (facts about the user at least a third) and the one-to-one balance left 18.
- OP2 (registered, running now): the same method from T6 (a K1.3 descendant with hard_dev 44 / 4 / recall 72, which
  errs by naming wrong values), rehearsal T6's own 2,487-row set. Its result is not known.
- Across about 25 earlier seed-82 tries (other row sets, rates, epochs, blends), passes sat at the gate lines and moved
  by about 4 on a 10-row edit; every try that named a third Demo older item sat at false retrieval 4 or more.

## Preferred answer (argue against it)

If OP2 fails a gate, run **OP3: a second on-policy round from OP's seed adapter**. OP's seed adapter answers the same
375 items; rows from its own new mistakes are built by exactly OP's rules (same cuts, same balance, same checker
lines); the stage trains from OP's seed adapter, 1e-4 x 1 epoch, on round 2's corrections plus round 1's corrections
plus K1.3's 1,094 rows (corrections aggregated across rounds). Seeds 83 and 94 first train OP's stage on their own
round-1 sets (about 12 minutes each), then their round-2 eval and build. Gates as above.

## Questions

1. Is OP3 a different approach or another draw of the same kind? Give the strongest case each way.
2. The binding failure is Demo older (declines after search). Does a second round add enough answer rows to move it,
   given the counts above? Estimate how many answer rows round 2 could give, from the counts only, and say it is an
   estimate.
3. What simpler change could explain any gain (a control), and is one needed before reading OP3's result?
4. Run it, run it changed (say exactly how), or do not run it. One recommendation, first line.
