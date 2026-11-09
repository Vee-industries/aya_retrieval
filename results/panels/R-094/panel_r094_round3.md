# Panel round 3: the merged plan for the who-is-who slip (accept, or name the smallest change)

0. No GPU, first. The slip pattern goes in `scoring.py` with known-bad and known-good cases; a hit the
   friend's own message contains is skipped. Calibrated once against judge 1 on 17m's Sheet A at seeds
   85-87, the table recorded. Registered now, before any run: probe slip count at most 5 of 96 every seed;
   pooled over the gate and confirmation seeds (82, 83, 88, 89, 90) at most 8 of 480; `hard_dev` at most 3
   a seed; recall not below v6's. Sheet A judged slips reported, not gated. R-076 and R-086 unchanged; v6
   stays valid. [all four]
1. Diagnostic, scoring only: 17m's saved epoch-2 adapters at seeds 87 and 84. [all four]
2. Fix A, one change from 17m: no slip-shaped `older` target. Each one is flipped mechanically ("My X[,] Y"
   and "Y's X" to "Your X Y"; "who is my" to "who is your"), only where the name is the item's own person,
   checked by `item_correct` and the pattern; else the scripted answer. The build must report zero
   slip-shaped targets or it stops. [lanes 1, 3; lane 4 preferred the item's other clean base reply first,
   but the builder keeps one reply an item, so that would mean regenerating, which is lane 1's fix 2]
3. A at seed 87 once, labelled as chosen because it failed, then 82 and 83 against R-086 plus the slip
   gate. Kill rule: slip above 5 of 96 at 87, or R-086 failed at 82 or 83, stops the track. [lanes 3, 4;
   lane 1 had 82, 83 first]
4. If A survives: seeds 88-90 for R-076's rule and the slip gate. [all four]
5. Fix B (lane 2's loss mask on the `older` base-reply rows only) runs only if A fails and the reserve
   allows, never stacked with A. [lanes 1, 3, 4; lane 2 wanted A and B side by side at 87]
6. v6's asked-before stress tests (already queued) run now, because R-088's reserve trigger depends on
   them; v6's other stress tests wait until the fix track is decided. [lane 3 wanted all to wait; lane 4
   wanted all in parallel]
7. Whether a fix that passes may replace v6 is Kevin's ruling, asked before any result. [all four]

Reply in under 120 words: ACCEPT, or ACCEPT IF with the one smallest change and its reason.
