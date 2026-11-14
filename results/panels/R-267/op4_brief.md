# Against lane brief: OP4 (on-policy second-search rows), 2026-11-14 08:05 ET

You are the against lane of a panel. Argue against the lever below: what would make it fail, what simpler thing would
explain any gain, and whether it is worth the GPU at all. One page. First line: your recommendation in one sentence
("run as written", "run changed: ...", or "do not run: ..."). Mark anything that is arithmetic on these counts, not a
measurement, as "estimate".

Read only these files (all in `C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House\b661dc83-6f03-4b4c-a6db-a2f5580bf6a7\scratchpad\lane\`):
`op4_brief.md` (this), `records_extract.md` (records R-253, R-257, R-261 to R-265), `op3_against.md` (the last
against lane, R-263), `reach2.py` (the script that made count 3 below). Run no code. Write your answer to
`op4_against.md` in the same folder.

## Project in two lines

A LoRA adapter on Tiny Aya Global (a small open model) that searches the user's own chat history with a keyword tool
(SQLite FTS, OR search, top 5 passages) and answers with the stored fact, or says it was not told. The shippable pick
is K1.3. Kevin's order: keep trying until a candidate beats K1.3 on every gate and on pick recall.

## Gates, in order (a try stops at the first it fails)

1. Seed 82 hard_dev: never_told at least 44, false retrieval at most the reference's + 3 (K1.3: 46 / 2; OP: 48 / 1).
2. Demo4 (a fresh writer's chat, 6 older questions, 4 never-told with search): at least 3 of 6 older and 3 of 4
   never-told, two blind judges. K1.3 1 of 6 / 2 of 4; C0 2 / 2; OP 2 / 3.
3. Demo5 (held out, same line), then seeds 83 and 94 trained and the whole screening, then the pick rule.
Deadline: seed 82's gates by 14:00 today (about 6 hours from now). One seed 82 try takes about 1 hour on the card.

## Facts (counts from the files)

1. OP (K1.3 plus one stage of 36 on-policy corrections; R-261) failed only Demo4's older line, 2 of 6. Its four older
   misses: two declines after search where the source was second in its own search output, behind a passage about
   someone else; one search with no result (it searched "instrument", the chat said "ukulele"); one reply that was
   only a search call (no answer).
2. OP seed 82 on its 375 training-chat items (R-265), older questions, tool loop: about the user 128 (11 right, 117
   wrong); about someone else 122 (57 right, 65 wrong). Of the 117 wrong about the user, **9 had the fact in OP's own
   search output and 106 did not** (2 more made no search). Of the 65 wrong about others, 49 had it in the output.
   So OP's errors about the user are almost all search misses; its errors about others are mostly reading errors.
3. **New count (08:00, `reach2.py`, CPU only).** Each item carries the writer's `second_query` (other words for the
   same fact, for example "pet kitty" for "what breed is the cat"). Over the 106 + 2 user misses where OP's search did
   not find the fact: the second_query's real search returns the source for **76** (69 of them after a first search,
   cut to R-205's rule, that returned text; 7 after one that returned nothing); 32 not reached. Over 16 such misses
   about others: 12 reached. No second_query holds a value word.
4. The earlier written-ahead version of this idea: K4.9 = K4.8 plus 27 miss-then-hit rows (writer-written miss query,
   then the question's query finds the source), first call kept out of the loss (R-223, R-224). R2d (K4.9's set,
   1e-4 x 1 from K1.3) failed hard_dev: never_told 42, false retrieval 6 (R-248). It never reached a Demo. A lane on
   2026-11-13 (R-226) judged no candidate after K4.9 likely to pass.
5. The on-policy rounds so far: OP's round 1 kept 18 answer rows (user-fact share rule: user facts at least a third
   of answer rows; one-to-one answer to decline balance). Round 2 (OP3) built 41 answer rows, all about others, so 0
   kept and it stopped by its rule (R-265). About 260 older questions in the training chats are unused by the items.
6. Rules that bind any set: `check_k3.py` 0 FAIL (R-205's lines: first query uses only the question's words, at most
   4, no filler; a second query holds no value word; user-fact share; check_false share 15%; one-to-one balance); the
   item chats share no answer run with any gate set (checked, 0).

## The lever proposed (OP4)

From OP's seed adapter, one stage at 1e-4 x 1 (as OP and OP3). Answer rows from OP's own user-fact search misses:
first call = OP's own query cut to the rule, with its real output (no source); second call = the item's second_query,
with its real output (holds the source); reply = the writer's value reply; the first call kept out of the loss
(R-223's mask). Decline rows to balance one to one: OP's own trap items (never-told questions whose wrong value is in
the chat), the same two searches, then a decline. Rehearsal: OP's whole seed set. Stop rule (registered before any
result): fewer than 10 answer rows after every cut means no training. Same gates as above.

## Questions

1. Is this a different lever from K4.9/R2d, or the same one with more rows? Does fact 2 change the case?
2. Does it reach any of OP's four Demo4 misses (fact 1)? Which, and how?
3. What does it risk on hard_dev false retrieval and never_told, given R2d's 42 / 6?
4. Balance: is OP's trap pool large enough for one-to-one, and is "two searches then decline" the right decline row?
5. What control is needed, and what stop rule or change would you require? Or is no lever worth the card, in which
   case the next step is to report K1.3 as the pick to Kevin?
