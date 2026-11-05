# Teaching a 3B model to remember a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

> **Draft. Numbers are development results on the probe pool; the registered held-out run replaces them before submission.**

## Abstract

A small model in a long chat forgets: once a fact scrolls out of its context window, it either says
it was never told or makes something up. We train a LoRA adapter on Tiny Aya Global (3.35B
parameters) to search the earlier conversation when, and only when, the answer is out of view, to
read what comes back, and to answer in the model's own voice. With only the last three exchanges
in view, the adapter answers questions about earlier facts correctly 98% of the
time in 58-message chats and 96% in 419-message chats, against
31% and 31% for the untrained model (+213% and
+207%). A blind judge finds the adapter's replies 14% more often coherent than the untrained model's, and at or above it on every kind judged. It names the wrong person's fact in 0.3% of replies, against 5.4% for the untrained model. On a harder development pool written by an independent agent, recall falls to 60% (untrained: 21%), because the adapter searches unfamiliar kinds of fact as if they were ones it was trained on. Every training change was
screened against a rule written before its run, and the final test was registered in advance and
then only made harder: a crowded condition with four distracting facts per chat, and a second
test pool written by an independent agent and never read by the authors. We also report two
findings about the toolkits we built on: a defect in AuditKIT's significance test, and a change to
TRL's loss that gives the same results with 2.7 GiB less memory.

![Recall before and after training](../figures/recall_by_length.png)

## 1. Introduction

Chat products keep long conversations, but a small model can only attend to a short window. The
usual answers are to send the whole conversation every turn, which costs more with every message,
or to bolt retrieval on with code around the model. We ask whether a 3B model can learn the
retrieval behaviour itself: decide when an answer is out of view, write a search, read the
result, and answer without sounding any different from before.

The Track 3 statement asks for a model that "decides when and what to retrieve, grounds its answers
in the retrieved text and ignores distracting documents". Each phrase maps to a measure here:

| Track statement | Measure |
|---|---|
| decides **when** to retrieve | right decisions: searched exactly when the answer was out of view |
| decides **what** to retrieve | the fact was found by the model's own query |
| **grounds** its answers | recall: the right fact in the reply |
| **ignores distracting documents** | false retrieval: a decoy's fact in the reply, with one and four decoys a chat |

**Contributions.**
1. A training recipe that teaches the habit without changing the voice: the model is trained on
   its own replies wherever they are right, and the tool's real output is always shown.
2. A test that is hard to game: pre-registered, amended only to make it harder, with a sealed pool
   written by an independent agent, a crowded condition, blind coherence judges and a second
   scorer from AuditKIT.
3. An ablation record of every change tried, kept or dropped, each against its own reference.
4. Two toolkit findings (AuditKIT's bootstrap, TRL's loss memory) and a cost comparison against
   closed models.

## 2. Related work

Tool use can be learned from demonstrations of when a call helps (Toolformer, Schick et al., 2023)
and interleaved with reasoning (ReAct, Yao et al., 2023). Adaptive retrieval asks when to retrieve
at all: popular facts are answered from memory, rare ones looked up (Mallen et al., 2023), and
Self-RAG trains a model to decide and to critique its own retrievals (Asai et al., 2024). RAFT
fine-tunes on retrieved sets that include distractor documents, so the model learns to cite the
right one (Zhang et al., 2024); our decoys play the same role inside a conversation. For long
chats, MemGPT manages memory with an agent loop around the model (Packer et al., 2023), and
LongMemEval measures long-term chat memory (Wu et al., 2025); models also use the middle of long
contexts poorly (Liu et al., 2024), which is one reason to keep the window short and search
instead. Training on a model's own outputs that pass a check follows STaR (Zelikman et al., 2022).
Coherence is judged by a model, as in LLM-as-a-judge evaluation (Zheng et al., 2023), but blind to
which model wrote each reply. Adapters are LoRA (Hu et al., 2022).

## 3. Task

A conversation has run for 58 or 419 messages. The model sees the system prompt, the last three
exchanges and the friend's newest message. Everything earlier sits behind one tool,
`search_corpus`, a full-text search over the earlier conversation that returns the top five
passages; the model may call it up to three times a turn. The newest message is one of five kinds:

| Kind | Example | What a good reply does |
|---|---|---|
| Fact told long ago | "drawing a blank on my daughter's tattoo" | searches, then answers ("a koi") |
| "Did I tell you…?" | "did i say anything about my godfather's tattoo" | searches, then confirms with the fact |
| Fact still on screen | "what language does Chidi speak" | answers from view, no search |
| Never told | "did i ever bring up what my mentor grows" | searches, finds nothing, says so |
| Just chatting | "i got stuck talking to Lucia for an hour" | replies, no search |

Every chat also holds **decoys**: the same type of fact about other people ("my classmate is scared
of heights" beside "my tutor is scared of spiders"), so a search can bring back the wrong person's
fact.

**Pools.** Conversations are built from templates in four pools that share no people, relations,
values, subjects or wording: **train**, **probe** (development; never trained on), **held-out**
(sealed) and **independent** (sealed, written by a separate agent; section 5).

## 4. Method

**Training data.** 800 rows (Fact told long ago 200, “Did I tell you…?” 150, Fact still on screen 150, Never told 150, Just chatting 150); LoRA rank 32 on the attention and MLP projections, learning rate 3e-4, 3 epochs, batch 2. For every training conversation the untrained model is run on
the same turn. Where its reply passes the scorer, that reply is the target, so training teaches
the habit of searching and reading without teaching a new voice. Where a search is needed, the row
shows a clean call with the demonstrated query, the tool's real output and then the answer; if the
real search missed the fact, the row says the model does not know, so a demonstration never
contradicts what the tool returned. Where the untrained model's answer fails, a short scripted
answer stands in. The number of decoys varies per row, so the number of passages a search returns
never gives the answer away. Plain chat lines take the untrained model's reply when it is asked to
be brief (the instruction is not part of the row), and a blind judge marks every such target on the
coherence rubric before training; the 8% it rejects are swapped for spares it accepted (R-058,
R-060). This filters the targets by the same rubric the coherence judges use, so the adapter is
trained toward what this kind of judge accepts; the held-out judges are the same kind.

**Training.** LoRA on Tiny Aya Global through AgentTune's distillation trainer (TRL underneath),
with the loss replaced by an equivalent that uses less memory (section 9). Three training seeds per
version. Rows were passed to TRL as chat messages with its defaults, which put the loss on every
token of a row, not only on the turns it teaches (4% of the tokens): the model also learned to
write the friend's lines, the tool's passages and the scripted small talk in view (R-076).

**How changes were made.** One change at a time. A change is screened on one training seed against
its reference on a development probe; if it gains, a rule is written down and then it is trained on
three seeds and confirmed on a second probe, with blind coherence sheets. Every step is a dated
entry in [`RECORDS.md`](../RECORDS.md), and every rule is committed before its runs.

## 5. Evaluation protocol

**Measures.** Recall (correct answers on the two kinds that need a search), right decisions,
correct answers per kind, false retrieval (a reply naming a wrong value of the fact asked about:
a decoy's, or for a question never told, any value), and coherence. Our scorer fails a reply that
names any wrong value; AuditKIT's agent evaluation scores every reply a second time with its own
oracles.

**Coherence.** A fresh judge model receives only a rubric and a shuffled sheet of replies, without
knowing which model wrote which, and marks each 1 or 0: does it respond to the newest message, fit
what was said, read as ordinary language, and avoid contradicting what is in view? The key is
opened only after the marks are in. Fact questions are judged with the tool for both models;
on-screen facts and ordinary chat are judged against the untrained model with no tool at all, so
the adapter is held to the model's own ordinary talk.

**Statistics.** Base and adapter run on identical conversations. Paired comparisons use the exact
sign test on the conversations where they differ; intervals are 95% percentile bootstraps over
conversations, keeping the pairing.

**The final test.** Registered before training (R-016) and amended twice before any run, each time
to make it harder: four conditions, base and three adapters on identical conversations, 300
conversations each.

| Condition | Pool | Decoys a chat | Added by |
|---|---|---|---|
| A | held-out | 1 | R-016 |
| B | held-out | 4 | R-038 |
| C | independent | 1 | R-039 |
| D | independent | 4 | R-039 |

Recall must be at least 20 points above the untrained model at each chat length with a sign test
below p = 0.01, counting all right answers and again counting only retrieved ones (R-041), false retrieval no higher than the untrained model's, and coherence at or above
it, in every condition. The held-out pool was written by Claude, the author's AI assistant, in the same
session as the training pool; the independent pool was written by a fresh agent that saw only a brief, an
avoid-list and a checker, and nobody on the project has read it (R-039).

**Development tests beyond the probe.** Every probe used in development shares the training pool's
author and style, so three harder checks were added before the final test, none of them deciding a
version: the crowded condition on the probe; `hard_dev`, a twin of the independent pool written by
a second fresh agent from the same brief, readable and used for development only (R-066); and
stress transforms applied to any pool, taken from the failure categories of the author's earlier
chat engine (its categories only, none of its text): the user's typing style, facts corrected
later, and 1,000-message chats (R-067). Writing the twin from the independent pool's brief, and
training on material written to a similar brief, makes the sealed independent pool less
independent of development than it was; it still shares no content with any other pool.

## 6. Results

Development numbers: the probe pool, 240 conversations (24 of each kind at each length), the untrained model against 3 adapters (v5) trained on seeds 82, 83, 84. The held-out run replaces these.

Recall above the untrained model, at 58 messages +213% (95% interval +119% to +422%, 48 conversations); at 419 messages +207% (95% interval +116% to +407%, 48 conversations).

### Retrieved, not guessed

A right answer can come from reading the fact or from guessing among plausible values. Each answer is
counted by where it came from: **retrieved** if the exchange holding the fact was among the results
of a search the model itself made, and a **guess** otherwise.

| Questions that need a search | Untrained (96) | Adapter, 3 seeds (288) |
|---|---|---|
| Right, fact in its own search results | 30 | 279 |
| Right, searched but the fact was not returned | 0 | 0 |
| Right without searching | 0 | 0 |
| Wrong although the fact was returned | 4 | 9 |

Of the adapter's 279 right answers, 279 were retrieved and 0 were guesses (the untrained model: 30 and 0). The gain is recovered information, not better guessing. The final test applies the recall rule to retrieved answers alone as well (R-041).

### Every kind of message

![Every kind, before and after](../figures/by_kind.png)

| Kind | Untrained | Adapter | Above untrained |
|---|---|---|---|
| Fact told long ago | 48% | 97% | +101% |
| “Did I tell you…?” | 15% | 97% | +567% |
| Fact still on screen | 71% | 90% | +27% |
| Never told | 88% | 99% | +13% |
| Just chatting | 65% | 100% | +55% |

Right decisions, searching exactly when the answer is out of view: 119 of
240 untrained, 240, 240, 240 (seeds 82, 83, 84) of 240 with the adapter. Every kind of message improves.

### Coherence, judged blind

![Coherence by kind](../figures/coherence_by_kind.png)

Pooled over 3 adapter seeds and 6 sheets, each with its own judge:

| Kind | Setting | Untrained | Adapter | Above untrained |
|---|---|---|---|---|
| Fact told long ago | both with the tool | 95 of 144 | 129 of 144 | +36% |
| “Did I tell you…?” | both with the tool | 141 of 144 | 144 of 144 | +2% |
| Fact still on screen | untrained with no tool | 99 of 144 | 119 of 144 | +20% |
| Just chatting | untrained with no tool | 135 of 144 | 142 of 144 | +5% |

Fact questions are judged with the search tool for both models. On-screen facts and ordinary chat are judged against the untrained model with no tool at all, so the adapter is held to the model's own ordinary talk.

### False retrieval: the wrong person's fact

![False retrieval by kind](../figures/false_retrieval.png)

| Kind | Untrained | Adapter |
|---|---|---|
| Fact told long ago | 1 of 48 | 0 of 144 |
| “Did I tell you…?” | 0 of 48 | 0 of 144 |
| Fact still on screen | 5 of 48 | 0 of 144 |
| Never told | 6 of 48 | 2 of 144 |
| Just chatting | 1 of 48 | 0 of 144 |
| **All** | **13 of 240** | **2 of 720** |

Over every kind the adapter names a wrong value in 0.3% of replies against 5.4%, -95%. Most of the gain is on facts still on screen and questions never told, where the untrained model fills in a value. On the two kinds that need a search the counts are small, 1 and 0, and the untrained model searches far less often (37 of 96 questions against 288 of 288), so it has fewer chances to pick up a decoy. The registered final test adds a crowded condition with four decoys a chat for exactly this reason.

### Harder development checks: where it still fails

With four decoys a chat instead of one, the adapter keeps 277 of 288 recall answers (279 with one) and names a wrong person's fact in 0 of 720 replies; the untrained model does so in 19 of 240 (R-065).

On `hard_dev`, the adapter answers 172 of 288 recall questions (60%) against the untrained model's 20 of 96 (21%): still +187%, but far below its 97% on the probe. In 103 of its 116 misses the search brought the fact back. The searches show why: the adapter writes the query phrase of the nearest training fact type, not words from the question, so a question about where someone grew up is searched as a birthday month, and the reply then denies the fact or answers the question it searched for (R-068). This is the largest gap found, and the sealed independent pool, written to the
same brief, is likely to show it; fix 14 (a wider training pool of new fact types) is aimed at it.

### A second scorer: AuditKIT

Each turn becomes an AuditKIT episode (the friend's message, the search calls, the final reply),
and AuditKIT's own oracles decide each case; for the fact questions this is its `AnswerAssertion`,
which matches whole words and is stricter than our scorer. AuditKIT agrees with our scorer on 959 of 960 cases. The exact sign test on AuditKIT's verdicts puts every adapter seed above the untrained model with p between 7e-26 and 1e-24.

## 7. Ablations: every change tried

Each row is one training seed on the development screen, against its own reference. Recall is out
of 96, on-screen answers out of 48, right decisions out of 240; the paired counts and sign test are
over all 240 conversations.

![Recall across training sets](../figures/development_path.png)

| Change | Recall of 96 (reference) | On screen of 48 | Right decisions of 240 | Right, all kinds: only reference / only change | Sign test p | Outcome |
|---|---|---|---|---|---|---|
| Untrained model | 38 | 32 | 109 | | | |
| v2: the full training set | 70 (38) | 33 | 232 | 20 / 76 | <0.01 | the reference for fixes 1 and 1b |
| Fix 1: read in-view facts through a hint | 69 (70) | 37 | 235 | 12 / 16 | 0.57 | led to 1b (R-024) |
| Fix 1b: 75 hard in-view rows | 75 (70) | 38 | 234 | 7 / 19 | 0.03 | **v3** (R-026) |
| Fix 3: fewer never-told rows | 73 (75) | 37 | 228 | 19 / 11 | 0.20 | dropped (R-028) |
| v3 retrained with the lean loss | 74 (75) | 37 | 233 | 8 / 5 | 0.58 | same results (R-032) |
| Fix 4: a second search after an empty one | 62 (74) | 37 | 233 | 22 / 11 | 0.08 | dropped (R-032) |
| Fix 5: a judge filters the training answers | 76 (74) | 41 | 233 | 8 / 14 | 0.29 | dropped on coherence (R-032) |
| Fix 5b: plain answers on “did I tell you…?” | 71 (74) | 37 | 232 | 14 / 12 | 0.85 | failed its coherence rule (R-034) |
| Fix 5c: 5b, and answers name the relation | 76 (74) | 37 | 232 | 12 / 15 | 0.70 | **v4** (R-036) |
| 4 epochs instead of 3 | 78 (76) | 39 | 231 | 3 / 7 | 0.34 | candidate (R-037) |
| Learning rate 1e-4 instead of 2e-4 | 67 (76) | 35 | 228 | 33 / 9 | <0.01 | dropped (R-040) |
| Fix 6: more ways of saying “I forgot” | 84 (76) | 36 | 235 | 10 / 16 | 0.33 | candidate (R-040) |
| LoRA on the MLP layers too | 87 (76) | 37 | 234 | 6 / 17 | 0.03 | candidate (R-044) |
| LoRA rank 32 | 86 (76) | 43 | 233 | 5 / 20 | <0.01 | candidate (R-044) |
| Learning rate 3e-4 | 86 (76) | 39 | 235 | 3 / 15 | <0.01 | candidate (R-046) |
| Fix 6 with LoRA on the MLP layers | 87 (84) | 39 | 235 | 16 / 18 | 0.86 | no gain over fix 6 (R-047) |
| Fix 6 at rank 32 | 92 (84) | 39 | 235 | 11 / 19 | 0.20 | beaten (R-052) |
| Fix 6 at rank 32 with the MLP layers | 90 (84) | 43 | 235 | 11 / 20 | 0.15 | ties rank 32 alone (R-048) |
| Fix 7: searches in the friend's own words | 94 (84) | 39 | 229 | 36 / 19 | 0.03 | dropped on false retrieval (R-050) |
| Fix 8: more ways of stating each fact | 86 (84) | 41 | 238 | 9 / 15 | 0.31 | candidate on the lead's settings (R-054) |
| Fix 6 at 3e-4 | 92 (84) | 41 | 238 | 4 / 16 | 0.01 | ties rank 32 (R-052) |
| Fix 6 at rank 32, with MLP, at 3e-4 | 95 (84) | 44 | 238 | 4 / 22 | <0.01 | failed its coherence rule (R-055) |
| Fix 6 at rank 64 | 91 (92) | 35 | 235 | 12 / 10 | 0.83 | no gain over rank 32 (R-053) |
| Fix 7b: 7, never-told rows only with results | 95 (84) | 38 | 222 | 27 / 19 | 0.30 | dropped on statements (R-054) |
| Fix 6 at rank 32 and 3e-4, attention only | 93 (95) | 42 | 231 | 15 / 4 | 0.02 | loses statements (R-053) |
| Fix 9: more plain-chat lines, lead's settings | 94 (95) | 45 | 240 | 3 / 4 | 1.00 | failed coherence at one seed of three (R-057) |
| Fix 8 data on the lead's settings | 94 (95) | 42 | 232 | 16 / 4 | 0.01 | loses statements (R-056) |
| Fix 10: fix 9 with judge-vetted chat targets | 96 (94) | 43 | 240 | 2 / 2 | 1.00 | failed coherence at one seed by one reply (R-059) |
| Fix 11: fix 10 with brief chat targets | 95 (96) | 42 | 240 | 4 / 3 | 1.00 | **v5** (R-061) |
| Fix 12: v5 with brief, vetted in-view answers | 90 (95) | 45 | 239 | 7 / 5 | 0.77 | dropped at the screen gate (R-063) |
| Fix 13: v5 with more indirect in-view questions | 91 (95) | 45 | 240 | 7 / 6 | 1.00 | dropped at the screen gate (R-064) |
| Lead's settings, 4 epochs | 93 (95) | 44 | 230 | 13 / 3 | 0.02 | loses statements (R-056) |
| Fix 14: v5 with half its fact rows from 47 new fact types | 92 (95) | 47 | 236 | 11 / 7 | 0.48 | dropped at the screen gate (R-071) |
| Fix 14c: a quarter of the fact rows from the new fact types | 93 (95) | 43 | 239 | 7 / 5 | 0.77 | dropped at the screen gate (R-073) |
| Fix 14b: fix 14 with plain-chat lines naming the new pool's people | 92 (92) | 44 | 240 | 9 / 8 | 1.00 | dropped at the screen gate (R-073) |
| Fix 15: fix 14c with 250 never-told rows that return someone else's fact | 96 (93) | 44 | 240 | 3 / 8 | 0.23 | dropped at confirmation, on plain-chat coherence (R-075) |
| Fix 16a: v5 with the loss on the taught turns only | 96 (95) | 43 | 240 | 3 / 5 | 0.73 | dropped at the screen gate, on plain-chat coherence (R-077) |
| Fix 16b: v5 with the loss on all but the scripted small talk | 87 (95) | 44 | 240 | 10 / 4 | 0.18 | dropped at the screen gate (R-079) |
| Fix 16c: fix 16a at learning rate 1e-4 | 93 (96) | 43 | 238 | 6 / 1 | 0.12 | dropped at the screen gate (R-079) |
| Fix 17: fix 16c with plain-chat targets vetted by two judges on a stricter rubric | 91 (93) | 45 | 237 | 3 / 2 | 1.00 | dropped at the screen gate (R-080) |

What the path shows:

1. **The first adapter memorised.** It scored 119 of 120 on training-style conversations and then
   failed on the probe pool's unseen content. In training, the number of passages a search returned
   gave the answer away, so it learned to search, not to read. Varying the decoys fixed it (**v1**).
2. **A false denial from one training sentence.** Many found-fact answers opened with the same word
   as a training sentence meaning "I don't know", and one seed slid into it. Changing that sentence
   fixed it (**v2**).
3. **Facts still on screen.** Rows where the untrained model had failed were added, answered through
   a hint that is removed from the row (**v3**).
4. **Coherence on "Did I tell you…?" fell below the untrained model.** The adapter answered a
   question with "That's great news!", or "Esme, who is my tutor, speaks fluent Turkish". Both came
   from training answers: some of the untrained model's own answers on this kind opened with a
   reaction to news, and most scripted answers left the relation out, so the model never saw the
   friend's "my tutor" turned into "your tutor". Plain answers that name the relation from the
   friend's side closed the gap (**v4**).
5. **Changes that did not help were dropped**, with their numbers in the table: fix 3: fewer never-told rows; fix 4: a second search after an empty one; fix 5: a judge filters the training answers; learning rate 1e-4 instead of 2e-4; fix 7: searches in the friend's own words; fix 7b: 7, never-told rows only with results; fix 12: v5 with brief, vetted in-view answers; fix 13: v5 with more indirect in-view questions; fix 14: v5 with half its fact rows from 47 new fact types; fix 14c: a quarter of the fact rows from the new fact types; fix 14b: fix 14 with plain-chat lines naming the new pool's people; fix 15: fix 14c with 250 never-told rows that return someone else's fact; fix 16a: v5 with the loss on the taught turns only; fix 16b: v5 with the loss on all but the scripted small talk; fix 16c: fix 16a at learning rate 1e-4; fix 17: fix 16c with plain-chat targets vetted by two judges on a stricter rubric. Having a judge filter the training answers (fix 5) left “Did I tell you…?” coherence at 35 of 48 against the untrained model's 47, because the judge passed the same openers.
6. **Training harder raised recall and cost coherence on plain chat.** A higher rank, LoRA on the
   MLP layers and a higher learning rate each gained recall on the screen, and all three together
   came close to every recall question. Its confirmation failed on the blind check of plain chat
   lines: told "my tutor has been acting strange lately", it searched and stated a stored fact about
   the tutor (R-055). The training set had six chat lines against 25 fact templates, so a model
   trained harder treated any line about a named person as a lookup. Searching in the friend's own
   words (fix 7) showed the same pull from the other side: recall rose and never-told questions
   were answered with other people's facts (R-050, R-054).
7. **The plain-chat habits came from the targets.** Adding 48 chat lines (fix 9) fixed the lookups,
   and its recall was 34% above v4's, but at one seed of three the judge still marked six chat
   replies incoherent, among them "Lucia is a great name." Those were the untrained model's own
   habits, copied from its replies in the training set. A blind judge vetting those targets first
   (fix 10) cut that seed's misses from six to three, one short of the untrained model; asking the
   untrained model for brief replies before vetting them (fix 11) passed on every seed (**v5**,
   R-057 to R-061).

## 8. Cost

At 419 messages the adapter reads 1,214 tokens a turn on average over 1.60 model calls and writes 28; the whole chat is 5,409 tokens, so it reads 78% less. Sending the whole chat costs more with every message; the adapter's cost per turn
stays flat.

| Per million turns | Cost | With the chat prefix cached |
|---|---|---|
| This adapter, self-hosted, batch 1 | $457 | |
| This adapter, self-hosted, batch 4 | $145 | |
| This adapter, self-hosted, batch 8 | $96 | |
| This adapter, self-hosted, batch 16 | $76 | |
| gpt-6-astra, whole chat each turn | $55,469 | $6,792 |
| gpt-6.1-sol, whole chat each turn | $11,094 | $817 |
| gpt-6.1-terra, whole chat each turn | $5,547 | $409 |
| gpt-6-luna, whole chat each turn | $555 | $68 |

At batch 16 the adapter costs $76 per million turns, 7× to 730× less than these closed models sent the whole chat. With every chat token billed at the cached rate, the cheapest closed model (gpt-6-luna, $68) costs about the same or less, so the saving there is privacy and control rather than money.

**Assumptions.** Self-hosted cost assumes the NVIDIA A10G on Hugging Face Inference Endpoints (AWS) at $1.00 an hour serves calls as fast as the measured card (NVIDIA GeForce RTX 3080, plain Transformers, calls of about 714 prompt tokens). The A10G has less memory bandwidth than that card, so it would likely be somewhat slower, while a dedicated serving engine would be faster. Closed-model cost sends the whole chat each turn and writes as many tokens as the adapter; the cached column charges every chat token at the cached rate, the most favourable case for the closed model. A closed model could also retrieve instead of reading the whole chat; the point here is that a 3B model can do the retrieval itself.

## 9. Toolkit findings

**AuditKIT's paired bootstrap does not centre its resamples.** A gain on 100 of 100 pairs comes out
as p = 1.0, and on this project's data it reported p = 0.52 for 57% → 88% over 240 paired cases. It is
shared by AuditKIT's model comparison, run comparison and experiment significance. We use the exact
sign test and a correctly centred bootstrap instead; the defect, a reproduction and a one-line fix
are in [`docs/auditkit_bootstrap_defect.md`](auditkit_bootstrap_defect.md).

**TRL's chunked loss copies the output layer for every chunk.** Training first peaked at
9.81 GiB on a 10 GiB card, so any other program on the card pushed it into shared memory
at several times the step time. The loss computes `h.float() @ w.float().t()`; under bf16 autocast
both float32 copies of the 262,144-word output layer are cast straight back to bf16, so they change
nothing but memory. A replacement that takes the bf16 product directly gives TRL's loss, scores and
gradients bit for bit (tested), and training peaks at 7.12 GiB at about 1.1 s
a step. Retrained with it, v3 differed from its original on 13 of 240 conversations, inside
run-to-run variation (R-032).

![Training memory](../figures/training_memory.png)

## 10. Threats to validity

- **Synthetic conversations.** All chats are generated from templates; real chats are messier. The
  independent pool was written to be harder (run-on messages, texting style, values that are easy to
  confuse), but it is still templated.
- **One author for train and held-out.** The held-out pool shares no content with training but was
  written by the same assistant; condition C and D's independent pool exists for this reason.
- **Development numbers.** The probe pool guided every change, so its numbers flatter the adapter;
  only the sealed pools decide.
- **The never-told scorer** passes any reply that names none of the listed values, so an invented
  value outside the list can pass; false retrieval undercounts for that kind.
- **The coherence judge** sees only the turns in view, so it cannot tell a false "you never told me"
  from a true one; recall is always read beside it. In development, "never told" replies were not
  on a coherence sheet; the final sheets cover every kind.
- **One judge a sheet.** The untrained model's replies are the same on every sheet of a kind, so
  its score shows how much judges agree. On plain-chat and in-view lines they agreed within one line
  in 48; on "fact told long ago" lines, three judges gave the same 48 replies 34, 17 and 30, because
  one marked down any reply that opens with a name (R-057). Claims on that kind rest on the pooled,
  paired comparison, where the adapter's lead (130 against 81) is larger than that spread.
- **Development pools and the sealed one share a brief.** `hard_dev` and the wide training pool
  were written to briefs like the independent pool's, so the final test's independent condition is
  less independent of development than when it was registered (R-066, R-069). One writer of the
  wide pool, since discarded, saw fragments of sealed wording through a checker that reported
  only counts; that pool was never used (R-070).
- **Training is not bit-reproducible on this card.** With the same rows and seed, TRL's own first
  gradient norm varied from run to run (R-029), so every claim pools three seeds.
## 11. Errors and corrections

Every error of method below was found during the work and is recorded where it happened; none is
hidden by a later result.

- **The first adapter's score was memorised.** It answered 119 of 120 on conversations like its
  training set and failed on a fresh probe, because in training the number of passages a search
  returned gave the answer away. Decoy counts now vary per row so the count carries no signal
  (R-018, R-020).
- **A plateau called too early.** After two fixes failed, we called v5 final on the strength of
  the probe alone (R-064). Challenged, we tested harder conditions: the crowded condition held,
  but the `hard_dev` twin showed recall of 60% against 97% on the probe (R-065, R-068). The probe
  shared the training pool's author and style and hid the gap.
- **A screen that counted the wrong thing.** The screen scored plain chat by whether the model
  searched, not whether its reply made sense, so a stronger adapter passed the screen and failed
  the blind judge (R-055). Every confirmation since judges plain chat on every seed.
- **One judge a sheet.** Three judges gave the same 48 untrained replies 34, 17 and 30 on one kind
  (R-057). Conclusions on that kind rest on pooled, paired comparisons, and section 10 says so.
- **A checker that pushed a writer to the sealed data.** The checker for an independent writer
  reported only how many of its lines clashed with other pools, so the writer wrote its own
  script, which printed fragments of sealed wording. That pool, meant for training, was discarded
  unused, and the checker now names only the writer's own lines (R-070).
- **A toolkit defect.** AuditKIT's paired bootstrap does not centre its resamples, so it reports
  large gains as not significant; we use an exact sign test and a centred bootstrap (section 9,
  R-031).
- **A training default not checked.** Every adapter through v5 was trained with TRL's default of a
  loss on every token of a row, found only when replies turned out to be copied from the scripted
  history (R-076; see the failure modes below).
- **A build that wrote before it checked.** The training-set build wrote its file before checking
  that no row exceeded the 1,024 tokens training keeps, so three screens (fixes 14, 14b and 14c)
  trained on sets with three to five rows whose answers were cut. The build now skips such rows
  and checks before writing; those screens are reported as screens of the sets they used (R-073).

**Failure modes found in the model.** Each was found by reading replies, not totals, and each
came from something in the training data.

- **A name became a search instruction.** Trained harder, the adapter treated any line about a
  named person as a lookup: told "my tutor has been acting strange lately", it searched and
  stated a stored fact about the tutor (R-055). The training set had six plain-chat lines against
  25 fact templates. Forty-eight more chat lines fixed the lookups (fix 9). The same bug came back
  with the wide pool: its names appeared only in rows that need a search, so "i should really
  call my mentor" was searched as "mentor phone number" (R-071; fix 14b adds the wide pool's
  people to plain-chat rows).
- **The untrained model's habits, copied.** Plain-chat targets are the untrained model's own
  replies, so the adapter learned its weak ones: "Lucia is a great name.", a book character for a
  friend's name, an earlier topic pulled into a reply (R-057, R-059). Vetting the targets with a
  blind judge, then asking for brief replies before vetting, removed them (fixes 10 and 11, v5).
- **Unfamiliar facts forced into familiar ones.** On text written by someone else, the adapter
  searched for an unfamiliar kind of fact with the query phrase of the nearest training fact type:
  "where my babysitter came of age" became "babysitter born birthday month". The right passage
  came back and the reply denied it or answered the question it had searched for (R-068).
  Training on 47 new fact types lifted recall there from 58 to 76 of 96 at one seed (fix 14,
  R-071); not yet confirmed.
- **Another person's fact, stated as the answer.** With the new fact types, a question about a
  fact never told brought back someone else's fact of that type, and the reply gave it as the
  answer: asked what "my goddaughter" studied, it replied "Isolde finished a course in
  philosophy", from a line about Isolde, the babysitter (R-071). All 16 such misses at one seed
  repeat the other person's value. When a search returned passages, v5 declined correctly 22
  times of 23 and the wide-trained adapter 17 of 33: it finds more and checks less whose fact it
  found (R-073). Showing it 100 more same-type facts about other people (fix 15) brought
  `never_told` back to 136 of 144 over three seeds with recall kept (R-075).
- **Scripted small talk, copied word for word.** Some plain-chat replies are lines from the
  scripted small talk that fills each training conversation: "Hm, good question, i'd say it
  depends", "Hope my barber settles down soon" (R-061, R-075). Training put its loss on every token
  of a row, and the five most common scripted replies each appear more than 100 times in the
  assistant's place, against at most 16 for any reply a row teaches (R-076). Fixes 16a and 16b put
  the loss on the taught turns only, or on all but the scripted replies; open.
- **A search built from the wrong message.** In the demo chat, "what did i fix under the sink"
  was searched as "brother new job", the query for a question two messages earlier, and declined
  (R-076). Open.
- **A found fact denied.** Shorter in-view answers (fix 12) and more indirect in-view questions
  (fix 13) each made the model trust the turns in view more and a search result less: searches
  found the fact and the reply said "I don't have that from you" (R-063, R-064). Both dropped.
- **Forgetting read as wordplay.** "drawing a blank on my tutor's tattoo", with the tattoo still on
  screen, is read as a joke, a drawing request or disappointment, by the untrained model and every
  adapter; it is most of v5's remaining misses on facts in view (R-063). Open.
- **One sentence, one false denial.** Many found-fact answers opened with the same word as a
  training sentence meaning "I don't know", and one seed slid from one into the other (v2).

## 12. Limitations

What this work does not cover, whatever its numbers:

- **One model, one size.** Only Tiny Aya Global (3.35B) was trained. Whether the recipe carries to
  Aya Expanse 8B or 32B, or to other families, is untested.
- **English only.** Tiny Aya is multilingual, and the friend's messages here are all English.
- **Facts never change.** Each fact is told once and stays true. Real friends correct themselves
  ("actually they moved again"), and the model is never asked to prefer the newer of two facts.
- **One tool, read only.** The model searches but never writes: it cannot save a note, update a
  fact or forget one, which a real memory needs.
- **A fixed window.** The view is always the last three exchanges, and conversations are 58 or 419
  messages. Other window sizes and much longer histories are untested.
- **No hostile text.** Retrieved passages are the friend's own words. Instructions hidden inside
  retrieved text, a risk for any model that reads search results, are out of scope here.
- **Greedy decoding only.** Every reply is greedy; behaviour under sampling is not measured.
- **Judged by models, not people.** Coherence is marked by a language model with a fixed rubric;
  no human panel checked the marks.
- **One machine.** All training and timing ran on one consumer card; costs elsewhere are estimates
  from measured speed and published prices.

## 13. Future work

- **Facts that change.** Train and test conversations where a fact is told, then corrected, and
  score whether the reply uses the newer one.
- **Injection in retrieved text.** Train the model to treat instructions inside search results as
  content, not commands, and test it with hidden instructions in the friend's earlier messages.
  This was the second behaviour in the original plan.
- **Writing memory.** Add a tool that saves a note, so the model decides what is worth keeping, and
  measure recall when only the notes, not the full history, are searchable.
- **Reinforcement on verified outcomes.** The decision to search and the answer are both checkable
  by code, so they suit reward-based training (for example GRPO through AgentTune) on top of the
  supervised adapter.
- **Other languages and larger models.** Repeat the recipe in the languages Tiny Aya supports, and
  on Aya Expanse 8B, with the same sealed-test protocol.
- **Real conversations.** Test on consented real chat logs, and add a human panel beside the model
  judge.
- **Upstream fixes.** Offer the memory-lean loss to TRL and the bootstrap fix to AuditKIT.

## 14. Reproduce

Everything runs on one 10 GB card. The repository holds the pinned model revision, the data
builder, training and evaluation scripts, every results file with its provenance (command, commit,
package versions), every coherence sheet with its key and the judge's marks, and the scripts that
make every number and figure here: `python scripts/make_figures.py` and
`python scripts/make_article.py`. No number in this article is typed by hand.

## Author contributions

Kevin Vaillancourt directed this work, carried out with an AI assistant, Claude (Anthropic), as an
executive-function accommodation. Test pools meant to be independent were written by fresh AI
agents that saw only a brief, and coherence was marked by fresh AI judges that saw only a rubric
and a sheet.

## References

- Asai, A., et al. (2024). Self-RAG: Learning to retrieve, generate, and critique through self-reflection. *ICLR*.
- Hu, E. J., et al. (2022). LoRA: Low-rank adaptation of large language models. *ICLR*.
- Liu, N. F., et al. (2024). Lost in the middle: How language models use long contexts. *TACL*.
- Mallen, A., et al. (2023). When not to trust language models: Investigating effectiveness of parametric and non-parametric memories. *ACL*.
- Packer, C., et al. (2023). MemGPT: Towards LLMs as operating systems. *arXiv:2310.08560*.
- Schick, T., et al. (2023). Toolformer: Language models can teach themselves to use tools. *NeurIPS*.
- Wu, D., et al. (2025). LongMemEval: Benchmarking chat assistants on long-term interactive memory. *ICLR*.
- Yao, S., et al. (2023). ReAct: Synergizing reasoning and acting in language models. *ICLR*.
- Zelikman, E., et al. (2022). STaR: Bootstrapping reasoning with reasoning. *NeurIPS*.
- Zhang, T., et al. (2024). RAFT: Adapting language model to domain specific RAG. *COLM*.
- Zheng, L., et al. (2023). Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. *NeurIPS*.

*Prior work: Latent Lab Explorer, the author's local chat engine, enforces these behaviours with
code around a Llama model; this project trains them into a model, and uses none of its code or test
sets. Built with AgentTune and AuditKIT from Lexsi Labs. Tiny Aya is CC-BY-NC-4.0, and the adapter
carries that licence.*
