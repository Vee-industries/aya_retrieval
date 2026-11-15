# Teaching a 3B model to search a long chat it can no longer see

Track 3, Agentic Fine-tuning, problem statement 4. Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya
Global (3.35B), shown only the last three exchanges of a chat, search the rest when the answer is out of view. On a
sealed test registered before training ({{sealed_conversations}} unseen chats in each of four conditions, made by the
same generator as the training chats, run once), the shipped seed recalls {{sealed_ship_range}} of
{{sealed_recall_n}} facts; the untrained model with the same tool recalls {{sealed_shipbase_range}}. Every registered
rule of that test passed. On its {{long_size}}-message chats, which fit the model's {{model_max_tokens}}-token window but could not be shown whole under this project's 10 GB memory cap, seed 82 recalls {{long_ship}} of
{{r168_recall_n}} across the four conditions, against {{long_code}} for code that searches every turn (run late,
exploratory).

On chats from outside writers the strongest simple baselines change the reading. When the chat fits, the untrained
model shown the whole chat recalls most ({{wc_recall_1}} and {{wc_recall_2}} of {{as_recall_n}}), and code shows no
measured difference from 6.37 ({{as_recall_1}} and {{as_recall_2}} against {{ow_82_recall_1}} and
{{ow_82_recall_2}}). On LongMemEval-S, histories past the window, 6.37 and code show no measured difference on answers
({{lme_j_ship}} and {{lme_j_code}} of a stratified {{lme_judged_n}}; Claude judges); code's first search finds the
evidence more often, {{lme_h2_code}} (registered H2, R-170); 6.37 declines {{lme_refuse_ship}} of
{{lme_answerable_n}} answerable questions.

A scripted demo then showed two faults: 6.37 answered never-told questions with unrelated stored facts and repeated
its own wrong answer while it was in view. I reopened the project. A second sealed test, S3, was written by
{{s3_writers}} blind writer agents and sealed before any new training row, with its ship rule fixed before it opened.
On S3, 6.37 does worse than the untrained model on both faults: it names its in-view wrong value on {{s3_copy_637}}
questions against {{s3_copy_base}}, and a listed value on {{s3_nhit_637}} never-told questions against
{{s3_nhit_base}}.

The pick, C1 (chosen after the demo test changed twice once both models' readings existed), cut these to
{{s3_copy_c1}} and {{s3_nhit_c1}} and failed one clause: that second rate had to be no higher than the untrained
model's. The 95% interval of the difference ({{c1_gap_interval}}) cannot separate them; the rule requires every
clause, so 6.37 stays shipped and C1 is published beside it, labelled. On S3, code that searches every turn recalls
more than both. S3's flags see only listed values of the asked category, so invented values and other stored facts
pass unseen.

Both sealed tests and their rules were registered before they ran; S3's scorer was written after S3 started, before
any S3 file was read, and rules changed after development readings are disclosed. Every decision and result is in a
dated log.
