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
| R-016 | ★ **Pre-registration: training design, held-out test, recall threshold, coherence gate** (amended by R-038, R-039 and R-041) |
| R-017 | ★ Recall development baseline: base on its own tool loop; the 419 ceiling fails again |
| R-018 | ★ First recall adapter: 119 of 120 on development items, on training vocabulary; a third pool and a stricter coherence comparison added |
| R-019 | Probe check, rules written and committed before the run |
| R-020 | ★ **Probe fails: the habit carried and reading did not; passage count gave the answer away in training.** New training design, rules before the run |
| R-021 | ★ **Adapter seed 82 passes the probe rule and both blind coherence sheets**; false denials remain on `confirm`. Seeds 83 and 84 next |
| R-022 | One training sentence replaced to test the false denials on `confirm`; rule before the run |
| R-023 | R-022's rule passes: the new training data replaces the old |
| R-024 | Screens are full runs; fix 1 (read in-view facts) points the right way, too small to call |
| R-025 | Fix 1b (more hard in-view rows) beats the full adapter on the screen; confirmation rule registered |
| R-026 | ★ R-025's rule passes: fix 1b replaces v2 as the current set (v3) |
| R-027 | Sheet A on v3: above base overall, below base on `confirm` |
| R-028 | Fix 3 (fewer `never_told` rows) is worse than v3 on the screen: dropped |
| R-029 | ★ Fix 5 and fix 4 data built; training slowed by card memory, a lean loss fixes it; records moved out of scratch |
| R-030 | AuditKIT joins the evaluation: a second scorer and a second significance test, registered before use |
| R-031 | ★ AuditKIT's paired bootstrap is defective; R-030 uses a sign test and a centred bootstrap instead; AuditKIT on v3 |
| R-032 | Lean loss leaves v3 unchanged; fix 4 dropped; fix 5 ties on recall and does not restore `confirm` coherence; fix 5b next |
| R-033 | Fix 5b (scripted `confirm` answers) ties v3 on the screen; confirmation rule registered before its runs and marks |
| R-034 | R-033's rule fails on coherence: v3 stands; fix 5b is better than v3 on `confirm` coherence but still below base |
| R-035 | Fix 5c (answers name the relation) on the screen; confirmation rule registered before its runs and marks |
| R-036 | ★ R-035's rule passes: fix 5c replaces v3 as the current set (v4) |
| R-037 | v4 is a checkpoint: its misses ranked, and the next screens |
| R-038 | ★ Amendment to R-016, made before any held-out run: the registered test gets harder (crowded results, false retrieval) |
| R-039 | ★ Amendment to R-016 and R-038, before any final run: an independent, harder test pool |
| R-040 | Screens on v4: 4 epochs a candidate, learning rate 1e-4 dropped, fix 6 gains on recall; confirmation rule registered |
| R-041 | ★ Amendment to R-016, R-038 and R-039, before any final run: recall counted by source; the recall rule must also hold on retrieved answers alone |
| R-042 | Fix 6's remaining misses, and fix 7: searches in the friend's own words |
| R-043 | Wrong although retrieved: a reading failure; fix 8 states each training fact in more ways |
| R-044 | Capacity screens beat every data fix: LoRA on the MLP layers, and rank 32; R-040's confirmation superseded before it ran; combinations next |
| R-045 | R-038's crowded condition on the probe, development: v4 holds with four decoys |
| R-046 | Learning rate 3e-4 also beats v4: three ways to train harder all gain; two more combinations queued |
| R-047 | Fix 6 at rank 32 is the best screen (recall 92 of 96); stronger training costs a few statements on one opening |
| R-048 | Rank 32 with the MLP layers ties rank 32 alone; rank 32 alone stays the lead |
| R-049 | Confirmation rule for fix 6 at rank 32, written before its runs and sheets |
| R-050 | Fix 7 lifts recall to 94 but answers never-told questions with others' facts: dropped; fix 7b queued |
| R-051 | Fix 8 is a small, non-significant gain and misses its target; screened again at rank 32 |
| R-052 | Fix 6 with all three capacity changes is the best screen (95 of 96); R-049 superseded; confirmation rule |
| R-053 | Rank 64 adds nothing; rank 32 at 3e-4 without MLP fails one statement opening 8 of 10; R-052 stands |
| R-054 | Fix 7b brings never_told only part way back and loses statements: fix 7 line dropped |
| R-055 | R-052 fails on Sheet B at seed 82: v4 stands; statements answered with stored facts; fix 9 (more chat lines) |
| R-056 | Fix 9 passes the screen gate (statement 48, recall 94); fix 8 and 4 epochs dropped; fix 9 confirmation rule |
| R-057 | R-056 fails on Sheet B at seed 84 (statement 42 against 46): v4 stands; items 1 to 6 pass; Sheet A judges disagree |
| R-058 | Fix 10: blind judge vets statement training targets; gate and confirmation rule written first |
| R-059 | Fix 10 passes six of seven items (recall 282 of 288); seed 84 statement 45 against 46: v4 stands |
| R-060 | Fix 11: brief statement targets (hint left out of the row), vetted; rule written before the build |

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

**Coherence, blind, fresh agent given the rubric and sheets only, Sonnet.** Sheets, marks and key in `results/coherence/R-020/`.
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

## R-021 · 2026-11-01 · SPRINT · Adapter seed 82 passes the probe rule and both blind coherence sheets; false denials remain on `confirm`

**Result.** `results/recall_eval/probe2_base_seed_73157.json` and `probe2_tuned82_seed_73157.json`, clean trees,
commits `b649f6c` and `e84a0f8`. Training data `1069d0f`, adapter `7c14ba2`, peak VRAM 9.82 GiB. Development
only: probe wording has been seen, and the held-out pool remains the only test that counts.

| Correct, of 24 (58 / 419 messages) | `older` | `confirm` | `in_view` | `never_told` | `statement` |
|---|---|---|---|---|---|
| base, `tool_loop` | 14 / 9 | 1 / 6 | 18 / 16 | 20 / 22 | 18 / 13 |
| base, no tool | 1 / 0 | 0 / 0 | 17 / 19 | 24 / 24 | 24 / 24 |
| adapter seed 82, `tool_loop` | 14 / 20 | 14 / 11 | 17 / 20 | 24 / 23 | 24 / 24 |

R-020's rule, every part passes:
- `older` and `confirm` together: adapter 28 of 48 and 31 of 48, base 15 and 15. That is +27.1 points at 58
  messages and +33.3 at 419.
- Right search decisions 237 of 240 (base 119). Searches on `statement` 0 of 48, on `in_view` 2 of 48.
- On `older`, the search found the fact on 40 of 48 and the adapter answered 34 of those, 85%. Adapter 81 was
  7 of 22, so the reading failure R-020 set out to fix is fixed on this kind.

**Coherence, blind, fresh agent given the rubric and sheets only, Sonnet.** Sheets by
`make_coherence_sheet.py`, shuffle seeds 90411 and 90412. Sheets, marks and key in `results/coherence/R-021/`.
- Sheet A, adapter against base on `tool_loop`: 225 against 180 of 240. Only adapter coherent 55, only base 10.
- Sheet B, adapter against base with no tool, ordinary talk: 85 against 79 of 96. Only adapter 12, only base 6.
  `statement` 45 against 45 of 48. `in_view` 40 against 34 of 48. Adapter 81 lost this sheet, 34 against 39.

Both gates pass. Sheet B is at or above base, so R-020 says to train the other two seeds.

**Limits, read beside the pass.**
1. *False denials remain on `confirm`.* The search found the fact on 46 of 48 and the adapter answered 25. Of
   the 27 found-fact misses on `older` and `confirm`, 25 are one training sentence, "That's new to me. Tell me
   about it?". Sheet A marks that sentence coherent, 47 of 48 on `confirm`, because the fact is out of the
   shown turns. As R-020 reported, coherence cannot see this, and the recall count must be read beside it.
2. *The 13 "have i ever mentioned" misses are one fact type.* All 13 found-fact items of that wording are wrong,
   against 15 of 17 right for "did i say". Each fact type has one confirm wording, so wording and fact type
   cannot be separated here. Training has 4 rows with that opening. Cause not established.
3. *`older` at 58 messages did not gain*, 14 against 14. The gain on `older` is at 419; `confirm` gains at both.
4. *Adapter queries still carry training words on unseen questions*, such as "daughter age raffle" for a fear
   question. Some found the fact only because the relation word matched.
5. *`never_told`'s 24 and 23 keep R-020's limit.* The scorer passes invented facts outside the list. The sampled
   replies are unknown sentences, but that is a sample, not a measure.
6. *The judge's method.* The judge reported using a short script only to turn its own lists of 0-marked lines
   into the JSON files, so the marks rest on it having read every line. It took about 2 minutes for 672 lines.
   The same judge marked both models blind, so this bears on strictness more than on the comparison.
7. *The judge's notes.* It found these hard: replies naming a person it could not check, generic unknown
   sentences (marked 1), and replies asking for something already said (marked 0).
8. *One seed.* 24 per size is about plus or minus 10 points, and adapter 82 alone does not show the design holds.

**Decisions (Claude).**
- Train seeds 83 and 84 on the same data with the same settings, as R-020 says, and score each on the same
  probe seed. This shows whether the pass depends on the seed, which is the next thing to know.
- The held-out run does not follow automatically. It is one run, so limit 1 gets looked at first, with the three
  adapters' results beside it. Any change to training after this is disclosed and retrains all three.
- Context tokens per turn, listed in R-016 as reported beside the result, were not logged until `24a0fa3`.
  Base and adapter 82 rerun on probe seed 73157 to log them. Their replies must match the first run exactly,
  and any difference is reported.

## R-022 · 2026-11-01 · SPRINT · One training sentence replaced to test the false denials on `confirm`; rule before the run

Written at 21:40 while adapter seed 84 was training, before its result existed. Development only, probe pool.

**Finding.** On adapter 82, found-fact replies on `older` and `confirm` that open "That's" split into 13 "That's
great", all right, and 25 "That's new", all wrong. Only 2 other found-fact replies are wrong. Training has
"That's great" as a common opening of base's own answers and "That's new to me. Tell me about it?" as an unknown
sentence, so both share their first word. The likely cause on that seed is a collision at that word.

**Adapter 83, same data, same settings.** `probe2_tuned83_seed_73157.json`: +47.9 points at 58 messages and +52.1
at 419, right decisions 225 of 240, `older` read 42 of 44, `confirm` read 36 of 46, and "That's new" on 1 of the
misses. Its misses open "I don't" and "I searched". So the collision is specific to seed 82, and seeds differ by
about 20 points on recall. A one-seed comparison would be noise, so the comparison below uses all three seeds.

**Other results.** Reruns for token logging matched exactly: base 480 of 480 replies, adapter 82 240 of 240.
Tokens read per reply, adapter 82 against the whole chat: 1,203 against 1,113 at 58 messages, 1,199 against 5,409
at 419. Base on `tool_loop` reads 1,041 and 1,118, on 91 searches against the adapter's 145, so the adapter does
not read fewer tokens than base with the tool. It reads about 78% fewer than the whole chat at 419 messages.

**Disclosure.** While testing a cause that turned out wrong, Claude counted how many confirm wordings share a topic
word with their statement in each pool, and that count included `heldout` (0 of 5). No held-out item was run, and
nothing below uses that count. Later: the held-out pool's wording is less like the training wording than the probe's.

**Change.** In `TRAIN.unknown_replies` only, "That's new to me. Tell me about it?" becomes "Haven't heard about that.
Tell me about it?". Same build seed, 71119, so the training rows differ only where that sentence was drawn, and any
difference beyond that is reported. Three adapters, seeds 82, 83 and 84, in `adapters/v2_seed_*`, scored on probe
seed 73157 as `probe3_tuned*`. `results/recall_train/seed_8*.json` are overwritten; the old ones stay in git.

**Rule, fixed now, pooled over three seeds against the first three on the same probe conversations.** The new set
replaces the old one only if correct `older` plus `confirm` is not lower, `confirm` read rate is higher, and right
decisions stay at or above 200 of 240 on every seed. Then Sheet B runs on it, and it must hold at or above base.
Otherwise the old data and adapters stand. No held-out run comes out of this without Kevin.

## R-023 · 2026-11-02 · SPRINT · R-022's rule passes: the new training data replaces the old

Development only, probe pool, probe seed 73157. Counts from `scripts/records/rule_r022.py` and `gate_r022.py` on
the committed results files; Sheet B counts from `scripts/records/unblind.py` on `results/coherence/R-023/`.

**Rule, three seeds against three.** Correct `older` plus `confirm`, pooled over seeds 82, 83 and 84: old data
210 of 288, new data 234 of 288 (per seed old 59, 78, 73; new 76, 79, 79 of 96). Base is 30 of 96. `confirm`
read rate, found-fact items: old 99 of 139, new 120 of 138. Right decisions on the new data: 233, 229 and 230 of
240. All three parts of the rule hold, and every new adapter passes R-020's per-seed gate.

**Sheet B, each new adapter against base with no tool, `statement` and `in_view`.** One sheet per seed, 192 lines,
shuffle seeds 90422, 90423 and 90424, each marked by a fresh judge that saw only the rubric and its sheet.

| Seed | Base coherent | Adapter coherent | Only base | Only adapter |
|---|---|---|---|---|
| 82 | 81 of 96 | 87 of 96 | 7 | 13 |
| 83 | 83 of 96 | 84 of 96 | 8 | 9 |
| 84 | 81 of 96 | 86 of 96 | 8 | 13 |

Every adapter is at or above base, so the gate holds. The three sheets share base's replies; the three judges
gave the same mark to 86 of 89 base replies that appear on all three, so the judges agree with each other.
`statement` is a point or two lower than base on 82 and 83 and higher on 84; the gain is on `in_view`.

**Decision.** `adapters/v2_seed_82`, `v2_seed_83` and `v2_seed_84` replace `seed_82` to `seed_84` as the current
set. The old adapters stay on disc for comparison. No held-out run comes out of this without Kevin.

**Disclosure, run conditions.** Windows Update replaced the card driver (572.60 to 610.88) at 02:12. Seed 83 of
the new set trained on 610.88 in 16,337 s, against 4,485 to 7,513 s for every earlier run; scoring speed did not
change. Kevin rolled the driver back to 572.60 and rebooted; seed 84 was retrained from scratch after that. Seed
84 also slowed while other programs held card memory, because training peaks at 9.81 of 10 GiB. Speed does not
enter any result here.

**Where the new set still misses (for the next fixes).** Wrong replies by cause, seeds 82, 83, 84: `in_view`
answered without searching and wrong 10, 8 and 5; `older` searched without finding the fact 6, 4 and 6; `confirm`
fact found and not used 7, 7 and 4. In a first look at seed 84, several queries that miss change the relation word ("mentress",
"step sister").

## R-024 · 2026-11-02 · SPRINT · Screens are full runs; fix 1 (read in-view facts) points the right way, too small to call

Development only, probe pool, probe seed 51203 (48 items per kind, 240 rows, tool loop). Counts from
`scripts/records/screen_cmp.py` on the committed results files. Screens train on seed 82 and are compared with the
current adapter `v2_seed_82` scored on the same probe seed (`screen_full82`). Base differs a lot between probe
seeds (`older` 23 of 48 on 73157, 33 of 48 here), so screen numbers are compared only within probe seed 51203.

**Method change: a screen is a full run.** Two shorter references were tried first and neither stands in for the
full adapter, so each fix is screened with all rows and 3 epochs.

| Run | `older`+`confirm` | `in_view` | `never_told` | `statement` | Right decisions |
|---|---|---|---|---|---|
| Base | 38 of 96 | 32 | 46 | 25 | 109 of 240 |
| Half the rows, 1 epoch | 76 | 13 | 18 | 46 | 199 |
| Half the rows, 3 epochs | 57 | 31 | 38 | 45 | 221 |
| Full, `v2_seed_82` | 70 | 33 | 46 | 48 | 232 |
| Fix 1, `screens/read_hint_82` | 69 | 37 | 47 | 48 | 235 |

**Fix 1.** Kevin's decision: in-view questions are not searched; the adapter learns to read the fact from the turns
in view. The registered decision metric is unchanged. `run_build_training_set.py --read-hint`: when base answers
an `in_view` item wrong, base is asked again with the fact restated in the system prompt; if that reply passes the
same copy checks, the row keeps it without the hint. Of 39 such items on build seed 71119, 16 were kept and 20 were
still rejected. Data `data/screens/read_hint.jsonl`, 800 rows.

**Data differences, disclosed.** Against the current training set, fix 1 changes 16 `in_view` rows. Because the
build draws from one random stream, 77 `never_told` rows also have different conversations; their replies are
scripted and their form is unchanged.

**Result.** `in_view` correct 37 against 33 (+12% over the full adapter, +16% over base); on the same items fix 1
alone is right on 7 and the full adapter alone on 3, sign test p = 0.34. `older`+`confirm` 69 against 70 (8 and 9
discordant, p = 1.0). `in_view` answered without a search and wrong: 9 against 12. Right decisions 235 against 232.
Nothing is lost, and the gain is not distinguishable from noise on one seed. No coherence sheet for screens;
coherence is checked when a fix is confirmed on three seeds.

**Next: fix 1b, a larger dose.** `--hard-in-view 75` keeps 75 of the 150 `in_view` rows for items base got wrong
(read through the hint), against 16 in fix 1. Same build seed, same screen. If it beats the full adapter on
`in_view` without losing `older`+`confirm`, it is confirmed on seeds 82, 83 and 84 with Sheet B.

## R-025 · 2026-11-02 · SPRINT · Fix 1b (more hard in-view rows) beats the full adapter on the screen; confirmation rule registered

Development only, probe pool, probe seed 51203, same screen as R-024. Counts from `scripts/records/screen_cmp.py` on the
committed results files.

**Data.** `--read-hint --hard-in-view 75`, build seed 71119: 75 `in_view` rows base answered unaided and 75 from
items base got wrong, read through the hint (102 more were rejected by the copy checks; 719 easy items were
skipped once the easy share was full). Other kinds as in fix 1. `data/screens/hard_in_view.jsonl`, 800 rows.

| Run | `older`+`confirm` | `in_view` | `never_told` | `statement` | Right decisions |
|---|---|---|---|---|---|
| Base | 38 of 96 | 32 | 46 | 25 | 109 of 240 |
| Full, `v2_seed_82` | 70 | 33 | 46 | 48 | 232 |
| Fix 1, 16 hard rows | 69 | 37 | 47 | 48 | 235 |
| Fix 1b, 75 hard rows | 75 | 38 | 48 | 48 | 234 |

Against the full adapter on the same items: `in_view` fix 1b alone right on 7, full alone on 2 (p = 0.18);
`older`+`confirm` 10 and 5 (p = 0.30); the two together 17 and 7 (p = 0.064). Better on every kind, not yet
distinguishable from noise on one training seed.

**Run conditions.** Training took 10,770 s (8.97 s a step), against 4,485 to 7,513 s for earlier full runs on the
same settings; speed does not enter any result.

**Confirmation rule, registered before the runs.** Fix 1b trains on seeds 82 (the screen adapter), 83 and 84 and
is scored on probe seed 73157, compared with the current set `v2_seed_82` to `v2_seed_84` from R-023. Fix 1b
replaces v2 only if, pooled over the three seeds: correct `older` plus `confirm` is not lower than v2's 234 of 288;
correct `in_view` is higher than v2's 109 of 144 (34, 37, 38); and right decisions stay at or above 200 of 240 on
every seed. Then Sheet B runs on each new adapter and must hold at or above base, as in R-023. Otherwise v2 stands.
No held-out run comes out of this without Kevin.

## R-026 · 2026-11-03 · SPRINT · R-025's rule passes: fix 1b replaces v2 as the current set (v3)

Development only, probe pool, probe seed 73157. Counts from `scripts/records/rule_r025.py` and `gate_r022.py` on
the committed results files; Sheet B counts from `scripts/records/unblind.py` on `results/coherence/R-026/`.

**Rule, three seeds against three.** Correct `older` plus `confirm`, pooled over seeds 82, 83 and 84: v2 234 of
288, fix 1b 242 of 288 (per seed 80, 86, 76 of 96). Correct `in_view`: v2 109 of 144, fix 1b 120 of 144 (38, 42,
40). Right decisions 238, 230 and 230 of 240. Base is 30 of 96 and 34 of 48. All three parts hold, and every
adapter passes R-020's per-seed gate. `confirm` read rate, found-fact items: 122 of 141 (v2 120 of 138).

**Sheet B, each adapter against base with no tool, `statement` and `in_view`.** 192 lines a sheet, shuffle seeds
90425, 90426 and 90427, each marked by a fresh judge that saw only the rubric and its sheet.

| Seed | Base coherent | Adapter coherent | Only base | Only adapter |
|---|---|---|---|---|
| 82 | 79 of 96 | 88 of 96 | 4 | 13 |
| 83 | 79 of 96 | 87 of 96 | 8 | 16 |
| 84 | 79 of 96 | 89 of 96 | 5 | 15 |

Every adapter is above base, so the gate holds. `statement` is equal to base or one higher on every seed; the gain
is on `in_view` (42, 43 and 43 of 48 against base 34, 35 and 34).

**Decision.** The fix 1b adapters, copied to `adapters/v3_seed_82` to `v3_seed_84`, replace v2 as the current set;
training data `data/screens/hard_in_view.jsonl`. v2 stays on disc for comparison. No held-out run comes out of this
without Kevin.

**Disclosure, run conditions.** Seed 84's first run slowed at step 545 from about 7 s to 300 to 650 s a step when
it spilled out of card memory (training peaks at 9.8 of 10 GiB), and was stopped and retrained from scratch at
02:08 (6,807 s). A stall watcher now runs beside every training run. Speed does not enter any result.

**Where v3 still misses (for the next fixes).** Wrong replies by cause, seeds 82, 83, 84: fact found and not used
(`older` plus `confirm`) 10, 4 and 14, mostly a "not told" reply; `in_view` answered without a search and wrong 10,
5 and 6; searched without finding the fact 6, 2 and 4. Next screen, fix 3: the same data with 100 `never_told`
rows instead of 150, to weaken the lean towards "not told".

## R-027 · 2026-11-03 · SPRINT · Sheet A on v3: above base overall, below base on `confirm`

Development only, probe seed 73157, v3 seed 82 against base, both on `tool_loop`, every kind. 480 lines, shuffle
seed 90428, marked by a fresh judge that saw only the rubric and its sheet (asked afterwards, it confirmed it
judged every line itself; code only wrote its list of zeros to the file). Counts from `scripts/records/unblind.py`
on `results/coherence/R-027/`.

**Overall.** Adapter coherent 203 of 240, base 169 of 240 (+20% over base). Only adapter coherent 58, only base 24.

| Kind | Base coherent | Adapter coherent |
|---|---|---|
| `older` | 32 of 48 | 39 |
| `confirm` | 47 | 35 |
| `in_view` | 32 | 39 |
| `never_told` | 29 | 45 |
| `statement` | 29 | 45 |

**`confirm` is below base, 35 against 47 (-26%).** This breaks "coherence cannot decrease" for one kind under the
tool loop, and the overall gain does not cancel it. The adapter's incoherent `confirm` replies open with a stock
phrase that does not fit ("That's great to hear!", "That's a relief."), speak as the friend ("Farah is my
stepsister"), or mix up who is who. The training targets carry the same openers: base's own answers to found
facts are kept when they contain the answer, and nothing checks their coherence (`confirm` targets: "That's great
news!" 9, "That's great to" 4, "Thanks for the update" and similar).

**Next: fix 5, coherent targets.** A fresh judge marks base's found-fact answers in the v3 training data with the
same rubric, blind; answers marked incoherent fall back to the scripted answer, as answers that fail the scorer
already do. The fix 5 screen then gets a Sheet A on `older` and `confirm` against the v3 screen adapter.

## R-028 · 2026-11-03 · SPRINT · Fix 3 (fewer `never_told` rows) is worse than v3 on the screen: dropped

Development only, screen probe seed 51203, adapter seed 82, 240 items. Counts from `scripts/records/screen_cmp.py`.
Fix 3 is v3's build (`--read-hint
--hard-in-view 75`) with `--never-told-rows 100` in place of 150 (750 rows). It targets v3's misses where the
search found the fact and the reply still said it was never told.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) |
|---|---|---|---|---|---|---|---|
| base | 38 | 33 | 5 | 32 | 46 | 25 | 109 |
| v3 (`screen_hard_in_view82`) | 75 | 37 | 38 | 38 | 48 | 48 | 234 |
| fix 3 (`screen_few_never_told82`) | 73 | 38 | 35 | 37 | 44 | 47 | 228 |

Fix 3 is below v3 on recall (73 against 75), `never_told` (44 against 48) and decisions (228 against 234), and
above it on nothing but `older` by one. Fewer `never_told` rows did not cut the false denials and cost correct
refusals. Dropped; v3 stays the current set. Next on the card: fix 5, then fix 4.

## R-029 · 2026-11-03 · SPRINT · Fix 5 and fix 4 data built; training slowed by card memory, a lean loss fixes it; records moved out of scratch

**Fix 5 targets, judged blind.** `scripts/run_target_coherence.py` puts every `older` and `confirm` row of the
v3 data whose search found the fact and whose last turn is base's own answer (350 rows) on one sheet, shuffle
seed 5. A fresh judge marked it with the R-020 rubric alone; 79 marked incoherent (`older` 52, `confirm` 27),
listed in `data/screens/fix5_rejected.json`. Sheet, key, rubric and marks: `results/coherence/R-029_fix5_targets/`.
The fix 5 build (`--reject-replies`) gives those rows the scripted answer: `older` base answers 90 and scripted
110, `confirm` 67 and 83. **Caveat:** the judge also marked down some answers for using a detail not in the
shown turns, which the rubric allows, so a few coherent answers were probably replaced. The scripted answer they
get is coherent, so the cost is a little less of base's own wording, not incoherent targets.

**Fix 4 data.** `--second-search 0.33`: rows that make an empty search in the message's own words before the
real one, `older` 65, `confirm` 43, `never_told` 53; 2, 14 and 3 more were drawn and left at one search because
the longer row passed 1,024 tokens. The build ran 09:26 to 10:15 beside the memory checks below, because
stopping the queue's background task did not stop its child script; its training then refused to start on the
uncommitted loss change, so no adapter came from it.

**Training slowed by card memory.** Fix 3 trained at 11.7 s a step (13,152 s for 1,125 steps) against 5.7 s for
v3 seeds 83 and 84. The first fix 5 run ran at about 22 s a step with 1.4 GiB in shared memory: training needed
9.8 of the card's 10 GiB and Firefox held about 1 GiB. It was stopped at step 103 of 1,200; nothing from it is
used. The stall watcher's 60 s limit missed a steady slowdown; it now trips at 12 s a step after step 20.

**Cause and fix.** The model's weights are 6.27 GiB. TRL's chunked loss computes `h.float() @ w.float().t()`
for every chunk of tokens; under bf16 autocast both float32 copies are cast back to bf16 before the product, so
the copies (2 GiB float32 plus 1 GiB bf16 of the 262,144 x 2,048 output layer) change nothing but memory. Peak
was 9.56 GiB at 256 tokens a row and 9.65 at 512, so it did not depend on row length. `lean_loss.lean_chunk`
takes the bf16 product directly when the tensors already have autocast's dtype and is TRL's code otherwise;
`tests/test_lean_loss.py` shows loss, scores and gradients equal to TRL's bit for bit, with and without
autocast. Loss chunks drop from 256 to 128 tokens. Peak on the longest rows falls from 9.81 to 7.12 GiB.

**Disclosure: training is not bit-reproducible on this card.** On the same rows and seed, TRL's own loss gave
first-step gradient norms 3.86, 3.42 and 3.63 in three runs (first-step loss 2.963 every time); the lean loss
gave 3.45, 3.65 and 3.56. Seeds fix data order and starting weights, not the exact result. Fix 5 and fix 4 train
with the lean loss while the v3 screen they are compared with trained with TRL's; the difference sits inside
this run-to-run spread. If either fix wins by a small margin, the v3 screen is retrained with the lean loss
before it is called.

**Records moved out of the scratchpad.** Every coherence sheet, key and judge's marks behind R-020 to R-027 now
sits under `results/coherence/R-0xx/`, and the counting scripts the records cite under `scripts/records/`
(`screen_cmp.py`, `rule_r022.py`, `gate_r022.py`, `rule_r025.py`, `unblind.py`). The scripts were reformatted
for lint only; on the committed results they print what the scratch copies printed, and `unblind.py` gives every
coherence count in R-020 to R-027 from the moved files.

## R-030 · 2026-11-03 · SPRINT · AuditKIT joins the evaluation: a second scorer and a second significance test, registered before use

The hackathon asks for at least two Lexsi toolkits chained. Training runs through AgentTune; until now
AuditKIT only read a smoke run's trajectories (R-007). From here every scored results file can be scored
again by AuditKIT's agent evaluation (`aya_retrieval.audit`, `scripts/run_audit.py`), written before any
full run of it was read.

**How.** Each results row becomes an AuditKIT episode: the friend's message, one `search_corpus` call per
query the model made, and its final reply. Search results were not kept, so AuditKIT marks them
unavailable. Each item is rebuilt from its seed and checked against the row before scoring. The outcome
of each case is an AuditKIT oracle:
- `older`, `confirm`, `in_view`: AuditKIT's `AnswerAssertion` in `contains` mode, which matches the planted
  answer on word boundaries. Our scorer (R-016) matches any substring and also fails a reply that names a
  wrong value, so the two can disagree; every disagreement is listed with its reply.
- `never_told`: a `CustomPredicate` (version 1) that the reply names no value of that kind, our own rule
  run inside AuditKIT.
- `statement`: a `CustomPredicate` (version 1) that the episode holds no tool call.
Diagnostics: AuditKIT's `tool_call_validity` and `redundant_tool_calls`. Base and each adapter are compared
with AuditKIT's paired bootstrap (10,000 resamples, seed 0), on every case and on `older` plus `confirm`.

**Rule.** This is a second scorer and a second test, reported beside R-016's and never in place of them.
R-016's recall rule, sign test and coherence gate still decide the project. On the held-out run AuditKIT
runs on the same results files after R-016's numbers are computed, and its numbers are reported whatever
they show, with the disagreements counted.

## R-031 · 2026-11-03 · SPRINT · AuditKIT's paired bootstrap is defective; R-030 uses a sign test and a centred bootstrap instead; AuditKIT on v3

**Defect.** AuditKIT 1.1.3's `_bootstrap.paired_bootstrap`, which `compare_models`, `Experiment.significance`
and `ComparisonResult.significance` share, resamples the paired differences and counts resampled means at
least as large as the observed one, without centring them under no difference. Every resampled mean then
sits around the observed mean, so p is about 0.5 for any real effect and 1.0 when every pair improves:

| Pairs | AuditKIT's p |
|---|---|
| 100 of 100 improve | 1.0 |
| 50 improve, 50 the same | 0.53 |
| none change | 1.0 |

The first full AuditKIT run on v3 read p = 0.52 for 57% to 88% over 240 paired cases, which is how this was
found. Upstream `main` was still 1.1.3 (`71316da`) when checked. The write-up for Lexsi is in
`docs/auditkit_bootstrap_defect.md`; Kevin reports it in the submission, not publicly. `tests/test_stats.py` pins the defect, so a
fix upstream fails that test and this note gets updated.

**Change to R-030, before any held-out use.** AuditKIT's bootstrap is dropped. The AuditKIT link compares
base and adapter with the exact sign test R-016 registered and a paired bootstrap centred under no
difference (`aya_retrieval.stats`, 10,000 resamples, seed 0; tests check both on known cases). AuditKIT's
scoring is unchanged and still decides each case.

**AuditKIT on v3, development, probe seed 73157** (`results/audit/v3_probe73157.json`). Verified successes:
base 137 of 240; adapters 212, 220 and 211 (seeds 82, 83, 84). AuditKIT's verdict agrees with our scorer on
959 of 960 cases. The one disagreement is seed 82's `419_in_view_03`: the answer is "thistle" and the reply
says "Thistles"; our substring scorer passes it and AuditKIT's whole-word match does not.

| Seed | Only base right | Only adapter right | Sign test p | `older` + `confirm`: only base, only adapter |
|---|---|---|---|---|
| 82 | 10 | 85 | 6e-16 | 4, 54 |
| 83 | 8 | 91 | 6e-19 | 3, 59 |
| 84 | 10 | 84 | 1e-15 | 7, 53 |

The centred bootstrap gives p at its floor (1 in 10,001) for every adapter, on every case and on the recall
kinds. AuditKIT's diagnostics: every recorded search call is valid for base and adapters; base repeats a
call in some turns (redundant-call score summed 1.3 over 83 turns that searched), the adapters never do.

## R-032 · 2026-11-03 · SPRINT · Lean loss leaves v3 unchanged; fix 4 dropped; fix 5 ties on recall and does not restore `confirm` coherence; fix 5b next

Development only, screen probe seed 51203, adapter seed 82, 240 items. Counts from `scripts/records/screen_cmp.py`;
sign tests on correct answers from `aya_retrieval.stats`. Every run here trains with the lean loss (R-029), about
1,300 s a run at 7.1 to 7.2 GiB peak.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) |
|---|---|---|---|---|---|---|---|
| base | 38 | 33 | 5 | 32 | 46 | 25 | 109 |
| v3, TRL loss (`screen_hard_in_view82`) | 75 | 37 | 38 | 38 | 48 | 48 | 234 |
| v3, lean loss (`screen_hard_in_view_lean82`) | 74 | 36 | 38 | 37 | 47 | 48 | 233 |
| fix 5 (`screen_coherent_targets_82`) | 76 | 36 | 40 | 41 | 47 | 48 | 233 |
| fix 4 (`screen_second_search_82`) | 62 | 29 | 33 | 37 | 48 | 48 | 233 |

**Lean loss.** v3 retrained on the same data with the lean loss differs from the TRL-loss run on 13 of 240 items
(5 and 8 each way, p = 0.58): the loss change leaves results where run-to-run variation puts them. Fixes below are
compared with the lean-loss v3.

**Fix 4 dropped.** Correct answers: v3 alone right on 22 items, fix 4 alone on 11 (p = 0.080); recall 62 against 74.
Teaching an empty first search made the model worse at answering.

**Fix 5: recall ties, coherence does not recover.** Correct answers 8 and 14 each way (p = 0.29). Sheet A on
`older` and `confirm`, fix 5 against base on probe seed 51203: 192 lines, shuffle seed 90429, a fresh judge with only
the rubric and its sheet (it judged every line by reading it and typed its 44 zero lines into a short script to write
the file). Files in `results/coherence/R-032/`. Base coherent 79 of 96, fix 5 69 (only base 18, only fix 5 8).
`older` 32 against 34, **`confirm` 47 against 35**, the same gap R-027 found for v3 on probe seed 73157. Fix 5's
incoherent `confirm` replies open with a news reaction ("That's great news!", "That's great to hear!", "That's a
change") to a question, or name the wrong person. The training targets still carry those openers: 14 of 150
`confirm` answers in fix 5's data, as in v3's, because R-029's judge marked them coherent there. Judging the
targets was the wrong filter. Fix 5 is not adopted.

**Next: fix 5b.** `--scripted-answers confirm`: every `confirm` row whose search found the fact gets the short
scripted answer ("Your cousin Ivan's dog is called Waffles.") in place of base's own answer. One change from v3,
same build seed, same screen, then Sheet A on `older` and `confirm` against base with a fresh judge. It is adopted
for confirmation on three seeds only if recall does not fall and `confirm` coherence reaches base's.

## R-033 · 2026-11-03 · SPRINT · Fix 5b (scripted `confirm` answers) ties v3 on the screen; confirmation rule registered before its runs and marks

Development only, screen probe seed 51203, adapter seed 82, lean loss. `--scripted-answers confirm`, build seed 71119:
all 150 `confirm` rows whose search found the fact get the scripted answer (base answers 0, against 94 in v3's
data); other kinds as v3. `data/screens/scripted_confirm.jsonl`, 800 rows.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) |
|---|---|---|---|---|---|---|---|
| base | 38 | 33 | 5 | 32 | 46 | 25 | 109 |
| v3, lean loss | 74 | 36 | 38 | 37 | 47 | 48 | 233 |
| fix 5b (`screen_scripted_confirm_82`) | 71 | 33 | 38 | 37 | 48 | 48 | 232 |

Against v3 on correct answers: 14 items v3 alone, 12 fix 5b alone (p = 0.85). The stock news openers are gone from
fix 5b's `confirm` replies; its most common openings are "I don't have" (5) and a name followed by the fact. Sheet A
on `older` and `confirm` against base (192 lines, shuffle seed 90430, `results/coherence/R-033/`) went to a fresh
judge before this rule was written; its marks are not read yet.

**Confirmation rule, written before seeds 83 and 84 exist and before any fix 5b coherence mark is read.** Fix 5b
trains on seeds 82 (the screen adapter), 83 and 84 and is scored on probe seed 73157 as `probe5_tuned8x`, against v3
(`probe4_tuned8x`, R-026). It replaces v3 only if all of these hold:
1. correct `older` plus `confirm`, pooled, at least 230 of 288 (v3: 242);
2. correct `in_view`, pooled, at least 114 of 144 (v3: 120);
3. right decisions at least 200 of 240 on every seed;
4. Sheet A on `older` and `confirm`, each seed against base on probe seed 73157, each sheet to a fresh judge:
   pooled over the three sheets, `confirm` coherent at or above base's count, and `older` plus `confirm` coherent at
   or above base's count.
Items 1 and 2 allow 5% below v3 (12 and 6 items). This is a judgment made now, not a measured noise band: fix 5b
gives up base's wording on `confirm` to remove the incoherent openers, the screen shows a 3-item drop that the sign
test cannot tell from noise, and Kevin's hard rule is that coherence cannot decrease. Otherwise v3 stands. Sheet B
runs on the result before it is final. No held-out run comes out of this without Kevin.

## R-034 · 2026-11-03 · SPRINT · R-033's rule fails on coherence: v3 stands; fix 5b is better than v3 on `confirm` coherence but still below base

**Screen sheet (R-033), unblinded after the rule was written.** Fix 5b against base, probe seed 51203: base 79 of 96,
fix 5b 80 (only base 9, only fix 5b 10); `older` 32 against 36, `confirm` 47 against 44. Fix 5 on the same items
(R-032) had `confirm` 35.

**Confirmation runs, probe seed 73157** (`probe5_tuned8x`; seeds 83 and 84 trained with the lean loss, seed 82 is
the screen adapter).

| Rule item | Needed | Fix 5b | Holds |
|---|---|---|---|
| 1. `older` + `confirm` correct, pooled | at least 230 of 288 | 232 (67, 87, 78); v3 242 (80, 86, 76) | yes |
| 2. `in_view` correct, pooled | at least 114 of 144 | 122; v3 120 | yes |
| 3. Right decisions, each seed | at least 200 of 240 | 235, 236, 227 | yes |
| 4a. `confirm` coherent, pooled over three sheets | at least base's 141 of 144 | 121 (42, 37, 42) | **no** |
| 4b. `older` + `confirm` coherent, pooled | at least base's 241 of 288 | 236 (80, 77, 79) | **no** |

Sheets: `older` and `confirm`, base against each seed, 192 lines each, shuffle seeds 90431 to 90433, three fresh
judges with only the rubric and one sheet each; marks written to the scratchpad and copied in, files in
`results/coherence/R-034/`. Each judge reported judging every line itself; two typed their own zero lines into a
short script to write the file. The seed 82 judge saw that the folder already held the seed 83 marks and did not
open them. Per seed, base against fix 5b: 81 against 80, 79 against 77, 81 against 79; `older` 34/38, 32/40, 34/37
and `confirm` 47/42, 47/37, 47/42.

**Decision, by the rule: v3 stands.** Fix 5b is not adopted. For the record, it removes most of v3's `confirm`
loss: v3 seed 82 had `confirm` 35 of 48 against base 47 on R-027's sheet (every kind, a different judge); fix 5b
seed 82 has 42 against 47. It is still below base, and the rule asks for base.

**What is left.** 23 incoherent fix 5b `confirm` replies over the three sheets. 15 copy the friend's own wording of
the relation, "Esme, who is my tutor, speaks fluent Turkish" or "Kofi is my classmate", or name the wrong person;
the rest are a news opener (2), an unrelated follow-up question after "I don't have that from you" (2) and other
off-topic replies. The scripted answers fix 5b trains on do not show the change from the friend's "my tutor" to
"your tutor": 20 of the train pool's 25 answer templates drop the relation ("{person} speaks fluent {value}."),
so a reply that names the relation can only copy the friend's "my" from the found passage.

**Next: fix 5c.** Fix 5b's data with the train pool's answer templates rewritten to name the relation from the
friend's side ("Your {relation} {person} speaks fluent {value}."). Only the train pool changes; the probe and
held-out pools' answer templates are never used as targets. The template is plain formatting, so every
conversation and draw is unchanged. Same screen, then Sheet A on `older` and `confirm` against base.

## R-035 · 2026-11-03 · SPRINT · Fix 5c (answers name the relation) on the screen; confirmation rule registered before its runs and marks

Development only, screen probe seed 51203, adapter seed 82, lean loss. Fix 5b's build (`--read-hint --hard-in-view
75 --scripted-answers confirm`, build seed 71119) with the train pool's answer templates naming the relation (R-034).
`data/screens/relation_answers.jsonl`, 800 rows.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) |
|---|---|---|---|---|---|---|---|
| base | 38 | 33 | 5 | 32 | 46 | 25 | 109 |
| v3, lean loss | 74 | 36 | 38 | 37 | 47 | 48 | 233 |
| fix 5b | 71 | 33 | 38 | 37 | 48 | 48 | 232 |
| fix 5c (`screen_relation_answers_82`) | 76 | 34 | 42 | 37 | 48 | 48 | 232 |

Against v3 on correct answers: 12 items v3 alone, 15 fix 5c alone (p = 0.70). Replies to `older` and `confirm` that
give the friend's relation as the model's own ("who is my tutor", "is my classmate"): fix 5b 7 of 96, fix 5c 0.

**Confirmation rule, written before seeds 83 and 84 exist and before any fix 5c coherence mark is read.** The same
as R-033's, for fix 5c: seeds 82 (the screen adapter), 83 and 84, scored on probe seed 73157 as `probe6_tuned8x`,
against v3. Fix 5c replaces v3 only if: (1) correct `older` plus `confirm`, pooled, at least 230 of 288; (2) correct
`in_view`, pooled, at least 114 of 144; (3) right decisions at least 200 of 240 on every seed; (4) Sheet A on `older`
and `confirm`, each seed against base on probe seed 73157, each to a fresh judge: pooled `confirm` coherent at or
above base's count, and pooled `older` plus `confirm` coherent at or above base's count. The screen's Sheet A
(against base, probe seed 51203) is reported but does not decide. Otherwise v3 stands. Sheet B runs on the result
before it is final. No held-out run comes out of this without Kevin.

## R-036 · 2026-11-03 · SPRINT · R-035's rule passes: fix 5c replaces v3 as the current set (v4)

**Screen sheet (R-035), unblinded after the rule was written.** Fix 5c against base, probe seed 51203, shuffle seed
90434: base 80 of 96, fix 5c 90 (only base 2, only fix 5c 12); `older` 33 against 43, `confirm` 47 against 47.

**Confirmation runs, probe seed 73157** (`probe6_tuned8x`; seed 82 is the screen adapter, 83 and 84 trained with the
lean loss).

| Rule item | Needed | Fix 5c | Holds |
|---|---|---|---|
| 1. `older` + `confirm` correct, pooled | at least 230 of 288 | 252 (84, 87, 81); v3 242 | yes |
| 2. `in_view` correct, pooled | at least 114 of 144 | 115; v3 120 | yes |
| 3. Right decisions, each seed | at least 200 of 240 | 236, 229, 226 | yes |
| 4a. `confirm` coherent, pooled | at least base's 141 of 144 | 142 (48, 47, 47) | yes |
| 4b. `older` + `confirm` coherent, pooled | at least base's 240 of 288 | 260 (88, 89, 83) | yes |

Sheets in `results/coherence/R-036/`: shuffle seeds 90435 to 90437, three fresh judges, one sheet each, marks written
to the scratchpad and copied in. Each judge reported judging every line itself; three turned their own zero lines
into the file with a short script or loop. Base on these sheets: `older` 33 and `confirm` 47 on each seed.

**Sheet B, before final** (`results/coherence/R-036B/`, shuffle seeds 90438 to 90440, base with no tool against fix
5c on `statement` and `in_view`, built as R-026's: all 96 base lines come from base's `three_exchanges` replies).
Base against fix 5c: 77 against 91, 80 against 81, 78 against 83. Per kind, `statement` 44/48, 44/44, 45/46 and
`in_view` 33/43, 36/37, 33/37. At or above base on every seed and kind. (v3's Sheet B in R-026: 79 against 88, 87,
89.)

**AuditKIT** (`results/audit/fix5c_probe73157.json`): verified successes base 137 of 240, fix 5c 218, 218, 214.
Agreement with our scorer 957 of 960. Sign test, every case: only base right 7, 10, 11 against only adapter 88, 91,
88, p from 6e-19 to 5e-16; `older` + `confirm`: 4/58, 3/60, 6/57, p from 3e-13 to 2e-11.

**Decision, by the rule: fix 5c is v4.** `adapters/v4_seed_82` to `v4_seed_84` (copies of
`screens/relation_answers_8x`, checked byte for byte), data `data/screens/relation_answers.jsonl`, train pool
templates as of commit `bc5f6d8`. Against v3, pooled on probe seed 73157: recall 252 against 242, `confirm` correct
133 against 122, `in_view` 115 against 120, and `confirm` coherence at base instead of below it. `in_view` is the one
measure that falls, inside R-035's allowance. Not yet measured on v4: Sheet A on `in_view`, `never_told` and
`statement` with the tool; the held-out run's full sheet covers every kind. No held-out run without Kevin.

## R-037 · 2026-11-03 · SPRINT · v4 is a checkpoint: its misses ranked, and the next screens

Kevin: "lets push this until gains become insubstantial". v4's wrong answers and wrong decisions on probe seed
73157, three seeds pooled, 79 in all, by cause:

| Kind | Cause | 58 msgs | 419 msgs |
|---|---|---|---|
| `in_view` | no search, wrong answer | 15 | 9 |
| `older` | no search | 10 | 3 |
| `never_told` | no search (right refusal, wrong decision) | 5 | 4 |
| `older` | searched, fact not found | 4 | 4 |
| `older` / `confirm` | fact found, not used | 4 / 4 | 1 / 2 |
| `confirm` | searched, fact not found | 2 | 3 |
| `in_view` | searched, wrong | 3 | 2 |
| `never_told` | named a value | 1 | 2 |
| `statement` | searched | 1 | 0 |

Most of the first two rows are indirect questions: "drawing a blank on my classmate's tattoo", "i cannot think what
my godfather grows", "i'm blanking on what my mentor is scared of". v4 reads them as the friend's mood ("It sounds
like you're having a bit of a brainfog") and neither searches nor reads the fact in view. The train pool has one
indirect phrasing per fact type, 25 in all, each used for a third of that type's questions.

**Screens queued, each against v4's screen adapter (`screen_relation_answers_82`) on probe seed 51203:**
1. 4 epochs instead of 3, v4 data (`screen_epochs4_82`).
2. Learning rate 1e-4 instead of 2e-4, v4 data (`screen_lr1e4_82`).
3. Fix 6, `--more-indirect`: v4's build plus three more indirect phrasings per train fact type
   (`train_phrasings.py`, 75 in all), written by Claude for this fix, mostly statements about forgetting. None uses
   an idiom from the probe pool ("drawing a blank", "blanking", "tip of my tongue", "cannot think"), which Claude had
   read in the loss list above; a test enforces it, so the probe still measures phrasings the model has not seen. The
   held-out pool's phrasings were not read. Drawn from a separate generator, so only the question changes.
A screen that gains goes to three seeds under a rule written before those runs, as R-033 and R-035 did.

## R-038 · 2026-11-03 · SPRINT · ★ Amendment to R-016, made before any held-out run: the registered test gets harder (crowded results, false retrieval)

**What changes.** R-016's held-out test stays exactly as registered, and two requirements are added to it. Nothing in
R-016 is loosened or dropped.

1. **A crowded condition.** Every held-out conversation is also run with four decoys (`run_recall_eval.py --pool
   heldout --final --decoys 4`): four more facts of the same type about other people, so a search for the asked fact
   comes back with several same-type facts and only one is the friend's. Base and each adapter run on identical
   conversations in both conditions, 300 conversations each (30 per kind at each of 58 and 419 messages), once.
2. **False retrieval as a gated measure.** A reply that names a wrong value of the asked fact's type, whether a decoy
   about someone else or, for a question never told, any value of that type, is a false retrieval
   (`report_data.false_retrieval`). In each condition, each adapter's false retrievals must be no more than base's
   on the same conversations.
3. **R-016's rules apply in both conditions.** The recall rule (at least 20 points above base at each message size,
   pooled over the three adapters, and the paired exact sign test below p = 0.01) and the hard coherence gate (each
   adapter's coherent count at or above base's on the same conversations, blind judge, rubric only) must hold with one
   decoy and with four. **The project passes only if every rule holds in both conditions.** Each condition's results
   are reported in full whether it passes or fails, with false retrieval per kind beside them.

**Why it is added now.** On 2026-11-03 Kevin asked whether the project accounts for false retrieval. Checking showed
that it does in the scorer, which fails a reply naming a wrong value, but that the registered test does not press on
it: every test conversation holds one decoy, while training shows 0 to 3, so the test never asks whether the model
picks the right person out of several same-type facts. Kevin: "we're just making the registered test harder ... we
want our answers to be toight." The amendment can only make the project's claims harder to earn.

**Why now is still clean.**
- No held-out conversation has been built, run or scored. No results file exists for the `heldout` pool.
- What Claude has seen of the held-out pool: a count of wording overlap with its statements (R-022, disclosed there);
  its five answer templates, which appeared in a search output on 2026-11-03 while Claude counted train answer
  templates; and its counts of values per fact type (at least 5), people (10) and relations (8), read to find how many
  decoys it supports. No held-out question, conversation or value list was read.
- The decoy count is fixed now, before any four-decoy result exists on any pool: four is the most the held-out pool
  supports (at least five values per type, one of them the answer) and more than training ever shows (three).

**Development.** The same four-decoy run on the probe pool (base and v4, probe seed 73157) shows where the current
adapter stands. It is development only and decides nothing. If training is later changed in response to it, the probe's
four-decoy numbers stop being a clean measure, and the held-out run is the only clean read; any such change is recorded
as one.

## R-039 · 2026-11-03 · SPRINT · ★ Amendment to R-016 and R-038, before any final run: an independent, harder test pool

**Why.** Kevin asked who wrote the held-out pool. Claude did, on 2026-11-01 (commit `c662adf`, R-015), in the same
session as the training pool. A test keeps the pools free of shared content, but not of shared style, and Claude also
wrote today's training phrasings (fix 6). A test written by the same author as the training data is easier than an
independent one. Kevin chose a pool written by a fresh agent, and asked for it to be harder.

**How it was written.** A fresh agent with no project context received only `docs/independent_pool/BRIEF.md` (written
by Claude: the five kinds, the pool format, rules for hard material, and two example words, "landlady" and "the bus
stop"), an avoid-list built by code from the other pools (`avoid.json`: their people, relations, values, subjects,
fact-type names, acknowledgements and unknown replies) and a checker (`check_pool.py`). It was told to open nothing
else, and reported that it did not. It ran the checker until it passed; the first version passed the checker but
failed the repository's own tests on fact-type names and reply variety, which the checker did not yet cover, and the
agent fixed both after the checker was extended. Its replies to Claude carried only counts: 12 people, 10 relations,
6 fact types with 6 values each, 35 subjects, 3 moods (5 lines, 12 replies each), 18 acknowledgements, 12 statement
pairs, 4 unknown replies. The brief asked for hard material: run-on statements with the fact buried mid-sentence,
texting-style questions, `new_words` without the type's keyword, forgetting phrased without the probe's idioms, and
values within a type that are easy to confuse.

**Sealed.** `src/aya_retrieval/pool_independent.py` (sha256 begins `f65ea72e1d91276f`), registered as pool
`independent`, readable only with `--final` like `heldout`. Claude has not read it: every check ran by code and
printed only pass or fail, test failures were listed by name only, and the scratch copy was deleted. Tests confirm it
shares no people, relations, values, subjects, fact types, acknowledgements or unknown replies with any other pool and
no fact or question wording with the training pool.

**The final test, as amended.** Four conditions, each run once, base and the three adapters on identical
conversations, 300 conversations per condition (30 per kind at each of 58 and 419 messages):

| Condition | Pool | Decoys a chat |
|---|---|---|
| A (R-016 as registered) | `heldout` | 1 |
| B (R-038) | `heldout` | 4 |
| C (this record) | `independent` | 1 |
| D (this record) | `independent` | 4 |

R-016's recall rule and sign test, R-038's false-retrieval rule, and the coherence gate must hold in every condition;
the project passes only if all four do, and every condition is reported in full either way. Coherence: condition A
is judged in full as R-016 registered (every conversation, base and adapter). In B, C and D each adapter is judged
on a fixed sample of 120 conversations (12 per kind at each length, drawn with seed 39 before any run) against base on
the same conversations, one fresh judge per sheet, to keep judging within reach; the gate is the same, each adapter's
coherent count at or above base's on its sample.

## R-040 · 2026-11-03 · SPRINT · Screens on v4: 4 epochs a candidate, learning rate 1e-4 dropped, fix 6 gains on recall; confirmation rule registered

Development only, screen probe seed 51203, adapter seed 82, lean loss, against v4's screen adapter
(`screen_relation_answers_82`). Counts from `scripts/records/screen_cmp.py`; sign tests from `aya_retrieval.stats`.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) |
|---|---|---|---|---|---|---|---|
| base | 38 | 33 | 5 | 32 | 46 | 25 | 109 |
| v4 (`screen_relation_answers_82`) | 76 | 34 | 42 | 37 | 48 | 48 | 232 |
| 4 epochs (`screen_epochs4_82`) | 78 | 36 | 42 | 39 | 48 | 48 | 231 |
| learning rate 1e-4 (`screen_lr1e4_82`) | 67 | 30 | 37 | 35 | 35 | 48 | 228 |
| fix 6 (`screen_more_indirect_82`) | 84 | 41 | 43 | 36 | 48 | 47 | 235 |

- **4 epochs**: correct answers 3 v4 alone, 7 alone (p = 0.34). A candidate, not confirmed.
- **Learning rate 1e-4**: 33 v4 alone, 9 alone (p < 0.01); `never_told` falls from 48 to 35. Dropped. A screen at 3e-4
  is queued.
- **Fix 6** (`--more-indirect`, R-037; data `data/screens/more_indirect.jsonl`, 800 rows): on `older` plus `confirm`,
  2 items v4 alone right and 10 fix 6 alone (p = 0.039); over all kinds 10 and 16 (p = 0.33). On the 38 `older` and
  `in_view` items asked with a forgetting phrase, v4 24 right and fix 6 28. `in_view` does not move (36 against 37).

**Confirmation rule for fix 6, written before seeds 83 and 84 exist and before any fix 6 coherence sheet.** Fix 6 is
meant to raise recall, so it must beat v4, not only stay near it. Seeds 82 (the screen adapter), 83 and 84, scored on
probe seed 73157 as `probe7_tuned8x`, against v4 (`probe6_tuned8x`, R-036). Fix 6 replaces v4 only if: (1) correct
`older` plus `confirm`, pooled, is higher than v4's 252 of 288; (2) correct `in_view`, pooled, at least 110 of 144
(v4 115, 5% below); (3) right decisions at least 200 of 240 on every seed; (4) Sheet A on `older` and `confirm`, each
seed against base on probe seed 73157, a fresh judge per sheet: pooled `confirm` coherent at or above base's count, and
pooled `older` plus `confirm` coherent at or above base's count. Then Sheet B before it is final. Otherwise v4 stands.

## R-041 · 2026-11-03 · SPRINT · ★ Amendment to R-016, R-038 and R-039, before any final run: recall counted by source; the recall rule must also hold on retrieved answers alone

**Why.** Kevin: "are the additional correct recalls genuinely recovered information, or are they better guesses? Those
need separate accounting." A right answer on `older` or `confirm` can come from reading the fact or from guessing
among the six or so plausible values of its type.

**The split** (`report_data.recall_sources`, tested). Each answer to a question that needs a search is
**retrieved** if the exchange holding the fact was among the top five results of a search the model itself made
(`found_fact`, `recall_tool.search_finds_fact`), and otherwise a guess, either after a search that did not return it
or with no search. Answers that were wrong although the fact came back are counted too.

| Probe seed 73157, `older` + `confirm` | Base (96) | v4, three seeds (288) |
|---|---|---|
| Right, fact retrieved | 30 | 251 |
| Right, searched but not returned | 0 | 0 |
| Right, no search | 0 | 1 |
| Wrong although retrieved | 4 | 11 |

Of v4's 252 right answers, 251 were retrieved. On the screen probe, fix 6's 84 right answers were all retrieved (v4's
screen adapter: 75 of 76). The gains so far are recovered information.

**Amendment.** In every condition of the final test, recall is reported by source, and R-016's recall rule (at least
20 points above base at each length, pooled over the three adapters, sign test below p = 0.01) must also hold when
only retrieved answers count, for base and adapters alike. A guess can no longer carry the result. Nothing is
loosened. No final run has happened.

## R-042 · 2026-11-03 · SPRINT · Fix 6's remaining misses, and fix 7: searches in the friend's own words

Fix 6's screen adapter (`screen_more_indirect_82`, probe seed 51203) misses, by cause: `in_view` answered without
searching and wrong 9; `older` searched and not found 4, found and not used 3; `in_view` searched and wrong 3;
`confirm` searched and not found 3, found and not used 2; `statement` searched 1.

The searches that miss are written in the training pool's words, not the friend's: "what freaks my barber out the
most" is searched as `bruder born winter month`, "did i mention what language my barber speaks" as `bank brother
city`, "what's the new ink on my stepsister" as `sister new title book`. "born", "month", "city", "title" and "teaches"
are keywords of the train pool's fact types. Every demonstrated search in training is a fixed keyword pattern per fact
type (`{who} moving city`, `{who} promoted title`), often with words the friend never said, so the model learned to
recite them, and it also bends unfamiliar relation words ("barber") toward familiar ones.

**Fix 7, `--message-queries`.** Each demonstrated search is built from the friend's own message: the name or relation
they gave first, then up to three other words of theirs, with function words and ways of saying "I forgot" dropped
(`demonstrations.message_words_query`, tested). On 300 train questions (`older` and `confirm`, build seeds as
`run_build_training_set.py` draws them), these searches found the fact 300 times, the same as the fixed keywords, so
no demonstration loses its fact. The rest of the build is fix 6's. Screened against fix 6's screen adapter on probe seed
51203; a gain goes to three seeds under a rule written first.

## R-043 · 2026-11-03 · SPRINT · Wrong although retrieved: a reading failure; fix 8 states each training fact in more ways

Kevin agreed the answers that were wrong although the fact was retrieved are worth fixing. v4, probe seed 73157, three
seeds: 11 such answers; with fix 6's screen adapter, 16 in all. 12 of the 16 are false denials ("I don't have that from
you", "I checked and you haven't told me that"); 3 give other content; 1 names the decoy.

**Not position.** In 10 of v4's 11 the fact was the top search result (successes: 247 of 251 at the top). In
`58_confirm_12` the model searched `tutor scares` and got one passage, "Ayaan, who is my tutor, is terrified of
pigeons", and replied "I don't have that from you"; seed 83 searched `tutor fear` and answered "Your tutor, Ayaan, is
scared of pigeons".

**A reading failure on wording.** The probe's `fear` type fails 7 of 68 retrieved answers (10%) against about 2% for the
other types; its statement says "terrified of" and its questions say "scares", "scared", "freaks out". Failures share no
content word with the fact statement 6 times in 11, successes 96 in 251. Each train fact template states its fact in
one wording, so the model saw every fact one way and learned to match on words.

**Fix 8, `--more-statements`.** Three more statements per train fact type (`train_phrasings.MORE_STATEMENTS`, 75,
written by Claude), each with different words for the fact ("has a new pup called" beside "adopted a dog named"), each
opening the way an existing train statement opens, so no opening matches a sealed pool's (tested). Every fact line,
decoys included, draws its wording from a separate generator, so the rest of the conversation is unchanged (tested).
The probe's wording was read in the loss list above, and none of the new statements copies it. Built on fix 6's data
and screened against fix 6's screen adapter on probe seed 51203, independently of fix 7.

## R-044 · 2026-11-03 · SPRINT · Capacity screens beat every data fix: LoRA on the MLP layers, and rank 32; R-040's confirmation superseded before it ran; combinations next

Development only, screen probe seed 51203, adapter seed 82, lean loss, v4's data, against v4's screen adapter
(`screen_relation_answers_82`). The `--lora-targets` and `--lora-r` options (commit `aca12f9`) leave the defaults as
they were.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | Peak GiB |
|---|---|---|---|---|---|---|---|---|
| v4 | 76 | 34 | 42 | 37 | 48 | 48 | 232 | 7.12 |
| fix 6 (R-040) | 84 | 41 | 43 | 36 | 48 | 47 | 235 | |
| LoRA on attention and MLP (`screen_lora_mlp_82`) | 87 | 39 | 48 | 37 | 48 | 48 | 234 | 7.47 |
| LoRA rank 32 (`screen_lora_r32_82`) | 86 | 40 | 46 | 43 | 48 | 47 | 233 | 7.22 |

On `older` plus `confirm`, against v4: MLP 1 alone right and 12 alone (p < 0.01); rank 32 2 and 12 (p = 0.013). Over all
kinds: MLP 6 and 17 (p = 0.035); rank 32 5 and 20 (p < 0.01). Rank 32 also lifts `in_view` from 37 to 43, which no data
fix has moved. Both fit well within the card (training 1,696 s and 1,367 s).

**R-040's confirmation is superseded before it ran.** Its runs had not started; the queued job was stopped at 20:07.
Confirming fix 6 on v4's settings would confirm a set already outgrown, so the card goes to combinations first. R-040's
rule is not applied to anything; fix 6's screen stands as recorded.

**Combinations, next.** Fix 6's data with (a) LoRA on attention and MLP, (b) rank 32, (c) both, each against fix 6's
screen adapter. The best goes to three seeds under a rule written before those runs, with Sheet A and Sheet B. Fixes 7
and 8 are still screened on v4's settings against fix 6, as R-042 and R-043 set out, and join the winner if they gain.

## R-045 · 2026-11-03 · SPRINT · R-038's crowded condition on the probe, development: v4 holds with four decoys

Development only, probe seed 73157, the same conversations as R-036 with four decoys a chat instead of one
(`run_recall_eval.py --decoys 4`, labels `probe_d4_base`, `probe_d4_v4_8x`; v4 adapters `adapters/v4_seed_8x`). Counts from
`report_data` (`recall`, `false_retrieval`, `recall_sources`).

| Probe seed 73157 | Base, 1 decoy | Base, 4 decoys | v4, 1 decoy (3 seeds) | v4, 4 decoys (3 seeds) |
|---|---|---|---|---|
| `older` + `confirm` correct | 30 of 96 | 27 of 96 | 252 of 288 | 245 of 288 |
| of which retrieved / guessed | 30 / 0 | 27 / 0 | 251 / 1 | 245 / 0 |
| wrong although retrieved | 4 | 7 | 11 | 17 |
| False retrieval, all replies | 13 of 240 | 19 of 240 | 8 of 720 | 22 of 720 |
| False retrieval on `older` + `confirm` | 1 | 7 | 4 | 12 |
| Right decisions per seed | 119 | 119 | 236, 229, 226 | 236, 229, 226 |

Four decoys cost v4 7 of 288 correct answers. Its false-retrieval rate rises from 1.1% to 3.1% and stays below base's
(5.4% to 7.9%); per adapter, 2, 9 and 11 false retrievals against base's 19 on the same conversations. Every right answer under
four decoys was retrieved. Answers wrong although the fact came back rise from 11 to 17, the reading failure R-043 targets.
This decides nothing; it shows where the current adapter stands on the condition R-038 added to the final test.

## R-046 · 2026-11-03 · SPRINT · Learning rate 3e-4 also beats v4: three ways to train harder all gain; two more combinations queued

Development only, screen probe seed 51203, adapter seed 82, v4's data, against v4's screen adapter.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) |
|---|---|---|---|---|---|---|---|
| v4 | 76 | 34 | 42 | 37 | 48 | 48 | 232 |
| learning rate 3e-4 (`screen_lr3e4_82`) | 86 | 40 | 46 | 39 | 48 | 48 | 235 |

On `older` plus `confirm`, 1 v4 alone right and 11 alone (p = 0.006); all kinds 3 and 15 (p = 0.008). With R-044, a higher
learning rate, a higher rank and LoRA on the MLP layers each gain about ten recall answers, and a lower learning rate
loses nine (R-040): v4's settings under-train it. Queued after fix 8, against fix 6's screen adapter: fix 6's data at
learning rate 3e-4 (`fix6_lr3e4`), and with all three changes together (`fix6_all`: rank 32, attention and MLP, 3e-4),
beside R-044's three combinations. The best goes to three seeds under a rule written first.

## R-047 · 2026-11-03 · SPRINT · Fix 6's data at rank 32 is the best screen yet (recall 92 of 96); every stronger setting costs a few statements, all on one probe opening

Development only, screen probe seed 51203, adapter seed 82, fix 6's data (`data/screens/more_indirect.jsonl`), against
fix 6's screen adapter (`screen_more_indirect_82`) and v4's (`screen_relation_answers_82`).

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | Train s | Peak GiB |
|---|---|---|---|---|---|---|---|---|---|
| v4 | 76 | 34 | 42 | 37 | 48 | 48 | 232 | | 7.12 |
| fix 6 (R-040) | 84 | 41 | 43 | 36 | 48 | 47 | 235 | | |
| fix 6 + LoRA on attention and MLP (`screen_fix6_mlp_82`) | 87 | 42 | 45 | 39 | 48 | 43 | 235 | 1,651 | 7.48 |
| fix 6 + rank 32 (`screen_fix6_r32_82`) | 92 | 45 | 47 | 39 | 48 | 44 | 235 | 1,282 | 7.22 |

Exact sign tests on conversations one adapter got right and the other wrong:

| Comparison | `older` + `confirm` | All kinds | `statement` |
|---|---|---|---|
| rank 32 combination against v4 | 0 and 16 (p < 0.0001) | 8 and 22 (p = 0.016) | 4 and 0 (p = 0.125) |
| rank 32 combination against fix 6 | 1 and 9 (p = 0.022) | 11 and 19 (p = 0.20) | 3 and 0 (p = 0.25) |
| MLP combination against v4 | 3 and 14 (p = 0.013) | 14 and 22 (p = 0.24) | 5 and 0 (p = 0.063) |
| MLP combination against fix 6 | 5 and 8 (p = 0.58) | 16 and 18 (p = 0.86) | 4 and 0 (p = 0.13) |

**Rank 32 adds to fix 6; the MLP layers do not.** On fix 6's data the MLP combination gains 3 recall answers and is
not separable from fix 6 (p = 0.58). Rank 32 gains 8 (p = 0.022) and gets every recall answer v4 got.

**The cost is on `statement`.** All four statements the rank 32 combination fails are one probe opening, "my {relation}
has been acting strange lately": it searches ("barber promotion") and recites a stored fact ("Your barber, Beatriz, got a
lighthouse tattoo."). The MLP combination fails the same opening four times and "texted me out of nowhere" once. Fix 6
failed it once; v4 never. This opening reads close to a question about the person, and harder training makes the model
treat it as one. Each loss is small and none is significant alone, but it is the one kind that falls as recall rises, so
the confirmation rule below this record must hold `statement` and a blind coherence check, not recall alone. Fix 8
(more ways of stating facts, queued) is the data fix aimed at this.

Still to read tonight: fix 6 + rank 32 + MLP, fix 7, fix 8, fix 6 + 3e-4, and fix 6 with all three changes.

## R-048 · 2026-11-03 · SPRINT · Rank 32 with the MLP layers ties rank 32 alone; rank 32 alone stays the lead

Development only, screen probe seed 51203, adapter seed 82, fix 6's data.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | Train s | Peak GiB |
|---|---|---|---|---|---|---|---|---|---|
| fix 6 (R-040) | 84 | 41 | 43 | 36 | 48 | 47 | 235 | | |
| fix 6 + rank 32 (R-047) | 92 | 45 | 47 | 39 | 48 | 44 | 235 | 1,282 | 7.22 |
| fix 6 + rank 32 on attention and MLP (`screen_fix6_mlp_r32_82`) | 90 | 42 | 48 | 43 | 48 | 43 | 235 | 1,663 | 7.83 |

Against rank 32 alone: recall 4 and 2 (p = 0.69), all kinds 6 and 7 (p = 1.0), `in_view` 0 and 4 (p = 0.13). Against
fix 6: recall 3 and 9 (p = 0.15). The MLP layers add no recall, cost 30% more training time and 0.6 GiB more card
memory, and lose one more statement; the `in_view` gain of 4 is not significant on its own. Rank 32 alone stays the
lead. Its four `in_view` gains are noted for the confirmation: rank 32 on v4's data also lifted `in_view` (R-044).

## R-049 · 2026-11-03 · SPRINT · Confirmation rule for fix 6 at rank 32, written before seeds 83 and 84 exist and before any of its coherence sheets

Fix 6 at rank 32 (R-047) is the lead on the screen. It is meant to raise recall, and R-047 found it loses a few
statements, so the rule must check that it beats v4 on recall, and also that it holds `statement`, coherence and false
retrieval. Seeds 82 (the screen adapter, `adapters/screens/fix6_r32_82`), 83 and 84, trained on
`data/screens/more_indirect.jsonl` with `--lora-r 32`, scored on probe seed 73157 as `probe8_tuned8x`, against v4
(`probe6_tuned8x`, R-036) and base (`probe2_base`).

v4 on this probe, pooled over its three seeds: recall 252 of 288, `in_view` 115 of 144, `statement` 143 of 144, false
retrieval 8 of 720 replies. Base: false retrieval 13 of 240.

Fix 6 at rank 32 replaces v4 (as v5) only if all of these hold:

1. Correct `older` plus `confirm`, pooled, higher than v4's 252 of 288.
2. Correct `in_view`, pooled, at least 110 of 144 (v4's 115 less 5%, as R-040).
3. Correct `statement`, pooled, at least 136 of 144 (v4's 143 less 5%, the same tolerance as item 2). This item is new:
   R-047 showed `statement` is the kind that falls as recall rises.
4. Right decisions at least 200 of 240 on every seed.
5. False retrieval, pooled, no higher than base's rate (13 of 240, so at most 39 of 720), as R-038 requires of the
   final test. v4's 8 is reported beside it.
6. Sheet A on `older` and `confirm`, each seed against base on probe seed 73157, a fresh judge per sheet: pooled
   `confirm` coherent at or above base's count, and pooled `older` plus `confirm` coherent at or above base's count.
7. Sheet B on `statement` and `in_view`, each seed against base with no tool (built as R-036B), a fresh judge per
   sheet: on every seed, coherent `statement` and coherent `in_view` each at or above base's count on that sheet.
   Until now Sheet B ran after the decision; this rule makes it decide, because the statements this setting fails
   are replies that recite an unasked fact.

Otherwise v4 stands. Judges get only the rubric and the sheet; marks go to the scratchpad and are copied in. No
held-out or independent run comes out of this without Kevin. The runs are queued after the screens already on the
card (fix 7, fix 8, R-046's two combinations, rank 64, rank 32 at 3e-4); if one of those beats this lead on the screen,
it gets its own rule and runs, and this one is still decided as written.

## R-050 · 2026-11-03 · SPRINT · Fix 7 (searches in the friend's own words) lifts recall to 94 of 96 but answers never-told questions with other people's facts: dropped; fix 7b queued

Development only, screen probe seed 51203, adapter seed 82, rank 16. Fix 6's build plus `--message-queries` (R-042),
`data/screens/message_queries.jsonl`, 800 rows; trained 1,239 s, peak 7.13 GiB.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | False retrieval (of 240) |
|---|---|---|---|---|---|---|---|---|
| fix 6 (R-040) | 84 | 41 | 43 | 36 | 48 | 47 | 235 | 0 |
| fix 7 (`screen_message_queries_82`) | 94 | 46 | 48 | 39 | 21 | 44 | 229 | 27, all `never_told` |

Against fix 6: recall 1 alone right and 11 (p = 0.006); all kinds 36 and 19 (p = 0.030, fix 6 better). On 27 of 48
never-told questions fix 7 searches in the question's words, gets back the same fact about other people, and gives
one of them as the answer ("did i mention what language my daughter speaks" → "Your daughter Hana speaks Tagalog.").
That is false retrieval, which R-038 forbids above base. Fix 7 is dropped as built.

**Why.** With the friend's own words, the search in a never-told training row often finds nothing, because the
question's words are not in any statement ("coworker band" against "plays bass in Salt Road"). Of fix 7's 150
never-told rows, 77 have an empty result; fix 6's have 20. So fix 7 taught declining mainly on empty results, while on
the probe the question's words ("language", "speaks") do match other people's facts. The recall gain is real (the
searches find more facts); the training simply stopped showing the case where the wrong person's fact comes back.

**Fix 7b, `--never-told-hits`** (commit `1eb289a`): fix 7's build, but a never-told row is kept only if its search
returns passages, so all 150 show other people's facts coming back and the reply declining. Screened against fix 7
and fix 6 on probe seed 51203, after R-049's confirmation runs. It goes forward only if `never_told` is back at fix
6's level with false retrieval at 0 and recall stays above fix 6.

## R-051 · 2026-11-04 · SPRINT · Fix 8 (more ways of stating each fact) is a small, non-significant gain; it misses its target; screened again at rank 32

Development only, screen probe seed 51203, adapter seed 82, rank 16. Fix 6's build plus `--more-statements` (R-043),
`data/screens/more_statements.jsonl`, 800 rows; trained 1,290 s, peak 7.12 GiB.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | False retrieval | Wrong though retrieved |
|---|---|---|---|---|---|---|---|---|---|
| fix 6 (R-040) | 84 | 41 | 43 | 36 | 48 | 47 | 235 | 0 | 5 |
| fix 8 (`screen_more_statements_82`) | 86 | 42 | 44 | 41 | 47 | 47 | 238 | 1 | 7 |

Against fix 6: recall 5 alone right and 7 (p = 0.77); all kinds 9 and 15 (p = 0.31); `in_view` 3 and 8 (p = 0.23).
Fix 8 was built for the answers the model got wrong although the search returned the fact (R-043). Those did not fall
(7 against 5), so it misses its target. The `in_view` gain of 5 is the largest any data fix has made on that kind, but
it is not significant alone.

Fix 8's data is screened again at rank 32 against fix 6 at rank 32 (queued after fix 7b): R-047 found that rank 32
loses statements, and more ways of stating facts is the data change most likely to prevent that. It is kept as a
candidate for that reason only.

## R-052 · 2026-11-04 · SPRINT · Fix 6 with all three capacity changes is the best screen (recall 95 of 96, false retrieval 0); R-049 superseded before its runs; confirmation rule for it

Development only, screen probe seed 51203, adapter seed 82, fix 6's data.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | False retrieval | Train s | Peak GiB |
|---|---|---|---|---|---|---|---|---|---|---|
| fix 6 (R-040) | 84 | 41 | 43 | 36 | 48 | 47 | 235 | 0 | | |
| fix 6 + rank 32 (R-047) | 92 | 45 | 47 | 39 | 48 | 44 | 235 | 0 | 1,282 | 7.22 |
| fix 6 + 3e-4 (`screen_fix6_lr3e4_82`) | 92 | 45 | 47 | 41 | 48 | 46 | 238 | 0 | 1,315 | 7.12 |
| fix 6 + rank 32, attention and MLP, 3e-4 (`screen_fix6_all_82`) | 95 | 47 | 48 | 44 | 48 | 46 | 238 | 0 | 1,643 | 7.83 |

Sign tests (conversations one adapter got right and the other wrong):

| Comparison | `older` + `confirm` | All kinds | `in_view` |
|---|---|---|---|
| 3e-4 against fix 6 | 0 and 8 (p = 0.008) | 4 and 16 (p = 0.012) | 3 and 8 (p = 0.23) |
| 3e-4 against rank 32 | 1 and 1 (p = 1.0) | 5 and 9 (p = 0.42) | 4 and 6 (p = 0.75) |
| all three against fix 6 | 0 and 11 (p = 0.001) | 4 and 22 (p < 0.001) | 3 and 11 (p = 0.057) |
| all three against rank 32 | 1 and 4 (p = 0.38) | 3 and 13 (p = 0.021) | 1 and 6 (p = 0.13) |

With all three changes the adapter misses one recall question of 96, gains on `in_view` (44 against 36), loses one
statement where rank 32 alone lost three, and names no wrong value anywhere. Over all kinds it beats R-049's lead
(p = 0.021).

**R-049 is superseded before its runs.** Its queue was still waiting for earlier screens and had produced nothing; it
was stopped at 01:41. Confirming rank 32 alone would confirm a setting already beaten on the screen, as R-044 found for
R-040. R-049's rule is not applied to anything. (R-049 said a better screen would get its own runs beside it; the card
time goes to the better setting instead, and this record says so.)

**Confirmation rule for fix 6 with all three changes, written before seeds 83 and 84 exist and before any of its
coherence sheets.** R-049's seven items, unchanged, for this setting: seeds 82 (`adapters/screens/fix6_all_82`), 83
and 84, trained on `data/screens/more_indirect.jsonl` with `--lora-r 32 --lora-targets q_proj k_proj v_proj o_proj
gate_proj up_proj down_proj --learning-rate 3e-4`, scored on probe seed 73157 as `probe9_tuned8x`, against v4
(`probe6_tuned8x`) and base (`probe2_base`). It replaces v4 (as v5) only if: (1) recall pooled above 252 of 288;
(2) `in_view` pooled at least 110 of 144; (3) `statement` pooled at least 136 of 144; (4) right decisions at least 200
of 240 on every seed; (5) false retrieval pooled at most 39 of 720; (6) Sheet A, pooled `confirm` and pooled `older`
plus `confirm` coherent at or above base; (7) Sheet B on every seed, `statement` and `in_view` coherent each at or
above base. Otherwise v4 stands. Fresh judges, rubric and sheet only, marks to the scratchpad and copied in. No
held-out or independent run without Kevin.

Still on the card before these runs: rank 64 and rank 32 at 3e-4 (R-047's queue). After them: fix 7b (R-050) and fix 8
at rank 32 (R-051).

## R-053 · 2026-11-04 · SPRINT · Rank 64 gains nothing over rank 32; rank 32 at 3e-4 without the MLP layers fails one statement opening 8 times in 10; R-052's lead stands

Development only, screen probe seed 51203, adapter seed 82, fix 6's data. Both queued in R-047.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | False retrieval | Train s | Peak GiB |
|---|---|---|---|---|---|---|---|---|---|---|
| fix 6 + rank 32 (R-047) | 92 | 45 | 47 | 39 | 48 | 44 | 235 | 0 | 1,282 | 7.22 |
| fix 6 + all three (R-052) | 95 | 47 | 48 | 44 | 48 | 46 | 238 | 0 | 1,643 | 7.83 |
| fix 6 + rank 64 (`screen_fix6_r64_82`) | 91 | 45 | 46 | 35 | 48 | 47 | 235 | 0 | 1,331 | 7.42 |
| fix 6 + rank 32 + 3e-4 (`screen_fix6_r32_lr3e4_82`) | 93 | 45 | 48 | 42 | 48 | 39 | 231 | 0 | 1,349 | 7.22 |

- **Rank 64** against rank 32: recall 4 and 3 (p = 1.0), all kinds 12 and 10 (p = 0.83). Raising the rank past 32
  adds nothing: capacity through rank has levelled off. Against all three: all kinds 14 and 2 (p = 0.004).
- **Rank 32 at 3e-4, attention only** against all three: recall 2 and 0 (p = 0.50), all kinds 15 and 4 (p = 0.019),
  `statement` 8 and 1 (p = 0.039). Eight of its nine statement failures are the one opening R-047 found, "my
  {relation} has been acting strange lately". Out of the ten probe statements with that opening, the failures are:
  v4 0, all three 2, rank 32 4, rank 32 at 3e-4 8.

The MLP layers did not add recall on their own (R-047, R-048), but with rank 32 and 3e-4 they are what keeps this
opening from being read as a question. R-052's lead stands, and its confirmation is next on the card. The "acting
strange" opening is the one weak spot left on the screen, and R-052's item 3 and Sheet B check it.

## R-054 · 2026-11-04 · SPRINT · Fix 7b brings `never_told` only part of the way back and loses statements: the fix 7 line is dropped; next screens on the lead's settings

Development only, screen probe seed 51203, adapter seed 82, rank 16. Fix 7's build plus `--never-told-hits` (R-050),
`data/screens/never_told_hits.jsonl`, 800 rows; trained 1,330 s, peak 7.12 GiB.

| Label | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | False retrieval (of 240) |
|---|---|---|---|---|---|---|---|---|
| base (`screen_base`) | 38 | 33 | 5 | 32 | 46 | 25 | 109 | 9 |
| fix 6 (R-040) | 84 | 41 | 43 | 36 | 48 | 47 | 235 | 0 |
| fix 7 (R-050) | 94 | 46 | 48 | 39 | 21 | 44 | 229 | 27 |
| fix 7b (`screen_never_told_hits_82`) | 95 | 47 | 48 | 38 | 36 | 38 | 222 | 13 (12 `never_told`) |

Against fix 6: recall 0 alone right and 11 (p = 0.001), but `statement` 9 and 0 (p = 0.004) and all kinds 27 and 19.
Every recall answer it gets right is retrieved (95 of 95). R-050's bar for going forward was `never_told` back at 48
with no false retrieval. Fix 7b reaches 36, names a wrong value 13 times (base 9), and searches on statements of every
opening, not one. Dropped, and with it the fix 7 line: training searches in the friend's own words teach the model
that any line naming a person is a lookup, and showing it more declines fixes only part of that.

The recall gain from searching in the friend's words (95 of 96) equals R-052's lead (95 of 96), which gets there with
fix 6's keyword searches and no loss on `never_told` or false retrieval.

**Next, on the lead's settings** (rank 32, attention and MLP, 3e-4), against `screen_fix6_all_82`, queued after R-052's
confirmation: fix 8's data (`fix8_all`), which replaces R-051's plan for fix 8 at rank 32 alone, since rank 32 alone is
no longer the lead; and fix 6's data at 4 epochs (`fix6_all_e4`).

## R-055 · 2026-11-04 · SPRINT · R-052's rule fails on Sheet B at its first seed: v4 stands; the lead answers "just chatting" lines with stored facts; fix 9, more chat lines

**R-052's confirmation, seed 82** (the screen adapter, probe seed 73157, `probe9_tuned82`):

| Measure | fix 6 + all three, seed 82 | v4, seed 82 (`probe6_tuned82`) | Base |
|---|---|---|---|
| Recall (`older` + `confirm`, of 96) | 92 | 84 | 30 |
| `in_view` (of 48) | 41 | 39 | 34 |
| `statement` (of 48) | 43 | 48 | 31 |
| `never_told` (of 48) | 47 | 47 | 42 |
| Right decisions (of 240) | 235 | 236 | 119 |
| False retrieval (of 240) | 1 | 1 | 13 |

Sheet A (`results/coherence/R-055/`, shuffle seed 90441, a fresh Sonnet judge, rubric and sheet only): base against
the adapter, `older` 29 against 38, `confirm` 47 against 48. At or above base.

Sheet B (`results/coherence/R-055B/`, shuffle seed 90444, base's `three_exchanges` replies, a second fresh judge):
`in_view` 33 against 43, but **`statement` 45 against 41**. R-052's item 7 needs `statement` at or above base on every
seed, so **the rule fails at seed 82 and v4 stands.** Seeds 83 and 84 could not change that; seed 83's training was
stopped at 03:41, five minutes in, and its partial adapter deleted. Items 1 to 5 are not reported as passed or failed,
because the rule is decided on item 7.

**What the judge marked down.** Of the adapter's 7 incoherent `statement` replies, 4 are "my {relation} has been
acting strange lately": it searches ("tutor acting strange") and states a stored fact ("My tutor, Ayaan, got a swallow
tattoo last week."), once claiming the friend's tutor as its own. The other 3 did not search but answered off the
point ("Esme must be feeling a bit fed up with you."). The screen (R-047, R-053) showed the same opening failing, but
`statement` correctness there counts only searching; Sheet B counts the reply.

**Fix 9, `--more-chat`** (this commit). The train pool has 6 chat lines against 25 fact templates, and none about how
a person is behaving or feeling. Trained harder, the model treats any line about a named person as a lookup.
`train_phrasings.MORE_CHAT` adds 48 chat lines in the train pool's voice: moods and behaviour, plans, complaints,
small events, feelings about someone. Statement rows take base's own reply with no tool, as before. A test checks that
no four-word run of any new line appears in the probe's, the held-out pool's or the independent pool's chat lines; it
reports only the new line, so the sealed pools stay unread. Seven drafted lines failed that test and were reworded
before this commit. Disclosure: the category (how a person is behaving) was chosen because the probe's failures are
in it. The probe's own wording is excluded by the test, and the sealed pools are the test of whether it generalises.

**Next.** Fix 9's build (fix 6's flags plus `--more-chat`) on the lead's settings (rank 32, attention and MLP, 3e-4),
screened against `screen_fix6_all_82`. It goes to a confirmation only if `statement` on the screen is at least v4's 48
less one and recall is not below the lead's 95 less 3. Its confirmation then runs R-052's seven items, with Sheet B on
every seed. After it: fix 8's data and 4 epochs on the lead's settings (R-054's plan).

## R-056 · 2026-11-04 · SPRINT · Fix 9 passes R-055's screen gate (statement 48 of 48, recall 94 of 96, every decision right); fix 8 and 4 epochs on the lead's settings lose statements; confirmation rule for fix 9

Development only, screen probe seed 51203, adapter seed 82, all at rank 32 on attention and MLP, 3e-4 (R-052's
settings).

| Label | Data | Recall (of 96) | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions (of 240) | False retrieval | Train s | Peak GiB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Base (`screen_base`) | | 38 | 33 | 5 | 32 | 46 | 25 | 109 | 9 | | |
| v4 (`screen_scripted_confirm_82`) | | 71 | 33 | 38 | 37 | 48 | 48 | 232 | 0 | | |
| Lead, R-052 (`screen_fix6_all_82`) | fix 6 | 95 | 47 | 48 | 44 | 48 | 46 | 238 | 0 | 1,643 | 7.83 |
| `screen_fix9_all_82` | fix 9 (`more_chat.jsonl`) | 94 | 47 | 47 | 45 | 47 | 48 | 240 | 1 | 1,659 | 7.83 |
| `screen_fix8_all_82` | fix 8 (`more_statements.jsonl`) | 94 | 46 | 48 | 42 | 45 | 40 | 232 | 3 | 1,630 | 7.82 |
| `screen_fix6_all_e4_82` | fix 6, 4 epochs | 93 | 45 | 48 | 44 | 48 | 38 | 230 | 0 | 2,267 | 7.83 |

Sign tests for fix 9 (conversations one adapter got right and the other wrong): against the lead, recall 1 and 2
(p = 1.0), all kinds 4 and 3 (p = 1.0), `statement` 2 and 0 (p = 0.5); against v4, recall 24 and 1 (p < 0.0001), all
kinds 34 and 4 (p < 0.0001), `in_view` 10 and 2 (p = 0.039); against base, recall 56 and 0, all kinds 94 and 1.
Recall is 34% above v4 and 147% above base on this probe. Its one false retrieval is a `never_told` reply; base has 9.
No `statement` line was searched.

**Fix 9 passes R-055's gate** (`statement` at least 47, recall at least 92). The screen counts `statement` by whether
it searched, so the gate does not show whether the replies are good chat; Sheet B does, and R-055 failed there.

**Fix 8 on the lead's settings is dropped**: `statement` 40 of 48 and 3 false retrievals on `never_told`. **Four
epochs is dropped**: against the lead it loses 8 statements and gains none (p = 0.008), and over all kinds 3 against
13 (p = 0.021). Training longer, like training harder (R-055), costs plain chat before it adds recall.

**Confirmation rule for fix 9, written before seeds 83 and 84 exist and before any of its coherence sheets.** R-052's
seven items, unchanged, for this data: seeds 82 (`adapters/screens/fix9_all_82`), 83 and 84, trained on
`data/screens/more_chat.jsonl` with `--lora-r 32 --lora-targets q_proj k_proj v_proj o_proj gate_proj up_proj
down_proj --learning-rate 3e-4`, scored on probe seed 73157 as `probe10_tuned8x`, against v4 (`probe6_tuned8x`) and
base (`probe2_base`). It replaces v4 (as v5) only if: (1) recall pooled above 252 of 288; (2) `in_view` pooled at
least 110 of 144; (3) `statement` pooled at least 136 of 144; (4) right decisions at least 200 of 240 on every seed;
(5) false retrieval pooled at most 39 of 720; (6) Sheet A, pooled `confirm` and pooled `older` plus `confirm` coherent
at or above base; (7) Sheet B on every seed, `statement` and `in_view` coherent each at or above base. Otherwise v4
stands. Seed 82 is scored first and its Sheet B judged while seed 83 trains; if seed 82 fails item 7, the remaining
runs stop, as in R-055. Fresh judges, rubric and sheet only, marks to the scratchpad and copied in. No held-out or
independent run without Kevin. From this queue on, runs set `HF_HUB_OFFLINE=1` and `HF_HUB_DISABLE_TELEMETRY=1`:
TRL had sent a usage ping to huggingface.co at the start of each training run; nothing else went online.

## R-057 · 2026-11-04 · SPRINT · R-056's rule fails on Sheet B at seed 84 (statement 42 against base 46): v4 stands; items 1 to 6 pass by wide margins

**R-056's confirmation** (probe seed 73157, `probe10_tuned8x`, seeds 82, 83, 84; queue finished 08:44):

| Measure | Fix 9, seed 82 | 83 | 84 | Fix 9 pooled | v4 pooled (`probe6_tuned8x`) | Rule |
|---|---|---|---|---|---|---|
| Recall (`older` + `confirm`) | 90 | 96 | 90 | **276 of 288** | 252 | above 252: pass |
| `in_view` | 42 | 40 | 46 | **128 of 144** | 115 | at least 110: pass |
| `statement` | 48 | 48 | 48 | **144 of 144** | 143 | at least 136: pass |
| Right decisions (of 240) | 240 | 240 | 240 | | 236, 229, 226 | at least 200 each: pass |
| False retrieval | 1 | 0 | 0 | **1 of 720** | 8 | at most 39: pass |

Against v4 on the same conversations, pooled: recall 33 and 9 (p = 0.0003), all kinds 54 and 14 (p < 0.0001). Base
(`probe2_base`, one run) has recall 30 of 96, so fix 9's 92 a seed is 207% above base.

Coherence, six fresh Sonnet judges, rubric and sheet only, one judge a sheet, marks in `results/coherence/R-057/` and
`R-057B/`. Shuffle seeds: Sheet B 90445, 90446, 90447 (seeds 82, 83, 84); Sheet A 90448, 90449, 90450.

| Sheet | Kind | Base | Fix 9, seed 82 | 83 | 84 | Pooled base | Pooled fix 9 |
|---|---|---|---|---|---|---|---|
| A | `older` | 34, 17, 30 | 42 | 42 | 46 | 81 | 130 |
| A | `confirm` | 47, 41, 47 | 48 | 48 | 48 | 135 | 144 |
| B | `in_view` | 34, 35, 34 | 44 | 41 | 40 | 103 | 125 |
| B | `statement` | 45, 45, 46 | 48 | 46 | **42** | 136 | 136 |

Item 6 passes. Item 7 needs `statement` at or above base on every seed; **seed 84 is 42 against 46, so the rule fails
and v4 stands.** Pooled, `statement` ties base at 136.

**What the judge marked down at seed 84.** Six replies, none searched: "Lucia is a great name.", "Dmitri is a great
name. What did you talk about?" and "Esme is a great name..." to "i got stuck talking to {person} for an hour"; "It
sounds like you're feeling a bit down" twice to "i should really call my {relation}"; and a reply that asks about the
camera and the chimney from earlier turns. These are the untrained model's habits: statement rows train on base's own
no-tool reply, and some of those targets are weak (a sample of 20 from `more_chat.jsonl` shows a bulleted list, "Is
there anything I can do to help?", and a reply that contradicts the line). Seed 83's two were "Esme is a character from
the TV show *The Office*" and "How did they get your number?".

**Judge agreement.** Base's replies are the same on every sheet of a kind, so its score measures the judges. On Sheet B
they agree within one line (`statement` 45, 45, 46; `in_view` 34, 35, 34), so seed 84's 42 is a difference between
adapters, not between judges. On Sheet A they do not: base `older` is 34, 17 and 30 on the same 48 replies. The
judge of A83 marked down any reply that opens with a name and a comma. Sheet A's item is pooled and passes by 49 lines,
so this does not change the result; it is recorded for the write-up's threats to validity.

## R-058 · 2026-11-04 · SPRINT · Fix 10: a blind judge vets the statement training targets before training; screen gate and confirmation rule written before the judging

**Why.** At seed 84 the adapter's incoherent `statement` replies were the untrained model's own habits ("Lucia is a
great name.", "It sounds like you're feeling a bit down" to "i should really call my classmate"), and statement rows
train on base's own no-tool reply, unvetted (R-057).

**Fix 10.** Fix 9's data (`more_chat.jsonl`) with its 150 `statement` targets vetted:

1. 150 spare statement rows, built with fix 9's flags at seed 71120 (`--kinds statement --statement-rows 150`,
   `data/screens/more_chat_spare.jsonl`).
2. `scripts/vet_statement_targets.py sheet` shuffles all 300 statement targets into one blind sheet (shuffle seed
   90451); the judge cannot tell targets from spares. A fresh Sonnet judge marks it with the same rubric as the
   coherence sheets, given only the rubric and the sheet.
3. `apply` swaps each target marked 0 for the next spare marked 1, preferring spares whose message is not already in
   the set. Every other row is unchanged. Output: `data/screens/vetted_chat.jsonl`.

Disclosure: the training targets are filtered by the same rubric the coherence judges use. The rubric is the
definition of coherence in this study, and filtering targets by it is ordinary rejection of bad examples; but it trains
toward what this kind of judge accepts, and the held-out judges are the same kind. The write-up says so.

**Gate and rule, written before the sheet is judged and before any fix 10 adapter exists.** Train seed 82 on
`vetted_chat.jsonl` at R-052's settings (`--lora-r 32 --lora-targets q_proj k_proj v_proj o_proj gate_proj up_proj
down_proj --learning-rate 3e-4`), screen it on probe seed 51203 (`screen_fix10_all_82`). It goes on only if `statement`
is at least 47 of 48 and recall at least 92 of 96 (R-055's gate). Then seeds 82, 83 and 84 are scored on probe seed
73157 as `probe11_tuned8x`, and R-052's seven items apply unchanged against v4 (`probe6_tuned8x`) and base
(`probe2_base`), with Sheet B on every seed. It replaces v4 (as v5) only if all seven pass. Fresh judges, rubric and
sheet only. No held-out or independent run without Kevin.

**Vetting result** (fresh Sonnet judge, `results/coherence/R-058/`): of the 150 targets, 137 coherent and 13 not; of
the 150 spares, 137 and 13. The 13 rejected targets were swapped for coherent spares. The judge's reasons: the
direction of a debt reversed, "great that you're catching up" to "haven't seen {person} in ages", "Who did you run
into?" to "guess who ran into {person}", a name taken for a TV character or "a male name", a topic carried over from
earlier turns, and one reply that contradicts the line.

## R-059 · 2026-11-04 · SPRINT · Fix 10 passes six of R-058's seven items; Sheet B `statement` at seed 84 is 45 against base 46: v4 stands

Probe seed 73157, `probe11_tuned8x`, seeds 82, 83, 84 (queue finished 11:11). Seed 82's screen on 51203
(`screen_fix10_all_82`): recall 96 of 96, `statement` 48, `in_view` 43, `never_told` 47; it passed R-055's gate.

| Measure | Seed 82 | 83 | 84 | Pooled | v4 pooled | Fix 9 pooled (R-057) | Rule |
|---|---|---|---|---|---|---|---|
| Recall (`older` + `confirm`) | 93 | 96 | 93 | **282 of 288** | 252 | 276 | above 252: pass |
| `in_view` | 42 | 40 | 42 | **124 of 144** | 115 | 128 | at least 110: pass |
| `statement` | 48 | 48 | 48 | **144 of 144** | 143 | 144 | at least 136: pass |
| Right decisions (of 240) | 240 | 240 | 240 | | 236, 229, 226 | 240 each | at least 200: pass |
| False retrieval | 1 | 0 | 2 | **3 of 720** | 8 | 1 | at most 39: pass |

Paired against v4, pooled: recall 35 and 5 (p < 0.0001), all kinds 55 and 15 (p < 0.0001). Against fix 9: recall 8 and
2 (p = 0.11), all kinds 13 and 13. Base (`probe2_base`) has recall 30 of 96, so fix 10's 94 a seed is 213% above base.

Coherence, six fresh Sonnet judges, one a sheet, rubric and sheet only, each seed's two sheets judged while the next
seed trained (`results/coherence/R-059/`, `R-059B/`). Shuffle seeds: Sheet B 90452, 90454, 90456; Sheet A 90453, 90455,
90457.

| Sheet | Kind | Base (seed 82, 83, 84 sheets) | Fix 10, seed 82 | 83 | 84 | Pooled base | Pooled fix 10 |
|---|---|---|---|---|---|---|---|
| A | `older` | 29, 33, 31 | 42 | 44 | 43 | 93 | 129 |
| A | `confirm` | 47, 47, 47 | 48 | 48 | 48 | 141 | 144 |
| B | `in_view` | 34, 35, 36 | 45 | 42 | 39 | 105 | 126 |
| B | `statement` | 46, 46, 46 | 48 | 48 | **45** | 138 | 141 |

Items 1 to 6 pass. Item 7 needs `statement` at or above base on every seed; **seed 84 is 45 against 46, so the rule
fails and v4 stands.** The three judges gave base's same 48 statement replies 46 each time, marking down the same two
("Dmitri is a character from the book *The Brothers Karamazov*", "Gustav is a powerful storm system"), so the gap is
one reply, not judge noise. Seed 84's three: "It sounds like you could use a call from your barber" to "i should
really call my barber"; "...or you could just enjoy the fact that..." to "Dmitri forgot my birthday again"; and "Did
she say what she wanted to know about my skateboard?" to "my daughter texted me out of nowhere", which pulls in an
earlier topic as the reply's own.

Against fix 9 (R-057), vetting the targets moved seed 84's `statement` from 42 to 45 and kept the other two seeds at
48; it did not remove the untrained model's habits entirely.

## R-060 · 2026-11-04 · SPRINT · Fix 11: brief statement targets, then vetted; gate and confirmation rule written before the build

**Why.** Every incoherent `statement` reply in R-057 and R-059, the adapter's and base's alike, is a long reply that
drifts: a book character, a storm system, an earlier topic taken as the reply's own, a reversed direction. Base's
replies are cut at 60 tokens, so the longer the reply, the more room to drift and the more often it ends mid-thought.

**Fix 11, `--brief-chat`** (commit `da083cf`). When the set is built, base is asked for its `statement` reply with "Reply
briefly, in one or two sentences." added to its system prompt. The training row leaves that sentence out, as
`--read-hint` does for `in_view`, so the adapter learns short replies to chat without being told. No other kind
changes; `statement` is built last, so every other row is identical to fix 9's at the same seed.

1. Full set, fix 9's flags plus `--brief-chat`, seed 71119: `data/screens/brief_chat.jsonl`.
2. 150 spares, same flags, seed 71120, `--kinds statement`: `data/screens/brief_chat_spare.jsonl`.
3. R-058's vetting: one blind sheet of all 300 statement targets (shuffle seed 90458), a fresh Sonnet judge, rejected
   targets swapped for coherent spares: `data/screens/vetted_brief.jsonl`.

**Gate and rule, written before the build.** As R-058, with labels `screen_fix11_all_82` and `probe12_tuned8x` and
adapters `adapters/screens/fix11_all_8x`: R-055's screen gate at seed 82, then R-052's seven items unchanged, with
Sheet B on every seed. It replaces v4 (as v5) only if all seven pass. No held-out or independent run without Kevin.
