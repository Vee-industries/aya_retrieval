# Against lane: on-policy corrections (written 04:50 EST, Sat 2026-11-14)

**Recommendation: do not run it as written. Run seed 82 only, on K1.3, after three changes: (1) balance the
correction rows by type, (2) train a rehearsal-only control on the same 1,094 rows at the same settings, (3) print
the row counts by type and the chat-id overlap with every gate set before training. Expect the same trade unless the
balance holds.**

## 1. Different approach, or another draw?

For: this is the first try whose rows come from what the model really sees. Its own queries return result lists
that mix the source message with other people's facts. Writer rows came with writer queries and writer-chosen
results. K1.3's known fault (Demo2 older 0 of 6, declining facts its own search found) is a fault in reading its
own result lists, and only on-policy rows show it that input. That changes the material of the trade, not only the
mix.

Against: the label rule decides the outcome, and the label rule is lopsided. K1.3 errs mostly by declining (Demo2
older 0 of 6) and rarely by naming a wrong value (hard_dev false retrieval 2 of 48). Applying those rates to the
proposed sample (my estimate, unsourced beyond those two figures): about 127 trap items give about 5 decline rows;
about 254 older items give tens of "answer" rows. The correction set is then mostly "answer when the search shows
something", which is the same lever every earlier try pulled. Also, the sample is K1.3's own training chats, so its
error rate there is lower than on new chats and the errors it does make are the rows it failed to fit once already.
A set of a few dozen rows against 1,094 rehearsal rows is about the size of the 10-row edit that moved hard_dev by 4,
so a gate pass would sit inside the gates' own variation again. As written, it is most likely another draw.

## 2. Prediction for seed 82

Demo2 older: up, to about 2 of 6. hard_dev false retrieval: up, to 4 to 6. never_told: down 1 to 3 from 46.
Recall: up some. That is the same trade line the earlier tries sit on. These are estimates from the figures in the
brief, not measurements.

## 3. Leakage, circularity, and what must change

- No screening set is read, so no direct leakage. But the training trap questions use the same construction as
  hard_dev (another person's same-type fact). Confirm by chat id that no hard_dev, Demo2 or Demo3 chat, and no chat
  made from the same writer template instance, is in the sample. Print the overlap count; it must be 0.
- The seeds stop being seeds. Each seed trains on its own correction set, so the 82/83/94 spread now mixes data and
  initialisation. Report it as such; do not compare that spread with K1.3's seed spread as if it were the same thing.
- Must change before it runs:
  - Balance. Add the model's own correct trap declines (items it got right) as rows until decline rows equal answer
    rows. Equal counts is my rule, unsourced; the reason is the asymmetry above. If fewer than about 20 decline rows
    exist (unsourced floor), widen the trap sample, not the older sample.
  - Rehearsal-only control. 1,094 K1.3 rows at 1e-4 x 1 epoch is a second epoch of K1.3 by itself and can move the
    gates alone. The simplest baseline that could explain any change must be measured and reported first.
  - The "search returned the source message" test must be an exact match on the stored message id in the tool's real
    output, not a text match, or rows where it saw only a near-miss get an "answer" label and teach false retrieval.
  - Report row counts by type, and the 25-minute eval's own score on the sample, before training.

## 4. K1.3 or T6 as the base

K1.3 for seed 82 now. It is the pick, it has all three seeds, and the decision is made against it. T6 has the better
error profile for this method (it errs by naming wrong values, so its corrections would be decline rows and would
press on the binding gate), but its false retrieval is already at the limit (4), only seed 82 exists, and seeds 83
and 94 cost about 160 minutes before their correction sets can even be built. If K1.3 seed 82 shows only the trade
after balancing, T6 seed 82 is the second try, still inside the 14:00 deadline only if started by about 09:00.
