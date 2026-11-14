# Against lane: a stage on the model's own mistakes

Read only this file. Answer in under one page, written to the file named at the end. Plain words, no metaphors.

## Setting

A LoRA adapter on Tiny Aya Global searches older chat history with a fixed keyword tool and must name the stored
fact when told and say "not told" when not. Gates on seed 82: hard_dev (never_told at least 44 of 48, built with a
same-type fact about another person; false retrieval at most 4), Demo2 (read 21 times), Demo3 (read twice), then full
screening on seeds 82 and 83 and pick recall over 82, 83, 94 against the pick K1.3 (742). A try must clear seed 82 by
Saturday 14:00 ET (now 04:55); every seed trained by 20:00.

Every try so far trained on rows written ahead of time (writer chats with writer queries, or scripted templates).
Results sit on one trade: tries that name a third Demo2 older item reach or pass false retrieval 4 on hard_dev, and
gate passes sit inside the gates' own variation (a 10-row edit moved hard_dev by 4). K1.3 itself: hard_dev 46 / 2 /
recall 52, Demo2 older 0 of 6 (it declines facts its own search found). The owner asked for a different approach.

## The proposal: on-policy corrections

For each seed s (82, 83, 94), separately:
1. Run K1.3's seed-s adapter through the fixed eval harness on a fixed sample of the **training** chats (never a
   screening set): per chat, 2 older questions and 1 trap question (the writers' near-miss or wrong-person questions,
   whose chat holds another person's or category's fact as the wrong value). About 380 items, about 25 minutes.
2. For each item the model got wrong, build one row from its own turns: its own search queries, the tool's real
   outputs for them, then the right reply: the writer's value reply where its search returned the source message and
   it declined or answered wrong; a decline where it named the trap's wrong value. Items it got right, and older items
   whose fact its searches never returned, make no row.
3. Stage K1.3's seed-s adapter, 1e-4 x 1 epoch, on these correction rows plus K1.3's own 1,094 rows (rehearsal).
4. Gates as usual (hard_dev first). The correction rows go through the set checker's applicable lines.

## Questions

1. Is this a different approach in the sense that matters (it changes what the trade is made of), or another draw?
   Strongest reason for, strongest against.
2. What will it most likely do to Demo older and to hard_dev false retrieval? Prediction for seed 82.
3. Leakage or circularity: anything here that tunes to a screening set, or makes a gate meaningless? Anything that must
   change before it runs (row balance, rehearsal, the sample, the base)?
4. Is K1.3 the right base, or T6 (hard_dev 44 / 4 / recall 72, Demo2 2 of 6; only seed 82 exists, 80 minutes a seed)?

## Output

Write to `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\77d169a0-08a5-413f-bd51-6c88c27447de\scratchpad\k48\onpolicy_against.md`:
a recommendation line first, then the four answers. Reply with the recommendation line only.
