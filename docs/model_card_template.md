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

A LoRA adapter for [Tiny Aya Global](https://huggingface.co/CohereLabs/tiny-aya-global) (revision
`af89d219`), shipped as 6.37 (`fix17cs37` seed 82). Shown only the last part of a chat, the model
calls a `search_corpus` tool over the earlier conversation when a question needs something out of
view, reads what comes back, and answers. When the fact was never told it should decline; the
scorer passes any reply that names none of the listed values, so an invented value outside the list
passes (R-020). When the friend is just chatting it should not search; on the outside-writer sets it
searched {{ow_82_stmt_searched_1}} and {{ow_82_stmt_searched_2}} of {{kind_noise_n}} such lines,
more than base ({{ow_base_stmt_searched_1}} and {{ow_base_stmt_searched_2}}) on both sets (R-146,
R-157).

{{status_line}}

## First: when the chat fits, give it the whole chat

On two sets of chats by outside writers who never saw this project's generator (about
{{ow_tokens_mean}} tokens a chat), the untrained model with every message in view answers
{{wc_base_older_1}} and {{wc_base_older_2}} of {{older_n}} questions about facts told earlier,
against {{tool82_older_1}} and {{tool82_older_2}} for this adapter with the tool and the last three
exchanges (R-164). Given the whole chat and the tool, the adapter and the untrained model show
no measured difference (one seed, two sets of {{ow_chats}} chats; gaps under about {{kind_noise}} points on a kind of {{kind_noise_n}} questions could not be seen, R-142) on every kind of message
(R-165). The adapter is for chats
too long to show whole. Not measured: the untrained model reading the whole chat at 419 messages
(about {{hd_419_tokens}} tokens on `hard_dev`). Those runs ran out of card memory under the
{{oom_allowed}} GiB cap on a 10 GB card (R-166); every three-exchange run in the sealed run peaked at
{{sealed_peak_range}} GiB (R-163).

## Results with only the last three exchanges in view

- **Outside-writer sets** (40 chats each, written blind to the generator): recall
  {{ow_82_recall_1}} and {{ow_82_recall_2}} of {{ow_recall_n}} against the untrained model's
  {{ow_base_recall_1}} and {{ow_base_recall_2}} (gain {{ow_82_int_1}} and {{ow_82_int_2}} points, 95%
  intervals resampling chats; set 1's p = {{ow_82_p_1}} is above the registered 0.01) (R-146, R-157).
  The gain is on direct questions; on "..., right?" questions with a false claim it corrects
  {{claims_82_corrected_1}} and {{claims_82_corrected_2}} of {{claims_false_n}} and goes along with
  the rest (R-164).
- **The shipped seed is not the strongest.** Seed 82 is the lowest of the eight training seeds on
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

## How to use it

When the chat is short enough to show whole, show it the whole chat; the tool may stay in the
prompt (R-165). The measured chats were about {{ow_tokens_mean}} tokens; whole chats near the model's
{{model_max_tokens}}-token limit were not measured.
When it does not, use the harness the adapter was trained in: a system prompt that describes the
`search_corpus` tool (`aya_retrieval.tool_prompt.system_prompt_with_tools`), the last three
exchanges as chat turns, and the earlier exchanges indexed for search, one passage per exchange.
`run_turn` in `src/aya_retrieval/harness.py` runs that loop: up to {{max_calls}} searches a
message, top {{top_k}} passages each. Decoding in every test was greedy.

## Limitations

- On short chats the whole chat beats the three-exchange view with search (above).
- It goes along with most false claims in tag questions ("..., right?").
- Its commonest misses: a search that misses the fact (including facts told with a pronoun), and a
  found fact answered from the line's first clause, leaving out the detail asked for.
- English only; tested on generated and agent-written chats, never on real ones.
- Coherence was judged by Claude models only, never checked against a person.
- Licence: Tiny Aya is CC-BY-NC-4.0 and this adapter, trained from it, carries that licence.

## Training

{{training_rows}} rows ({{training_kinds}}), built from the training pool only: targets are the
untrained model's own replies where they pass the scorer, vetted plain-chat replies, and scripted
answers where needed. {{training_setup}}. The method, the registered tests, every candidate tried,
the errors found and every results file are in the repository: `docs/ARTICLE.md` and `RECORDS.md`.

## Authors

Kevin Vaillancourt, working with an AI assistant (Claude, Anthropic) as an executive-function
accommodation. Built for the Lexsi AI Safety and Alignment Hackathon 2026, Track 3.
