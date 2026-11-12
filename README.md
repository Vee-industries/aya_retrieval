# aya_retrieval

Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya Global (3.35B), shown only the last three
exchanges of a chat, search the rest when the answer is out of view. On the sealed test (300 unseen generated chats
in each of four conditions, run once), the shipped seed recalls 91 to 107 of 120 facts; the untrained model with
the same tool recalls 13 to 32. On chats from outside writers (written by Claude Opus agents, about 1,400 tokens),
the untrained model shown the whole chat does best (71 and 65 of 120), and code that searches every turn recalls as
well as 6.37 (42 and 47 against 39 and 53) and runs faster. There, training's measured gain is when to search:
6.37 searches for facts out of view, which base rarely does, and leaves answers already in view alone (35 and 37 of
40 right), where code searches every turn (13 and 16).

The write-up is [`docs/ARTICLE.md`](docs/ARTICLE.md); a short version is
[on Hugging Face](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37/blob/main/ARTICLE.md) (`docs/submission/HF_ARTICLE.md`).

Built for the [Lexsi AI Safety and Alignment Hackathon](https://hackathon.lexsi.ai) (1 to 15 November
2026), Track 3, Agentic Fine-tuning. Author: Kevin Vaillancourt, working with an AI assistant
(Claude) as an executive-function accommodation.

Published on Hugging Face: the adapter
([aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37)), the training and outside-writer
chats ([aya-retrieval-chats](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-chats)) and every
evaluation log ([aya-retrieval-eval-logs](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-eval-logs)),
in two collections
([models](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-models-6af35d3c521e8481db061df5),
[datasets](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-datasets-6af35d3cf9a91556f52af373)).

**Access.** The adapter and both datasets are public and un-gated (checked 2026-11-12, no login). The base model
CohereLabs/tiny-aya-global is gated: accept its licence on Hugging Face first.

## Results at a glance

Base is the untrained Tiny Aya Global. The tool is the full-text search over messages older than the last three
exchanges. Code is code that searches on every turn with the newest message as the query, then hands base the
passages (nothing trained). 6.37 is the shipped seed, 82, of eight training seeds.

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
| Recall, of 60, sealed pools after the run (R-168) | 5 to 17 | 14 to 32 | 21 to 33 (58 messages only; 419 messages does not fit 10 GB) | 44 to 55 (46 to 55 at 58 messages) |
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

The shipped adapter is 6.37 (`fix17cs37`, seed 82), frozen on 9 November (RECORDS R-160) with the scorer and judge
(`results/freeze/sealed_manifest.json`, R-154). The sealed run is R-162, with results in R-163
(`results/analysis/R-162/`). The write-up and model card in `docs/` are built from these results and R-164 to R-170
by `scripts/make_article.py`. [`RECORDS.md`](RECORDS.md) is the dated log of every decision, run and result, each
marked PRE-SPRINT or SPRINT. [`STANDARD.md`](STANDARD.md) is the standard this repository is built to.

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

The three Lexsi toolkits, at the commits recorded in RECORDS R-003. AgentTune trained every adapter. AuditKIT served
as a second scorer in development (`scripts/run_audit.py`): it agreed with this project's scorer on 959 of 960 cases
on v3 and was not run on 6.37. CuratorKIT's grounding gate audited v6's 350 found-fact training answers and rejected
22 (`scripts/run_curator_check.py`, R-096); the replacements it passed are in 6.37's lineage, and the rest of 6.37's
1,094 rows were not gated by it. CuratorKIT goes in with `--no-deps`, as in R-096: its core requirements are already
installed by the line before, so nothing else in the environment changes.

Tiny Aya is gated: accept the licence on its [model page](https://huggingface.co/CohereLabs/tiny-aya-global),
then log in to Hugging Face.

## Chat with it

**In a browser:** [`notebooks/demo_6_37.ipynb`](notebooks/demo_6_37.ipynb)
([open in Colab](https://colab.research.google.com/github/Vee-industries/aya_retrieval/blob/main/notebooks/demo_6_37.ipynb)).
Part A prints the recorded demo runs with no login. Part B reruns base and 6.37 live on a GPU runtime (a free T4)
after you accept Tiny Aya's licence; it checks the adapter weights against the sealed manifest and marks any reply
that differs from the recorded run. Part B was tested on an RTX 3080, where all 30 replies matched the recorded
runs; it has not been run on a T4.

**Locally:** `scripts/run_chat.py` runs the model, with or without an adapter, in the harness it was tested in:
the last three exchanges in view, everything older reachable only by search. Each search it makes
is printed before its reply.

```bash
../venv/Scripts/python scripts/run_chat.py --adapter ../adapters/screens/fix17cs37_82 --index chat.sqlite
```

The shipped adapter is published at
[huggingface.co/KevinVaillancourt/aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37);
its weights' SHA-256 matches the sealed manifest (`results/freeze/sealed_manifest.json`). To fetch it:

```bash
../venv/Scripts/hf download KevinVaillancourt/aya-retrieval-6.37 --local-dir ../adapters/screens/fix17cs37_82
```

To train the shipped one from
scratch (about 35 minutes on an RTX 3080):

```bash
../venv/Scripts/python scripts/run_recall_train.py --seed 82 --out-dir ../adapters/screens/fix17cs37_82 --data data/screens/fix17cs37.jsonl --lora-r 32 --lora-targets q_proj k_proj v_proj o_proj gate_proj up_proj down_proj --learning-rate 3e-4 --loss-on chat_decision --max-vram-fraction 0.85
```

### What a chat looks like

The scripted demo (`demo/chat.txt`, 15 messages: three facts told early, then plain chat, then four questions),
run once for 6.37 and once for base, greedy, with the last three exchanges in view. Plain chat lines searched: 6.37 0 of 11, base 2 of 11. Every
turn is in [`docs/demo.md`](docs/demo.md), built by `scripts/make_demo_table.py` from the recorded runs in
`results/demo/`.

| Turn | Expected | 6.37 | Base |
|---|---|---|---|
| 10 | Thursdays (turn 1) | right | wrong: says it has no access |
| 11 | Halifax (turn 5) | right | wrong: says it has no access |
| 12 | never told | wrong: gives the Tobias fact | right |
| 14 | the leak under the kitchen sink (turn 3) | wrong: gives the pottery fact | close guess: says a leaky faucet, with turn 3 out of view and no search |

On the two questions 6.37 gets wrong it searched with queries copied from its training set: `brother new job` and
`sister broke skiing injury` each appear in 3 rows of `data/screens/fix17cs37.jsonl`. The earlier adapters v5 and
fix 15 searched `brother new job` on both turns too, then declined:

| Turn | Adapter | Search | Reply | Grade |
|---|---|---|---|---|
| 12 | v5 | `brother new job` | I don't have that from you. What is it? | right: declines |
| 12 | fix 15 | `brother new job` | I don't have that from you. What is it? | right: declines |
| 14 | v5 | `brother new job` | I don't have that from you. What is it? | wrong: declines |
| 14 | fix 15 | `brother new job` | I don't have that from you. What is it? | wrong: declines |

I wrote `demo/chat.txt` on 2026-11-04 (commit 723da40), before 6.37 was trained (2026-11-08), but it was visible
during development (R-076 logged earlier adapters failing turn 14), and three training rows hold a different pottery
fact. I ran this demo once for 6.37 and once for base on 2026-11-12 at 05:05 Eastern, read the result, and only then
registered it (R-175); the decision to publish it whole came after the run. It is shown whole, as run, with no rerun
of 6.37 and no change to the script. Base's run matches its earlier run (2026-11-05) on all 15 turns. Four questions
are an illustration, not a measurement; the measurements are the sealed run and the outside-writer sets.

<details>
<summary>All 15 turns, both models</summary>

| Turn | Message | 6.37 search | 6.37 reply | Base search | Base reply |
|---|---|---|---|---|---|
| 1 | hey, long day. my sister Marisol just started a pottery class on thursdays | none | That sounds like a wonderful class! | `Tips for beginners in pottery classes` | Hey! No results found for tips for beginners in pottery classes. Maybe you could ask about general advice for pottery classes or Marisol's class specifically? |
| 2 | she says the teacher is very strict about centring the clay | none | That might be a bit of a challenge, but it's a great way to ensure that your pottery pieces are well-balanced and stable. Centering the clay is an important technique in pottery, as it helps to create a strong foundation for your work. | `how to center clay in pottery class` | It sounds like Marisol's pottery teacher is emphasizing proper technique, which is important for shaping and firing clay. Centering the clay is a fundamental skill that helps create balanced and aesthetically pleasing pottery. If you're new to pottery, you might want to practice centring your clay before starting your projects. This |
| 3 | anyway i finally fixed the leak under the kitchen sink | none | That's great news! Leaks can be a real pain, especially when you're trying to get things done around the house. | none | That's great news! Fixing a leak under the kitchen sink is a big job, and I'm glad you were able to get it sorted. If you need any more tips or advice on home repairs or maintenance, feel free to ask. |
| 4 | took three trips to the hardware store but it's done | none | That sounds like a bit of a journey. | none | That's impressive! It sounds like you were quite determined to find the right solution. If you need any more help with anything else, just let me know. |
| 5 | my neighbour Tobias is moving to Halifax next month | none | That sounds like a big move. Halifax is a beautiful city with a lot of history and culture. | none | That's exciting! Halifax is a great city with a lot to offer. If you need any recommendations or tips for newcomers, feel free to ask. |
| 6 | he's been here eleven years so it's a big change for the street | none | It sounds like Tobias is making a big change in his life. Moving to a new city can be a big decision, and it's great that he's taking the time to think about it. | none | Eleven years is a significant amount of time, and it's understandable that the street would notice a change. If you want to make a good impression on Tobias, you could consider a friendly welcome or a small gesture to show you're excited for him. |
| 7 | been reading a lot lately, mostly old detective novels | none | That sounds like a great way to spend your free time. Detective novels can be a fun and engaging read, and it's great that you're enjoying them. | none | Old detective novels are a classic choice! They often have rich characters, intricate plots, and a sense of mystery that can be really engaging. If you're into that genre, you might enjoy authors like Agatha Christie, Arthur Conan Doyle, or Dashiell Hammett. What kind of |
| 8 | the weather has been grey all week | none | That sounds like a bit of a struggle. Grey weather can be a bit of a drag, but it's always nice to have a bit of a break from it. | none | Grey weather can be a bit of a drag, but it also sets a cozy mood for reading. If you're into detective novels, you might enjoy the atmosphere of a stormy night or a rainy evening, which often adds to the tension in these stories. If you need a change of scenery, you |
| 9 | thinking of making soup tonight | none | That sounds like a great meal. Soup can be a comforting and delicious dish, and it's always nice to have a warm and hearty meal on a grey day. | none | Soup sounds like a great idea for a cozy evening! If you're in the mood for something comforting, you might enjoy a classic beef stew or a creamy vegetable soup. If you need some inspiration, you could try a recipe like "Beef Stew with Potatoes and Carrots" or |
| 10 | what day is Marisol's pottery class again | `Marisol pottery class` | Your sister Marisol's pottery class is on Thursdays. | none | I don't have access to real-time information, including your personal schedule or class reminders. However, if you're trying to remember when Marisol's pottery class is, you might want to check your calendar, a shared planner, or ask Marisol directly. If you're looking for a reminder, you could set |
| 11 | where is Tobias moving to | `Tobias moving city` | Your neighbour Tobias is moving to Halifax next month. | none | I don't have access to real-time information, including personal details about individuals like their moving plans. If you're trying to remember where Tobias is moving to, you might want to check with him directly or look for updates on social media or other communication channels. If you're looking for a reminder, you could set |
| 12 | did i ever tell you what my brother does for work | `brother new job` | Your neighbour Tobias is moving to Halifax next month. | none | No, you haven't mentioned anything about your brother's job. If you'd like to share, I can help you remember or provide information about it! |
| 13 | i should really call my mum this weekend | none | That sounds like a good idea. | none | Yes, that sounds like a good idea! Calling your mom can be a great way to catch up and spend some quality time together. If you'd like, I can help you draft a message or remind you of the best time to call her. |
| 14 | what did i fix under the sink | `sister broke skiing injury` | Your sister Marisol's pottery class is on Thursdays. | none | You fixed a leaky faucet under the sink. |
| 15 | thanks, that's all for now | none | No problem! If you need anything else, feel free to ask. | none | Have a great weekend! |

</details>

## When the chat fits: give it the whole chat

The sealed test and the outside-writer runs show the model only the last three exchanges, as a stand-in for a chat
too long to show. When a chat is short enough to show whole, that is the better choice. On the outside-writer
sets (chats of about 1,400 tokens), base with every message in view answers 58 and 52 of 80 `older`
questions, against 28 and 34 for 6.37 seed 82 with the tool and the last three exchanges (R-164).
Given the whole chat and the tool, 6.37 shows no measured difference from base given the whole chat,
on any kind, on both sets (R-165). That is one seed and two sets of 40 chats, so gaps under about
15 points on a kind of 40 questions are below what this test resolves (R-142). So the design this supports is to
show the trained model the whole chat when it fits, and let it search when it does not: no measured
loss against base when the chat fits, and much better than base once only part of the chat can be
shown. The whole-chat result holds on the outside-writer chats, not on this project's generated
chats:
on the sealed pools, base with the whole chat got 21 to 33 of 60 recall questions against seed 82's
46 to 55 (R-168).

**Code that searches every turn, with no training,** was registered as a reference in R-016 and run
late (R-167). On the outside-writer chats it recalls as well as 6.37 (42 and 47 of 120 against 39 and 53;
p = 0.76 and 0.45, R-169). Base searches too little and code searches every turn. Training adds searching when the
answer is out of view (against base) and not searching when it is in view (against code): answers already on screen
35 and 37 of 40 against code's 13 and 16; facts never told 37 and 36 against 31 and 24; plain statements left
unsearched 37 and 35 against code's 0 (by construction), and below base's 38 and 39. On the generated sealed pools the adapters are also far above
code on recall (seed 82 44 to 55 of 60 against 14 to 32, R-168). The code is faster than 6.37: 1.0
to 1.2 s a conversation against 1.7 to 2.1 s on the sealed pools (R-168), and 1.45 to 1.48 s a
question against 1.70 to 1.96 s on the outside-writer sets (R-169).

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
| evidence found by the first search (of 476) | 333 | 238 | 372 | no tool |
| gold answer in the reply (of 411 read) | 51 | 51 | 63 | 34 |
| declines on the 30 unanswerable | 21 | 2 | 0 | 10 |
| declines on the 470 answerable | 233 | 22 | 1 | 140 |
| judged right, 248 judged questions (Claude judge, not official) | 53 | 34 | 40 | 13 |
| of those, the 233 answerable | 40 | 32 | 40 | 8 |
| of those, the 15 unanswerable | 13 | 2 | 0 | 5 |
| seconds a question | 3.81 | 3.47 | 3.09 | 2.09 |

- 6.37 finds evidence more often than base with the tool (p below 0.000001) only because it searches
  more often: on the 294 questions both searched, each found it on 226.
- Code that always searches finds evidence more often than 6.37 (372 against 333, p = 0.0004) and is
  faster. Gold answers in the reply show no measured difference (63 against 51, p = 0.20).
- 6.37 declines far more than base: on 21 of the 30 questions that should be declined, and on 233 of
  the 470 that should be answered.
- Every arm that ran all 500 answers few (8 to 16%). Base reading only the evidence sessions gets 63 of 114 on
  the short questions it can fit.
- **Judged accuracy** (LongMemEval's own judge prompts, three Claude Sonnet judges, labelled not the official score):
  6.37 53 of 248 against base with the tool 34 (p = 0.014) and code that always searches 40 (p = 0.12, no
  measured difference). Of its 19-question lead over base, 11 come from the 15 unanswerable questions (13
  against 2; code 0). On the 233 answerable ones it ties code (40 and 40) and shows no measured difference
  from base (40 against 32, p = 0.29). The split into answerable and unanswerable questions was not registered; it
  was added after I read the registered result and is disclosed as such (R-170). The judges agree on 1,027 to 1,030
  of 1,035 lines; I (the author) agree with each on 46 of my 50 blind lines (kappa 0.78). Where I differ: on an
  unanswerable question I count a reply that cannot answer because it is a language model as a failure; the judge
  prompt counts it right. Only base with three exchanges gives such replies among the judged-right lines (4 of its
  5), so my rule would change no comparison with 6.37 (R-170).

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
| `data/blind_dev/` | R-142, R-143, R-146 | a development set since R-151, when candidate 7 was designed from 6.37's failures on it |
| `data/blind_dev2/` | R-152, R-157 | the test set for the 7.x candidates (R-151, R-156); no 7.x candidate passed, so its 6.37 run became a report on the shipped adapter, read by no decision that changed 6.37 (R-157) |

## Known limits

The holes a reviewer will look for first, each measured and recorded where it was found:

- **On short chats the whole chat beats the tool.** See the section above. R-016 registered
  `whole_chat` and `always_search` as references to report beside the rules; the sealed run
  (R-162) ran neither, and that omission was not disclosed until R-167. Both were run afterwards: the whole chat on
  the outside-writer sets (R-164, R-165) and, at 58 messages only, on the sealed pools; code on both (R-168, R-169).

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
- **It reuses training queries on the demo.** On the scripted demo (`demo/chat.txt`, run 2026-11-12, greedy), 6.37
  searched on two of its four questions with queries copied from its training set ("brother new job" and "sister
  broke skiing injury", each in 3 rows of `data/screens/fix17cs37.jsonl`) and answered both with an unrelated stored
  fact. The earlier adapters v5 and fix 15 declined on those two turns.
- **Coherence is judged by Claude models only.** Every coherence sheet is marked by fresh Claude Sonnet
  agents (three a sheet in the later gates), so their agreement is weaker evidence than agreement across
  model families (R-096 says the same of CuratorKIT's judges). Their spread is measured: R-128's three
  judges split on 13 of 576 lines (R-154). The two human checks (I, the author, R-144; a second, independent
  marker, R-145) check the recall scorer, not coherence, on 50 lines from the development pools `probe` and
  `hard_dev`, not from the sealed or outside-writer chats.
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
| `results/curator/` | CuratorKIT's grounding gate over v6's 350 found-fact training answers, with each judge's verdicts (R-096, R-098) |
| `results/freeze/` | The freeze (R-154): the judge's brief, the judges' measured spread, a trial manifest, and the sealed manifest (`sealed_manifest.json`, R-160): SHA-256 hashes of the scorer, sealed pools, judge brief, human check and adapter |
| `results/analysis/R-162/` | The sealed final run scored against the registered rules, one file per condition (`scripts/records/score_r162.py`; the runs themselves are `results/recall_eval/final_*`) |
| `results/coherence/R-162/` | The sealed run's blind coherence sheets with their keys, each judge's brief, agent id, marks and wall time |
| `results/panels/` | Each panel's brief and round messages, by record; R-134's with every expert's answer |
| `results/human_check/` | The blind check of the scorer by me (the author) and a second, independent marker (R-139, R-144, R-145) |
| `tests/` | The test suite |
| `demo/` | The scripted demo conversation; its transcripts are in `results/demo/`, every turn in `docs/demo.md` (`scripts/make_demo_table.py`, R-175) |
| `.github/workflows/` | CI: lint and tests on CPU (see Checks) |
| `notebooks/` | The demo notebook (Colab); `tests/test_notebook.py` keeps its pins equal to CI's |
| `figures/` | The write-up's figures, drawn from `results/` by `scripts/make_figures.py` |
| `docs/` | The write-up (`ARTICLE.md`) and model card (`MODEL_CARD.md`), both made from `results/` by `scripts/make_article.py` from their templates; sample rows in `docs/samples/` |

## Checks

```bash
../venv/Scripts/python -m ruff check .
../venv/Scripts/python -m ruff format --check .
../venv/Scripts/python -m pytest
```

CI (`.github/workflows/ci.yml`) runs the same three on a CPU runner on every push, with AgentTune and AuditKIT at
the commits every result was made with and no model weights. `tests/test_inference.py` needs Tiny Aya's gated
tokenizer, so CI runs it only when the repository has an `HF_TOKEN` secret; without one, CI says so and runs the
other 24 test files.

## Licences

The code here is Apache-2.0. Tiny Aya is CC-BY-NC-4.0, and anything trained from it carries that
licence. See [`NOTICE`](NOTICE).
