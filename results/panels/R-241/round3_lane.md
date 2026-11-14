# Design lane, round 3 levers (against-minded)

Read: the brief, `scripts/records/build_k3.py`, `docs/k4_4/WRITER_BRIEF.md`. Nothing else. Training and eval minutes
are not in those files, so cost is given in units of runs already done (one T stage, one seed 82 screen); the
minutes are unsourced here and must come from the run logs.

## 1. Ranked levers

1. **L1. Stage from K4.6 epoch 3, 1e-4, 1 epoch, on its own set's two-search fact rows only (meta `searches` = 2 and
   `names_value` true), to teach a second search after a first that returns passages without the fact.**
   Cost: one T stage plus one seed 82 screen. Data: a filter over the existing set's provenance `meta`; no new
   writing. Code: a few lines to select rows by meta. Why first: K4.6 epoch 3 already passes hard_dev (46 / 4 / 72,
   best recall on record) and is one Demo2 item short; the measured cause of misses is retrieval (3 of 4 unanswered
   items never returned; 65 of 108 outside-writer misses searched once and stopped), and this targets that cause
   and nothing else. Odds against: false retrieval is at the limit (4 of 4), and more searches bring back more
   same-type facts, so one more false retrieval fails it. Drop if round 2's miss-then-hit rows are already staged
   on K4.6 epoch 3.
2. **L2. Stage from T4, 1e-4, 1 epoch, on the K4.4 other_person and contrast rows only, as pairs, to repair T4's
   wrong-person answers while keeping its Demo2 3 / 3.** Cost: one T stage plus one screen. Data: K4.4 rows (exist
   if K4.4 was built). Lever 2 lost recall (27) with unpaired scripted declines; pairs keep a value-naming row for
   every decline with the same search. Odds against: if K4.4's rows are already inside the 1,393 natural rows, T4
   saw them at 3e-4 and still made 12 false retrievals; the gap (38 to 44, 12 to 4) is large. I did not check
   whether they are included.
3. **L3. Merge-delta blend of K4.6 epoch 3 and T4 at w = 0.5, to test whether the recall-and-decline adapter and
   the Demo2 adapter combine.** Cost: no training; one screen. Code: the queued blend's code, pointed at K4.6
   epoch 3. Odds against: the two were trained from different starts, so only a blend of the merged weight
   changes (not of the A and B matrices) is meaningful; run only after the K1.3 and T4 blend shows any w that
   passes hard_dev.
4. **L4. Fresh K4.6 recipe (3e-4, 3 epochs) with `NEVER_TOLD_TWICE` off, to test whether K4.6's second never_told
   search is what pulls in other people's facts.** Cost: one fresh 3-epoch run plus one screen. Data: rebuild with
   one flag. Odds against: K4.6 epoch 3 passes hard_dev, so the flag is not the main harm, and turning it off may
   cost Demo2 retrieval. Lowest-value of the four; a cause test more than a candidate.

No fifth lever: every other one I could name needs a rate, epoch count or ratio not in the record.

## 2. Queued results that would change the ranking

- Round 2 "stage from K4.6 epoch 3 on K1.3's set": if it reaches Demo2 3 older and passes hard_dev, it is the new
  pick and L1 should start from it instead. If it drops hard_dev below 44, L1's odds fall (K4.6 epoch 3 does not
  take a stage well).
- Round 2 merged first query or miss-then-hit rows: a gain in Demo2 older confirms the retrieval cause and raises
  L1; no gain lowers L1 below L2.
- K1.3 and T4 blend: any w that passes both gates makes L3 first (cheap, same method); no w passing hard_dev drops
  L3.
- T6 passing hard_dev with Demo2 at 3 makes it the base for L1 and L2.

## 3. Must not be done

- No change to the tool, prompt, eval or gates; no rows written from hard_dev, Demo2 or Demo3 chats or questions.
- Demo3 stays read once per candidate; Demo2 not used to choose among stages beyond its 18 reads.
- No more unpaired scripted declines (Lever 2 measured the cost: recall 27).
- No rate, epoch count, blend weight or balance ratio outside the record.
- No pick on seed 82 alone: pick stays pooled recall over 82, 83, 94 after full screening.
