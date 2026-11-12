# Shared text for every write-up (one source; builders copy numbers exactly, may adjust layout)

All numbers checked in lane_sources.md section 1 or by the orchestrator against docs/ARTICLE.md section 6
(lines 399 to 404). Seed 82 is the shipped adapter, 6.37. "Code" = code that searches on every turn with the newest
message as the query, then hands base the passages (nothing trained). "Base" = the untrained Tiny Aya Global.
"Tool" = the full-text search tool over messages older than the last three exchanges.

## Lead (first paragraph of HF_ARTICLE, README, MODEL_CARD, ABSTRACT; wording may be tightened, not the facts)

Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya Global (3.35B), shown only the last three
exchanges of a chat, search the rest when the answer is out of view. On the sealed test (300 unseen generated chats
in each of four conditions, run once), the shipped seed recalls 91 to 107 of 120 facts; the untrained model with
the same tool recalls 13 to 32. On chats from outside writers (written by Claude Opus agents, about 1,400 tokens),
the untrained model shown the whole chat does best (71 and 65 of 120), and code that searches every turn recalls as
well as 6.37 (42 and 47 against 39 and 53) and runs faster. There, training's measured gain is when to search:
6.37 searches for facts out of view, which base rarely does, and leaves answers already in view alone (35 and 37 of
40 right), where code searches every turn (13 and 16).

## Results at a glance (table)

Outside-writer chats, two sets (set 1 / set 2), one run each:

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
| Recall, of 60, sealed pools after the run (R-168) | builder: fill from results/analysis/R-168/refs.json if base-with-tool is there, else "see the row above" | 14 to 32 | 21 to 33 (58 messages only; 419 messages does not fit 10 GB) | 44 to 55 (46 to 55 at 58 messages) |
| Right search decisions, of 300 (sealed) | 180, 193 | not run | not run | 298, 296 |
| Clean first calls (sealed; of the turns that searched; format only, unclean calls still ran) | 52 of 136, 49 of 107 | scripted | no tool | 180 of 180, 184 of 184 |

LongMemEval-S (500 questions; history about 115,000 tokens, so no whole-chat arm fits; judged by three Claude
Sonnet judges with LongMemEval's prompts, not the official GPT-4o judge):

| Measure | Base, tool | Code | 6.37, tool |
|---|---|---|---|
| Judged right, of 248 judged | 34 | 40 | 53 (p = 0.014 against base, 0.12 against code) |
| Of those, answerable, of 233 | 32 | 40 | 40 (p = 0.29 against base) |
| Declines on answerable, of all 470 | 22 | 1 | 233 |
| Declines on unanswerable, of all 30 | 2 | 0 | 21 |
| Gold answer in reply, of 411 (mechanical) | 51 | 63 | 51 |
| Clean first calls (of questions that searched) | 146 of 328 | scripted | 441 of 441 |
| Seconds a question | 3.47 | 3.09 | 3.81 |

## Which to use when (three lines)
1. If the whole chat fits in the context, show it whole: base with the whole chat recalls best on outside-writer
   chats, and needs no adapter.
2. If it does not fit, code that searches every turn recalls as well as 6.37 on outside-writer chats and is faster.
   6.37 adds leaving in-view answers alone and fewer needless searches.
3. On very long histories (LongMemEval-S), 6.37 declines half the questions that have an answer (233 of 470);
   code declines 1.

## Terms (glossary, define at first use)
base; code; tool; recall (`older` and `confirm` questions); in view; never told; statement; seed 82 (= 6.37, the
shipped seed of eight); sealed test; outside-writer sets (set 1 became a development set when 7 was designed from
its failures; set 2 was read by no decision that changed 6.37); judge 1 (three judges mark each reply; judge 1's
mark is the score, the other two are reported); clean call (above).

## Toolkits (one table)
| Toolkit | What it did | Ran on 6.37? |
|---|---|---|
| AgentTune | Trained every adapter (supervised LoRA) | Yes |
| CuratorKIT | Its grounding gate audited v6's 350 found-fact training answers and rejected 22; the replacements it passed are in 6.37's lineage | On an ancestor set only |
| AuditKIT | Second scorer in development: agreed 959 of 960 on v3; its paired bootstrap does not centre resamples (project's proposed one-line fix, not adopted upstream) | No |

## Access
Adapter and both datasets are public and un-gated (checked 2026-11-12, no login). The base model
CohereLabs/tiny-aya-global is gated: accept its licence on Hugging Face first.
