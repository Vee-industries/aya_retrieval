# Teaching a 3B model to search a long chat it can no longer see

Track 3, Agentic Fine-tuning, problem statement 4. Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya
Global (3.35B), shown only the last three exchanges of a chat, search the rest when the answer is out of view. On a
sealed test registered before training (300 unseen chats in each of four conditions, made by the
same generator as the training chats, run once), the shipped seed recalls 91 to 107 of
120 facts; the untrained model with the same tool recalls 13 to 32. Every registered
rule of that test passed. On its 419-message chats, which fit the model's 8,192-token window but could not be shown whole under this project's 10 GB memory cap (R-166), seed 82 recalls 52, 52, 46 and 44 of
60 across the four conditions, against 32, 30, 17 and 14 for code that searches every turn (run late,
exploratory).

On chats from outside writers the strongest simple baselines change the reading. When the chat fits, the untrained
model shown the whole chat recalls most (71 and 65 of 120), and code shows no
measured difference from 6.37 (42 and 47 against 39 and
53). On LongMemEval-S, long histories from outside the project, 6.37 shows no measured difference from
code (53 against 40 of 248 (+5.2 points, 95% interval -0.8 to +11.3, p = 0.12); Claude judges with LongMemEval's prompts) and declines 233 of
470 answerable questions.

A scripted demo then showed two faults: 6.37 answered never-told questions with unrelated stored facts and repeated
its own wrong answer while it was in view. I reopened the project. A second sealed test, S3, was written by
six blind writer agents and sealed before any new training row, with its ship rule fixed before it opened.
On S3, 6.37 does worse than the untrained model on both faults: it names its in-view wrong value on 195 of 894 (21.8%)
questions against 11 of 298 (3.7%), and a value listed for the chat on 286 of 708 (40.4%) never-told questions against
14 of 236 (5.9%). Of 24 candidates, the pick, C1, cut these to 5 of 894 (0.6%) and 51 of 708 (7.2%) with no
measured change in recall, and failed one clause: the second had to be no higher than the untrained model's. The
95% interval of that difference (-3.1 to +5.7 points) cannot tell them apart, but a miss is a miss: 6.37 stays
shipped, and C1 is published beside it, labelled. Report arms K1 and K2.1 met every measured S3 line (two seeds,
exploratory). The S3 measures count only values listed for the chat, so invented values pass unseen.

Both sealed tests and their rules were registered before they ran; rules changed after some development readings are
disclosed with their reasons. Every decision and result is in a dated log.
