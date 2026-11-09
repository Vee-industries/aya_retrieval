# aya_retrieval

**Teaching a small open model to remember a long chat it can no longer see.** Tiny Aya Global
(3.35B) is trained with LoRA to search the earlier conversation when, and only when, the answer is
out of view, to read what comes back, and to answer in its own voice, while staying as coherent as
the untrained model. The write-up is [`docs/ARTICLE.md`](docs/ARTICLE.md).

Built for the [Lexsi AI Safety and Alignment Hackathon](https://hackathon.lexsi.ai) (1–14 November
2026), Track 3, Agentic Fine-tuning. Author: Kevin Vaillancourt, working with an AI assistant
(Claude) as an executive-function accommodation.

> **Status: in progress.** The shipped adapter is 6.37 (`fix17cs37`, seed 82; RECORDS R-131, R-140). One
> last candidate, 7.1 (`fix17cs71`, R-156), replaces it only if it passes every registered line before
> the model freeze on 11 November. All numbers are development numbers until the sealed final run, which
> is scored with the scorer and judge frozen with the model (R-154). The write-up and model card in
> `docs/` are drafts that still show v5's development numbers, as their banners say; they are rebuilt
> from `results/` at the freeze. [`RECORDS.md`](RECORDS.md) is the dated log of every decision, run
> and result, each marked PRE-SPRINT or SPRINT. [`STANDARD.md`](STANDARD.md) is the standard this
> repository is built to.

## Pools

Conversations are built from pools of people, relations, fact types and small talk
(`src/aya_retrieval/pools.py`, with `pool_wide.py`, `pool_hard_dev.py` and `pool_independent.py`).
No two pools share any content; tests enforce it.

| Pool | Written by | Used for |
|---|---|---|
| `train` | Claude | training |
| `wide` | a fresh agent, from a brief | training experiments with 47 new fact types (R-069 to R-073) |
| `probe` | Claude | development screens and confirmations |
| `heldout` | Claude | the registered final test only; sealed |
| `independent` | a fresh agent, from a brief | the registered final test only; sealed, never read |
| `hard_dev` | a second fresh agent, same brief | development: a readable twin of `independent` (R-066) |

`src/aya_retrieval/stress.py` makes any pool harder at evaluation: the user's typing style, facts
corrected later, and longer chats (R-067).

## Independent sets

Two sets of chats written by writers who never saw the generator, its pools or its results, to test
whether the gain survives a change of structure. Each is 40 chats from four fresh Opus agents
writing from one brief (in the set's folder), frozen by SHA-256 before anyone read a chat.

| Set | Records | Used for |
|---|---|---|
| `data/blind_dev/` | R-142, R-143, R-146 | development since R-151 (7 was designed from its failures) |
| `data/blind_dev2/` | R-152 | the test for the 7.x candidates (R-151, R-156); its results are unread until a candidate's target is computed |

## Known limits

The holes a reviewer will look for first, each measured and recorded where it was found:

- **Few templates behind the generated sets.** The 96 recall questions per run come from only 5 fact
  templates on `probe` and 8 on `hard_dev`, so item-level p-values overstate the evidence. Intervals
  that resample whole templates still exclude zero (R-141).
- **The generalization number is the independent set's.** On chats by writers who never saw the
  generator, 6.37 seed 82 gets recall 39 of 120 against base's 26 of 120 (+50%, sign test p = 0.047;
  whole-chat bootstrap +2.5 to +19.2 points; R-146). On the generated `hard_dev` set the same adapter
  goes from 20 to 73 of 96 (+265%). The +50% is the figure to read as generalization.
- **Coherence is judged by Claude models only.** Every coherence sheet is marked by fresh Claude Sonnet
  agents (three a sheet in the later gates), so their agreement is weaker evidence than agreement across
  model families (R-096 says the same of CuratorKIT's judges). Their spread is measured: R-128's three
  judges split on 13 of 576 lines (R-154). The two human
  checks (Kevin, R-144; a second marker, R-145) check the recall scorer, not coherence.
- **The judge's version and decoding cannot be set.** The judges run as Claude Code agents, which
  take a model family but no exact version or temperature; the model each judge ran on is read from
  its transcript and recorded (R-154).

## Prior work

The behaviours come from Latent Lab Explorer, the author's local chat engine, which enforces them
with code around a Llama model. This project asks whether they can be trained into the model's
weights instead. Nothing from that project's code or test sets is used here.

## Layout

| Path | What it holds |
|---|---|
| `src/aya_retrieval/` | The package: pinned model, tool prompt, scoring, provenance |
| `scripts/` | Entry points, one `run_*.py` per experiment; each documents its own usage |
| `scripts/records/` | Scripts tied to one record (building a training set, a sheet, a gate or a report), most named by that record |
| `data/` | Training sets, the independent sets and their provenance |
| `results/` | Results files, each with its own provenance |
| `results/curator/` | CuratorKIT's grounding gate over the training answers, with each judge's verdicts (R-096, R-098) |
| `results/freeze/` | The freeze (R-154): the judge's brief, the judges' measured spread, and a trial manifest of SHA-256 hashes (scorer, sealed pools, judge brief, human check, adapter); the sealed manifest is added at the model freeze |
| `results/human_check/` | The blind check of the scorer by Kevin and a second marker (R-139, R-144, R-145) |
| `tests/` | The test suite |
| `demo/` | The scripted demo conversation; its transcripts are in `results/demo/` |
| `figures/` | The write-up's figures, drawn from `results/` by `scripts/make_figures.py` |
| `docs/` | The write-up (`ARTICLE.md`) and model card (`MODEL_CARD.md`), both made from `results/` by `scripts/make_article.py` from their templates; sample rows in `docs/samples/` |

## Chat with it

`scripts/run_chat.py` runs the model, with or without an adapter, in the harness it was tested in:
the last three exchanges in view, everything older reachable only by search. Each search it makes
is printed before its reply.

```bash
../venv/Scripts/python scripts/run_chat.py --adapter ../adapters/screens/fix17cs37_82 --index chat.sqlite
```

The adapters are not in this repository and are not published yet. To train the shipped one from
scratch (about 35 minutes on an RTX 3080):

```bash
../venv/Scripts/python scripts/run_recall_train.py --seed 82 --out-dir ../adapters/screens/fix17cs37_82 --data data/screens/fix17cs37.jsonl --lora-r 32 --lora-targets q_proj k_proj v_proj o_proj gate_proj up_proj down_proj --learning-rate 3e-4 --loss-on chat_decision --max-vram-fraction 0.85
```

## Setup

Needs Python 3.12 and one 10 GB GPU. On Windows, match the PyTorch build to your driver.

```bash
python -m venv ../venv
../venv/Scripts/python -m pip install "torch==2.11.0+cu128" --index-url https://download.pytorch.org/whl/cu128
git clone https://github.com/Lexsi-Labs/AgentTune ../vendor/AgentTune
git clone https://github.com/Lexsi-Labs/AuditKIT ../vendor/AuditKIT
git clone https://github.com/Lexsi-Labs/CuratorKIT ../vendor/CuratorKIT
git -C ../vendor/AgentTune checkout d4db4c12d52342227c4113a70183d0f64aa2f345
git -C ../vendor/AuditKIT checkout 71316da345784ff220d5ed59337441a59ab31526
git -C ../vendor/CuratorKIT checkout dd9e835301fcddc74a37501d9e207a5a060d209f
../venv/Scripts/python -m pip install -e ../vendor/AgentTune -e "../vendor/AuditKIT[transformers]" -e ".[dev]"
../venv/Scripts/python -m pip install --no-deps -e ../vendor/CuratorKIT
```

The three Lexsi toolkits, at the commits recorded in RECORDS R-003: AgentTune trains, AuditKIT
re-scores recorded replies as a check on this project's scorer (`scripts/run_audit.py`), and
CuratorKIT's grounding gate checks the training answers (`scripts/run_curator_check.py`, R-096). CuratorKIT goes in with `--no-deps`, as in R-096: its core
requirements are already installed by the line before, so nothing else in the environment changes.

Tiny Aya is gated: accept the licence on its [model page](https://huggingface.co/CohereLabs/tiny-aya-global),
then log in to Hugging Face.

## Checks

```bash
../venv/Scripts/python -m ruff check .
../venv/Scripts/python -m ruff format --check .
../venv/Scripts/python -m pytest
```

## Licences

The code here is Apache-2.0. Tiny Aya is CC-BY-NC-4.0, and anything trained from it carries that
licence. See [`NOTICE`](NOTICE).
