# Panel R-102, round 2: the merged plan (ACCEPT, or ACCEPT IF with the one smallest change)

Round 1: lanes 1, 2, 3 chose B; lane 4 chose C (or A without expecting a ship) and accepts B only if the held-out
form, threshold and guards are hashed and logged before the arm is built, the phone guard holds at all five seeds, and
the held-out correction wordings come from a source other than the builder.

1. **B, as an amendment to R-099 item 6 only, Kevin's decision.** Recorded as R-102: made after the battery, before
   any arm row is built or scored; R-099's item 6 text kept beside it, with the reason (a phone-form gain is not what
   correction rows are built to move, so the arm could never ship). The trigger (item 3), the gap list, every existing
   gate and seeds 91 to 93 are unchanged. If Kevin declines, R-099 stands as written. [lanes 1, 2, 3; lane 4's
   condition]
2. **Held-out correction form, `corrected_heldout`.** Its wordings are written by a fresh agent that sees no repo
   file, no training transform and no result: asked only for the ways people correct an earlier fact when texting a
   friend, as openings ("..., ") and as endings after the restated fact. From its list, the first six it gives that
   are not in `CORRECTION_OPENINGS` become the held-out set. The correction sits in the last out-of-view slot, nearest
   the view; the old value is never named. Code written and its sha256 recorded before anything is scored on it;
   never edited after. The build stops if any training row's correction uses a held-out wording or equals the
   held-out form. [lanes 1, 3 for the form; lane 4 for the source]
3. **Baseline first.** v6 (82, 83) and base scored on `corrected_heldout` on both pools, scoring only, before any arm
   row is built.
4. **The arm, one dose, one try**, on v6's set, about 170 appended rows, scripted targets, every existing row
   byte-identical: about 110 correction rows (the four `CORRECTION_OPENINGS` plus new training openings and endings
   disjoint from the held-out ones; correction positions anywhere out of view except the held-out slot); about 30
   non-correction rows carrying a correction-style opening, so the opening is not a cue; about 30 `asked_before` rows
   (a gap by the registered line; no gain claim, `in_view` guarded). Cue balance and decoy counts per R-099, counts
   reported. [lanes 1, 2; lane 3 would leave asked-before out]
5. **Gain that counts**, pooled over 82 and 83 against v6 at the same seeds on `corrected_heldout`: at least **48 of
   192 on the probe and 32 of 192 on `hard_dev`**, and positive at each seed. At 91 to 93: each seed at least 24 of 96
   (probe) and 16 of 96 (`hard_dev`) above v6's 82-and-83 mean. [lane 3; lane 1 said 32 on both, lane 2 at least 16]
6. **Guards.** Every existing gate unchanged: R-086 at 82 and 83, R-094's slip gate (pooled over 82, 83, 91, 92, 93),
   R-097's stop rule, R-076's rule at 91 to 93. Phone form at all five seeds: pooled over 82 and 83 not below v6 by
   more than 8 of 192 (probe) or 16 (`hard_dev`), and at 91 to 93 each seed within 4 (probe) or 8 (`hard_dev`) of
   v6's 82-and-83 mean; the original item 6 phone-gain result reported beside it. Plain corrections (`corrected`) and
   plain `confirm` reported. [lanes 1, 3, 4]
7. **Clock**: Kevin's ruling and the held-out form tonight; baseline and build overnight; seeds 82 and 83 Saturday
   early; judged sheets; 91 to 93 only if 82 and 83 pass. Not started by Sunday 12:00 = dropped; nothing starts after
   Monday 12:00. [lane 3]
8. **Write-up**: the amendment, its date and reason; that the held-out wordings came from a blind agent and the form
   from the builder after the battery; corrections, phone typing and asked-before reported as measured, with base
   beside them, whatever the arm does. [lane 2]

Reply in under 120 words: ACCEPT, or ACCEPT IF with the one smallest change and its reason.
