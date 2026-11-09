# Panel brief: is there a 6.4, and if so what is it

You are one lane of a three-lane panel. You read; you write nothing to disk and run nothing that changes a file. Your
answer is your final message.

## Hard limits (break one and your answer is void)

- Never open `src/aya_retrieval/pool_independent.py`, anything under `docs/independent_pool/`, or line 452 onward of
  `src/aya_retrieval/pools.py` (sealed held-out material). Never open any file whose name contains "token".
- Training rows may come only from the TRAIN pool (`pools.py` lines 1 to 451). Never from probe, `hard_dev`, the
  independent set (`data/blind_dev/`) or the break-test results. `phone_style` never enters training.
- A candidate trains from scratch (never on top of an earlier adapter), at seeds 82 and 83, with 6.37's recipe unless
  the design says otherwise, and must start training before 12:00 today (it is about 08:20 now). Building the rows
  must take under an hour, CPU only, no new model calls unless they are cheap and scripted.
- It must pass every gate 6.37 passed, unchanged (`scripts/records/gate_r086.py`, `stone_report.py`, and R-134's lines:
  probe and `hard_dev` recall pooled at 82 and 83 not below 6.37's 192 and 163, probe `in_view` at least 41 each seed,
  R-102's stress runs, R-086's judged sheets), and then beat 6.37 on `hard_dev` recall at fresh seed 75002 over
  `plain` and `long` chats, seeds 82 and 83 pooled (ties fail). Any fail and 6.37 ships.

## Repo

`C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`. Read `RECORDS.md` from R-138 to R-149 (the last
day), and as needed R-110, R-113, R-115, R-117 to R-128 (how the 6.3x copies were built and why they failed). 6.37's
set is `data/screens/fix17cs37.jsonl` (1,094 rows); the builders are in `scripts/records/` (`build_r110.py`,
`build_r134.py` are good examples).

## The facts

- 6.37 (fix17cs37 seed 82) is frozen and passes everything. On `hard_dev` (seed 73157) recall is 73 and 90 of 96 at
  seeds 82 and 83.
- Its commonest `hard_dev` miss (R-144, R-146, R-148): it searches, finds the right line, and answers from the
  line's first clause, leaving out the asked detail when it sits later in a long line. Example: the line is "Rhys is
  my coach, remember, and they finally hosted dinner last night after ages of promising, ... the dish everyone fought
  over seconds of was the minestrone"; 6.37 answers "Your coach Rhys hosted a big dinner." It is concentrated in two
  `hard_dev` templates ("collected the keys ... had the corner by the window ready for the parrots" and "hosted dinner
  ... the dish was the chowder"). The TRAIN pool's fact lines are all one short clause.
- 6.37's recall training answers almost all read "Your {relation} {person} {verb phrase} {value}." (a restatement of
  the line from its start).
- R-110's 100 rows (a found line that says more: two facts about the person, or small talk joined around the fact)
  were tried three times (6.21 on top of 6.2; 6.39 from scratch inside 6.37's set). Each time `hard_dev` recall fell
  and the found-but-incomplete miss rose (6.39 at seed 83: 3 to 15). They are not to be used again.
- R-121: scripted in-view answers cost found-fact detail (both copies with them failed).
- R-127: a copy with no defect misses one probe question in 192 about 28% of the time; four of the last nine copies
  failed by exactly one probe question.
- On chats written by independent writers (R-146) other failures matter more (tag questions do not trigger a search;
  queries reuse training wording; pronoun facts are missed), but that set is report only: nothing may be designed
  from it.

## The question

Should there be a 6.4 before the freeze, and if so, exactly what? Give one design or say "no 6.4", with your reasons.
A design names: which rows change or are added (from the TRAIN pool only), how they are built (by script, from what),
how many, what the target answer reads like, and why it should lower the found-but-incomplete miss without costing
probe recall or `in_view`. Say what result would show it failed, and the single biggest risk.

## Your lane

SOURCES. Check the record. Read the RECORDS.md entries named in the brief and the relevant builders and data (6.37's set, R-110's rows, the 6.3x builds), and report what the evidence says about what has and has not moved the found-but-incomplete miss and hard_dev recall, with record numbers. Then say which kind of design the evidence supports, if any, and which it rules out.
