# Teaching a 3B model to search a long chat it can no longer see

Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya Global (3.35B), shown only the last three
exchanges of a chat, search the rest when the answer is out of view. On a sealed test registered before training
(300 unseen generated chats in each of four conditions, run once), the shipped seed recalls
91 to 107 of 120 facts; the untrained model with the same tool recalls
13 to 32. On the first sealed test, every registered rule passed: every right answer came from a search that found the fact,
no adapter made more false retrievals than the untrained model, and three judges rated every adapter coherent more
often.

The strongest simple baselines change the reading. On chats from outside writers (Claude Opus agents, about
1,400 tokens), the untrained model shown the whole chat recalls most (71 and
65 of 120), and code that searches every turn recalls as well as 6.37 (42 and
47 against 39 and 53) and runs faster. Training's measured gain there
is when to search: 6.37 leaves answers already in view alone (35 and 37 of
40 right), where code searches every turn (13 and 16).

A scripted demo then showed two faults: 6.37 answered never-told questions with unrelated stored facts and repeated
its own wrong answer while it was in view. With the deadline extended, the project was reopened. A second sealed
test, S3, was written by six blind writer agents and sealed before any new training row, with its ship
rule fixed before it opened. 24 candidates were listed for screening on development sets, six read on every line; the pick, C1,
cut copies of a wrong answer in view from 195 of 894 (21.8%) to 5 of 894 (0.6%), and false answers to never-told
questions whose search returned text from 286 of 708 (40.4%) to 51 of 708 (7.2%). It failed one clause: those false
answers had to be no higher than the untrained model's 14 of 236 (5.9%). By the registered rule, 6.37 stays shipped.
On S3 the whole chat (274 of 414 (66.2%)) and code (161 of 414 (38.9%)) again recall more than either trained model.

On LongMemEval-S (500 questions, histories far longer than the context), judged by Claude judges with
LongMemEval's prompts, not the official GPT-4o judge, 6.37 is right on 53 of 248 judged
questions against 34 for the untrained model with the tool, but declines 233 of
470 answerable questions. Every test was registered before it ran; every decision and result is in
a dated log.
