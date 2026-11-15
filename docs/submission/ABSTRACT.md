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
53). On LongMemEval-S, histories past the window, 6.37 and code show no measured difference
(53 and 40 of a stratified 248; Claude judges); 6.37 declines 233
of 470 answerable questions.

A scripted demo then showed two faults: 6.37 answered never-told questions with unrelated stored facts and repeated
its own wrong answer while it was in view. I reopened the project. A second sealed test, S3, was written by
six blind writer agents and sealed before any new training row, with its ship rule fixed before it opened.
On S3, 6.37 does worse than the untrained model on both faults: it names its in-view wrong value on 195 of 894 (21.8%)
questions against 11 of 298 (3.7%), and a listed value on 286 of 708 (40.4%) never-told questions against
14 of 236 (5.9%). The pick, C1, cut these to 5 of 894 (0.6%) and 51 of 708 (7.2%) and failed one clause: that second
rate had to be no higher than the untrained model's. The 95% interval of the difference (-3.1 to +5.7 points) cannot
separate them; the rule requires every clause, so 6.37 stays shipped and C1 is published beside it, labelled. On S3,
code that searches every turn recalls more than both. S3's flags see only listed values of the asked category, so
invented values and other stored facts pass unseen.

Both sealed tests and their rules were registered before they ran; S3's scorer was written before any S3 file was
read, and rules changed after development readings are disclosed. Every decision and result is in a dated log.
