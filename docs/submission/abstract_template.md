# Teaching a 3B model to search a long chat it can no longer see

Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya Global (3.35B), shown only the last three
exchanges of a chat, search the rest when the answer is out of view. On a sealed test registered before training
({{sealed_conversations}} unseen generated chats in each of four conditions, run once), the shipped seed recalls
{{sealed_ship_range}} of {{sealed_recall_n}} facts; the untrained model with the same tool recalls
{{sealed_shipbase_range}}. On the first sealed test, every registered rule passed: every right answer came from a search that found the fact,
no adapter made more false retrievals than the untrained model, and three judges rated every adapter coherent more
often.

The strongest simple baselines change the reading. On chats from outside writers (Claude Opus agents, about
{{ow_tokens_mean}} tokens), the untrained model shown the whole chat recalls most ({{wc_recall_1}} and
{{wc_recall_2}} of {{as_recall_n}}), and code that searches every turn recalls as well as 6.37 ({{as_recall_1}} and
{{as_recall_2}} against {{ow_82_recall_1}} and {{ow_82_recall_2}}) and runs faster. Training's measured gain there
is when to search: 6.37 leaves answers already in view alone ({{ship_in_view_1}} and {{ship_in_view_2}} of
{{as_kind_n}} right), where code searches every turn ({{as_in_view_1}} and {{as_in_view_2}}).

A scripted demo then showed two faults: 6.37 answered never-told questions with unrelated stored facts and repeated
its own wrong answer while it was in view. With the deadline extended, the project was reopened. A second sealed
test, S3, was written by {{s3_writers}} blind writer agents and sealed before any new training row, with its ship
rule fixed before it opened. {{reopened_n}} candidates were listed for screening on development sets, {{reopened_full}} read on every line; the pick, C1,
cut copies of a wrong answer in view from {{s3_copy_637}} to {{s3_copy_c1}}, and false answers to never-told
questions whose search returned text from {{s3_nhit_637}} to {{s3_nhit_c1}}. It failed one clause: those false
answers had to be no higher than the untrained model's {{s3_nhit_base}}. By the registered rule, 6.37 stays shipped.
On S3 the whole chat ({{s3_recall_wc}}) and code ({{s3_recall_as}}) again recall more than either trained model.

On LongMemEval-S ({{lme_questions}} questions, histories far longer than the context), judged by Claude judges with
LongMemEval's prompts, not the official GPT-4o judge, 6.37 is right on {{lme_j_ship}} of {{lme_judged_n}} judged
questions against {{lme_j_base}} for the untrained model with the tool, but declines {{lme_refuse_ship}} of
{{lme_answerable_n}} answerable questions. Every test was registered before it ran; every decision and result is in
a dated log.
