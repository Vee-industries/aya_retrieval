# Teaching a 3B model to search a long chat it can no longer see

Track 3, Agentic Fine-tuning, problem statement 4. Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya
Global (3.35B), shown only the last three exchanges of a chat, search the rest when the answer is out of view. On a
sealed test registered before training ({{sealed_conversations}} unseen chats in each of four conditions, from the
training chats' generator, run once), the shipped seed recalls {{sealed_ship_range}} of {{sealed_recall_n}} facts,
against {{sealed_shipbase_range}} for the untrained model (base) with the same tool, and every registered rule passed. On its
{{long_size}}-message chats it recalls {{long_ship}} of {{r168_recall_n}}, against {{long_code}} for code that
searches every turn (run late, exploratory).

On chats from outside writers (Claude agents) that fit the window, base shown the whole chat recalls most ({{wc_recall_1}} and {{wc_recall_2}} of {{as_recall_n}}), and code shows no
measured difference from 6.37 ({{as_recall_1}} and {{as_recall_2}} against {{ow_82_recall_1}} and
{{ow_82_recall_2}}). On LongMemEval-S, histories past the window, 6.37 and code show no measured difference on answers
({{lme_j_ship}} and {{lme_j_code}} of a stratified {{lme_judged_n}}; Claude judges); code's first search finds the
evidence more often, {{lme_h2_code}} (registered H2); 6.37 declines {{lme_refuse_ship}} of
{{lme_answerable_n}} answerable questions.

A scripted demo then showed two faults: 6.37 answered never-told questions with unrelated stored facts and repeated
its own wrong answer in view. With the deadline reported extended (R-173), I saw results I had missed and judged the
extra time enough to train further, so I reopened the project. A second sealed test, S3, by
{{s3_writers}} blind writer agents, was sealed before any new training row, its ship rule fixed before it opened.
On S3, 6.37 does worse than base on both faults: it names its in-view wrong value on {{s3_copy_637}}
questions against {{s3_copy_base}}, and a listed value on {{s3_nhit_637}} never-told questions whose search returned text, against
{{s3_nhit_base}}.

The pick, C1 (trained on corrections of its own errors; picked after two demo-test changes, both after its demo
readings, the second also after K1.3's Demo5 reading), cut these to {{s3_copy_c1}} and {{s3_nhit_c1}} and failed
one clause by {{s3_gap_points}} points: that second rate had to be no higher than base's. The 95% interval of the
difference ({{c1_gap_interval}}) cannot separate them; the rule requires every clause, so 6.37 stays shipped and C1
is published beside it, labelled. On S3, code recalls more than both.

Both sealed tests and their rules were registered before they ran (S3's scorer after S3 started, before any S3 file
was read); rule changes after development readings are disclosed, and every decision is in a dated log.
