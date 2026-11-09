# Panel round 2: one agreed plan (2026-11-05 12:00)

Kevin: "once the fixes are proposed you'll run them to the panel again as a 2nd iteration and force
consensus on a plan". Round 1's four lanes proposed the fixes below. In this round, every lane reads all
of them and the panel must end with ONE plan all four lanes accept.

## Correction to the round-1 brief

Training normally takes about 30 min (1,632 to 2,077 s for 800 to 900 rows at 1.3 s a step). The 85 min
figure came from 17b's run (4,475 s), which slowed when part of its GPU memory was moved to system memory.
19a's first run did the same at step 884 and was restarted. So one candidate-seed (train plus four
scorings) is about 65 min: about 90 candidate-seeds to Tuesday if the card stays fast. A scoring-only
candidate (no training) is about 35 min.

## Round-1 proposals, in short (full text in each lane's report)

**Lane 1 (plain chat), ranked:**
1. Scale 17b's LoRA at inference (0.85, 0.7) at seeds 82, 83; scoring only.
2. Distinct chat targets each epoch: R-078 has 383 accepted targets; search rows repeated three times,
   about 127 different chat rows per epoch, same chat share; seeds 82, 83, then 84.
3. Replace, don't add: swap 25 to 40 of 17b's 150 plain targets for vetted fact-word lines, one a type;
   800 rows; seeds 82, 83.
4. Loss on only the first 3 to 4 reply tokens and the end marker of chat rows; new mask; seeds 82 to 84.
5. Save the epoch-2 checkpoint of every run and score it where epoch 3 misses a gate item.

**Lane 2 (recall), ranked:**
1. Interpolate 17b and 18a adapters at seed 82 (a = 0.3, 0.5, 0.7), merged deltas; scoring only.
2. Repair the answer after the find: sample 17b on ~250 train indirect `older` rows, keep replies with the
   value, no decline, under 40% copied from the message; replace ~60 `older`/`confirm` targets; seeds 82, 83.
3. Stitched asked-before rows by splicing existing `never_told` question-and-decline exchanges before
   `in_view`, `statement` and `never_told` rows (~15 each, replacing rows); checked with the stress test's
   own function as the different check; seeds 82, 83.
4. Same-conversation pairs at 2:1 with forget phrases built from parts, plus forget-word chat lines; check
   on 48 fresh indirect questions and 48 fresh chat lines written blind.
5. Epoch-2 checkpoints, as lane 1's 5.

**Lane 3 (portfolio and selection):**
- Keep 19a 82, 83; fix20 82, 83; fix20k2 and k3 at 82 only; 19b 82 only; seed 84 for gate passes.
- 17b settings sweep at 82, 83: lr 1e-4, 2 epochs, rank 16 alpha 32; plus 17b's lora_B scaled by 0.75
  (scoring only) at 82, 83, 84.
- Fix 17c: re-vet 17b's chat targets on a who-is-who and tone rubric (no GPU), 2 seeds.
- 17b at fresh seeds 85, 86 to see how often the one-line failure happens.
- Hold ~12 for a second round chosen Saturday night; stress tests on the finalist only.
- Selection: screen at 82, 83; confirm survivors at fresh seeds (85+) under R-076's rule; ship the recipe
  with the fewest changes from 17b unless another's pooled hard_dev recall is higher by more than 15;
  ship seed 82 of it, fixed in advance; append-only candidates list in RECORDS.md; the write-up states
  how many recipes and candidate-seeds were scored on the development pools.
- Proposed a judge tolerance (an item met at base minus 1 per seed and at base pooled) and said itself that
  it was chosen after seeing 17b fail by one line.

**Lane 4 (against the current course):**
- Item 1g and the check-set gate are near coin flips (judge spread one to two lines); chasing them with
  added rows pays in recall. The dose ladder cannot resolve doses at two seeds.
- The cause is the chat targets being copied (loss on demonstrated turns), not the row count.
- Keep 19a 82, 83 and fix20 82, 83; cancel fix20k2, k3 and 19b.
- "17m": 17b's data, but chat rows get loss only on the no-search decision (first assistant token and
  end marker), so chat replies stay base's own; seeds 82 to 84, then 85 to 87.
- Gentler optimisation on 17b's data: 2 epochs, lr 2e-4, seeds 82 to 84.
- 17b at seeds 85 to 87 to estimate how often item 1g fails.
- Stress tests kept.

## Where they already agree

- 17b is the front-runner; more added chat rows cost recall.
- Scoring-only dials on 17b (scaling, interpolation) are cheap and worth trying.
- A lighter pull on chat targets (partial loss, fewer epochs, lower lr, or epoch-2 checkpoints).
- 17b at fresh seeds, to measure how often the rule's one-line failure happens.
- Report the number of candidates tried on the development pools.

## Where they differ

- The dose ladder and 19b: keep (lanes 1 and 3 partly) or cancel (lane 4).
- Whether to change the judged items' tolerance (lane 3) or keep R-076's rule as written.
- Which new data fixes are worth a slot (replace-don't-add, distinct targets per epoch, answer repair,
  stitched asked-before rows, pairs).
- Order and the size of the reserve.
