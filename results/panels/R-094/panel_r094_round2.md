# Panel round 2: the who-is-who slip (2026-11-06)

Every lane reads all four round-1 proposals and gives the one plan it would accept. The panel ends with
one plan all four accept.

## Round-1 proposals, in short

**Lane 1 (targets).** Measured: all 150 `confirm` targets are scripted ("Your {relation} {person} ...");
of 200 `older` targets, 60 are scripted and 140 are base's own replies; of those, 29 open "My <relation>",
28 open "<Name>'s ...", about 17 are odd. So every slip-shaped target is an `older` base reply.
1. Mechanical flip: rewrite only sentence openings ("My X[,] Y" / "Y's X" to "Your X Y"; "who is my" to
   "who is your"), checked by `item_correct` and by a no-pattern check, else the scripted answer. About 57
   targets; no regeneration.
2. Slip-checked regeneration with a hint not kept in the row, one retry, else scripted.
3. Scripted variety (two or three "Your {relation} {person}" phrasings a type) on slip rows.
4. Wider relations (diagnostic).

**Lane 2 (training).** 0. Diagnostic, no training: score 17m's saved epoch-2 adapters at seeds 87 and 84
and count the slip. 1. A new mask on found-fact answers: the search call keeps full loss, the reply after
the tool result keeps loss only on its first token and end marker (as 17m does for chat). 2. Mask only the
39 pattern rows. 3. Two epochs, only if the diagnostic shows the slip falls at epoch 2.

**Lane 3 (measurement).** The scorer cannot see the slip; judges disagree (15, 15, 6 at seed 87); 17m's
seeds 82-86 run 1-4 a seed and 87 is one tail seed; three clean seeds would happen 58% of the time by
chance with a 1-in-6 tail. Register first: the regex in `scoring.py` with known-bad and known-good cases,
skipping a hit the friend's own message contains; calibrate it once against judge 1 on 17m's Sheet A at
seeds 85-87; zero slip-shaped targets in the new set. A separate slip gate (R-076 and R-086 unchanged, v6
stays valid): probe slip count at most 5 of 96 every seed; pooled over five seeds at most 8 of 480 (17m:
13 over 82-86); `hard_dev` at most 3 a seed; recall not below v6's. Run the fix at seed 87 once, labelled
as chosen because it failed. Its own fix: replace the slip-shaped targets with the same item's other clean
base replies, else the scripted answer for those rows only. Caution: the slip's output rate (about 4.7%) is
below its target rate (11%), so cleaning targets may lower the median but not remove the tail.

**Lane 4 (against).** The shipped seed 82 is at base's rate (3 of 96); the slip is one tail seed in six, in
17b too, so it is the base model's own wording. Under R-088's ship rule a fix (two changes from 17b, not
aimed at recall) cannot replace 17m without a rule change, which is Kevin's. Data edits have cost before
(R-033, fix 20). Recommends no new fix: judge Sheet A on v6 seed 82, report the slip and its seed rate in
the write-up, ask Kevin whether one bad seed in six is acceptable, spend the compute on v6's stress tests.
If Kevin wants a fix, run it with the slip count reported, and settle the ship rule before results.

## Where they already agree

- The slip lives in the `older` base-reply targets, not `confirm`.
- The regex is needed as a measure; the judged count is too noisy to gate on alone.
- The tail is seed-level; a fix needs fresh seeds (88-90) and cannot be proven on 82 and 83 alone.
- Whether a fix may replace v6 is a ship-rule question for Kevin, settled before results.

## Where they differ

- Fix now (lanes 1, 2, 3) or report only (lane 4).
- Which fix: mechanical flip (1), clean replies else scripted (3), loss mask on answers (2).
- Whether the epoch-2 diagnostic runs first.

## Note from the runner

Kevin asked for this fix ("don't love that weak spot", "panel a fix"). The ship-rule question is put to
him in parallel with this round; the plan should say what runs either way.
