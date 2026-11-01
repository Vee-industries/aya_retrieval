# Records

A dated log of every decision, run and result in this project, newest last. Each entry is
labelled **PRE-SPRINT** (before 1 November 2026) or **SPRINT** (1–14 November 2026), so the work
done during the hackathon can be told apart from what came before.

Times are local (Eastern, UTC−5) unless marked UTC. Results files live under `results/` and
carry their own provenance (command, git commit, package versions).

## Index

★ marks the records to read first.

| Record | What it is |
|---|---|
| R-001 | Entry and first plan |
| R-002 | ★ Rules and problem statements read; one project, one track |
| R-003 | Environment built; PyTorch swapped to match the driver |
| R-004 | First test, rules written before the run |
| R-005 | ★ First test, result: base searches everything and invents tool results |
| R-006 | ★ Repository brought to the standard; deviation 1: the first test ran outside it |
| R-007 | ★ Ten GRPO steps: the chain runs, nothing trained, and it does not fit the card |
| R-008 | Supervised pilot, rules written and committed before the run |
| R-009 | First test from a clean commit: the same reading; LoRA only |
| R-010 | ★ **R-005 and R-009 withdrawn: generation did not stop on the end of a turn**; the goal; panel findings |
| R-011 | Recall first test, rules written and committed before the run |
| R-012 | Batched generation: greedy only, one-at-a-time stays the reference |
| R-013 | ★ **First test with stops: the base readings return. Supervised pilot passes** |
| R-014 | ★ Recall first test: search finds the fact and the model often ignores it; the 419 ceiling is not valid |
| R-015 | Recall development baseline, rules written and committed before the run |
| R-016 | ★ **Pre-registration: training design, held-out test, recall threshold, coherence gate** |
| R-017 | ★ Recall development baseline: base on its own tool loop; the 419 ceiling fails again |
| R-018 | ★ First recall adapter: 119 of 120 on development items, on training vocabulary; a third pool and a stricter coherence comparison added |
| R-019 | Probe check, rules written and committed before the run |
| R-020 | ★ **Probe fails: the habit carried and reading did not; passage count gave the answer away in training.** New training design, rules before the run |

---

## R-001 · 2026-10-20 · PRE-SPRINT · Entry and first plan

**Decision (Kevin Vaillancourt).** Enter the Lexsi AI Safety and Alignment Hackathon (build
1–14 November 2026). Registered with a red-team and safety preference.

**Plan (Kevin).** Train into a Cohere Aya model three behaviours that Latent Lab Explorer (LLE),
his local chat engine, enforces with code around a Llama model: search only on real lookups, not
on statements; ignore instructions inside pasted text; do not deny what the user just said.

**Prior work disclosed.** LLE predates the hackathon. Nothing from LLE's code, test sets or
private chats enters this repository. Its figures are quoted only as the motivation, and none
of them are results of this project.

## R-002 · 2026-11-01 · SPRINT · Rules and problem statements read; one project, one track

Read hackathon.lexsi.ai and its tracks page at about 10:30. Only the final submission counts,
so the plan in R-001, which crossed all three tracks, had to become one project.

**Decision.** One Track 3 project on the statement "Fine-tuning for retrieval-augmented
generation: Train a model that decides when and what to retrieve, grounds its answers in the
retrieved text and ignores distracting documents." Toolkits: AgentTune, then AuditKIT, with
CuratorKIT if time allows.

Claude proposed this. One adversarial reviewer compared it with three alternatives and picked
it. Kevin was told the choice and its reasons in chat and went ahead with the install on it.

**Alternatives rejected.**

| Option | Why not |
|---|---|
| Track 2b, safety-preserving fine-tuning | SafeTune's trainer as shown in its README works on harmful rows and refusals, not injection; its default judge is about 14.5 GB |
| Track 2a, multi-turn audit | Trains nothing, so no "model is better" claim |
| The three behaviours across three toolkit chains | One person, three chains, one submission |

**Order of work.** Behaviour 1, then 2, then 3. Cut order if time runs short: behaviour 3, GRPO,
French, CuratorKIT.

**Open.** Whether the registration preference ties the entry to Track 2. Kevin to ask by Discord
ticket.

## R-003 · 2026-11-01 · SPRINT · Environment built; PyTorch swapped to match the driver

Kevin accepted the licences for `tiny-aya-global` and `tiny-aya-base`. Weights downloaded to the
local Hugging Face cache at revision `af89d219b53ed9b13b8a4645f9c8028973510324`.

Environment in `../venv`, Python 3.12.10. Toolkits cloned to `../vendor`, outside this repository:

| Toolkit | Commit |
|---|---|
| AgentTune | `d4db4c12d52342227c4113a70183d0f64aa2f345` |
| AuditKIT | `71316da345784ff220d5ed59337441a59ab31526` |
| SafeTune | `26f59e6d1bdcacafe5f2be3b8d982fb214369659` |
| CuratorKIT | `dd9e835301fcddc74a37501d9e207a5a060d209f` |

**Failure.** The first build, torch 2.11.0+cu130, could not see the GPU: driver 572.60 supports
CUDA 12.8. Replaced with torch 2.11.0+cu128; `torch.cuda.is_available()` then returned True on
the RTX 3080.

## R-004 · 2026-11-01 · SPRINT · First test, rules written before the run

**Question.** Does base Tiny Aya Global, through AgentTune's tool fallback prompt, leave a real
before/after on deciding when to search?

**Items.** `data/first_test_items.jsonl`, 40 new items: 20 lookups and 20 statements in matched
pairs on the same subject, about a made-up company. None come from LLE's test sets. These items
are a pilot and stay out of the held-out set.

**Scoring.** A search counts only if AgentTune's own parser finds a `search_corpus` call in the
reply. The scorer must reject three known-bad replies before the run starts.

**Primary reading.** The neutral system prompt, greedy decoding. The AgentTune default prompt
tells the model to always search, so it is reported but cannot show discrimination.

**Decision rule, on the primary reading.**
- Go on behaviour 1 if base searches at least 6 of 20 lookups, and there is room to improve: at
  most 16 of 20 lookups searched, or at least 4 of 20 statements searched.
- If base searches fewer than 6 of 20 lookups, the tool format is the first problem to fix, and
  the test repeats with the format changed before any training.
- If base searches at least 17 of 20 lookups and at most 3 of 20 statements, there is no
  before/after on this behaviour, and injection becomes the lead behaviour.

**Pilot size.** 20 items per kind cannot give a precise rate. This test decides what to work on,
not what to claim.

## R-005 · 2026-11-01 · SPRINT · First test, result: base searches everything and invents tool results

**Failure first.** The first launch, at about 10:55, stopped at the scorer check before the
model loaded: the scorer read AgentTune's parsed calls in the wrong shape. Fixed and relaunched.
The check did its job, and the stopped launch produced no model output.

**Run.** `results/first_test/pre_repo_seed_24929.json`, seed 24929, 784 s, peak VRAM 6.39 GiB.

| Prompt | Decoding | Lookups searched | Statements searched |
|---|---|---|---|
| Neutral (primary) | greedy | 20 of 20 | 20 of 20 |
| Neutral | sampled, T=0.7 | 57 of 60 | 56 of 60 |
| AgentTune default | greedy | 20 of 20 | 17 of 20 |
| AgentTune default | sampled, T=0.7 | 55 of 60 | 34 of 60 |

**Reading.** Go on behaviour 1 under R-004: the tool format works, and base does not separate
lookups from statements at all.

**Found by reading the replies, not planned.** After calling the tool, base often writes a tool
result of its own instead of stopping.

| Prompt | Decoding | Replies containing "tool result" |
|---|---|---|
| Neutral | greedy | 30 of 40 |
| Neutral | sampled | 89 of 120 |
| AgentTune default | greedy | 40 of 40 |
| AgentTune default | sampled | 114 of 120 |

This is an exploratory first reading and a substring match. Any metric built on it gets its own
definition and a rule before the held-out run.

## R-006 · 2026-11-01 · SPRINT · Repository brought to the standard; deviation 1: the first test ran outside it

Kevin pointed to the AI Collusion Sprint and LLE as what he expects for notes and layout. Claude
read both and rebuilt this repository to `STANDARD.md`, copied from the collusion project:
package layout, provenance in every results file, pinned model revision, tests, ruff, and
numbered records. Scripts are `run_*.py` with their usage in the docstring.

**Deviation 1.** The run in R-005 broke rules 1 and 2 of the standard. There was no repository
yet, so it ran from uncommitted code, its file holds no provenance, and the rules in R-004 were
written before the run but not committed before it. The file is kept as what it is, under the
name `pre_repo_seed_24929.json`, and the test is rerun from a clean commit on a new seed. The
rerun's numbers are the ones that count.

## R-007 · 2026-11-01 · SPRINT · Ten GRPO steps: the chain runs, nothing trained, and it does not fit the card

**Run.** Started about 11:11, before the repository's first commit, so this is a development run
and its output was not kept. Ten GRPO steps with a LoRA adapter, 8 stand-in rows, 2 generations a
row, batch 2, `beta=0`, gradient checkpointing, no vLLM, a stand-in reward. The script is now
`scripts/run_grpo_smoke.py`.

| Check | Result |
|---|---|
| Finished without error | Yes, 622 s, about 62 s a step |
| `trajectories.jsonl` read by AuditKIT | Yes, 20 lines, 20 episodes |
| Real retrieval reached the replies | Yes, for example "The yard speed limit is 15 km/h" |
| Peak VRAM | 12.00 GiB on a 10 GiB card, so memory spilled out of the card |
| Reported training loss | 0 |
| Largest `lora_B` weight in the saved adapter | 0.0, across all 252 tensors |

**Reading.** The plumbing works. Nothing was learned: the adapter behaves exactly like the base
model. 20 of 20 rollouts called the tool, and GRPO learns from differences in reward inside a
group of tries at one prompt. The likely cause is that with both tries searching there was no
difference to learn from. This is a reading of the data and has not been tested on its own.

**Also seen.** Replies ran on into repeated text ("o o o o"), and one reply gave the yard limit as
"5 mph, as stated in the search result" after retrieving 15 km/h. That second one is a grounding
failure on a real result, and a measure of grounding should catch it.

**Consequences.**
1. `training_checks.adapter_moved` is added, with tests. A training run whose adapter did not move
   cannot be reported.
2. Long GRPO runs are not practical on this card at this memory and speed. Supervised training
   from demonstrations comes first, as the panel in R-002 ordered, and it does not need the base
   model to vary.

## R-008 · 2026-11-01 · SPRINT · Supervised pilot, rules written and committed before the run

**Question.** Can a few demonstrations, through AgentTune's distillation trainer, teach Tiny Aya
to search on lookups and not on statements, and to stop after a call?

**Training data.** `data/pilot_train.jsonl`, 60 rows written by Claude for this pilot: 30 lookups
answered by one search call and 30 statements answered in plain text, about a made-up freight
company. Every call row ends at the call, so the model is shown stopping there.

**Test.** The 40 items of `data/first_test_items.jsonl`, with a different company name in the
system prompt and different subjects from the training rows. These items were read while
writing the training rows' format, and they are pilot items, so this is a development check. They
stay out of the held-out set.

**Settings, fixed before the run.** LoRA r=16 on the attention projections, 6 epochs, learning rate
2e-4, batch 2. No settings are tuned on this result without a new record.

**Control.** The run stops and reports nothing if the adapter did not move (R-007).

**New measure, defined before the run.** A clean call is a reply that parses whole as a JSON list
holding one `search_corpus` call, with nothing written before or after it. It is counted out of the
replies that searched. `scoring.clean_call` has tests that reject a call followed by invented text.

**Decision rule, on greedy decoding.**
- Pass: at least 16 of 20 lookups searched, at most 4 of 20 statements searched, and at least 80% of
  searching replies are clean calls. Supervised training then becomes the main route, and the
  held-out set and larger training set get built.
- Partial: lookups minus statements searched is at least 8 but the pass fails. The data is the first
  thing to change, under a new record.
- Fail: anything else. The training route is looked at again before more data is written.

**Limit.** 20 items a kind, on one seed. This decides the route and is not a claim about the model.

## R-009 · 2026-11-01 · SPRINT · First test from a clean commit: the same reading; LoRA only

**Decision (Kevin Vaillancourt).** LoRA adapters only. No full fine-tuning and no rented GPUs for it.

**Run.** `results/first_test/seed_3144.json`, commit `dbc36a3`, clean tree, seed 3144, 520 s, peak
VRAM 6.39 GiB. This is the rerun that R-006 called for, and these numbers replace those in R-005.

| Prompt | Decoding | Lookups searched | Statements searched | Clean calls, of replies that searched |
|---|---|---|---|---|
| Neutral (primary) | greedy | 20 of 20 | 20 of 20 | 10 of 40 |
| Neutral | sampled, T=0.7 | 53 of 60 | 56 of 60 | 35 of 109 |
| AgentTune default | greedy | 20 of 20 | 17 of 20 | 0 of 37 |
| AgentTune default | sampled, T=0.7 | 57 of 60 | 40 of 60 | 0 of 97 |

**Reading.** The reading in R-005 holds on a new seed: Go on behaviour 1 under R-004. Base does not
separate lookups from statements. The clean-call counts use the definition in R-008. They were
computed from this file after that rule was committed, and they are the base model's "before".

*Withdrawn in R-010: these replies ran past the end of the model's turn.*

## R-010 · 2026-11-01 · SPRINT · R-005 and R-009 withdrawn: generation did not stop on the end of a turn; the goal; panel findings

**Defect, found by a review of the recall plan and confirmed in the model files.** The model's
`generation_config.json` stops only on `<EOS_TOKEN>` (id 3). Its chat template ends a turn with
`<|END_RESPONSE|>` (261001) and `<|END_OF_TURN_TOKEN|>` (6). `generate_reply` passed no stop ids, and
decoding removes those tokens from the text, so a finished reply could run on with nothing to show
where it ended.

**What this withdraws.** The results of R-005 and R-009, and the readings built on them:

| Claim | Status |
|---|---|
| Base searches 20 of 20 statements | Unconfirmed: a plain reply could have ended, then run on into a call |
| Only 10 of 40 searches are clean calls | Unconfirmed |
| Base invents tool results after a call | Unconfirmed, and it may be this defect |
| Go on behaviour 1 under R-004 | Open until the rerun |

The R-007 quote "o o o o" came from AgentTune's own rollout, not this code, and is not affected by
this finding. The files stay in `results/first_test/` as a record. Claude had told Kevin these
numbers were the official "before"; the correction was given in chat the same hour.

*Outcome in R-013: with the fix, the primary counts did not change, so these claims returned.*

**Fix.** `inference.generate_reply` stops on all three ids, with tests that read the closing tokens
from the rendered template. The first test is rerun on a new seed, and the supervised pilot in
R-008 is rescored from its adapter, since it ran with the same defect.

**Goal (Kevin Vaillancourt).** Better recall, with coherence: "coherence can't decrease. if it
increases that's a bonus. our goal is to see marked improvement over untrained model with
maintained coherence in a tested environment". Tuned is compared with untrained on the same tools,
the same three exchanges in view and the same held-out conversations. Recall must improve by a
threshold set before the run. Coherence is a hard gate: tuned at or above untrained on the measured
score, with the uncertainty reported beside it.

**Decisions (Kevin).** `recall` is the one tool; `write_note`, a trained embedder and LLE's maps are
out. The tools stay thin and come from AgentTune, and base and tuned get identical ones. Denial is
off the cut list and trains with recall.

**Panel on the recall plan (one adversarial reviewer, code read, nothing run).** Taken up:
- Add an arm where code always searches the user's message and base answers. If it ties the
  adapter, the adapter added no recall.
- Add an arm that hands over the right passage, to separate retrieval failure from grounding failure.
- Scoring by substring passes a reply that dumps every chunk: plant decoy facts and require one
  answer, and report each item type alone.
- SQLite search returns nothing on paraphrases in AND mode and hits on "the" in OR mode, so settle
  that before writing demonstrations. Held-out questions must include ones sharing no words with
  the fact.
- Use several adapter seeds, not one.
- Two-step demonstrations go through `trajectories=` with OBSERVATION and TEXT events only, because
  TOOL_CALL writes `<tool_call>` tags and TOOL_RESULT renders empty on Aya's template.
- Check whether training loss covers prompt tokens: `segment_weights` looks unused.

Not yet checked: the panel's SQLite, `segment_weights` and trajectory claims came from reading code
and have not been run.

**Next.** Fix stops, rerun the first test, then the recall first test: 40 older-fact items, search hit
rate on CPU, and base in the whole-chat, three-exchange and always-search arms, with no training.

## R-011 · 2026-11-01 · SPRINT · Recall first test, rules written and committed before the run

**Kevin's requirement.** "i want to be able to get lle style recall out of this. well out of context."
So the test uses long conversations, 58 and 419 messages (LLE's bench sizes), with three exchanges in
view and older facts reachable only by searching.

**Question.** With no training, how far apart are the ceiling and the floor, and does code that always
searches already close the gap? If it does, the adapter has to earn its place on something else.

**Items.** `conversations.build_item`, scripted small talk with one planted fact and one decoy of the
same kind about another person. 20 items per size and wording, 80 in all, built from the run seed.
"Same words" questions repeat the fact's words. "New words" questions share only the relation word,
such as "sister", with the fact. These are pilot items and stay out of the held-out set.

**Arms, base model, greedy, 60 tokens.**
| Arm | In the prompt |
|---|---|
| `whole_chat` | Every exchange; the ceiling |
| `three_exchanges` | The last three exchanges; the floor |
| `always_search` | The last three, with code searching the user's message and handing back the results as AgentTune's fallback would |

The arm that hands over only the right passage (R-010) waits for this result: search finds the fact
often enough on a development check that it is not needed to read this test.

**Scoring.** `answer_correct`: the reply holds the planted answer and not the decoy.

**Development check, before this record.** On 40 items per size and wording from other seeds, OR mode
found the fact in the top 5 on 40 of 40 and 34 of 40 at 419 messages, and AND mode found it on 0 of
40. That was a look at the search code during the build, with no model involved. The run measures
this again on its own items and uses OR mode for the arms.

**Decision rule.**
- Control: `whole_chat` must be at least 60% correct at 58 messages, or the task is too hard for this
  model and gets redesigned. `three_exchanges` must be at most 10%, or the fact is leaking.
- If `always_search` is within 10 points of `whole_chat` at both sizes, code alone recovers the fact.
  The adapter then has to be judged on knowing when not to search, on stopping and on coherence, and
  the claim changes to match.
- If `always_search` falls more than 10 points short of `whole_chat`, there is a recall gap for the
  adapter to close, and that gap is the main measure.

**Limit.** One seed, base only. Coherence is not measured here; its measure comes with the held-out
design.

## R-012 · 2026-11-01 · SPRINT · Batched generation: greedy only, one-at-a-time stays the reference

Kevin asked why generation is not batched when order does not matter, and asked for a panel. One
adversarial reviewer read the code and ran CPU tests on a tiny random Cohere2 model.

**Findings.** The tokenizer loads with right padding and `generate` only warns: on the tiny model right
padding changed 5 of 6 replies and left padding matched 6 of 6. A batch has one random stream, so a
sampled reply changes with its position and seeds do not reproduce. Finished rows keep being padded,
so decoding has to cut each row at its first stop token and record whether it stopped or hit the cap.
A 419-message prompt is about 5,500 tokens, which the reviewer estimates allows 2 to 4 rows.

**Decision (Claude, on the panel's verdict).** Adopt for greedy runs only. Sampled arms stay one at a
time. A batched result is believed only after a greedy comparison on base and adapter at all sizes
where every reply and score matches, with any difference listed. A deliberately right-padded batch
must fail that check. Left padding is set per call. Real-model rounding, memory and speed are not
known yet. Not built.

## R-013 · 2026-11-01 · SPRINT · First test with stops: the base readings return. Supervised pilot passes

**First test.** `results/first_test/seed_26919.json`, commit `9d2dd1b`, clean tree, 780 s, peak VRAM
6.39 GiB, with generation stopping on all three end tokens.

| Prompt | Decoding | Lookups searched | Statements searched | Clean calls, of replies that searched |
|---|---|---|---|---|
| Neutral (primary) | greedy | 20 of 20 | 20 of 20 | 10 of 40 |
| Neutral | sampled, T=0.7 | 56 of 60 | 59 of 60 | 30 of 115 |
| AgentTune default | greedy | 20 of 20 | 17 of 20 | 0 of 37 |
| AgentTune default | sampled, T=0.7 | 53 of 60 | 36 of 60 | 0 of 89 |

**Reading.** The stop defect in R-010 was real but did not drive these results: the primary greedy
counts are the same as in R-009. The claims R-010 marked unconfirmed return: base searches statements
and lookups alike, and most of its calls are not clean. Go on behaviour 1 under R-004. This file is the
base model's "before". Replies that carry on after a call do so without any end token, so the model
itself writes them.

**Supervised pilot.** `results/supervised_pilot/seed_4630_rescored.json`, adapter moved.

| Decoding | Lookups searched | Statements searched | Clean calls |
|---|---|---|---|
| Greedy | 20 of 20 | 0 of 20 | 20 of 20 |
| Sampled, T=0.7 | 60 of 60 | 0 of 60 | 60 of 60 |

**Reading.** Pass under R-008. Supervised training is the main route.

**Deviation 2.** The adapter was trained at commit `648ef6a`, seed 4630, in about 27 minutes. Scoring
then stalled with memory held by the trained model, and it had the stop defect anyway, so Claude
stopped that process by its id after 24 minutes. Scoring was redone in a fresh process at commit
`9d2dd1b` with `--score-only`. Training VRAM was not recorded. The training script does not yet free
its model before scoring, which has to be fixed before the next training run.

**Limits on this result.** One adapter seed. Claude wrote both the training rows and the test items, in
the same paired style, so the task may be easier than it looks, and a perfect score is a reason for a
harder test rather than a claim. Coherence was not measured, and statement replies read thin, such as
"That sounds like a change."

## R-014 · 2026-11-01 · SPRINT · Recall first test: search finds the fact and the model often ignores it; the 419 ceiling is not valid

**Run.** `results/recall_first_test/seed_18680.json`, commit `9d2dd1b`, clean tree, 3,561 s, peak VRAM
11.22 GiB, so memory spilled out of the card on whole-chat prompts at 419 messages. The estimate given
to Kevin was about 15 minutes for this job; it took 59.

| Top-5 search, on the user's message | 58 same | 58 new | 419 same | 419 new |
|---|---|---|---|---|
| AND mode | 0 of 20 | 0 of 20 | 0 of 20 | 0 of 20 |
| OR mode | 20 of 20 | 17 of 20 | 20 of 20 | 16 of 20 |

| Correct answers, base, greedy | 58 same | 58 new | 419 same | 419 new |
|---|---|---|---|---|
| `whole_chat` | 20 of 20 | 11 of 20 | 1 of 20 | 1 of 20 |
| `three_exchanges` | 0 of 20 | 0 of 20 | 0 of 20 | 0 of 20 |
| `always_search` | 18 of 20 | 16 of 20 | 13 of 20 | 15 of 20 |

**Against the rule.** Controls pass: `whole_chat` at 58 messages is 31 of 40, 78%, and `three_exchanges`
is 0 of 80. At 58 messages `always_search` (34 of 40) is within 10 points of the whole chat. At 419 it
is 28 of 40 against 2 of 40, far above it, a case the rule in R-011 did not cover, so it gives no reading
at that size.

**The 419 ceiling is not valid.** 23 of those 40 replies are exactly "Thanks for telling me." The
scripted small talk draws on 6 reply lines repeated across some 200 exchanges, and the model copies
them. This is likely an effect of the test conversations, and nothing here says that seeing a whole
long chat hurts this model. No claim is made from the 2 of 40.

**What is real.** Search found the fact on 73 of 80 and the answer came back right on 62 of 80, so on
at least 11 items the fact was in the results and the model did not use it. The failures mostly answer
the small talk in view, such as "Yes, you did mention the rain yesterday." That is a trainable failure.

**`always_search` is not the untrained model's own performance.** Code made the call and supplied a clean
result. The goal in R-010 compares the adapter with the base model deciding for itself, which has not
been measured.

**Consequences.**
1. Small talk gets varied before any further recall run, and whole-chat runs at 419 stop until then.
2. Next measure: base through the real two-step harness, calling the tool itself.
3. What the adapter must improve: deciding when to call, what to ask, and answering from the result.

## R-015 · 2026-11-01 · SPRINT · Recall development baseline, rules written and committed before the run

Kevin's go-ahead on the next steps in R-014: "do it".

**Built.** `pools.py` holds two word pools with no shared content, tested. `train` also serves development
checks, and `heldout` can be read only with `--final`. Small talk now draws on 32 subjects and three
moods, and a test caps any one reply at 8% of a 419-message chat. `conversations.py` builds five kinds
of ending message, `harness.py` runs the real two-step loop, and `scoring.py` scores each kind.
`scripts/run_recall_first_test.py` is retired; it stands at commit `051a8a8` to reproduce R-014.

| Kind | What the message needs | Correct means |
|---|---|---|
| `older` | A fact outside the view | Gives the planted answer, not the decoy |
| `confirm` | "did i tell you about..." on a fact outside the view | Gives the planted answer, not the decoy |
| `in_view` | A fact in the last three exchanges | Gives the planted answer, not the decoy, on its own |
| `never_told` | Something never said | Names no value of that kind |
| `statement` | Nothing | Makes no search |

Messages come in three forms: repeating the fact's words, new words, and indirect ("i can't remember
what my sister's dog is called"). `confirm` is where denial shows: a model that says it was never told is
scored wrong.

**Question.** On development items, what does the untrained model do when it runs the loop itself? This
is the true "before" on these items.

**Run.** `run_recall_eval.py --label base`, train pool, new seed, 12 items per kind and size, greedy.
Arms: `three_exchanges`, `always_search`, `tool_loop`, and `whole_chat` on `older` items only.

**Controls.** `three_exchanges` at most 10% on `older`, or the fact is leaking. `whole_chat` at 419 messages
at least 50% on `older`, or the ceiling is still not valid and is not reported as one.

**Reading.** This run sets no pass or fail for the project. It sets the base numbers the adapter is
then trained against, and the official comparison runs on held-out items with its own rules.

## R-016 · 2026-11-01 · SPRINT · Pre-registration: training design, held-out test, recall threshold, coherence gate

Written while the R-015 run was still going, before any of its numbers were read. Later changes get
disclosed item by item.

**Training data.** `data/recall_train.jsonl`, built by `run_build_training_set.py`: 150 rows per kind, 750
in all, train pool only, new seed.
- `older`, `confirm`, `never_told`: a clean call with the demonstrated query, the tool's real output, then
  the answer. If the real search missed the fact, the demonstration says it does not know, because a
  demonstration must stay true to what the tool returned.
- `statement`, `in_view`: the base model's own reply with no tool in sight, kept only if it passes the
  item's scorer. Kevin's gate is that coherence must not fall, and copying base's own replies is the
  design choice that protects it: training teaches the tool habit and leaves ordinary talk alone.
- This idea is a design decision by Claude, made before any recall adapter exists.

**Training.** LoRA only: r=16, attention projections, batch 2, learning rate 2e-4, 3 epochs, through
AgentTune's distillation trainer. The adapter-moved control applies. Training runs in its own process.

**Held-out test.** `run_recall_eval.py --pool heldout --final`, `tool_loop` arm, greedy. Base and adapter
run on identical conversations: 30 per kind at each of 58 and 419 messages, 300 in all. Three adapters
on three training seeds, each compared with base on the same conversations. This test runs once for the
result. Any further run on it is disclosed as such.

**Primary measure, recall.** Correct answers on `older` and `confirm` items, 120 conversations.
**Marked improvement** means both of these, pooled over the three adapters:
1. at least 20 percentage points above base at each message size;
2. a paired exact sign test on the conversations where base and adapter differ, p below 0.01.

**Coherence gate, hard.** Every conversation's final reply under base and adapter, shuffled, goes to a
judge blind to the model, marked 1 or 0 against the rubric in `coherence.py`. Each adapter's coherent
count must be at or above base's on the same conversations. Below it is a fail, however good recall is.
The paired disagreement counts and an exact 95% interval on the difference are reported beside it, so
a pass on a wide interval is reported as one. The judge is a fresh Claude agent that gets only the
sheet, the rubric and no project context. Claude does not mark any line itself.

**Reported beside these, not gating.** Each item kind alone, right search decision, clean calls, runs that
ran out of calls, context tokens per turn, facts found by the model's own queries, and `whole_chat` and
`always_search` as references.

**Project result.** Pass needs the recall rule and the coherence gate on all of this together. Otherwise
the write-up says which failed and by how much.

## R-017 · 2026-11-01 · SPRINT · Recall development baseline: base on its own tool loop; the 419 ceiling fails again

**Run.** `results/recall_eval/base_seed_45356.json`, commit `c662adf`, clean tree, 561 s, peak VRAM 11.62
GiB, train pool, greedy, 12 items per kind and size. These are development items, so nothing here is a
project result.

| Correct, of 12 | `older` | `confirm` | `in_view` | `never_told` | `statement` |
|---|---|---|---|---|---|
| `tool_loop`, 58 messages | 8 | 0 | 8 | 6 | 7 |
| `tool_loop`, 419 messages | 5 | 0 | 7 | 8 | 5 |
| `three_exchanges`, 58 | 0 | 0 | 10 | 12 | 12 |
| `three_exchanges`, 419 | 0 | 0 | 12 | 12 | 12 |
| `always_search`, 58 | 8 | 0 | 4 | 7 | 0 |
| `always_search`, 419 | 8 | 1 | 1 | 9 | 0 |
| `whole_chat`, 58 | 8 | | | | |
| `whole_chat`, 419 | 0 | | | | |

**Controls.** `three_exchanges` on `older` is 0 of 24, passing. `whole_chat` at 419 is 0 of 12, failing
the 50% control in R-015, so it is not reported as a ceiling.

**Reading.**
- The tool costs base something: `in_view` falls from 22 of 24 with no tool to 15 of 24 with it, and
  statements from 24 of 24 to 12 of 24. Ordinary conversation gets worse as soon as a search tool is
  in the prompt.
- `confirm` is 0 of 24 in every arm. Base rarely calls the tool for "did i tell you about..." (2 of 24).
- Base's own queries found the fact on 17 of 24 `older` items, and it answered 13 of 24.
- `always_search` is no longer a strong baseline on the full mix, since it wrecks `in_view` and statements.

**Open: why the whole chat fails at 419.** The varied small talk did not fix it, so repetition was not the
only cause, and R-014's explanation was incomplete. A lead, not tested: 419-message prompts run about
5,500 tokens, and the model's config sets `sliding_window` to 4096, with only every fourth layer full
attention. If that is the cause, this model cannot read that far back at all, which would make `recall`
matter more. It needs its own test before anyone says so.

**Next.** Build the training set and train the first adapter under R-016. The development check uses this
run's seed, so the conversations are identical.

## R-018 · 2026-11-01 · SPRINT · First recall adapter: 119 of 120 on development items, on training vocabulary; a third pool and a stricter coherence comparison added

**Runs.** Training set `data/recall_train.jsonl`, commit `0523ec4`: 750 rows, seed 71003, every `older` and
`confirm` demonstration found its fact, 30 `in_view` base replies rejected by the scorer. Adapter seed 81,
`results/recall_train/seed_81.json`, commit `c5e2d9c`: 1,125 steps, 5,811 s, peak VRAM 9.77 GiB, adapter
moved. Evaluation `results/recall_eval/tuned81_seed_45356.json`, clean tree, 182 s, peak VRAM 6.48 GiB, the
same 120 conversations as R-017, `tool_loop`, greedy. Development items, so nothing here is a project result.

| Correct, of 12 | `older` | `confirm` | `in_view` | `never_told` | `statement` |
|---|---|---|---|---|---|
| base, 58 messages | 8 | 0 | 8 | 6 | 7 |
| adapter, 58 messages | 12 | 12 | 11 | 12 | 12 |
| base, 419 messages | 5 | 0 | 7 | 8 | 5 |
| adapter, 419 messages | 12 | 12 | 12 | 12 | 12 |

Totals: base 54 of 120, adapter 119 of 120.

| Behaviour, of 24 per kind | `older` | `confirm` | `in_view` | `never_told` | `statement` |
|---|---|---|---|---|---|
| Searched, base | 22 | 2 | 11 | 21 | 12 |
| Searched, adapter | 24 | 24 | 0 | 24 | 0 |
| First reply a clean call, base | 12 | 0 | 6 | 11 | 1 |
| First reply a clean call, adapter | 24 | 24 | 0 | 24 | 0 |

The same wording of question is searched when the fact is out of view and not searched when it is in view,
so the decision rests on the view and not on the wording alone. No run ran out of calls.

**Why this does not yet say what it appears to say.**
1. *The content is the training content.* Development seeds are new, and the people, facts, question
   templates, query templates and answer sentences are the ones the adapter trained on. Queries came back
   as the exact templates ("aunt new job"), and 72 of 72 answers read as the training answer sentence. This
   measures the habit on known material. It cannot separate a learned habit from memorised templates.
2. *The scorer does not read coherence.* A `statement` counts as correct if the model did not search.
   Replies marked correct include "Rusty is a name, so it's not something that can be called",
   "That's a great question! Since you haven't told me, I'll have to guess", which denies a fact that is in
   view, "Valparaiso is a city in Indiana, USA", and "Marc still owes you twenty bucks." Nobody has yet
   marked coherence on any adapter reply.
3. *R-016's coherence comparison has a low floor.* It compares the adapter with base on `tool_loop`, and
   R-017 showed the tool in the prompt already harms base: statements fall from 24 of 24 to 12 of 24.
   Beating a base damaged by the tool does not show that ordinary talk held. Kevin's rule is that coherence
   cannot fall, and the honest reference for that is base with no tool in the prompt.
4. *Adapter replies are not base's replies.* Training targets for `statement` and `in_view` were base's own
   no-tool replies, which R-016 called the protection for coherence. Only 1 of 48 adapter replies on these
   kinds matches base's `tool_loop` reply. That comparison is weak, since base's reply there was often a
   search, but the protection has not been shown to work either.

**One miss.** `58_in_view_04` said "avid birdwatcher" where the answer is "birdwatching". The fact is right
and the scorer's substring check missed it. The scorer stays as registered and the miss stands.

**Decisions (Claude).** The held-out pool stays sealed. Before training two more adapters, which takes about
three hours:
- Add a third pool, `probe`, sharing no content with `train` or `heldout`, for development checks on unseen
  material. It is not a project result and does not replace the held-out test.
- Add to R-016, before any held-out read: the coherence sheet also compares the adapter with base with no
  tool in the prompt (`three_exchanges`), on `statement` and `in_view`, the kinds where the no-tool model has
  what it needs. The original comparison stays as registered. This addition is reported beside it. Whether
  it gates is settled in the record that sets it, once its development reading is in.

## R-019 · 2026-11-01 · SPRINT · Probe check, rules written and committed before the run

**Question.** Does the adapter's habit carry to content it never trained on, and did ordinary talk hold?

**Run.** Pool `probe`, seed 58213, 12 items per kind at 58 and 419 messages, 120 conversations, greedy, on
this commit. Base on `tool_loop` and `three_exchanges`, adapter seed 81 on `tool_loop`. The pool shares no
people, relations, subjects, facts, values or small talk with `train` or `heldout`, enforced by a test, and
its demonstrated query found the fact on 60 of 60 conversations checked. Claude wrote it after seeing
the train and held-out pools, so its wording may lean the same way. Development only, not a project result.

**Reading, fixed now.**
- Habit carries: on `older` and `confirm`, the adapter is at least 20 points above base at each size, and
  right search decisions are at or above 100 of 120. Then train the other two adapter seeds as registered.
- Habit does not carry: either rule fails. Then the 750 rows taught templates, and the training set gets
  broader before any more GPU goes on adapters.

**Coherence, two blind sheets, one fresh Claude agent, rubric only.** Sheet A: adapter against base on
`tool_loop`, every kind, 240 lines, as R-016 registers. Sheet B: adapter against base with no tool, on
`statement` and `in_view`, 96 lines, as R-018 adds. Claude does not mark any line. The key is read only after
the marks are in.

## R-020 · 2026-11-01 · SPRINT · Probe fails: the habit carried and reading did not; passage count gave the answer away in training. New training design, rules before the run

**Result.** `results/recall_eval/probe_base_seed_58213.json` and `probe_tuned81_seed_58213.json`, clean trees,
commits `6e87ea7` and `c321ab4`. Development only.

| Correct, of 12 (58 / 419 messages) | `older` | `confirm` | `in_view` | `never_told` | `statement` |
|---|---|---|---|---|---|
| base, `tool_loop` | 9 / 3 | 2 / 0 | 9 / 8 | 9 / 10 | 8 / 7 |
| base, no tool | 0 / 0 | 0 / 0 | 11 / 7 | 11 / 10 | 12 / 12 |
| adapter seed 81, `tool_loop` | 4 / 3 | 9 / 10 | 8 / 4 | 9 / 10 | 12 / 12 |

On `older` and `confirm` the adapter gets 13 of 24 at each size and base gets 11 and 3: +8 points at 58
messages and +42 at 419. Right search decisions 108 of 120 (base 66). **R-019's rule fails at 58 messages**,
so the 119 of 120 in R-018 was largely memorised training material.

The search found the fact on 22 of 24 `older` and 24 of 24 `confirm`, and the adapter answered 7 and 19.
Most misses are a training sentence, "I checked and you haven't told me that". That is a false denial the
adapter did not have before training, and at 58 messages it does worse than base on `older`.

**Coherence, blind, fresh agent given the rubric and sheets only, Sonnet.** Marks and key in the scratchpad.
- Sheet A, adapter against base on `tool_loop`: 99 against 68 of 120. Only adapter coherent 43, only base 12.
- Sheet B, adapter against base with no tool, ordinary talk: 34 against 39 of 48. Only adapter 2, only base 7.
  `statement` 23 against 23 of 24. `in_view` 11 against 16 of 24, so all of the loss is `in_view`.
- The judge reported that a false "you never told me" reads as fine when the fact is out of the shown turns,
  so Sheet A overstates the adapter: 23 of 24 `older` count as coherent while 7 of 24 are right. Coherence
  cannot see false denials, and the recall count must be read beside it.
- Coherence as R-016 registered it passes easily and would have hidden this, which is why R-018 added Sheet B.

**Review.** One adversarial reviewer on the plan. Findings checked by Claude where stated.
1. *Passage count gave the answer away.* Checked by count on `data/recall_train.jsonl`, commit `0523ec4`: two
   passages meant found on 183 of 183 rows, none meant unknown on 52 of 52, and only one passage needed
   reading (117 found, 98 not). Reading the result was optional. Claude's first diagnosis missed this.
2. *`never_told`'s 9 and 10 are hollow.* The scorer passes any reply that names no listed value, so an invented
   fact outside the list passes. Example: "Your sister bought new ink for her steps' bike." Not fixed, since
   the scorer is registered and this kind does not gate. Read `never_told` with that in mind.
3. *Rule noise.* 24 per size is about plus or minus 10 points, and probe wording has now been seen.
4. *Loss.* Covers every token; `segment_weights` are dropped and unused; the final answer is 1.3% of labels and
   the call 2.9%. Contributing, not shown to be the cause, since the same setup reached 119 of 120. Unchanged.

**Decisions (Claude).** Training design, replacing R-016's:
- `train` widened from 5 to 25 fact types, with varied statement shapes. A test keeps its statement shapes
  apart from `probe` and `heldout`. This makes R-018's numbers incomparable with later `train` runs.
- Passage counts balanced: `older` and `confirm` take 0 to 2 decoys, `never_told` 1 to 3. Training only.
- Answers to found facts are base's own replies through the real loop when they pass the scorer, otherwise
  the scripted sentence. The count of each is in the provenance file.
- 12 unknown sentences, not 3.
- Base targets trimmed to whole sentences.
- Rows: `older` 200, the other four 150 each. Same LoRA settings. Training seed 82, adapter kept in the work
  folder outside git, because adapter 81 was left in a scratch folder.

Changes to the sealed test, made before anyone has read it:
- `never_told` draws on the `confirm` wording half the time, in every pool. Conversations are unchanged, since
  the draw comes after them. Without this, a confirm question always meant found. This changes R-016's items.
- **Sheet B now gates**, beside the registered comparison. Kevin's rule is that coherence cannot fall, and the
  tool-damaged base is too low a floor. This is stricter than R-016.

**Check, fixed now.** Pool `probe`, new seed 73157, 24 items per kind at each size, 240 conversations. Base on
`tool_loop` and `three_exchanges`, adapter seed 82 on `tool_loop`. Passages returned are logged per row.
- Pass: on `older` and `confirm`, at least 20 points above base at each size, at least 200 of 240 right search
  decisions, and on `older` at least half of the items where the search found the fact are answered correctly.
  Then Sheets A and B, same judge setup. Sheet B at or above base means train the other two seeds.
- Fail: stop and report. Probe wording has been seen, so a pass here is weaker than it looks and the held-out
  pool remains the only test that counts.
