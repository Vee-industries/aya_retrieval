# Teaching a 3B model to remember a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

> **{{status_line}}**

A small model in a long chat forgets. Once a fact scrolls out of its context window it is gone, and
when the friend asks about it the model either says it was never told or makes something up. This
project trains a LoRA adapter on **Tiny Aya Global** (3.35B parameters) so that the model looks the
fact up instead: it searches the earlier conversation when, and only when, the answer is out of view,
reads what comes back, and answers in the same easy voice as before.

With only the last three exchanges in view, the adapter answers questions about earlier facts
correctly **{{tuned_recall_58}}%** of the time in 58-message chats and **{{tuned_recall_419}}%** in
419-message chats. The untrained model gets {{base_recall_58}}% and {{base_recall_419}}%. That is
**{{gain_58}}%** and **{{gain_419}}%** above the untrained model. {{kinds_summary}}
{{coherence_summary}}

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
5. **Fixes that did not work were dropped.** {{dropped_fixes}}

## Results

{{results_scope}}

### Every kind of message improves

![Every kind, before and after](../figures/by_kind.png)

| Kind | Untrained | Adapter | Above untrained |
|---|---|---|---|
{{kind_table}}

Right decisions, searching exactly when the answer is out of view: {{decisions_base}} of
{{decisions_n}} untrained, {{decisions_tuned}} of {{decisions_n}} with the adapter.

### Coherence, judged blind

A fresh judge model receives only a rubric and a shuffled sheet of replies, without knowing which
model wrote which, and marks each reply 1 or 0: does it respond to the newest message, fit what was
said, read as ordinary language, and avoid contradicting what is in view? The key is opened only
after the marks are in.

![Coherence by kind](../figures/coherence_by_kind.png)

{{coherence_text}}

### A second scorer: AuditKIT

Every reply is scored again with AuditKIT's agent evaluation. Each turn becomes an AuditKIT episode
(the friend's message, the search calls, the final reply), and AuditKIT's own oracles decide each
case. For the fact questions this is its `AnswerAssertion`, which matches whole words and is stricter
than our scorer. {{auditkit_text}}

**AuditKIT's significance test is broken, so it is not used.** Its paired bootstrap does not centre
its resamples under the hypothesis of no difference. A gain on 100 of 100 pairs comes out as
p = 1.0, and on this project's data it reported p = 0.52 for {{auditkit_bug_example}}. The exact sign
test and a correctly centred bootstrap are used instead, and the defect is written up for Lexsi in
[`docs/auditkit_bootstrap_defect.md`](auditkit_bootstrap_defect.md).

## Engineering notes

**The same loss with 2.7 GiB less memory.** Training first used {{mem_before}} GiB of a 10 GiB card,
so any other program on the card pushed it into shared memory, at two to ten times the step time.
TRL's chunked loss makes a float32 copy of the model's 262,144-word output layer for every chunk of
tokens, and under bf16 autocast that copy is cast straight back to bf16. A replacement that skips the
copies gives TRL's loss, scores and gradients bit for bit, and training now peaks at {{mem_after}} GiB
at about {{step_seconds}} s a step, while a browser plays video beside it.

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
