---
base_model: CohereLabs/tiny-aya-global
library_name: peft
license: cc-by-nc-4.0
language:
- en
pipeline_tag: text-generation
tags:
- lora
- tool-use
- long-context
- memory
---

# aya_retrieval 6.37: search a long chat for Tiny Aya Global

Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets
[Tiny Aya Global](https://huggingface.co/CohereLabs/tiny-aya-global) (3.35B, revision `af89d219`),
shown only the last three exchanges of a chat, search the rest when the answer is out of view. On
the sealed test ({{sealed_conversations}} unseen generated chats in each of four conditions, run
once), the shipped seed recalls {{sealed_ship_range}} of {{sealed_recall_n}} facts; the untrained
model with the same tool recalls {{sealed_shipbase_range}}. On chats from outside writers (written
by Claude Opus agents, a mean of {{ow_tokens_mean}} tokens), the untrained model shown the whole chat
recalls most ({{wc_recall_1}} and {{wc_recall_2}} of {{as_recall_n}}), and code that searches every
turn shows no measured difference from 6.37 ({{as_recall_1}} and {{as_recall_2}} against {{ow_82_recall_1}} and
{{ow_82_recall_2}}) and runs faster. There, training's measured gain is when to search: 6.37
searches on {{ow_82_recall_searched_1}} and {{ow_82_recall_searched_2}} of the {{as_recall_n}} recall questions,
base on {{ow_base_recall_searched_1}} and {{ow_base_recall_searched_2}}, and leaves answers already in view alone
({{ship_in_view_1}} and {{ship_in_view_2}} of {{as_kind_n}} right), where code searches every turn
({{as_in_view_1}} and {{as_in_view_2}}). On S3, a second sealed test from outside writers, 6.37 shows two faults more
often than the untrained model: it names its own in-view wrong value on {{s3_copy_637}} questions against
{{s3_copy_base}}, and a listed value on {{s3_nhit_637}} never-told questions against {{s3_nhit_base}}.

The shipped adapter is 6.37 (`fix17cs37` seed 82):
[aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37). The training and
test chats are in
[aya-retrieval-chats](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-chats) and
every evaluation log in
[aya-retrieval-eval-logs](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-eval-logs),
in two collections
([models](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-models-6af35d3c521e8481db061df5),
[datasets](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-datasets-6af35d3cf9a91556f52af373)).
The adapter and both datasets are public and un-gated (checked 2026-11-15, no login). The base
model `CohereLabs/tiny-aya-global` is gated: accept its licence on Hugging Face first.

{{status_line}}

## Reopened, 12 to 15 November

A scripted demo, run for 6.37 on 12 November, showed two faults: it answered questions it was never told with
unrelated stored facts, and it repeated its own wrong answer while that answer was still in view (R-175, R-176). With
the deadline reported extended (R-173), I saw results I had missed and judged the extra time enough to train further, so I reopened the
project (R-177); the push to replace 6.37 ran inside the time that remained. A second sealed test, S3, was written by {{s3_writers}} blind
writer agents and sealed before any new training row, and its ship rule was fixed before it opened (R-178, R-179,
R-191). {{reopened_n}} candidates were listed for screening, {{reopened_full}} read on every line; C1 became the pick (R-279). On S3, 6.37 does worse than the untrained
model on both faults: it names its in-view wrong value when answering another question on {{s3_copy_637}} questions
against {{s3_copy_base}}, and names a value listed for the chat on {{s3_nhit_637}} never-told questions against
{{s3_nhit_base}} (this seed alone: {{s3_ship82_copy}} and {{s3_ship82_nhit}}). C1 cut these to {{s3_copy_c1}} and
{{s3_nhit_c1}}. The second had to be no higher than the untrained model's, so C1 failed the rule on one clause (95%
interval of the difference {{c1_gap_interval}}) and **this adapter, 6.37 seed 82, stays shipped** (R-287) because no
replacement passed, not because it passed S3. C1 seed 82 is published beside it, labelled:
[aya-retrieval-c1](https://huggingface.co/KevinVaillancourt/aya-retrieval-c1). The S3 measures count only values
listed for the chat; invented values pass unseen. The full account is in the write-up,
sections 7 to 9.

## Results at a glance

Outside-writer chats, two sets (set 1 / set 2), one run each, the last three exchanges in view
except for base with the whole chat:

| Measure | Base, tool | Code | Base, whole chat | 6.37, tool |
|---|---|---|---|---|
| Recall, of {{as_recall_n}} | {{ow_base_recall_1}} / {{ow_base_recall_2}} | {{as_recall_1}} / {{as_recall_2}} | {{wc_recall_1}} / {{wc_recall_2}} (most) | {{ow_82_recall_1}} / {{ow_82_recall_2}} |
| Answer already in view, of {{as_kind_n}} | {{ow_base_in_view_1}} / {{ow_base_in_view_2}} | {{as_in_view_1}} / {{as_in_view_2}} | {{ow_wc_in_view_1}} / {{ow_wc_in_view_2}} | {{ship_in_view_1}} / {{ship_in_view_2}} |
| Never told: names no listed value, of {{as_kind_n}} | {{ow_base_never_told_1}} / {{ow_base_never_told_2}} | {{as_never_told_1}} / {{as_never_told_2}} | {{ow_wc_never_told_1}} / {{ow_wc_never_told_2}} | {{ship_never_told_1}} / {{ship_never_told_2}} |
| Plain statement left unsearched, of {{as_kind_n}} | {{ow_base_statement_1}} / {{ow_base_statement_2}} | {{as_statement_1}} / {{as_statement_2}} (searches every turn) | {{ow_wc_statement_1}} / {{ow_wc_statement_2}} (no tool) | {{ship_statement_1}} / {{ship_statement_2}} |

Generated chats:

| Measure | Base, tool | Code | Base, whole chat | 6.37, tool |
|---|---|---|---|---|
| Sealed test recall, of {{sealed_recall_n}}, four conditions | {{sealed_shipbase_range}} | not in the sealed run | not in the sealed run | {{sealed_ship_range}} |
| Recall, of {{r168_recall_n}}, sealed pools after the run (R-168) | {{r168_tool}} | {{r168_as}} | {{r168_wc}} (58 messages only; {{long_size}} messages does not fit 10 GB) | {{r168_ship}} ({{r168_ship58}} at 58 messages) |
| Right search decisions, of {{sealed_conversations}} (sealed; `heldout`, `independent`) | {{sealed_decisions_base}} | not run | not run | {{sealed_decisions_ship}} |
| Clean first calls (sealed; of the turns that searched; format only, unclean calls still ran) | {{sealed_clean_base}} | scripted | no tool | {{sealed_clean_ship}} |

LongMemEval-S ({{lme_questions}} questions; a history of {{lme_exchanges}} exchanges, so no
whole-chat arm fits; judged by three Claude Sonnet judges with LongMemEval's prompts, not the
official GPT-4o judge):

| Measure | Base, tool | Code | 6.37, tool |
|---|---|---|---|
| Judged right, of {{lme_judged_n}} judged | {{lme_j_base}} | {{lme_j_code}} | {{lme_j_ship}} (p = {{lme_judged_p_base}} against base, {{lme_judged_p_code}} against code) |
| Of those, answerable, of {{lme_judged_answerable_n}} (split after reading) | {{lme_ans_base}} | {{lme_ans_code}} | {{lme_ans_ship}} (p = {{lme_ans_p_base}} against base) |
| Declines on answerable, of all {{lme_answerable_n}} | {{lme_refuse_base}} | {{lme_refuse_code}} | {{lme_refuse_ship}} |
| Declines on unanswerable, of all {{lme_abstain_n}} | {{lme_abstain_base}} | {{lme_abstain_code}} | {{lme_abstain_ship}} |
| Gold answer in reply, of {{lme_read_n}} (mechanical) | {{lme_answer_base}} | {{lme_answer_code}} | {{lme_answer_ship}} |
| Clean first calls (of questions that searched) | {{lme_clean_base}} | scripted | {{lme_clean}} |
| Seconds a question | {{lme_secs_base}} | {{lme_secs_code}} | {{lme_secs_ship}} |

**Which to use when.**
1. If the chat was written outside this project's generator and fits the context, show it whole: base with the
   whole chat recalls most on outside-writer chats and S3, and needs no adapter. On S3 it names a listed value more
   often than base with the tool: on {{s3_nhit_wc}} never-told N-hit questions, against base's {{s3_nhit_base}}; and it
   names no listed value on {{s3_ntp_wc}} plain never-told questions, against base's {{s3_ntp_base}}.
2. If it is longer than the {{model_max_tokens}}-token window, 6.37 and code that searches every turn show no
   measured difference on LongMemEval-S answers; code's first search finds the evidence more often,
   {{lme_h2_code}} (registered H2, R-170), and code needs no training. 6.37 declines {{lme_refuse_ship}} of the
   {{lme_answerable_n}} questions that have an answer there; code declines {{lme_refuse_code}}. On S3 code names its
   in-view wrong value on {{s3_copy_as}} questions and a listed value on {{s3_nhit_as}} N-hit questions, against
   base's {{s3_copy_base}} and {{s3_nhit_base}}; neither fault was measured on chats past the window.
3. If repeating a wrong answer or naming a listed value on never-told questions matters, do not use this adapter: on
   S3 it does both more often than base. C1
   ([aya-retrieval-c1](https://huggingface.co/KevinVaillancourt/aya-retrieval-c1)) measured lower rates than this
   adapter ({{s3_rel_copy}} on copies, {{s3_rel_nhit}} on N-hit false answers) but is not below base on N-hit
   ({{s3_nhit_c1}} against {{s3_nhit_base}}); it missed one registered clause and is not the shipped model.

"Base" is the untrained Tiny Aya Global. "Code" is code that searches on every turn with the
newest message as the query, then hands base the passages (nothing trained). Recall counts the
`older` (a fact told long ago) and `confirm` ("did I tell you...?") questions. A clean first call is
a reply that parses whole as one `search_corpus` call with nothing before or after it, counted of
the replies that searched; an unclean call still ran its search, so the count is a format measure.

## First: when an outside chat fits, give it the whole chat; and plain code shows no measured difference

On two sets of chats by outside writers who never saw this project's generator (a mean of
{{ow_tokens_mean}} tokens a chat), the untrained model with every message in view answers
{{wc_base_older_1}} and {{wc_base_older_2}} of {{older_n}} questions about facts told earlier,
against {{tool82_older_1}} and {{tool82_older_2}} for this adapter with the tool and the last three
exchanges (R-164). Given the whole chat and the tool, the adapter and the untrained model show
no measured difference on every kind of message (one seed, two sets of {{ow_chats}} chats;
differences under {{kind_noise_diff}} points between two arms on a kind of {{kind_noise_n}} questions, the 95%
half-width of a difference between two rates near 50%, are below what this test resolves, and the test is not
powered to show equality; R-142, R-165). This holds on those
outside-writer chats only. On the project's generated sealed chats of 58 messages, {{r168_wc_tokens}} tokens, the untrained
model with the whole chat answers {{r168_wc}} of {{r168_recall_n}} recall questions against this
adapter's {{r168_ship58}} with the tool (R-168).

On the outside-writer chats, plain code that searches on every turn, with no training, shows no measured
difference from this adapter on recall, both with the last three exchanges in view: {{as_recall_1}} and
{{as_recall_2}} of {{as_recall_n}} against {{ow_82_recall_1}} and {{ow_82_recall_2}}, no measured
difference (p = {{as_p_1}} and {{as_p_2}}; R-169). Base with the tool searches on
{{ow_base_recall_searched_1}} and {{ow_base_recall_searched_2}} of the {{as_recall_n}} recall questions; code
searches every turn. Training adds searching when the answer is out of view (against base) and not
searching when it is in view (against code): where the answer is in view the adapter answers
{{ship_in_view_1}} and {{ship_in_view_2}} of {{as_kind_n}} and code {{as_in_view_1}} and
{{as_in_view_2}}; on facts never told, no listed value named, {{ship_never_told_1}} and {{ship_never_told_2}} against
{{as_never_told_1}} and {{as_never_told_2}}. On plain statements it leaves {{ship_statement_1}} and
{{ship_statement_2}} unsearched, below base's {{ow_base_statement_1}} and
{{ow_base_statement_2}}; code searches every one. On the generated sealed pools this adapter is
above code on recall: {{r168_ship}} of {{r168_recall_n}} at each of 58 and {{long_size}} messages
against code's {{r168_as}} (every sign test below 0.001; R-168); it is above the whole chat at 58 messages, the only
size the whole chat ran at (table above). The code is faster on every set:
{{speed_sealed_short}} on the sealed pools, {{speed_ow_short}} on the outside-writer sets.

Not measured: the untrained model reading the whole chat at {{long_size}} messages ({{hd_419_tokens}}
tokens on `hard_dev`, inside the window). Those runs ran out of card memory under the {{oom_allowed}} GiB cap on a
10 GB card (R-166); every three-exchange run in the sealed run peaked at {{sealed_peak_range}} GiB
of card memory at inference (R-163).

## Results with only the last three exchanges in view

- **Outside-writer sets** ({{ow_chats}} chats each, written blind to the generator): recall
  {{ow_82_recall_1}} and {{ow_82_recall_2}} of {{ow_recall_n}} against the untrained model's
  {{ow_base_recall_1}} and {{ow_base_recall_2}} (gain {{ow_82_int_1}} and {{ow_82_int_2}} points, 95%
  intervals resampling chats; set 1's p = {{ow_82_p_1}} is above the registered 0.01) (R-146, R-157).
  The gain is on direct questions; on "..., right?" questions with a false claim it corrects
  {{claims_82_corrected_1}} and {{claims_82_corrected_2}} of {{claims_false_n}} (R-164).
- Seed 82, the shipped seed, is the lowest of the eight training seeds on
  the first outside-writer set, on sealed conditions C and D, and on `hard_dev`; the eight seeds
  pooled gain {{ow_seeds_diff_1}} and {{ow_seeds_diff_2}} points on the two sets
  ({{ow_seeds_int_1}} and {{ow_seeds_int_2}}) (R-141, R-146, R-157, R-163).
- **Who wrote and judged the tests.** The outside writers are {{ow_writers}} fresh Claude Opus agents
  a set; the coherence judges are Claude Sonnet agents only, never checked against a person.
- **The registered sealed test** (R-162, R-163): two generator-built pools, one and four decoys a
  chat, the untrained model and all eight training seeds run once. Every registered rule passes in
  all four conditions. Recall pooled over the eight seeds is {{sealed_adapters_range}}% against the
  untrained model's {{sealed_base_range}}% ({{sealed_gain_range}} points; registered rule met, p below
  0.01); this seed gets {{sealed_ship_range}} of {{sealed_recall_n}} against {{sealed_shipbase_range}}.
  Every right answer came from a search that found the fact; no seed made more false retrievals than
  the untrained model; every seed was judged coherent more often by all three judges.
- **LongMemEval-S, an outside check** (R-170): a third kind of chat, user-to-assistant chats, partly
  real logs and partly model-simulated, never pooled with the sets above. The adapter's system
  prompt ("You are chatting with a friend") does not fit them. No arm is judged right on more than
  {{lme_j_max}} of {{lme_judged_n}}.
  This adapter finds the evidence more often than the untrained model with the tool only because it
  searches more often; code that always searches finds it more often still ({{lme_found_code}}
  against {{lme_found_ship}} of {{lme_evidence_n}}), with no measured difference in gold answers
  ({{lme_answer_code}} against {{lme_answer_ship}} of {{lme_read_n}}), and is faster. The adapter
  declines {{lme_abstain_ship}} of all {{lme_abstain_n}} unanswerable questions, and also
  {{lme_refuse_ship}} of all {{lme_answerable_n}} answerable ones. Judged with LongMemEval's prompts
  by Claude judges (not the official score, which uses GPT-4o): {{lme_j_ship}} of {{lme_judged_n}}
  right, against {{lme_j_base}} for the untrained model with the tool and {{lme_j_code}} for code.
  Split after reading, on the {{lme_judged_answerable_n}} answerable questions it ties code and shows
  no measured difference from the untrained model ({{lme_split_vs_base_short}}); {{lme_lead_unans}}
  of its {{lme_lead}}-question lead come from the {{lme_unanswerable_n}} unanswerable ones. My blind
  check of 50 lines (the author, not an independent marker) agrees with each judge on
  {{lme_kevin}}.

## How to use it

When the chat is short enough to show whole, show base the whole chat and leave this adapter out.
On S3 the whole chat has its own weakness: base with the whole chat names a listed value on
{{s3_nhit_wc}} never-told N-hit questions, against {{s3_nhit_base}} for base with the tool, and names
no listed value on {{s3_ntp_wc}} plain never-told questions, against {{s3_ntp_base}}.
This adapter with the whole chat was measured only on the outside-writer chats, of a mean of
{{ow_tokens_mean}} tokens (R-165, one seed), where it shows no measured difference from base with the
whole chat (the test cannot show equality); it was not run on S3, where this adapter with the tool is
worse than base on both faults, nor on the generated chats, where the untrained model with the whole
chat was below this adapter with the tool (R-168). Whole chats near the model's
{{model_max_tokens}}-token limit were not measured.
When it does not, use the harness the adapter was trained in: a system prompt that describes the
`search_corpus` tool (`aya_retrieval.tool_prompt.system_prompt_with_tools`), the last three
exchanges as chat turns, and the earlier exchanges indexed for search, one passage per exchange.
`run_turn` in `src/aya_retrieval/harness.py` runs that loop: up to {{max_calls}} searches a
message, top {{top_k}} passages each. Decoding in every test was greedy. Loading it (not run in this
form; the repository's `aya_retrieval.models.load_model` loads the same revision in bfloat16):

```python
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base, revision = "CohereLabs/tiny-aya-global", "af89d219b53ed9b13b8a4645f9c8028973510324"
tokenizer = AutoTokenizer.from_pretrained(base, revision=revision)
model = AutoModelForCausalLM.from_pretrained(base, revision=revision, dtype=torch.bfloat16)
model = PeftModel.from_pretrained(model, "KevinVaillancourt/aya-retrieval-6.37")
```

## Limitations

- On S3 this adapter repeats its own in-view wrong value and names listed values on never-told questions more often than
  the untrained model (above).
- On the short outside-writer chats the whole chat beats the three-exchange view with search,
  and plain code that searches every turn shows no measured difference from this adapter and is faster (above).
  The adapter's recall gain over plain code is shown on the generated sealed pools only (R-168). On S3, code
  recalls more than this adapter ({{s3_recall_as}} against {{s3_recall_637}}; {{s3_code_vs_637}}), and the whole
  chat {{s3_recall_wc}}.
- On LongMemEval-S it declines {{lme_refuse_ship}} of {{lme_answerable_n}} questions it should
  answer, and no arm is judged right on more than {{lme_j_max}} of {{lme_judged_n}} (R-170). Replies are capped at {{lme_cap}} tokens in every
  test, and the longest LongMemEval-S views run out of memory on a 10 GB card.
- It corrects {{claims_82_corrected_1}} and {{claims_82_corrected_2}} of {{claims_false_n}} false claims in tag questions ("..., right?").
- When the friend is just chatting it should not search; on the outside-writer sets it searched
  {{ow_82_stmt_searched_1}} and {{ow_82_stmt_searched_2}} of {{kind_noise_n}} such lines, more than
  base ({{ow_base_stmt_searched_1}} and {{ow_base_stmt_searched_2}}) on both sets (R-146, R-157).
- The scorer does not catch an invented value on `never_told`. When a fact was never told the
  adapter should decline, and the scorer passes any reply that names none of the listed values, so
  a reply that invents a value outside the list still passes (R-020). The scorer was checked by
  hand on {{human_check_n}} lines from development pools: I (the author, not an independent marker)
  agreed with it on {{human_check_author}} and an independent second marker on
  {{human_check_second}} (R-144, R-145).
- On the scripted demo (`demo/chat.txt`, greedy), the adapter searched with queries copied from its
  training set on two of its four questions ("brother new job" and "sister broke skiing injury",
  each in 3 rows of `data/screens/fix17cs37.jsonl`) and answered both with an unrelated stored fact.
  The earlier adapters v5 and fix 15 declined on those two turns (R-175).
- On eight more demo questions registered before they ran (R-176), the untrained model was right on 2 and 6.37 on 0: 6.37 repeated its own earlier wrong answer, still in view, on 6 of the 8.
- Its commonest misses: a search that misses the fact (including facts told with a pronoun), and a
  found fact answered from the line's first clause, leaving out the detail asked for.
- English only. Tested on generated and agent-written chats, and on LongMemEval-S, whose chats
  mix real logs of people talking to an assistant with model-simulated sessions (the sessions
  holding the answers were simulated).
- Coherence was judged by Claude models only, never checked against a person. The LongMemEval-S
  judges are Claude, not the official GPT-4o, and I (the author, not an independent marker)
  checked 50 of their lines.
- Licence: Tiny Aya is CC-BY-NC-4.0 and this adapter, trained from it, carries that licence. The
  base model is gated on Hugging Face.

## Training

{{training_rows}} rows ({{training_kinds}}), built from the training pool only: targets are the
untrained model's own replies where they pass the scorer, vetted plain-chat replies, and scripted
answers where needed. {{training_setup}}. Trained with AgentTune; {{train_minutes}} minutes a seed
on an RTX 3080, with a training peak of {{train_peak}} GiB of card memory. The method, the
registered tests, every candidate tried, the errors found and every results file are in the
repository,
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval):
`docs/ARTICLE.md` and `RECORDS.md`.

## Authors

Kevin Vaillancourt, working with an AI assistant (Claude, Anthropic) as an executive-function
accommodation. Built for the Lexsi AI Safety and Alignment Hackathon 2026, Track 3.
