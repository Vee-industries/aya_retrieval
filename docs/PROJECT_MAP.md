# Project map

Created 2026-11-13 (R-216), when the SOP check found the project had none. What each part does, how the parts
connect, and what each stage changes. `RECORDS.md` holds every decision and number; this file only says where things
are.

## What the project is

A LoRA adapter on Tiny Aya Global that searches its own chat history with a keyword tool (AgentTune's
`search_corpus`, SQLite FTS, OR search, top 5) and answers with the stored fact, or says it was not told. Lexsi
hackathon, Track 3. Submitted as 6.37 (R-172). Reopened from R-179 to fix the demo weakness (answering never-told
questions from unrelated passages, copying wrong answers).

## Parts

| Part | What it does |
|---|---|
| `src/aya_retrieval/` | The library: `pools.py` (fact templates and the training pool; never read past line 451), `conversations.py` (row kinds), `recall_tool.py` (the search tool over exchanges), `chat.py` and `tool_prompt.py` (system prompt), `harness.py`, `inference.py`, `scoring.py`, `stress.py` (eval), `provenance.py` (run metadata in every result file) |
| `scripts/run_recall_train.py` | Trains one adapter from a training set (`--data`), one seed |
| `scripts/run_recall_eval.py` | Scores an adapter on a pool (`hard_dev`, `probe`), an items folder (`blind_dev`, `blind_dev2`) or a stress kind; writes `results/recall_eval/LABEL_seed_N.json` |
| `scripts/run_demo2.py` | Demo2: one fresh writer's chat (`demo2/`), 24 messages and 12 questions, base then each adapter |
| `scripts/records/build_*.py` | Training-set builds, one per candidate (K1, K1.3, K3 to K4.9); each writes `data/screens/NAME.jsonl` and its `.provenance.json` |
| `scripts/records/check_k3.py --set NAME` | The set checker (R-205 lines and later ones) before any training |
| `scripts/records/decide_r191.py` | Screening of every candidate against base and 6.37, and the registered pick (R-191, R-192) |
| `scripts/records/demo2_judges.py` | Blind judge sheet and tally for a Demo2 run |
| `scripts/records/validate_k3_writers.py` | Structure check of K3-brief writer files |
| `scripts/records/build_onpolicy_items.py`, `build_onpolicy_rows.py` | On-policy tries (R-253 to R-270): K4.8's training chats as 375 eval items (`data/onpolicy/items/`), then one seed's stage set from a model's own mistakes on them (start `k13`, `t6` or `op`; `op4` builds second-search rows from OP's eval, R-267) |
| `scripts/records/demo_contamination.py` | Checks a demo's answer keys against every training value and six-word run (R-254); Demo4 and Demo5 replaced Demo2 and Demo3 |
| `docs/k3/`, `docs/k4/`, `docs/k4_4/`, `docs/k4_9/` | Writer briefs for the natural training chats and questions |
| `data/screens/` | Training sets and writer files; `k4_5/`, `k4_6/`, `k4_7/` hold each chain's stripped writer copies and intermediates |
| `results/recall_eval/` | Every eval result; `results/demo2/` Demo2 runs and judge folders; `results/panels/R-NNN/` panel and count outputs |
| Sealed | `data/heldout*`, `data/*independent*`, S3 chats, `results/longmemeval/`: not opened before the sealed run; never uploaded |

## How a candidate runs

1. A build script makes the set; `check_k3.py` must report 0 FAIL.
2. A queue (`qNNN.sh` under the card lock, in the session's scratchpad) trains seed 82, runs Demo2 at once, and is
   stopped if Demo2 bombs (fewer than 3 of 6 older or 3 of 4 never-told by the two-judge rule; Kevin keeps this gate).
3. Otherwise it scores seed 82 (screen, hard_dev, probe, stresses, outside-writer sets), trains and scores 83, then 94.
4. `decide_r191.py` gives each candidate's lines and the shippable pick.
5. The pick runs the sealed S3 once (`qs3.sh PICK`), Saturday 19:00 at the latest (R-194, R-202).

## Candidate chain (K4.x)

Each builds on the one before; `RECORDS.md` R-205 to R-215 has the reasons and numbers.

K3 natural writer rows, then K3.1 (drops), K3.2 (check_false share), K4.1 (near-miss and contrast rows), K4.2 and
K4.3 (declines after empty searches), K4.4 (wrong-person rows), K4.5 (possessives out of every query, chain rebuilt
by `build_k4_5.py`), K4.6 (never-told rows search twice when both return text), K4.7 (64 more natural chats), K4.8 (near-miss and
wrong-person questions for those 64 chats). K4.6e2 is K4.6 read at its epoch-2 checkpoint (R-219); K4.8 is read at
R-222's checkpoint rule (Demo2 on epoch 3 and epoch 2, epoch 3 read if it passes). K4.9 (R-224) is K4.8 plus 27
miss-then-hit rows marked `loss_from_second_call`: the trainer keeps their first search call out of the loss (R-223).
