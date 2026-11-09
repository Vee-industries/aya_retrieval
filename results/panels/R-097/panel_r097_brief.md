# Panel brief: fix C, built on CuratorKIT's rejections (2026-11-06 ~09:30)

Kevin: "Yes, panel it". The panel comes up with the fix, then a second round agrees one plan.

## Where things stand

- v6 = 17m seed 82 (17b's rows `strict_chat.jsonl`, `--loss-on chat_decision`), passed R-076's rule at seeds
  85-87 (R-093). Its fact answers sometimes pin a relation on the wrong person (the who-is-who slip): probe
  slips 3, 4, 1, 1, 2, 14 at seeds 82-87 (`scoring.slip_shape`, R-094).
- Registered slip gate (R-094): probe slips at most 5 of 96 every seed; pooled over 82, 83, 88, 89, 90 at most
  8 of 480; hard_dev at most 3 a seed; recall not below v6's. Plus R-086's gate at 82 and 83 (counts and judged
  sheets, judge 1 decides) and R-076's rule at fresh seeds 88-90. Kevin's ruling: a fix passing all of that
  replaces v6; no extra recall needed.
- Fix A (fix17w): the 27 slip-shaped `older` answers rewritten to "Your <relation> <name> ...". Slips 2, 1, 0
  at 82, 83, 87 (v6 had 14 at 87); every count passed; failed R-086 by one judged line (probe Sheet B in_view
  33 vs base 34 under judge 1; judges 2 and 3 pass it) (R-095).
- Fix B (a loss mask on the base-reply answers): failed the slip gate at seed 82 (hard_dev 4) (R-095).
- R-096: CuratorKIT's grounding gate over v6's 350 found-fact answers, three Claude judges, rejected when 2 of 3
  reject: 22 rejected, all `older` base replies (of 140). 8 slip-shaped; 14 other faults: who-is-who where the
  question names the person ("Greta's brother adopted a dog named Pepper." for "the dog Greta adopted"),
  claims the passage does not make ("seems to be a source of frustration", "Glastonbury is a famous music
  festival"), off-topic talk ("Funny how the snow keeps coming up ..."). 19 slip-shaped answers pass it (voice,
  not facts: "My roommate, Omar, writes ..."). 26 of fix A's 27 rewrites pass; one keeps "and is having a great
  time!".
- The builder keeps one base reply per item; a scripted answer ("Your {relation} {person} ...") exists for any
  row via the train templates, but scripted answers alone once cost coherence (fix 5b, R-033); 60 of 200
  `older` targets and all 150 `confirm` targets are scripted already.
- Compute: about 65 min a candidate-seed; R-088's reserve has room; freeze Tuesday Nov 10 (today is Friday).
  Judging: screens get one judge, confirmations three (Kevin's usage).

## Files the lanes may read

RECORDS.md sections R-086, R-088, R-093, R-094, R-095, R-096; `results/curator/R-096/rejected.json`;
`scripts/records/splice_r094.py`; `scripts/run_curator_check.py`; `scripts/run_build_training_set.py`;
`src/aya_retrieval/scoring.py`; `data/screens/strict_chat.jsonl`.
