# Panel round 3: the merged plan, for acceptance (2026-11-05)

Built from the four round-2 replies. Each item says who backed it. Accept the whole plan, or name the
smallest change you need and why; the panel ends when all four accept.

## Rules (all four lanes agreed)

- R-076's rule stands as written; no tolerance change. Three judges a sheet are reported, with the spread,
  as information. Any change of rule is Kevin's call, made before results.
- Ship rule: among recipes that pass the rule at three seeds never used to screen them, ship the one with
  the fewest changes from 17b, unless another's pooled hard_dev recall is higher by more than 15. The seed
  shipped is named in the candidates list before its confirmation.
- An append-only candidates list in RECORDS.md, stamped before each run, killed and failed runs included;
  the write-up gives the number of recipes and candidate-seeds scored on the probe, hard_dev and the
  check set, all development evidence.
- Every new training run saves its epoch-2 checkpoint (flag, off by default, committed first).
- Scaled or mixed adapters are dials or diagnostics; any shipped model is a trained adapter under the rule.

## Queue, in order (cs = candidate-seed, about 65 min; scoring-only = 0.5)

1. 19a at 82, 83 (training now). 2 cs. [all]
2. Scoring-only dials on 17b: LoRA scaled 0.85 and 0.7 at 82, 83 (4 runs); 17b/18a mixed at a = 0.3, 0.5,
   0.7 at seed 82 (3 runs), built as a rank-64 adapter (A1 and A2 stacked, B1 scaled by a and B2 by 1 - a:
   the exact blend of the full deltas). 3.5 cs. [all; mixed as diagnostic only, lanes 1, 4]
3. 17b at fresh seeds 85, 86, 87: how often item 1g fails. 3 cs. [all]
4. Fix 20 (k1) at 82, 83. 2 cs. [all] Fix 20 k2, k3 and 19b cancelled. [all]
5. 17m: chat rows get loss only on the no-search decision and the end marker (lane 1's first-tokens mask is
   the fallback variant) at 82, 83, 84. 3 cs. [lanes 1, 2, 3; lane 4 asked 82, 83]
6. Gentler, one variable at a time on 17b's data: 2 epochs at 3e-4, at 82, 83; then 2 epochs at 2e-4 at
   82, 83. lr 1e-4 is dropped (R-079, R-080: it failed before). 4 cs. [merged: lane 1 wanted 2e-4 with
   2 epochs and no 1e-4; lane 3 wanted one variable each; lanes 2, 4 offered both]
7. Distinct chat targets per epoch at 82, 83. 2 cs. [all; lane 2: two seeds only unless it passes]
8. Replace-don't-add (fact-word lines in place of 25 to 40 of 17b's chat targets) at 82, 83. 2 cs. [all]
9. Answer repair (lane 2's on-policy found-fact targets, replacing about 60 rows) at 82, 83. 2 cs.
   [lanes 2, 3, 4; lane 1 wanted it only if recall stays the weak point]
10. 17c: 17b's chat targets re-vetted on a who-is-who and tone rubric (no GPU to vet) at 82, 83. 2 cs.
    [lanes 1, 2, 3; lane 4 did not address it]
11. Seed 84 for each candidate passing gate_r086.py, up to 8 cs.
12. Confirmation: up to two finalists at three fresh seeds each, under R-076 as written. 6 cs.
13. Stress tests on the finalist only. 2 to 3 cs.
14. Reserve, committed Saturday night from the results: about 25 cs, plus about 10 cs buffer for the card
    slowing. Stitched asked-before rows, same-conversation pairs and a second dose come from it if
    the results call for them. [lanes 1, 3, 4; lane 2 conceded]

Committed about 45 cs, reserve and buffer about 35, total about 80 of 90.

## Points to settle in this round

- Item 6 as merged (2 epochs at 3e-4, then at 2e-4; no 1e-4).
- Item 9 run now, not conditional.
- Item 10, for lane 4.
- Item 5 at three seeds, for lane 4.
