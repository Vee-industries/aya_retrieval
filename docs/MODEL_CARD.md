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
the sealed test (300 unseen generated chats in each of four conditions, run
once), the shipped seed recalls 91 to 107 of 120 facts; the untrained
model with the same tool recalls 13 to 32. On chats from outside writers (written
by Claude Opus agents, about 1,400 tokens), the untrained model shown the whole chat
does best (71 and 65 of 120), and code that searches every
turn recalls as well as 6.37 (42 and 47 against 39 and
53) and runs faster. There, training's measured gain is when to search: 6.37
searches for facts out of view, which base rarely does, and leaves answers already in view alone
(35 and 37 of 40 right), where code searches every turn
(13 and 16).

The shipped adapter is 6.37 (`fix17cs37` seed 82):
[aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37). The training and
test chats are in
[aya-retrieval-chats](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-chats) and
every evaluation log in
[aya-retrieval-eval-logs](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-eval-logs),
in two collections
([models](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-models-6af35d3c521e8481db061df5),
[datasets](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-datasets-6af35d3cf9a91556f52af373)).
The adapter and both datasets are public and un-gated (checked 2026-11-12, no login). The base
model `CohereLabs/tiny-aya-global` is gated: accept its licence on Hugging Face first.

Final numbers for the shipped model, 6.37 (`fix17cs37` seed 82, frozen before the sealed run): the sealed run, the two outside-writer sets, the whole-chat control, the two registered references run late, and LongMemEval-S as an outside check. Every number is computed from committed results files by `scripts/make_article.py`; `RECORDS.md` holds the dated record behind each.

## Results at a glance

Outside-writer chats, two sets (set 1 / set 2), one run each, the last three exchanges in view
except for base with the whole chat:

| Measure | Base, tool | Code | Base, whole chat | 6.37, tool |
|---|---|---|---|---|
| Recall, of 120 | 26 / 27 | 42 / 47 | 71 / 65 (best) | 39 / 53 |
| Answer already in view, of 40 | 36 / 34 | 13 / 16 | 35 / 32 | 35 / 37 |
| Never told, of 40 | 34 / 32 | 31 / 24 | 31 / 28 | 37 / 36 |
| Plain statement left unsearched, of 40 | 38 / 39 | 0 / 0 (searches every turn) | 40 / 40 (no tool) | 37 / 35 |

Generated chats:

| Measure | Base, tool | Code | Base, whole chat | 6.37, tool |
|---|---|---|---|---|
| Sealed test recall, of 120, four conditions | 13 to 32 | not in the sealed run | not in the sealed run | 91 to 107 |
| Recall, of 60, sealed pools after the run (R-168) | 5 to 17 | 14 to 32 | 21 to 33 (58 messages only; 419 messages does not fit 10 GB) | 44 to 55 (46 to 55 at 58 messages) |
| Right search decisions, of 300 (sealed; `heldout`, `independent`) | 180, 193 | not run | not run | 298, 296 |
| Clean first calls (sealed; of the turns that searched; format only, unclean calls still ran) | 52 of 136, 49 of 107 | scripted | no tool | 180 of 180, 184 of 184 |

LongMemEval-S (500 questions; a history of 244 (197 to 305) exchanges, so no
whole-chat arm fits; judged by three Claude Sonnet judges with LongMemEval's prompts, not the
official GPT-4o judge):

| Measure | Base, tool | Code | 6.37, tool |
|---|---|---|---|
| Judged right, of 248 judged | 34 | 40 | 53 (p = 0.014 against base, 0.12 against code) |
| Of those, answerable, of 233 (split after reading) | 32 | 40 | 40 (p = 0.29 against base) |
| Declines on answerable, of all 470 | 22 | 1 | 233 |
| Declines on unanswerable, of all 30 | 2 | 0 | 21 |
| Gold answer in reply, of 411 (mechanical) | 51 | 63 | 51 |
| Clean first calls (of questions that searched) | 146 of 328 | scripted | 441 of 441 |
| Seconds a question | 3.47 | 3.09 | 3.81 |

**Which to use when.**
1. If the whole chat fits in the context, show it whole: base with the whole chat recalls best on
   outside-writer chats, and needs no adapter.
2. If it does not fit, code that searches every turn recalls as well as 6.37 on outside-writer
   chats and is faster. 6.37 adds leaving in-view answers alone and fewer needless searches.
3. On very long histories (LongMemEval-S), 6.37 declines half the questions that have an answer
   (233 of 470); code declines 1.

"Base" is the untrained Tiny Aya Global. "Code" is code that searches on every turn with the
newest message as the query, then hands base the passages (nothing trained). Recall counts the
`older` (a fact told long ago) and `confirm` ("did I tell you...?") questions. A clean first call is
a reply that parses whole as one `search_corpus` call with nothing before or after it, counted of
the replies that searched; an unclean call still ran its search, so the count is a format measure.

## First: when the chat fits, give it the whole chat; and plain code recalls as well

On two sets of chats by outside writers who never saw this project's generator (about
1,400 tokens a chat), the untrained model with every message in view answers
58 and 52 of 80 questions about facts told earlier,
against 28 and 34 for this adapter with the tool and the last three
exchanges (R-164). Given the whole chat and the tool, the adapter and the untrained model show
no measured difference on every kind of message (one seed, two sets of 40 chats; gaps
under about 15 points on a kind of 40 questions are below what this test
resolves; R-142, R-165). This holds on those outside-writer chats only. On the project's generated
sealed chats of about the same length (58 messages, 1,105 to 1,332 tokens), the untrained
model with the whole chat answers 21 to 33 of 60 recall questions against this
adapter's 46 to 55 with the tool (R-168).

On the outside-writer chats, plain code that searches on every turn, with no training, recalls as
well as this adapter, both with the last three exchanges in view: 42 and
47 of 120 against 39 and 53, no measured
difference (p = 0.76 and 0.45; R-169). Base with the tool searches too little and code
searches every turn. Training adds searching when the answer is out of view (against base) and not
searching when it is in view (against code): where the answer is in view the adapter answers
35 and 37 of 40 and code 13 and
16; on facts never told 37 and 36 against
31 and 24. On plain statements it leaves 37 and
35 unsearched, below base's 38 and
39; code searches every one. On the generated sealed pools this adapter is far
above both references on recall: 44 to 55 of 60 at each of 58 and 419 messages
against code's 14 to 32 (every sign test below 0.001; R-168). The code is faster on every set:
1.01 to 1.23 s a conversation against 1.67 to 2.08 on the sealed pools, 1.45 to 1.48 s a question against 1.70 to 1.96 on the outside-writer sets.

Not measured: the untrained model reading the whole chat at 419 messages (about 6,236
tokens on `hard_dev`). Those runs ran out of card memory under the 8.50 GiB cap on a
10 GB card (R-166); every three-exchange run in the sealed run peaked at 6.71 to 7.02 GiB
of card memory at inference (R-163).

## Results with only the last three exchanges in view

- **Outside-writer sets** (40 chats each, written blind to the generator): recall
  39 and 53 of 120 against the untrained model's
  26 and 27 (gain +2.5 to +19.2 and +13.3 to +30.0 points, 95%
  intervals resampling chats; set 1's p = 0.047 is above the registered 0.01) (R-146, R-157).
  The gain is on direct questions; on "..., right?" questions with a false claim it corrects
  1 and 3 of 20 and goes along with
  the rest (R-164).
- **The shipped seed is not the strongest.** Seed 82 is the lowest of the eight training seeds on
  the first outside-writer set, on sealed conditions C and D, and on `hard_dev`; the eight seeds
  pooled gain +18.0 and +20.8 points on the two sets
  (+9.7 to +26.1 and +12.9 to +28.3) (R-141, R-146, R-157, R-163).
- **Who wrote and judged the tests.** The outside writers are 4 fresh Claude Opus agents
  a set; the coherence judges are Claude Sonnet agents only, never checked against a person.
- **The registered sealed test** (R-162, R-163): two generator-built pools, one and four decoys a
  chat, the untrained model and all eight training seeds run once. Every registered rule passes in
  all four conditions. Recall pooled over the eight seeds is 85.2 to 90.4% against the
  untrained model's 8.3 to 28.3% (60 to 82 points; registered rule met, p below
  0.01); this seed gets 91 to 107 of 120 against 13 to 32.
  Every right answer came from a search that found the fact; no seed made more false retrievals than
  the untrained model; every seed was judged coherent more often by all three judges.
- **LongMemEval-S, an outside check** (R-170): a third kind of chat, user-to-assistant chats, partly
  real logs and partly model-simulated, never pooled with the sets above. The adapter's system
  prompt ("You are chatting with a friend") does not fit them. Every arm answers few questions.
  This adapter finds the evidence more often than the untrained model with the tool only because it
  searches more often; code that always searches finds it more often still (372
  against 333 of 476), with no measured difference in gold answers
  (63 against 51 of 411), and is faster. The adapter
  declines 21 of all 30 unanswerable questions, and also
  233 of all 470 answerable ones. Judged with LongMemEval's prompts
  by Claude judges (not the official score, which uses GPT-4o): 53 of 248
  right, against 34 for the untrained model with the tool and 40 for code.
  Split after reading, on the 233 answerable questions it ties code and shows
  no measured difference from the untrained model (40 against 32, p = 0.29); 11
  of its 19-question lead come from the 15 unanswerable ones. My blind
  check of 50 lines (the author, not an independent marker) agrees with each judge on
  46 of 50 (kappa 0.78).

## How to use it

When the chat is short enough to show whole, show it the whole chat; the tool can stay in the
prompt (R-165). This was measured on the outside-writer chats, of about 1,400 tokens;
on the generated chats the untrained model with the whole chat was far below this adapter with the
tool (R-168), and this adapter with the whole chat was not run there. Whole chats near the model's
8,192-token limit were not measured.
When it does not, use the harness the adapter was trained in: a system prompt that describes the
`search_corpus` tool (`aya_retrieval.tool_prompt.system_prompt_with_tools`), the last three
exchanges as chat turns, and the earlier exchanges indexed for search, one passage per exchange.
`run_turn` in `src/aya_retrieval/harness.py` runs that loop: up to 3 searches a
message, top 5 passages each. Decoding in every test was greedy.

## Limitations

- On the short outside-writer chats the whole chat beats the three-exchange view with search,
  and plain code that searches every turn recalls as well as this adapter and is faster (above).
  The adapter's recall gain over plain code is shown on the generated sealed pools only (R-168).
- On LongMemEval-S it declines 233 of 470 questions it should
  answer, and every arm answers few (R-170). Replies are capped at 60 tokens in every
  test, and the longest LongMemEval-S views run out of memory on a 10 GB card.
- It goes along with most false claims in tag questions ("..., right?").
- When the friend is just chatting it should not search; on the outside-writer sets it searched
  3 and 5 of 40 such lines, more than
  base (2 and 1) on both sets (R-146, R-157).
- The scorer does not catch an invented value on `never_told`. When a fact was never told the
  adapter should decline, and the scorer passes any reply that names none of the listed values, so
  a reply that invents a value outside the list still passes (R-020). The scorer was checked by
  hand on 50 lines from development pools: I (the author, not an independent marker)
  agreed with it on 47 and an independent second marker on
  48 (R-144, R-145).
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

1,094 rows (`older` 332, `confirm` 230, `in_view` 150, `never_told` 160, `statement` 222), built from the training pool only: targets are the
untrained model's own replies where they pass the scorer, vetted plain-chat replies, and scripted
answers where needed. LoRA rank 32 on `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`; peak learning rate 3e-4, 3 epochs, batch 2, loss mode `chat_decision`, with TRL's chunked loss replaced by `lean_loss.lean_chunk`; trained from no adapter; 222 plain-chat rows carry loss only on the reply's first token and its end-of-turn marker. Trained with AgentTune; 33 to 35 minutes a seed
on an RTX 3080, with a training peak of 7.81 to 7.84 GiB of card memory. The method, the
registered tests, every candidate tried, the errors found and every results file are in the
repository,
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval):
`docs/ARTICLE.md` and `RECORDS.md`.

## Authors

Kevin Vaillancourt, working with an AI assistant (Claude, Anthropic) as an executive-function
accommodation. Built for the Lexsi AI Safety and Alignment Hackathon 2026, Track 3.
