# Teaching a 3B model to search a long chat it can no longer see

Track 3, Agentic Fine-tuning, problem statement 4. Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya
Global (3.35B), shown only the last three exchanges of a chat, search the rest when the answer is out of view. On a
sealed test registered before training (300 unseen chats in each of four conditions, from the
training chats' generator, run once), the shipped seed recalls 91 to 107 of 120 facts,
against 13 to 32 for the untrained model (base) with the same tool, and every registered rule passed. On its
419-message chats it recalls 52, 52, 46 and 44 of 60, against 32, 30, 17 and 14 for code that
searches every turn (run late, exploratory).

On chats from outside writers (Claude agents) that fit the window, base shown the whole chat recalls most (71 and 65 of 120), and code shows no
measured difference from 6.37 (42 and 47 against 39 and
53). On LongMemEval-S, histories past the window, 6.37 and code show no measured difference on answers
(53 and 40 of a stratified 248; Claude judges); code's first search finds the
evidence more often, 372 against 333 of 476 (registered H2); 6.37 declines 233 of
470 answerable questions.

A scripted demo then showed two faults: 6.37 answered never-told questions with unrelated stored facts and repeated
its own wrong answer in view. With the deadline reported extended (R-173), I saw results I had missed and judged the
extra time enough to train further, so I reopened the project. A second sealed test, S3, by
six blind writer agents, was sealed before any new training row, its ship rule fixed before it opened.
On S3, 6.37 does worse than base on both faults: it names its in-view wrong value on 195 of 894 (21.8%)
questions against 11 of 298 (3.7%), and a listed value on 286 of 708 (40.4%) never-told questions whose search returned text, against
14 of 236 (5.9%).

The pick, C1 (trained on corrections of its own errors; picked after two demo-test changes, both after its demo
readings, the second also after K1.3's Demo5 reading), cut these to 5 of 894 (0.6%) and 51 of 708 (7.2%) and failed
one clause by 1.3 points: that second rate had to be no higher than base's. The 95% interval of the
difference (-3.1 to +5.7 points) cannot separate them; the rule requires every clause, so 6.37 stays shipped and C1
is published beside it, labelled. On S3, code recalls more than both.

Both sealed tests and their rules were registered before they ran (S3's scorer after S3 started, before any S3 file
was read); rule changes after development readings are disclosed, and every decision is in a dated log.
