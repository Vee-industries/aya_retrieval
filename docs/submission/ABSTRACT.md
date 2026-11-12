# Teaching a 3B model to search a long chat it can no longer see

Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya Global (3.35B), shown only the last three
exchanges of a chat, search the rest when the answer is out of view. On the sealed test (300 unseen generated chats
in each of four conditions, run once), the shipped seed recalls 91 to 107 of 120 facts; the untrained model with the
same tool recalls 13 to 32. On chats from outside writers (written by Claude Opus agents, about 1,400 tokens), the
untrained model shown the whole chat does best (71 and 65 of 120), and code that searches every turn recalls as well
as 6.37 (42 and 47 against 39 and 53) and runs faster. There, training's measured gain is when to search: 6.37
searches for facts out of view, which the untrained model rarely does, and leaves answers already in view alone (35
and 37 of 40 right), where code searches every turn (13 and 16).

Targets in the 1,094 generated training rows are the untrained model's own replies where they pass the scorer.
CuratorKIT's grounding gate audited an ancestor set (v6's 350 found-fact answers, 22 rejected); AuditKIT was a
second scorer in development, not run on 6.37. Each test was registered before it ran; every decision and result is
in a dated log.

On the sealed test every registered rule passed: every right answer came from a search that found the fact, no
adapter made more false retrievals than the untrained model, and three judges rated every adapter coherent more
often than the untrained model. Afterwards, on the same chats, code recalls 14 to 32 of 60 against the shipped
seed's 44 to 55 at both lengths; the untrained model reading the whole 58-message chat recalls 21 to 33 against its
46 to 55.

On the outside-writer chats 6.37 declines facts never told on 37 and 36 of 40, against code's 31 and 24, and leaves
plain statements unsearched on 37 and 35, below the untrained model's 38 and 39. On the first set the shipped seed
is the lowest of eight seeds, and its gain has p = 0.047, above the registered 0.01; it corrects 1 and 3 of 20 false
"..., right?" claims; the coherence judges were never checked against a person.

Only LongMemEval-S (500 questions, histories of about 115,000 tokens) is long. Judged with LongMemEval's prompts by
Claude judges, not the official GPT-4o judge, on the 233 answerable of 248 judged questions, 6.37 and code are right
on 40 and the untrained model with the tool on 32 (p = 0.29). Over all 248, 6.37 is right on 53 against 34 (p =
0.014) and code's 40 (p = 0.12). 6.37 declines 21 of all 30 unanswerable questions, and 233 of all 470 answerable
ones, where code declines 1. Code is faster than 6.37 on every set.
