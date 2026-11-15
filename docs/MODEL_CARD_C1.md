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

# aya_retrieval C1: the reopened candidate, published beside 6.37

C1 is a LoRA adapter on [Tiny Aya Global](https://huggingface.co/CohereLabs/tiny-aya-global) (3.35B, revision
`af89d219`) from the reopened work of the aya_retrieval project (Lexsi AI Safety and Alignment Hackathon 2026, Track 3).
**It is not the shipped model.** It failed one clause of the ship rule registered before the sealed test S3 opened, so
6.37 seed 82 stays the shipped model:
[aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37). This repository holds C1 seed 82,
the seed the rules named to ship.

## Why it is published

The project reopened after 6.37 shipped, to fix two faults a scripted demo showed: 6.37 repeats its own wrong answer
when that answer is in view, and it answers questions it was never told with values from passages its search returned.
On S3 (60 chats written by blind Claude Opus writers and sealed before any new training row, run once), C1
against 6.37, each pooled over seeds 82, 83 and 94:

| S3 measure | Base with the tool | 6.37 | C1 | C1 seed 82 (this adapter) |
|---|---|---|---|---|
| Recall of facts out of view | 59 of 414 (14.3%) | 347 of 1,242 (27.9%) | 364 of 1,242 (29.3%) | 127 of 414 (30.7%) |
| Names its own earlier wrong value, in view, when answering another question | 11 of 298 (3.7%) | 195 of 894 (21.8%) | 5 of 894 (0.6%) | 1 of 298 (0.3%) |
| Never told, search returned text: names a value listed for the chat | 14 of 236 (5.9%) | 286 of 708 (40.4%) | 51 of 708 (7.2%) | 11 of 236 (4.7%) |
| Never told, plain: names no listed value | 111 of 120 (92.5%) | 238 of 360 (66.1%) | 344 of 360 (95.6%) | 116 of 120 (96.7%) |
| Answer in view: right | 52 of 60 (86.7%) | 161 of 180 (89.4%) | 160 of 180 (88.9%) | 55 of 60 (91.7%) |
| Plain statement: no search | 58 of 60 (96.7%) | 180 of 180 (100.0%) | 166 of 180 (92.2%) | 50 of 60 (83.3%) |

Relative to 6.37, C1's rate changes by -97% on the first fault and -82% on the second; recall
shows no measured difference.

## Where it missed the rule

The rule (registered 12 November, before S3 opened): the pick replaces 6.37 only if (a) it beats base on recall, is
no more than 5 points below base on in view, statements and plain never-told, and its coherent share is at least
base's times 0.95, (b) its copy rate is at most half of 6.37's and at least 10 points lower, and (c) its rate of
naming a listed value on never-told questions is at least 10 points below 6.37's and not above base's. C1 passed (a),
(b) and the first two parts of (c). It failed "not above base's" by 1.3 points: 51 of 708 (7.2%) against
14 of 236 (5.9%). The chat-resampled 95% interval of that difference is -3.1 to +5.7 points, so S3 cannot tell C1 from
base on this line; C1 fails the rule as registered. By seed: 11 of 236 (seed 82), 29 of 236 (seed 83), 11 of 236 (seed 94). This adapter, seed 82, is under base on
that line on its own and is below (a)'s statement line, base's rate minus 5 points (91.7%).

## What the measures count

The never-told and copy measures check for values listed for the chat (the asked category's values in that chat and the
writers' listed wrong values). A reply that invents a new value, or gives an unrelated fact of another category, is not
counted. The untrained model invents many values on S3, so its rate of naming a listed value is a floor and its rate of naming
no listed value a ceiling. Coherence (three blind Claude Sonnet judges; the first decides), out of 120 lines
each: C1 97, base 95.

## How it was trained and chosen

From K1.3 seed 82, the reopened work's earlier pick, the same stage ran twice: training on corrections of the model's
own errors on its training chats (`data/screens/k13op_82_r253.jsonl`, 1,137 rows; learning rate 0.0001, 1 epoch, batch 2 each time), 26 minutes in all
on an RTX 3080, training peak 7.87 GiB. C1 was chosen for S3 over K1.3 on the totals of two fresh demos (older
facts 5 of 12 against 4 of 12; never told 6 of 8 against
5 of 8) and on pooled development recall over three seeds (775 against
742). The demo test was changed to totals after both models' demo readings existed; the long write-up
discloses it.

## How to use it

The same harness as 6.37: a system prompt that describes the `search_corpus` tool
(`aya_retrieval.tool_prompt.system_prompt_with_tools`), the last three exchanges as chat turns, and the earlier
exchanges indexed for search, one passage per exchange; up to 3 searches a message, top 5 passages
each; greedy decoding. When the chat is short enough to show whole, show it whole.

## Limits

One sealed test of 60 chats, written by Claude agents, in English. Three training seeds of C1 ran on S3; this
repository holds one. The coherence judges are Claude models and were never checked against a person. No person
checked S3's flags. The method, every candidate, the registered rules and every results file are in
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval) (`docs/ARTICLE.md`,
`RECORDS.md`).

## Authors

Kevin Vaillancourt, working with an AI assistant (Claude, Anthropic) as an executive-function accommodation.
