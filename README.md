# aya_retrieval

Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya Global (3.35B), shown only the last three
exchanges of a chat, search the rest when the answer is out of view. It is strong on chats from the generator that
made its training chats: on the sealed test (300 unseen generated chats in each of four conditions, run once) the
shipped seed recalls 91 to 107 of 120 facts, against 13 to 32 for the untrained model with the same tool. It is weak
on chats from outside writers (Claude agents): there the untrained model shown the whole chat recalls most (71 and 65 of 120), code
that searches every turn shows no measured difference from 6.37, and on S3, a second sealed test from outside writers,
code recalls more and 6.37 repeats its own wrong answers and names listed values on never-told questions more often than the
untrained model. A replacement, C1, cut both faults and missed one clause of the rule fixed before S3 opened, so 6.37
stays shipped and C1 is published beside it, labelled. The write-ups give every number with its record.

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

**Access.** The adapter and both datasets are public and un-gated (checked 2026-11-15, no login). The base model
CohereLabs/tiny-aya-global is gated: accept its licence on Hugging Face first.

## Reopened, 12 to 15 November

On 12 November the scripted demo, run for 6.37 for the first time, showed two faults: it answered questions it was
never told with unrelated stored facts (2 of 4 demo questions), and it repeated its own wrong answer while that answer
was in view (6 of 8 further questions, registered before they ran) (R-175, R-176). With the deadline reported extended (R-173), I saw
results I had missed and judged the extra time enough to train further, so I reopened the project to fix them
(R-177); the push to replace 6.37 ran inside the time that remained. A second sealed test, S3, was written by six blind writer agents and sealed
before any new training row, with its ship rule fixed before it opened (R-178, R-179, R-191). From 12 to 14 November
24 candidates were listed for screening on development sets, each registered before it was built; C1, K1.3 trained
twice on corrections of its own errors, became the pick after I changed the demo test twice (R-276 to R-279; disclosed
in the write-ups).

S3 ran once on 14 November (R-280 to R-292). C1 cut 6.37's two faults on S3 (copies 195 to 5 of 894; listed values
named on never-told questions 286 to 51 of 708) with no measured change in recall, and failed one clause: that second
rate, 51 of 708 (7.2%), had to be no higher than the untrained model's 14 of 236 (5.9%); S3 cannot tell the two apart
(95% interval -3.1 to +5.7 points), but the rule requires every clause, so **6.37 stays shipped** (R-287, R-294). On
S3, 6.37 itself does worse than the untrained model on both faults, and code that searches every turn (161 of 414)
and the whole chat (274 of 414) recall more than either trained model. C1 seed 82 is published beside 6.37, labelled
as failing one clause: [aya-retrieval-c1](https://huggingface.co/KevinVaillancourt/aya-retrieval-c1) (R-296). Four
review rounds checked the write-ups: two of ten reviewers (R-295, R-298) and two of thirteen (R-301, R-303). The long write-up, sections 7 to 9, gives every
candidate, ruling and number.

## Submission summary

**Title and claim.** Teaching a 3B model to search a long chat it can no longer see: a LoRA adapter trained with
AgentTune (6.37) makes Tiny Aya Global recall 91 to 107 of 120 out-of-view facts on the sealed test, where the
untrained model with the same tool recalls 13 to 32. A replacement built to fix two of its faults failed the second
sealed test (S3) on one clause, and 6.37 stays shipped.

**Track and problem statement.**

- Track 3, Agentic Fine-tuning, problem statement 4 of the track's list: "Fine-tuning for retrieval-augmented
  generation: Train a model that decides when and what to retrieve, grounds its answers in the retrieved text and
  ignores distracting documents."
- No other track and no "Other" statement.

**Headline, before to after.** Recall of out-of-view facts on the sealed test (four conditions, run once): 13 to 32 of
120 for base with the tool, 91 to 107 for 6.37 seed 82; pooled over the eight training seeds, base 8.3 to 28.3% and
6.37 85.2 to 90.4%. On chats from outside writers the picture is different (two sets, recall of 120): base with the
tool 26 and 27, 6.37 39 and 53, base shown the whole chat 71 and 65.

**Base model and method.** Tiny Aya Global (`CohereLabs/tiny-aya-global`, 3.35B, CC-BY-NC-4.0) plus a rank-32 LoRA,
trained by supervised fine-tuning with AgentTune on 1,094 rows to call a keyword search tool, read the passages and
answer, or decline when the chat never held the fact.

**For judges: one minute.**

- Built: a LoRA adapter that makes a 3.35B model search an old chat with a keyword tool, answer from what it finds,
  trained to decline when the fact was never told. It is tested with only the last three exchanges in view. On
  S3 it names a stored value on 402 of 708 (56.8%) never-told questions whose search returned text (exploratory,
  R-298).
- Strongest baselines first: on short outside-writer chats (a mean of 1,400 tokens), base shown the whole chat
  recalls most (71 and 65 of 120), and plain code that searches every turn shows no measured difference from 6.37 and
  runs faster. On S3 code recalls more than 6.37 (161 of 414 against 347 of 1,242). On LongMemEval-S, no measured
  difference from code on answers; code's first search finds the evidence more often, 372 against 333 of 476
  (registered H2, R-170).
- Where training helps: on the sealed generated chats 6.37 recalls 91 to 107 of 120 against 13 to 32 for base with the
  tool. On the outside-writer chats it searches when the answer is out of view and leaves answers in view alone, where
  code searches every turn.
- Where it fails: on S3 it names its in-view wrong value on 21.8% of wrong-view questions (base 3.7%) and a listed value on
  40.4% of never-told questions whose search returned text (base 5.9%); on LongMemEval-S it declines 233 of 470 answerable questions; on the
  scripted demo it gave an unrelated stored fact on 2 of 4 questions and repeated its own wrong answer on 6 of 8
  (R-175, R-176).
- State: the project was reopened on 12 November to fix those two demo failures. The pick, C1, failed one clause of
  the S3 ship rule (R-287), so 6.37 is still the shipped model (see "Reopened").
- Where to look: `RECORDS.md` (every decision and number), the README (reproduction), and the two Hugging Face
  collections.

## Results at a glance

Base is the untrained Tiny Aya Global. The tool is the full-text search over messages older than the last three
exchanges. Code is code that searches on every turn with the newest message as the query, then hands base the
passages (nothing trained). 6.37 is the shipped seed, 82, of eight training seeds.

Outside-writer chats, two sets (set 1 / set 2), one run each:

| Measure | Base, tool | Code | Base, whole chat | 6.37, tool |
|---|---|---|---|---|
| Recall, of 120 | 26 / 27 | 42 / 47 | 71 / 65 (best) | 39 / 53 |
| Answer already in view, of 40 | 36 / 34 | 13 / 16 | 35 / 32 | 35 / 37 |
| Never told, names no listed value, of 40 | 34 / 32 | 31 / 24 | 31 / 28 | 37 / 36 |
| Plain statement left unsearched, of 40 | 38 / 39 | 0 / 0 (searches every turn) | 40 / 40 (no tool) | 37 / 35 |

Generated chats:

| Measure | Base, tool | Code | Base, whole chat | 6.37, tool |
|---|---|---|---|---|
| Sealed test recall, of 120, four conditions | 13 to 32 | not in the sealed run | not in the sealed run | 91 to 107 |
| Recall, of 60, sealed pools after the run (R-168) | 5 to 17 | 14 to 32 | 21 to 33 (58 messages only; 419 messages does not fit 10 GB) | 44 to 55 (46 to 55 at 58 messages) |
| Right search decisions, of 300 (sealed) | 180, 193 | not run | not run | 298, 296 |
| Clean first calls (sealed; of the turns that searched; format only, unclean calls still ran) | 52 of 136, 49 of 107 | scripted | no tool | 180 of 180, 184 of 184 |

LongMemEval-S (500 questions; history of 244 exchanges at the median, past the model's window, so no whole-chat arm fits; judged by three Claude
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

S3, the second sealed test (60 chats from six blind writer agents, run once; 6.37 and C1 pool seeds 82, 83 and 94,
the other arms one run each; recall intervals resample chats; R-287):

| Measure | Base, tool | Code | Base, whole chat | 6.37, tool | C1, tool |
|---|---|---|---|---|---|
| Recall (older and confirm) | 59 of 414 (10 to 18%) | 161 of 414 (32 to 46%) | 274 of 414 (61 to 72%, best) | 347 of 1,242 (23 to 33%) | 364 of 1,242 (24 to 34%) |
| Copies: names its in-view wrong value when answering another question (lower is better) | 11 of 298 (3.7%) | 65 of 298 (21.8%) | 2 of 298 (0.7%) | 195 of 894 (21.8%) | 5 of 894 (0.6%) |
| N-hit false answers: never told, search returned text, names a value listed for the chat (lower is better) | 14 of 236 (5.9%) | 121 of 236 (51.3%) | 57 of 236 (24.2%) | 286 of 708 (40.4%) | 51 of 708 (7.2%) |

Ship rule for C1 (R-287): (a) pass, (b) pass, (c) fail by 1.3 points (C1's N-hit false-answer rate above base's).

The report arms, earlier candidates run on S3 at seeds 82 and 83 outside the ship rule (exploratory): K1 and K2.1 met
every measured line (N-hit false answers 12 and 14 of 472; coherence not judged); K1.3 failed clause (c) like C1 (37
of 472, 7.8%, against base's 5.9%).

The shipped adapter is 6.37 (`fix17cs37`, seed 82), frozen on 9 November (RECORDS R-160) with the scorer and judge
(`results/freeze/sealed_manifest.json`, R-154). The sealed run is R-162, with results in R-163
(`results/analysis/R-162/`). The write-up and model card in `docs/` are built from these results and R-164 to R-170
by `scripts/make_article.py`. [`RECORDS.md`](RECORDS.md) is the dated log of every decision, run and result, each
marked PRE-SPRINT, SPRINT or REOPENED. [`STANDARD.md`](STANDARD.md) is an earlier version of the author's research
standard (rules 1 to 12); the rule numbers above 12 in the papers refer to version 3, which is not in this repository.

## Setup

Needs Python 3.12 and one 10 GB GPU. Training the shipped seed peaked at 7.83 GiB of card memory and took 34 minutes; the sealed run's inference peak was 7.02 GiB. On Windows, match the PyTorch build to your driver.

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
then log in to Hugging Face and download the pinned revision, which every script loads from the local cache only:

```bash
../venv/Scripts/hf download CohereLabs/tiny-aya-global --revision af89d219b53ed9b13b8a4645f9c8028973510324
```

On Linux the paths are `../venv/bin/` in place of `../venv/Scripts/`. The package versions every result was made with
are recorded in each run file's provenance and pinned in CI's install step (`.github/workflows/ci.yml`); a local
install that resolves newer versions is not the tested one.

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
../venv/Scripts/hf download KevinVaillancourt/aya-retrieval-c1 --local-dir ../adapters/screens/k13opc1_r263_82
```

To train the shipped one from
scratch (about 35 minutes on an RTX 3080), into a folder apart from the downloaded weights and under a report name
apart from the committed reports (without `--report-name` the run writes over `results/recall_train/seed_82.json`):

```bash
../venv/Scripts/python scripts/run_recall_train.py --seed 82 --out-dir ../adapters/retrain/fix17cs37_82 --report-name fix17cs37_82_retrain --data data/screens/fix17cs37.jsonl --lora-r 32 --lora-targets q_proj k_proj v_proj o_proj gate_proj up_proj down_proj --learning-rate 3e-4 --loss-on chat_decision --max-vram-fraction 0.85 --save-epochs 2
```

The recorded command (`results/recall_train/fix17cs37_82.json`, provenance) is the same apart from the paths and
report name; `--save-epochs 2` only saves an extra checkpoint after epoch 2. Retraining does not give the same
weights bit for bit (R-029).

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

The script `demo/chat.txt` was written on 2026-11-04 (commit 723da40), before 6.37 was trained (2026-11-08), but it was visible
during development (R-076 logged earlier adapters failing turn 14), and three training rows hold a different pottery
fact. I ran this demo once for 6.37 and once for base on 2026-11-12 at 05:05 Eastern, read the result, and only then
registered it (R-175); the decision to publish it whole came after the run. It is shown whole, as run, with no rerun
of 6.37 and no change to the script. Base's run matches its earlier run (2026-11-05) on all 15 turns. Four questions
are an illustration, not a measurement; the measurements are the sealed run and the outside-writer sets.

**Eight more questions, registered before they ran (R-176).** After this result, an agent that saw only
`demo/chat.txt` wrote one question for each fact not yet asked and one more never-told question; each was asked on
its own branch after message 14, and two blind judges graded every answer (they agreed on all 32).

| Arm | Facts right, of 7 | Never-told right, of 1 |
|---|---|---|
| Base, search off | 1 | 1 |
| 6.37, search off | 0 | 0 |
| Base, with search | 1 | 1 |
| 6.37, with search | 0 | 0 |

On these eight the untrained model scores 2 and 6.37 scores 0. Base never searched; it was right on the one fact still
in view and on the never-told question, and invented the rest. 6.37 found the source message once and answered six
of the eight with "Your sister Marisol's pottery class is on Thursdays.", its own wrong answer from message 14, still
in view. That explanation was written after the run and is not tested. With search off, 6.37 said "I don't see it,
so I'd only be guessing." to all eight; both judges marked that ABSTAINED on the never-told question, which the
judges' own brief would count as right. Every answer: [`docs/demo.md`](docs/demo.md).

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

## When the chat fits: give base the whole chat

The sealed test and the outside-writer runs show the model only the last three exchanges, as a stand-in for a chat
too long to show. When a chat is short enough to show whole, that is the better choice. On the outside-writer
sets (chats of about 1,400 tokens), base with every message in view answers 58 and 52 of 80 `older`
questions, against 28 and 34 for 6.37 seed 82 with the tool and the last three exchanges (R-164).
Given the whole chat and the tool, 6.37 shows no measured difference from base given the whole chat,
on any kind, on both sets (R-165). That is one seed and two sets of 40 chats, so differences under 22 points between
two arms on a kind of 40 questions (the 95% half-width of a difference between two rates near 50%) are below what
this test resolves, and the test is not powered to show equality (R-142). So when a chat fits, show base the whole
chat and leave the adapter out. 6.37 with the whole chat was measured only on the outside-writer sets, where it
shows no measured difference from base with the whole chat (one seed; the test cannot show equality); it was not run
on S3, where 6.37 with the tool is worse than base on both faults. The whole-chat result holds on the outside-writer
chats, not on this project's generated chats:
on the sealed pools, base with the whole chat got 21 to 33 of 60 recall questions against seed 82's
46 to 55 (R-168).

**Code that searches every turn, with no training,** was registered as a reference in R-016 and run
late (R-167). On the outside-writer chats it shows no measured difference from 6.37 (42 and 47 of 120 against 39 and 53;
p = 0.76 and 0.45, R-169). Base with the tool searches on 54 and 42 of the 120 recall questions; code searches every
turn. Training adds searching when the answer is out of view (against base) and not searching when it is in view
(against code): answers already on screen 35 and 37 of 40 against code's 13 and 16; facts never told, answered with
no listed value, 37 and 36 against 31 and 24; plain statements left
unsearched 37 and 35 against code's 0 (by construction), and below base's 38 and 39. On the generated sealed pools the adapters are also above
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
user-to-assistant history (244 exchanges at the median), partly real logs and partly model-simulated (R-170).
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
- 6.37 declines more than base: on 21 of the 30 questions that should be declined (base 2), and on 233 of
  the 470 that should be answered (base 22).
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

- On S3, written by outside writers, 6.37 names its own in-view wrong value on 21.8% of wrong-view questions (base 3.7%) and a
  listed value on 40.4% of never-told questions whose search returned text (base 5.9%); code that searches every turn recalls more than it. S3's
  flags see only listed values of the asked category, so invented values and other stored facts pass unseen (R-287,
  R-298).

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
  goes from 20 to 73 of 96 (+265%). The +50% and +96% are the figures to read as generalization (against base;
  code shows no measured difference from 6.37, and the whole chat recalls more).
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
- **It repeats a wrong answer in view.** On eight more demo questions registered before they ran (R-176), the untrained model was right on 2 and 6.37 on 0: 6.37 repeated its own earlier wrong answer, still in view, on 6 of the 8.
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
| `RECORDS.md`, `HANDOFF.md`, `docs/PROJECT_MAP.md` | The dated log of every decision and result; where the project stands; what each part does and how the parts connect (R-216) |
| `data/screens/` | Every candidate's training set and writer files, each with its provenance file; `data/heldout3/` holds S3, sealed and hashed (R-179) and opened once for its run on 14 November (R-280) |
| `results/demo2/`, `results/panels/` | Demo2 runs and judge folders; each panel's and count's output, by record |
| `results/s3/` | S3, the second sealed test: one run file an arm and seed, the ship rule's result (`ship_rule.json`, R-287) and the coherence sheet, key and judges' marks (`coherence/`, R-284 to R-286) |
| `scripts/run_s3_eval.py`, `scripts/records/score_s3.py` | S3's runner (`--final` checks the seal manifest before loading the model) and its scorer (`sheet`, `tally`, `rule`; registered R-281, shown failing planted results first, R-282) |
| `docs/` | The long write-up (`ARTICLE.md`), 6.37's and C1's model cards (`MODEL_CARD.md`, `MODEL_CARD_C1.md`), and in `docs/submission/` the short paper (`HF_ARTICLE.md`), the form abstract (`ABSTRACT.md`) and the publishing plan (`PUBLISH.md`); every built file made from `results/` by `scripts/make_article.py` from its template; sample rows in `docs/samples/` |

## Reproduce the results

Every run and training file under `results/` carries its provenance (command, commit, package versions); the
Reproduce steps below and the Layout table name the script that writes each analysis, except the pre-repository
first run. The confirmatory
results can be rescored from the committed run files (`score_r162.py`, `score_s3.py`); they cannot be rerun from
scratch by someone else, because only 6.37 seed 82 and C1 seed 82 are published and retraining does not give the same
weights (R-029). Training is not bit-reproducible on this card (R-029); generation is: a repeated run of
seed 82 gave the same reply on 240 of 240 questions (R-156). Runs need the card to themselves. The base is pinned to
revision `af89d219b53ed9b13b8a4645f9c8028973510324`.

1. Train the shipped adapter (34 minutes on an RTX 3080; the command is under "Chat with it").
2. Score it on a development pool. This command reproduces `results/recall_eval/hd_fix17cs37_82_seed_73157.json`;
   `probe` runs the same way with `--pool probe`.

```bash
../venv/Scripts/python scripts/run_recall_eval.py --pool hard_dev --seed 73157 --items-per-kind 24 --index ../scratch/eval_hard_dev.sqlite --label hd_fix17cs37_82 --arms tool_loop --max-vram-fraction 0.85 --adapter ../adapters/screens/fix17cs37_82
```

3. The sealed run (R-162): `scripts/records/queue/final.sh`, sourced by `scripts/records/queue/runner2.sh`; both
   queues (this one and S3's `qs3.sh`) are kept as run, with the author's paths and a Windows-only lock. `final.sh`
   starts with `scripts/records/freeze_r154.py check
   results/freeze/sealed_manifest.json` and stops unless every frozen file and value matches. The sealed pools are
   read only with `--final`; the run is scored by `scripts/records/score_r162.py` into `results/analysis/R-162/`, with
   sheets from `sheets_r162.py`, briefs from `briefs_r162.py` and judge transcripts checked by `audit_judge_r162.py`.
4. The later analyses: `scripts/records/writeup_r164.py` (whole-chat control), `blind_r146.py` and `blind2_r157.py`
   (the outside-writer sets), `refs_r168.py` (code that always searches, on the sealed pools), `rigor_r139.py`
   (development rigor).
5. LongMemEval-S: `scripts/run_longmemeval.py` (one arm a call; its data file is not in the repository, its SHA-256 is
   in R-170), then `scripts/records/score_r170.py` and, for judged accuracy, `judge_sheets_r170.py` and
   `score_judged_r170.py`.
6. The write-ups and figures: `PYTHONPATH=src ../venv/Scripts/python scripts/make_article.py` and
   `PYTHONPATH=src ../venv/Scripts/python scripts/make_figures.py`; the long and short
   write-ups (`docs/ARTICLE.md`, `docs/submission/HF_ARTICLE.md`), the form abstract and `docs/MODEL_CARD.md` are filled
   from results files by their templates, and so is C1's card (`docs/MODEL_CARD_C1.md`); the few numbers quoted from
   records are listed in the article's section 15.
7. S3 (R-280): one run an arm and seed, base arms first, then 6.37 and C1 at seeds 82, 83 and 94, then the report arms
   at 82 and 83 (the queue, `scripts/records/queue/qs3.sh`, run as `qs3_lock.py C1`, kept as run; R-280). Each run is
   `scripts/run_s3_eval.py --final --index <sqlite> --label <label> --max-vram-fraction 0.85` with `--arm
   always_search`, `--arm whole_chat` or `--arm tool [--adapter <adapter>]`. Then `scripts/records/draw_s3_sample.py
   --final`, `scripts/records/score_s3.py sheet --final`, the three judges, `score_s3.py tally` and `score_s3.py rule`.

## Checks

```bash
../venv/Scripts/python -m ruff check .
../venv/Scripts/python -m ruff format --check .
../venv/Scripts/python -m pytest
```

CI (`.github/workflows/ci.yml`) runs the same three on a CPU runner on every push, with AgentTune and AuditKIT at
the commits every result was made with and no model weights. `tests/test_inference.py` needs Tiny Aya's gated
tokenizer, so CI runs it only when the repository has an `HF_TOKEN` secret; without one, CI says so and runs the
other test files.

## Declaration, AI use and team

- Outside the hackathon: only the plan of 20 October (R-001) and Latent Lab Explorer, the author's local chat engine,
  none of whose code, test sets or private chats is in this repository. Everything else was made from 1 November 2026
  (`RECORDS.md` marks each entry PRE-SPRINT, SPRINT or REOPENED).
- AI use: Claude (Anthropic) wrote the code, the generated pools, the training sets, the tests and the write-ups and
  ran the experiments, under my direction; every commit through R-301 (1,627) carries a Claude co-author
  line. Claude Opus agents wrote the outside-writer chats and S3, Claude Sonnet agents judged. People marked 50 scorer
  lines (the author and a second, independent marker) and 50 LongMemEval-S lines (the author). No percentage of
  generated code or text is claimed; the records do not count it.
- Team: Kevin Vaillancourt alone; no teammates tagged.
- Acknowledgements and more detail: the full write-up, `docs/ARTICLE.md`.

## Changelog

- **10 November (R-171, R-172).** First published version: the adapter 6.37, both datasets and both collections on
  Hugging Face, and the write-up with the sealed result, the outside-writer sets and LongMemEval-S.
- **12 November (R-173 to R-178).** Write-ups reworked after a blind rubric read, with overstatements corrected
  (R-173); notebook, CI and demo block (R-174); the scripted demo and eight more registered questions, which showed
  two weaknesses of 6.37 (R-175, R-176); the project reopened with a new sealed test and ship rule (R-177, R-178).
- **12 to 13 November (R-179 to R-217).** The reopened work: the "Reopened" section added with S3's seal
  (R-179) and updated through R-215, covering candidates K1 to K4.7 (R-180 to R-215). Added to match the submission
  checklist (R-217): a submission summary, the data, language, split and leak-check description, metric directions,
  the tool environment, a threat model, models and licences, compute and time per 1,000 replies, planned work, a
  declaration of work done outside the hackathon, an LLM usage statement and the team line. No number about 6.37
  changed, and 6.37 is still the shipped model.
- **14 November (R-218 to R-293).** The "Reopened" section carried through S3 (R-287: C1 fails one
  clause, 6.37 stays shipped); the long and short write-ups and the form abstract rebuilt from templates by
  `scripts/make_article.py` (R-288) and fixed after an audit (R-289); S3's layout rows and reproduce step added;
  decisions stated in my own voice (R-290, R-291); S3's report arms completed (R-292).
- **15 November (R-294 to R-305), this version.** A three-lane panel on the ship choice (R-294); two ten-lane review
  rounds (R-295, R-298); C1 published beside 6.37 (R-296); 6.37's S3 weakness and what S3's flags count stated in
  every document; the short paper cut to its story and required items; the audit of the write-ups (R-299); the long
  paper's detail moved to three appendices (R-300); two thirteen-lane review rounds' fixes (R-301, R-303); an audit's
  fixes (R-302). R-304: two private names that a sweep record had named were removed from the whole history; every
  commit from 10 November on has a new id (map in `results/scrub/`). An audit of R-303's write-up and its fixes
  (R-305).

## Licences

The code here is Apache-2.0. Tiny Aya is CC-BY-NC-4.0, and anything trained from it carries that
licence. See [`NOTICE`](NOTICE).
