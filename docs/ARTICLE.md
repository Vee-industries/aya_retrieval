# Teaching a 3B model to search a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

> **Final numbers for the shipped model, 6.37 (`fix17cs37` seed 82, frozen in R-160): the sealed final run (registered in R-162, results in R-163), the outside-writer sets (R-146, R-157) and the whole-chat control (R-164, R-165). Every number is computed from committed results files by `scripts/make_article.py`.**

## Abstract

When a chat fits in what the model can read, give it the whole chat. On two sets of chats written
by outside writers who never saw this project's generator (about 1,400 tokens a chat),
untrained Tiny Aya Global (3.35B) with every message in view answers 58 and
52 of 80 questions about facts told earlier. Our trained model, 6.37, with
a search tool and only the last three exchanges in view, answers 28 and
34 (R-164). Given the whole chat and the tool, 6.37 and the untrained model show
no measured difference (one seed, two sets of 40 chats; gaps under about 15 points on a kind of 40 questions could not be seen, R-142) on every kind
of message (R-165). So the gain below is for chats too long to show whole.

For those chats, 6.37 is a LoRA adapter trained to search the earlier conversation when the answer
is out of view, to read what comes back, and to answer in the model's own voice. With only the last
three exchanges in view, as a stand-in for a chat too long to show, the shipped seed answers
39 and 53 of 120 recall questions on the two
outside-writer sets, against the untrained model's 26 and 27
(gain +2.5 to +19.2 and +13.3 to +30.0 points, 95% intervals resampling chats; on the first set
the sign test gives p = 0.047, above the registered 0.01) (R-146, R-157). The gain is on
facts asked about directly. On "..., right?" questions that make a false claim, 6.37 corrects
1 and 3 of 20 and goes along with
the rest (R-164). The shipped seed, 82, is the lowest of the eight training seeds on the first
outside-writer set, on sealed conditions C and D, and on `hard_dev`; the eight seeds pooled gain
+18.0 and +20.8 points on the two sets (+9.7 to +26.1 and
+12.9 to +28.3) (R-141, R-146, R-157, R-163). The outside writers are 4 fresh
Claude Opus agents a set, and the coherence judges are Claude Sonnet agents only, never checked
against a person. On the registered sealed test, run once on the untrained model and all eight
training seeds in four conditions, every registered rule passes: recall 85.2 to 90.4%
pooled over the eight against the untrained model's 8.3 to 28.3%, every right answer from
a search that found the fact, no adapter with more false retrievals than the untrained model, and
every adapter judged coherent more often (R-163). Both sealed pools come from the project's own
generator. Not measured: the untrained model reading the whole chat at 419 messages.

## 1. Introduction

A chat assistant keeps a long conversation, but a model attends to a limited window. Tiny Aya Global
takes at most 8,192 tokens, and 9 of its 36 layers
attend to all of them; the other layers attend to the last 4,096 (the model's config).
Past that, a fact told early in the chat is either out of the prompt or in a part most layers do
not see.

**The first answer is to show the whole chat when it fits.** We measured it late, after the
sealed run (R-164, R-165), and it changes how the rest of this paper should be read. On chats of
about 1,400 tokens, the untrained model with every message in view beats our trained
model working from the last three exchanges and a search, by a wide margin (section 6). Given the
whole chat as well, the trained model and the untrained one show no measured difference (one seed, two sets of 40 chats; gaps under about 15 points on a kind of 40 questions could not be seen, R-142) on every kind. The design
this supports is plain: show the model the whole chat when it fits, and let it search when it does
not.

**What the trained model adds** is the second half: a model that, shown only the last part of a
chat, decides when an answer is out of view, writes a search, reads the result and answers without
sounding different from before. We test it with the last three exchanges in view, as a stand-in for
a chat too long to show. It beats the untrained model there on every test set: on the
outside-writer sets by +10.8 and +21.7 points (+50% and
+96% over base; R-146, R-157), and by 60 to 82 points on the generator's
sealed pools (sections 7 and 8).

The Track 3 statement asks for a model that "decides when and what to retrieve, grounds its answers
in the retrieved text and ignores distracting documents". Each phrase maps to a measure here:

| Track statement | Measure |
|---|---|
| decides **when** to retrieve | right decisions: searched exactly when the answer was out of view |
| decides **what** to retrieve | the fact was found by the model's own query |
| **grounds** its answers | recall: the right fact in the reply, counted again on retrieved answers alone |
| **ignores distracting documents** | false retrieval: a decoy's fact in the reply, with one and four decoys a chat |

**Contributions.**
1. A measured answer to "why not show the whole chat": on short chats, do; given the whole chat,
   the trained model and the untrained one show no measured difference (R-164, R-165; one seed,
   two sets of 40 chats).
2. A training recipe that teaches the search habit while keeping the model's own voice (section 4).
3. A test that is hard to game: registered before training, amended only to make it harder, frozen
   with its scorer and judge, run once on every training seed (R-016, R-038, R-039, R-041, R-154,
   R-162), and two sets of chats by writers who never saw the generator.
4. A ledger of every candidate tried, with the line each failed (section 10), and three toolkit
   findings (section 11).

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

## 3. Task and pools

A conversation has run for some time. In the main tests the model sees the system prompt, the last
three exchanges and the friend's newest message. Everything earlier sits behind one tool,
`search_corpus`, a full-text search over the earlier conversation that returns the top 5
passages, one passage per exchange; the model may call it up to 3 times a turn. The
newest message is one of five kinds, each scored by a fixed rule (`src/aya_retrieval/scoring.py`,
R-015):

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
Training took 33 to 35 minutes a seed, peaking at 7.81 to 7.84 GiB of card memory.

**The Lexsi toolkits.** AgentTune trains every adapter (R-003, R-016). AuditKIT re-scored recorded
replies as a second scorer during development: its files are `fix5c_probe73157`, `v3_probe73157`, `v5_probe73157` (R-030, R-031); no
AuditKIT run on 6.37 exists. CuratorKIT's grounding gate audited v6's found-fact training answers
and passed the replacements before they were used (R-096, R-098). Section 11 reports what each
showed.

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
the recall scorer: Kevin agreed with the scorer on 47 of 50 lines (Cohen's kappa 0.88), and the scorer passed no reply he failed (R-144). A second marker agreed with the scorer on 48 of 50 (kappa 0.92) and with Kevin on 49 (kappa 0.96) (R-145). In every disagreement the scorer was the stricter; the two lines
both people passed and the scorer failed name the answer and a wrong value together (R-144, R-145).

**Statistics.** Paired exact sign tests on the questions where two runs differ, and 95% percentile
bootstrap intervals that resample whole conversations or chats, keeping the pairing. The adapter
pairs in rule 1 share conversations, so its p-value overstates independence; the whole-conversation
interval is the figure to read (R-162). Generated questions share fact templates: the development
pools' recall questions come from 5 templates (`probe`) and 8
(`hard_dev`), so item-level p-values there overstate the evidence (R-141). The sealed pools' template
count is not known without opening them, which this project's rules forbid, and the sealed intervals
do not resample templates (R-164).

**Every deviation from the registered plan, in one place.**
1. *Eight seeds, not three.* R-016 named three adapters; the sealed run used all eight trained on
   6.37's set, at Kevin's word, so no seed was chosen after a result (R-162). Rule 1 on R-016's own
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
7. *R-016's references were not run.* R-016 lists `whole_chat` and `always_search` as references
   to report beside the rules; R-162 ran neither and did not say so, and the omission was first
   disclosed in R-167. The pass rules did not depend on them. The whole-chat reference was run
   afterwards, on the outside-writer sets only (R-164, R-165); `always_search` was never run on a
   set the trained model was tested on (section 6).
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

## 6. Results: whole chat or search

On the outside-writer sets, `older` questions (R-164, R-165; one seed, 40 chats a set; in brackets,
the paired counts against base with the whole chat):

| Set | Base, last three exchanges and the tool | 6.37, last three exchanges and the tool | Base, whole chat | 6.37, whole chat (only base right, only 6.37 right, sign test) | 6.37, whole chat and the tool (the same, against base with the whole chat) |
|---|---|---|---|---|---|
| Set 1 | 11 | 28 | 58 | 59 (8, 9, p = 1.0) | 57 (12, 11, p = 1.0) |
| Set 2 | 12 | 34 | 52 | 56 (10, 14, p = 0.54) | 54 (12, 14, p = 0.85) |

![Whole chat or search](../figures/whole_chat_or_search.png)

Base with every message in view beats 6.37 working from the last three exchanges on both sets
(set 1: 36 right only for base with the whole chat and 6 only for 6.37 with the tool, p = 2.8 × 10<sup>-6</sup>; set 2: 28 right only for base with the whole chat and 10 only for 6.37 with the tool, p = 0.0051; R-164). Given the whole chat, 6.37 and base
show no measured difference (one seed, two sets of 40 chats; gaps under about 15 points on a kind of 40 questions could not be seen, R-142), with or without the tool (R-165): no measured damage to how the model uses the context it
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

**What is not measured.** Base with the whole chat on the generated pools, whose 419-message chats
run about 6,236 tokens on `hard_dev` and 5,409 on `probe`. Those runs were
registered (R-164) and have no results, because they ran out of card memory (R-166; the queue log is
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

**Code that always searches is a competitor for long chats, and was not tested against.** R-014's
`always_search` arm (code makes a search on every turn and hands base the result; no training)
answered 28 of 40 at 419 messages, against the whole chat's
2 of 40, and 34 of 40 at 58. It has a cost: in R-017 it answered
5 of 24 facts in view (base with no tool 22 of 24) and
0 of 24 plain-chat lines without a search (base with no tool
24 of 24), because it searches on every turn. R-016 registered it as a
reference; it was never run on any set the trained model was tested on (R-167, item 1).

## 7. Results: the sealed run

Every rule passes in every condition (R-163). Recall, rule 1 (counts of right answers, `older` and
`confirm`):

| Condition | Base, 58 messages | Eight adapters pooled, 58 | Points | Base, 419 messages | Eight adapters pooled, 419 | Points | Gain, 95% interval resampling conversations (points) |
|---|---|---|---|---|---|---|---|
| A, `heldout`, 1 decoy | 17 of 60 (28.3%) | 426 of 480 (88.8%) | +60.4 | 15 of 60 (25.0%) | 409 of 480 (85.2%) | +60.2 | +50.8 to +69.7 |
| B, `heldout`, 4 decoys | 15 of 60 (25.0%) | 434 of 480 (90.4%) | +65.4 | 14 of 60 (23.3%) | 409 of 480 (85.2%) | +61.9 | +54.4 to +72.8 |
| C, `independent`, 1 decoy | 10 of 60 (16.7%) | 434 of 480 (90.4%) | +73.8 | 11 of 60 (18.3%) | 429 of 480 (89.4%) | +71.0 | +64.9 to +79.4 |
| D, `independent`, 4 decoys | 5 of 60 (8.3%) | 434 of 480 (90.4%) | +82.1 | 8 of 60 (13.3%) | 424 of 480 (88.3%) | +75.0 | +71.9 to +84.6 |

![Recall out of view](../figures/recall_out_of_view.png)

The gain is 60 to 82 points at each size against the 20 required; the registered sign
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

**Behaviour**, reported beside the rules (of 300; clean first calls are calls with nothing written
after them):

| Condition | Right search decisions: base | seed 82 | eight seeds | Clean first calls: base | seed 82 | Ran out of calls: base | all eight adapters | Seed 82 recall: fact found / right |
|---|---|---|---|---|---|---|---|---|
| A | 180 | 298 | 283 to 300 | 52 of 136 | 180 of 180 | 1 | 0 | 106 / 106 |
| B | 180 | 298 | 283 to 300 | 52 of 136 | 180 of 180 | 2 | 0 | 107 / 107 |
| C | 193 | 296 | 294 to 300 | 49 of 107 | 184 of 184 | 3 | 0 | 111 / 92 |
| D | 193 | 296 | 294 to 300 | 49 of 107 | 184 of 184 | 3 | 0 | 111 / 91 |

## 8. Results: the outside-writer sets

Recall (`older` and `confirm`, of 120) with the last three exchanges in view (R-146,
R-157, R-164):

| Set | Base | 6.37 seed 82 | Only base right, only seed 82 right, sign test | Seed 82 gain, 95% interval resampling chats (points) | Each seed (82, 83, 94 to 99) | Eight seeds pooled, gain interval (points) |
|---|---|---|---|---|---|---|
| Set 1 | 26 | 39 | 12, 25, p = 0.047 | +2.5 to +19.2 | 39, 43, 57, 46, 48, 52, 46, 50 | +9.7 to +26.1 |
| Set 2 | 27 | 53 | 9, 35, p = 1.1 × 10<sup>-4</sup> | +13.3 to +30.0 | 53, 53, 47, 56, 51, 56, 56, 44 | +12.9 to +28.3 |

On set 1 seed 82's gain is +10.8 points and its sign test p = 0.047, above the
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
3 of 20, about as often as base. This is a result, not only
a limit. 7.1, trained to search tag questions, searched nearly all of them and grounded every right
answer, but did not raise recall and failed a development line (R-157, R-158).

**The prompted baseline.** Two fixed system prompts on base, written before any result: A states
five rules, B adds four worked examples (R-137, R-161). Recall:

| Set | Base | Base, prompt A (rules) | Base, prompt B (rules and four worked examples) | 6.37 seed 82 | Prompt A against seed 82: only A right, only 6.37 right, sign test | Prompt B against seed 82 |
|---|---|---|---|---|---|---|
| Set 1 | 26 | 19 | 15 | 39 | 8, 28, p = 0.0012 | 8, 32, p = 1.8 × 10<sup>-4</sup> |
| Set 2 | 27 | 18 | 20 | 53 | 4, 39, p = 3.1 × 10<sup>-8</sup> | 5, 38, p = 2.5 × 10<sup>-7</sup> |

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

## 9. Cost

The sealed run's times, on this machine (an RTX 3080, 10 GB, each run with the card to itself)
(R-163):

| Condition | Base: seconds, per conversation | Seed 82: seconds, per conversation | Eight adapters: seconds per conversation | Tokens read per turn, base / seed 82 | Whole chat, tokens | Seed 82 reads, share of the whole chat | Tokens written per turn, base / seed 82 | Searches per conversation, base / eight adapters |
|---|---|---|---|---|---|---|---|---|
| A | 389, 1.30 | 535, 1.78 | 1.73 to 2.18 | 1,148 / 1,196 | 3,227 | 37% | 37 / 26 | 0.47 / 0.57 to 0.63 |
| B | 385, 1.28 | 502, 1.67 | 1.67 to 1.92 | 1,154 / 1,207 | 3,239 | 37% | 38 / 26 | 0.48 / 0.57 to 0.63 |
| C | 381, 1.27 | 524, 1.75 | 1.75 to 2.03 | 1,122 / 1,239 | 3,496 | 35% | 36 / 27 | 0.39 / 0.60 to 0.62 |
| D | 434, 1.45 | 624, 2.08 | 2.08 to 2.34 | 1,145 / 1,266 | 3,610 | 35% | 37 / 27 | 0.39 / 0.60 to 0.62 |

Seed 82 reads 35 to 37% of the whole chat's tokens a turn and writes fewer tokens than base.
It takes longer per conversation than base because it searches more often, and each search adds a
model call. Peak card memory in the sealed run was 7.02 GiB. The 33 judges took
53 to 129 s each, median 80 s (`results/coherence/R-162/judge_times.json`). Training took 33 to 35
minutes a seed. On the outside-writer sets the comparison runs the other way: a chat of about
1,400 tokens costs less to read whole than to search (section 6).

## 10. How 6.37 was chosen: the candidate ledger

Every candidate after v5, in order, with the line it failed. The records number the candidates read
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

**Since v6** (from R-103 on, Kevin's tree names: 6.1 is v6 plus a first stepping stone, 6.11 a second
on top of it, 6.2 a different first stone):

| # | Candidate (set) | What it changed | How it ended | Screen recall, seed 82 (of 96) | `hard_dev` recall, seed 82 (of 96) | Record |
|---|---|---|---|---|---|---|
| 1 | Fix A (`fix17w`) | v6, with its 27 slip-shaped answers rewritten | failed a judged sheet under judge 1 | 96 | 78 | R-094, R-095 |
| — | Fix B (`fix17mb`) | v6, with base-written answers' loss only on the first token and end marker | trained and scored at 82 and 83 and counted (R-101); no record states its result | 95 | 75 | R-095, R-101 |
| 2 | Fix C1 (`fix17y`) | fix A without the 15 answers CuratorKIT's gate rejected | probe recall pooled below v6's | 96 | 74 | R-097, R-098 |
| 3 | Fix C2 (`fix17z`) | fix A with those 15 answers scripted | `hard_dev` recall pooled below v6's; the track ends | 96 | 77 | R-098, R-101 |
| 4 | 6.1 (`fix17cr`) | v6 plus 170 train-pool rows: corrections in training's wordings, cue controls, earlier questions in view | a stepping stone, not gated; it broke the screen recall and `hard_dev` recall lines | 93 | 82 | R-102 to R-104 |
| 5 | 6.11 (`fix17cr11`) | 6.1 with fix C2's 41 rewritten answers, one epoch on top | probe recall pooled below v6's | 95 | 85 | R-105, R-106 |
| 6 | 6.111 (`fix17cr111`) | one more epoch on 6.11, nothing added | recall below v6's on both sets | 94 | 84 | R-107, R-108 |
| 7 | 6.2 (`fix17cs2`) | 6.11's rows, from scratch | passed at 82 and 83; failed a judged `statement` sheet at fresh seed 92 | 96 | 85 | R-109, R-112 |
| 8 | 6.21 (`fix17cs21`) | 6.2 plus 100 rows whose found line says more than the asked detail, one epoch on top | `hard_dev` recall pooled below v6's | 96 | 81 | R-110, R-113 |
| 9 | 6.3 (`fix17cs3`) | 6.2 plus 57 chat lines naming a fact type and 52 questions asked as statements | probe slips at seed 83; screen `statement` | 96 | 85 | R-114, R-116 |
| 10 | 6.31 (`fix17cs31`) | 6.3 with those 52 answers scripted, plus 24 contrast statements (someone else forgets or loses something; no search) | probe recall pooled below v6's | 95 | 82 | R-117, R-119 |
| 11 | 6.311 (`fix17cs311`) | 6.31 plus 72 scripted in-view rows, one epoch on top (Kevin's call) | `hard_dev` recall pooled | 95 | 65 | R-118, R-120 |
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

What the ledger shows. Probe recall sits at its ceiling, so a copy with no real defect often misses
one question by chance, and each removal copy from 6.33 to 6.36 fell short of v6's probe recall
(R-123 to R-127). `hard_dev` recall moves between training seeds alone (73 to 90 of 96 for
6.37, R-141) by more than most changes moved it. Later panels judged that a
further candidate could not be told from a draw (R-150, R-159). The gates did not move; 6.37 is the
only copy after v6 that passed every registered line.

## 11. Toolkit findings

**AuditKIT's paired bootstrap does not centre its resamples.** It reports a large gain as not
significant: on this project's data it did so for 57% → 88% over 240 paired cases (R-031; the value it gave
and a reproduction are in the defect note). It is shared by AuditKIT's model comparison, run comparison and experiment significance. We use the
exact sign test and a centred bootstrap instead; the defect, a reproduction and a one-line fix are
in [`docs/auditkit_bootstrap_defect.md`](auditkit_bootstrap_defect.md). As a second scorer on v3,
AuditKIT's whole-word oracles agreed with ours on 959 of 960 cases (R-031,
`results/audit/v3_probe73157.json`). Runs on fix 5c and v5 exist in `results/audit/`; no record reads
the v5 file. AuditKIT was not run on 6.37.

**TRL's chunked loss copies the output layer for every chunk.** Training first peaked at
9.81 GiB on a 10 GiB card, so any other program on the card pushed it into shared memory
at several times the step time. The loss computes `h.float() @ w.float().t()`; under bf16 autocast
both float32 copies of the 262,144-word output layer are cast straight back to bf16, so they change
nothing but memory. A replacement that takes the bf16 product directly gives TRL's loss, scores and
gradients bit for bit (tested), and training peaks at 7.12 GiB at about 1.1 s
a step. Retrained with it, v3 differed from its original on 13 of 240 conversations,
inside run-to-run variation (R-029, R-032). 6.37 is trained with it.

![Training memory](../figures/training_memory.png)

**CuratorKIT's grounding gate finds faulty training answers our own checks missed.** The gate asks a
judge whether each answer is supported by its source. Run over v6's found-fact training answers with
three Claude judges plugged into CuratorKIT's own backend class (prompts recorded, answered, then
replayed, so CuratorKIT's prompt, parsing and threshold decide every verdict), it rejected
22 of 350: 8 that pin a relation on the wrong person and 14 that
our pattern check could not see, such as claims the passage does not make (R-096). As an acceptance
test for replacement answers, it passed every replacement, rejected the old rejections hidden on the
sheet as controls (22 of 22) and rejected no answer it had passed before (R-098). It is
an audit of training targets, not a test of the model, and its judges are the same model family as
the coherence judges.

## 12. Threats to validity

- **Both sealed pools come from the project's generator.** `independent` was written by a fresh
  agent and never read, but its chats follow the generator's structure: where facts sit, how
  questions are worded, how decoys look. The sealed run shows the gain holds on unseen people, facts
  and small talk; the outside-writer sets are the measure of chats with a different structure
  (R-163, disclosure 5).
- **The outside-writer sets are small and close.** 4 writers a set, all fresh agents of
  one model family, about 40 questions a kind; the intervals resample chats, not writers (R-142).
  The first set also became a development set (R-151).
- **Development data was read many times.** Every candidate in section 10 was chosen on `probe`,
  `hard_dev` and later the first outside-writer set; their numbers flatter whatever was chosen.
  Seed 82 was fixed before seeds 94 to 99 existed and is the lowest of the eight on `hard_dev` (R-141).
- **Few templates.** The generated recall questions come from few fact templates, so item-level
  p-values overstate the evidence; template-resampled intervals still exclude zero on development
  pools (R-141). The sealed intervals do not resample templates (R-164).
- **Training seeds differ more than one run can show.** On `hard_dev` 6.37 ranges 73 to 90
  of 96 by seed (R-141); fix 17b's plain chat fell below base at some seeds and not others (R-091).
  Training is not bit-reproducible on this card (R-029); generation is: a repeated run of seed 82
  gave the same reply on 240 of 240 questions (R-156).
- **The judges are Claude models only, and see only the turns in view.** Agreement among them is
  weaker evidence than agreement across model families (R-096); they cannot tell a false "you never
  told me" from a true one, so recall is always read beside coherence (R-020). No person checked
  their marks.
- **The scorer.** It fails a reply that names the answer and a wrong value together, which the two
  people passed (R-144, R-145). On the development runs counted (base and seed 82 on `probe` and
  `hard_dev`), this lowered only base's recall, on `hard_dev` by at most 9 of 96; it was
  not counted on other runs (R-144). On `never_told` it passes an
  invented value outside the listed ones (R-020). On the outside-writer sets many questions list no
  wrong value, so a reply that adds something false is not caught there (R-143, R-152). It does not
  look for leaked tool text, which only base produced (R-144).
- **Shared briefs.** `hard_dev` and the wide training pool were written to briefs like the sealed
  `independent` pool's, so condition C and D are less independent of development than when
  registered; one discarded writer saw fragments of sealed wording (R-066, R-069, R-070).
- **The baselines tried.** Base with the tool, base with two fixed prompts (R-137, R-161) and base
  with the whole chat on short chats (R-164, R-165). No search over prompts and no other retrieval
  system was tried.

## 13. Errors and corrections

Each error below was found during the work and is recorded where it happened.

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
- **A toolkit defect** in AuditKIT's bootstrap (R-031, section 11).
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

## 14. Limitations

- **Short chats are better shown whole.** Given the whole chat, the trained model and base show
  no measured difference (one seed, two sets of 40 chats; gaps under about 15 points on a kind of 40 questions could not be seen, R-142). On chats of about 1,400 tokens the whole
  chat beats the three-exchange view with search (section 6). The adapter's case rests on chats too
  long to show, and the whole-chat reading at that length is not measured.
- **Tag questions.** 6.37 goes along with most false claims in "..., right?" questions (section 8).
- **Found but not used.** Its commonest miss on generated chats finds the right line and answers
  from its first clause, leaving out a detail later in the line (R-144, R-149); on outside-writer
  chats the commonest is a search that misses, including facts told with a pronoun (R-146).
- **One model, one size, English only.** Only Tiny Aya Global was trained; the friend's messages are
  all English.
- **Generated or agent-written chats only.** No chat is from a real person. Corrections, phone-style
  typing, an earlier question in view, four decoys and chats of 1,000 and 2,000 messages were tested
  on generated chats (R-102 to R-133, R-138, R-148). LoCoMo, a public chat set, was registered as an
  outside check and deferred; it was never run (R-100, R-139 item 6).
- **One tool, read only**, with a fixed three-exchange view. The model cannot save a note.
- **No hostile text.** Instructions hidden in retrieved passages are out of scope.
- **Greedy decoding only**, and **one machine**: times are an RTX 3080's.
- **Judged by models, not people** (sections 5 and 12).

## 15. Future work

- **Measure the whole chat at length.** Base and 6.37 with every message in view on 419-message
  chats, on a card that holds them, to find where searching starts to beat reading.
- **Ground tag questions.** 7.1 showed the search can be trained (R-158); the next step is queries in
  the claim's own words (R-159's 7.2 design), judged on a new outside-writer set.
- **Injection in retrieved text.** Train the model to treat instructions inside search results as
  content, and test it with hidden instructions in earlier messages.
- **Writing memory.** A tool that saves a note, so the model decides what is worth keeping.
- **Reinforcement on verified outcomes.** The decision to search and the answer are checkable by
  code, so they suit reward-based training (for example GRPO through AgentTune).
- **Other languages and larger models**, with the same sealed-test protocol.
- **Real conversations**, with consent, and a human panel beside the model judges.
- **Upstream fixes.** Offer the lean loss to TRL and the bootstrap fix to AuditKIT.

## 16. Reproduce

Everything runs on one 10 GB card. Every results file carries its provenance (command, commit,
package versions).

- **The sealed run:** `scripts/records/queue/final.sh` (run by the queue), starting with
  `scripts/records/freeze_r154.py check` on `results/freeze/sealed_manifest.json`; scored by
  `scripts/records/score_r162.py` into `results/analysis/R-162/`; sheets from
  `scripts/records/sheets_r162.py`, judges' briefs from `scripts/records/briefs_r162.py`, judge
  transcripts audited by `scripts/records/audit_judge_r162.py`.
- **Analyses:** `scripts/records/writeup_r164.py` (`results/analysis/R-164/`),
  `scripts/records/blind_r146.py` and `scripts/records/blind2_r157.py` (the outside-writer sets),
  `scripts/records/rigor_r139.py` (development rigor).
- **This article and the model card:** `PYTHONPATH=src python scripts/make_article.py`, from their
  templates in `docs/`; figures by `scripts/make_figures.py`. No result number in either is typed by
  hand.

## Author contributions

Kevin Vaillancourt directed this work, carried out with an AI assistant, Claude (Anthropic), as an
executive-function accommodation. Test pools and chat sets meant to be independent were written by
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
