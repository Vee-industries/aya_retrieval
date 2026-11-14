# Against lane brief: the next lever after C1, 2026-11-14 09:25 ET

You are the against lane of a panel. Argue against the options below: what would make each fail, what simpler thing
explains any gain, and whether either is worth the GPU. One page. First line: your recommendation in one sentence
("run A", "run B changed: ...", "run A then B", or "run neither: ..."). Mark arithmetic on these counts "estimate".
Read only this file and `op4_against.md` in the same folder (the last lane). Run no code. Write your answer to
`c2_against.md` in the same folder:
`C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\b661dc83-6f03-4b4c-a6db-a2f5580bf6a7\scratchpad\lane\`.

## Project in two lines

A LoRA adapter on Tiny Aya Global that searches the user's chat history with a keyword tool (top 5 passages) and
answers with the stored fact, or says it was not told. The pick is K1.3. Kevin (09:20): keep trying today.

## Gates (a try stops at the first it fails), seed 82 first

1. hard_dev (templated questions, 240 replies): never_told at least 44 of 48, false retrieval at most 4.
2. Demo4 (a fresh writer's natural chat): at least 3 of 6 older and 3 of 4 never-told, two blind judges. Read 4 times.
3. Demo5 (held out, same line). Read once (by C1).
4. Seeds 83 and 94 trained by 20:00; whole screening; the pick needs higher pick recall than K1.3 (742).
One seed 82 try to Demo5 takes about 45 minutes; seed 82's gates are due by 14:00 (about 4.5 hours).

## The dose record (seed 82; hard_dev never_told / false retrieval / recall = older + confirm right of 96; Demo older
of 6 / never-told of 4)

| Try | What it is | hard_dev | Demo4 | Demo5 |
|---|---|---|---|---|
| K1.3 | the pick | 46 / 2 / 52 | 1 / 2 | not read |
| C0 | K1.3 + 1 stage (1e-4 x 1) on its own 1,094 rows | 48 / 0 / 54 | 2 / 2 | not read |
| OP | K1.3 + 1 stage on its rows + 36 on-policy corrections (18 answer, 18 decline) | 48 / 1 / 60 | 2 / 3 | not read |
| C1 | OP + the same stage again on OP's set (2 epochs in all) | 46 / 0 / 68 | 3 / 3 | 2 / 3 |
| OP4 | OP + stage with 14 + 14 second-search rows | 33 / 5 | not read | not read |

## C1's misses

- hard_dev older + confirm (96): 68 right with the fact in its own search output; **23 wrong with the fact in its own
  output** (reading errors); 5 wrong with the fact not found. K1.3: 52 / 32 / 12. OP: 60 / 27 / 9.
- Demo4 older misses: questions 1 and 4 declined with the source in its own output (second, behind a passage about
  someone else, as OP); question 3 searched 4 times and ran out of calls.
- Demo5 older misses: questions 1 and 3 wrong with the source in its own output; question 2 ran out of calls; question
  4 declined with the source not found.
So 4 of C1's 7 demo older misses, and 23 of its 28 hard_dev misses, are reading errors.

## Options

**A. C2:** C1 + the same stage a third time on OP's set (1e-4 x 1). No new data, no code. The record shows each
repeat of the stage raised recall and Demo4 older by about one item.

**B. OPT (on-policy on the training templates):** C1 runs the eval on a fresh draw of the *training* pool (the same
templates K1.3 was built from; not hard_dev, probe or any gate pool; about 240 items, about 10 minutes). Rows from
its own turns: an older or confirm item answered wrong with the fact in its own output gets the template's correct
reply after its own query and the real output; a never-told item where it named a value gets a decline. Balanced one
to one with its own correct declines, as OP. One stage from C1 at 1e-4 x 1 on OP's set plus those rows. It needs new
build code (about 40 minutes) and must pass `check_k3.py` 0 FAIL. Risk: the rows share hard_dev's template family, so
a hard_dev gain may not carry to the natural demos.

## Questions

1. Is A a lever or a draw? Is B different from OP in a way that matters, given the error counts above?
2. Which reaches Demo5's older line (3 of 6), and by what route? What does each risk on never_told (C1 already fell
   48 to 46)?
3. Stop rules and controls for each. If one, which first, and what result stops the day?
