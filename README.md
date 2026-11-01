# aya_retrieval

**Training a small open model to decide when to search and what to trust.** Tiny Aya is taught to
search on real lookups and not on statements, to stop and wait for the real search result, and to
ignore instructions hidden inside the text it retrieves.

Built for the [Lexsi AI Safety and Alignment Hackathon](https://hackathon.lexsi.ai) (1–14 November
2026), Track 3, Agentic Fine-tuning. Author: Kevin Vaillancourt.

> **Status: in progress.** [`RECORDS.md`](RECORDS.md) is the dated log of every decision, run and
> result, each marked PRE-SPRINT or SPRINT. [`STANDARD.md`](STANDARD.md) is the standard this
> repository is built to.

## Prior work

The behaviours come from Latent Lab Explorer, the author's local chat engine, which enforces them
with code around a Llama model. This project asks whether they can be trained into the model's
weights instead. Nothing from that project's code or test sets is used here.

## Layout

| Path | What it holds |
|---|---|
| `src/aya_retrieval/` | The package: pinned model, tool prompt, scoring, provenance |
| `scripts/` | Entry points, one `run_*.py` per experiment; each documents its own usage |
| `data/` | Test items |
| `results/` | Results files, each with its own provenance |
| `tests/` | The test suite |

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
