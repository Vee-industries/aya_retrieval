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
when that answer is in view, and it answers questions it was never told with unrelated stored facts.
On S3 ({{s3_chats}} chats written by blind Claude Opus writers and sealed before any new training row, run once), C1
against 6.37, each pooled over seeds 82, 83 and 94:

| S3 measure | Base with the tool | 6.37 | C1 | C1 seed 82 (this adapter) |
|---|---|---|---|---|
| Recall of facts out of view | {{s3_recall_base}} | {{s3_recall_637}} | {{s3_recall_c1}} | {{c1s82_recall}} |
| Names its own earlier wrong value, in view, when answering another question | {{s3_copy_base}} | {{s3_copy_637}} | {{s3_copy_c1}} | {{c1s82_copy}} |
| Never told, search returned text: names a value listed for the chat | {{s3_nhit_base}} | {{s3_nhit_637}} | {{s3_nhit_c1}} | {{c1s82_nhit}} |
| Never told, plain: names no listed value | {{s3_ntp_base}} | {{s3_ntp_637}} | {{s3_ntp_c1}} | {{c1s82_ntp}} |
| Answer in view: right | {{s3_iv_base}} | {{s3_iv_637}} | {{s3_iv_c1}} | {{c1s82_iv}} |
| Plain statement: no search | {{s3_st_base}} | {{s3_st_637}} | {{s3_st_c1}} | {{c1s82_st}} |

Relative to 6.37, C1's rate changes by {{s3_rel_copy}} on the first fault and {{s3_rel_nhit}} on the second; recall
shows no measured difference.

## Where it missed the rule

The rule (registered 12 November, before S3 opened): the pick replaces 6.37 only if (a) it beats base on recall, is
no more than 5 points below base on in view, statements and plain never-told, and its coherent share is at least
base's times 0.95, (b) its copy rate is at most half of 6.37's and at least 10 points lower, and (c) its rate of
naming a listed value on never-told questions is at least 10 points below 6.37's and not above base's. C1 passed (a),
(b) and the first two parts of (c). It failed "not above base's" by {{s3_gap_points}} points: {{s3_nhit_c1}} against
{{s3_nhit_base}}. The chat-resampled 95% interval of that difference is {{c1_gap_interval}}, so S3 cannot tell C1 from
base on this line; C1 fails the rule as registered. By seed: {{c1_nhit_seeds}}. This adapter, seed 82, is under base on
that line on its own (counting the asked category only; counting the chat's other stored facts too, {{s3_off_c182}}
against base's {{s3_off_base}}) and is {{c1s82_st_line}}: {{c1s82_st_gap}} against base.

## What the measures count

The never-told and copy measures check for values listed for the chat (the asked category's values in that chat and the
writers' listed wrong values). A reply that invents a new value, or gives an unrelated fact of another category, is not
counted; C1 still gives such unrelated stored facts (exploratory: {{s3_off_c1}} of its N-hit questions answered with
a value when they are counted). The untrained model invents many values on S3, so its rate of naming a listed value is a floor and its rate of naming
no listed value a ceiling. Coherence (three blind Claude Sonnet judges; the first decides), out of {{s3_coh_n}} lines
each: {{s3_coh_j1}}.

## How it was trained and chosen

From K1.3 seed 82, the reopened work's earlier pick, the same stage ran twice: training on corrections of the model's
own errors on its training chats ({{c1_set}}, {{c1_rows}} rows; {{c1_stage}} each time; LoRA rank {{c1_rank}} on the same seven projections as 6.37), {{c1_minutes}} minutes in all
on an RTX 3080, training peak {{c1_peak}} GiB. C1 was chosen for S3 over K1.3 on the totals of two fresh demos (older
facts {{demos_c1_older}} against {{demos_k13_older}}; never told {{demos_c1_never_told}} against
{{demos_k13_never_told}}) and on pooled development recall over three seeds ({{pick_recall_c1}} against
{{pick_recall_k13}}). The demo test was changed to totals after both models' demo readings existed; the long write-up
discloses it.

## How to use it

The same harness as 6.37: a system prompt that describes the `search_corpus` tool
(`aya_retrieval.tool_prompt.system_prompt_with_tools`), the last three exchanges as chat turns, and the earlier
exchanges indexed for search, one passage per exchange; up to {{max_calls}} searches a message, top {{top_k}} passages
each; greedy decoding. When the chat is short enough to show whole, show it whole.

## Limits

One sealed test of {{s3_chats}} chats, written by Claude agents, in English. Three training seeds of C1 ran on S3; this
repository holds one. The coherence judges are Claude models and were never checked against a person. No person
checked S3's flags. The method, every candidate, the registered rules and every results file are in
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval) (`docs/ARTICLE.md`,
`RECORDS.md`).

## Authors

Kevin Vaillancourt, working with an AI assistant (Claude, Anthropic) as an executive-function accommodation.
