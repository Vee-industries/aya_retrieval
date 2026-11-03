# Teaching a 3B model to remember a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

> **Draft. Numbers are development results on the probe pool; the registered held-out run replaces them before submission.**

A small model in a long chat forgets. Once a fact scrolls out of its context window it is gone, and
when the friend asks about it the model either says it was never told or makes something up. This
project trains a LoRA adapter on **Tiny Aya Global** (3.35B parameters) so that the model looks the
fact up instead: it searches the earlier conversation when, and only when, the answer is out of view,
reads what comes back, and answers in the same easy voice as before.

With only the last three exchanges in view, the adapter answers questions about earlier facts
correctly **84%** of the time in 58-message chats and **91%** in
419-message chats. The untrained model gets 31% and 31%. That is
**+169%** and **+191%** above the untrained model. Every kind of message improves.
A blind judge finds the adapter's replies 8% more often coherent than the untrained model's, and at or above it on every kind judged. It names the wrong person's fact in 1.1% of replies, against 5.4% for the untrained model.

![Recall before and after training](../figures/recall_by_length.png)

## The problem

The setting is a friendly chat that has run for 58 or 419 messages. The model sees only the last three
exchanges and the friend's newest message. Everything earlier sits behind one tool, `search_corpus`,
which runs a full-text search over the earlier conversation and returns the top passages.

The newest message is one of five kinds, and each calls for a different move:

| Kind | Example | What a good reply does |
|---|---|---|
| Fact told long ago | "drawing a blank on my daughter's tattoo" | searches, then answers ("a koi") |
| "Did I tell you…?" | "did I ever mention where my brother works" | searches, then confirms with the fact |
| Fact still on screen | asks about something in the last three exchanges | answers from view, no search |
| Never told | asks about something never mentioned | searches, finds nothing, says so |
| Just chatting | "i got stuck talking to Lucia for an hour" | replies, no search |

Each test has two scores. **Recall** counts correct answers on the first two kinds, the ones that
need a search. **Right decisions** counts the times the model searched exactly when it should have.
Coherence is judged separately and blind (below).

The idea comes from Latent Lab Explorer, the author's local chat engine, which does this with code
around a Llama model. This project asks whether the behaviour can live in the weights of a small
model instead. Nothing from that engine's code or test sets is used here.

## Setup

- **Model.** `CohereLabs/tiny-aya-global`, pinned to one revision. Generation is greedy.
- **Conversations.** Generated from templates with planted facts, in three pools that share no
  content: **train** (training data), **probe** (development) and **held-out** (sealed until one
  final run, registered in advance).
- **Harness.** A tool loop of up to three calls per turn, with AgentTune's tool prompt. Base and
  adapter run on identical conversations and identical tools.
- **Training.** LoRA r=16 on the attention projections, learning rate 2e-4, 3 epochs, batch 2,
  through **AgentTune**'s distillation trainer, on 800 rows.
- **Evaluation.** Our scorer, then **AuditKIT**'s agent evaluation as a second, independent scorer.
  The final test was registered before training began and made harder before it was run: every
  held-out chat runs once with one decoy and once with four, and recall, coherence and false
  retrieval must all hold in both (RECORDS R-016, R-038).
- **Records.** Every decision, run and result is in a dated log
  ([`RECORDS.md`](../RECORDS.md)). Rules for each comparison were written before its run.

## How the training data is built

The main design choice protects coherence: **the adapter learns from the untrained model's own
words.** For each training conversation, the untrained model is run on the same turn. Where its
reply passes the scorer, that reply is the training target. Training then teaches the habit of
searching and reading without teaching a new voice.

Where a search is needed, the row shows a clean call with the model's query, the tool's real output,
and then the answer. If the real search missed the fact, the row says the model does not know,
because a demonstration must stay true to what the tool returned. Where the untrained model's
answer fails the scorer, a short scripted answer stands in.

## What it took: one fix at a time

The method was "one small fix, see the results, repeat". Each change was screened on one training
seed, and a change replaced the current set only if it beat it on three seeds under a rule written
before the runs.

![Recall across training sets](../figures/development_path.png)

1. **The first adapter memorised.** It scored 119 of 120 on training-style conversations and then
   failed on the probe pool's unseen content. It had learned to search, not to read: in training,
   the number of passages returned gave the answer away. The data was rebuilt so that reading the
   result is the only way to answer (**v1**).
2. **A false denial from one training sentence.** On one seed, many found-fact answers opened with
   the same word as a training sentence that means "I don't know", and the model slid into it.
   Changing that one sentence fixed it (**v2**).
3. **Facts still on screen.** The adapter searched less but still missed facts in plain view. Rows
   where the untrained model had failed were added, answered through a hint that is removed from the
   row (**v3**).
4. **Coherence on "Did I tell you…?" fell below the untrained model.** A blind judge found the
   adapter answering a question with "That's great news!" or "Esme, who is my tutor, speaks fluent
   Turkish". Both came from the training answers. Some of the untrained model's own answers on this
   kind opened with a reaction to news, so this kind's rows got a plain answer instead.
   And most plain answers left the relation out ("Esme speaks fluent Turkish"), so the model never
   saw the friend's "my tutor" turned into "your tutor" and copied the "my" from the search result.
   Answers that name the relation from the friend's side closed the gap (**v4**).
5. **Fixes that did not work were dropped.** Fewer “never told” rows (fix 3): recall 73 against 74 of 96 on the screen (sign test p = 0.50). A second search after an empty one (fix 4): recall 62 against 74 of 96 on the screen (sign test p = 0.08). Having a judge filter the training answers (fix 5) left “Did I tell you…?” coherence at 35 of 48 against the untrained model's 47, because the judge passed the same openers.

## Results

Development numbers: the probe pool, 240 conversations (24 of each kind at each length), the untrained model against 3 adapters (v4) trained on seeds 82, 83, 84. The held-out run replaces these.

### Every kind of message improves

![Every kind, before and after](../figures/by_kind.png)

| Kind | Untrained | Adapter | Above untrained |
|---|---|---|---|
| Fact told long ago | 48% | 83% | +72% |
| “Did I tell you…?” | 15% | 92% | +533% |
| Fact still on screen | 71% | 80% | +13% |
| Never told | 88% | 98% | +12% |
| Just chatting | 65% | 99% | +54% |

Right decisions, searching exactly when the answer is out of view: 119 of
240 untrained, 236, 229, 226 (seeds 82, 83, 84) of 240 with the adapter.

### Coherence, judged blind

A fresh judge model receives only a rubric and a shuffled sheet of replies, without knowing which
model wrote which, and marks each reply 1 or 0: does it respond to the newest message, fit what was
said, read as ordinary language, and avoid contradicting what is in view? The key is opened only
after the marks are in.

![Coherence by kind](../figures/coherence_by_kind.png)

Pooled over 3 adapter seeds and 6 sheets, each with its own judge:

| Kind | Setting | Untrained | Adapter | Above untrained |
|---|---|---|---|---|
| Fact told long ago | both with the tool | 99 of 144 | 118 of 144 | +19% |
| “Did I tell you…?” | both with the tool | 141 of 144 | 142 of 144 | +1% |
| Fact still on screen | untrained with no tool | 102 of 144 | 117 of 144 | +15% |
| Just chatting | untrained with no tool | 133 of 144 | 138 of 144 | +4% |

Fact questions are judged with the search tool for both models. On-screen facts and ordinary chat are judged against the untrained model with no tool at all, so the adapter is held to the model's own ordinary talk.

### False retrieval: the wrong person's fact

Every test chat also holds a decoy: the same kind of fact about someone else, so a search for the
friend's tutor's fear can bring back their classmate's too. A reply that names a wrong value of the
fact asked about, the decoy's or, for a question never told, any value at all, is a false retrieval.
The scorer already fails such a reply; here it is counted on its own.

![False retrieval by kind](../figures/false_retrieval.png)

| Kind | Untrained | Adapter |
|---|---|---|
| Fact told long ago | 1 of 48 | 3 of 144 |
| “Did I tell you…?” | 0 of 48 | 1 of 144 |
| Fact still on screen | 5 of 48 | 1 of 144 |
| Never told | 6 of 48 | 3 of 144 |
| Just chatting | 1 of 48 | 0 of 144 |
| **All** | **13 of 240** | **8 of 720** |

Over every kind the adapter names a wrong value in 1.1% of replies against 5.4%, -79%. Most of the gain is on facts still on screen and questions never told, where the untrained model fills in a value. On the two kinds that need a search the counts are small, 1 and 4, and the untrained model searches far less often (37 of 96 questions against 275 of 288), so it has fewer chances to pick up a decoy. The registered final test adds a crowded condition with four decoys a chat for exactly this reason.

### A second scorer: AuditKIT

Every reply is scored again with AuditKIT's agent evaluation. Each turn becomes an AuditKIT episode
(the friend's message, the search calls, the final reply), and AuditKIT's own oracles decide each
case. For the fact questions this is its `AnswerAssertion`, which matches whole words and is stricter
than our scorer. AuditKIT agrees with our scorer on 957 of 960 cases. The exact sign test on AuditKIT's verdicts puts every adapter seed above the untrained model with p between 6e-19 and 5e-16.

**AuditKIT's significance test is broken, so it is not used.** Its paired bootstrap does not centre
its resamples under the hypothesis of no difference. A gain on 100 of 100 pairs comes out as
p = 1.0, and on this project's data it reported p = 0.52 for 57% → 88% over 240 paired cases. The exact sign
test and a correctly centred bootstrap are used instead, and the defect is written up for Lexsi in
[`docs/auditkit_bootstrap_defect.md`](auditkit_bootstrap_defect.md).

## Engineering notes

**The same loss with 2.7 GiB less memory.** Training first used 9.81 GiB of a 10 GiB card,
so any other program on the card pushed it into shared memory, at two to ten times the step time.
TRL's chunked loss makes a float32 copy of the model's 262,144-word output layer for every chunk of
tokens, and under bf16 autocast that copy is cast straight back to bf16. A replacement that skips the
copies gives TRL's loss, scores and gradients bit for bit, and training now peaks at 7.12 GiB
at about 1.1 s a step, while a browser plays video beside it.

![Training memory](../figures/training_memory.png)

**Training is not bit-reproducible on this card.** With the same rows and seed, TRL's own first
gradient norm varied from run to run (3.86, 3.42, 3.63). Seeds fix data order and starting weights,
not the exact result, so every claim here pools three training seeds.

## Limitations

- The conversations are generated from templates. Real chats are messier, and the vocabulary is
  narrower than real speech.
- In development, coherence was judged on four of the five kinds; "never told" replies were not on a
  coherence sheet. The held-out run's sheet covers every kind.
- The "never told" scorer passes any reply that names none of the listed values, so an invented
  fact outside the list can pass. It is reported, not used to decide.
- The coherence judge sees only the turns in view, so it cannot tell a false "you never told me"
  from a true one. Recall is always read beside coherence for that reason.
- English only.

## Reproduce

Everything runs on one 10 GB card. The repository holds the pinned model revision, the data builder,
the training and evaluation scripts, every results file with its provenance, every coherence sheet
with its key and the judge's marks, and the scripts that make every number and figure in this
article: `python scripts/make_figures.py` and `python scripts/make_article.py`.

*Prior work: Latent Lab Explorer, the author's chat engine, enforces these behaviours with code; this
project trains them into a model. Built with AgentTune and AuditKIT from Lexsi Labs. Tiny Aya is
CC-BY-NC-4.0, and the adapter carries that licence.*
