# Teaching a 3B model to search a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

This is the full write-up. A short version (about five pages) is on Hugging Face,
[ARTICLE.md in the model repository](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37/blob/main/ARTICLE.md), with its source in
`docs/submission/HF_ARTICLE.md`.

> **Final numbers for the shipped model, 6.37 (`fix17cs37` seed 82, frozen before the sealed run): the sealed run, the two outside-writer sets, the whole-chat control, the two registered references run late, and LongMemEval-S as an outside check. Every number is computed from committed results files by `scripts/make_article.py`; `RECORDS.md` holds the dated record behind each.**

## Abstract

Trained with Lexsi's AgentTune, a LoRA adapter (6.37) lets Tiny Aya Global (3.35B), shown only the
last three exchanges of a chat, search the rest when the answer is out of view. On the sealed test
(300 unseen generated chats in each of four conditions, run once), the shipped
seed recalls 91 to 107 of 120 facts; the untrained model with the same
tool recalls 13 to 32. On chats from outside writers (written by Claude Opus
agents, about 1,400 tokens), the untrained model shown the whole chat does best
(71 and 65 of 120), and code that searches every turn
recalls as well as 6.37 (42 and 47 against 39 and
53) and runs faster. There, training's measured gain is when to search: 6.37
searches for facts out of view, which base rarely does, and leaves answers already in view alone
(35 and 37 of 40 right), where code searches every turn
(13 and 16).

Its 1,094 training rows are generated, with the untrained model's own passing replies
as targets. CuratorKIT's grounding gate audited an
ancestor set's found-fact answers (rejected 22 of 350); AuditKIT, a second scorer in
development, was not run on 6.37.

On the sealed test every registered rule passes: recall pooled over the eight seeds is
85.2 to 90.4% against base's 8.3 to 28.3%, every right answer came from a
search that found the fact, no adapter made more false retrievals than base, and three judges rated
every adapter coherent more often. Run later on the same pools, seed 82 recalls 44 to 55 of
60 at each chat length against code's 14 to 32, and 46 to 55 at 58
messages against 21 to 33 for base reading the whole chat.

Given the whole chat, 6.37 and base show no measured difference on the outside-writer chats. On
plain statements 6.37 searches more often than base (37 and 35
of 40 left unsearched, against 38 and 39).

On LongMemEval-S (500 questions over histories of
244 (197 to 305) exchanges; judged by three Claude Sonnet judges with LongMemEval's prompts, not
the official GPT-4o judge), 6.37 is right on 53 of 248 judged questions,
base with the tool on 34 (p = 0.014) and code on 40 (p =
0.12). Split after reading: on the 233 answerable ones,
6.37 gets 40, base 32 (p = 0.29), code
40. 6.37 declines 21 of all 30 unanswerable
questions and 233 of all 470 answerable ones; code declines
1. Code is faster on every set. Only LongMemEval-S is long; the outside-writer
chats are short, seen through an artificial three-exchange view.

**Limits.** Seed 82 is the lowest of the eight training seeds on the first outside-writer set, on
sealed conditions C and D and on `hard_dev`; there its gain over base has p =
0.047, above the registered 0.01. It corrects 1 and
3 of 20 false claims in "..., right?" questions. The coherence judges are Claude Sonnet agents only, never checked against a
person. Both sealed pools are generator-built.

## Results at a glance

Outside-writer chats, two sets (set 1 / set 2), one run each, the last three exchanges in view
except for base with the whole chat:

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
| Right search decisions, of 300 (sealed; `heldout`, `independent`) | 180, 193 | not run | not run | 298, 296 |
| Clean first calls (sealed; of the turns that searched; format only, unclean calls still ran) | 52 of 136, 49 of 107 | scripted | no tool | 180 of 180, 184 of 184 |

LongMemEval-S (500 questions; a history of 244 (197 to 305) exchanges, so no
whole-chat arm fits; judged by three Claude Sonnet judges with LongMemEval's prompts, not the
official GPT-4o judge):

| Measure | Base, tool | Code | 6.37, tool |
|---|---|---|---|
| Judged right, of 248 judged | 34 | 40 | 53 (p = 0.014 against base, 0.12 against code) |
| Of those, answerable, of 233 (split after reading) | 32 | 40 | 40 (p = 0.29 against base) |
| Declines on answerable, of all 470 | 22 | 1 | 233 |
| Declines on unanswerable, of all 30 | 2 | 0 | 21 |
| Gold answer in reply, of 411 (mechanical) | 51 | 63 | 51 |
| Clean first calls (of questions that searched) | 146 of 328 | scripted | 441 of 441 |
| Seconds a question | 3.47 | 3.09 | 3.81 |

![Whole chat or search](../figures/whole_chat_or_search.png)

*Figure 1. Outside-writer sets, `older` questions (of 80 a set): base and 6.37 seed 82
with the last three exchanges and the tool, and each given the whole chat (section 6).*

![Recall out of view](../figures/recall_out_of_view.png)

*Figure 2. Recall with the last three exchanges in view: base against the eight training seeds
pooled (small dots: each seed), on both outside-writer sets and the four sealed conditions; both
sealed pools are generator-built (sections 7 and 8).*

**Which to use when.**
1. If the whole chat fits in the context, show it whole: base with the whole chat recalls best on
   outside-writer chats, and needs no adapter.
2. If it does not fit, code that searches every turn recalls as well as 6.37 on outside-writer
   chats and is faster. 6.37 adds leaving in-view answers alone and fewer needless searches.
3. On very long histories (LongMemEval-S), 6.37 declines half the questions that have an answer
   (233 of 470); code declines 1.

**Terms.**
- **Base**: the untrained Tiny Aya Global.
- **Seed 82**: the shipped adapter, 6.37; 6.37 names the training set, and seed 82 is the one of
  its eight training seeds that ships.
- **Tool**: `search_corpus`, a full-text search over the messages older than the last three
  exchanges; top 5 passages, up to 3 searches a message.
- **Code**: code that searches on every turn with the newest message as the query, then hands base
  the passages; nothing is trained.
- **Recall**: right answers on `older` (a fact told long ago) and `confirm` ("did I tell
  you...?") questions; the registered primary measure.
- **In view** (`in_view`): the answer is still in the last three exchanges, so no search is needed.
- **Never told** (`never_told`): the chat never held the fact; right when the reply names no value
  of that type.
- **Statement**: a plain chat line; right when the model makes no search.
- **Sealed test**: registered before training and run once, on base and all eight seeds, over
  300 generated chats in each of four conditions (two pools, one or four decoy
  facts a chat).
- **Outside-writer sets**: two sets of 40 chats by Claude Opus agents who never saw the
  generator. Set 1 became a development set when candidate 7 was designed from its failures; set 2
  was read by no decision that changed 6.37.
- **Judge 1**: three Claude Sonnet judges mark each reply; judge 1's mark is the score, and the
  other two are reported.
- **Clean call**: a reply that parses whole as one `search_corpus` call with nothing before or
  after it, counted of the replies that searched. An unclean call still ran its search, so the
  count is a format measure.

## 1. Introduction

A chat assistant keeps a long conversation, but a model attends to a limited window. Tiny Aya Global
takes at most 8,192 tokens, and 9 of its 36 layers
attend to all of them; the other layers attend to the last 4,096 (the model's config).
Past that, a fact told early in the chat is either out of the prompt or in a part most layers do
not see.

**The first answer is to show the whole chat when it fits.** It was measured late, after the
sealed run (R-164, R-165), and it changes how the rest of this paper should be read. On the
outside-writer chats, of about 1,400 tokens, the untrained model with every message in
view beats the trained model working from the last three exchanges and a search, by a wide margin
(section 6). Given the whole chat as well, the trained model and the untrained one show no
measured difference on every kind (one seed, two sets of 40 chats; gaps under about
15 points on a kind of 40 questions are below what this test resolves).
On those chats this supports one design: show the model the whole chat when it fits, and let it
search when it does not. On the generated sealed chats of about the same length the whole chat
does not win: there the untrained model reading it is far below the trained model with the tool
(section 7). So which is better depends on the kind of chat, and every result below names the
kind of chat it is on.

**The second answer is plain code that searches on every turn.** It was registered as a reference
before any adapter existed (R-016), left out of the sealed run, and run late (R-167, R-168, R-169).
On the outside-writer chats it recalls as well as the trained model, with no measured difference,
and is faster (sections 6 and 10). Base with the tool searches too little and code searches every
turn. Training adds searching when the answer is out of view (against base) and not searching
when it is in view (against code): 6.37 answers what is still in view far more often than code,
and declines what was never told more often (a sign test below 0.05 on the second set only). On
plain chat lines it searches more often than base: it leaves 37 and
35 of 40 unsearched, base 38 and
39. On the generated sealed pools the trained model is
far above code on recall as well (section 7).

**What the trained model adds over the untrained one with the same tool** is a model that, shown
only the last part of a chat, decides when an answer is out of view, writes a search, reads the
result and answers without sounding different from before. It is tested with the last three
exchanges in view, as a stand-in for a chat too long to show. It beats the untrained model with
the tool on every set built for this project: on the outside-writer sets by +10.8 and
+21.7 points (+50% and +96% over base), and by
60 to 82 points pooled over the eight seeds on the generator's sealed pools (sections
7 and 8). On LongMemEval-S, an outside set of user-to-assistant chats, it is judged above the
untrained model overall, with no measured difference on the questions that can be answered (a
split made after reading the registered result, R-170), and plain code finds the evidence more
often (section 9).

The Track 3 statement asks for a model that "decides when and what to retrieve, grounds its answers
in the retrieved text and ignores distracting documents". Each phrase maps to a measure here:

| Track statement | Measure |
|---|---|
| decides **when** to retrieve | right decisions: searched exactly when the answer was out of view |
| decides **what** to retrieve | the fact was found by the model's own query |
| **grounds** its answers | recall: the right fact in the reply, counted again on retrieved answers alone |
| **ignores distracting documents** | false retrieval: a decoy's fact in the reply, with one and four decoys a chat |

**Contributions.**
1. A measured answer to "why not show the whole chat": on short outside-writer chats, do; given
   the whole chat, the trained model and the untrained one show no measured difference (one seed,
   two sets of 40 chats). On generated chats of the same length, the untrained model
   reading the whole chat is far below the trained model with the tool.
2. A measured answer to "why not plain code that always searches": on the outside-writer chats it
   recalls as well and is faster, and training adds when to search (searching when the answer is
   out of view, against base; not searching when it is in view, against code); on the generated
   sealed pools the trained model is far above it.
3. A training recipe that teaches the search habit while keeping the model's own voice (section 4).
4. A test registered before training, amended only to make it harder, frozen
   with its scorer and judge, run once on every training seed (R-016, R-038, R-039, R-041, R-154,
   R-162), two sets of chats by writers who never saw the generator, and an outside check on
   LongMemEval-S (R-170).
5. A ledger of every candidate tried, with the line each failed (section 11), and three toolkit
   findings (section 12).

## 2. Related work

Tool use can be learned from demonstrations of when a call helps (Toolformer, Schick et al., 2023)
and interleaved with reasoning (ReAct, Yao et al., 2023). Adaptive retrieval asks when to retrieve
at all: popular facts are answered from memory, rare ones looked up (Mallen et al., 2023), and
Self-RAG trains a model to decide and to critique its own retrievals (Asai et al., 2024). RAFT
fine-tunes on retrieved sets that include distractor documents, so the model learns to cite the
right one (Zhang et al., 2024); this project's decoys play the same role inside a conversation. For long
chats, MemGPT manages memory with an agent loop around the model (Packer et al., 2023), and
LongMemEval measures long-term chat memory (Wu et al., 2025); models also use the middle of long
contexts poorly (Liu et al., 2024), which is one reason to keep the window short and search
instead. Training on a model's own outputs that pass a check follows STaR (Zelikman et al., 2022).
Coherence is judged by a model, as in LLM-as-a-judge evaluation (Zheng et al., 2023), but blind to
which model wrote each reply. Adapters are LoRA (Hu et al., 2022).

## 3. Task and pools

A conversation has run for some time. In the main tests the model sees the system prompt, the last
three exchanges and the friend's newest message. Everything earlier sits behind one tool,
`search_corpus`, a full-text search over the earlier conversation that returns the top 5
passages, one passage per exchange; the model can call it up to 3 times a turn. The
newest message is one of five kinds, each scored by a fixed rule (`src/aya_retrieval/scoring.py`):

| Kind | Example | Scored right when |
|---|---|---|
| `older`: fact told long ago | "drawing a blank on my daughter's tattoo" | the reply names the answer and no listed wrong value |
| `confirm`: "did I tell you…?" | "did i say anything about my godfather's tattoo" | the same; saying it was never told is wrong |
| `in_view`: fact still in view | "what language does Chidi speak" | the same |
| `never_told` | "did i ever bring up what my mentor grows" | the reply names no value of that type |
| `statement`: just chatting | "i got stuck talking to Lucia for an hour" | the model makes no search (the reply's words are not scored) |

`older` and `confirm` together are **recall**, the registered primary measure (R-016). Every chat
also holds **decoys**: the same type of fact about other people ("my classmate is scared of heights"
beside "my tutor is scared of spiders"), so a search can bring back the wrong person's fact.

**Pools.** Generated conversations are built from pools of people, relations, fact types and small
talk that share no content; tests enforce it (README, Pools).

| Pool | Written by | Used for |
|---|---|---|
| `train`, `wide` | Claude; `wide` by a fresh agent from a brief | training (R-015, R-069) |
| `probe` | Claude | development screens and confirmations |
| `hard_dev` | a fresh agent, from the sealed pool's brief | development: a readable twin of `independent` (R-066) |
| `heldout` | Claude | the sealed test only (conditions A and B); run once (R-162) |
| `independent` (generator-built, sealed) | a fresh agent, from a brief; never read | the sealed test only (conditions C and D); run once (R-039, R-162) |

The generated tests use chats of 58 and 419 messages. A development run holds 24 conversations of
each kind at each size; a sealed condition holds 30, 300 in all.

**The outside-writer sets** are different in kind. Each is 40 chats with 240
questions, written by 4 fresh Opus agents from one behaviour brief, with no access to
the generator, its pools or any result, and frozen by SHA-256 before anyone read a chat (R-142,
R-143, R-152). The chats have 20 to 30 exchanges and about 1,400 tokens (at most
1,786). Half the `confirm` questions claim a wrong value, so agreeing with the user
cannot pass (R-142). They are tag questions: a count of the `confirm` messages finds a tag
("right?", "yeah?", "isn't it" and the like) in 40 of 40 on set 1 and 40 of 40 on set 2, ending
the message in 37 and 33 (the rest carry it mid-message, before a further
sentence; R-153 found all 40 on set 1 to be tags). A
loader turns each question into the same harness item as every other test (R-142). The first set
(`data/blind_dev/`) was registered as report only and became a development set when 7 was designed
from its failures (R-151); the second (`data/blind_dev2/`) was written after 6.37 was fixed and was
read by no decision that changed 6.37 (R-152, R-157). It was 7's judge (R-151, R-153), and the
freeze panel's lane cited it in arguing for the freeze (R-159).

## 4. Method

**The loop.** The model's turn either answers or calls `search_corpus`; the harness runs the search,
returns the passages, and the model answers from them, up to 3 searches a message
(`src/aya_retrieval/harness.py`). Decoding is greedy.

**6.37's training set** (`data/screens/fix17cs37.jsonl`, 1,094 rows: `older` 332, `confirm` 230, `in_view` 150, `never_told` 160, `statement` 222) was built in
steps, each recorded before it trained:

- *Targets in the model's own voice* (R-016, R-020). Where the untrained model's reply passes the
  scorer, that reply is the target; where a search is needed, the row shows a clean call with the
  demonstrated query, the tool's real output and then the answer, and if the real search missed the
  fact the answer says it does not know. Decoy counts vary per row (0 to 2 for recall rows, 1 to 3
  for `never_told`), because the first adapter learned that the number of passages gave the answer
  away (R-018, R-020).
- *Plain chat* (R-055 to R-061). More plain-chat lines; their targets are the untrained model's
  replies when asked to be brief, vetted by a blind judge on the coherence rubric (v5).
- *Loss on what is taught* (R-076, R-077, R-088, R-092, R-093). Until v5, TRL's default put the loss
  on every token of a row, scripted small talk included. Loss now falls on the taught turns, and on
  plain-chat rows only on the reply's first token and its end-of-turn marker, so the reply's words
  stay the model's own (17m, v6).
- *Stricter plain-chat targets* (R-078 to R-080): two judges re-vetted the targets on a rubric that
  names reading a complaint as good news, a wrong name and an invented event.
- *Who-is-who answers* (R-094 to R-098, R-105): answers that pinned the friend's relation on the
  wrong person were rewritten in the form "Your {relation} {person} ...", with replacements first
  passed by CuratorKIT's grounding gate.
- *Corrections and an earlier question in view* (R-102, R-104): 170 train-pool rows where a fact is
  corrected later, with cue controls, and rows with an earlier question still in view. Built from
  6.1 to 6.2 (R-105 to R-109), trained from scratch.
- *Statements and indirect questions* (R-114, R-117): chat lines that name a fact type answered
  without a search, questions asked as statements answered from one with the pool's scripted
  answer, and contrast lines where someone else forgets or loses something, answered without a
  search (6.31).
- *Removals* (R-122 to R-127): 6.37 is 6.31 less 9 of those contrast lines (the lost wallet, the
  forgotten umbrella, lost track of time), which went with one missed probe question.

No row comes from `probe`, `hard_dev`, either outside-writer set or a sealed pool. Several rows were
designed after reading failures on development pools, so those pools are development evidence for
6.37, not tests of it (R-117, R-122, R-128).

**Training.** LoRA rank 32 on `q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`; peak learning rate 3e-4, 3 epochs, batch 2, loss mode `chat_decision`, with TRL's chunked loss replaced by `lean_loss.lean_chunk`; trained from no adapter; 222 plain-chat rows carry loss only on the reply's first token and its end-of-turn marker. Through AgentTune's distillation trainer (TRL underneath). Eight
training seeds (82, 83, 94 to 99) were trained on the same set; seed 82 was named to ship before
seeds 94 to 99 or any outside-writer chat existed (R-114, R-141), and is the frozen model (R-160).
Training took 33 to 35 minutes a seed; 6.37's training peak was 7.81 to 7.84 GiB of card
memory, already under the lean loss of section 12.

**The Lexsi toolkits** (R-003, R-016, R-030, R-031, R-096, R-098):

| Toolkit | What it did | Ran on 6.37? |
|---|---|---|
| AgentTune | Trained every adapter (supervised LoRA) | Yes |
| CuratorKIT | Its grounding gate audited v6's found-fact training answers and rejected 22 of 350; the replacements it passed are in 6.37's lineage. The rest of 6.37's 1,094 rows were not gated by it | On an ancestor set only |
| AuditKIT | Second scorer in development: agreed 959 of 960 on v3 (its files: `fix5c_probe73157`, `v3_probe73157`, `v5_probe73157`); its paired bootstrap does not centre resamples (the project's proposed one-line fix, not adopted upstream) | No |

Section 12 reports what each showed.

## 5. Evaluation protocol

**Registration.** R-016 registered the test before any recall adapter existed: base and adapters on
identical held-out conversations, 30 per kind at each of 58 and 419 messages, greedy, run once.
Three amendments, each made before any held-out run and each only adding requirements: four decoys
a chat as a second condition and false retrieval as a gated measure (R-038); a second sealed pool,
`independent`, written by a fresh agent and never read (R-039); and the recall rule must also hold
when only retrieved answers count (R-041). R-020 changed one thing in every pool before any was
read: `never_told` questions use the `confirm` wording half the time, so a `confirm` wording does
not mean the fact exists.

**The freeze.** The scorer, the sealed pools, the judge's brief and rubric, the human check and the
adapter's weights were hashed into `results/freeze/sealed_manifest.json`, the judge pinned to
`claude-sonnet-5-5` (R-154, R-160). The sealed run began with a check of that manifest and ended
with a check of every judge's transcript (R-162, R-163).

**The sealed run** (R-162). Four conditions, each run once, base and all eight 6.37 seeds on the
same 300 conversations, item seed 90311:

| Condition | Pool | Decoys a chat | Added by |
|---|---|---|---|
| A | `heldout` | 1 | R-016 |
| B | `heldout` | 4 | R-038 |
| C | `independent` (generator-built, sealed) | 1 | R-039 |
| D | `independent` (generator-built, sealed) | 4 | R-039 |

Rules, every one in every condition: (1) recall pooled over the adapters at least 20 points above
base at each size, with a paired exact sign test below 0.01; (2) rule 1 again on retrieved answers
only; (3) each adapter's false retrievals no more than base's; (4) each adapter's coherent count at
or above base's, on all 300 conversations in A and a fixed sample of 120 in B to D.

**Coherence.** A judge sees the turns in view, the newest message and a reply, and marks 1 if the
reply "is a sensible next turn: it responds to the newest message, fits what was said in the turns
shown, reads as ordinary language, and does not contradict or deny anything said there"
(`coherence.RUBRIC`). Each sheet shuffles every model's reply to the same conversations with the
names removed, so one judge marks base and every adapter (R-090, R-162). Three fresh judges mark
each sheet; judge 1 decides and judges 2 and 3 are reported. Every judge's transcript was audited
(model, folders touched, commands run, every line marked) before its marks were filed
(`scripts/records/audit_judge_r162.py`, R-163). Measured spread: R-128's three judges split on
13 of 576 lines (R-154). **The judges were never checked against a person.** The human checks check
the recall scorer, on 50 lines drawn from base and seed 82 on the development pools
`probe` and `hard_dev`, not from the sealed or outside-writer chats: I (the author, not an independent marker) agreed with the scorer on 47 of 50 lines (Cohen's kappa 0.88), and the scorer passed no reply I failed (R-144). A second, independent marker agreed with the scorer on 48 of 50 (kappa 0.92) and with me on 49 (kappa 0.96) (R-145). In every
disagreement the scorer was the stricter; the two lines both markers passed and the scorer failed
name the answer and a wrong value together (R-144, R-145).

**Statistics.** Paired exact sign tests on the questions where two runs differ, and 95% percentile
bootstrap intervals that resample whole conversations or chats, keeping the pairing. The adapter
pairs in rule 1 share conversations, so its p-value overstates independence; the whole-conversation
interval is the figure to read (R-162). Generated questions share fact templates: the development
pools' recall questions come from 5 templates (`probe`) and 8
(`hard_dev`), so item-level p-values there overstate the evidence (R-141). The sealed pools' template
count is not known without opening them, which this project's rules forbid, and the sealed intervals
do not resample templates (R-164).

**Every deviation from the registered plan, in one place.** Ten deviations; four first disclosed in
R-167 after the write-up's review (items 7 to 10); none changes a pass rule.
1. *Eight seeds, not three.* R-016 named three adapters; the sealed run used all eight trained on
   6.37's set, at my word, so no seed was chosen after a result (R-162). Rule 1 on R-016's own
   three seeds (82, 83, 94) is in section 7 and is met in every condition.
2. *A brief's word count* (R-163, disclosure 1): the judges' brief named "two files" instead of
   "these five files", to match the files given.
3. *The judge audit tightened during condition A* (R-163, disclosure 2): counting commands were
   allowed; one judge's command was read and filed by hand.
4. *A duplicate line in the judge list* (R-163, disclosure 3), removed before the record.
5. *Fields added to the scorer after the run* (R-163, disclosure 4): reported fields only; every
   earlier value unchanged, no rule changed.
6. *The first outside-writer set became a development set* (R-151), when 7 was designed from its
   failures. 6.37's result on it was measured before that.
7. *R-016's references were left out of the sealed run and run late.* R-016 lists `whole_chat`
   and `always_search` as references to report beside the rules; R-162 ran neither and did not say
   so, and the omission was first disclosed in R-167, after the write-up's reviewer found it. The
   pass rules did not depend on them, so R-163's pass stands. Both were then run, on base only:
   the whole chat on the outside-writer sets (R-164, R-165) and on the sealed conversations at 58
   messages (R-168; at 419 it does not fit under the memory cap), and `always_search` on the sealed
   conversations at both sizes (R-168) and on the outside-writer sets (R-169). This read each
   sealed pool a second time, by base only; nothing chosen from these runs can change the frozen
   model (sections 6 and 7).
8. *No exact interval on the coherence difference.* R-016 asks for the paired disagreement counts
   and an exact 95% interval on the coherence difference; R-163 reports counts per model only
   (R-167).
9. *The training recipe differs from R-016's.* R-016 registered LoRA r = 16 on the attention
   projections, learning rate 2e-4 and 750 rows (R-016, R-018). 6.37 is rank
   32 on all seven projections, learning rate 3e-4,
   1,094 rows, with the loss on the taught turns only (R-044, R-046, R-052, R-076,
   R-127). Each change has its own record; none was listed as a deviation before R-167.
10. *LoCoMo* was registered as an outside check (R-100), deferred (R-139 item 6) and never run
    (R-167).

## 6. Results on the outside-writer sets: whole chat, plain code or search

Every result in this section is on the two outside-writer sets. The generated sealed pools give a
different answer on the whole chat (section 7).

On the outside-writer sets, `older` questions (R-164, R-165; one seed, 40 chats a set; in brackets,
the paired counts against base with the whole chat):

| Set | Base, last three exchanges and the tool | 6.37, last three exchanges and the tool | Base, whole chat | 6.37, whole chat (only base right, only 6.37 right, sign test) | 6.37, whole chat and the tool (the same, against base with the whole chat) |
|---|---|---|---|---|---|
| Set 1 | 11 | 28 | 58 | 59 (8, 9, p = 1.0) | 57 (12, 11, p = 1.0) |
| Set 2 | 12 | 34 | 52 | 56 (10, 14, p = 0.54) | 54 (12, 14, p = 0.85) |

Figure 1, at the top, plots these counts. Base with every message in view beats 6.37 working from the last three exchanges on both sets
(set 1: 36 right only for base with the whole chat and 6 only for 6.37 with the tool, p = 2.8 × 10<sup>-6</sup>; set 2: 28 right only for base with the whole chat and 10 only for 6.37 with the tool, p = 0.0051; R-164). Given the whole chat, 6.37 and base
show no measured difference (one seed, two sets of 40 chats; gaps under about 15 points on a kind of 40 questions are below what this test resolves, R-142), with or without the tool (R-165): no measured damage to how the model uses the context it
can see.

Every kind, base with the whole chat and no tool (`whole_chat_all`) against 6.37 with the whole chat
and the tool (`whole_chat_tool`), with both models' scores from the last three exchanges beside
them (R-165):

| Set | Kind (questions) | Base, whole chat | 6.37, whole chat and the tool | Only base right, only 6.37 right, sign test | 6.37, last three exchanges and the tool | Base, last three exchanges and the tool |
|---|---|---|---|---|---|---|
| 1 | `older` (80) | 58 | 57 | 12, 11, p = 1.0 | 28 | 11 |
| 1 | `confirm` (40) | 13 | 14 | 6, 7, p = 1.0 | 11 | 15 |
| 1 | `in_view` (40) | 35 | 35 | 1, 1, p = 1.0 | 35 | 36 |
| 1 | `never_told` (40) | 31 | 35 | 3, 7, p = 0.34 | 37 | 34 |
| 1 | `statement` (40) | 40 (no tool, so right by construction) | 39 | 1, 0, p = 1.0 | 37 | 38 |
| 2 | `older` (80) | 52 | 54 | 12, 14, p = 0.85 | 34 | 12 |
| 2 | `confirm` (40) | 13 | 13 | 6, 6, p = 1.0 | 19 | 15 |
| 2 | `in_view` (40) | 32 | 36 | 2, 6, p = 0.29 | 37 | 34 |
| 2 | `never_told` (40) | 28 | 27 | 8, 7, p = 1.0 | 36 | 32 |
| 2 | `statement` (40) | 40 (no tool, so right by construction) | 37 | 3, 0, p = 0.25 | 35 | 39 |

No kind differs near significance (smallest p = 0.25). The largest gap is `statement` on
set 2, 37 of 40 for 6.37: 3 needless searches, where base
cannot search at all. With the whole chat in view the trained model searches far less on `older`
and `confirm`, but still searches about half the `never_told` questions: set 1, `older` 15 of 80 (with the last three exchanges: 80), `confirm` 0 of 40 (9), `never_told` 22 of 40 (40); set 2, `older` 13 of 80 (with the last three exchanges: 78), `confirm` 0 of 40 (12), `never_told` 24 of 40 (40). On set 2,
`never_told` falls to 27 and `confirm` to 13 with the whole chat,
against 36 and 19 from the last three exchanges; base with
the whole chat is as low (28 and 13), so the drop comes with
having the whole chat in view, not with training (R-165).

Tokens read per turn: set 1, base with the whole chat 1,399, 6.37 with the last three exchanges and the tool 1,707, 6.37 with the whole chat and the tool 1,948; set 2, base with the whole chat 1,401, 6.37 with the last three exchanges and the tool 1,690, 6.37 with the whole chat and the tool 1,945 (R-164; whole-chat-and-tool from the raw runs). On chats this
short, reading the whole chat costs fewer tokens than searching, not more.

**Code that always searches** (R-169). R-016 registered it as a reference: code makes the first
search on every turn, with the newest message as the query, and hands base the passages; base can
then search again or answer. The last three exchanges are in view, and nothing is trained
(`scripts/run_recall_eval.py`). It was left out of the sealed run (R-167) and run
late on both outside-writer sets, seed 0, on the same questions as the other arms (registered
before it ran: if it is at or above seed 82 on recall, training adds nothing to recall over plain
code on these chats). Each kind, with seed 82's paired counts against code in brackets (sign tests
on the kinds other than recall were computed for this write-up from the same runs). One table a
set, each with base with the whole chat beside code and seed 82:

| Set 1: kind (questions) | Code always searches | Seed 82, tool (only code right, only seed 82 right, sign test) | Base, tool | Base, whole chat |
|---|---|---|---|---|
| recall (`older` and `confirm`, 120) | 42 | 39 (22, 19, p = 0.76) | 26 | 71 |
| `older` (80) | 23 | 28 (9, 14, p = 0.4) | 11 | 58 |
| `confirm` (40) | 19 | 11 (13, 5, p = 0.096) | 15 | 13 |
| `in_view` (40) | 13 | 35 (1, 23, p = 3.0 × 10<sup>-6</sup>) | 36 | 35 |
| `never_told` (40) | 31 | 37 (2, 8, p = 0.11) | 34 | 31 |
| `statement` (40) | 0 (wrong by construction) | 37 | 38 | 40 (right by construction) |

| Set 2: kind (questions) | Code always searches | Seed 82, tool (only code right, only seed 82 right, sign test) | Base, tool | Base, whole chat |
|---|---|---|---|---|
| recall (`older` and `confirm`, 120) | 47 | 53 (19, 25, p = 0.45) | 27 | 65 |
| `older` (80) | 24 | 34 (10, 20, p = 0.099) | 12 | 52 |
| `confirm` (40) | 23 | 19 (9, 5, p = 0.42) | 15 | 13 |
| `in_view` (40) | 16 | 37 (0, 21, p = 9.5 × 10<sup>-7</sup>) | 34 | 32 |
| `never_told` (40) | 24 | 36 (2, 14, p = 0.0042) | 32 | 28 |
| `statement` (40) | 0 (wrong by construction) | 35 | 39 | 40 (right by construction) |

On recall, code is above seed 82 on set 1 (22 right only for code and 19 only for seed 82, p = 0.76) and below on set 2 (19 right only for code and 25 only for seed 82, p = 0.45):
no measured difference on either set. Set 1 meets the registered outcome: on these chats, training
adds nothing measured to recall over plain code that searches every turn. Base with the tool
searches too little and code searches every turn; training adds searching when the answer is out
of view (against base) and not searching when it is in view (against code). On plain chat lines
seed 82 is below base with the tool on both sets (37 against 38, 35 against 39). Code,
which searches even when the answer is on screen, answers
`in_view` far worse (13 and 16 against 35 and
37). It does worse on `never_told` (31 and
24 against 37 and 36; sign test p =
0.11 on set 1 and 0.0042 on set 2). It fails every `statement` by construction, since that kind is scored on not
searching. Base with the whole chat is above both on recall.

**What is not measured.** Base with the whole chat on 419-message generated chats, which run about
6,236 tokens on `hard_dev` and 5,409 on `probe`. At 58 messages it was
run late on the sealed pools (R-168, section 7). The R-164 runs on `hard_dev` and `probe` were
registered and have no results, because they ran out of card memory (R-166; the queue log is
`results/control/R-164/wc_hd_base_oom.log`). The `hard_dev` run failed three tries with
`torch.OutOfMemoryError`: it asked for 2.35 GiB more with 6.84 GiB already
allocated and 8.50 GiB allowed, the cap these runs use (`--max-vram-fraction 0.85` of a
10 GB card, `scripts/records/queue/wc.sh`). The `probe` run failed the same way on its first try
(1.77 GiB more, 6.74 allocated); it was started three
times, tries 2 and 3 show no error line in the log, and try 3 shared the card with another run and
was stopped (R-166). Both pools hold 58- and 419-message
chats, and R-166 reads the failure as the whole 419-message chat not fitting under the cap. With the
three-exchange view, every run in the sealed run, base and adapters, peaked at 6.71 to 7.02
GiB on chats of the same two sizes (R-163). Earlier whole-chat runs at 419 messages, before any cap,
peaked at 11.22 and 11.62 GiB, more than the card holds (R-014, R-017); 6.37's
whole-chat runs on the outside-writer sets peaked at 7.11 to 7.59 GiB.

The only whole-chat readings at 419 messages are two development runs on the training pool, both
uncapped, and neither is a ceiling. R-014: 2 of 40 right at 419 messages against
31 of 40 at 58, ruled not valid because most replies copied the repeated scripted small
talk. R-017, after the small talk was varied: 0 of 12 `older` questions right at 419 messages
against 8 of 12 at 58, failing its own control. A low score at 419 messages agrees with the
model's sliding window but does not show it is the cause (R-017, R-164).

**Code that always searches, before the late runs.** In development, on the training pool, R-014's
`always_search` arm answered 28 of 40 at 419 messages, against the whole chat's
2 of 40, and 34 of 40 at 58. In R-017 it answered
5 of 24 facts in view (base with no tool 22 of 24) and
0 of 24 plain-chat lines without a search (base with no tool
24 of 24), because it searches on every turn. The late runs above (R-169)
and on the sealed pools (R-168, section 7) show the same cost on facts in view.

## 7. Results: the sealed run

Every rule passes in every condition. Recall, rule 1 (counts of right answers, `older` and
`confirm`; Figure 2, at the top, plots them beside the outside-writer sets):

| Condition | Base, 58 messages | Eight adapters pooled, 58 | Points | Base, 419 messages | Eight adapters pooled, 419 | Points | Gain, 95% interval resampling conversations (points) |
|---|---|---|---|---|---|---|---|
| A, `heldout`, 1 decoy | 17 of 60 (28.3%) | 426 of 480 (88.8%) | +60.4 | 15 of 60 (25.0%) | 409 of 480 (85.2%) | +60.2 | +50.8 to +69.7 |
| B, `heldout`, 4 decoys | 15 of 60 (25.0%) | 434 of 480 (90.4%) | +65.4 | 14 of 60 (23.3%) | 409 of 480 (85.2%) | +61.9 | +54.4 to +72.8 |
| C, `independent`, 1 decoy | 10 of 60 (16.7%) | 434 of 480 (90.4%) | +73.8 | 11 of 60 (18.3%) | 429 of 480 (89.4%) | +71.0 | +64.9 to +79.4 |
| D, `independent`, 4 decoys | 5 of 60 (8.3%) | 434 of 480 (90.4%) | +82.1 | 8 of 60 (13.3%) | 424 of 480 (88.3%) | +75.0 | +71.9 to +84.6 |

The results are R-163's. The gain is 60 to 82 points at each size against the 20 required; the registered sign
test is met in every condition, p below 0.01. Base is low here (8.3 to 28.3%), so ratios
over it are unstable and are not given. **Rule 2** (R-041): every right adapter answer came from a
search that found the fact, and so did every right base answer, so rule 2's numbers equal rule 1's
in every condition.

**Rule 3**, false retrievals (a reply naming a wrong value of the fact asked about):

| Condition | Base | Eight adapters | Seed 82 |
|---|---|---|---|
| A | 12 | 0 to 2 | 0 |
| B | 23 | 0 to 11 | 0 |
| C | 24 | 3 to 9 | 7 |
| D | 24 | 0 to 9 | 4 |

**Rule 4**, coherent replies (judge 1 decides; judges 2 and 3 reported). Every adapter is above base
under every judge:

| Condition | Conversations judged | Judge 1 (decides): base / eight adapters / seed 82 | Judge 2 | Judge 3 |
|---|---|---|---|---|
| A | 300 | 173 / 264 to 288 / 282 | 167 / 267 to 283 / 269 | 166 / 258 to 281 / 277 |
| B | 120 | 59 / 105 to 113 / 105 | 59 / 104 to 113 / 105 | 61 / 106 to 114 / 108 |
| C | 120 | 75 / 108 to 116 / 114 | 65 / 109 to 114 / 114 | 72 / 107 to 116 / 109 |
| D | 120 | 71 / 110 to 116 / 115 | 77 / 110 to 117 / 115 | 73 / 109 to 116 / 116 |

Base here has the search tool in its prompt; R-017 found the tool alone lowers the untrained
model's ordinary talk, so rule 4 compares with that base. In development, 6.37 was also judged
against base with no tool on plain chat and facts in view, and was at or above it (R-128, R-130).

**R-016's three seeds.** Rule 1 recomputed on seeds 82, 83 and 94, the test as first registered:

| Condition | 58 messages: base → seeds 82, 83, 94 pooled (points) | 419 messages | Rule 1 |
|---|---|---|---|
| A | 28.3% → 88.9% (+60.6) | 25.0% → 85.6% (+60.6) | met |
| B | 25.0% → 90.6% (+65.6) | 23.3% → 85.6% (+62.2) | met |
| C | 16.7% → 84.4% (+67.8) | 18.3% → 82.2% (+63.9) | met |
| D | 8.3% → 85.0% (+76.7) | 13.3% → 80.6% (+67.2) | met |

**Seed 82 beside the eight.** Recall of 120 for each seed (82, 83, 94 to 99):
A, 106, 104, 104, 106, 101, 102, 107, 105; B, 107, 105, 105, 107, 102, 103, 108, 106; C, 92, 109, 99, 116, 108, 108, 120, 111; D, 91, 109, 98, 116, 108, 108, 119, 109. Seed 82 against base: 106 against 32 (A), 107 against 29 (B), 92 against 21 (C), 91 against 13 (D); its sign test is below 0.01
in each. On `heldout` it is level with the other seeds. On `independent` it is the lowest of the
eight, most of all on `confirm` (42 of 60 in C and 40 of 60 in D, against up to
60): it found the fact in 111 and answered 92 right (C) and found the fact in 111 and answered 91 right (D), so most misses there are facts it found
and did not use (R-163).

**`older` and `confirm` apart** (of 60 a model; pooled of 480):

| Condition | `older`: base | seed 82 | eight seeds | eight pooled | `confirm`: base | seed 82 | eight seeds | eight pooled |
|---|---|---|---|---|---|---|---|---|
| A | 26 | 56 | 54 to 57 | 446 of 480 | 6 | 50 | 45 to 50 | 389 of 480 |
| B | 23 | 56 | 54 to 57 | 446 of 480 | 6 | 51 | 46 to 51 | 397 of 480 |
| C | 15 | 50 | 50 to 60 | 440 of 480 | 6 | 42 | 42 to 60 | 423 of 480 |
| D | 11 | 51 | 50 to 59 | 440 of 480 | 2 | 40 | 40 to 60 | 418 of 480 |

**The other kinds** (of 60):

| Condition | `in_view`: base / seed 82 / eight seeds | `never_told`: the same | `statement`: the same |
|---|---|---|---|
| A | 55 / 59 / 50 to 59 | 54 / 60 / 60 | 38 / 59 / 52 to 60 |
| B | 56 / 59 / 50 to 59 | 47 / 60 / 57 to 60 | 38 / 59 / 52 to 60 |
| C | 43 / 57 / 49 to 59 | 50 / 55 / 51 to 57 | 52 / 56 / 55 to 60 |
| D | 45 / 57 / 49 to 59 | 54 / 59 / 52 to 60 | 52 / 56 / 55 to 60 |

Below base, in the sealed run: on `in_view` in `heldout`, 8 of the 16 adapter runs
score below base, so some seeds lose a few questions whose answer is in view (R-163); every kind
where any seed is below base is listed at the end of section 8.

**Behaviour**, reported beside the rules (right search decisions of 300). A
clean first call is a reply that parses whole as one `search_corpus` call with nothing before or
after it. It is counted of the replies that searched, so base's and seed 82's counts have different
denominators, and an unclean call still ran its search: the count is a format measure, not a count
of failed searches (R-008).

| Measure | A | B | C | D |
|---|---|---|---|---|
| Right search decisions: base | 180 | 180 | 193 | 193 |
| Right search decisions: seed 82 | 298 | 298 | 296 | 296 |
| Right search decisions: eight seeds | 283 to 300 | 283 to 300 | 294 to 300 | 294 to 300 |
| Clean first calls: base | 52 of 136 | 52 of 136 | 49 of 107 | 49 of 107 |
| Clean first calls: seed 82 | 180 of 180 | 180 of 180 | 184 of 184 | 184 of 184 |
| Ran out of calls: base | 1 | 2 | 3 | 3 |
| Ran out of calls: all eight adapters | 0 | 0 | 0 | 0 |
| Seed 82 recall: fact found / right | 106 / 106 | 107 / 107 | 111 / 92 | 111 / 91 |

These right decisions are on generated chats. On the outside-writer sets seed 82 is below base on
`statement` (37 against 38 and 35 against 39, section 8).

**R-016's two references, run late** (R-167, R-168). Registered in R-016 and left out of the sealed
run, they were run afterwards on base only, on the same sealed conversations (item seed 90311),
registered before they ran: base with every message in view and no tool (`whole_chat_all`, every
kind) at 58 messages only, because at 419 it does not fit under the memory cap (R-166), and code
that always searches (`always_search`) at both sizes. Recall (`older` and `confirm`, of
60 at each size), with base with the tool and the adapters from the sealed run on
the same conversations:

| Recall (of 60 a size), or false retrievals | A | B | C | D |
|---|---|---|---|---|
| Base, whole chat, no tool, 58 messages | 33 | 28 | 21 | 22 |
| Code always searches, 58 messages | 32 | 31 | 20 | 15 |
| Code always searches, 419 messages | 32 | 30 | 17 | 14 |
| Base, tool, 58 messages | 17 | 15 | 10 | 5 |
| Base, tool, 419 messages | 15 | 14 | 11 | 8 |
| Seed 82, tool, 58 messages | 54 | 55 | 46 | 47 |
| Seed 82, tool, 419 messages | 52 | 52 | 46 | 44 |
| Eight adapters, tool, 58 messages | 51 to 55 | 52 to 56 | 46 to 60 | 47 to 60 |
| Eight adapters, tool, 419 messages | 49 to 52 | 49 to 52 | 46 to 60 | 44 to 59 |
| False retrievals: base, whole chat (58 messages only) | 7 | 16 | 9 | 16 |
| False retrievals: code always searches (both sizes) | 42 | 56 | 53 | 69 |

Seed 82 is far above both references in every condition and size: every exact sign test is below
0.001 (the largest p is 3.2 × 10<sup>-4</sup>, rounded; only the reference right on 1 to 7 questions, only seed 82 on
23 to 33). On these generated chats, then, training adds more than plain code that
searches every turn, and the whole chat does not win: base reading the whole 58-message chat
(1,105 to 1,332 tokens, about the outside-writer chats' length) answers 21 to 33 of
60, against seed 82's 46 to 55. This is the opposite of the outside-writer
result (section 6). R-014 recorded a likely cause on generated chats: base copies their repeated
scripted small talk. The false retrievals in the table compare with 0 to 11 for
each adapter over both sizes (rule 3 above). On facts in view, code that always searches answers
2 to 11 of 30 against seed 82's 28 to 30; base with the whole chat answers 16 to 21, below
base with three exchanges and the tool (21 to 27), so seeing more of these chats makes
base worse at what is in front of it. `statement` is scored on the call count, so code fails every
one and the whole chat passes every one by construction; neither is read.

## 8. Results: the outside-writer sets, against base with the tool

Recall (`older` and `confirm`, of 120) with the last three exchanges in view, one
column a set:

| Recall (of 120) | Set 1 | Set 2 |
|---|---|---|
| Base, tool | 26 | 27 |
| 6.37 seed 82, tool | 39 | 53 |
| Only base right, only seed 82 right, sign test | 12, 25, p = 0.047 | 9, 35, p = 1.1 × 10<sup>-4</sup> |
| Seed 82 gain, 95% interval resampling chats (points) | +2.5 to +19.2 | +13.3 to +30.0 |
| Each seed (82, 83, 94 to 99) | 39, 43, 57, 46, 48, 52, 46, 50 | 53, 53, 47, 56, 51, 56, 56, 44 |
| Eight seeds pooled, gain interval (points) | +9.7 to +26.1 | +12.9 to +28.3 |

The counts are in R-146 (set 1), R-157 (set 2) and R-164. On set 1 seed 82's gain is +10.8 points and its sign test p = 0.047, above the
registered 0.01; it is the lowest of the eight on that set. On set 2 it is +21.7 points, p =
1.1 × 10<sup>-4</sup>. The eight seeds pooled gain +18.0 and +20.8 points. Both
sets' gains are far below the generator's: on `hard_dev` the same seed goes from 20 to
73 of 96 (R-141, R-164). The eight seeds are runs over the same questions, not
independent cases (R-137). Each set has only 4 writers, all one model family, and the
intervals resample chats, not writers (R-142):

| Set | Recall per writer: base / seed 82 / eight seeds |
|---|---|
| Set 1 | w1: 6 / 11 / 11 to 16; w2: 7 / 10 / 10 to 17; w3: 7 / 9 / 9 to 16; w4: 6 / 9 / 7 to 9 (of 30 each) |
| Set 2 | x1: 6 / 10 / 7 to 12; x2: 4 / 14 / 11 to 15; x3: 8 / 14 / 11 to 15; x4: 9 / 15 / 14 to 17 (of 30 each) |

Seed 82 is above base in every writer's chats on both sets.

**Each kind** (R-146, R-157):

| Set | `older`: base / seed 82 / eight seeds | `confirm`: base / seed 82 / eight seeds | `in_view`: base / seed 82 / eight seeds | `never_told`: base / seed 82 / eight seeds | `statement`: base / seed 82 / eight seeds |
|---|---|---|---|---|---|
| Set 1 | 11 / 28 / 26 to 35 of 80 | 15 / 11 / 11 to 22 of 40 | 36 / 35 / 32 to 37 of 40 | 34 / 37 / 33 to 39 of 40 | 38 / 37 / 33 to 39 of 40 |
| Set 2 | 12 / 34 / 28 to 42 of 80 | 15 / 19 / 11 to 23 of 40 | 34 / 37 / 36 to 40 of 40 | 32 / 36 / 31 to 36 of 40 | 39 / 35 / 30 to 36 of 40 |

The gain is nearly all `older` (28 against 11 and 34 against 12). On `confirm` seed 82 is below
base on set 1 (11 against 15) and above on set 2 (19 against 15). On `statement` it is below
base on both sets (37 against 38, 35 against 39): it searched on chat lines where base did
not (R-146, R-157).

**Every kind where seed 82 or any seed is below base** (outside-writer sets and sealed run, counts
of right answers; R-146, R-157, R-163): set 1 `confirm`: seed 82 11 against base's 15; three of the eight seeds below base (11 to 14); set 1 `in_view`: seed 82 35 against base's 36; six of the eight seeds below base (32 to 35); set 1 `never_told`: seed 82 37 against base's 34; one of the eight seeds below base (33); set 1 `statement`: seed 82 37 against base's 38; six of the eight seeds below base (33 to 37); set 2 `confirm`: seed 82 19 against base's 15; three of the eight seeds below base (11 to 14); set 2 `never_told`: seed 82 36 against base's 32; one of the eight seeds below base (31); set 2 `statement`: seed 82 35 against base's 39; eight of the eight seeds below base (30 to 36); sealed A `in_view`: seed 82 59 against base's 55; four of the eight seeds below base (50 to 53); sealed B `in_view`: seed 82 59 against base's 56; four of the eight seeds below base (50 to 53); sealed D `never_told`: seed 82 59 against base's 54; two of the eight seeds below base (52).

**Tag questions.** Half the `confirm` questions claim the right value and half a wrong one (R-142).
6.37 rarely searches a tag question (set 1: 9 of 40, base 5; set 2:
12 of 40, base 2) and mostly agrees with the claim:

| Set | True claims confirmed: base / seed 82 | False claims corrected: base / seed 82 | False claims corrected, eight seeds | Tag questions searched: base / seed 82 |
|---|---|---|---|---|
| Set 1 | 14 / 10 of 20 | 1 / 1 of 20 | 0 to 7 | 5 / 9 |
| Set 2 | 15 / 16 of 20 | 0 / 3 of 20 | 0 to 8 | 2 / 12 |

So seed 82 goes along with most false claims: it corrects 1 and
3 of 20, about as often as base. 7.1, trained to search tag questions, searched nearly all of them and grounded every right
answer, but did not raise recall and failed a development line (R-157, R-158).

**The prompted baseline.** Two fixed system prompts on base, written before any result: A states
five rules, B adds four worked examples (R-137, R-161). Recall:

| Recall (of 120) | Set 1 | Set 2 |
|---|---|---|
| Base | 26 | 27 |
| Base, prompt A (rules) | 19 | 18 |
| Base, prompt B (rules and four worked examples) | 15 | 20 |
| 6.37 seed 82 | 39 | 53 |
| Prompt A against seed 82: only A right, only 6.37 right, sign test | 8, 28, p = 0.0012 | 4, 39, p = 3.1 × 10<sup>-8</sup> |
| Prompt B against seed 82 (the same) | 8, 32, p = 1.8 × 10<sup>-4</sup> | 5, 38, p = 2.5 × 10<sup>-7</sup> |

Both prompts lower base's recall on both sets: they make base search less. For these two prompts, a
written prompt does not buy the gain. A search over prompts was not tried.

**Where seed 82's wrong answers go wrong** (R-139's stages, R-146, R-157):

| Set | Wrong recall answers, seed 82 | Did not search | Searched, the fact not found | Named a listed wrong value | Found the fact, wrong otherwise |
|---|---|---|---|---|---|
| Set 1 | 81 | 23 | 38 | 6 | 14 |
| Set 2 | 67 | 17 | 36 | 5 | 9 |

The leading stage on both sets is a search that missed the fact. Read by hand (R-146): a tag
question does not trigger a search; queries reuse training wording ("aunt keeps animals yard") and
miss; a fact told with a pronoun ("she has a cockatiel") cannot be matched by a search for the
relation; and a found fact is answered from the line's first clause. On set 1, most misses state
something false, usually another person's fact from the found passage (R-146); on `hard_dev` almost
none did (R-144). The scorer checks only the answer on questions whose writer listed no wrong value;
on the questions that list one, seed 82 gets 31 against 19 of 88 (set 1) and 41 against 18 of 84
(set 2) (R-143, R-152).

## 9. Results: LongMemEval-S, an outside check

**A third kind of chat.** LongMemEval-S (Wu et al., 2025) holds user-to-assistant chats, partly
real logs and partly model-simulated: 500 questions, each over its own history of
244 (197 to 305) exchanges at the median, far more than the model's 8,192 tokens
hold. Its chats are unlike both the generated pools and the outside-writer sets, so its numbers are
never pooled with theirs. It is an outside check, never a decision: the model stayed frozen. The
plan was panelled and registered before any run, and each adaptation below is a
listed deviation from LongMemEval's own setup (R-170):

- The system prompt is the one 6.37 was trained with, "You are chatting with a friend", and these
  chats are a user talking to an assistant: a mismatch.
- Turns are paired into exchanges in order; a turn that does not pair is joined to its neighbour
  (1,932 turns, 1,900 of them across a session boundary). Each user text carries its session date, and the question its question date.
- Every arm sees the last three exchanges (a view of 1,941 tokens at the median, at most
  4,900). Everything earlier is indexed with the same tool, top 5. Passages are
  cut into 400-character chunks, so one exchange becomes 7 chunks at the median
  (116,939 of 120,932 older exchanges become more than one), and the top 5 can hold
  several chunks of one exchange.
- Replies are capped at 60 tokens, as in every other test here.
- The official score uses a GPT-4o judge, which was not available. The mechanical measures below
  and the judged accuracy after them are not the official score, and no ranking against published
  systems is made.

**Arms**, one at a time on the card: 6.37 seed 82 with the tool; base with the tool; code that
always searches first (base; its query is the question without its date); base with three
exchanges and no tool; and base reading only the sessions that hold the evidence (every message in
them in view, no tool), on evidence prompts under 4,000 tokens, as a reading
ceiling that tells failed search apart from failed reading.

**Mechanical measures** (476 questions with marked evidence outside the
3 whose evidence is in view; 411 questions whose gold answer can be
matched; 30 unanswerable questions):

| Measure | 6.37 seed 82, tool | base, tool | code always searches | base, three exchanges, no tool |
|---|---|---|---|---|
| Searched (of the questions with marked evidence it completed) | 421 of 466 | 309 of 460 | 450 of 450 | no tool |
| Evidence found by the first search (of 476; a failure or no search counts as not found) | 333 | 238 | 372 | no tool |
| Gold answer in the reply (of 411 read; a failure counts as wrong) | 51 | 51 | 63 | 34 |
| False matches (reply scored against another question's gold) | 1 of 402 | 7 of 398 | 2 of 389 | 4 of 408 |
| Declines, 30 unanswerable | 21 | 2 | 0 | 10 |
| Declines, 470 answerable | 233 | 22 | 1 | 140 |
| Clean first calls | 441 of 441 | 146 of 328 | 472 of 472 (scripted) | no tool |
| Ran out of calls | 0 | 12 | 31 | no tool |
| Words a reply / replies at the 60-token cap | 12.7 / 22 of 490 | 39.1 / 177 of 484 | 40.4 / 178 of 472 | 45.6 / 338 of 497 |
| Tokens read / seconds a question | 4,055 / 3.81 | 3,794 / 3.47 | 3,161 / 3.09 | 1,730 / 2.09 |
| Failures, before / after the rerun | 21 / 10 | 31 / 16 | 58 / 28 | 8 / 3 |

Two references on the CPU: a search on the question text finds the evidence at its top 5
for 395 of 476, and 5 random passages for 22 of 476. Base reading only
the evidence (123 completed, 372 skipped; the gold in 63 of 114 replies) shows the short questions are answerable when the evidence is
in view; on those same questions the gold is in the reply for 6.37 with the tool 28, base with the tool 19, code that always searches 23, base with three exchanges 6.

**The registered hypotheses.**
- **H1, 6.37 above base with the tool on evidence found by the first search: holds, but only
  because 6.37 searches more often.** 333 against 238 of 476 (+20.0 points, 95% interval +14.9 to +25.2, p = 1.5 × 10<sup>-13</sup>); on the questions every arm completed,
  321 against 234 of 447 (+19.5 points, 95% interval +14.3 to +24.6, p = 2.5 × 10<sup>-12</sup>). On the questions both searched, 226 and 226 of 294, p = 1.0: when both search, their
  searches find the evidence equally often. 6.37 searched 90% against 67% of the time, and
  its first calls were clean on 441 of 441, against base's 146 of 328 (of the questions
each searched, so the denominators differ; a format measure, since an unclean call still ran its
search).
- **H2, 6.37 against code that always searches: code finds more evidence; no measured difference
  in answers.** First search, 333 against 372 of 476 (-8.2 points, 95% interval -12.6 to -3.8, p = 4.0 × 10<sup>-4</sup>); over all searches, 333 against 375. Gold answer
  in the reply, 51 against 63 of 411 (-2.9 points, 95% interval -7.1 to +1.2, p = 0.2).
- **H3, 6.37's abstention not more than 5 points below base's: holds.** On the unanswerable
  questions, 21 against 2 of 30 (+63.3 points, 95% interval +43.3 to +83.3, p = 2.1 × 10<sup>-5</sup>). Beside it, as registered, declines on the answerable questions:
  233 against 22 of 470 (+44.9 points, 95% interval +39.8 to +49.8, p = 3.7 × 10<sup>-50</sup>). So 6.37 declines 233 of the 470 questions it
  should answer, and its gold answers equal base's (51 and 51).
- Every arm finds the gold answer in few replies (34 to 63 of 411 for the four arms that ran
  every question). That is low, but not near zero.

**Judged accuracy, not the official score.** LongMemEval's own per-type judge prompts (its
`evaluate_qa.py`, MIT licence), given to three fresh Claude Sonnet judges blind to the arm, R-154's
method; judge 1 decides and judges 2 and 3 are reported. The judged lines are every arm's reply on
the 148 single-session-user and knowledge-update questions (the types 6.37 was trained
for: what the user said, including facts that changed), plus a fixed random 100 of the rest. A
failure has no line and counts as wrong. I (the author, not an independent marker) marked a random
50 lines blind before any judged number was read; no second marker was used here.

| Judged right (questions) | 6.37 seed 82, tool | base, tool | code always searches | base, three exchanges, no tool | base, evidence only |
|---|---|---|---|---|---|
| single-session-user and knowledge-update (148) | 43 | 26 | 32 | 11 | 30 (of its 71 lines) |
| a fixed random sample of the rest (100) | 10 | 8 | 8 | 2 | 17 (of its 71 lines) |
| all judged questions (248) | 53 | 34 | 40 | 13 | 47 (of its 71 lines) |

- 6.37 against base with the tool: 53 against 34 of 248 (+7.7 points, 95% interval +2.0 to +13.3, p = 0.014). On the 148 core questions
  43 against 26, p = 0.012; on the questions every arm completed 51 against 33 of 234, p = 0.018.
- 6.37 against code that always searches: 53 against 40 of 248 (+5.2 points, 95% interval -0.8 to +11.3, p = 0.12). Core 43 against 32, p = 0.14.
  No measured difference.
- Judges 2 and 3 give the same counts as judge 1 within 2 on every cell. The
  judges agree with each other on 1,027 to 1,030 of 1,035 lines (kappa 0.97 to 0.98).
- On my blind lines, I agree with each judge on 46 of 50 (kappa 0.78); I marked 12 of them right, and judge 1 marked 12.

**Added after reading the registered result, and disclosed as such:** the same marks split into
answerable and unanswerable questions.

| Judged right | 6.37 seed 82, tool | base, tool | code always searches | base, three exchanges, no tool |
|---|---|---|---|---|
| 233 answerable | 40 | 32 | 40 | 8 |
| 15 unanswerable | 13 | 2 | 0 | 5 |

On the 233 answerable questions, 6.37 ties code that always searches
(40 against 40; 23 right only for 6.37 and 23 only for code that always searches, p = 1.0) and shows no measured difference from base with the tool
(40 against 32; 26 right only for 6.37 and 18 only for base with the tool, p = 0.29). Of 6.37's 19-question judged lead over base,
11 come from the 15 unanswerable questions, where code never
declines.

**Where my marks and the judges differ.** The three judges agree with each other on every one of my
lines, and I differ from them on four: one `single-session-preference` line from base with the tool, which I marked right and the judges wrong; one `temporal-reasoning` line from base with the tool, which I marked right and the judges wrong; two unanswerable lines from base with three exchanges, which I marked wrong and the judges right. On the unanswerable
lines my rule is that a reply which cannot answer because it is a language model without access to
the user's data is a failure, not a correct abstention; LongMemEval's abstention prompt accepts a
reply that says the information is incomplete, and the judges marked such replies right. The
registered result stands, and a re-judging under my rule was built and dropped at my word before
any judge saw it (R-170). How far my rule would move the counts was estimated in R-170 from the raw
replies, which are not committed; that estimate is not repeated here.

**Out of card memory.** Every failure in every arm was `torch.OutOfMemoryError`, under the same cap
as the other runs (8.50 GiB). The longest views, with a search's passages added, do not
fit (first-pass peaks 8.37 to 8.44 GiB). As amended before any score was read, each arm's failed
questions ran once more at `--max-vram-fraction 0.90` and nothing else changed (peaks
8.79 to 8.93 GiB); a question that failed again stays a failure, counted as wrong. Failures
before and after the rerun: 6.37 with the tool 21 to 10; base with the tool 31 to 16; code that always searches 58 to 28; base with three exchanges 8 to 3; base reading only the evidence 30 to 5.

**Reading.** On this third kind of chat, with the last three exchanges in view, training made the
model search more often, with clean first calls every time (a format measure), and decline far
more, including on
233 of the 470 questions it should answer. Plain code that searches on every question finds the evidence
more often than 6.37 and is faster (3.09 s a question against 3.81), with no measured difference in answers,
mechanical or judged. 6.37 is judged above base with the tool, and most of that lead is the
unanswerable questions.

## 10. Cost

The sealed run's times, on this machine (an RTX 3080, 10 GB, each run with the card to itself),
one column a condition:

| Measure | A | B | C | D |
|---|---|---|---|---|
| Base: seconds, per conversation | 389, 1.30 | 385, 1.28 | 381, 1.27 | 434, 1.45 |
| Seed 82: seconds, per conversation | 535, 1.78 | 502, 1.67 | 524, 1.75 | 624, 2.08 |
| Eight adapters: seconds per conversation | 1.73 to 2.18 | 1.67 to 1.92 | 1.75 to 2.03 | 2.08 to 2.34 |
| Tokens read per turn, base / seed 82 | 1,148 / 1,196 | 1,154 / 1,207 | 1,122 / 1,239 | 1,145 / 1,266 |
| Whole chat, tokens | 3,227 | 3,239 | 3,496 | 3,610 |
| Seed 82 reads, share of the whole chat | 37% | 37% | 35% | 35% |
| Tokens written per turn, base / seed 82 | 37 / 26 | 38 / 26 | 36 / 27 | 37 / 27 |
| Searches per conversation, base / eight adapters | 0.47 / 0.57 to 0.63 | 0.48 / 0.57 to 0.63 | 0.39 / 0.60 to 0.62 | 0.39 / 0.60 to 0.62 |

The counts are R-163's. Seed 82 reads 35 to 37% of the whole chat's tokens a turn and writes
fewer tokens than base. It takes longer per conversation than base because it searches more often,
and each search adds a model call. The sealed run's inference peak, the highest over base and all
eight adapters in the four conditions, was 7.02 GiB of card memory. The 33 judge
runs took 53 to 129 s each, median 80 s (`results/coherence/R-162/judge_times.json`). Training took
33 to 35 minutes a seed, with a training peak of 7.81 to 7.84 GiB for 6.37's eight
seeds. On the outside-writer sets the comparison runs the other way: a chat of about
1,400 tokens costs less to read whole than to search (section 6).

**Code that always searches is faster than 6.37 on every kind of chat it ran on.** Seconds are each
run's wall-clock time over its questions (a sealed conversation holds one question), from separate
runs on the same card:
- sealed pools (R-162, R-168): code that always searches 1.01 to 1.23 s a conversation, seed 82 1.67 to 2.08, base with the tool 1.27 to 1.45;
- outside-writer sets (R-169): code 1.45 to 1.48 s a question, seed 82 1.70 to 1.96, base with the tool 1.21 to 1.31, base with the whole chat and no tool 1.02 to 1.06;
- LongMemEval-S (R-170): code 3.09 s a question against 3.81 for 6.37 (section 9).

On the outside-writer sets base with the tool is faster than code, and base with the whole chat is
the fastest of all.

## 11. How 6.37 was chosen: the candidate ledger

`hard_dev` recall moves between training seeds alone (73 to 90 of 96 for 6.37, R-141) by
more than most changes moved it, and the 40 trained candidate sets below were screened
on reused development pools (`probe`, and all but two also on `hard_dev`), read many times. Every
candidate after v5 is listed, in order, with the line it failed. The records number the candidates read
at seeds 82 and 83 since v6 (R-093); by that count 6.37 is candidate 16 and 7.1 is
the 20th (R-127, R-134). Fix B was run in that time and is outside the records'
count. Before v6, 16 candidates were screened against v5. Screen recall is the
development screen (`probe`, seed 51203) at training seed 82; `hard_dev` is seed 73157 at seed 82;
both are development numbers, read many times.

**Before v6** (v5 stands until 17m):

| # | Candidate (set) | What it changed | How it ended | Screen recall, seed 82 (of 96) | `hard_dev` recall, seed 82 (of 96) | Record |
|---|---|---|---|---|---|---|
| | Base, untrained | | | 38 | 20 | R-017 |
| | v5 (`fix11_all`) | | the reference for this table | 95 | 58 | R-061 |
| | Fix 12 (`fix12_all`) | brief, vetted in-view answers | dropped at the screen gate, recall | 90 | not run | R-063 |
| | Fix 13 (`fix13_all`) | more indirect in-view questions | dropped at the screen gate, recall | 91 | not run | R-064 |
| | Fix 14 (`fix14_all`) | half the fact rows from 47 new fact types (the wide pool) | failed its gate on `statement` and `never_told` | 92 | 76 | R-069, R-071 |
| | Fix 14b (`fix14b_all`) | fix 14, with chat lines naming the wide pool's people | failed on `hard_dev` `never_told` | 92 | 74 | R-073 |
| | Fix 14c (`fix14c_all`) | a quarter of the fact rows from the new types | failed on `hard_dev` `never_told` | 93 | 79 | R-073 |
| | Fix 15 (`fix15_all`) | fix 14c, with never-told rows whose search returns someone else's fact | passed its gate; failed confirmation on judged coherence items | 96 | 81 | R-074, R-075 |
| | Fix 16a (`fix16a`) | the loss on the taught turns only | failed the screen gate on plain-chat coherence | 96 | 70 | R-076, R-077 |
| | Fix 16b (`fix16b`) | the loss on all but the scripted small talk | failed its gate on counts | 87 | 55 | R-079 |
| | Fix 16c (`fix16c`) | fix 16a at learning rate 1e-4 | failed its gate on counts | 93 | 48 | R-079 |
| | Fix 17 (`fix17`) | fix 16c, with plain-chat targets re-vetted on a stricter rubric | failed on counts | 91 | 53 | R-078, R-080 |
| | Fix 17b (`fix17b`) | fix 16a with the strictly vetted targets | failed R-076's rule on a judged sheet at seed 83, and again at fresh seeds 85 to 87 | 94 | 72 | R-082, R-091 |
| | Fix 18a (`fix18a`) | fix 17b, with chat lines that name a fact type | dropped at the screen gate, recall | 94 | 56 | R-083, R-085 |
| | Fix 18c (`fix18c`) | control for 18a: chat lines that name none | dropped at the screen gate, recall | 92 | 66 | R-085 |
| | Fix 19a (`fix19a`) | fix 18a, with questions asked as statements and answered from a search | passed every count; failed the judged check set | 95 | 74 | R-086, R-089 |
| | Fix 20 (`fix20`) | fix 17b, with one fact-word chat line and one indirect question a type | failed several counted lines | 93 | 62 | R-087, R-092 |
| | 17m (**v6**) (`fix17m`) | fix 17b, with plain-chat rows' loss only on the decision and the end marker | passed at 82 and 83 and at fresh seeds 85 to 87: v6 | 95 | 74 | R-088, R-092, R-093 |

**Since v6** (from R-103 on, the version names I gave: 6.1 is v6 plus a first stepping stone, 6.11
a second on top of it, 6.2 a different first stone):

| # | Candidate (set) | What it changed | How it ended | Screen recall, seed 82 (of 96) | `hard_dev` recall, seed 82 (of 96) | Record |
|---|---|---|---|---|---|---|
| 1 | Fix A (`fix17w`) | v6, with its 27 slip-shaped answers rewritten | failed a judged sheet under judge 1 | 96 | 78 | R-094, R-095 |
| not counted | Fix B (`fix17mb`) | v6, with base-written answers' loss only on the first token and end marker | trained and scored at 82 and 83 and counted (R-101); no record states its result | 95 | 75 | R-095, R-101 |
| 2 | Fix C1 (`fix17y`) | fix A without the 15 answers CuratorKIT's gate rejected | probe recall pooled below v6's | 96 | 74 | R-097, R-098 |
| 3 | Fix C2 (`fix17z`) | fix A with those 15 answers scripted | `hard_dev` recall pooled below v6's; the track ends | 96 | 77 | R-098, R-101 |
| 4 | 6.1 (`fix17cr`) | v6 plus 170 train-pool rows: corrections in training's wordings, cue controls, earlier questions in view | a stepping stone, not gated; it broke the screen recall and `hard_dev` recall lines | 93 | 82 | R-102 to R-104 |
| 5 | 6.11 (`fix17cr11`) | 6.1 with fix C2's 41 rewritten answers, one epoch on top | probe recall pooled below v6's | 95 | 85 | R-105, R-106 |
| 6 | 6.111 (`fix17cr111`) | one more epoch on 6.11, nothing added | recall below v6's on both sets | 94 | 84 | R-107, R-108 |
| 7 | 6.2 (`fix17cs2`) | 6.11's rows, from scratch | passed at 82 and 83; failed a judged `statement` sheet at fresh seed 92 | 96 | 85 | R-109, R-112 |
| 8 | 6.21 (`fix17cs21`) | 6.2 plus 100 rows whose found line says more than the asked detail, one epoch on top | `hard_dev` recall pooled below v6's | 96 | 81 | R-110, R-113 |
| 9 | 6.3 (`fix17cs3`) | 6.2 plus 57 chat lines naming a fact type and 52 questions asked as statements | probe slips at seed 83; screen `statement` | 96 | 85 | R-114, R-116 |
| 10 | 6.31 (`fix17cs31`) | 6.3 with those 52 answers scripted, plus 24 contrast statements (someone else forgets or loses something; no search) | probe recall pooled below v6's | 95 | 82 | R-117, R-119 |
| 11 | 6.311 (`fix17cs311`) | 6.31 plus 72 scripted in-view rows, one epoch on top (my call) | `hard_dev` recall pooled | 95 | 65 | R-118, R-120 |
| 12 | 6.32 (`fix17cs32`) | the same 72 rows, from scratch | `hard_dev` recall, probe recall, probe slips | 96 | 57 | R-118, R-121 |
| 13 | 6.33 (`fix17cs33`) | 6.31 less the 15 memory-word contrast rows | probe recall pooled below v6's, on a new question | 96 | 73 | R-122, R-123 |
| 14 | 6.34 (`fix17cs34`) | 6.33 less the 22 in-view targets that open “It sounds like” | screen `statement` and probe recall | 94 | 80 | R-122, R-125 |
| 15 | 6.36 (`fix17cs36`) | 6.31 less the 6 contrast rows whose reply has “Maybe” | screen `statement` and probe recall | 96 | 83 | R-124, R-126 |
| 16 | **6.37** (`fix17cs37`) | 6.31 less the 9 wallet, umbrella and lost-track contrast rows | passed every line at 82 and 83 and at fresh seeds 94 to 96; shipped and frozen | 94 | 73 | R-127 to R-131, R-160 |
| 17 | 6.38 (`fix17cs38`) | 6.37 with 28 deflecting in-view targets rewritten | `hard_dev` recall pooled below 6.37's | 95 | 80 | R-134, R-140 |
| 18 | 6.39 (`fix17cs39`) | 6.37 plus R-110's 100 rows, from scratch | `hard_dev` recall pooled below 6.37's | 94 | 71 | R-147, R-149 |
| 19 | 7 (`fix17cs7`) | 6.37 with 140 user messages reworded as tag questions (“..., right?”) | screen recall at seed 82 | 92 | 81 | R-153, R-155, R-156 |
| 20 | 7.1 (`fix17cs71`) | 7 without its 20 `in_view` tag rows | probe `in_view` at seed 83 | 94 | 83 | R-156, R-157 |

Not counted as candidates: the scaled and mixed 17b adapters of R-090, registered as diagnostics,
not shippable models (R-088); the controls `fix17crx` and `fix17cs2x`, reported only (R-106,
R-115); fix 15b and 6.35, registered and never trained (R-075, R-122). Trained and scored, with no
record reading the result: 17b at 2 epochs and 3e-4 (`fix17e2`: screen recall 94, `hard_dev` 74); 17b at 2 epochs and 2e-4 (`fix17e2lr2`: screen recall 85, `hard_dev` 54); 17r (`fix17r`: screen recall 95, `hard_dev` 79). The 40 counted here are trained candidate
sets: 16 before v6 (17m included), 21 since (fix B included) and
these 3. Listed but not counted: base and v5 (reference rows), the controls
`fix17crx` and `fix17cs2x`, and R-090's diagnostics.

What the ledger shows. Probe recall sits at its ceiling, so a copy with no real defect can miss
one question by chance, and each removal copy from 6.33 to 6.36 fell short of v6's probe recall
(R-123 to R-127). With the seed-to-seed spread above, later panels judged that a further candidate
was indistinguishable from a draw (R-150, R-159). The gates did not move; 6.37 is the only copy
after v6 that passed every registered line.

## 12. Toolkit findings

**AuditKIT's paired bootstrap does not centre its resamples.** It reports a large gain as failing its
significance test: on this project's data it did so for 57% → 88% over 240 paired cases (R-031; the value it gave
and a reproduction are in the defect note). It is shared by AuditKIT's model comparison, run comparison and experiment significance. This project uses the
exact sign test and a centred bootstrap instead; the defect, a reproduction and the project's
proposed one-line fix, not adopted upstream, are in
[`docs/auditkit_bootstrap_defect.md`](auditkit_bootstrap_defect.md). As a second scorer on v3,
AuditKIT's whole-word oracles agreed with this project's scorer on 959 of 960 cases (R-031,
`results/audit/v3_probe73157.json`). Runs on fix 5c and v5 exist in `results/audit/`; no record reads
the v5 file. AuditKIT was not run on 6.37.

**TRL's chunked loss copies the output layer for every chunk.** On an early development run, on
its longest training rows, before 6.37 existed (R-029), training first peaked at 9.81 GiB
on a 10 GiB card, so any other program on the card pushed it into shared memory at several times
the step time. The loss computes `h.float() @ w.float().t()`; under bf16 autocast
both float32 copies of the 262,144-word output layer are cast straight back to bf16, so they change
nothing but memory. A replacement that takes the bf16 product directly gives TRL's loss, scores and
gradients bit for bit (tested), and on the same early run training peaks at 7.12 GiB at
about 1.1 s a step (R-029). In a separate run, v3 retrained with it differed from its
original on 13 of 240 conversations, inside run-to-run variation (R-032). 6.37 is
trained with it; its own training peak is 7.81 to 7.84 GiB (section 4).

![Training memory](../figures/training_memory.png)

*Figure 3. Training memory on the early development runs of R-029, not 6.37's: TRL's loss against
the lean loss.*

**CuratorKIT's grounding gate finds faulty training answers the project's own checks missed.** The gate asks a
judge whether each answer is supported by its source. It was run over v6's found-fact training
answers only, an ancestor of 6.37's set; the rest of 6.37's 1,094 rows (corrections,
statements, contrast lines) were never gated by it. Run over those answers with
three Claude judges plugged into CuratorKIT's own backend class (prompts recorded, answered, then
replayed, so CuratorKIT's prompt, parsing and threshold decide every verdict), it rejected
22 of 350: 8 that pin a relation on the wrong person and 14 that
the project's pattern check did not catch, such as claims the passage does not make (R-096). As an acceptance
test for replacement answers, it passed every replacement, rejected the old rejections hidden on the
sheet as controls (22 of 22) and rejected no answer it had passed before (R-098). It is
an audit of training targets, not a test of the model, and its judges are the same model family as
the coherence judges.

## 13. Threats to validity

- **Both sealed pools come from the project's generator.** `independent` was written by a fresh
  agent and never read, but its chats follow the generator's structure: where facts sit, how
  questions are worded, how decoys look. The sealed run shows the gain holds on unseen people, facts
  and small talk; the outside-writer sets are the measure of chats with a different structure
  (R-163, disclosure 5).
- **The outside-writer sets are small and close.** 4 writers a set, all fresh agents of
  one model family, about 40 questions a kind; the intervals resample chats, not writers (R-142).
  The first set also became a development set (R-151).
- **Development data was read many times.** Every candidate in section 11 was chosen on `probe`,
  `hard_dev` and later the first outside-writer set; their numbers flatter whatever was chosen.
  Seed 82 was fixed before seeds 94 to 99 existed and is the lowest of the eight on `hard_dev` (R-141).
- **Few templates.** The generated recall questions come from few fact templates, so item-level
  p-values overstate the evidence; template-resampled intervals still exclude zero on development
  pools (R-141). The sealed intervals do not resample templates (R-164).
- **Training seeds differ more than one run can show.** On `hard_dev` 6.37 ranges 73 to 90
  of 96 by seed (R-141); fix 17b's plain chat fell below base at some seeds and not others (R-091).
  Training is not bit-reproducible on this card (R-029); generation is: a repeated run of seed 82
  gave the same reply on 240 of 240 questions (R-156).
- **The coherence judges are Claude models only, and see only the turns in view.** Agreement among
  them is weaker evidence than agreement across model families (R-096); they cannot tell a false
  "you never told me" from a true one, so recall is always read beside coherence (R-020). No person
  checked their marks.
- **The scorer.** It fails a reply that names the answer and a wrong value together, which both
  human markers passed: I, the author (R-144), and an independent second marker (R-145). Their
  50 lines come from development pools only, so the check says nothing directly about
  the sealed or outside-writer chats. On the development runs counted (base and seed 82 on `probe` and
  `hard_dev`), this lowered only base's recall, on `hard_dev` by at most 9 of 96; it was
  not counted on other runs (R-144). On `never_told` it passes an
  invented value outside the listed ones (R-020). On the outside-writer sets many questions list no
  wrong value, so a reply that adds something false is not caught there (R-143, R-152). It does not
  look for leaked tool text, which only base produced (R-144).
- **Shared briefs.** `hard_dev` and the wide training pool were written to briefs like the sealed
  `independent` pool's, so condition C and D are less independent of development than when
  registered; one discarded writer saw fragments of sealed wording (R-066, R-069, R-070).
- **The baselines tried.** Base with the tool; base with two fixed prompts (R-137, R-161); base with
  the whole chat on the outside-writer sets (R-164, R-165) and on the sealed pools at 58 messages
  (R-168); and code that always searches, on the sealed pools (R-168), the outside-writer sets
  (R-169) and LongMemEval-S (R-170). The last two were registered in R-016 and run only after the
  sealed run (R-167). No search over prompts and no other retrieval system was tried.
- **Which reference wins depends on the kind of chat.** On the outside-writer chats the whole chat
  beats the tool and plain code recalls as well as 6.37 (R-164, R-169); on the generated sealed
  chats 6.37 is far above both (R-168). Neither kind of chat is a real person's.
- **LongMemEval-S answers are low for every arm**: the gold is in 34 to 63 of 411 replies for
  the four arms that ran every question, and judged right on at most 53 of
  248. Its system prompt ("You are chatting with a friend") does not fit a user talking
  to an assistant, and the view, chunking and date prefixes are this project's adaptation, not
  LongMemEval's setup (section 9).
- **Replies are capped at 60 tokens**, in every test. On LongMemEval-S many base replies
  reach the cap (section 9's table), and a reply that reaches the cap stops there, so a gold answer placed later in it is lost; 6.37's
  replies are much shorter.
- **The LongMemEval judges are Claude, not GPT-4o.** The official score uses a GPT-4o judge; here
  three Claude Sonnet judges read LongMemEval's prompts, their temperature cannot be set, and each
  read a sheet of many prompts, not one prompt per call (R-170). I (the author, not an independent
  marker) checked 50 of their lines; no independent person checked them.
- **The longest views fail on a 10 GB card.** On LongMemEval-S the longest views, with a search's
  passages added, run out of card memory under the 8.50 GiB cap, and some still fail at
  0.90 of the card; those questions count as wrong, and the tool arms fail more often than the arm
  with no tool (section 9). At 419 messages the whole chat does not fit at all (R-166).

## 14. Errors and corrections

Each error below was found during the work, and the record named beside it holds both the error
and its correction.

- **Generation did not stop at the end of a turn.** The first test's readings were withdrawn and
  rerun with stops (R-010, R-013).
- **The first adapter's score was memorised.** It answered 119 of 120 on conversations like
  its training set and failed on a fresh probe: the number of passages a search returned gave the
  answer away. Decoy counts now vary per row (R-018, R-020).
- **A screen counted the wrong thing.** It scored plain chat by whether the model searched, so a
  stronger adapter passed it and failed the blind judge (R-055); confirmations since judge plain chat
  on every seed.
- **A plateau called too early.** v5 was called final on the probe alone (R-064); harder checks then
  showed a large gap on `hard_dev` (R-065, R-068).
- **A checker that pushed a writer to the sealed data.** A count-only checker led a writer to print
  fragments of sealed wording; that pool was discarded unused and the checker now names only the
  writer's own lines (R-070).
- **A toolkit defect** in AuditKIT's bootstrap (R-031, section 12).
- **A training default not checked.** Every adapter through v5 put the loss on every token of a row
  (R-076).
- **A build that wrote before it checked** (R-073), and **a build that doubled line endings**
  (R-136); both builds now check what they wrote.
- **A second queue runner** trained on the card beside another run (R-114); it was stopped.
- **Counts corrected.** R-130's slip counts took every kind instead of R-094's two (R-131); R-139's
  first text said ten tests where there were nine (R-139); R-155 counted a line that was not 7's
  (R-156); R-144's finding that 6.37's misses never state a false value did not hold on the first
  outside-writer set (R-146).
- **Rows built before the baseline they were to follow** (R-103), and **a panel's claim queued
  unchecked** (R-126); both disclosed where they happened.
- **Greps past the readable part of `pools.py`** printed one probe line and one assignment line,
  nothing sealed (R-155, R-157); multi-file searches now leave `pools.py` out.
- **The sealed run's disclosures** (R-163, items 1 to 4; section 5's deviation list).
- **A panel's claim corrected.** A panel lane wrote that no record had base reading the whole chat;
  R-014 and R-017 had (R-164). The control it asked for was then run (R-164, R-165).
- **A queue runner left waiting, and a record corrected.** R-165 called the queue runner stuck; it
  was waiting for a clean tree, which a results file left uncommitted overnight had blocked. When a
  commit cleaned the tree, it resumed and started a second run on the card; both were stopped, and
  every later GPU run was started on its own (R-165, corrected in R-166).
- **Registered references left out of the sealed run.** R-016 registered base with the whole chat
  and code that always searches as references beside the rules. R-162 ran neither and did not say
  so, and R-164 and the README then said R-016 had not included the whole chat. The write-up's
  reviewer found the omission (R-167); both references were run late, on base only (R-168,
  R-169), and one of them, plain code, recalls as well as 6.37 on the outside-writer chats. R-016's
  coherence interval, its training recipe and LoCoMo were also not carried out as registered, and
  R-167 lists them (section 5, deviations 8 to 10).
- **A memory failure read as a runner bug.** In LongMemEval-S's first dry run, most of the 20
  longest views ran out of card memory, and R-170 read the later failures as memory left over from
  an earlier one, freed too early in the runner. The runner was changed, and a second dry run on the
  same 20 failed on most of them again. So the reading was wrong: each failing question's own forward
  pass did not fit under the cap. The record was corrected where it was written, the change was kept
  as harmless, and the failures were reported per arm as registered (R-170).

## 15. Limitations

- **Short outside-writer chats are better shown whole.** Given the whole chat, the trained model
  and base show no measured difference (one seed, two sets of 40 chats; gaps under about
  15 points on a kind of 40 questions are below what this test resolves, R-142). On those
  chats, of about 1,400 tokens, the whole chat beats the three-exchange view with search
  (section 6). On generated chats of the same length it does not (R-168). The whole-chat reading at
  419 messages is not measured.
- **Plain code recalls as well on the outside-writer chats.** With the last three exchanges in view,
  code that searches every turn shows no measured recall difference from 6.37 there (R-169), and is
  faster. Training adds searching when the answer is out of view (against base) and not searching
  when it is in view (against code); on plain chat lines 6.37 searches more often than base. The
  adapter's recall gain over plain code is shown on the generated sealed pools only (R-168). On
  LongMemEval-S code finds more evidence than 6.37 and shows no measured difference in answers
  (R-170). No gated-search rule written by hand was tried as a baseline.
- **6.37 declines answerable questions on LongMemEval-S**: 233 of the 470
  questions it should answer, against base's 22 (R-170).
- **Tag questions.** 6.37 goes along with most false claims in "..., right?" questions (section 8).
- **Training queries copied into a demo chat.** On the scripted demo (`demo/chat.txt`, greedy),
  6.37 searched with queries copied from its training set on two of its four questions ("brother
  new job" and "sister broke skiing injury", each in 3 rows of `data/screens/fix17cs37.jsonl`) and
  answered both with an unrelated stored fact. The earlier adapters v5 and fix 15 declined on those
  two turns (R-175).
- **A wrong answer in view is repeated.** On eight more demo questions registered before they ran (R-176), the untrained model was right on 2 and 6.37 on 0: 6.37 repeated its own earlier wrong answer, still in view, on 6 of the 8.
- **Found but not used.** Its commonest miss on generated chats finds the right line and answers
  from its first clause, leaving out a detail later in the line (R-144, R-149); on outside-writer
  chats the commonest is a search that misses, including facts told with a pronoun (R-146).
- **One model, one size, English only.** Only Tiny Aya Global was trained; the friend's messages are
  all English.
- **Few real chats.** The generated pools and the outside-writer sets hold no chat from a real
  person. LongMemEval-S mixes real logs of people talking to an assistant with model-simulated
  sessions, and the sessions that hold its answers were simulated (R-170); it is a different kind of
  chat from the friend's chats 6.37 was trained on. Corrections, phone-style typing, an earlier
  question in view, four decoys and chats of 1,000 and 2,000 messages were tested on generated chats
  only (R-102 to R-133, R-138, R-148). LoCoMo, a public chat set, was registered as an outside check
  and deferred; it was never run (R-100, R-139 item 6).
- **One tool, read only**, with a fixed three-exchange view. The model cannot save a note.
- **No hostile text.** Instructions hidden in retrieved passages are out of scope.
- **Greedy decoding only**, and **one machine**: times are an RTX 3080's.
- **Judged by models, not people** (sections 5 and 13). The coherence judges were never checked
  against a person; the LongMemEval-S judges were checked on 50 lines by me, the author, not an
  independent marker (section 9). The recall scorer was checked by me and by one independent
  second marker, on 50 lines from development pools (R-144, R-145).
- **The shipped seed is the weakest of the eight on several sets.** Seed 82 is the lowest of the
  eight training seeds on the first outside-writer set, on sealed conditions C and D and on
  `hard_dev`; on the first outside-writer set its gain over base has p = 0.047, above the
  registered 0.01 (R-141, R-146, R-163).

## 16. Future work

- **Measure the whole chat at length.** Base and 6.37 with every message in view on 419-message
  chats, on a card that holds them, to find where searching starts to beat reading.
- **Ground tag questions.** 7.1 showed the search can be trained (section 8); the next step is
  queries in the claim's own words (the 7.2 design), judged on a new outside-writer set.
- **Injection in retrieved text.** Train the model to treat instructions inside search results as
  content, and test it with hidden instructions in earlier messages.
- **Writing memory.** A tool that saves a note, so the model decides what is worth keeping.
- **Reinforcement on verified outcomes.** The decision to search and the answer are checkable by
  code, so they suit reward-based training (for example GRPO through AgentTune).
- **Other languages and larger models**, with the same sealed-test protocol.
- **Real conversations**, with consent, and a human panel beside the model judges.
- **Upstream fixes.** Offer the lean loss to TRL and the bootstrap fix to AuditKIT.

## 17. Reproduce

Everything runs on one 10 GB card. Every results file carries its provenance (command, commit,
package versions).

- **The sealed run:** `scripts/records/queue/final.sh` (run by the queue), starting with
  `scripts/records/freeze_r154.py check` on `results/freeze/sealed_manifest.json`; scored by
  `scripts/records/score_r162.py` into `results/analysis/R-162/`; sheets from
  `scripts/records/sheets_r162.py`, judges' briefs from `scripts/records/briefs_r162.py`, judge
  transcripts audited by `scripts/records/audit_judge_r162.py`.
- **Analyses:** `scripts/records/writeup_r164.py` (`results/analysis/R-164/`),
  `scripts/records/blind_r146.py` and `scripts/records/blind2_r157.py` (the outside-writer sets),
  `scripts/records/rigor_r139.py` (development rigor), `scripts/records/refs_r168.py` (R-016's
  references on the sealed pools, `results/analysis/R-168/`).
- **LongMemEval-S:** `scripts/run_longmemeval.py` (one arm a call; the data file, its sha256 in
  R-170, is not in the repository), `scripts/records/profile_r170.py`, `scripts/records/score_r170.py`
  and, for the judged accuracy, `scripts/records/judge_sheets_r170.py` and
  `scripts/records/score_judged_r170.py`. Only the aggregates in `results/analysis/R-170/` are
  committed; the raw runs quote the chats and stay out of git.
- **This article and the model card:** `PYTHONPATH=src python scripts/make_article.py`, from their
  templates in `docs/`; figures by `scripts/make_figures.py`. No result number in either is typed by
  hand.

## Author contributions

I, Kevin Vaillancourt, directed this work, carried out with an AI assistant, Claude (Anthropic), as
an executive-function accommodation. Test pools and chat sets meant to be independent were written by
fresh AI agents that saw only a brief, and coherence was marked by fresh AI judges that saw only a
rubric and a sheet.

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
sets. Built with AgentTune, AuditKIT and CuratorKIT from Lexsi Labs. Tiny Aya is CC-BY-NC-4.0, and
the adapter carries that licence.*
