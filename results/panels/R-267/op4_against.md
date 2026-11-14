Recommendation: run OP4 changed: decline rows must have the same shape as answer rows (first cut search misses, the second search returns the trap's wrong value, then a decline), drop rows with no first call, count both pools and stop before training if either side is under 10, run C1 (OP's seed adapter, the same stage on OP's own seed set) in the same window, and log second-search and cut-reply counts on every gate.

# Against lane: OP4 (on-policy second-search rows), 2026-11-14

Counts are from the brief, R-253 to R-265, and `reach2.py`. "Estimate" marks arithmetic on those counts, not a measurement.

## 1. Same lever as K4.9/R2d?

Same row shape: two calls, first masked, the source found by the second, value reply. Same rate and epoch. R2d (27 such
rows from K1.3) moved hard_dev from 46 / 2 to 42 / 6. Two real differences: (a) the direction. K4.9 taught "miss with
writer words, then hit with the question's words"; at test time the first query is already the question's words
(R-205), so that lesson had nothing to act on. OP4 teaches "miss with the question's words, then try other words", the
case that occurs at test time. (b) Fact 2 is a measurement: 106 of 117 user-fact errors are search misses, a class OP
and OP3 could not reach, and fact 3 shows 76 of 108 are reachable by other words. So it is a different lever aimed at a
measured class. The risk mechanism is the same as R2d's, and the dose is larger (below).

The weak point: `second_query` was written by a writer who saw the source message. 76 of 108 is the writer's reach,
not the model's. If many second queries use words found only in the source (not inferable from the question), the
model learns to make a second call whose guesses miss. `reach2.py` does not count that. Not checked.

## 2. Demo4's four older misses (R-262)

- Q1, Q4 (declines with the source second in the output): not search misses. OP4 does not target them; only indirect
  help, if some second outputs hold the source below another person's passage.
- Q5 ("instrument", chat said "ukulele", reply "not stated"): the target class, but the empty-first-output case is only
  7 of the 76 reached, and a second query may not hold "ukulele" (a value word). Reaching it needs a word like "play"
  or "learning" that the model has to guess.
- Q3 (reply only a search call, cut at the reply length): OP4 makes this worse. Two calls per reply use more of the
  length; more replies may be cut before the answer. Not checked whether the length counts tool calls.

So at most one item (Q5) is a direct target, and Demo4 needs exactly one more. The simplest explanation of one more
item is a second stage: C0's stage alone moved Demo4 older from 1 to 2 with no new rows.

## 3. hard_dev risk (estimate)

OP's room: never_told 48 against 44 (4), false retrieval 1 against 5 (4). R2d's shift from K1.3 was -4 and +4. The same
shift from OP lands at 44 / 5, both exactly on the lines. Dose: 76 user + 12 other reached, less up to 7 with no valid
first call, gives about 80 answer rows before balance; with one-to-one, about 30 to 50 a side if the trap pool
holding the value is about 32 to 50 (round 2 had 30 correct declines and 2 decline rows with the value returned, round
1 had 18). That is 2 to 4 times R2d's 27. A second search on a never-told question finds more near-miss passages;
that is how R2d got 6.

## 4. Balance and the decline row

Count: 125 traps exceed the need, but only those whose search returns the wrong value make a useful row (68 did not in
round 2). "Two searches then decline" is right only when the second output holds the trap's value, so the only
difference between an answer row and a decline row is whether the passage fits the question. A decline after two empty
searches teaches "two calls then stop", which does not guard false retrieval. The 375 items hold no plain never-told
questions, so that case gets no rows; disclosed, not fixed here. Check that trap items carry a `second_query` at all.

## 5. Control, stop rule, logs

1. C1 as registered in R-263 (never run), on seed 82 beside OP4. It costs about one hour; both fit before 14:00.
   If C1 passes too, the record cannot credit OP4 rows; the pick still goes by the gates.
2. Stop rule: the registered 10 answer rows, and the same 10 on the decline side, counted before training.
3. Drop the up to 7 rows with no first call (`reach2.py` puts "no query left after the cut" and "empty output" in one
   bucket); report how many.
4. Log on hard_dev and Demo4: second searches made, how many false retrievals followed a second search, replies cut at
   length. Without these, a fail or a pass says nothing about the lever.
5. If OP4 fails hard_dev, no smaller-dose retry today; that is a draw. Then report K1.3 as the pick.
6. Demo4 has now been read 3 times to choose levers (this design is aimed at its misses). Demo5 stays unread until a
   try clears Demo4.

Prediction (estimate): hard_dev at or near the lines; Demo4 older 2 or 3 of 6.
