# Against lane brief: OPO (OPT trained from OP), 2026-11-14 10:04 ET

You argue against the lever below. One question: should the card run OPO, as written, changed, or not at all?
Answer in one page, first line a recommendation. Mark anything you work out from the counts as "estimate" and
anything you did not check as "not checked". Plain words, no metaphors.

## Goal and gates

A LoRA on Tiny Aya Global answers from a keyword search over its own chat history, or declines. The pick is K1.3.
A try must beat it on every gate, in order, on seed 82: hard_dev never_told at least 44 of 48 and false retrieval at
most 4; Demo4 (a natural chat, 6 older questions, 4 never-told) at least 3 of 6 older and 3 of 4 never-told; Demo5
(held out) the same; then seeds 83 and 94 trained by 20:00 and the whole screening. Seed 82 must clear by 14:00 ET.

## What failed today (do not repeat)

- More identical stages: OP (K1.3 plus one stage at 1e-4 x 1 on OP's set: K1.3's 1,094 template rows plus 36
  on-policy corrections and 7 check_false rows from its natural training chats), then C1 (OP plus the same stage again),
  then C2 (C1 plus the same stage a third time). hard_dev never_told / false retrieval / recall of 96:
  OP 48 / 1 / 60, C1 46 / 0 / 68, C2 43 / 2 / 66 (fails). K1.3 46 / 2 / 52.
- OP4: second-search rows. never_told 33; it learned to keep searching and ran out of calls.
- OP2, OP3: on-policy rounds on the natural training chats; nothing left to correct (the models already get those
  chats right, or their errors there are search misses about other people).

## The closest so far: C1

hard_dev 46 / 0 / 68. Demo4 3 of 6 older, 3 of 4 never-told (pass, at the line). Demo5 (first read) 2 of 6 older,
3 of 4 never-told (bomb). hard_dev older and confirm, right with the fact in its own search output / wrong with it there
(a reading error) / wrong with it not found: K1.3 52 / 32 / 12; OP 60 / 27 / 9; C1 68 / 23 / 5; C2 66 / 24 / 6.
C1's demo older misses: 4 of 7 are reading errors (Demo4 Q1 and Q4: declines with the source second in its output,
behind a passage about someone else; Demo5 Q1 and Q3: wrong replies with the source in its output), 2 ran out of
calls, 1 not found.

## The lever: OPO (OP start, OPT rows, C1's dose)

OPT (`scripts/records/build_onpolicy_template.py`, written for R-271, never run) builds rows from a model's own turns
on a fresh draw of the training template pool (`--pool train --seed 271071 --items-per-kind 24 --kinds older confirm
never_told`, so 72 items; no earlier row uses that seed): an older or confirm item answered wrong with the fact in its
own output gets the template's reply after its own unchanged queries and their real outputs, kept only if the answer
value is in the last output; a never_told item where it named a value gets a decline; balanced one to one with its own
correct declines; check_false filled as OP. R-271 put it on C1 plus a further stage (C2's dose), and C2's dose failed.

OPO changes only the start: **OP's seed adapter** runs the 72-item eval, the rows come from OP's own turns, and the
stage runs **from OP** at 1e-4 x 1 on OP's set plus the rows. So OPO's total training is exactly C1's (OP plus one more
stage on OP's set) plus the new rows, and **C1 is its exact control, already measured** on seed 82. Stop rule
proposed: fewer than 10 answer rows means no training. `check_k3.py` 0 FAIL before training. Cost: eval about 5 to 10
minutes, stage about 22, hard_dev about 10, each Demo about 6. Seeds 83 and 94: OP's start adapters trained as OP was
(the queue does this), then the same eval and build per seed.

## Points to weigh

1. With 48 older and confirm items, at OP's hard_dev reading-error rate (27 of 96), the answer side is about 13 rows
   (estimate); the template pool was trained on, so it may be lower. Is 10 the right floor, and is so small a dose
   worth the card?
2. Every new row presses toward answering. C1 already lost 2 never_told items from OP (48 to 46). Does adding reading
   rows to C1's dose put never_told under 44? What would you check in the build output before training?
3. The rows are template chats; the demo misses are natural chats with a passage about someone else ranked above the
   source. Count rows with the source not first (the build logs `source_not_first`). Does the lever reach the demo
   misses at all?
4. Demo5 has been read once (C1). Any Demo5 reading here is its second, chosen with the first known.
5. The simplest alternative is to stop and report K1.3 as the pick. Say plainly if that is the better call.

Files you may read: this brief, `results/panels/R-271/c2_against.md`, `scripts/records/build_onpolicy_template.py`,
`RECORDS.md` lines 9762 to 10001. Do not open `src/aya_retrieval/pools.py`, anything under `data/heldout*`,
`results/longmemeval/`, or `data/demo5/`. Run no code. Write your answer to the file path you are given and nothing else.
