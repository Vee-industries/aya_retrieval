# Panel R-099, round 2: the merged plan (ACCEPT, or ACCEPT IF with the one smallest change)

New evidence since round 1 (v6 = 17m seed 82, already scored; paired: same adapter, same items, plain vs messy):
earlier question in view (`--asked-before`): probe recall 96 vs 96, `statement` 48 vs 48; `hard_dev` recall 74 vs 67,
`in_view` 37 vs 36, `never_told` 48 vs 47. v6's typing style, corrections and 1,000-message results are not run yet.

1. **Measure first, train only on a registered gap** [lanes 3, 4]. Scoring only, no training: v6 at seeds 82 and 83
   (and C2 at the same seeds if C2 passes its counts) on the R-067 battery: typing style on probe and `hard_dev`,
   every kind; corrections on probe and `hard_dev`, `older` and `confirm`; earlier question in view at 83 (82 done).
   1,000-message chats cut [lanes 1, 3]. Queued after C2's seed 83. About 2 h of GPU.
2. **Trigger, registered now.** A messy form counts as a gap only if, paired over seeds 82 and 83 on one pool, it costs
   at least **8 of 192** recall answers, or at least 4 of 96 on `statement`, `never_told` or `in_view`, against the
   same adapter on plain items. [lane 3 said more than 3 of 96 per item; lane 4 said 10; paired comparisons carry no
   training-seed noise, R-091's spread is between training seeds.] No gap: no messy training; the battery's numbers
   go in the write-up as a finding ("tested, no headroom"), base beside them.
3. **If a gap: one messy arm, one dose, one try** [lanes 1, 2, 3]. Appended rows only, about 150, built by script from
   fresh TRAIN items with new seeds through `stress.py`'s transforms, only for the forms that showed a gap. The
   friend's messages change; every target is the scripted answer; every existing row byte-identical; no `in_view`
   answers rewritten. No writer agents; the build's inputs are TRAIN and `stress.py` only, never the sealed pools or
   their brief. Cue balance per lane 1 (a question in view on found rows too; correction openings on non-correction
   rows; style across all five kinds; decoy counts as R-020), counts reported.
4. **A held-out messy form is the arm's primary measure** [lane 1]: written now, before any run, in `stress.py`, and
   kept out of training (for example a correction opened by words `corrected` never uses, or a typing transform
   `typed` never applies: dropped apostrophes, run-together words). The transformed dev tests are secondary.
5. **Order and seeds.** C2's gate goes first and is never delayed. The messy arm sits on the shipping candidate's set
   (C2's if C2 passes, else v6's). Seeds 82 and 83 with R-086's gate and R-094's slip gate word for word, the R-097
   stop rule; then fresh seeds **91 to 93** for R-076's rule (88 to 90 stay C2's) [lane 3].
6. **Replacement** [lane 3 against lane 4]: the arm replaces the shipping candidate only if it passes every existing
   gate at 82, 83 and 91 to 93 **and** gains on the held-out messy form by at least 8 of 192 pooled at 82 and 83.
   Otherwise it is reported as a development finding. Nothing starts after Monday 12:00; cut order (b), (c) of lane 3.
7. **Disclose** [lane 2]: messy rows made by script from TRAIN and `stress.py`; the transforms are also dev tests; the
   sealed result is still template-built; no claim of real-chat robustness; every candidate-seed counted.

Reply in under 120 words: ACCEPT, or ACCEPT IF with the one smallest change and its reason.
