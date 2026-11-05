# aya_retrieval

**Teaching a small open model to remember a long chat it can no longer see.** Tiny Aya Global
(3.35B) is trained with LoRA to search the earlier conversation when, and only when, the answer is
out of view, to read what comes back, and to answer in its own voice, while staying as coherent as
the untrained model. The write-up is [`docs/ARTICLE.md`](docs/ARTICLE.md).

Built for the [Lexsi AI Safety and Alignment Hackathon](https://hackathon.lexsi.ai) (1–14 November
2026), Track 3, Agentic Fine-tuning. Author: Kevin Vaillancourt, working with an AI assistant
(Claude) as an executive-function accommodation.

> **Status: in progress.** The current adapter is v5 (RECORDS R-061); development numbers only, until
> the registered final test runs. [`RECORDS.md`](RECORDS.md) is the dated log of every decision, run
> and result, each marked PRE-SPRINT or SPRINT. [`STANDARD.md`](STANDARD.md) is the standard this
> repository is built to.

## Pools

Conversations are built from pools of people, relations, fact types and small talk
(`src/aya_retrieval/pools.py`). No two pools share any content; tests enforce it.

| Pool | Written by | Used for |
|---|---|---|
| `train` | Claude | training |
| `probe` | Claude | development screens and confirmations |
| `heldout` | Claude | the registered final test only; sealed |
| `independent` | a fresh agent, from a brief | the registered final test only; sealed, never read |
| `hard_dev` | a second fresh agent, same brief | development: a readable twin of `independent` (R-066) |

`src/aya_retrieval/stress.py` makes any pool harder at evaluation: the user's typing style, facts
corrected later, and longer chats (R-067).

## Prior work

The behaviours come from Latent Lab Explorer, the author's local chat engine, which enforces them
with code around a Llama model. This project asks whether they can be trained into the model's
weights instead. Nothing from that project's code or test sets is used here.

## Layout

| Path | What it holds |
|---|---|
| `src/aya_retrieval/` | The package: pinned model, tool prompt, scoring, provenance |
| `scripts/` | Entry points, one `run_*.py` per experiment; each documents its own usage |
| `data/` | Training sets and their provenance |
| `results/` | Results files, each with its own provenance |
| `tests/` | The test suite |
| `demo/` | The scripted demo conversation; its transcripts are in `results/demo/` |
| `docs/` | The write-up (`ARTICLE.md`) and model card (`MODEL_CARD.md`), both made from `results/` by `scripts/make_article.py` |

## Chat with it

`scripts/run_chat.py` runs the model, with or without an adapter, in the harness it was tested in:
the last three exchanges in view, everything older reachable only by search. Each search it makes
is printed before its reply.

```bash
../venv/Scripts/python scripts/run_chat.py --adapter ../adapters/v5_seed_82 --index chat.sqlite
```

## Setup

Needs Python 3.12 and one 10 GB GPU. On Windows, match the PyTorch build to your driver.

```bash
python -m venv ../venv
../venv/Scripts/python -m pip install "torch==2.11.0+cu128" --index-url https://download.pytorch.org/whl/cu128
git clone https://github.com/Lexsi-Labs/AgentTune ../vendor/AgentTune
git clone https://github.com/Lexsi-Labs/AuditKIT ../vendor/AuditKIT
../venv/Scripts/python -m pip install -e ../vendor/AgentTune -e "../vendor/AuditKIT[transformers]" -e ".[dev]"
```

Tiny Aya is gated: accept the licence on its [model page](https://huggingface.co/CohereLabs/tiny-aya-global),
then log in to Hugging Face. The toolkit commits used are in RECORDS R-003.

## Checks

```bash
../venv/Scripts/python -m ruff check .
../venv/Scripts/python -m ruff format --check .
../venv/Scripts/python -m pytest
```

## Licences

The code here is Apache-2.0. Tiny Aya is CC-BY-NC-4.0, and anything trained from it carries that
licence. See [`NOTICE`](NOTICE).
