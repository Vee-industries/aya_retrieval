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

# aya_retrieval: out-of-view recall for Tiny Aya Global

A LoRA adapter for [Tiny Aya Global](https://huggingface.co/CohereLabs/tiny-aya-global) (revision
`af89d219`) that lets the model answer questions about things said earlier in a long chat, after
they have left its view. The model sees only the last three exchanges. When a question needs
something older, it calls a `search_corpus` tool over the earlier conversation, reads what comes
back, and answers; when the fact was never told, it says so; when the user is just chatting, it
does not search.

{{status_line}}

## Results

{{results_scope}}

- Questions about earlier facts: {{tuned_recall_58}}% right in 58-message chats and
  {{tuned_recall_419}}% in 419-message chats, against {{base_recall_58}}% and
  {{base_recall_419}}% for the untrained model given the same tool ({{gain_58}}% and
  {{gain_419}}%).
- {{coherence_summary}}
- {{false_retrieval_summary}}
- {{hard_dev_abstract}}

Training: {{training_setup}}

## How to use it

The adapter expects the harness it was trained in: a system prompt that describes the
`search_corpus` tool (`aya_retrieval.tool_prompt.system_prompt_with_tools`), the last three
exchanges as chat turns, and the earlier exchanges indexed for search, one passage per exchange.
`run_turn` in `src/aya_retrieval/harness.py` runs that loop: the model decides, the tool runs, the
model answers from the result, up to three searches a message.

## Limitations

- English only, and tested only on made-up people and facts in generated chats.
- On a development pool written by another author, recall is lower and the adapter sometimes
  states another person's fact as the answer to a question about a fact never told. The
  write-up's failure-modes section lists each known failure and its status.
- It answers from what the search returns. It cannot know what a search missed, and an earlier
  message that was wrong will be repeated.
- Licence: Tiny Aya is CC-BY-NC-4.0 and this adapter, trained from it, carries that licence.

## Training data and method

Every training row is generated from a seed: scripted conversations of made-up people and facts,
with a final message of one of five kinds (an older fact, a confirmation, a fact still in view, a
fact never told, plain chat). Target replies are the untrained model's own replies where it
answered well (with the found passage in view for older facts; plain-chat replies vetted by a
blind judge), and scripted sentences for confirmations and for facts never told. The full method, the registered tests, the errors found and
corrected, and every results file are in the repository: `docs/ARTICLE.md` and `RECORDS.md`.

## Authors

Kevin Vaillancourt, working with an AI assistant (Claude, Anthropic) as an executive-function
accommodation. Built for the Lexsi AI Safety and Alignment Hackathon 2026, Track 3.
