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

Draft. Numbers are development results on the probe pool; the registered held-out run replaces them before submission.

## Results

Development numbers: the probe pool, 240 conversations (24 of each kind at each length), the untrained model against 3 adapters (v5) trained on seeds 82, 83, 84. The held-out run replaces these.

- Questions about earlier facts: 98% right in 58-message chats and
  96% in 419-message chats, against 31% and
  31% for the untrained model given the same tool (+213% and
  +207%).
- A blind judge finds the adapter's replies 14% more often coherent than the untrained model's, and at or above it on every kind judged.
- It names the wrong person's fact in 0.3% of replies, against 5.4% for the untrained model.
- On a harder development pool written by an independent agent, recall falls to 60% (untrained: 21%), because the adapter searches unfamiliar kinds of fact as if they were ones it was trained on.

Training: 800 rows (Fact told long ago 200, “Did I tell you…?” 150, Fact still on screen 150, Never told 150, Just chatting 150); LoRA rank 32 on the attention and MLP projections, learning rate 3e-4, 3 epochs, batch 2.

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
