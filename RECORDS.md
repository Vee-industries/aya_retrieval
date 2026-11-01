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
