# Panel brief: how to spend the compute left before the freeze (2026-11-05 12:00)

## The compute, as it is

- One 10 GB GPU, one job at a time; it is shared with Kevin's games and video, which can slow it.
- Training one candidate at one seed: about 85 min (900 rows, 3 epochs). Scoring it: about 35 min
  (probe 51203 screen, hard_dev 73157, probe 73157, chat check set; about 9 min each).
- So one candidate-seed is about 2 h. From now (Thu Nov 5, noon) to the freeze (Tue Nov 10) is about 100
  GPU hours: roughly 45 to 50 candidate-seeds if the card is free. Stress tests are about 9 min each.
- Judging (coherence sheets) runs on fresh judge agents in parallel and costs no GPU. Builds of new
  training rows take minutes.
- After the freeze: one sealed final run (held-out and independent pools), on Kevin's go.

The earlier panel (R-087) was told "about four screens left"; that was wrong by about ten times.

## The models and the rule

- v5 is current. 17b: hard_dev recall 72 / 73 / 83 at seeds 82 / 83 / 84 (v5 58 / ? / ?, pooled 172 of
  288 vs 17b 228), but failed R-076's three-seed rule by one judged plain-chat line at seed 83.
- On the 48-line blind chat check set, v5 is 36 against base 44; 17b 44 against 45.
- 18a (17b + 57 fact-word chat lines) and 18c (17b + 57 plain lines) fixed the check set (48, 47) but
  cut hard_dev recall to 56 and 66 at seed 82.

## The plan now in the queue (queue 64), all unconditional

1. 19a (18a + 57 indirect older questions of the same types) at seeds 82, 83 (82 training now).
2. Fix 20 dose ladder on 17b: 1, 2, 3 vetted fact chat lines a type over all 25 types (25, 48, 64
   lines), each type matched by as many indirect older questions; seeds 82, 83 each.
3. 19b (18c + the 57 questions) at seeds 82, 83.
4. Seed 84 for every candidate that passes the unjudged items of R-086's gate (`gate_r086.py`).
5. Remaining stress tests (12 runs).

That is about 12 to 17 candidate-seeds, about a day. Not yet planned: the asked-before failure (R-084,
plan_fix20.md, with the guards the last panel asked for: statement and never_told rows, a control, an
out-of-template check); more seeds per candidate; anything else.
