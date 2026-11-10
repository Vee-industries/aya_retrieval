# aya_retrieval

**Teaching a small open model to remember a long chat it can no longer see.** Tiny Aya Global
(3.35B) is trained with LoRA to search the earlier conversation when, and only when, the answer is
out of view, to read what comes back, and to answer in its own voice, while staying as coherent as
the untrained model. The write-up is [`docs/ARTICLE.md`](docs/ARTICLE.md).

Built for the [Lexsi AI Safety and Alignment Hackathon](https://hackathon.lexsi.ai) (1–14 November
2026), Track 3, Agentic Fine-tuning. Author: Kevin Vaillancourt, working with an AI assistant
(Claude) as an executive-function accommodation.

> **Status: sealed final run done, every registered rule passes.** The shipped adapter is 6.37
> (`fix17cs37`, seed 82), frozen on 9 November (RECORDS R-160) with the scorer and judge
> (`results/freeze/sealed_manifest.json`, R-154). On the sealed run (R-162, results R-163), base and
> all eight 6.37 seeds ran on 300 unseen conversations in each of four conditions (`heldout` and
> `independent` pools, one or four decoy facts a chat). The adapters' recall is 85 to 90% against
> base's 8 to 28%. Every right answer came from a search that found the fact. Each adapter made no
> more false retrievals than base, and was judged coherent more often than base by all three judges.
> Seed 82 alone gets 91 to 107 of 120 recall questions against base's 13 to 32
> (`results/analysis/R-162/`). The write-up and model card in `docs/` are built from these results
> and R-164 to R-166 by `scripts/make_article.py`; they do not yet include R-168 to R-170, which
> this README does. [`RECORDS.md`](RECORDS.md) is the dated log of every decision, run
> and result, each marked PRE-SPRINT or SPRINT. [`STANDARD.md`](STANDARD.md) is the standard this
> repository is built to.

## When the chat fits: give it the whole chat

The tests above show the model only the last three exchanges, as a stand-in for a chat too long to
show. When a chat is short enough to show whole, that is the better choice. On the outside-writer
sets (chats of about 1,400 tokens), base with every message in view answers 58 and 52 of 80 `older`
questions, against 28 and 34 for 6.37 seed 82 with the tool and the last three exchanges (R-164).
Given the whole chat and the tool, 6.37 shows no measured difference from base given the whole chat,
on any kind, on both sets (R-165). That is one seed and two sets of 40 chats, so gaps under about
15 points on a kind of 40 questions could not be seen (R-142). So the design this supports is to
show the trained model the whole chat when it fits, and let it search when it does not: no measured
loss against base when the chat fits, and much better than base once only part of the chat can be
shown. The whole-chat result holds on chats people write, not on this project's generated chats:
on the sealed pools, base with the whole chat got 21 to 33 of 60 recall questions against seed 82's
46 to 55 (R-168).

**Code that searches every turn, with no training,** was registered as a reference in R-016 and run
late (R-167). On chats people write it recalls as well as 6.37 (42 and 47 of 120 against 39 and 53;
p = 0.76 and 0.45, R-169). What training adds there is deciding when not to search: answers already
on screen 35 and 37 of 40 against code's 13 and 16; facts never told 37 and 36 against 31 and 24;
plain statements 37 and 35 against 0. On the generated sealed pools the adapters are also far above
code on recall (seed 82 44 to 55 of 60 against 14 to 32, R-168). The code is faster: 1.0 to 1.2 s a
conversation against 1.7 to 2.1 s (R-169).

What is not measured: base with the whole chat at 419 messages (about 6,200 tokens). Those runs
ran out of card memory under the 8.5 GiB cap on a 10 GB card (R-166, log in
`results/control/R-164/`); every three-exchange run in the sealed run peaked at 6.7 to 7.0 GiB
(R-163). Tiny Aya's limit is 8,192 tokens, and most of its layers attend to the last 4,096 (its
`config.json`). The only whole-chat readings at that length are R-014's (1 of 20 and 1 of 20,
ruled invalid for repeated small talk) and R-017's (0 of 12 `older` questions), both on the
training pool, uncapped.

## Outside check: LongMemEval-S

A third kind of chat: LongMemEval-S (Wu et al., ICLR 2025), 500 questions, each over its own
user-to-assistant history of about 115,000 tokens, partly real logs and partly model-simulated (R-170).
Every arm sees the last three exchanges. This is a mechanical score, not the official one (that uses
a GPT-4o judge), and it is never pooled with the other sets. Of 476 questions with marked evidence,
counting a failure or no search as not found:

| | 6.37 seed 82, tool | base, tool | code always searches | base, three exchanges |
|---|---|---|---|---|
| evidence found by the first search (of 476) | 333 | 238 | 372 | — |
| gold answer in the reply (of 411 read) | 51 | 51 | 63 | 34 |
| declines on the 30 unanswerable | 21 | 2 | 0 | 10 |
| declines on the 470 answerable | 233 | 22 | 1 | 140 |
| seconds a question | 3.81 | 3.47 | 3.09 | 2.09 |

- 6.37 finds evidence more often than base with the tool (p below 0.000001) only because it searches
  more often: on the 294 questions both searched, each found it on 226.
- Code that always searches finds evidence more often than 6.37 (372 against 333, p = 0.0004) and is
  faster. Gold answers in the reply show no measured difference (63 against 51, p = 0.20).
- 6.37 declines far more than base: on 21 of the 30 questions that should be declined, and on 233 of
  the 470 that should be answered.
- Every arm that ran all 500 answers few (8 to 16%). Base reading only the evidence sessions gets 63 of 114 on
  the short questions it can fit. Judged accuracy, R-170's measure 4, is not yet read.

Each arm's questions that ran out of card memory at 8.5 GiB were rerun once at 9.0 GiB, as amended
before any score: failures 21, 31, 58 and 8 fell to 10, 16, 28 and 3 (`results/analysis/R-170/scores.json`).

## Pools

Conversations are built from pools of people, relations, fact types and small talk
(`src/aya_retrieval/pools.py`, with `pool_wide.py`, `pool_hard_dev.py` and `pool_independent.py`).
No two pools share any content; tests enforce it.

| Pool | Written by | Used for |
|---|---|---|
| `train` | Claude | training |
| `wide` | a fresh agent, from a brief | training experiments with 47 new fact types (R-069 to R-073) |
| `probe` | Claude | development screens and confirmations |
| `heldout` | Claude | the registered final test only; run once, 9 November (R-162, R-163) |
| `independent` | a fresh agent, from a brief | the registered final test only; run once, 9 November (R-162, R-163); never read |
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
| `data/blind_dev2/` | R-152, R-157 | the test for the 7.x candidates (R-151, R-156); read as a report on 6.37 once none was left (R-157) |

## Known limits

The holes a reviewer will look for first, each measured and recorded where it was found:

- **On short chats the whole chat beats the tool.** See the section above. R-016 registered
  `whole_chat` and `always_search` as references to report beside the rules; the sealed run
  (R-162) ran neither, and that omission was not disclosed until R-167. The whole-chat reference
  was run afterwards, on the outside-writer sets only (R-164, R-165).

- **Few templates behind the generated sets.** The 96 recall questions per run come from only 5 fact
  templates on `probe` and 8 on `hard_dev`, so item-level p-values overstate the evidence. Intervals
  that resample whole templates still exclude zero (R-141).
- **The generalization numbers are the independent sets'.** On chats by writers who never saw the
  generator, 6.37 seed 82 gets recall 39 of 120 against base's 26 on the first set (+50%, sign test
  p = 0.047; whole-chat bootstrap +2.5 to +19.2 points; R-146) and 53 of 120 against 27 on the second
  (+96%, p = 0.0001; +13.3 to +30.0 points; R-157). On the generated `hard_dev` set the same adapter
  goes from 20 to 73 of 96 (+265%). The +50% and +96% are the figures to read as generalization.
  The sealed run's two pools both use this project's conversation generator, so its larger gains
  (R-163) show the result holds on unseen people, facts and small talk. They do not show it holds on
  chats with a different structure.
- **The shipped seed is not the strongest on the independent pool.** On the sealed `independent`
  pool, seed 82's `confirm` score is at the bottom of the eight seeds (42 and 40 of 60, against up
  to 60). Most of its misses there are facts it found and did not use (R-163).
- **It goes along with wrong claims in tag questions.** Asked "..., right?" about an out-of-view fact on the
  second independent set, 6.37 rarely searches (12 of 40) and corrects only 3 of the 20 false claims, so most of
  its `confirm` score is agreement with true ones. 7.1 shows the search can be trained (40 of 40, every right
  answer grounded), but it did not raise recall and cost lines on the generated pools (R-157, R-158).
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
| `scripts/records/queue/` | The gate scripts (`decide_r*.py`, `target_r*.py`), the GPU queue runner and its backlog, kept exactly as run (R-157) |
| `data/` | Training sets, the independent sets and their provenance |
| `results/` | Results files, each with its own provenance |
| `results/curator/` | CuratorKIT's grounding gate over the training answers, with each judge's verdicts (R-096, R-098) |
| `results/freeze/` | The freeze (R-154): the judge's brief, the judges' measured spread, a trial manifest, and the sealed manifest (`sealed_manifest.json`, R-160): SHA-256 hashes of the scorer, sealed pools, judge brief, human check and adapter |
| `results/analysis/R-162/` | The sealed final run scored against the registered rules, one file per condition (`scripts/records/score_r162.py`; the runs themselves are `results/recall_eval/final_*`) |
| `results/coherence/R-162/` | The sealed run's blind coherence sheets with their keys, each judge's brief, agent id, marks and wall time |
| `results/panels/` | Each panel's brief and round messages, by record; R-134's with every expert's answer |
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
