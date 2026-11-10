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
searched 3 and 5 of 40 such lines,
more than base (2 and 1) on both sets (R-146,
R-157).

Final numbers for the shipped model, 6.37 (`fix17cs37` seed 82, frozen in R-160): the sealed final run (registered in R-162, results in R-163), the outside-writer sets (R-146, R-157), the whole-chat control (R-164, R-165), R-016's two references run late (R-168, R-169) and LongMemEval-S as an outside check (R-170). Every number is computed from committed results files by `scripts/make_article.py`.

## First: when the chat fits, give it the whole chat; and plain code recalls as well

On two sets of chats by outside writers who never saw this project's generator (about
1,400 tokens a chat), the untrained model with every message in view answers
58 and 52 of 80 questions about facts told earlier,
against 28 and 34 for this adapter with the tool and the last three
exchanges (R-164). Given the whole chat and the tool, the adapter and the untrained model show
no measured difference (one seed, two sets of 40 chats; gaps under about 15 points on a kind of 40 questions are below what this test resolves, R-142) on every kind of message
(R-165). This holds on those outside-writer chats only. On the project's generated sealed chats
of about the same length (58 messages, 1,105 to 1,332 tokens), the untrained model with the
whole chat answers 21 to 33 of 60 recall questions against this adapter's
46 to 55 with the tool (R-168).

On the outside-writer chats, plain code that searches on every turn, with no training, recalls as
well as this adapter, both with the last three exchanges in view: 42 and
47 of 120 against 39 and 53, no measured
difference (p = 0.76 and 0.45; R-169). What training adds there is deciding when not to
search: where the answer is in view the adapter answers 35 and 37 of
40 and code 13 and 16; on facts never told
37 and 36 against 31 and
24; and it leaves 37 and 35 plain statements
unsearched, where code searches every one. On the generated sealed pools this adapter is far above
both references on recall, at 58 and 419 messages: 44 to 55 of 60 against
code's 14 to 32 (sign test p at most 3.2 × 10<sup>-4</sup>; R-168). The code is faster on every set:
1.01 to 1.23 s a conversation against 1.67 to 2.08 on the sealed pools, 1.45 to 1.48 s a question against 1.70 to 1.96 on the outside-writer sets.

Not measured: the untrained model reading the whole chat at 419 messages (about 6,236
tokens on `hard_dev`). Those runs ran out of card memory under the 8.50 GiB cap on a
10 GB card (R-166); every three-exchange run in the sealed run peaked at 6.71 to 7.02 GiB
(R-163).

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
  declines 21 of the 30 unanswerable questions, and also
  233 of the 470 answerable ones. Judged with LongMemEval's prompts
  by Claude judges (not the official score, which uses GPT-4o): 53 of 248
  right, against 34 for the untrained model with the tool and 40 for code.
  Split after reading, on the 233 answerable questions it ties code and shows
  no measured difference from the untrained model (40 against 32, p = 0.29); 11
  of its 19-question lead come from the 15 unanswerable ones. Kevin's
  blind check of 50 lines agrees with each judge on 46 of 50 (kappa 0.78).

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
  and plain code that searches every turn recalls as well as this adapter (above). The
  adapter's recall gain over plain code is shown on the generated sealed pools only (R-168).
- On LongMemEval-S it declines 233 of 470 questions it should
  answer, and every arm answers few (R-170). Replies are capped at 60 tokens in every
  test, and the longest LongMemEval-S views run out of memory on a 10 GB card.
- It goes along with most false claims in tag questions ("..., right?").
- Its commonest misses: a search that misses the fact (including facts told with a pronoun), and a
  found fact answered from the line's first clause, leaving out the detail asked for.
- English only. Tested on generated and agent-written chats, and on LongMemEval-S, whose chats
  mix real logs of people talking to an assistant with model-simulated sessions (the sessions
  holding the answers were simulated).
- Coherence was judged by Claude models only, never checked against a person. The LongMemEval-S
  judges are Claude, not the official GPT-4o, and Kevin checked 50 of their lines.
- Licence: Tiny Aya is CC-BY-NC-4.0 and this adapter, trained from it, carries that licence.

## Training

1,094 rows (`older` 332, `confirm` 230, `in_view` 150, `never_told` 160, `statement` 222), built from the training pool only: targets are the
untrained model's own replies where they pass the scorer, vetted plain-chat replies, and scripted
answers where needed. LoRA rank 32 on `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`; peak learning rate 3e-4, 3 epochs, batch 2, loss mode `chat_decision`, with TRL's chunked loss replaced by `lean_loss.lean_chunk`; trained from no adapter; 222 plain-chat rows carry loss only on the reply's first token and its end-of-turn marker. The method, the registered tests, every candidate tried,
the errors found and every results file are in the repository,
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval): `docs/ARTICLE.md` and `RECORDS.md`.

## Authors

Kevin Vaillancourt, working with an AI assistant (Claude, Anthropic) as an executive-function
accommodation. Built for the Lexsi AI Safety and Alignment Hackathon 2026, Track 3.
