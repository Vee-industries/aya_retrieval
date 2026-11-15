# Teaching a 3B model to search a long chat it can no longer see

Track 3, Agentic Fine-tuning, problem statement 4. Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya
Global (3.35B), shown only the last three exchanges of a chat, search the rest when the answer is out of view. On a
sealed test registered before training ({{sealed_conversations}} unseen chats in each of four conditions, made by the
same generator as the training chats, run once), the shipped seed recalls {{sealed_ship_range}} of
{{sealed_recall_n}} facts; the untrained model with the same tool recalls {{sealed_shipbase_range}}. Every registered
rule of that test passed. On its {{long_size}}-message chats, which fit the model's {{model_max_tokens}}-token window but could not be shown whole under this project's 10 GB memory cap (R-166), seed 82 recalls {{long_ship}} of
{{r168_recall_n}} across the four conditions, against {{long_code}} for code that searches every turn (run late,
exploratory).

On chats from outside writers the strongest simple baselines change the reading. When the chat fits, the untrained
model shown the whole chat recalls most ({{wc_recall_1}} and {{wc_recall_2}} of {{as_recall_n}}), and code shows no
measured difference from 6.37 ({{as_recall_1}} and {{as_recall_2}} against {{ow_82_recall_1}} and
{{ow_82_recall_2}}). On LongMemEval-S, long histories from outside the project, 6.37 shows no measured difference from
code ({{lme_judged_vs_code}}; Claude judges with LongMemEval's prompts) and declines {{lme_refuse_ship}} of
{{lme_answerable_n}} answerable questions.

A scripted demo then showed two faults: 6.37 answered never-told questions with unrelated stored facts and repeated
its own wrong answer while it was in view. I reopened the project. A second sealed test, S3, was written by
{{s3_writers}} blind writer agents and sealed before any new training row, with its ship rule fixed before it opened.
On S3, 6.37 does worse than the untrained model on both faults: it names its in-view wrong value on {{s3_copy_637}}
questions against {{s3_copy_base}}, and a value listed for the chat on {{s3_nhit_637}} never-told questions against
{{s3_nhit_base}}. Of {{reopened_n}} candidates, the pick, C1, cut these to {{s3_copy_c1}} and {{s3_nhit_c1}} with no
measured change in recall, and failed one clause: the second had to be no higher than the untrained model's. The
95% interval of that difference ({{c1_gap_interval}}) cannot tell them apart, but a miss is a miss: 6.37 stays
shipped, and C1 is published beside it, labelled. Report arms K1 and K2.1 met every measured S3 line (two seeds,
exploratory). The S3 measures count only values listed for the chat, so invented values pass unseen.

Both sealed tests and their rules were registered before they ran; rules changed after some development readings are
disclosed with their reasons. Every decision and result is in a dated log.
