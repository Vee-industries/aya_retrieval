Recommendation: run OP3 changed: check the two Demo4 search-declines first, stop if round 2 builds fewer than 10 new answer rows, dedupe by item, and run a registered same-stage control beside it.

# Against lane: OP3 (second on-policy round), 2026-11-14

All counts below are from the brief. Anything marked "estimate" is arithmetic on those counts, not a measurement.

## 1. Different approach or another draw of the same kind?

Case that it is different: round 2's rows come from OP's own mistakes, not K1.3's, and aggregating corrections across
rounds is the standard iterated on-policy method. OP's errors are not K1.3's errors: its four Demo older misses are
two declines after search, one "not stated" with no value, and one bare search call, while T6 errs by naming wrong
values. A second round asks a question round 1 did not: are the errors left after one correction round still
correctable from the model's own search results?

Case that it is the same kind: the same 375 items, the same cuts, the same balance, the same checker lines, the same
rate and epoch, the same 1,094 rehearsal rows. The only change is which roughly 10 to 30 rows sit beside 1,094. About
25 earlier tries show that a 10-row edit moves passes by about 4 at the gate lines, and none of them moved Demo older
to 3 without false retrieval reaching 4 or more. On that record OP3 is one more small-edit draw. I judge it closer to
this side.

## 2. Can round 2 add enough answer rows? (estimate)

Round 1 funnel on seed 82: 178 wrong, 48 with the source in its own results (27%), 40 built, 18 kept (45% of 40).
The user-fact cut and the one-to-one balance, not the build step, cut it most.

For round 2: the 130 items whose search never returned the source stay out of reach; the method cannot build a row
for them. Of the 48 reachable, some of the 18 trained items are now right and drop out. If OP's search hit rate is
unchanged, the reachable wrong pool is about 20 to 35 items; at round 1's 83% build rate and 45% keep rate that gives
about 7 to 13 new answer rows. Estimate only: OP's per-item results on the 375 are not in the brief.

So aggregated answer rows go from 18 to about 25 to 31. That is a 10-row-scale edit, the size that history says
moves hard_dev by about 4 and has not reached a third Demo older item cleanly. Two of OP's four Demo misses (the bare
search call, the "not stated" reply) are not the decline-after-found-source class these rows teach. Round 2 can only
plausibly reach the two declines after search, and only if search returned the source for them. If it did not, OP3
cannot move Demo older at all, whatever it builds.

Risk on the other gate: OP has false retrieval 1, so 3 of headroom. More answer rows push toward answering, and the
record ties a third Demo older item to false retrieval 4 or more. A pass at exactly 4 is a pass at the line, not a
margin.

## 3. Control

C0 already shows that one more 1e-4 x 1 epoch stage on K1.3's own rows moved Demo older 1 to 2 and never_told 46 to
48 with no on-policy rows. OP's gain over C0 is small: Demo never-told 3 of 4 against 2 of 4 (one item), recall 60
against 54, false retrieval 1 against 0. For OP3 the matching control is C1: OP's seed adapter, the same stage, on
round 1's corrections plus K1.3's 1,094 rows, with no round-2 rows. Without C1, an OP3 gain cannot be split between
"a second stage" and "new on-policy rows". C1 is not needed to read a gate pass (a pass ships on the gates), but it
is needed before the record says why. It costs one stage (about 12 minutes) plus evals, so register it with OP3 and
run it beside OP3, not after.

Note: Demo older has n = 6, so one item is 17 points. Demo4 has now selected among several tries; Demo5 is the only
unseen check and must stay unseen until a try clears Demo4.

## 4. Run it, changed

1. Before building: read OP's Demo4 logs for the two declines after search. If search did not return the source
   for either, do not run OP3; it cannot reach the binding failure.
2. Register a stop rule before the round-2 build: fewer than 10 new answer rows after all cuts means no training.
3. Dedupe by item: an item corrected in round 1 and still wrong in round 2 gets one row, not two copies.
4. Register C1 (above) at the same time as OP3 and run both on seed 82.
5. Keep every other rule as written. Seed 82's eval, build, checker and stage fit the 14:00 deadline only if OP2's
   result arrives early; seeds 83 and 94 (18 and 24 round-1 corrections, so likely fewer round-2 rows) run after.
