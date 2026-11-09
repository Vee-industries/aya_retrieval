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
| R-061 | **v5**: fix 11 passes all seven items (recall 279 of 288, statement coherent on every seed) |
| R-062 | Fix 12: brief, vetted in_view targets spliced into v5's set; nine-item rule written before the build |
| R-063 | Fix 12 fails the screen gate (recall 90): dropped; v5's 23 misses broken down; fix 13 rule (more indirect in_view) |
| R-064 | Fix 13 fails the screen gate (recall 91): dropped; in_view changes trade in_view for older; v5 is the final candidate |
| R-065 | v5 with four decoys (development): recall 277 of 288, false retrieval 0 of 720; style of the independent pool untested |
| R-066 | Development twin of the independent pool (`hard_dev`), fresh agent, R-039's brief; cost to independence disclosed |
| R-067 | Harder development tests from LLE's failure categories: user typing style, corrections, 1,000-message chats |
| R-068 | On `hard_dev` v5's recall is 172 of 288: unseen fact types searched with the training pool's query phrases |
| R-069 | Fix 14: a wide training pool of new fact types by a fresh agent; gate and rule on probe and `hard_dev` first |
| R-070 | First wide pool discarded (its writer saw sealed fragments via a debug script); checker fixed; docs updated |
| R-071 | Fix 14: `hard_dev` recall 58 to 76 at seed 82, fails gate on statements (44) and never_told; fixes 14b, 14c |
| R-072 | Operational errors not recorded at the time (queue race, untracked files, quoting bug, stalled push) and fixes |
| R-073 | Fixes 14b and 14c fail on `hard_dev` never_told (32; 14b mends statements, 48); wide training makes the model state another person's fact; over-long rows in fixes 14 to 14c; fix 15 |
| R-074 | Fix 15 passes its gate (hard_dev recall 81, never_told 46, false retrieval 3); confirmation rule written before seeds 83 and 84 |
| R-075 | Fix 15 fails R-074 on three coherence items (recall and never_told pass): v5 stands; fix 15b's rule |
| R-076 | Training put loss on every token of a row, scripted small talk included; fixes 16a and 16b mask it; rule before they exist; demo transcripts |
| R-077 | Fix 16a: copying gone and hard_dev recall 58 to 70, but plain chat below base; the targets carry the tone errors; 16c (1e-4) |
| R-078 | Fix 17: plain-chat targets re-vetted on a stricter rubric by two judges; plan and rule before any target changes |
| R-079 | Fixes 16b and 16c fail their gates on counts; strict vetting rejects 15 of v5's 150 chat targets; fix 17 runs at 1e-4 by R-078's rule |
| R-080 | Fix 17 fails on counts; fix 17b (strict targets, 3e-4) passes R-076's gate; three-seed confirmation queued |
| R-081 | The demo's stale search: no training view holds a question; a stress test for a question right after another |
| R-082 | Fix 17b fails R-076's rule on one item, seed 83's Sheet B `statement` by one line; v5 stands; a chat line naming a fact type read as a question |
| R-083 | Fix 18: chat lines that name a fact type in passing, with a control; recipe, review and rule before the build |
| R-084 | A question right after another: the adapters keep recall; base loses plain chat; 17b turns away facts in view after a decline |
| R-085 | Fix 18a and 18c both fail the screen gate on recall; both fix the check set; v5 is below base on it |
| R-086 | Fix 19: questions asked as statements naming the topic, answered from a search; plan, review and a two-seed gate before the build |
| R-087 | Fix 20 chosen by a three-lane panel before it was written: half the fact-word dose over all 25 types, run only if 19a fails |
| R-088 | The compute left, panelled in three rounds to one plan; R-087's ruling replaced; the candidates list starts |
| R-089 | 19a passes every count but fails the judged check set by one line (a stock reply at seed 83); two planned candidates dropped at build |
| R-090 | Ten seed-82 models on one blind check-set sheet, three judges: 19a above base with the most recall; the dials trade chat for recall |
| R-091 | 17b at fresh seeds 85 to 87 fails R-076's rule again, under all three judges; at seed 86 it searches on chat lines that name a person |
| R-092 | 17m passes R-086's whole gate, the first candidate to; fix 20 fails; 17m goes to confirmation at 85 to 87, seed 82 named to ship |
| R-093 | 17m passes R-076's rule at fresh seeds 85 to 87 under all three judges: it replaces v5 as v6, seed 82 |
| R-094 | The who-is-who slip: measured, its source found, a gate registered and a fix agreed by the panel before any run; Kevin's ship ruling |
| R-095 | Fix A (fix17w) clears the slip gate and every count but fails R-086's judged Sheet B by one line under judge 1; fix B queued |
| R-096 | CuratorKIT's grounding gate over the training answers, three Claude judges: 22 of v6's 350 fail, 14 of them faults the slip pattern misses |
| R-097 | Fix C agreed by the panel before it was built: fix A's set without CuratorKIT's rejections (C1), scripted fallback (C2), a Monday deadline |
| R-098 | Fix C1 stops one probe recall answer short of v6; fix C2's 15 scripted answers pass CuratorKIT's acceptance test (15 of 15, controls 22 of 22) and go to seeds 82 and 83 |
| R-099 | Messy chats: the panel's plan before any run (measure first, a held-out phone-typing form, a registered trigger); the headline-number ruling |
| R-100 | An outside check on LoCoMo after the freeze, agreed by the panel before any data is downloaded |
| R-101 | Fix C2 removes the slip at both seeds but its hard_dev recall is below v6's (149 vs 157); the second failure ends the track and v6 stands |
| R-102 | v6's messy-chat battery: corrections cost 187 of 192; Kevin amends R-099 item 6 before any arm exists; held-out correction form and every threshold frozen before the baseline |
| R-103 | Kevin's decision: train in steps on top of a fix that failed, instead of restarting from v6; stepping stones and their names; the held-out corrections baseline |
| R-104 | 6.1 (`fix17cr`), the corrections stone: held-out corrections 192 of 192 on the probe and 159 of 192 on `hard_dev`; what it broke, as 6.11's targets |
| R-105 | 6.11's design, panelled before it trains: 6.1 plus fix C2's 41 answers, one epoch at 1e-4 from 6.1's adapter, with a control; the fresh-seed chain; no 6.111 without a new panel |
| R-106 | 6.11 (`fix17cr11`) and its control: slips 0 everywhere, corrections kept, `hard_dev` above v6; probe recall 190 against v6's 192 fails R-094; the swap, not the extra epoch, removed the slips |
| R-107 | 6.111: one more epoch on 6.11's own set, no data added; 6.2 fixed now as the next try; v6 trained at 91 to 93 so R-094's recall line is read at the same seeds |
| R-108 | 6.111 (`fix17cr111`) fails R-094's recall line on both sets (probe 189, `hard_dev` 153 against v6's 192 and 157); 6.2 (`fix17cs2`) queued as R-107 fixed; the 6.1 and 6.11 fresh-seed pre-training dropped |
| R-109 | 6.2 (`fix17cs2`) passes every registered line at 82 and 83, counts, judged sheets (judge 1) and R-102's bar; judge 2 would fail one sheet; fresh seeds 91 to 93 queued |
| R-110 | 6.21 (`fix17cs21`) designed by a panel at Kevin's word: 6.2 plus 100 train-pool rows whose found line says more than the asked detail, one gentle epoch from 6.2's adapter, with a control; replacement rule proposed for Kevin |
| R-111 | Kevin rules on R-110 rule 3: if 6.2 and 6.21 both pass at 91 to 93, the better one is the base for 7; better is pooled `hard_dev` recall at 91 to 93, with no lead given to 6.2; recorded before any 91-to-93 result of either was read |
| R-112 | 6.2 (`fix17cs2`) at fresh seeds 91 to 93: every counted line passes, but R-076 fails on Sheet B `statement` at seed 92 (42 against base's 46, all three judges); 6.2 is not a base for 7; 6.21 goes to 91 to 93 (R-110 rule 2) |
| R-113 | 6.21 (`fix17cs21`) fails R-094's recall line at 82 and 83 (`hard_dev` 155 against v6's 157); it is not judged or taken to 91 to 93; neither 6.2 nor 6.21 is a base for 7, so a new panel decides the next step (R-111 rule 5) |
| R-114 | A new panel picks one more try: 6.3 (`fix17cs3`), 6.2's rows plus fix 19a's statement and indirect-question pair, trained from scratch; confirmation moves to unread seeds 94 to 96; a fail at any line and v6 ships; an R-113 correction (a second runner) |
| R-115 | The control `fix17cs2x` (6.2 plus one epoch on its own rows), reported only: `hard_dev` recall 160 at 82 and 83, against 6.2's 166 and 6.21's 155; the extra epoch and R-110's rows each cost about half of 6.21's drop |
| R-116 | 6.3 (`fix17cs3`) fails at 82 and 83: probe slips 7 at seed 83 (at most 5), a new "<Name>, who is my <relation>" shape, and probe 51203 `statement` 45 (at least 47); not judged; Kevin rules no more stones on top of earlier versions and that a fail does not end the tries; v6 at 94 to 96 queued |
| R-117 | 6.31 (`fix17cs31`), panelled before it trains: 6.3's rows with the 52 indirect-question answers given the pool's scripted answer and 24 contrast statements (another person forgets or loses something, no search), from scratch; candidate 10 at 82 and 83 since R-093; gates as R-114 items 1 and 2 |
| R-118 | 6.311 (`fix17cs311`, one epoch on top of 6.31) and 6.32 (`fix17cs32`, from scratch), each with 72 new in-view rows answered with the scripted answer; candidates 11 and 12 since R-093; the dilution diagnosis checked and rejected; which copy goes to 94 to 96 fixed before any result |
| R-119 | 6.31 fails at 82 and 83: probe recall pooled 191, one below v6's 192 (R-094); every other counted line passes; its stress lines stop; R-118's two copies go on |
| R-120 | 6.311 fails at 82 and 83: in-view rises (probe 48 and 48, `hard_dev` 42 and 37) but `hard_dev` recall pooled falls to 122 against v6's 157 and 6.31's 163 |
| R-121 | 6.32 fails at 82 and 83: `hard_dev` recall pooled 133 (floor 145, v6 157), probe recall pooled 190, probe slips 6 at 82; both copies with the 72 scripted in-view rows lose found-fact detail, so the rows are the cause |
| R-122 | 6.33 (`fix17cs33`, 6.31 less the 15 memory-word contrast rows), then 6.34 (both removals) or 6.35 (less the 22 "It sounds like" in-view rows), all from scratch, nothing added; candidates 13 and 14 since R-093; pick rule fixed before any result |
| R-123 | 6.33 fails at 82 and 83: probe recall pooled 191, one below v6's 192, on a new question (a search for "sister steps out"); the tattoo miss is gone and every other counted line passes; 6.34 trains as ruled |
| R-124 | 6.36 (`fix17cs36`, 6.31 less the 6 contrast rows whose reply has "Maybe"), trained only if 6.34 fails; chosen after 6.33's result, over 6.35; the stepsister miss is one question, not a pattern |
| R-125 | 6.34 fails at 82 and 83: probe 51203 `statement` 45 (floor 47; it searches "forgot my birthday") and probe recall pooled 191 (a second stepsister query split, on a new question); 6.36 trains as queued |
| R-126 | 6.36 fails at 82 and 83: probe 51203 `statement` 40 (floor 47) and probe recall pooled 191 (the tattoo miss is back); four removal copies, each one probe question short |
| R-127 | 6.37 (`fix17cs37`, 6.31 less the 9 wallet, umbrella and lost-track contrast rows), from scratch; candidate 16 since R-093; the panel's base rate: a copy with no defect misses one probe question in 192 about 28% of the time |
| R-128 | 6.37 passes R-086 (counts and judged sheets, all three judges), R-094 and R-097 at 82 and 83: probe recall pooled 192, `hard_dev` 163, no slips; it is R-122's pick and goes to 94 to 96; R-102 follows its stress runs |
| R-129 | 6.37 passes R-102 at 82 and 83 (held-out corrections 192 and 167 of 192 against v6's 1 and 5; phone typing 176 and 147 against v6's 178 and 132): every registered line at 82 and 83 passes; 94 training from 08:45 |
| R-130 | 6.37 at fresh seeds 94 to 96: R-076's rule passes under all three judges; R-094 passes (probe recall 287 against v6's 287, `hard_dev` 247 against 237); R-102's fresh-seed items wait on its stress runs |
| R-131 | 6.37 passes R-102's fresh-seed items at 94 to 96 (held-out corrections 96, 95, 93 and 83, 83, 77 of 96; phone guard held), so R-114 item 2 is met in full: 6.37 seed 82 replaces v6 and is the base for 7; R-130's slip counts corrected to R-094's count, no verdict changes |
| R-132 | Panel on 7: no 7; 6.37 seed 82 ships for the freeze. The one design the data supports (removing the 22 "It sounds like" in-view rows) was already run as 6.34 and lowered `hard_dev` in-view 78 to 69 |
| R-133 | 6.37's battery at 82 and 83: corrections fixed (probe +0, `hard_dev` -1 of 192; v6 -187, -146); a new gap on lower-case typing, facts in view (probe -8, `hard_dev` -5 of 96; v6 -1, -3); Kevin reopens 7 with a panel of experts, two rounds, a chair and a unanimous vote |
| R-134 | Panel of experts (six Opus experts, two rounds, a chair, a unanimous vote): 6.38 (`fix17cs38`) rewrites the final answer of 28 in-view rows that deflect, nothing else; registered before any row is built; candidate 17 since R-093 |
| R-135 | 6.38's set built and frozen (`fix17cs38.jsonl`, sha256 `f4daff77...` after R-136's rebuild): all 28 targets pass every R-134 rule and the blind judge (28 of 28; the 28 old targets, hidden controls, 0 of 28); queued at 82 and 83 |
| R-136 | 6.38's first set had doubled line endings (2,160 lines, 1,066 blank) and failed to load at 82 and 83; rebuilt with the same 28 answers (sha256 `f4daff77...`); a test now reads every training set as the trainer does |
| R-137 | Prompted-baseline control registered before it runs: base with two fixed prompts (A rules; B rules and four made-up worked examples), probe and `hard_dev`, everything else identical; reported, not gated; per-run scores reported beside pooled counts |
| R-138 | Kevin: 6.38 is the last try. Break tests registered before they run: four harder conditions at a new seed (74001) on 6.37, 6.38 and base; a break must be confirmed at 75001 before any targeted fix, which is judged at 75002 on a held-out form where one exists; go/no-go Mon 09:00 |
| R-139 | Rigor additions, registered before any is computed: one primary development comparison (R-016's test) with Holm on a named secondary family; a five-way failure breakdown; recall by distance and crowding; an independent development set written blind to the generator (report only); Kevin's blind check of 50 scored answers |
| R-140 | 6.38 fails R-134 on one line (`hard_dev` recall pooled over 82 and 83: 157 against 6.37's 163) and passes the other sixteen; 6.37 ships; Kevin's last try is spent; the GPU time freed goes to 6.37's missing stress runs at seeds 97 to 99 |
| R-141 | R-139 items 1 to 3: the primary and all eight secondary tests favour 6.37 (Holm); but the 96 recall questions come from only 5 fact templates on probe and 8 on `hard_dev`, so the item-level p-values overstate the evidence; template-resampled intervals still exclude zero; 6.37's main `hard_dev` failure is finding the fact and answering wrong; seed 82 is the lowest of eight seeds there |
| R-142 | R-139 items 4 and 5 set up before any chat is read: the writers' brief and its panel (nine edits taken, one declined), the loader and `--items-dir`, twelve queued runs (base, both R-137 prompts, 6.37 at all eight seeds), and Kevin's 50-line sheet, restratified by model |
| R-143 | The independent set is written and frozen: 40 chats from four blind writers, 240 questions, none dropped by the loader (sha256 `9919a24c...`); writer transcripts audited; the reshaped eval loop shown to build the same items as before |
| R-144 | Kevin's blind check of the scorer: 47 of 50 agree (kappa 0.88); the scorer never passed a reply he failed; its strictness can only lower base's `hard_dev` recall, by at most 9 of 96. 6.37's misses: 0 of 23 name a false value; 15 of 23 sit in two fact templates where the answer is in a trailing clause and 6.37 restates the main clause only |
| R-145 | A second, independent marker on R-144's 50 lines: 48 of 50 with the scorer (kappa 0.92), 49 of 50 with Kevin (0.96); both people differ from the scorer on the same two strict-scorer lines, 6 and 29 |
| R-146 | Independent set: 6.37 seed 82 recall 39/120 against base 26/120 (+50%, sign test p = 0.047, chat-resampled gain +2.5 to +19 points); seeds 39 to 57; `confirm` 11/40 against base 15 (it rarely searches a "..., right?" question). R-137: both prompts lower base's recall. R-138: one break, `long` on `hard_dev` (84 to 75 of 96), being confirmed at 75001 |
| R-147 | 6.39 (`fix17cs39`) at Kevin's word, registered before it trains: 6.37's rows plus R-110's 100 rows for the found-but-incomplete answer, from scratch at 82 and 83; every 6.37 gate unchanged, then it must beat 6.37 on `hard_dev` recall at fresh seed 75002; any fail and 6.37 ships |
| R-148 | R-138's confirm seed 75001: the `long` break does not hold (loss 6, rule 8); `askd4` against `d4` meets the rule there (8 lost, 0 gained) after falling one short at 74001; both are the found-but-incomplete failure 6.39 targets |
| R-149 | 6.39 fails at 82 and 83: `hard_dev` recall pooled 147 against 6.37's 163 (and v6's 157); every other line passes; the targeted miss (found, answered without the asked detail) rises from 21 to 33; 6.37 stays frozen |
| R-150 | The 6.4 panel (three Opus lanes, audited): two say no 6.4; the third offers value-first answers at about 15% to pass, the same rate as a copy with no effect; no 6.4; 6.37 is the model the sealed final run will score |
| R-151 | Kevin moves the model freeze to Wed Nov 11 night; a 7 is planned from scratch, its design open to the first independent set's failures, judged on a second independent set written now by four new blind writers; the seed-average idea measured and dropped |
| R-152 | The second independent set is written and frozen: 40 chats from four new blind writers, 240 questions, none dropped (sha256 `3a91c34b...`); writer transcripts audited; it judges 7 (R-151) |
| R-153 | 7 (`fix17cs7`) registered before it trains: 6.37's rows with 140 questions reworded as tag questions (the one change all three panel lanes support), five seeds from scratch; every gate, five-seed lines against 6.37, then a win on the second independent set; the next-exchange hop left for a 7.1 |
| R-154 | The scorer and the judge are frozen with the model: SHA-256 of every scoring file, the sealed pools, the judge's brief and rubric, the human check and the adapter, the judge pinned to `claude-sonnet-5-5`; recall scorer repeats on 1,200 rows; R-128's judges split on 13 of 576 lines; a repeat GPU run queued |
| R-155 | 7 fails R-153 at 82 and 83: probe 51203 recall 92 (at least 94) and probe recall pooled 189 (not below v6's 192); six of its seven probe misses are one probe wording ("drawing a blank on my {relation}'s tattoo") with no search; `hard_dev` recall 166 against 6.37's 163; 6.37 seed 82 stays the shipped model; a grep showed one probe line past line 451 |
| R-156 | 7.1 (`fix17cs71`) registered before it trains: 7 without its 20 `in_view` tag rows, a one-part removal (panel: two lanes for, the against lane for no 7.1 with this as the least bad); R-153's lines plus `confirm` right and searched on the second set; R-155 corrected (the v6 line was not 7's); a repeated GPU run gave identical replies on 240 of 240 |
| R-157 | 7.1 fails at 83 on one line (probe `in_view` 38, at least 41); 6.37 seed 82 ships and no candidate is left before the freeze; "drawing a blank" unsearched on 6 of 14 (7 10, 6.37 1); the second independent set, read as a report: 6.37 seed 82 recall 53 of 120 against base 27 (+96%, p = 0.0001); the gate scripts, queue and panel briefs now in the repo |
| R-158 | 7.1 on the second independent set (report only, registered first): it searches tag questions 40 and 39 of 40 (6.37 12 and 7) and every right answer is found by search (18 and 18; 6.37 6 and 4), but recall is not higher (51 and 52 against 53 and 53): it corrects more false claims (7 and 5 of 20 against 3 and 1) and confirms fewer true ones (11 and 13 against 16 and 16) |
| R-159 | The freeze panel (three Opus lanes, audited): two say freeze 6.37 now; the third would run a 7.2 (7.1 with tag-question searches in the claim's own words) on a new third set, but only if Kevin overrides R-156's reading and the pass rule is rewritten before training; Kevin decides; the prompted-baseline control on the second set registered, report only |
| R-160 | **The model is frozen: 6.37 (`fix17cs37` seed 82)**, on Kevin's word after the panel; `results/freeze/sealed_manifest.json` written at commit 2b04826 and checked; every frozen hash matches R-154's trial manifest; no 7.2; the sealed run waits for Kevin's go |
| R-161 | R-159's prompted-baseline control on the second set (report only): both R-137 prompts lower base's recall (18 and 20 of 120 against 27), as on the first set (19 and 15 against 26); 6.37 seed 82's 53 is above each (sign test p below 0.000001) |
| R-162 | The sealed final run, registered before it runs: R-016 as amended (R-038, R-039, R-041), four conditions, base and all eight 6.37 seeds (Kevin: "All eight seeds", a disclosed change from R-016's three); item seed 90311; the coherence sample and the sheets fixed; seed 82 reported alone as the shipped model |

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

**Build and vetting result.** `brief_chat.jsonl`: all 650 non-statement rows are identical to fix 9's. Brief statement
targets average 12.6 words against 21.3 before (spares), and 20 of 150 brief replies use a curly apostrophe (none
before). Vetting (fresh Sonnet judge, `results/coherence/R-060/`): of the 150 targets, 138 coherent and 12 not; of the
spares, 137 and 13. The 12 were swapped. Reasons given: "Enjoy the party, {person}" addressed to the inviter, "great
that you're catching up" to "haven't seen my uncle in ages", unrelated replies, and odd fits ("That sounds like a bad
day" to "guess who ran into {person}").

## R-061 · 2026-11-04 · SPRINT · Fix 11 passes all seven of R-060's items: **v5**

Probe seed 73157, `probe12_tuned8x`, seeds 82, 83, 84 (queue finished 13:33). Seed 82's screen on 51203
(`screen_fix11_all_82`): recall 95 of 96, `statement` 48; it passed R-055's gate.

| Measure | Seed 82 | 83 | 84 | Pooled | v4 pooled | Fix 10 pooled (R-059) | Rule |
|---|---|---|---|---|---|---|---|
| Recall (`older` + `confirm`) | 96 | 92 | 91 | **279 of 288** | 252 | 282 | above 252: pass |
| `in_view` | 43 | 44 | 43 | **130 of 144** | 115 | 124 | at least 110: pass |
| `statement` | 48 | 48 | 48 | **144 of 144** | 143 | 144 | at least 136: pass |
| Right decisions (of 240) | 240 | 240 | 240 | | 236, 229, 226 | 240 each | at least 200: pass |
| False retrieval | 1 | 0 | 1 | **2 of 720** | 8 | 3 | at most 39: pass |

Paired against v4, pooled: recall 35 and 8 (p < 0.0001), all kinds 58 and 14 (p < 0.0001). Against fix 10: recall 5
and 8, all kinds 17 and 13 (p = 0.58 both): no difference in correctness. Base has recall 30 of 96, so v5's 93 a seed
is 210% above base.

Coherence, six fresh Sonnet judges, one a sheet, rubric and sheet only, each seed's sheets judged while the next seed
trained (`results/coherence/R-061/`, `R-061B/`). Shuffle seeds: Sheet B 90459, 90461, 90463; Sheet A 90460, 90462,
90464.

| Sheet | Kind | Base (seed 82, 83, 84 sheets) | v5, seed 82 | 83 | 84 | Pooled base | Pooled v5 |
|---|---|---|---|---|---|---|---|
| A | `older` | 32, 31, 32 | 44 | 44 | 41 | 95 | 129 |
| A | `confirm` | 47, 47, 47 | 48 | 48 | 48 | 141 | 144 |
| B | `in_view` | 33, 32, 34 | 37 | 44 | 38 | 99 | 119 |
| B | `statement` | 46, 44, 45 | 47 | 48 | 47 | 135 | 142 |

**All seven items pass: fix 11 replaces v4 as v5** (adapters `adapters/screens/fix11_all_82`, `_83`, `_84`; data
`data/screens/vetted_brief.jsonl`; rank 32 on attention and MLP, 3e-4, 3 epochs). Its two incoherent `statement`
replies: "Hope my barber settles down soon." to "my barber texted me out of nowhere" (an acknowledgement copied from
the small talk, in the wrong voice) and "It sounds like you're feeling a bit down" to "i should really call my
teammate".

Base's `statement` score moved between sheets this time (46, 44, 45) where it held at 46 in R-059: one or two lines of
judge disagreement on the same replies. v5's margin over base is one to four lines a seed, so the result rests on
each seed's comparison as the rule asks, and pooled it is 142 against 135.

Next: the write-up moves to v5 (article, figures, AuditKIT run, throughput), then the question of what is left to fix.

## R-062 · 2026-11-04 · SPRINT · Fix 12: brief, vetted `in_view` targets spliced into v5's set; rule written before the build

**Why.** On v5's Sheet B, `in_view` is the kind with the most incoherent replies (119 of 144 coherent; base 99). The
judges' main reason, on every sheet since R-055, is "drawing a blank on my {relation}'s tattoo" read as wordplay, a
drawing request or disappointment. `in_view` targets are base's own replies (or its hinted replies), unvetted and
unshortened, as the statement targets were before fixes 10 and 11.

**Fix 12** (code `f59895c`). `--brief-in-view` asks base for brief `in_view` replies, plain and hinted; the
instruction is not part of the row. 150 `in_view` rows (seed 71121) and 150 spares (seed 71122) are built alone
(`--kinds in_view`, v5's other flags), vetted on one blind sheet (shuffle seed 90465, a fresh Sonnet judge), and the
vetted rows replace the `in_view` rows of v5's set (`vet_statement_targets.py apply --kind in_view --into
data/screens/vetted_brief.jsonl`), so every other row is v5's: `data/screens/vetted_view.jsonl`.

**Gate and rule, written before the build.** Labels `screen_fix12_all_82` and `probe13_tuned8x`, adapters
`adapters/screens/fix12_all_8x`, v5's training settings. R-055's screen gate at seed 82. Then R-052's seven items
against base, unchanged, with Sheet B on every seed, and two items against v5: (8) Sheet B `in_view` pooled coherent
above v5's 119 of 144, since that is what it is for; (9) recall pooled at least 273 of 288 (v5's 279 less 6). It
replaces v5 (as v6) only if all nine pass. No held-out or independent run without Kevin.

**Build and vetting result.** 150 `in_view` rows and 150 spares, each 75 base replies and 75 hinted replies (as v5's
set). Brief targets average 13.6 words against 21.8 in v5's set. Vetting (fresh Sonnet judge, `results/coherence/R-062/`):
of the 150 targets, 125 coherent and 25 not; of the spares, 125 and 25. The 25 were swapped and the vetted rows
spliced into v5's set: all 650 other rows are v5's, in v5's order. The judge's reasons: a reply that says it is not
sure of a fact the friend just stated (the scorer passes these because the value is named), the friend's relative
spoken of as the reply's own, "lost" read as the friend losing it, the wrong relation, and filler.

## R-063 · 2026-11-04 · SPRINT · Fix 12 fails R-055's screen gate (recall 90 of 96): dropped; where v5's last misses are

`screen_fix12_all_82` (probe seed 51203, queue stopped at the gate at 14:48): recall 90 (`older` 42, `confirm` 48),
`in_view` 45, `never_told` 48, `statement` 48. The gate needs recall at least 92, so fix 12 stops here and seeds 83
and 84 are not trained. `in_view` rose against v5's screen (45 against 42), but five of its six recall misses are
searches that found the fact followed by "I don't have that from you"; v5's screen had one recall miss in all. Brief
`in_view` answers appear to have moved the model toward declining.

**v5's misses on the confirmation probe** (`probe12_tuned8x`, 720 replies, 23 wrong):

| Kind | How | Count |
|---|---|---|
| `in_view` | no search, and no answer from the turns in view | 14 |
| `older` | search found the fact, reply denies it or names another value | 5 |
| `confirm` | search found the fact, reply denies it | 4 |
| `never_told` | searched, not found, reply named a value | 2 |

Twelve of the 14 `in_view` misses are indirect wordings ("drawing a blank on my {relation}'s tattoo", "i cannot think
what my {relation} grows", "i'm blanking on what my {relation} is scared of"): the reply treats them as feelings
("It sounds like you're trying to remember something...") and asks for a hint.

**Fix 13, `--in-view-indirect 0.5`.** In v5's set, an `in_view` row's question takes the indirect form one time in
three (`ASK_FORMS`). Fix 13 forces it on half the rows, so with the third of the rest it is two in three, drawing the indirect wording from the train pool and
`MORE_INDIRECT` as before; the probe's wordings stay out (the four-word test in `test_train_phrasings.py`). 150
`in_view` rows are built alone (seed 71123) and spliced into v5's set in place of its `in_view` rows; every other row
is v5's: `data/screens/indirect_view.jsonl`. No vetting, so the one change is the share of indirect questions.

**Gate and rule, written before the build.** Labels `screen_fix13_all_82` and `probe14_tuned8x`, v5's settings.
R-055's screen gate, plus `in_view` on the screen at least v5's 42. Then R-062's nine items (R-052's seven against
base, Sheet B on every seed; `in_view` coherent pooled above v5's 119 of 144; recall pooled at least 273). It
replaces v5 (as v6) only if all pass.

## R-064 · 2026-11-04 · SPRINT · Fix 13 fails R-055's screen gate (recall 91 of 96): dropped; changing `in_view` rows trades `in_view` for `older`

`screen_fix13_all_82` (probe seed 51203, gate at 15:47): recall 91 (`older` 43, `confirm` 48), `in_view` 45, `never_told`
48, `statement` 48. The gate needs recall at least 92, so seeds 83 and 84 are not trained.

| Screen (seed 82) | Recall | `older` | `in_view` | `statement` |
|---|---|---|---|---|
| v5 (`screen_fix11_all_82`) | 95 | 48 | 42 | 48 |
| Fix 12, brief vetted `in_view` (R-063) | 90 | 42 | 45 | 48 |
| Fix 13, two in three `in_view` indirect | 91 | 43 | 45 | 48 |

Both changes to the `in_view` rows gained three `in_view` answers and lost five or six `older` ones, and four of the
lost questions are the same in both ("what tattoo did Dmitri get", "which club did Ayaan join", "which club did Gustav
join", "where does my tutor go after work these days"): each search found the fact and the reply denied it ("I don't
have that from you") or said it was not in the results. v5 answered all four. On this screen, more confident reading
of the turns in view comes with less trust in a search result.

The build step of this queue also retried once on a dirty tree (an article commit of mine at 14:50); the retry
worked as the retry steps intended (R-072 records why they exist).

**Where this leaves the work.** Fixes 12 and 13, the two aimed at v5's largest remaining group of misses, both lose
more than they gain. v5's misses are 23 of 720 replies on the confirmation probe (3%), and its single-seed screen is
95 of 96 on recall. A further fix would chase a handful of questions on a probe that has guided every change, which
the sealed pools would not reward. v5 stands as the candidate for the registered final test.

## R-065 · 2026-11-04 · SPRINT · v5 in the crowded condition (four decoys), development: recall 277 of 288, no false retrieval

Development only, probe seed 73157, the same conversations as R-061 with four decoys a chat (`--decoys 4`, labels
`probe_d4_v5_8x`, adapters `adapters/v5_seed_8x`), beside R-045's base and v4 runs. Kevin questioned R-064's "final
candidate": the plateau there was measured only in the one-decoy condition, and the final test is harder.

| Probe seed 73157 | Base, 1 decoy | Base, 4 | v4, 1 (3 seeds) | v4, 4 | v5, 1 (3 seeds) | v5, 4 |
|---|---|---|---|---|---|---|
| `older` + `confirm` correct | 30 of 96 | 27 | 252 of 288 | 245 | 279 of 288 | **277** |
| of which retrieved | 30 | 27 | 251 | 245 | 279 | 277 |
| wrong although retrieved | 4 | 7 | 11 | 17 | 9 | 11 |
| `in_view` | 34 of 48 | 33 | 115 of 144 | 114 | 130 of 144 | 130 |
| `never_told` | 42 | 41 | 141 | 139 | 142 | 144 |
| False retrieval, all replies | 13 of 240 | 19 | 8 of 720 | 22 | 2 of 720 | **0** |
| Right decisions per seed | 119 | 119 | 236, 229, 226 | same | 240 each | 240 each |

Four decoys cost v5 2 of 288 recall answers (v4: 7) and no false retrievals (v4: 22 of 720, base 19 of 240). Every
right answer is retrieved. The crowded condition is not where v5's remaining room is.

**What has not been measured in development: the independent pool's style.** Every probe so far shares the training
pool's author and style. R-039's independent pool was asked for run-on statements with the fact buried mid-sentence,
texting-style questions, `new_words` without the type's keyword, forgetting without the probe's idioms, and values easy
to confuse. Nothing in development tests that. A development twin written by a fresh agent from the same brief would;
that choice is Kevin's, because tuning on it makes the sealed independent pool less independent (same brief, different
content).

## R-066 · 2026-11-04 · SPRINT · A development twin of the independent pool, written by a fresh agent from R-039's brief (Kevin's go)

**Why.** R-065: v5 holds in the crowded condition, and the one part of the final test with no development stand-in is
the independent pool's style. Kevin chose a twin: a pool written by a fresh agent from the same brief, readable and
used for development, so the sealed pool stays sealed.

**Cost, disclosed now.** Tuning against the twin moves the model toward what R-039's brief asks for. The sealed
independent pool came from that brief, so it is less independent of the development work than it was: it still
shares no people, relations, values, subjects, fact types or wording with any other pool (tests), and nobody on the
project has read it, but its style was written to the same instructions. The write-up says so.

**How.** As R-039, in `scratch/.../twin/`: `BRIEF.md` (R-039's brief with the pool name `hard_dev`, the file name, and
a final report that may describe the pool, since it is for development), `avoid.json` built by code from all four
pools, the sealed ones included, never printed, and `check_pool.py` (R-039's checker, plus: no question or statement
wording sharing four words in a row with the held-out or independent pool, reported as pass or fail only). A fresh
agent reads only those three files and runs the checker until it passes. The pool joins as
`src/aya_retrieval/pool_hard_dev.py`, registered as `hard_dev`, not sealed; the pool tests gain it, run with tracebacks
off so a failure names the test, never a sealed value.

**Use.** Base and v5 on `hard_dev` (seed 73157, 24 a kind, one and four decoys), development only. If v5 falls there,
the next fixes are screened on it, with R-055's gate on the probe kept so the probe does not slip.

## R-067 · 2026-11-04 · SPRINT · Harder development tests from LLE's failure categories (categories only, none of its text)

**Why.** Kevin asked for several held-out-style tests to find where the gaps are, and for the categories LLE tracks to
shape them. A read-only agent listed LLE's failure categories in its own general words, quoting no test, name or value
(R-066's rule on LLE stands: none of its code or test sets enters this repository). Of its 14 categories, four fit this
task's five kinds of message: how the real user types; corrections not applied; over-eager corrections (a same-type
fact about someone else replacing the right one, which R-038's crowded condition already tests); and recall across
very long chats. The others (web search, pasted-text injection, restarts, questions about the order of talk) are
outside it.

**`src/aya_retrieval/stress.py`** (tested in `tests/test_stress.py`), applied at evaluation to any pool:

1. **`--user-style`**: every friend line and the final message are typed as the user types, by general traits only:
   all lower case, names included; commas and exclamation marks dropped; contractions without the apostrophe one time
   in three; a final full stop dropped, or an ellipsis one time in six; a question mark kept six times in ten.
2. **`--corrections`**: an `older` or `confirm` fact is restated later, still out of view, with a new value of the
   same type after an opening that says the earlier one was wrong ("scratch what i told you earlier, "). The new value
   is the answer and the old one is forbidden.
3. **`--sizes 1000`**: chats of 1,000 messages.

**Runs, development only** (probe seed 73157, 24 a kind, base and v5's three seeds, labels `st_*`): user style on the
probe and on `hard_dev`, every kind; corrections on the probe and on `hard_dev`, `older` and `confirm`; 1,000-message
chats on the probe, `older`, `confirm` and `never_told`. They decide nothing; they show where v5's gaps are, and the
largest gap is the next fix. Any test here that a fix is aimed at joins the screen gate for that fix.

## R-068 · 2026-11-04 · SPRINT · On `hard_dev`, v5's recall is 172 of 288 (60%) against 279 on the probe: it maps unseen fact types onto the training pool's

Development only, seed 73157, 24 a kind, one decoy (`hd_base`, `hd_v5_8x`).

| | Probe: base | Probe: v5 (3 seeds) | `hard_dev`: base | `hard_dev`: v5 (3 seeds) |
|---|---|---|---|---|
| Recall (`older` + `confirm`) | 30 of 96 | 279 of 288 | 20 of 96 | **172 of 288** |
| `older` / `confirm` | 23 / 7 | 139 / 140 | 8 / 12 | 95 / 77 |
| `in_view` | 34 | 130 | 33 | 112 |
| `never_told` | 42 | 142 | 39 | 141 |
| `statement` | 31 | 144 | 36 | 144 |
| Recall misses: search found the fact / no search | 4 / 59 | 9 / 0 | 31 / 38 | **103** / 5 |
| False retrieval | 13 of 240 | 2 of 720 | 21 of 240 | 10 of 720 |
| Right decisions | 119 | 240 each | 167 | 233, 236, 237 |

v5 is still 187% above base on recall here, decides to search almost every time it should (5 recall questions of
288 without a search) and rarely names another person's fact; but 103 of its 116 recall misses are searches that
brought the fact back. The searches show why: v5 writes the training pool's query phrase for the nearest training fact
type, not words from the question. "where my babysitter came of age" is searched as "babysitter born birthday month";
"that hot drink my vicar lives on" as "vicar street address"; "the weekday my housemate faces the hiring panel" as
"housemate promoted title". The name in the query brings the right passage back, and the reply then denies it (47 of
the 103) or answers the training fact type it searched for ("Your coach, Henrik, was born in November").

The training set has 25 fact types, each with one fixed query phrase, and every training question is answerable by
one of them. v5 has learned those types and phrases, not how to search for and read an unfamiliar fact. The probe hid
this because its fact types were written by the same author in the same mould. This is the largest gap found so far,
and the sealed independent pool, written to the same brief as `hard_dev`, is likely to show it.

## R-069 · 2026-11-04 · SPRINT · Fix 14: a wide training pool of new fact types, written by a fresh agent (Kevin's go); rule written before it exists

**Why.** R-068: v5 searches unfamiliar fact types with the training pool's fixed query phrases. The training pool has
25 fact types; v5 learned them rather than how to search for and read a fact of any type.

**The pool.** A fresh agent writes `wide`, a training pool of at least 40 new fact types, from a brief that asks for
breadth (many areas of life, unusual types), chatty statements with the fact mid-sentence, varied question wordings,
and values that are easy to confuse within a type. It reads only its brief, an avoid-list built by code from all five
pools (sealed ones included, never printed) and a checker: R-066's, plus no fact-type name, value, person, relation or
subject shared with any pool, and no question or statement wording sharing four words in a row with the probe, the
held-out, the independent or `hard_dev` pool (pass or fail only). It joins as `src/aya_retrieval/pool_wide.py`, used
only for training. Disclosure: the brief asks for the same kind of hardness as R-039's, so training moves toward the
style the sealed independent pool was written in, with none of its content.

**Fix 14.** The fact rows of v5's set (`older`, `confirm`, `in_view`, `never_told`) are rebuilt with v5's flags, each
row from `wide` with probability one half and otherwise from `train` (`--wide-share 0.5`, `--kinds older confirm
in_view never_told`), and spliced into v5's set in place of its fact rows; v5's 150 vetted brief `statement` rows stay.
Same counts per kind, same settings (rank 32, attention and MLP, 3e-4, 3 epochs).

**Gate, at seed 82.** On the probe (51203), R-055's gate (recall at least 92 of 96, `statement` at least 47). On
`hard_dev` (73157, 24 a kind), recall above v5's seed-82 result of 58 of 96 by at least 10.

**Rule, three seeds.** R-052's seven items on the probe (73157) against base, Sheet B on every seed, unchanged; recall
on the probe pooled at least 273 of 288 (v5's 279 less 6); and on `hard_dev`: recall pooled at least 202 of 288 (v5's
172 plus 30), false retrieval pooled at most v5's 10 of 720 plus 10, and Sheet B `statement` and `in_view` pooled
coherent at or above base's `three_exchanges` replies (one sheet a seed). It replaces v5 (as v6) only if all pass.
Labels: `screen_fix14_all_82`, `hd_fix14_82`, `probe15_tuned8x`, `hd_fix14_8x`; adapters
`adapters/screens/fix14_all_8x`. No held-out or independent run without Kevin.

## R-070 · 2026-11-04 · SPRINT · The first wide pool is discarded: its writer saw fragments of sealed wording; the checker now names only the writer's own lines

The first fresh agent to write `wide` (R-069) passed the checker and reported "a temporary debug copy of the checker's
two checks" used to find which of its lines clashed. Its transcript shows a script that imported the project's pools
(sealed ones included) and printed every four-word run its lines shared with them: up to 46 short fragments of other
pools' wording, some from the held-out and independent pools. It also read the pools in code, against the brief.
The cause is the checker R-066 and R-069 wrote: it reported only a count of clashing lines, so a writer had to find
them some other way. The pool would have been training data, so it was deleted unused (with the agent's scratch
folder); nothing from it entered the repository.

`hard_dev`'s writer was checked the same way: it read only its brief, avoid-list and checker, and ran no code reading
the project, so `hard_dev` stands.

**Fix.** The wide checker now names the writer's own line that clashes ("reword (shares four words in a row with
another pool): <the writer's line>"), never the other pool's wording, so there is nothing to look for elsewhere; and
the brief forbids running any code but the checker or importing the project's modules. A second fresh agent writes
`wide` with these; its transcript is checked the same way before the pool is used.

**Docs.** The article gains the development checks beyond the probe (section 5), their results (R-065, R-068) in
section 6 and the abstract, and this incident and the shared brief under threats to validity; the README describes
the current project, the pools and the stress tests.

**Order of runs (R-067 to R-070).** R-067's stress runs had not started (their queue was waiting for the `hard_dev`
runs) and were stopped at 18:27 so fix 14 runs first: it targets the largest gap found, and the stress tests are
better spent on whichever adapter is current after it. The second `wide` pool (47 fact types, 8 values each, 33
people, 50 subjects) was written by a fresh agent under R-070's checker; its transcript shows it read only its three
files, edited only its pool, and ran only the checker. It joins as `src/aya_retrieval/pool_wide.py`, with a test that
it shares no four-word wording with any test pool. Fix 14 builds its fact rows at seed 71124.

**`hard_dev` with four decoys** (`hd_d4_base`, `hd_d4_v5_8x`, finished 18:31): v5's recall is 177 of 288 (one decoy:
172), base's 20 of 96 (20); false retrieval v5 9 of 720, base 26 of 240. More decoys cost v5 nothing here; R-068's gap
is the unfamiliar fact types, not the crowding (98 of its 111 recall misses are found-but-wrong).

## R-071 · 2026-11-04 · SPRINT · Fix 14 lifts `hard_dev` recall from 58 to 76 at seed 82 but fails the gate on statements; fixes 14b and 14c

Seed 82, gate at 19:31 (`screen_fix14_all_82` on the probe, 51203; `hd_fix14_82` on `hard_dev`, 73157):

| Seed 82 | Recall | `older` | `confirm` | `in_view` | `never_told` | `statement` | Decisions | False retrieval |
|---|---|---|---|---|---|---|---|---|
| Probe: v5 | 95 | 48 | 47 | 42 | 48 | 48 | 240 | 0 |
| Probe: fix 14 | 92 | 47 | 45 | 47 | 46 | **44** | 236 | 2 |
| `hard_dev`: v5 | 58 | 33 | 25 | 36 | 47 | 48 | 233 | 4 |
| `hard_dev`: fix 14 | **76** | 42 | 34 | 40 | **36** | 45 | 236 | 13 |

`hard_dev` recall rises 31% (58 to 76; gate 68) and `in_view` rises on both pools, so training on 47 new fact types
does teach the model to search for and read unfamiliar facts. Probe recall holds at the gate's floor (92). But
`statement` is 44 (gate 47): "i should really call my mentor" is searched as "mentor phone number", "my barber
texted me out of nowhere" gets a stored fact. And `hard_dev` `never_told` falls from 47 to 36: asked what someone
studied, never said, the search returns another person's degree and the reply states it as theirs ("Isolde finished
a course in philosophy"); false retrieval rises from 4 to 13. **Fix 14 is not confirmed.** Its statement rows were
v5's: no `wide` person, relation or topic ever appears in a training line that needs no search, so every `wide` name
in training meant a lookup.

**Fix 14b.** Fix 14's fact rows, and `statement` rows also drawn half from `wide` (its people, relations and chat
lines, plus `MORE_CHAT`), brief and vetted as R-058 and R-060: 150 rows (seed 71125) and 150 spares (seed 71126),
`--kinds statement --wide-share 0.5 --brief-chat --more-chat`, one blind sheet (shuffle seed 90466), a fresh Sonnet
judge, spliced into `wide_mix.jsonl` in place of its `statement` rows: `data/screens/wide_mix_b.jsonl`.

**Fix 14c.** Fix 14 at a quarter share (`--wide-share 0.25`, fact rows built at seed 71124, spliced into v5's set):
`data/screens/wide_mix_c.jsonl`. A smaller dose of the same change.

**Gate for both, at seed 82, written before either is built:** R-069's (probe recall at least 92, probe `statement`
at least 47, `hard_dev` recall at least 68), plus `hard_dev` `never_told` at least 44 (v5's 47 less 3). The confirmation
rule is R-069's, with `hard_dev` `never_told` pooled at least 132 of 144 (v5's 141 less 9) added. Labels
`screen_fix14b_all_82` / `hd_fix14b_82` and `screen_fix14c_all_82` / `hd_fix14c_82`.

## R-072 · 2026-11-04 · SPRINT · Operational errors not recorded when they happened, and their fixes

Four faults in how runs were queued were fixed at the time but not written here; the write-up's errors section cites
this record for them.

1. **Records racing the queue (2026-11-04, about 02:38).** An R-053 records edit, left uncommitted by a lint failure,
   landed between a queued confirmation's clean-tree check and the evaluation's own check; the evaluation refused to
   run ("NO RESULTS seed 82"), the queue stopped, and the next queue started early. Since then every queued step waits
   for a clean tree before it starts and retries up to three times if its output is missing.
2. **Untracked files and the clean-tree check (R-060's queue).** The queue's wait counted untracked files, which the
   repository's `require_clean_tree` ignores, so a freshly built data file would have held the queue for ever. The
   wait now ignores untracked files too (`git status --untracked-files=no`); it was caught before it cost a run.
3. **A quoting bug (R-063's queue, 15:05).** The step that spliced fix 13's rows into v5's set was written as
   Python inside the shell script and broke on its string quoting ("NO SPLICE"). The built rows were sound; the
   splice was run by hand from its own script file and the queue restarted at training. Splice and gate steps now
   live in their own script files.
4. **A stalled push (18:58).** A push to GitHub hung in `send-pack` for about ten minutes. It was stopped and retried
   successfully. A push inside a queue's `&&` chain would hold the GPU the same way, so queues now run
   `timeout 120 git push -q || echo "push failed, continuing"`.

**Fix 14b data.** `wide_chat.jsonl` (seed 71125) and its spares (71126): 81 of the 150 statement lines name a `wide`
person or relation. Vetting (fresh Sonnet judge, `results/coherence/R-071/`): targets 139 coherent and 11 not, spares
139 and 11; the 11 were swapped, and the vetted rows spliced into `wide_mix.jsonl` in place of its statement rows.
All 650 fact rows are fix 14's: `data/screens/wide_mix_b.jsonl`.

## R-073 · 2026-11-04 · SPRINT · Fix 14c fails on `hard_dev` `never_told`: wide training makes the model state another person's fact; three sets had over-long rows; fix 15

**Fix 14c at seed 82** (`data/screens/wide_mix_c.jsonl`, fact rows a quarter from `wide`, v5's statement rows;
trained 1,648 s, peak 7.83 GiB). Labels `screen_fix14c_all_82` and `hd_fix14c_all_82` (R-071 named the second
`hd_fix14c_82`; the queue's label carries `_all`, as the gate reads it).

| Label | Probe recall (of 96) | Probe `statement` (of 48) | `hard_dev` recall (of 96) | `hard_dev` `never_told` (of 48) | `hard_dev` false retrieval (of 240) |
|---|---|---|---|---|---|
| base (`hd_base`, tool loop) | | | 20 | 39 | 21 |
| v5 (`screen_fix11_all_82`, `hd_v5_82`) | 95 | 48 | 58 | 47 | 4 |
| fix 14 (R-071) | 92 | 44 | 76 | 36 | 13 (12 `never_told`) |
| fix 14c | 93 | 47 | 79 | 32 | 16 (all `never_told`) |

Gate (R-071): probe recall 93 (92), statement 47 (47), `hard_dev` recall 79 (68), `never_told` 32 (44): **fail**.
Probe false retrieval is 0. On `hard_dev`, recall is 36% above v5's but false retrieval is four times v5's.

**What the 16 `never_told` misses are.** Every one states the decoy's value: the same fact about another person in the
chat, given as the answer ("i wonder if you got told what my sponsor spent three years on at uni" gets "Lorcan
finished a course in astronomy", from "Lorcan (my plumber) rang mid-match ..."). Nine are `hard_dev`'s degree type,
five its housewarming gift. When the search returned passages, v5 answered `never_told` right 22 times of 23; fix 14c
17 of 33. The wide-trained model finds more and checks less whose fact it found.

**A cause considered and dropped.** The `wide` pool names the person as "my {relation} {person}" in 41 of 47 facts,
the train pool in 13 of 35, and the degree type uses "{person} (my {relation})". A build option to vary that form
was written and not used: a fresh Sonnet reviewer, asked to argue against it, pointed out that the gift type shares its
form with the hometown type, which had no such misses, and the rebuilt misses include decoys in the plain form. The
misses follow the person, not the form.

**Over-long rows (data defect).** `run_build_training_set.py` wrote its output before its 1,024-token check, and the
queue took a non-empty file as success. Training cuts rows at 1,024 tokens, so these rows lost the end of their
answer: fix 14's set and 14b's (which keeps 14's fact rows) 5 rows (`older_0028`, `older_0052`, `older_0150`,
`confirm_0148`, `never_told_0103`; 1,032 to 1,066 tokens), 14c's 3. Five rows of 800 cannot explain a gap of 12 on
`never_told`, but the three screens stand as screens of those sets only. Commit `1b184b3`: the build now skips a row
over the limit (tallied as `{kind}_too_long`) and checks before writing; queues take the provenance file as
success. Earlier builds had no over-long row, so they rebuild unchanged. The as-trained sets of fixes 14 and 14c are
committed without provenance files, since their builds stopped at the check.

**Fix 14b** (`data/screens/wide_mix_b.jsonl`: fix 14's fact rows, statement rows half from `wide`, vetted; labels
`screen_fix14b_all_82`, `hd_fix14b_all_82`): probe recall 92 (92), statement 48 (47), `hard_dev` recall 74 (68),
`never_told` 32 (44): **fail**. False retrieval: probe 5 (4 `never_told`), `hard_dev` 17 (16 `never_told`). The plain-chat
change works: statements go from fix 14's 44 to 48 of 48, so the wide pool's people in chat lines end the "mentor phone
number" searches. The fact rows, unchanged from fix 14, keep the `never_told` failure. If fix 15 mends `never_told`,
its statement rows are the next thing to swap for 14b's.

**Fix 15.** 14c's settings with `never_told` rows raised from 150 to 250, each kept only if its search returns
passages, all about someone else (`--never-told-hits`, R-050), built at seed 71124 with the fixed build; v5's 150
statement rows; 900 rows (`data/screens/wide_mix_15.jsonl`). R-054 found `--never-told-hits` brought `never_told` part
of the way back when the cause was searching in the friend's words; here the misses come from reading, and more rows
that show a same-type fact about someone else are the direct remedy. Same gate, label `fix15_all`, plus `hard_dev`
false retrieval reported against v5's 4.

## R-074 · 2026-11-04 · SPRINT · Fix 15 passes its gate; confirmation rule written before seeds 83 and 84 exist

**Fix 15 at seed 82** (`data/screens/wide_mix_15.jsonl`, 900 rows; trained from 21:43; labels `screen_fix15_all_82`,
`hd_fix15_all_82`).

| Label | Probe recall (of 96) | Probe `statement` (of 48) | `hard_dev` recall (of 96) | `hard_dev` `never_told` (of 48) | `hard_dev` `statement` | `hard_dev` false retrieval (of 240) |
|---|---|---|---|---|---|---|
| v5 | 95 | 48 | 58 | 47 | 48 | 4 |
| fix 14c | 93 | 47 | 79 | 32 | 46 | 16 |
| fix 15 | 96 | 48 | 81 | 46 | 48 | 3 |

Gate (R-071): probe recall 96 (92), statement 48 (47), `hard_dev` recall 81 (68), `never_told` 46 (44): **pass**.
Probe false retrieval 0. On `hard_dev`, recall is 40% above v5's at this seed, with false retrieval 3 against v5's 4.
The 100 extra `never_told` rows, each showing a same-type fact about someone else, undo what the wide rows did to
`never_told` (32 to 46) and lose no recall (79 to 81). Fix 15b (R-073's next step, 14b's statement rows) is not run:
fix 15's statements are already 48 of 48 on both pools.

**Confirmation rule, written before seeds 83 and 84 are trained and before any of fix 15's coherence sheets.** R-069's
rule with R-071's addition, unchanged, for this setting: seeds 82 (`adapters/screens/fix15_all_82`), 83 and 84,
trained on `data/screens/wide_mix_15.jsonl` with `--lora-r 32 --lora-targets q_proj k_proj v_proj o_proj gate_proj
up_proj down_proj --learning-rate 3e-4`, scored on probe seed 73157 as `probe13_tuned8x` and on `hard_dev` seed 73157
as `hd_fix15_all_8x` (seed 82's `hard_dev` run is the screen's: same adapter, pool, seed and items). It replaces v5
(as v6) only if all of these pass:

1. On the probe, against base (`probe2_base`), R-052's seven items: recall pooled above 252 of 288; `in_view` pooled
   at least 110 of 144; `statement` pooled at least 136 of 144; right decisions at least 200 of 240 on every seed;
   false retrieval pooled at most 39 of 720; Sheet A, pooled `confirm` and pooled `older` plus `confirm` coherent at
   or above base; Sheet B on every seed, `statement` and `in_view` coherent each at or above base.
2. Probe recall pooled at least 273 of 288.
3. `hard_dev` recall pooled at least 202 of 288.
4. `hard_dev` false retrieval pooled at most 20 of 720.
5. `hard_dev` `never_told` pooled at least 132 of 144.
6. `hard_dev` Sheet B (against `hd_base`'s `three_exchanges` replies, one sheet a seed), `statement` and `in_view`
   pooled coherent at or above base.

Fresh Sonnet judges, one a sheet, rubric and sheet only; shuffle seeds from 90467. No held-out or independent run
without Kevin. After the confirmation's runs, the queue runs R-067's stress tests on base and v5 seed 82 (and on the
new version if it passes), then the demo transcripts.

## R-075 · 2026-11-04 · SPRINT · Fix 15 fails R-074 at seed 83's Sheet B: v5 stands; fix 15b, rule written before it exists

**Fix 15's confirmation so far** (probe seed 73157, `probe13_tuned8x`; `hard_dev` seed 73157, `hd_fix15_all_8x`;
seed 84 training at the time of writing). Coherence: one fresh Sonnet judge a sheet, rubric and sheet only, each
transcript checked (each read only its rubric and sheet and wrote its marks from a list it typed); shuffle seeds 90467
to 90472; `results/coherence/R-075/`, `R-075B/`, `R-075H/`; `scripts/records/rule_r074.py` computes every item.

| Measure | Seed 82 | Seed 83 |
|---|---|---|
| Probe recall (of 96) | 94 | 95 |
| Probe `in_view`, `statement`, `never_told` (of 48) | 42, 48, 48 | 45, 48, 48 |
| Probe right decisions (of 240), false retrieval | 240, 0 | 240, 0 |
| `hard_dev` recall (of 96), `never_told` (of 48) | 81, 46 | 81, 44 |
| Sheet A `older` / `confirm` coherent, base and fix 15 | 31 / 48, 36 / 48 | 33 / 47, 36 / 47 |
| Sheet B `statement` / `in_view`, base and fix 15 | 46 / 33, **46** / 38 | 46 / 31, **43** / 35 |
| `hard_dev` Sheet B `statement` / `in_view`, base and fix 15 | 42 / 30, 45 / 39 | 41 / 31, 41 / 42 |

**Item 1(g) fails at seed 83:** `statement` coherent 43 of 48 against base's 46. R-074 asks for at or above base on
every seed, so fix 15 cannot replace v5 whatever seed 84 shows; **v5 stands**. Seed 84 is still run and judged so the
record is complete.

Four of the five rejected replies answer "i got stuck talking to X for an hour" as if the hour were a pleasure ("That
sounds like a lot of time well spent.", "Hana is a great conversation partner."). v5 gave the same "time well spent"
reply to the same lines at seeds 83 and 84, and R-061's judges marked those coherent, so part of this is judge
disagreement on a borderline reply (R-057). The rule is applied as written. Pooled over the same two seeds, fix 15's
`statement` coherence is 89 of 96 against v5's 95: it misreads the tone of a complaint about a named person more
often, which is the plain-chat side of the wide pool's names.

**Seed 84 and the full rule** (`python scripts/records/rule_r074.py`). Seed 84: probe recall 94, `in_view` 41,
`statement` 48, `never_told` 48; `hard_dev` recall 75, `never_told` 46, `statement` 47. Sheets (base, fix 15): A
`older` 33, 38, `confirm` 48, 46; B `statement` 45, 48, `in_view` 36, 42; `hard_dev` B `statement` 45, 38, `in_view`
29, 38. Shuffle seeds 90473 to 90475; each judge read only its rubric and sheet.

| Item | Result | |
|---|---|---|
| 1(a) to 1(e): recall, `in_view`, `statement`, decisions, false retrieval | 283, 128, 144, 240 each, 0 | pass |
| 1(f) Sheet A pooled `confirm`, `older` + `confirm` | 141 against 143; 251 against 240 | **fail** |
| 1(g) Sheet B every seed | seed 83 `statement` 43 against 46 | **fail** |
| 2 probe recall pooled at least 273 | 283 | pass |
| 3 `hard_dev` recall pooled at least 202 | 237 (v5 172: 38% above) | pass |
| 4 `hard_dev` false retrieval at most 20 | 10 | pass |
| 5 `hard_dev` `never_told` at least 132 | 136 | pass |
| 6 `hard_dev` Sheet B pooled | `statement` 124 against 128; `in_view` 119 against 90 | **fail** |

**Fix 15 fails R-074; v5 stands.** Every count passes and every failure is coherence. The clearest is seed 84's
`hard_dev` plain chat, 38 against base's 45: three replies are "Hm, good question, i'd say it depends", a scripted
small-talk reply from the `wide` pool's history turns, copied word for word; five misread "my plumber has vanished off
somewhere warm till next month" (two as the friend leaving: "Enjoy the warmth and relaxation!"); one answers "next
door are scheming over the hedge" with "That sounds like a lot of noise."; one recites a stored fact on a chat line.
R-076 traces the copied reply to how training computes its loss.

**Fix 15b, and its rule, written before it is built or trained.** Fix 15's fact rows (`data/screens/wide_mix_15.jsonl`)
with fix 14b's 150 vetted statement rows (half drawn from `wide`, so plain-chat lines name the wide pool's people;
R-071, R-073), 900 rows, `data/screens/wide_mix_15b.jsonl`; same settings. 14b alone took statements from 44 to 48
on the screen. Seed 82 is screened on probe 51203 (R-071's gate), `hard_dev` 73157 and probe 73157
(`probe14_tuned82`), and its Sheet B and `hard_dev` Sheet B are judged before seeds 83 and 84 are trained. It replaces
v5 (as v6) only if R-074's rule passes for it unchanged, with labels `probe14_tuned8x` and `hd_fix15b_all_8x`
(`results/coherence/R-076*`). Queued after the stress tests and demo transcripts (R-074's queue).

## R-076 · 2026-11-05 · SPRINT · Every adapter so far learned the whole row, scripted small talk included; fixes 16a and 16b; rule written before they exist

**The finding.** `run_recall_train.py` passes rows as chat `messages` to TRL 1.7.1's `SFTTrainer` with its defaults
(`assistant_only_loss` False; no prompt and completion split), so the loss falls on every token of a row: the system
prompt with the tool description, the friend's lines, the tool's passages, the scripted small-talk replies in view, and
the turns the row is meant to teach. On v5's 800 rows the taught turns are 26,432 of 655,477 tokens (4.0%). Every
adapter in these records was trained this way. It explains the copied replies: "Hm, good question, i'd say it depends"
(R-075, three times at one seed) is a scripted reply in the `wide` pool's history turns, and "Hope my barber settles
down soon" (R-061) is one of the train pool's acknowledgements. In v5's set the five most repeated history replies
occur 118 to 161 times each ("Love that for you." 161), in the assistant's slot; the most repeated taught reply
occurs 16 times. It does not explain everything: "That sounds like a lot of time well spent." (R-075) is in no data file.
A fresh Sonnet reviewer, asked to argue against the fix, agreed with this reading and the limit, and proposed the
second variant below.

**The option** (commit `d42eb93`). `--loss-on` with `all` (TRL's default, unchanged, so earlier runs reproduce),
`demonstrated` (loss only on the assistant turns after the friend's message: each search call and the reply, with their
end-of-turn markers) or `no_history_replies` (every token but the scripted replies in view). The row is tokenized with
the chat template, each turn's span found as what its message adds to the conversation before it, and a check refuses
a template that does not render as a prefix; `tests/test_loss_masks.py` decodes the labelled tokens on Tiny Aya's own
template. The training report records the choice.

**Fix 16a and 16b, one variable each against v5.** v5's data (`data/screens/vetted_brief.jsonl`) and settings (rank 32,
attention and MLP, 3e-4, 3 epochs), with `--loss-on demonstrated` (16a) or `--loss-on no_history_replies` (16b).
Learning rate unchanged for the screen; if 16a passes the counts but replies read stiff or recall drops, 1e-4 is next.

**Gate, at seed 82.** Probe 51203: recall at least 92 of 96 and `statement` at least 47 (R-055). `hard_dev` 73157:
`never_told` at least 44 and false retrieval at most 6 (v5's 4 plus 2). Probe 73157 (`probe15_tuned82`,
`probe16_tuned82`): Sheet B `statement` and `in_view` coherent each at or above base; and `hard_dev` Sheet B
`statement` at or above base. One fresh judge a sheet, shuffle seeds from 90476, `results/coherence/R-077*`.

**Rule, three seeds, for a variant that passes the gate.** R-074's rule with item 3 changed for data that has no `wide`
rows: `hard_dev` recall pooled at least v5's 172 of 288 instead of 202. It replaces v5 (as v6) only if every item
passes. No held-out or independent run without Kevin.

**Demo transcripts** (`results/demo/`, `scripts/run_chat.py`, `demo/chat.txt`; base, v5 seed 82, fix 15 seed 82). Both
adapters search and answer the pottery class (Thursdays) and the move (Halifax), decline the brother's job, and do not
search on "i should really call my mum this weekend"; base says it has no access to personal information. Asked "what
did i fix under the sink", both adapters search "brother new job" again, the query of the question two messages back,
and decline: a new failure, a search built from an earlier message in view. Base invents "a leaky faucet".

**Order.** The stress tests (R-067) were started at 00:23 and are paused after `st_style_probe_v5_82` to run 16a and
16b first; fix 15b (R-075) waits, since a masked loss may change what 15b is for. The remaining stress runs follow.

## R-077 · 2026-11-05 · SPRINT · Fix 16a stops the copying and lifts hard_dev recall, but fails the gate on plain chat; the targets carry the errors; fix 16c

**Fix 16a at seed 82** (v5's data, `--loss-on demonstrated`, trained 00:39 to 01:08; labels `screen_fix16a_82`,
`hd_fix16a_82`, `probe15_tuned82`). Training: at step 50 the loss on the taught turns is 0.72 with gradient norm 1.26,
against fix 15's 0.52 and 0.30 over whole rows.

| Measure | v5, seed 82 | fix 16a, seed 82 | Gate |
|---|---|---|---|
| Probe 51203 recall, `statement` | 95, 48 | 96, 48 | 92, 47: pass |
| `hard_dev` recall (of 96) | 58 | **70** | |
| `hard_dev` `never_told`, `statement`, false retrieval | 47, 48, 4 | 48, 48, 3 | 44, 6: pass |
| Probe 73157 recall, `in_view`, `statement`, `never_told` | 96, 43, 48, 47 | 96, 44, 48, 48 | |
| Replies containing a scripted small-talk line, `hard_dev` (of 240) | 1 | **0** | |

Fix 15 had 7 and 8 such replies at seeds 82 and 84; the count is an exact substring match of each reply against the
127 scripted replies and acknowledgements of the train, probe, `wide` and `hard_dev` pools.

Coherence (fresh Sonnet judges, one a sheet, rubric and sheet only, each transcript checked; shuffle seeds 90476 to
90478; `results/coherence/R-077*`):

| Sheet | Kind | Base | Fix 16a |
|---|---|---|---|
| A | `older` | 31 | **46** |
| A | `confirm` | 47 | 48 |
| B | `statement` | 44 | **40** |
| B | `in_view` | 33 | 37 |
| `hard_dev` B | `statement` | 43 | **41** |
| `hard_dev` B | `in_view` | 33 | 42 |

**Gate: fails** on Sheet B `statement` (40 against 44) and `hard_dev` `statement` (41 against 43). Answers to questions
gain the most on any sheet yet (`older` 46 against 31). The rejected plain-chat replies misread tone or person: "i got
stuck talking to Dmitri for an hour" gets "That sounds like a fun story."; "Hana forgot my birthday again" gets advice
on making it up to her. The plain-chat targets carry the same errors, accepted by the vetting judge: "guess who ran into
Omar at the store" to "That sounds like a fun story. Who did you run into?", "Omar invited me to a party" to "Enjoy the
party, Omar.", "my sister will be staying with me all week" to "Enjoy your stay!". With the loss on the taught turns
only, the adapter copies its targets more closely, faults included. The masked loss removes copying from the history;
it does not mend the targets.

**Fix 16c** (registered in R-076: "if 16a passes the counts but replies read stiff ... 1e-4 is next"). Fix 16a at
learning rate 1e-4: a lighter pull toward the targets. Same gate as R-076, label `probe17_tuned82`, sheets
`results/coherence/R-078*`; R-076's three-seed rule if it passes. Fix 16b (`no_history_replies`) was training at the
time of writing and is scored on the same gate.

**Next, if neither passes: the targets.** The plain-chat targets are vetted by one judge on the general rubric. A
stricter pass for who-is-who and tone, before training, is the next fix; it is planned in its own record before any
target is changed. The stress tests run after 16c.

## R-078 · 2026-11-05 · SPRINT · Fix 17: re-vet the plain-chat targets on a stricter rubric, two judges; plan and rule written before any target changes

**Why.** R-077: the adapter trained with the loss on its targets alone copies them closely, and v5's plain-chat targets
carry the faults the judges reject (a complaint read as good news, the friend called by another person's name, the
friend taken for the one who is visiting). The first vetting (R-060) used the coherence rubric, which does not name
those faults, and one judge.

**The rubric for targets** (`aya_retrieval.vetting.TARGET_RUBRIC`, commit `ec27528`): the coherence rubric's text, plus
"Also mark 0 if it gets the feeling wrong ...; mixes up who is who or who did what ...; asks for something the friend
has just said; or adds a detail that does not fit." It is used only to vet training targets; every evaluation sheet
keeps the coherence rubric. Disclosure, as in R-060: the targets are filtered by the same kind of judge that marks the
evaluation, now with a stricter instruction than that judge gets.

**The data.** v5's 150 plain-chat targets (`data/screens/vetted_brief.jsonl`) and 300 new spares built the same way
(`data/screens/strict_spare_1.jsonl`, seed 71127; `strict_spare_2.jsonl`, seed 71128; R-076's queue builds them) go
on one blind sheet of 450 lines. Two fresh Sonnet judges mark it independently on the target rubric; a line counts as
coherent only if both mark it 1 (`vet_statement_targets.py apply --marks a b`). Each rejected target is swapped for a
spare both accepted, as before; every other row of v5's set is unchanged. Output `data/screens/strict_chat.jsonl`.

**Fix 17.** That set, rank 32, attention and MLP, 3 epochs, with the loss setting of whichever of fix 16a (3e-4) and
fix 16c (1e-4) has more `statement` replies coherent on its seed-82 Sheet B; a tie goes to 16a. Gate, rule and sheets
as R-076 (label `probe18_tuned82`, `results/coherence/R-079*`). Fix 16b is scored on the same gate. No held-out or
independent run without Kevin.

## R-079 · 2026-11-05 · SPRINT · Fixes 16b and 16c fail their gates on counts; the strict vetting; fix 17 runs at 1e-4 by R-078's rule

**Seed 82, against R-076's gate** (probe 51203 recall at least 92 and `statement` at least 47; `hard_dev` `never_told`
at least 44 and false retrieval at most 6):

| Measure | v5 | 16a (3e-4, demonstrated) | 16b (3e-4, no history replies) | 16c (1e-4, demonstrated) |
|---|---|---|---|---|
| Probe 51203 recall, `statement` | 95, 48 | 96, 48 | **87**, 48 | 93, 48 |
| `hard_dev` recall | 58 | 70 | 55 | 48 |
| `hard_dev` `never_told`, false retrieval | 47, 4 | 48, 3 | 48, 1 | **40, 19** |
| Probe 73157 recall, `in_view`, `statement` | 96, 43, 48 | 96, 44, 48 | 87, 42, 48 | 91, 41, 47 |
| Gate on counts | | pass | **fail** (recall) | **fail** (`never_told`, false retrieval) |

16b keeps the loss on the system prompt, the friend's lines and the tool's passages and drops only the scripted replies:
recall falls. 16c, the lighter pull, loses `hard_dev` precision. Neither needs its other sheets judged to fail.

**16c's Sheet B, judged for R-078's choice of loss** (shuffle seed 90480, one fresh judge, transcript checked,
`results/coherence/R-077C/`): base `statement` 46, 16c 46; base `in_view` 35, 16c 37. 16a's was 40 (base 44, on its
own sheet and judge). R-078: fix 17 takes the setting with more `statement` replies coherent on its Sheet B, so **16c's,
1e-4**, though 16c failed its gate on false retrieval; the rule was written before either result and is followed. Base
scored 46 on this sheet and 44 on 16a's: the same replies, two judges, two lines apart.

**The strict vetting** (`results/coherence/R-078/`, shuffle seed 90479). Two fresh Sonnet judges, each with its own
folder, marked the 450-line sheet (v5's 150 plain-chat targets, 300 spares from seeds 71127 and 71128) on the target
rubric; each read only its rubric and sheet. They agreed on 445 lines; judge 1 accepted 383, judge 2 388. Both accepted
135 of v5's 150 targets and 248 of 300 spares. The 15 rejected targets include "Enjoy the party, Omar." (to "Omar
invited me to a party"), "That sounds like a fun story. Who did you run into?" (to "guess who ran into Omar at the
store"), "Enjoy your stay!" (to "my sister will be staying with me all week") and "Good luck with your date with Marc."
(to "Ivan asked me to be their plus one"). Swapped for spares both accepted: `data/screens/strict_chat.jsonl` (commit
`b985f38`), which differs from v5's set in those 15 rows only.

**Fix 17** started training at 03:23 (`--loss-on demonstrated --learning-rate 1e-4`, `strict_chat.jsonl`). Fix 17b,
the same data at 3e-4 (16a's setting), runs after it whatever fix 17 shows: against 16a it changes only the targets,
so it is the one-variable test of the strict vetting. Same gate (R-076), label `probe19_tuned82`, sheets
`results/coherence/R-080*`; R-076's three-seed rule if it passes.

## R-080 · 2026-11-05 · SPRINT · Fix 17 fails on counts at 1e-4; fix 17b, the strict targets at 3e-4, passes the counts; its plain-chat sheets

**Seed 82, against R-076's gate** (probe 51203 recall at least 92 and `statement` at least 47; `hard_dev` `never_told`
at least 44 and false retrieval at most 6):

| Measure | v5 | 16a (v5's targets, 3e-4) | 17 (strict targets, 1e-4) | 17b (strict targets, 3e-4) |
|---|---|---|---|---|
| Probe 51203 recall, `statement` | 95, 48 | 96, 48 | **91**, 48 | 94, 48 |
| `hard_dev` recall | 58 | 70 | 53 | 72 |
| `hard_dev` `never_told`, false retrieval | 47, 4 | 48, 3 | **41, 16** | 46, 4 |
| Probe 73157 recall, `in_view`, `statement` | 96, 43, 48 | 96, 44, 48 | 90, 40, 47 | 94, 43, 48 |
| Gate on counts | | pass | **fail** | pass |

Fix 17 fails as 16c did: the lighter pull at 1e-4 loses recall on the probe and precision on `hard_dev`, so the setting
R-078's rule picked from 16c's sheet is the weak one on counts. 17b differs from 16a in the 15 swapped targets only.
Results: `screen_fix17_82`, `hd_fix17_82`, `probe18_tuned82`, `screen_fix17b_82`, `hd_fix17b_82`, `probe19_tuned82`.

**17b's plain-chat sheets** (one fresh Sonnet judge a sheet, each read only its rubric and sheet, transcripts checked;
replies against base's `three_exchanges` arm):

| Sheet | Shuffle seed | `statement` base, 17b | `in_view` base, 17b |
|---|---|---|---|
| Probe 73157 Sheet B (`results/coherence/R-080B/`) | 90481 | 45, **46** | 35, **40** |
| `hard_dev` Sheet B (`results/coherence/R-080H/`) | 90482 | 42, **44** | 29, **39** |

**17b passes R-076's gate**, the first variant since v5 to do so. With the same loss and learning rate, 16a's
`statement` count on its Sheet B was 40 against base's 44. The 15 replaced targets are the only difference in training.
The sheets and judges differ too: R-079 found the same base replies two lines apart under two judges. So 16a's gap of
four is beyond that spread, and 17b's lead of one is within it.

**Next, under R-076's rule as written** (R-074's items, with `hard_dev` recall pooled at least v5's 172 of 288): seeds 83
and 84 of 17b are trained and scored on probe 73157 (`probe19_tuned83`, `probe19_tuned84`) and `hard_dev`
(`hd_fix17b_83`, `hd_fix17b_84`). Sheets A (all three seeds) and B and `hard_dev` B (seeds 83 and 84) then go to fresh
judges, shuffle seeds from 90483, under `results/coherence/R-081*`. 17b replaces v5 as v6 only if every item passes. The
stress tests (R-067) resume after the seeds, with 17b at seed 82 added to each trio. No held-out or independent run
without Kevin.

## R-081 · 2026-11-05 · SPRINT · The demo's stale search: no training view holds a question; a stress test for a question right after another

**The finding.** In the demo (R-076), "what did i fix under the sink" was searched as "brother new job", the query of the
question just before it, which was still in view. In fix 17b's training set (`data/screens/strict_chat.jsonl`) 16 of
the 2,900 friend lines in view contain a question mark; the three exchanges in view are almost always small talk, and
the evaluation builds its views the same way. So no training row and no test item has an earlier question in view,
though in a real chat one question often follows another.

**The test** (development only, R-067's family). `aya_retrieval.stress.asked_before` and `run_recall_eval.py
--asked-before`: the newest exchange in view (the one before it if the item's fact sits there) becomes a question
about a fact of another type, about a relation and person the conversation never mentions, with a reply that
declines, as the demo's did. Nothing the item is scored on changes; `tests/test_stress.py` checks this on three pools,
every kind, 20 seeds. Runs: probe 73157 and `hard_dev` 73157 on base, v5 seed 82 and fix 17b seed 82, after 17b's
confirmation seeds. A drop against the same model's plain run is the size of the gap; a training fix comes after,
planned before code.

## R-082 · 2026-11-05 · SPRINT · Fix 17b fails R-076's rule on one item by one line; v5 stands; a chat line naming a fact type is read as a question

**Seeds 83 and 84** (`fix17b_83`, `fix17b_84`, trained by queue 60 with seed 82's settings; results `probe19_tuned83`,
`probe19_tuned84`, `hd_fix17b_83`, `hd_fix17b_84`). Six blind sheets, shuffle seeds 90484 to 90489, one fresh Sonnet
judge each; every transcript checked: each judge read only its own rubric and sheet, and its commands only wrote the
marks it listed by hand. Sheets in `results/coherence/R-081` (Sheet A, seeds 82 to 84), `R-081B` and `R-081H` (seeds 83
and 84; seed 82's are R-080's). The folder names were set in R-080 before R-081 became the record of the stress test.

**R-076's rule** (`scripts/records/rule_r080.py`):

| Item | Value | Verdict |
|---|---|---|
| 1a probe recall pooled above 252 | 283 | pass |
| 1b `in_view` pooled at least 110 | 130 | pass |
| 1c `statement` pooled at least 136 | 142 | pass |
| 1d right decisions at least 200 every seed | 240, 239, 239 | pass |
| 1e false retrieval pooled at most 39 | 3 | pass |
| 1f Sheet A `confirm`, and `older` plus `confirm`, at or above base | 144 vs 141; 265 vs 234 | pass |
| 1g Sheet B `statement` and `in_view` at or above base, every seed | `statement` 46 vs 45, **44 vs 45**, 45 vs 45; `in_view` 40 vs 35, 42 vs 33, 43 vs 35 | **fail** |
| 2 probe recall pooled at least 273 | 283 | pass |
| 3 `hard_dev` recall pooled at least 172 (v5's) | 228 | pass |
| 4 `hard_dev` false retrieval pooled at most 20 | 17 | pass |
| 5 `hard_dev` `never_told` pooled at least 132 | 136 | pass |
| 6 `hard_dev` Sheet B `statement` and `in_view` pooled at or above base | 136 vs 129; 119 vs 100 | pass |

**The rule fails, so v5 stands.** The failing item is one line on one sheet; R-079 found two judges two lines apart on
the same replies, so this is within the spread of a single judge, but the rule was written before the result and is
followed. Fix 15 failed the same item at the same seed (R-075). The `hard_dev` false retrieval of 17 is near its limit
of 20: 4 at seed 82, 13 at seeds 83 and 84 together.

**What the marked-down replies show.** 17b's `statement` replies marked 0: at seeds 83 and 84, "Esme forgot my birthday
again" is answered "I don't have that from you. What is it?"; at seed 83, "my mentor texted me out of nowhere" (and the
same line about the barber and the teammate) is answered "That's a bit harsh." and variants. Neither line is in the
training set: no plain-chat target mentions a birthday or "out of nowhere". The first is a new failure of the kind in
R-055: a chat line that names a fact type (a birthday) is taken for a question about it. The second reads a neutral
line as a complaint. Base's marked-down replies are its own known faults (Dmitri as a character in a novel, Gustav as a
storm).

**Next.** Fix 18 starts from 17b's recipe. Its plan, written before code, waits for R-081's test of a question right
after another, so both gaps are planned together.

## R-083 · 2026-11-05 · SPRINT · Fix 18: chat lines that name a fact type in passing, with a control; recipe, review and rule written before the build

**Where the gap came from.** R-082's marked-down replies on the probe (seed 73157) and `hard_dev`: a chat line that
names a fact type is answered as a question about it. Found on development data, so the probe and `hard_dev` are not
clean evidence for this fix; only the sealed pools are, and they wait for Kevin.

**The recipe, fixed before the lines were written** (`aya_retrieval.train_phrasings`, commit with this record):
`MORE_CHAT_FACTS`, three lines for each of the train pool's 25 fact types, one good news, one complaint, one neutral;
each names the type's topic word in passing (dog, car, band, born, class ...), asks nothing, says nothing about
remembering, and states no value of any open pool's facts; `{person}` and `{relation}` about evenly split. No line
restates a probe line's situation (no forgotten birthday, no unexpected text). `MORE_CHAT_PLAIN`, the control: 75
lines with the same moods and split that name no fact topic of the train, probe or `hard_dev` pools. Tests
(`tests/test_train_phrasings.py`) check all of this, and that no line shares four words in a row with the probe,
`hard_dev`, held-out or independent chat lines; that test names only the new line on a clash. Writing them, the check
on values caught three weekday words, which are `hard_dev` values; they were replaced. The builder's `--chat-set
{facts,plain}` makes statement rows take these lines in order, one row a line; the targets are base's brief replies, as
for every plain-chat target since fix 11.

**Review before code.** A fresh Sonnet reviewer, asked to argue against the plan, said go with changes; adopted: the
recipe recorded first; a control; about three lines a type, with results per type; a fresh check set of fact-word chat
lines, written by another author and never trained on, as a gate item; recall must not fall (a model that learned "a
fact word means no search" would lose it); the question-right-after-another fix (R-081) kept apart until its test has
run. Not adopted now: running the sealed pools for 18a, which needs Kevin.

**Builds.** 75 fact rows and 75 control rows (`--kinds statement --chat-set facts|plain --brief-chat`, seed 71129 and
71130), each target vetted by two fresh judges on the target rubric (R-078's method, both must accept); rejected rows
are dropped and counted per fact type. 18a is 17b's 800 rows plus the accepted fact rows; 18c is 17b's 800 plus the
accepted control rows. Same settings as 17b.

**Gate, seed 82, for 18a and 18c alike.** R-076's gate; probe 51203 recall at least 17b's 94 and `hard_dev` recall at
least 17b's 72; and the fresh check set's chat lines judged coherent at or above base. 18a counts as a fix only if it
passes and beats 18c on the check set. **Rule**: R-076's, unchanged, three seeds. No held-out or independent run
without Kevin.

## R-084 · 2026-11-05 · SPRINT · A question right after another (R-081's test): the adapters keep recall, base loses plain chat, fix 17b turns away facts in view after a decline

Probe 73157 and `hard_dev` 73157, `--asked-before`, against the same model's plain run (`st_asked_<pool>_<model>`,
queue 61). Recall is `older` plus `confirm`, of 96; the rest of 48.

| Model, pool | Recall, plain to asked | `in_view` | `never_told` | `statement` |
|---|---|---|---|---|
| Base, probe | 30 to 28 | 34 to 34 | 42 to 42 | **31 to 11** |
| v5 seed 82, probe | 96 to 94 | 43 to 43 | 47 to 48 | 48 to 48 |
| 17b seed 82, probe | 94 to 93 | **43 to 37** | 47 to 48 | 48 to 48 |
| Base, `hard_dev` | 20 to 16 | 33 to 32 | 39 to 38 | **36 to 18** |
| v5 seed 82, `hard_dev` | 58 to 54 | 36 to 36 | 47 to 48 | 48 to 48 |
| 17b seed 82, `hard_dev` | 72 to 69 | **38 to 33** | 46 to 48 | 48 to 48 |

**Reading.** The demo's stale search is not common here: recall falls by one to four answers for both adapters. The
untrained model loses most of its plain chat, so an earlier question in view is a real condition that the adapters
handle and base does not. Fix 17b, alone, turns away facts still in view after a declined question: of its six new
`in_view` misses on the probe, the replies are "You can ask your godfather what he grows." (twice), "You can ask her
directly.", a guess about spiders, and two that talk around the question; four of the six follow an indirect question
("i cannot think what my godfather grows", "i forget which language my barber knows"). v5, trained with the loss on
every token, does not. 17b's loss is on the taught turns only, so the declines it was taught may weigh more against
the turns in view. Training rows with an earlier question in view (the plan's 18b) are aimed at this; they wait for
fix 18a and 18c's results, as R-083 set.

## R-085 · 2026-11-05 · SPRINT · Fix 18a and 18c fail the screen gate on recall; both fix the chat check set, where v5 falls below base

**Screens, seed 82** (queue 62; R-083's gate). Recall is `older` plus `confirm`, of 96; the rest of 48. False
retrieval counted as in R-076.

| Run | Recall | `in_view` | `never_told` | `statement` | False retrieval |
|---|---|---|---|---|---|
| 17b, probe 51203 (`screen_fix17b_82`) | 94 | 44 | 45 | 48 | 4 |
| 18a, probe 51203 | 94 | 41 | 48 | 48 | 1 |
| 18c, probe 51203 | **92** | 43 | 48 | 48 | 0 |
| 17b, `hard_dev` 73157 | 72 | 38 | 46 | 48 | 4 |
| 18a, `hard_dev` 73157 | **56** | 33 | 48 | 48 | 3 |
| 18c, `hard_dev` 73157 | **66** | 36 | 48 | 48 | 1 |
| 18a, probe 73157 | 95 | 41 | 48 | 47 | |
| 18c, probe 73157 | 94 | 41 | 48 | 48 | |

R-083 set probe 51203 recall at least 94 and `hard_dev` recall at least 72. **18a fails on `hard_dev`; 18c fails on
both.** Neither is a fix, and v5 stands. Their Sheet B and `hard_dev` Sheet B were not judged, since the recall items
decide.

**Where 18a lost `hard_dev` recall.** It searched 95 of 96 times and found the fact 88 times, against 17b's 94 and 89,
so the loss is in the reply after the find. Of the 26 answers 17b gave and 18a did not, 15 restate the friend's
situation instead of the fact ("Your coach Rhys got a job interview.", "Your housemate Delphine hosted a dinner.") and
11 decline, several with the fact found. `hard_dev` questions are statements with no question mark that name the topic
("my head has lost what my housemate ladled out for that big dinner"); 18a was taught that a statement naming a topic
gets a brief chat reply. 18c found the fact 80 times: more chat rows of any kind cost recall here, and rows that name a
fact type cost more.

**The chat check set** (`data/check/chat_check.json`, 48 lines written blind by another author and never trained on;
`st_cc_*` runs, probe 73157 conversations with each statement line replaced). One fresh Sonnet judge a sheet, each
read only its rubric and sheet (transcripts checked); tuned `tool_loop` against base `three_exchanges`, the same 48
base replies on every sheet. Shuffle seeds 90491 to 90494; sheets, keys and marks in `results/coherence/R-085C/`.

| Sheet | Base | Adapter | Only base | Only adapter |
|---|---|---|---|---|
| v5 seed 82 | 44 | **36** | 10 | 2 |
| 17b seed 82 | 45 | 44 | 3 | 2 |
| 18a seed 82 | 45 | 48 | 0 | 3 |
| 18c seed 82 | 45 | 47 | 1 | 3 |

Four judges gave the same base replies 44 or 45, so the judge spread here is about one line. **v5, the current model,
is eight lines below base on chat lines that name a fact type.** Of its 12 lines marked down, seven echo the friend's
"my" ("Hope my godfather gets some rest soon.", "That's a small win. my barber sounds good.") and six use one stock
reply, "That sounds annoying. Hope ... settles down soon.", the scripted small talk R-076 traced to the loss on every
token (two lines do both). 17b is one line below base, within that spread. 18a beats 18c by one line, also within it, so the gain on the
check set comes mostly from more vetted chat rows, not from naming the fact type. The check set has now been used to
choose, so it is development data from here on.

**Next.** The trade is chat rows against recall on indirect questions. Fix 19's plan, to be reviewed before any code:
18a's fact-word chat rows, each paired with a training row that asks about the same topic indirectly, as `hard_dev`
does, and is answered from a search, so the rows differ in whether a question is asked, not in the topic word. Same
gate as R-083. The freeze is Tuesday, November 10.

## R-086 · 2026-11-05 · SPRINT · Fix 19: questions asked as statements naming the topic, answered from a search; plan, review and gate written before the build

**Aim.** R-085: chat rows that name a fact type teach "a statement naming a topic gets a chat reply", and `hard_dev`
asks its questions that way. Fix 19 adds the contrast: rows that name the same topic in a statement with no question
mark, asking for the fact, answered from a search. Only whether something is asked separates them from 18a's chat lines.

**Recipe.** 57 `older` rows (`--kinds older --indirect-types ... --more-indirect`, seed 71131), one per fact chat line
in 18a, of the same fact type and in the same order. Each asks in the indirect form, drawn from the template's own
and `MORE_INDIRECT`'s phrasings (train pool only), and the found-fact answer is base's reply to the real search
result (only `confirm` rows get the scripted answer). 17b's set already has 63 indirect `older` rows of 200, so this nearly
doubles them. `build_item` gains `fact_type` (the draw is still made); a test checks that every type, asked this way,
gives one of its indirect phrasings with no question mark. 18a's 57 fact lines cover only the first types in build
order, `animals` to `race`, because R-083's splice kept the first accepted rows; the 57 new rows match them, so
`shop`, `subject` and the other later types get neither. **19a** is 18a's 857 rows plus these 57; **19b** is 18c's
857 plus the same 57. Same training settings as 17b.

**Review before code.** A fresh Sonnet reviewer, asked to argue against the plan, said go with changes. Adopted:
`confirm` rows always use the confirm wording, so forcing the indirect form there does nothing, and the new rows are
`older` only; screen 19a at two seeds with pooled thresholds, since 17b's `hard_dev` recall alone spans 72 to 83
across seeds; 19b runs after 19a, not before; report how many indirect rows 17b already has (above). Raised for Kevin
and not decided here: what is frozen if fix 19 fails, given v5 is below base on the chat check set (R-085); and the go
for the sealed final run.

**Gate, written before the build.** For 19a, seeds 82 and 83: R-076's gate at seed 82; probe 51203 recall at seed 82
at least 94; `hard_dev` recall pooled at least 17b's 145 (72 and 73); probe 73157 recall pooled at least 17b's 189
(94 and 95); the chat check set coherent at or above base, pooled over both seeds. If 19a passes, seed 84 is trained and
R-076's rule decides, unchanged. 19b, seed 82 only, is reported against the same single-seed thresholds and goes
further only if 19a fails the gate and 19b passes it. The check set is development data from R-085 on; only the sealed
pools are clean evidence.

## R-087 · 2026-11-05 · SPRINT · Fix 20 chosen by a three-lane panel before it was written

Kevin, 2026-11-05: "if 19 fails move onto 20", and "i want you to panel before you write the fix also". From here
every fix goes to a panel of several lanes before it is written, and its plan is reviewed before code.

**The draft put to the panel.** Training rows with a declined question in view (R-084's failure: 17b turns away
facts on screen after one), built with the stress test's own `asked_before`. Three fresh Sonnet lanes, each reading
only the draft, these records, the failure modes and the code named; transcripts checked.

- **Against the draft:** it does not touch the item 17b failed (R-076's rule, Sheet B `statement`, a chat line read
  as a question); rows with a decline in view only before a found fact teach "a decline in view means answer", and
  the draft's gate does not look at `statement` or `never_told`; training and test share one function; added rows
  have cost recall every time (R-085). Do it with changes, only if 19a fails.
- **Best fix for the time left:** the live trade is chat lines that name a fact type against recall on indirect
  questions, which decides what ships; the draft's target is outside the rule. If 19a fails: 17b plus half the
  dose of fact-word chat lines, spread over all 25 types (18a's covered only `animals` to `race`), each paired
  with an indirect question of the same type. If 19a passes: spend the GPU on its seed 84 confirmation.
- **Measurement:** the draft's pass would show the template was learned, not the failure fixed; it needs a control,
  a question placed and answered differently as an out-of-template check, guards on `never_told`, `statement` and
  false retrieval, and two seeds. The probe and `hard_dev` have now chosen among fixes 14 to 20 and are development
  evidence only; the write-up says how many candidates were checked on them.

**Ruling.** The lanes agree that fix 20 waits on 19a, and two of three that the asked-before rows need more than
the days left allow to show anything; it stays an open failure mode, with R-084's numbers. Fix 20 is the second
lane's: **17b's 800 rows, plus one vetted fact chat line a type (the first both R-083 judges accepted, 25 lines),
plus one indirect `older` question a type (25 rows, seed 71132, built as in R-086)**, 850 rows, same settings
(`scripts/records/splice_r087.py`). Gate: R-086's, unchanged, at seeds 82 and 83 (`scripts/records/gate_r086.py`
counts the items that need no judge).

**Order on the GPU.** 19a at seeds 82 and 83. If 19a passes `gate_r086.py`, seed 84 is trained and R-076's rule
decides with the judged sheets. If it fails, fix 20 is built and screened at seeds 82 and 83, and seed 84 follows
if it passes. Then 19b at seed 82, then the stress tests. Still open for Kevin: what is frozen on Tuesday if no
candidate passes (R-076's rule as written keeps v5), and the go for the sealed final run.

## R-088 · 2026-11-05 · SPRINT · The compute left, panelled in three rounds to one agreed plan; the candidates list starts

**Why R-087's ruling was replaced.** Its panel was told "about four screens left". Kevin: "you don't understand what 5
days of compute time means.. ?" and "re-panel with the compute limit known"; the panel is there "to help you come up
with the fix", and "once the fixes are proposed you'll run them to the panel again as a 2nd iteration and force
concensus on a plan". Training one candidate normally takes about 30 min (1,632 to 2,077 s for 800 to 900 rows); 17b's
4,475 s run and 19a's first run slowed when part of their GPU memory was moved to system memory, and 19a's was
restarted at step 888. One candidate-seed (training plus four scorings) is about 65 min: about 90 before the freeze.

**The panel.** Four fresh Sonnet lanes, each reading only the brief, these records, the failure modes and the code
named (transcripts checked): fixes for plain chat; fixes for the recall failures; the split of the compute and the
choice of model; and one arguing against the course and what the runner wants to be true. Round 1: each proposed
fixes. Round 2: each read all four and gave the plan it would accept. Round 3: a merged plan, accepted by all four
with three changes, and one seed question settled in a fourth exchange. Briefs and plans in the scratch files
`panel_r088_*.md` are summarised here.

**Rules agreed.** R-076's rule stands as written; no change of tolerance (one lane proposed one, chosen after 17b's
one-line miss, and withdrew it). Three judges a sheet are reported with their spread, as information; any change of
rule is Kevin's, made before results. Ship rule: among recipes that pass R-076's rule at three seeds never used to
screen them, ship the one with the fewest changes from 17b, unless another's pooled `hard_dev` recall is higher by
more than 15; the seed shipped is named in this list before its confirmation. Seeds 85 to 87 are reserved for
confirmation: 17b runs there first (item 3), and any finalist confirms there, paired seed for seed. Every new training
run saves its epoch-2 checkpoint. Scaled or mixed adapters are dials or diagnostics, not shippable models. The
write-up gives the number of recipes and candidate-seeds scored on the probe, `hard_dev` and the check set, all
development evidence, killed and failed runs included.

**The plan, in order** (cs = candidate-seed).

| # | Candidate | Seeds | What changes from 17b |
|---|---|---|---|
| 1 | 19a | 82, 83 | R-086 (running) |
| 2 | 17b scaled 0.85, 0.7 | 82, 83 | LoRA B scaled at load; scoring only |
| 2 | 17b/18a mixed, a = 0.3, 0.5, 0.7 | 82 | rank-64 adapter, the exact blend of the two deltas; diagnostic |
| 3 | 17b | 85, 86, 87 | none: how often R-076's item 1g fails |
| 4 | fix 20 | 82, 83 | R-087's set (25 fact-word lines and 25 indirect questions added) |
| 5 | 17m | 82, 83 (84 if it passes) | chat rows get loss only on the no-search decision and the end marker |
| 6 | 17b, 2 epochs | 82, 83 | 2 epochs at 3e-4; then 2 epochs at 2e-4 at 82, 83 |
| 7 | distinct chat targets | 82, 83 | each pass over the data sees different vetted chat rows; same chat share |
| 8 | replace, don't add | 82, 83 | fact-word lines in place of 25 of the 150 chat targets; 800 rows |
| 9 | answer repair | 82, 83 | about 60 found-fact targets replaced by 17b's own replies that give the value and do not echo |
| 10 | 17c | 82, 83 | 17b's chat targets re-vetted on a who-is-who and tone rubric |
| 11 | seed 84 | | for each candidate passing `gate_r086.py` |
| 12 | confirmation | 85, 86, 87 | up to two finalists, R-076's rule as written |
| 13 | stress tests | | the finalist only |
| 14 | reserve | | about 25 cs plus about 10 for the card slowing, committed Saturday night |

Cancelled: fix 20 at doses 2 and 3, and 19b (two seeds cannot separate doses; added chat rows cost recall, R-085);
lr 1e-4 (R-079, R-080); rank 16; the remaining stress tests on base, v5 and 17b (finalist only). In the reserve:
stitched asked-before rows, with a trigger written now: if the finalist is of the 17b family and its `--asked-before`
probe `in_view` is below 41 of 48, they are built next, replacing rows. Same-conversation pairs were withdrawn.

**Candidates scored on the development pools before this record**, for the count the write-up gives: every
`screen_*` label in `results/recall_eval` (fixes 1 to 18), plus 18a and 18c. From here each record that starts a run
adds its candidates to this list before the result.

## R-089 · 2026-11-05 · SPRINT · 19a passes every count but fails the judged check set by one line; two planned candidates dropped at build

**19a at seeds 82 and 83** (R-086's set; backlog runner, `runner.log`). `scripts/records/gate_r086.py fix19a`:

| Item | 19a | Needed | 17b |
|---|---|---|---|
| probe 51203 recall, seed 82 | 95 | 94 | 94 |
| probe 51203 `statement`, seed 82 | 48 | 47 | 48 |
| `hard_dev` `never_told`, seed 82 | 46 | 44 | 46 |
| `hard_dev` recall, seeds 82 and 83 | 148 | 145 | 145 |
| probe 73157 recall, seeds 82 and 83 | 191 | 189 | 189 |
| `hard_dev` false retrieval, seed 82 | 5 | at most 6 | 4 |

The questions asked as statements undid 18a's loss: `hard_dev` recall 74 at each seed against 18a's 56. Facts in view
rose too: `hard_dev` `in_view` 40 and 40 against 17b's 38 and 36; probe 46 and 44 against 43.

**Judged items** (`results/coherence/R-089/`; three fresh Sonnet judges a sheet, each in its own folder reading only
the rubric and the sheet, transcripts checked: every judge's code only wrote marks it had listed by reading). Judge 1
decides, as written before the marks; judges 2 and 3 give the spread. Base is `three_exchanges`.

| Sheet | Judge 1: base, 19a | Judge 2 | Judge 3 |
|---|---|---|---|
| Probe Sheet B `statement` (`probe2_base` vs `probe_fix19a_82`, seed 90496) | 46, 48 | 45, 46 | 45, 46 |
| Probe Sheet B `in_view` | 35, 41 | 36, 43 | 34, 43 |
| `hard_dev` Sheet B `statement` (seed 90497) | 44, 46 | 44, 47 | 44, 47 |
| `hard_dev` Sheet B `in_view` | 29, 35 | 30, 37 | 29, 38 |
| Check set, seed 82 (seed 90498) | 44, 46 | 44, 47 | 45, 46 |
| Check set, seed 83 (seed 90499) | 45, **42** | 44, 46 | 45, 44 |

**The check set pooled over both seeds is 88 against base's 89 under judge 1, so 19a fails R-086's gate by one line.**
Judges 2 and 3 would pass it (93 against 88, 90 against 90). The lines judge 1 marked down at seed 83 are not noise
alone: five of them are one stock reply, "That sounds like a lot of work ...", to a sprained ankle, a commute, a cat
scratching the sofa, loud music and a truck; judge 3 marked three of these down too, judge 2 none. The same kind
of repeated reply as v5's "Hope ... settles down soon" (R-085), at one seed of two. 19a's seed 84 runs from the
backlog under R-088's item 11 (the unjudged items), as information; it does not go to confirmation.

**Dropped at build, each by the lane that proposed it.** Item 7, distinct chat targets in each pass: R-078's
accepted pool holds only 117 distinct messages and 129 distinct targets, so a set with no target twice has a 6% chat
share against 17b's 19% and changes two things at once. Item 10, 17c: two fresh judges re-vetted 17b's 150 chat
targets and 300 spares on R-078's target rubric (all 450 lines each, agreeing on 439; `results/coherence/R-089V/`)
and rejected 1 target of 150, so 17c would be 17b with one row changed. A finding, not a candidate: 17b's remaining
plain-chat faults do not come from faulty targets. Both slots go to the reserve. A first pair of judges on that sheet
marked only 45 and 46 lines of 450 and were discarded; the sheet was split into five parts and judged again.

**Training speed.** Training runs now cap the process at 85% of card memory (`--max-vram-fraction`): at 9.6 of 10 GB
reserved, other programs' memory pushed training into system memory and steps slowed from 1.3 s to 20 s. 19a's seed
83 trained in 28 min under the cap.

**Candidates scored since R-088:** 19a at 82 and 83. Next on the backlog: 17b scaled 0.85 and 0.7 (82, 83), 17b and
18a mixed (82), 17b at 85 to 87, fix 20, 17m, 2 epochs at 3e-4 and 2e-4, 17r, answer repair (17p).

## R-090 · 2026-11-05 · SPRINT · Ten seed-82 models on one blind check-set sheet: 19a is above base with the most recall; scaling and mixing trade one for the other

**Why one sheet.** Two-model sheets put each model before a different judge, and judges differ by one to five
lines on the same replies (R-085, R-089). `scripts/make_multi_sheet.py` shuffles every model's replies to the same 48
check-set conversations into one blind sheet (480 lines, shuffle seed 90500), so each judge marks every model. Three
fresh Sonnet judges, each reading only the rubric and the sheet in five parts, transcripts checked (their code only
wrote marks they had listed). A diagnostic: it decides no gate. Sheet, key, run list and marks in
`results/coherence/R-090/`.

**The dials** (R-088 item 2, scoring only; `scripts/make_dial_adapter.py`): 17b with LoRA B scaled by 0.85 and 0.7,
and 17b and 18a mixed into one rank-64 adapter whose change is exactly `a` times 17b's plus `1 - a` times 18a's.

| Model, seed 82 | Judge 1 | Judge 2 | Judge 3 | Mean | `hard_dev` recall | `hard_dev` `never_told` |
|---|---|---|---|---|---|---|
| base | 45 | 42 | 45 | 44.0 | 20 | 39 |
| v5 | 41 | 38 | 41 | 40.0 | 58 | 47 |
| 17b | 39 | 42 | 44 | 41.7 | 72 | 46 |
| 17b scaled 0.85 | 39 | 41 | 44 | 41.3 | 70 | 46 |
| 17b scaled 0.7 | 44 | 44 | 46 | 44.7 | 70 | 45 |
| mixed, a = 0.7 | 43 | 42 | 45 | 43.3 | 71 | 47 |
| mixed, a = 0.5 | 43 | 41 | 43 | 42.3 | 70 | 47 |
| mixed, a = 0.3 | 46 | 46 | 46 | 46.0 | 66 | 48 |
| 18a | 47 | 46 | 48 | 47.0 | 56 | 48 |
| **19a** | **45** | **45** | **46** | **45.3** | **74** | 46 |

**Reading.** Under the same three judges, 19a at seed 82 is at or above base for each judge and has the most `hard_dev`
recall of any model; its failure in R-089 is the stock reply at seed 83, not seed 82. 17b is below base for two judges
of three. Moving toward 18a, by mixing or by scaling 17b down, buys plain chat with `hard_dev` recall, nearly in step;
scaled 0.7 is at base for chat with recall 70, but at seed 83 its `hard_dev` `never_told` fell to 38 of 48 (17b 47),
so a weaker pull also weakens declining. No dial beats 19a on both. Base's `hard_dev` recall and `never_told` are its
`tool_loop` arm at seed 73157 (`hd_base`).

## R-091 · 2026-11-05 · SPRINT · 17b at fresh seeds 85 to 87 fails R-076's rule again, under all three judges: its plain chat is unstable across seeds

**Why** (R-088, item 3): 17b failed R-076's rule at seeds 82 to 84 by one judged line at seed 83 (R-082); seeds 85 to 87
show how often that happens. Trained from `strict_chat.jsonl` with 17b's settings (backlog runner, cap on card
memory); scored on probe and `hard_dev` 73157. Sheets A, B and `hard_dev` B for each seed (shuffle seeds 90501 to
90509), three fresh Sonnet judges a sheet type, each marking its three seeds in its own folder, transcripts checked.
`scripts/records/rule_r076.py`, the rule as written for any name, seeds and judge; judge 1 decides.

| 17b, seed | 82 | 83 | 84 | 85 | 86 | 87 |
|---|---|---|---|---|---|---|
| Probe recall, of 96 | 94 | 95 | 94 | 96 | 96 | 95 |
| Probe `statement` (no search on chat), of 48 | 48 | 47 | 47 | 48 | **42** | 48 |
| `hard_dev` recall, of 96 | 72 | 73 | 83 | 82 | 65 | 77 |
| `hard_dev` `in_view`, of 48 | 38 | 36 | 41 | 34 | 35 | 32 |

**Rule at seeds 85 to 87**: every count passes (probe recall 287 of 288, `hard_dev` recall 224 against 172, false
retrieval 0 and 16, `never_told` 137). **Item 1g fails under all three judges**: Sheet B `statement` at seed 86 is 37,
41 and 37 against base's 44, 45 and 45. Judge 2 also fails item 6 (131 against 135). Sheet A passes under all three
(older plus confirm 286 against 237 to 240).

**Seed 86's failure.** Six chat lines that name a person or relation were searched, and answered with an unrelated
fact about that person: "i should really call my classmate" got "Hana is your classmate and is terrified of
spiders."; "my godfather has been acting strange lately" got "Your godfather Farah speaks fluent Turkish."; "Dmitri
forgot my birthday again" got "I don't have that from you. What is it?". R-082's failure, worse. 19a, trained with
fact-word chat lines and matching questions, searched on none of the 96 chat lines at seeds 82 and 83.

**Reading.** 17b's miss at seed 83 was not a judging accident: across six seeds its plain chat falls below base at
two (83 and 86) and its `hard_dev` recall spans 65 to 83. R-076's rule rejected it correctly. The spread across seeds
is wider than any single-seed screen can resolve, which bears on every screen in this work: a candidate's seed-82
result says little alone.

**Candidates scored since R-090:** 17b at 85, 86, 87.

## R-092 · 2026-11-05 · SPRINT · 17m passes R-086's whole gate, counts and judged sheets; fix 20 fails; 17m goes to confirmation

**17m** (R-088 item 5): 17b's rows and settings, with `--loss-on chat_decision`: on plain-chat rows only the reply's
first token and its end-of-turn marker carry loss, so the reply's words stay the model's own; every other row as
17b. Its first run failed on a check of mine that compared 150 chat rows with their 129 distinct messages; fixed to
count rows, and a check added that no chat row shares its message and reply with a row of another kind.

`scripts/records/gate_r086.py fix17m`, the items that need no judge:

| Item | 17m | 19a | 17b | Needed |
|---|---|---|---|---|
| probe 51203 recall, seed 82 | 95 | 95 | 94 | 94 |
| probe 51203 `statement`, seed 82 | 48 | 48 | 48 | 47 |
| `hard_dev` `never_told`, seed 82 | 48 | 46 | 46 | 44 |
| `hard_dev` recall, seeds 82 and 83 | **157** | 148 | 145 | 145 |
| probe 73157 recall, seeds 82 and 83 | 192 | 191 | 189 | 189 |
| `hard_dev` false retrieval, seed 82 | **1** | 5 | 4 | at most 6 |

**Judged** (`results/coherence/R-092/`, shuffle seeds 90510 to 90513; three fresh Sonnet judges, each marking all four
sheets in its own folder, transcripts checked; judge 1 decides). Base is `three_exchanges`.

| Sheet | Judge 1: base, 17m | Judge 2 | Judge 3 |
|---|---|---|---|
| Probe Sheet B `statement` | 45, 48 | 45, 48 | 45, 48 |
| Probe Sheet B `in_view` | 36, 41 | 35, 41 | 36, 40 |
| `hard_dev` Sheet B `statement` | 44, 48 | 43, 48 | 43, 48 |
| `hard_dev` Sheet B `in_view` | 43, 45 | 39, 45 | 41, 44 |
| Check set, seed 82 | 45, 47 | 45, 47 | 45, 47 |
| Check set, seed 83 | 45, 43 | 45, 43 | 45, 43 |

**17m passes every item of R-086's gate, under all three judges**: the check set pooled is 90 against base's 90. The
first candidate to pass both the counts and the judged items. Its misses on the check set at seed 83 are R-091's
failure, at a lower rate: three of 48 chat lines that name a person were searched and answered with an unrelated fact
("my tutor hurt a knee playing football and is gutted" got "Your tutor Ayaan got a swallow tattoo last week."); the
probe's `statement` count at seed 83 is 46.

**Fix 20** (R-087's set: 17b plus one vetted fact-word chat line and one indirect question a type, 25 each) fails the
gate on four items: probe 51203 `statement` 39 (nine chat lines searched), `hard_dev` recall 125 against 145, probe
recall 185 against 189. Half of 19a's dose, spread over every type, is worse than 17b; with R-085 and R-089, the
fact-word lines help only at 19a's full dose and with their matching questions.

**Next, under R-088 as agreed.** 17m's seed 84 (item 11), then confirmation at seeds 85, 86 and 87 (item 12), paired
seed for seed with 17b's runs there (R-091); R-076's rule as written decides (`scripts/records/rule_r076.py fix17m
R-093 1 85 86 87`), judge 1 deciding. **Named before confirmation: if 17m passes, the seed shipped is 82.** By R-088's
ship rule 17m, one change from 17b (the loss on chat rows), is the recipe with the fewest changes among those that pass
so far. The other screens (2 epochs at two learning rates, 17r, 17p) run after, and any that passes is weighed by the
same rule.

**Candidates scored since R-091:** fix 20 at 82 and 83; 17m at 82 and 83.

## R-093 · 2026-11-06 · SPRINT · 17m passes R-076's rule at fresh seeds 85 to 87, under all three judges: v6

**Confirmation** (R-088 item 12): 17m trained at seeds 85, 86 and 87, never used to screen it, paired seed for seed
with 17b's runs there (R-091). Sheets A, B and `hard_dev` B for each seed (shuffle seeds 90514 to 90522); three fresh
Sonnet judges a sheet type, each marking its three seeds in its own folder, transcripts checked (every judge read only
its own folder; their code only wrote marks they had listed). `scripts/records/rule_r076.py fix17m R-093 <judge> 85 86
87`; judge 1 decides.

| Item | 17m, seeds 85 to 87 | Needed | 17b, same seeds |
|---|---|---|---|
| 1a probe recall pooled | 288 | above 252 | 287 |
| 1b `in_view` pooled | 125 | 110 | 120 |
| 1c `statement` pooled | 143 | 136 | 138 |
| 1d right decisions, each seed | 239, 240, 240 | 200 | 240, 234, 240 |
| 1e false retrieval pooled | 2 | at most 39 | 0 |
| 1f Sheet A, judge 1: confirm; older plus confirm | 144 vs 141; 265 vs 228 | at or above base | 144 vs 141; 286 vs 240 |
| 1g Sheet B, judge 1: `statement`, `in_view` per seed | 47/46, 41/35; 46/46, 40/35; 46/46, 41/35 | at or above base, each seed | **fail**: 37 vs 44 at 86 |
| 2 probe recall pooled | 288 | 273 | 287 |
| 3 `hard_dev` recall pooled | **249** | 172 | 224 |
| 4 `hard_dev` false retrieval pooled | 4 | at most 20 | 16 |
| 5 `hard_dev` `never_told` pooled | 143 | 132 | 137 |
| 6 `hard_dev` Sheet B, judge 1: `statement`, `in_view` | 137 vs 129, 127 vs 99 | at or above base | 131 vs 129, 101 vs 93 |

**RULE: PASS under judge 1, and under judges 2 and 3.** Item 1g is the closest: at seed 86, 17m's `statement` equals
base's (46 against 46 under each judge). By R-088's ship rule 17m, one change from 17b,
replaces v5 as **v6, shipped at seed 82** as named in R-092 before these results. Against v5 at its own seeds (R-076),
`hard_dev` recall pooled rises from 172 to 249 of 288.

**Failure seen at seed 87.** On Sheet A, judge 1 marked down 15 of 17m's 48 "fact told long ago" answers at seed 87
(judges 2 and 3: 15 and 6), against 2 and 6 at seeds 85 and 86. The fact is right and the relation is pinned on the
wrong person: "i'm blanking on what my barber is scared of" got "Hana's barber is scared of clowns." (should be "your
barber Hana"); "which club did Chidi join" got "Chidi, who is my daughter, joined a water polo club this month." The
item passes on the pooled count; the failure goes in the write-up. 17m's chat replies are the base model's own words
by design, so its plain chat sits at base's level rather than above it.

**Still to run under R-088**: 2 epochs at 3e-4 and 2e-4, 17r, answer repair (17p). Any that passes the screen and then
confirmation is weighed against 17m by the ship rule (fewest changes from 17b, unless pooled `hard_dev` recall is
higher by more than 15). Freeze Tuesday; the sealed final run on Kevin's go.

**Candidates scored since R-092:** 17m at 84, 85, 86, 87.

## R-094 · 2026-11-06 · SPRINT · The who-is-who slip: source, a registered gate and a panelled fix, before any run

Kevin: "don't love that weak spot", then "panel a fix". The same four-lane panel as R-088 (targets, training,
measurement, against), three rounds, consensus; transcripts checked (one lane listed `data/screens` with sealed names
filtered out and read nothing sealed).

**The slip.** A fact answer that names the right value but pins the friend's relation on the wrong person or on the
speaker: "Hana's barber is scared of clowns." for "i'm blanking on what my barber is scared of"; "Chidi, who is my
daughter, joined a water polo club"; "My godfather, Lucia, speaks fluent Turkish." `item_correct` passes these, since
the value is there.

**Measure, registered now.** `scoring.slip_shape(reply, message)`: the relation is the word after "my" in the friend's
message; a slip is "<Name>'s <relation>" (unless the friend's own message has those words), a sentence opening
"My <relation>", or "who is my". Known-bad and known-good cases in `tests/test_scoring.py`. Calibrated once against
judge 1 on 17m's Sheet A at seeds 85 to 87 (R-093), 17m's lines only: flagged and marked 0, 17; flagged and marked 1,
0; not flagged and marked 0, 6 (other faults); not flagged and marked 1, 265. No false hits; it finds 17 of the 23
answers judge 1 marked down.

Counts on probe 73157 `older` and `confirm` (of 96): base 2; v5 1, 1, 1; 17b 4, 1, 11, 5, 1, 10 (seeds 82 to 87); 17m
3, 4, 1, 1, 2, **14** (82 to 87). `hard_dev`: base 1; v5 1, 0, 0; 17m 0, 3, 3, 4, 6, 6. The shipped seed 82 is at
base's rate on the probe; seed 87 is the tail.

**Source.** Every `confirm` target in 17b's set (`strict_chat.jsonl`, which 17m uses) is the scripted "Your
{relation} {person} ...". Of 200 `older` targets, 140 are base's own replies to the search result; `slip_shape` flags
27 of them ("My roommate, Omar, writes western novels at night."; "Marc's sister writes science fiction novels at
night."). The slip's rate in replies (about 3% at most seeds) is below its rate in targets (27 of 350 found-fact targets, 8%), so cleaning
targets may lower the typical seed and not remove the tail.

**Gate, registered before any run** (R-076 and R-086 unchanged; v6 stays valid):
- probe slip count at most 5 of 96 at every seed;
- pooled over the gate and confirmation seeds (82, 83, 88, 89, 90) at most 8 of 480;
- `hard_dev` slip count at most 3 a seed;
- probe and `hard_dev` recall not below v6's at the same seeds;
- Sheet A judged slips reported, not gated.

**Kevin's ruling, before any result**: "given the near impossibility of the getting better by another 15 lets consider
that metric solved". R-088's ship rule no longer needs a fix to beat v6's pooled `hard_dev` recall by 15: a fix that
passes R-086's gate at 82 and 83, R-076's rule at fresh seeds 88 to 90 and this slip gate replaces v6, with recall
only not below v6's.

**The plan, agreed by all four lanes.**
1. Diagnostic, scoring only: 17m's epoch-2 adapters (saved under R-088) at seeds 87 and 84, slip counted.
2. **Fix A, fix17w**: 17m's recipe on a set with no slip-shaped target. `scripts/records/splice_r094.py` rewrites each
   flagged answer's subject to "Your <relation> <name>", the name taken from the fact the search returned; the rest of
   the answer is kept, and a row stops the build if the rewrite still slips or drops the name. All 27 rewrote cleanly
   ("My aunt finally switched to a Pixel." to "Your aunt Greta finally switched to a Pixel."); 800 rows, 0 slip-shaped.
3. fix17w at seeds 82 and 83 against R-086 and the slip gate; it stops if either fails. Then seed 87 once, reported,
   chosen because 17m failed there, kept out of the pooled count; only a clear regression (above 17m's 14) stops it.
4. If it survives: seeds 88, 89 and 90 for R-076's rule and the slip gate.
5. Fix B, a loss mask on the `older` base-reply rows (only the first token and end marker carry loss), only if A fails
   and the reserve allows; never stacked with A.
6. v6's asked-before stress tests run now (R-088's reserve trigger depends on them); its other stress tests wait until
   this track is decided.

## R-095 · 2026-11-06 · SPRINT · Fix A clears the slip gate but fails R-086's judged Sheet B by one line; fix B next

**Diagnostic** (R-094 step 1): 17m's epoch-2 adapters, scoring only. Seed 87: probe slip 0 (17m at 3 epochs: 14), but
`hard_dev` recall 63 (78). Seed 84: probe slip 9 (1), probe recall 82 (96), `hard_dev` recall 38 (78). The saved
epoch-2 adapter is mid-schedule, its recall well short, and its slip count does not fall consistently: stopping early
is not the lever.

**v6's asked-before tests** (R-088's reserve trigger): 17m seed 82 under `--asked-before`, probe `in_view` 41 of 48,
`hard_dev` 36. The trigger (below 41) does not fire.

**Fix A, fix17w** (17m's recipe on R-094's set with the 27 slip-shaped answers rewritten), seeds 82 and 83:

| Item | fix17w | 17m (v6) | Needed |
|---|---|---|---|
| probe 51203 recall, `statement` (82) | 96, 47 | 95, 48 | 94, 47 |
| `hard_dev` `never_told`, false retrieval (82) | 47, 6 | 48, 1 | 44, at most 6 |
| `hard_dev` recall, 82 and 83 | 159 | 157 | 145, and not below v6 |
| probe 73157 recall, 82 and 83 | 192 | 192 | 189, and not below v6 |
| probe slips, 82 / 83 | 2 / 1 | 3 / 4 | at most 5 each |
| `hard_dev` slips, 82 / 83 | 0 / 0 | 0 / 3 | at most 3 each |

Every count and the slip gate pass. At seed 83, fix17w searched on six `hard_dev` chat lines (`statement` 42; 17m 46).

**Judged** (`results/coherence/R-095/`, shuffle seeds 90523 to 90526; three fresh Sonnet judges, own folders,
transcripts checked; judge 1 decides):

| Sheet | Judge 1: base, fix17w | Judge 2 | Judge 3 |
|---|---|---|---|
| Probe Sheet B `statement` | 45, 48 | 46, 48 | 45, 47 |
| Probe Sheet B `in_view` | **34, 33** | 36, 38 | 36, 39 |
| `hard_dev` Sheet B `statement` | 42, 47 | 45, 47 | 43, 47 |
| `hard_dev` Sheet B `in_view` | 37, 41 | 41, 45 | 39, 43 |
| Check set, seed 82 | 45, 46 | 44, 46 | 43, 47 |
| Check set, seed 83 | 45, 45 | 44, 46 | 43, 44 |

**fix17w fails R-086's gate by one line**: probe Sheet B `in_view` 33 against base's 34 under judge 1; judges 2 and 3
would pass it. Eleven of the 15 lines judge 1 marked down are ones two or three judges marked down, most of them
R-063's "forgetting read as wordplay" ("drawing a blank on my tutor's tattoo" got "That's a unique way to express your
thoughts."), which every model shows. On the counts, fix17w answers 39 facts in view at seed 82 (17m 41) and 46 at 83
(17m 45). Under R-094's plan the track stops: seeds 88 to 90 are taken off the backlog; seed 87, already training,
finishes and is reported (whether a clean set removes the tail).

**Fix B, fix17mb** (R-094 step 5): 17m's rows, `--loss-on chat_answer_decision`. Chat rows keep only the decision, as
17m; the 140 `older` rows whose answer is base's own reply (not the scripted "Your {relation} {person} ...") keep the
search call's full loss, and on the answer only its first token and end-of-turn marker
(`loss_masks.answer_decision_labels`). 290 rows masked: 150 chat and 140 answers. Same gate and slip gate, seeds 82 and
83, then 87 reported, then 88 to 90 if it passes.

**Candidates scored since R-093:** 17m epoch-2 at 87 and 84 (scoring only); fix17w at 82 and 83.

## R-096 · 2026-11-06 · SPRINT · CuratorKIT's grounding gate over the found-fact training answers, with a Claude judge

**Why CuratorKIT.** The who-is-who slip (R-094) came from training answers that were base's own replies to a search
result and were not faithful to the passage they answered from: "Marc's sister writes science fiction novels at night."
where the passage says "my sister, Marc, writes science fiction novels at night". Checking a generated answer against
the exact source it came from is what CuratorKIT's `HallucinationGate` is for. It gives a check on the training answers
that is independent of this project's own slip pattern (`scoring.slip_shape`) and of the coherence judges, and it makes
CuratorKIT the third Lexsi toolkit in the work, as R-002 planned ("CuratorKIT if time allows").

**Why a Claude judge.** The gate needs a judge model. The organisers allow other models for supporting work: "the core
of the submission should include the cohere's 7 models listed. for any supplemental work like teacher model, validation
by another model, comparisons etc.. its fine to use others", and for judging "you can use any model , not just the 7"
(Lexsi Discord, 2026-11-03). The trained model and everything it is scored on stay Tiny Aya. A Claude judge needs no API
key or payment and leaves the GPU to training; a small local judge would be weak at the distinction that matters here
(which person holds which relation).

**How the judge is plugged in.** CuratorKIT takes its judge as a backend class (`curatorkit.llm.base.BaseLLM`, one
method). A Claude agent cannot be called from Python, so `scripts/run_curator_check.py` runs the gate twice. First with
a backend that records every prompt the gate sends; the same prompts are written as a judge sheet (the gate's own
instructions once, then each item's source text, question and answer), and every recorded prompt is checked against
the sheet by its SHA-256 digest: all 377 matched. A fresh Sonnet agent, reading only that sheet, answers each item in
the gate's JSON format. Then the gate runs again with a backend that replays those answers by digest, so CuratorKIT's
own prompt, score parsing, threshold (its default, 0.7), rejection reasons and provenance decide every verdict.
CuratorKIT is installed from the commit in R-003 (`dd9e835`) with `--no-deps`: its four core requirements were already
in the environment, so nothing else changed.

**What it covers.** v6's 350 found-fact answers (`strict_chat.jsonl`: 200 `older`, 150 `confirm`) and fix17w's 27
rewritten answers, 377 items. The questions it answers: does the gate reject the 27 slip-shaped answers the pattern
found; does it reject answers the pattern missed; does it pass the 27 rewrites.

**Limits.** All three judges are Claude models. They may share blind spots with each other and with the Claude judges
on the coherence sheets, so their agreement is weaker evidence than agreement across model families would be.

**Result** (`results/curator/R-096/`: summary, the rejected answers with each judge's reason, and the judges' verdicts and
key). Three fresh Sonnet judges, each reading only its sheet in its own folder, transcripts checked; the gate run once
per judge, an answer rejected when at least two of the three runs reject it (fixed before the second and third judges'
verdicts were read). The judges rejected 23, 25 and 21 answers; 21 of the 23 rejected by two or more were rejected by
all three, and 2 answers by one judge only.

- **22 of v6's 350 found-fact answers fail the gate** (6.3%), all `older` answers that are base's own replies.
  - 8 are slip-shaped ("Marc's sister writes science fiction novels at night.").
  - 14 are faults `slip_shape` does not cover. Who-is-who where the question names the person, not "my <relation>":
    "Greta's brother adopted a dog named Pepper." for "what is the name of the dog Greta adopted"; "Yusuf's aunt broke
    her jaw while skiing."; "Lena's neighbor's kitten is named Noodle." Claims the passage does not make: "Marc's new
    street, Cedar Court, seems to be a source of frustration for him."; "Glastonbury is a famous music festival, so
    it's a fantastic o[pportunity] ...". Talk off the point: "Funny how the snow keeps coming up, but at least the
    florist shop is finally her[e]".
- **19 of the 27 slip-shaped answers pass**: the gate checks facts against the source, and "My roommate, Omar, writes
  western novels at night." states the passage's facts in the friend's voice. Grounding and voice are different checks.
- **26 of fix17w's 27 rewritten answers pass.** The one rejected keeps an embellishment of the original ("Your brother
  Yusuf is going to Oktoberfest and is having a great time!").

**Reading.** CuratorKIT finds a wider class of faulty training answers than this project's pattern: about one in six
of the `older` answers that are base's own replies (22 of 140) claims something its passage does not support. That is
a likely source of v6's who-is-who slips as well as of the slips the pattern counts. A fix built on it (replacing the
gate's rejections) goes to the panel before it is written.

## R-097 · 2026-11-06 · SPRINT · Fix C, agreed by the panel before it was built

Kevin: "Yes, panel it" (a fix built on R-096). The four-lane panel (data, gate risk, measurement, against), three
rounds, consensus; transcripts checked.

**Round 1 positions.** Data: fix A's set plus at most 23 changed rows, scripted answers, a CuratorKIT re-check with
hidden controls. Gate risk: changing `older` targets pulls against facts in view (R-063, R-064), the item fix A failed;
change as few rows as possible, leave every other row byte-identical, read seed 82's counts before judging.
Measurement: the gates word for word, a one-line miss is a miss, template rewrites only, only seeds 88 to 90 are clean.
Against: keep v6 and spend the weekend on the write-up; CuratorKIT is an audit, not a pipeline stage.

**Agreed plan.**
1. **C1 = fix17w (fix A's set) minus 15 rows** (`scripts/records/splice_r097.py`): the 14 `older` answers at least two
   of R-096's judges rejected that fix A did not rewrite, and fix A's one rejected rewrite. Dropped: `older_0008`,
   `0014`, `0026`, `0032`, `0043`, `0059`, `0063`, `0072`, `0081`, `0086`, `0097`, `0165`, `0168`, `0176`, `0194`.
   785 rows (185 `older`); nothing new is written; all 450 `in_view`, `statement` and `never_told` rows are
   byte-identical to 17m's; `slip_shape` reads 0. No CuratorKIT re-check: the 335 found-fact answers kept are the
   ones R-096's judges passed (the same judges who chose the drops). 17m's recipe (`--loss-on chat_decision`).
2. Seed 82, counts only. **Stop rule, not a pass criterion**: if any R-086 count or slip-gate item fails, or probe
   `in_view` is below 41 (17m's at 82; fix A had 39), no judging; the run is reported and counted, and C2 is built.
   A stop at 40 is not read as proof that dropping rows hurts.
3. Seed 83, counts and slips, the same stop rule; then R-086's judged sheets for C1 at 82 and 83 as registered
   (two-model sheets against base, judge 1 decides, judges 2 and 3 reported), read beside fix A's (R-095).
4. If C1 passes: seeds 88, 89 and 90 for R-076's rule and the pooled slip gate. A pass there replaces v6 (Kevin's
   ruling, R-094); otherwise v6 stands.
5. If C1 stops: **C2** = fix A's set with the same 15 rows given the scripted "Your {relation} {person} ..." answer,
   built only after a fresh three-judge CuratorKIT acceptance test on one blind sheet: the 15 new answers, the 22
   original rejections as hidden controls and about 20 passing answers; go only if all 15 pass at 2 of 3 and at
   least 18 of the 22 controls are rejected (a failed control voids the sheet). Then steps 2 to 4. A second failure
   ends the track.
6. **Deadline**: no training or scoring starts after Monday, November 9, 12:00; if C1 or C2 has not finished the whole
   gate by then, v6 stands. The write-up comes first if GPU time and it compete.
7. Write-up: CuratorKIT is a data-quality audit and acceptance test on the training targets, with Claude verdicts that
   are saved and replay to the same result; not an independent check of the model, not a Cohere model, not a training
   stage; no claim that the faults cause the slips; every candidate-seed counted.

## R-098 · 2026-11-06 · SPRINT · Fix C1 stops by one recall answer; fix C2 passes its acceptance test

**Fix C1, fix17y** (R-097 step 1: fix A's set without the 15 answers R-096's gate rejected), seeds 82 and 83:

| Item | fix17y | 17m (v6) | Needed |
|---|---|---|---|
| probe 51203 recall, `statement` (82) | 96, 48 | 95, 48 | 94, 47 |
| `hard_dev` `never_told`, false retrieval (82) | 47, 4 | 48, 1 | 44, at most 6 |
| `hard_dev` recall, 82 and 83 | 74 + 88 = 162 | 74 + 83 = 157 | 145, and not below v6 |
| probe 73157 recall, 82 and 83 | 96 + 95 = **191** | 96 + 96 = **192** | 189, and **not below v6** |
| probe slips, 82 / 83 | 1 / 1 | 3 / 4 | at most 5 each |
| `hard_dev` slips, 82 / 83 | 0 / 0 | 0 / 3 | at most 3 each |
| probe `in_view`, 82 / 83 (reported) | 44 / 41 | 41 / 45 | 41 at 82 (R-097's stop rule) |

Every R-086 count passes (`scripts/records/gate_r086.py fix17y`). The slip gate's item "probe and `hard_dev` recall
not below v6's at the same seeds" fails on the probe, 191 against 192, read pooled over 82 and 83 as in R-095. A miss
by one is a miss: under R-097's stop rule C1 is not judged, and both seeds are counted (development candidates). Slips
and v6's numbers are recounted by `scoring.slip_shape` over each run's `older` and `confirm` rows; v6's match R-094's.
The one-answer gap is within the seed spread R-091 measured and is not read as harm from dropping rows.

**Fix C2, fix17z** (R-097 step 5): fix A's set with the same 15 answers replaced by the pool's scripted answer
(`scripts/records/splice_r098.py`). The value is the one fact value the row's answer names; the person and relation are
the ones in the search-result chunk that holds it; a row stops the build unless each is found exactly once. All 15
built ("Your uncle Marc lives on Cedar Court."; "Your roommate Tomas was born in November."); 800 rows; every other row
byte-identical to fix17w; `slip_shape` reads 0.

**Acceptance test, before any training** (`scripts/run_curator_check.py --test R-098`, `results/curator/R-098/`):
one blind sheet of 57 items, shuffled with seed 98: the 15 scripted answers, R-096's 22 v6 rejections as hidden
controls, and 20 answers no R-096 judge rejected (drawn with seed 98). Three fresh Sonnet judges, own folders;
CuratorKIT's gate replays each judge's verdicts. The changed script replays R-096's saved verdicts to the identical
rejected list.

| | Rejected (2 of 3) | Needed |
|---|---|---|
| Scripted answers | 0 of 15 | 0 |
| Hidden controls | 22 of 22 | at least 18 |
| Answers passed before | 0 of 20 | reported |

Each judge's run rejected 22 items. C2 goes. Transcript audit: judges 2 and 3 read their sheet and wrote their file
only; judge 1 also wrote an empty `/tmp/gen.py` with one shell command and ran nothing else (deleted); its marks were
written by hand like the others and are used.

**Next** (R-097 steps 2 to 4): `cand fix17z 82` and `83`, queued after the running screen; the same stop rule, then
R-086's judged sheets, then seeds 88 to 90. Deadline unchanged: nothing starts after Monday, November 9, 12:00.

## R-099 · 2026-11-06 · SPRINT · Messy chats: measure first, train only on a registered gap

**Headline number** (Kevin: "accepted", after this proposal). The write-up's headline is the sealed final run's
number. Until that run, the development headline is `hard_dev` recall, base 20 to v6 74 of 96 at seed 82 (+270%),
not the probe's 30 to 96: `hard_dev`'s questions are worded unlike training.

**Request.** Kevin: "can we get some messy proxies in for training?", after hearing that every pool, sealed ones
included, is template-built, so a pass shows new words in our kind of chat, not real messy chats.

**Evidence in hand** (development, seed 73157, tool arm; paired: one adapter, the same items plain and messy). Typing
style (R-067): v5 seed 82 probe recall 92 styled (plain about 93 to 96), `hard_dev` 58 against 58; base 30 to 38 on
the probe. Earlier question in view, v6 seed 82: probe recall 96 against 96, `statement` 48 against 48; `hard_dev`
recall 67 against 74, `in_view` 36 against 37, `never_told` 47 against 48.

**Panel** (four lanes: data, test integrity, measurement and schedule, against; two rounds; consensus; transcripts
checked: no lane opened a sealed file). Round 1: data proposed about 150 appended rows built by `stress.py`'s
transforms on fresh TRAIN items, with cue balance; test integrity required a separate candidate, the friend's messages
changed only, and a build brief free of the sealed pool's description; measurement put scoring first, with a trigger;
against argued for measuring the frozen model only, accepting training only on a measured drop. Round 2 accepted the
merged plan with four changes, all taken.

**Agreed plan.**
1. **Measure first, scoring only.** v6 at seeds 82 and 83 (and C2 at the same seeds if C2 passes its counts) on the
   battery: typing style (`--user-style`) and the held-out phone form (`--phone-style`) on the probe and `hard_dev`,
   every kind; corrections (`--corrections`, `older` and `confirm`) on both; earlier question in view at 83. The
   1,000-message chats are cut. Queued after C2's seed 83.
2. **The held-out form, fixed now:** `stress.phone_style` (`phone_typed`): every apostrophe dropped, "you" and "your"
   as "u" and "ur", and one pair of neighbouring letters swapped in one word of five letters or more, never a name,
   relation or fact value. `typed` does none of these. It is written by the builder, not blind, and is never used to
   build a training row; the messy build checks that no row's message equals its `phone_style` form. sha256 of the
   source of `phone_typed`, `phone_style` and `_SHORT_FORMS`: `cd89c1028f70e34a9b5d18089c34b3cc1812e2461c275f71d79a55de79a4f686`.
3. **Trigger, registered before the battery runs.** A messy form is a gap only if, paired over seeds 82 and 83 on one
   pool, it costs at least **8 of 192** recall answers, or at least 4 of 96 on `statement`, `never_told` or
   `in_view`, against the same adapter on plain items. No gap: no messy training, and the battery goes in the
   write-up as a finding, base beside it.
4. **If a gap: one messy arm, one dose, one try.** About 150 appended rows, built by script from fresh TRAIN items
   through `stress.py`'s transforms, only for the forms that showed a gap; scripted targets; every existing row
   byte-identical; no `in_view` answer rewritten; no writer agents; inputs TRAIN and `stress.py` only. Cue balance:
   a question in view on found rows too; correction openings on non-correction rows; style across all five kinds;
   decoy counts as R-020; counts reported.
5. **Order and seeds.** C2's gate first, never delayed. The arm sits on the shipping candidate's set (C2's if C2
   passes, else v6's): seeds 82 and 83 under R-086's gate and R-094's slip gate word for word and R-097's stop rule,
   then fresh seeds **91 to 93** for R-076's rule (88 to 90 stay C2's).
6. **Replacement.** The arm replaces the shipping candidate only if it passes every existing gate at 82, 83 and 91 to
   93 and gains on the held-out phone form, against the shipping candidate at the same seeds on the pool where the
   trigger fired, by at least **8 of 192** on the probe or **16 of 192** on `hard_dev` (training-seed noise, R-091).
   Otherwise it is a development finding.
7. **Clock.** If the battery is not scored and the arm's seed 82 and 83 runs have not started by **Sunday,
   November 8, 12:00**, the arm is dropped and the battery goes in the write-up. Nothing starts after Monday 12:00.
8. **Disclose:** messy rows made by script from TRAIN and `stress.py`; those transforms are also development tests;
   the held-out form was written by the builder; the sealed result is still template-built; no claim of robustness
   to real chats; every candidate-seed counted.

## R-100 · 2026-11-06 · SPRINT · An outside check on LoCoMo, agreed before any data is downloaded

**Request.** Kevin: "Yes, panel it", to score the frozen model and base on LoCoMo's memory questions (Maharana et al.,
ACL 2024, arXiv 2402.17753) after the freeze. Every pool of ours, sealed ones included, is built from our templates;
a public set built by someone else is the outside check. Kevin also: "make sure everything makes it into the write
up".

**What LoCoMo is** (from its repo and paper, read before the panel; the data not yet downloaded): `data/locomo10.json`,
10 long two-speaker conversations (paper averages for its 50: 305 turns, 19 sessions, 9,209 tokens), made by
gpt-3.5-turbo agents and edited by people; questions in the third person with gold answers, evidence turn ids and a
category 1 to 5 (by its scorer's code: multi-hop, temporal, inference, single-hop, adversarial with no answer); token
F1 after normalisation; data licence CC BY-NC 4.0.

**Panel** (four lanes: adaptation, validity and claims, measurement and schedule, against; two rounds; consensus;
transcripts checked). Against argued a 3B-class model trained for first-person template recall will sit near the
paper's weakest baselines on third-person multi-hop and temporal questions, and that a confusing number costs
clarity; it accepted a capped version.

**Agreed plan.**
1. **An outside check, never a decision.** Run on the frozen model; no tuning, prompt edit, candidate, seed or go for
   the sealed run rests on it. Losses and nulls reported in full.
2. **Data.** Kevin downloads `locomo10.json`; its sha256 is registered. The data, its questions, answers and turns,
   and per-item outputs quoting them stay local, out of git. Committed: scripts, the hash, the registration, item ids,
   aggregate numbers, and a NOTICE line with attribution and the licence.
3. **Adaptation**, every item a listed deviation: consecutive turns paired as (user, assistant) within each session,
   speaker names kept in the text; the last three exchanges in view; one passage per older exchange indexed, one
   index per conversation, top 5; each exchange prefixed with its session date; images as their caption; questions
   verbatim, third person, as the last user message; system prompts unchanged; a check that no exchange is split by
   the index's chunk size, counted in the index's own unit.
4. **Arms**: base with the tool, the frozen model with the tool, base without the tool.
5. **Sample**, drawn by a registered seed from a hash of the question text before any scoring: 300 questions from
   categories 1 to 4 in proportion, and 100 from category 5. Budget about 1.5 GPU hours.
6. **Scoring.** Primary: LoCoMo's token F1 with its own normaliser and category rules, per category and pooled over 1
   to 4. Category 5 two ways: LoCoMo's refusal check, and a widened list written now from the training pool's own
   unknown-reply wording (not from any LoCoMo output) together with "the reply does not contain the adversarial
   answer's tokens". Secondary, mechanical: gold-token recall, evidence recall at 5, search rate. No judges.
7. **Hypotheses.** H1: the frozen model with the tool above base with the tool on pooled F1 (categories 1 to 4); a gain
   counts only if the lower bound of a paired bootstrap 95% interval clustered by conversation (10,000 resamples; 10
   clusters, stated) is above 0, a sign test beside it. H2: the frozen model's category 5 rate on the widened list not
   more than 5 points below base's, read with its interval, not a pass or fail gate. Results as relative increase
   over base. **A floor result**, both arms near the paper's weakest baselines, **is uninformative**, stated now.
8. **Timing.** Converter, scorer and analysis (bootstrap, sign test, tables): CPU only, Nov 7 to 9, the scorer tested
   on gold-as-answer and on known-wrong answers. A format dry run of 10 base items, ids registered and excluded from
   the sample, read for format only: no score computed or printed. The registration is committed before the first
   scored item; not committed by the end of Nov 9, the check is dropped. The GPU run comes after the sealed final run
   and never delays it; not finished by 08:00 on Nov 12, the write-up says "not completed" and no partial arm is
   reported.
9. **Write-up**: its own section, "outside check, not the registered test", never in the sealed table. Allowed: "on an
   outside chat set built differently from our templates, the frozen model scored X against base's Y on the same
   questions", per category, with intervals. Forbidden: robustness to real chats, a ranking against published
   systems (their scores only as context, "not comparable"), anything about the sealed result, any claim that the
   freeze was validated.

## R-101 · 2026-11-06 · SPRINT · Fix C2 stops on hard_dev recall; the track ends and v6 stands

**Fix C2, fix17z** (R-098: fix A's set with the 15 answers C1 dropped given the scripted answer), seeds 82 and 83:

| Item | fix17z | 17m (v6) | Needed |
|---|---|---|---|
| probe 51203 recall, `statement` (82) | 96, 48 | 95, 48 | 94, 47 |
| `hard_dev` `never_told`, false retrieval (82) | 48, 1 | 48, 1 | 44, at most 6 |
| `hard_dev` recall, 82 and 83 | 77 + 72 = **149** | 74 + 83 = **157** | 145, and **not below v6** |
| probe 73157 recall, 82 and 83 | 96 + 96 = 192 | 96 + 96 = 192 | 189, and not below v6 |
| probe slips, 82 / 83 | **0 / 0** | 3 / 4 | at most 5 each |
| `hard_dev` slips, 82 / 83 | 0 / 0 | 0 / 3 | at most 3 each |
| probe `in_view`, 82 / 83 (reported) | 44 / 41 | 41 / 45 | 41 at 82 (R-097's stop rule) |

Every R-086 count passes (`scripts/records/gate_r086.py fix17z`). The slip gate's item "probe and `hard_dev` recall not
below v6's at the same seeds" fails on `hard_dev`, 149 against 157, read pooled over 82 and 83 as in R-095 and R-098.
Under R-097's stop rule C2 is not judged, and both seeds are counted (development candidates).

**The track ends** (R-097 step 5: "A second failure ends the track"). v6 (17m seed 82) stands as the shipped model and
its who-is-who slip stays a reported failure mode. Not run: C2's judged sheets and seeds 88 to 90. The fixes' seeds
in this track, all counted: fix A 82, 83, 87; fix B 82, 83; C1 82, 83; C2 82, 83.

**What the track shows**, reported and not used to choose anything: the slip count at the four C1 and C2 seeds was 1,
1, 0 and 0 of 96 on the probe (v6 3 and 4 at the same seeds), and 0 on `hard_dev` at all four; recall on `hard_dev`
moved within R-091's measured seed spread (65 to 83) in both directions. No claim is made that the faulty answers
cause the slips (R-097 item 7).

**Next.** v6's messy-chat battery (R-099) is running; the messy arm, if triggered, sits on v6's set. The GPU time kept
for C2's seeds 88 to 90 is free.

## R-102 · 2026-11-06 · SPRINT · Battery result; R-099 item 6 amended before any arm exists

**Battery** (R-099 step 1; v6 = 17m, seeds 82 and 83 pooled; messy minus plain, same adapter and items; tool arm):

| Form | probe recall /192 | probe `in_view`, `never_told`, `statement` /96 | `hard_dev` recall /192 | `hard_dev` `in_view`, `never_told`, `statement` /96 |
|---|---|---|---|---|
| lower-case typing (`user_style`) | -3 | -1, +2, -1 | -2 | -3, -1, -1 |
| phone typing (`phone_style`, held out) | **-14** | 0, +2, **-6** | **-25** | -3, +1, -1 |
| fact corrected later (`corrected`) | **-187** | recall only | **-146** | recall only |
| earlier question in view (`asked_before`) | -2 | -1, +2, -3 | -7 | **-4**, 0, 0 |

Gaps by R-099's registered trigger: corrections and phone typing on both pools; asked-before on `hard_dev` `in_view`,
exactly on the line. No gap: lower-case typing. Corrections, read in the replies: the search returns the original and
the correcting passage, and v6 answers the old value ("Your daughter Gustav got a koi tattoo." when the correction
said lighthouse). Base on corrections, probe, seed 73157: 19 of 96 recall (v6 at 82: 5), so v6 is 74% below base here;
base's remaining runs are recorded with the baseline.

**The problem.** R-099 item 6 lets the arm replace v6 only by gaining on the phone form, which correction rows are not
built to move, so the largest gap found could never ship.

**Panel** (four lanes: fix design, rule integrity, measurement and schedule, against; two rounds; consensus;
transcripts checked). Round 1: three lanes chose amending item 6 (B); against chose dropping the arm or keeping the
rule, and accepted B only with the held-out form, thresholds and guards hashed and logged before the arm is built, the
phone guard at all five seeds, and the held-out wordings from a source other than the builder. Round 2 accepted the
merged plan with four changes, all taken: every number frozen here before the baseline is scored (lanes 2, 4); the
blind list supplies the endings by the same rule, and the overlap check works on content words (lane 1); the
`hard_dev` phone guard at 91 to 93 read on the three-seed mean (lane 3).

**Kevin's decision**: "yeah of course as long as we explain why". The write-up explains the change and why.

**The amendment** (R-099 item 6 only; the trigger, the gap list, every existing gate and seeds 91 to 93 unchanged).
R-099 item 6 as registered: the arm replaces the shipping candidate only if it passes every existing gate at 82, 83
and 91 to 93 and gains on the held-out phone form by at least 8 of 192 (probe) or 16 of 192 (`hard_dev`). Amended:

1. **Held-out correction form, `stress.corrected_heldout`.** Training's own wordings were committed first (commit
   0d73bcb: `TRAIN_CORRECTION_OPENINGS`, the four R-067 openings and five more; `TRAIN_CORRECTION_ENDINGS`, three).
   Then a fresh agent that saw no project file, no transform and no result wrote 25 openings and 25 endings for
   correcting an earlier fact when texting, most common first; only 3 of its openings shared no content word with
   training's, so it was asked once for 25 more openings, read by no one before selection
   (`results/stress/R-102/blind_wordings.json`; transcripts checked: one write each). `scripts/records/select_r102.py`
   took the first six of each sharing no content word with training's: openings "hang on, ", "ah i just remembered, ", "sorry brain fart, ", "oh i should say, ", "so i just double checked and ", "thinking about it again, "; endings ", sorry", ", sorry about that", " just so you know", " lol sorry", " i think", ", sorry for the confusion"
   (`src/aya_retrieval/corrections_heldout.json`). The correction restates the fact with a new value, worded with a
   held-out opening or ending (half each), in the latest free out-of-view slot after the fact; the old value is never
   named. Some endings are mild ("i think", "lol sorry"); they were chosen by the rule and stay. sha256 of the source
   of `corrected_heldout`, `_worded`, `_corrected` and the wordings file: `81b545144c1b5da7f6b622ad68f25c2192b1d6ced00c2564505b862aeea94544`. `corrected` was refactored onto
   the same helper; it returns identical items on 1,200 checked (probe, `hard_dev`, train; 200 seeds each kind).
2. **Training transform, `stress.corrected_for_training`**: training's wordings only, any free out-of-view slot after
   the fact except the latest; tests check no training wording shares a content word with a held-out one.
3. **Baseline, before any arm row is built**: v6 at 82 and 83, and base, on `corrected_heldout`, both pools, scoring
   only.
4. **The arm**: about 170 rows appended to v6's set (`strict_chat.jsonl`), scripted targets, every existing row
   byte-identical: about 110 `corrected_for_training` rows (`older`, `confirm`); about 30 rows whose search returns a
   same-type fact about another person introduced by a training correction opening, answered with the asked person's
   own value, so the opening is not a cue; about 30 `asked_before` rows (no gain claim; `in_view` guarded). Cue
   balance and decoy counts as R-020 and R-099, counts reported. One dose, one try, 17m's recipe.
5. **Gain that counts** on `corrected_heldout`, against v6 at the same seeds: pooled over 82 and 83 at least **48 of
   192 on the probe and 32 of 192 on `hard_dev`**, and above v6 at each seed; at 91, 92 and 93 each seed at least 24
   of 96 (probe) and 16 of 96 (`hard_dev`) above v6's 82-and-83 mean.
6. **Guards**: R-086's gate at 82 and 83, R-094's slip gate (pooled over 82, 83, 91, 92, 93), R-097's stop rule,
   R-076's rule at 91 to 93, all word for word. Phone form: pooled over 82 and 83 not below v6 by more than 8 of 192
   (probe) or 16 of 192 (`hard_dev`); at 91 to 93 each probe seed within 4 of 96 of v6's 82-and-83 mean, and the
   `hard_dev` three-seed mean within 8 of 96 of it. R-099's original phone-gain test is reported beside, whatever it
   shows; plain `corrected` and plain `confirm` reported.
7. **Frozen.** These numbers do not change after the baseline is seen; if the baseline makes one unreachable, the arm
   is reported as not shippable and the number stays.
8. **Clock**: arm not started by Sunday, November 8, 12:00 = dropped; nothing starts after Monday 12:00.
9. **Write-up**: the amendment, its date and reason; the held-out wordings from a blind agent, the form from the
   builder after the battery; corrections, phone typing and asked-before reported as measured, base beside them,
   whatever the arm does.

## R-103 · 2026-11-06 · SPRINT · Two-stage training: build on a failed fix instead of restarting from v6

**When.** Friday, November 6, about 18:10, while 6.1 (below) was training and before any of its results existed.

**Who decided.** Kevin, in three messages:

- "train v6 up like you've been doing apply the fix to make it v7 and train v7 on what's fucked up to get a working
  v7.1 as the final copy instead of 1 step make it 2 steps"
- "i'm saying "pass it" temporarily then train the passed model instead of retraining the one that just failed"
- "lets call it 6.1 as the tstepping stone and 6.11 if it's a second stepping stone 6.2 if it's a new stepping stone
  .21 if the new stepping stone with a second added stepping stone"

**The decision.** A fix that fails a gate is no longer thrown away. It is kept as a stepping stone, and the next step
trains on top of it, from its saved adapter, on new rows aimed at what it broke. A stepping stone is not a candidate:
it is not gated and is never shipped. Only the final copy runs the full registered gate, unchanged: R-086's gate at
seeds 82 and 83, R-094's slip gate, R-097's stop rule and R-076's rule at fresh seeds, plus R-102's corrections measure
for a copy that carries the corrections fix.

**Why.** Every fix since v6 restarted from v6, so a fix that improved one thing and broke another lost both. Fix C2
removed the who-is-who slip at both seeds (0 of 96, against v6's 3 and 4) but fell below v6's `hard_dev` recall, and
was discarded with its gain (R-101); C1 missed by one recall answer (R-098); fix A by one judged line (R-095). Building
on the stone keeps what it fixed and spends the next step only on what it broke. Training in stages is ordinary
practice; what keeps it honest here is that the gates do not move and only the final copy is judged by them.

**Names.** A tree off v6; each digit after the point is one training step:

| Name | Meaning |
|---|---|
| 6.1 | v6 plus a first stepping stone |
| 6.11 | 6.1 trained further, a second stone on top of 6.1 |
| 6.2 | a different first stone, also from v6 |
| 6.21 | 6.2 trained further |

6.1 is the corrections arm (R-102), internal name `fix17cr`. Internal names (`fixNN`, adapter folders, results files)
stay as they are; the record gives each stone's tree name beside its internal one. Proposed, not yet ruled: the copy
that passes the full gate ships as v7.

**Rules for each step**, so stepping does not turn into training on the tests:

1. A step's rows come from the train pool only, built for the kind of failure the stone shows, never from the probe or
   `hard_dev` questions it got wrong.
2. Each step's design goes to an adversarial panel and into this record before it trains.
3. A child trains from its parent's adapter at the same seed (6.11 at seed 82 starts from 6.1's seed-82 adapter), so
   each seed is its own chain; training scripts gain an option to start from a saved adapter.
4. Every stone's seeds are counted as development candidates; the confirmation seeds (91 to 93) stay unused until the
   final copy.
5. The clock is unchanged: nothing starts after Monday, November 9, 12:00.

**Also recorded: R-102's baseline and one order slip.** `corrected_heldout`, older and confirm, of 96 a seed: v6 1 and 0
on the probe at seeds 82 and 83 (1 of 192), 5 and 0 on `hard_dev` (5 of 192); base 9 (probe) and 8 (`hard_dev`). So
6.1 needs at least 49 of 192 on the probe and 37 of 192 on `hard_dev` over 82 and 83 (R-102 item 5). Base on the other
messy forms (seed 73157): plain corrections 19 (probe) and 7 (`hard_dev`), v6 at 82 5 and 10; phone typing recall 32
and 20 (plain 30 and 20), v6 at 82 88 and 58. R-102 said the baseline would be scored before any arm row was built;
the rows were built and committed first (`scripts/records/build_r102.py`, commit c7cdecc), then the baseline was
scored. The rows were fixed before the baseline existed, so it could not shape them; the order is disclosed.

## R-104 · 2026-11-06 · SPRINT · 6.1 (`fix17cr`): the corrections stone's results and what it broke

**What ran.** 6.1 is R-102's corrections arm: v6's 800 rows plus 170 train-pool rows (110 corrections in training's
wordings, 30 correction-cue controls, 30 earlier-question rows; `scripts/records/build_r102.py`), trained from scratch
like v6 (3 epochs, 3e-4, `--loss-on chat_decision`; corrected from 2e-4 in R-105) at seeds 82 and 83 by the backlog runner, then scored on the plain
sets, the screen (seed 51203, seed 82 only), the held-out corrections form, the phone-typing form and the
training-worded corrections form. Every count below is printed by `scripts/records/stone_report.py fix17cr` and
`scripts/records/gate_r086.py fix17cr`; tool arm, older and confirm, of 96 a seed unless named.

| Measure | Base | v6 at 82, 83 | 6.1 at 82, 83 |
|---|---|---|---|
| Held-out corrections, probe | 9 | 1, 0 | 96, 96 |
| Held-out corrections, `hard_dev` | 8 | 5, 0 | 81, 78 |
| Training-worded corrections, probe | 19 | 5, 0 | 96, 96 |
| Phone typing recall, probe | 32 | 88, 90 | 91, 86 |
| Phone typing recall, `hard_dev` | 20 | 58, 74 | 79, 63 |
| Plain recall, probe | 30 | 96, 96 | 96, 96 |
| Plain recall, `hard_dev` | 20 | 74, 83 | 82, 69 |
| Who-is-who slips, probe | 2 | 3, 4 | 1, 2 |
| Who-is-who slips, `hard_dev` | 1 | 0, 3 | 4, 0 |

Base is one unadapted run (seed 73157 items), so its column is one number. On held-out corrections 6.1 is
+967% over base on the probe (96 against 9) and +894% on `hard_dev` (pooled 159 against 16); v6 was below base on
both.

**Against R-102's frozen bar** (82 and 83 pooled): held-out corrections 192 on the probe (bar 49) and 159 on
`hard_dev` (bar 37), above v6 at each seed; phone typing 177 on the probe against v6's 178 (allowed 8 below) and 142 on
`hard_dev` against v6's 132. All pass. These are development seeds; R-102's seeds 91 to 93 apply to the final copy.

**What 6.1 broke**, which a stone may do (R-103); these are 6.11's targets:

1. `hard_dev` recall pooled 151 against v6's 157, below R-094's line. The loss is at seed 83, older facts: 27 of 48
   against v6's 43. Of seed 83's 27 recall misses, 10 found the fact and replied without the asked detail ("Your
   housemate Joaquin got a job interview." asked for the weekday), 7 named the right value and another person's, 3
   gave a summary, 4 did not search and 3 searched and missed. Seed 82's 14 misses were 6 found-without-the-detail,
   5 search misses and 3 with no search. The split is `stone_report.py`'s own reading of each reply (search made,
   fact found, value named, length), not a judge's.
2. `hard_dev` who-is-who slips 4 at seed 82, over R-094's 3.
3. Screen recall 93 at seed 82, under R-086's 94; it is the only R-086 line 6.1 fails without judges.

The rest of R-086's unjudged gate passes: screen statement 48, `hard_dev` never_told 48, `hard_dev` recall pooled 151
(line 145), probe recall pooled 192 (line 189), false retrieval 0. No judged sheet was scored: a stone is not gated.

## R-105 · 2026-11-06 · SPRINT · 6.11's design: 6.1 plus the who-is-who answers, one gentle epoch on top

**Written** about 20:35, after 6.1's results (R-104) and before any 6.11 row is trained. One adversarial panel of four
lanes, one arguing against, reviewed the plan (agent transcript audited: it read no sealed file and changed nothing).

**Data.** 6.11 = `fix17cr11` = 6.1's 970 rows with fix C2's 41 rewritten final answers swapped in
(`scripts/records/build_r105.py`; the build stops unless each swapped row keeps its id, kind and every turn but the
last, and every other row is 6.1's byte for byte). No rows are added. Both sources are built from the train pool only
(R-098, R-102). Why this swap: all 4 of 6.1's `hard_dev` slips at seed 82 are the friend's-voice echo ("My goddaughter
Delphine collected the keys...") that fix C2's rewrites remove, and fix C2 and its parents (17w, 17y) had 0 `hard_dev`
slips at every seed they ran.

**Training.** From 6.1's adapter at the same seed (`--init-adapter adapters/screens/fix17cr_<seed>`, R-103), seeds 82
and 83, `--loss-on chat_decision`, **1 epoch at a peak learning rate of 1e-4**, the same linear decay to 0 and every
other setting as 6.1. Why: every run in the family is 3 epochs at 3e-4 decaying linearly, so its last epoch already
ran from 1e-4 to 0; one epoch at 1e-4 repeats one more such epoch. R-095 shows one such epoch can move both targets
(17m at seed 84: `hard_dev` recall 38 to 78 and probe slips 9 to 1 over its last epoch). A fresh epoch at 3e-4 on a
trained adapter would add a third of a whole run's learning; earlier 4-epoch runs lost statements (R-040, R-056). No
earlier run in the repo continues from a saved adapter, so the evidence for this choice is thin; it is the smallest
step the R-095 numbers show can still change slips and recall.

**Control**, reported and not gated: `fix17crx` = 6.1 with the same one epoch on its own unchanged set, at seeds 83
and 82. Without it, a 6.11 pass could be one more epoch, not the swap; R-095 shows a final epoch varies a lot by seed.

**What the panel expects.** The swap should remove the seed-82 slips. It probably does not fix seed 83's `hard_dev`
recall: fix C2 also misses about half the seed-83 items 6.1 misses and v6 gets right. No rows were added for seed
83's misses (found the fact, left out the detail asked for): rows shaped by what `hard_dev` got wrong would break
R-103's rule 1 in spirit.

**How 6.11 is judged.** It is a candidate for the final copy, so at 82 and 83 it runs the full registered gate:
R-086 (with its judged sheets), R-094's slip gate and recall line, R-097's stop rule and R-102's corrections measure,
unchanged. If it passes, the fresh-seed chain is: 6.1 trained from scratch at seeds 91, 92 and 93, not scored, then
6.11 trained from each, then R-076's rule and R-102's seed-91-to-93 items on 6.11 only.

**Two rules added before training, at the panel's against-lane's request:**

1. If 6.11 fails, no further stone (6.111) is built from the same seed-82/83 reading without a new panel and record,
   so the tree does not turn into repeated draws against the gate.
2. Two of 6.1's three misses are one answer (screen 93 against 94) and one slip (4 against 3); a pass at 82 and 83 by
   such margins is read as development noise until seeds 91 to 93 confirm it. Only those seeds count as evidence.

**Correction.** R-104 said 6.1 trained at 2e-4, as did the panel's brief; the training reports
(`results/recall_train/fix17cr_82.json`, `fix17m_82.json`) show 3e-4, the runner's setting. R-104 is corrected in
place. Nothing was trained or scored on the wrong figure.

## R-106 · 2026-11-07 · SPRINT · 6.11 misses one line by two answers; the control credits the swap

**What ran** (R-105's design, unchanged): 6.11 (`fix17cr11`) and the control (`fix17crx`), each one epoch at a peak of
1e-4 from 6.1's adapter at the same seed; the runner's reports confirm `init_tensors_loaded` 504 and
`adapter_changed` true at every seed. `--loss-on chat_decision` keeps full loss on older rows, so the 41 swapped
answers were trained (only statement rows are cut to the decision). 6.11 then ran the held-out corrections and
phone-typing forms at both seeds. Counts from `scripts/records/stone_report.py` and `scripts/records/gate_r086.py`
(older and confirm, of 96 a seed):

| Measure | v6 at 82, 83 | 6.1 | 6.11 | Control |
|---|---|---|---|---|
| Plain recall, probe | 96, 96 | 96, 96 | 95, 95 | 96, 96 |
| Plain recall, `hard_dev` | 74, 83 | 82, 69 | 85, 75 | 86, 68 |
| Slips, probe | 3, 4 | 1, 2 | 0, 0 | 1, 1 |
| Slips, `hard_dev` | 0, 3 | 4, 0 | 0, 0 | 6, 2 |
| Screen recall (seed 82) | | 93 | 95 | 95 |
| Held-out corrections, probe | 1, 0 | 96, 96 | 95, 95 | |
| Held-out corrections, `hard_dev` | 5, 0 | 81, 78 | 85, 82 | |
| Phone typing recall, probe | 88, 90 | 91, 86 | 92, 87 | |
| Phone typing recall, `hard_dev` | 58, 74 | 79, 63 | 74, 69 | |

**6.11 against the gate at 82 and 83.** R-086's unjudged lines all pass (screen recall 95, statement 48, `hard_dev`
never_told 45, `hard_dev` recall pooled 160, probe recall pooled 190, false retrieval 3). R-094's slip lines all
pass (0 at every seed on both sets) and `hard_dev` recall is 160 against v6's 157. R-102's bar passes (held-out
corrections 190 and 167 of 192; phone typing 179 and 143 against v6's 178 and 132). **One line fails: probe recall
pooled 190 against v6's 192** (R-094, "not below v6"). v6 answered every probe recall question at both seeds, so the
line asks for none missed. 6.11's two misses: at seed 82 it searched "sister steps" for a question about a
stepsister and found nothing; at seed 83 it did not search for a vaguely worded question ("drawing a blank on my
classmate's tattoo"). By R-105's rule 2 a result this close is read as noise until fresh seeds; the gate is not
changed, and the judged sheets were not scored for a copy that fails an unjudged line.

**The control** fails twice (`hard_dev` slips 6 at seed 82, `hard_dev` recall 154), so the extra epoch alone does not
remove the slips: the swap is what took them from 6 and 2 to 0 and 0 and lifted `hard_dev` recall from 154 to 160.
The control kept the probe at 192; the swap may have cost the two probe answers, or they may be the noise one epoch
adds (R-095).

**Corrections survive the step:** 6.11 keeps 6.1's gain on held-out corrections (+956% over base on the probe, 190
against 18 pooled; +944% on `hard_dev`, 167 against 16).

**Kevin, 2026-11-06 about 22:40,** after 6.11's plain counts: "there is no standing yet". No copy is final before the
freeze; a stone that misses a line is followed by another step, under R-105's rule that each needs a new panel.
**Next:** that panel (R-107) designs the step after 6.11.

`stone_report.py` now skips the messy-form lines until every seed's file exists (it stopped with an error on 6.11
before its messy-form runs finished); 6.1's output is unchanged byte for byte.

## R-107 · 2026-11-07 · SPRINT · 6.111 designed by a new panel; the next try and the fresh-seed reading fixed now

**Written** about 01:00 Saturday, after R-106 and before any 6.111 step trains. R-105's rule 1 requires a new panel
before a stone after 6.11; one ran (four lanes, one against; transcript audited: it read `pools.py` lines 1 to 451
only, no token file, and changed nothing).

**What the panel found.**

- The probe line has a ceiling. v6 is 192 of 192, so "not below v6" asks for no probe recall miss. Since v6, 9 of
  12 candidate seeds at 82 and 83 scored 96 of 96 (fix17w 2, 17y 1, 17z 2, 6.1 2, control 2, 6.11 0), so a copy no
  worse than v6 misses the line about a third of the time.
- 6.1 and the control both scored 192; the swap changes final answers, not searches. The panel reads 6.11's two
  misses as draw noise, not harm from the swap. That is a reading, not a measurement.
- **Rows aimed at the two probe misses are ruled out** (option B). In 6.11's set, all 556 search rows that name a
  relation put that word in the query unchanged; the train pool has 8 simple relations, and
  `tests/test_conversations.py::test_the_pools_share_no_content` forbids sharing relations with the probe or
  `hard_dev`. `train_phrasings.py` keeps "drawing a blank" and similar out of training on purpose, so the probe can
  measure wordings training never used. Rows built for compound relation words or that idiom would be built from
  the probe questions 6.11 got wrong (R-103 rule 1).

**The step.** 6.111 = `fix17cr111`: 6.11's 970 rows byte for byte (`data/screens/fix17cr11.jsonl`), nothing added,
from 6.11's adapter at the same seed, 1 epoch at a peak of 1e-4 with the same linear decay and every other setting as
6.11, `--loss-on chat_decision`, seeds 82 and 83. It is a re-run of one more gentle epoch with no target. The only
measured evidence for such an epoch is at 1e-4, and it raised `hard_dev` both times it ran (6.1 151 to the control's
154 and to 6.11's 160). A smaller rate would be a number no run in the repo has tested. The panel put the chance of
passing every line at 82 and 83 at 20 to 30%, a judgement, not a measurement.

**Recorded before it trains:**

1. 6.111 adds no data. A pass at 82 and 83 is one more draw against a perfect-probe line and counts as evidence only
   at seeds 91 to 93 (R-105 rule 2). Candidate seeds read at 82 and 83 since R-093: fix17w, 17y, 17z, 6.1, the
   control and 6.11, two seeds each; 6.111 is the seventh. The write-up reports that count.
2. **If 6.111 fails any line at 82 or 83, the next try is 6.2**, fixed now so it is not chosen after seeing which
   line failed: v6's 800 rows with fix C2's 41 answers, plus 6.1's 170 rows (exactly `fix17cr11.jsonl`), trained from
   scratch like v6 (3 epochs, 3e-4, `--loss-on chat_decision`) at 82 and 83, under the same full gate. No 6.1111 is
   built from the same reading.
3. **Fresh seeds.** For a copy that passes at 82 and 83, each of seeds 91, 92 and 93 retrains its chain (6.1 from
   scratch, then 6.11, then 6.111, each step as at 82 and 83) and only the last copy is scored. To save time, 6.1 and
   6.11 are trained at 91 to 93 now, unscored; nothing at those seeds is scored until the copy that uses them is
   chosen.
4. **R-094's recall line at fresh seeds, read literally.** R-094 says recall not below v6's "at the same seeds", and
   v6 has never run at 91 to 93. v6 is trained at 91, 92 and 93 with its own recipe (`strict_chat.jsonl`, 3 epochs,
   3e-4, `--loss-on chat_decision`) and scored on the plain sets, so the line compares at the same seeds. This is
   the stricter of the two readings (the other compares against v6's 82 and 83); it was chosen by Claude without Kevin,
   since it cannot flatter a candidate, and is his to overrule. v6's runs at 91 to 93 select nothing.

**Clock.** 6.111 at 82 and 83 by about 03:30, its messy forms by about 05:00, then v6 and the pre-trained chain at
91 to 93. If 6.111 fails, 6.2 replaces it in the queue.

## R-108 · 2026-11-07 · SPRINT · 6.111 fails two lines; 6.2 runs as fixed in R-107

**What ran** (R-107's design, unchanged): 6.111 (`fix17cr111`), one epoch at a peak of 1e-4 from 6.11's adapter on
6.11's own 970 rows, seeds 82 and 83, scored about 02:50 Saturday. Counts from `scripts/records/stone_report.py` and
`scripts/records/gate_r086.py` (older and confirm, of 96 a seed):

| Measure | v6 at 82, 83 | 6.11 | 6.111 |
|---|---|---|---|
| Plain recall, probe | 96, 96 | 95, 95 | 93, 96 |
| Plain recall, `hard_dev` | 74, 83 | 85, 75 | 84, 69 |
| Slips, probe | 3, 4 | 0, 0 | 0, 1 |
| Slips, `hard_dev` | 0, 3 | 0, 0 | 0, 0 |
| Screen recall (seed 82) | | 95 | 94 |

**Against the gate.** R-086's unjudged lines all pass (screen recall 94, statement 48, `hard_dev` never_told 46,
`hard_dev` recall pooled 153, probe recall pooled 189, false retrieval 3). R-094's slip lines all pass. **Two lines
fail:** probe recall pooled 189 against v6's 192, and `hard_dev` recall pooled 153 against v6's 157. The extra epoch
moved both recall sets down from 6.11 (190 to 189, 160 to 153); seed 83's `hard_dev` misses are mostly "found the
fact, answered without the detail asked" (15 of 27). The three probe misses at seed 82: no search for "drawing a blank
on my daughter's tattoo"; a search for "sister tickets festival" on a stepsister question that found nothing; and one
reply that is a malformed tool call naming a tool that does not exist (`search_cuphor`), which the tool loop did not
run. The messy-form runs were not needed for the verdict; they are moved behind 6.2's and run when the queue reaches
them, reported and not gated.

**Next, as R-107 rule 2 fixed before this result:** 6.2 = `fix17cs2`, `data/screens/fix17cr11.jsonl` (v6's 800 rows
with fix C2's 41 answers, plus 6.1's 170 rows) trained from scratch like v6 (3 epochs, 3e-4, `--loss-on
chat_decision`) at 82 and 83, then its held-out corrections and phone-typing forms, under the same full gate. No
6.1111 is built. 6.2 is the eighth candidate read at 82 and 83 since R-093.

**Queue changes, made after this result.** 6.1 and 6.11 were to be pre-trained at 91 to 93 for 6.111's fresh-seed
chain (R-107 rule 3); with 6.111 failed no chain uses them, so those six runs are dropped and 6.2 is pre-trained at 91
to 93 instead, unscored. v6 at 91 to 93 stays (R-107 rule 4). Nothing at 91 to 93 is scored until a copy passes at 82
and 83. These change what runs, not any line of the gate.

## R-109 · 2026-11-07 · SPRINT · 6.2 passes the whole gate at 82 and 83; fresh seeds next

**What ran** (R-107 rule 2, unchanged): 6.2 = `fix17cs2`, `data/screens/fix17cr11.jsonl` (970 rows) trained from
scratch like v6, 3 epochs at 3e-4, `--loss-on chat_decision`, seeds 82 and 83, then its held-out corrections and
phone-typing forms. Scored 03:52 and 04:41 Saturday; the messy forms by 05:40.

**Counts** (`scripts/records/stone_report.py fix17cs2`, `scripts/records/gate_r086.py fix17cs2`; older and confirm, of
96 a seed):

| Measure | Base | v6 at 82, 83 | 6.2 at 82, 83 |
|---|---|---|---|
| Plain recall, probe | 30 | 96, 96 | 96, 96 |
| Plain recall, `hard_dev` | 20 | 74, 83 | 85, 81 |
| Slips, probe | 2 | 3, 4 | 0, 0 |
| Slips, `hard_dev` | 1 | 0, 3 | 0, 0 |
| Screen recall (seed 82) | | 95 | 96 |
| Held-out corrections, probe | 9 | 1, 0 | 96, 96 |
| Held-out corrections, `hard_dev` | 8 | 5, 0 | 85, 84 |
| Phone typing recall, probe | 32 | 88, 90 | 87, 89 |
| Phone typing recall, `hard_dev` | 20 | 58, 74 | 77, 73 |

- R-086's unjudged lines all pass: screen recall 96 (needs 94), statement 48 (47), `hard_dev` never_told 48 (44),
  `hard_dev` recall pooled 166 (145), probe recall pooled 192 (189), false retrieval 1 (at most 6).
- R-094 passes: slips 0 at every seed on both sets; probe recall 192 against v6's 192, `hard_dev` 166 against 157.
- R-097's stop rule passes: probe `in_view` 45 and 43 (below 41 stops).
- R-102 passes: held-out corrections 192 and 169 of 192 against v6's 1 and 5 (needs v6 + 48 and v6 + 32, and above v6
  at each seed); phone typing 176 and 150 against v6's 178 and 132 (within 8 and 16).

Against base, pooled over both seeds: probe recall +220% (192 against 60), `hard_dev` recall +315% (166 against 40),
held-out corrections +967% on the probe (192 against 18) and +956% on `hard_dev` (169 against 16).

**Judged** (`results/coherence/R-109/`, shuffle seeds 90530 to 90533; three fresh Sonnet judges, each marking all four
sheets in its own folder under R-095's rubric and brief; base is `three_exchanges`; judge 1 decides). Transcripts
audited: each judge read only its own folder's rubric and sheets, and its one script wrote marks it had listed line by
line.

| Sheet | Judge 1: base, 6.2 | Judge 2 | Judge 3 |
|---|---|---|---|
| Probe Sheet B `statement` | 45, 46 | 44, 47 | 44, 46 |
| Probe Sheet B `in_view` | 35, 40 | 35, 45 | 33, 43 |
| `hard_dev` Sheet B `statement` | 45, 48 | 45, 48 | 45, 47 |
| `hard_dev` Sheet B `in_view` | 38, 39 | **43, 41** | 40, 46 |
| Check set, seed 82 | 44, 44 | 45, 44 | 45, 44 |
| Check set, seed 83 | 44, 47 | 45, 47 | 45, 47 |

**6.2 passes every judged item under judge 1**, the registered decider (check set pooled 91 against base's 88), and
under judge 3. **Judge 2 would fail one item**: `hard_dev` Sheet B `in_view`, 41 against base's 43. The rule is not
changed; the split is reported, as R-095 reported fix17w's (where judge 1 failed it and judges 2 and 3 passed it).

**6.2 is the first copy since v6 to pass every registered line at 82 and 83**, and the eighth candidate read there
since R-093 (R-107 rule 1). By R-105 rule 2 this is development evidence only; seeds 91 to 93 decide.

**Next.** At 91, 92 and 93: 6.2 trained from scratch with the same recipe and scored on the plain sets, the held-out
corrections and the phone form; v6 at the same seeds (R-107 rule 4); then R-076's rule with Sheets A, B and h judged
by fresh judges, R-094's slip gate pooled over 82, 83 and 91 to 93, and R-102's seed-91-to-93 items. The 6.1 and 6.11
chain is not used. 6.111's remaining messy-form runs follow, reported only.

## R-110 · 2026-11-07 · SPRINT · 6.21's design: found lines that say more than the asked detail

**Kevin, 2026-11-07 about 05:55,** after 6.2 passed every line at 82 and 83: "a candidate for 6.21 either way".
6.21 is built on 6.2 whether or not 6.2 passes at 91 to 93. One panel of four lanes, one arguing against, designed it
(transcript audited: it read `pools.py` lines 1 to 451 only, its one outline of that file filtered to lines below 452
before display, no token file; it wrote only in its scratch folder).

**What the panel found.**

- In 6.2's set all 350 found-fact answers name the found value, and the 110 correction answers name the new value; but
  every passage is one short fact line (1,252 of 1,475 passage lines are 40 to 80 characters). No row shows a line
  that holds two facts, or a fact among other talk. `hard_dev` states facts in long run-on lines on purpose.
- Read for diagnosis only (no row was built from them): 6.2's `hard_dev` misses of the kind "found the fact, answered
  without the asked detail" come from three `hard_dev` fact types; 13 of 19 are one of them (a dinner hosted, the
  dish not named), 5 another (an interview, the weekday not named). The same items fail at both seeds, and `hard_dev`
  is scored on the same items (probe seed 73157) at every training seed, so seeds 91 to 93 read them again. **The
  multi-detail form was chosen after reading `hard_dev` misses by kind**; it is a failure kind (R-103 rule 1), and
  the shapes of the missed template (an event first and its value at the end: hosted, served, booked, dishes,
  weekdays) are kept out.
- Ruled out: phone-typed rows (R-099: `phone_style` never enters training; it is the held-out measure) and a gentle
  epoch with no data (6.11 and 6.111 show it is a re-draw).

**Data.** 6.21 = `fix17cs21`: 6.2's 970 rows byte for byte (`data/screens/fix17cr11.jsonl`) plus 100 rows from
`scripts/records/build_r110.py` (train pool only, fresh conversations, the real search tool, scripted answers):

- 40 `two`: the fact line also states a second fact of another type about the same person; the question asks one,
  the asked fact first in 20 and second in 20; `older` and `confirm` alternate.
- 40 `runon`: the fact line joined with one or two of the pool's small-talk lines, the fact first, in the middle or
  last (about a third each).
- 20 `never`: `never_told` questions whose returned passages include such a line about another person, so a long
  passage is not a cue that the answer is there.
- Decoy counts as R-020 (0 to 2 found, 1 to 3 not found). Coffee orders are left out (no food or weekday values).

**Vetting.** The build stops if an answer leaves out the asked value, names the line's other value, or has the
who-is-who slip shape, or if 6.2's rows change; a row whose search does not return its changed line (1), whose
row is over 1,024 tokens (1), or whose changed line shares a four-word run with the probe or `hard_dev` pools (9) is
skipped. Two of the pool's own small-talk lines and three of its fact wordings already share such a run with those
pools, in 6.2's rows; the panel's rule (no shared run) was applied as a skip, so the step adds none. The build is
deterministic (two runs, same SHA-256 `f62f0c9b7171…`). No phone-typing or held-out correction form is used. One fresh Sonnet judge, reading only the 100 rows' questions, search results and answers (`results/vet/R-110/`), marked all 100 as naming exactly the asked detail, or saying it does not know where nothing was found; transcript audited (it read its two files whole and wrote only its marks).

**Training.** From `adapters/screens/fix17cs2_<seed>` (`--init-adapter`), 1 epoch at a peak of 1e-4 with linear decay
to 0, `--loss-on chat_decision`, every other setting as 6.2; the report must show `init_tensors_loaded` 504 and
`adapter_changed` true. Seeds 82 and 83. **Control** `fix17cs2x`: the same epoch on 6.2's 970 rows alone, at 82 and
83, reported and not gated.

**Order on the GPU.** v6 and 6.2 at 91 to 93 are not pre-empted. Then 6.21 at 82 and 83, the control, and 6.21's
held-out corrections and phone forms. If 6.21 passes the whole gate there (R-086 counts and judged sheets, R-094,
R-097, R-102), 6.21 is trained at 91 to 93 from `fix17cs2_91` to `_93` and judged as 6.2 is.

**Recorded before it trains:**

1. 6.21 is the ninth candidate read at 82 and 83 since R-093; its control is counted beside it. A pass there is
   development evidence only (R-105 rule 2).
2. **If 6.2 fails at 91 to 93**, 6.21 goes to 91 to 93 through 6.2's adapters there (R-103 rule 3); the write-up
   says two related candidates were read on the confirmation seeds. If 6.21 passes, it replaces v6 (R-094's ruling).
3. **If both pass at 91 to 93: proposed, for Kevin to rule before any 91-to-93 result is read.** R-088's ship rule
   as written: 6.21 has one more change than 6.2, so 6.2 ships unless 6.21's pooled `hard_dev` recall at 91 to 93
   (of 288, the same seeds) is higher by more than 15. The against lane adds a guard, which the others accept: a
   gain that comes mostly from one `hard_dev` fact type does not count, and any gain is reported by fact type.
4. No 6.211 or 6.22 is built from this reading without a new panel.
5. The panel's estimates, judgements and not measurements: about 30% that 6.21 passes every line at 82 and 83, about
   50% that a pass there holds at 91 to 93. The lines most likely to fail at 91 to 93, for 6.2 or 6.21, are judged
   (`hard_dev` Sheet B `in_view`, 39 against base's 38 under judge 1) and the phone guard; neither can be trained for
   without moving a gate.

**Clock.** 6.21 and its control at 82 and 83 by about 15:00 Saturday; 6.21 at 91 to 93, if it gets there, by about
18:30. Nothing starts after Monday 12:00.

## R-111 · 2026-11-07 · SPRINT · Kevin's ruling: the better of 6.2 and 6.21 is the base for 7

**Kevin, 2026-11-07 about 07:40,** asked about R-110 rule 3 (which one ships if both pass at 91 to 93): "whichever
performs better could go in as the base for 7". **Written at 07:42, before any result of 6.2 or 6.21 at 91 to 93 was
read.** v6's runs at 91 to 93 were being scored; none of their results had been read either.

**This replaces R-110 rule 3.** R-088's lead for the copy with fewer changes (6.21 needing more than 15 more) is
dropped, at Kevin's word. The measure is the one R-110's panel fixed; only the margin changes.

1. **Both must pass every line at 91 to 93** (R-076 with Sheets A, B and h judged, R-094 pooled, R-097, R-102's
   seed-91-to-93 items). The gates do not move. A copy that fails is not a base for 7.
2. **If both pass, "better" is pooled `hard_dev` recall at 91 to 93** (older and confirm, of 288, the same seeds). It is
   the measure with room left: probe recall is at or near its ceiling (192 of 192 at 82 and 83 for both v6 and 6.2).
3. **An exact tie** goes to fewer slips pooled over probe and `hard_dev` at 91 to 93, then to 6.2, which has one change
   fewer. No margin is added; none was registered, and Kevin's word sets none.
4. **Reported, not deciding:** the gap by `hard_dev` fact type (R-110's guard, kept as a report line), and that a gap of
   a few items is within one copy's seed spread (6.2's `hard_dev` recall was 85 and 81 at 82 and 83).
5. **If only one passes,** that one is the base for 7 (for 6.21 alone, as R-110 rule 2). **If neither passes,** neither
   is, and the next step goes to a new panel.
6. **7** is the next version, built on the chosen copy. Its design is not fixed here. The model freeze (Tuesday
   November 10) and "nothing starts after Monday 12:00" still hold.

## R-112 · 2026-11-07 · SPRINT · 6.2 fails one judged line at seed 92; 6.21 goes to the fresh seeds

**What ran** (R-109's next step, unchanged): 6.2 = `fix17cs2` trained from scratch at 91, 92 and 93 with its recipe,
scored on the plain sets, the held-out corrections and the phone form; v6 (`fix17m`) at the same seeds on the plain
sets (R-107 rule 4). Scored by 12:13 Saturday. R-111 was written before any of these results was read.

**Counted lines** (`scripts/records/fresh_report.py fix17cs2`, new; older and confirm, of 96 a seed):

| Measure | Base | v6 at 91, 92, 93 | 6.2 at 91, 92, 93 |
|---|---|---|---|
| Plain recall, probe | 30 | 94, 96, 96 | 96, 96, 96 |
| Plain recall, `hard_dev` | 20 | 81, 81, 76 | 87, 82, 75 |
| Slips, probe | 2 | 5, 0, 2 | 0, 1, 0 |
| Slips, `hard_dev` | 1 | 2, 4, 2 | 0, 0, 0 |
| Probe `statement` (of 48) | | 48, 48, 48 | 47, 43, 47 |
| Held-out corrections, probe | 9 | (1, 0 at 82, 83) | 94, 93, 96 |
| Held-out corrections, `hard_dev` | 8 | (5, 0 at 82, 83) | 86, 83, 82 |
| Phone typing recall, probe | 32 | (88, 90 at 82, 83) | 89, 88, 89 |
| Phone typing recall, `hard_dev` | 20 | (58, 74 at 82, 83) | 80, 76, 67 |

- R-094 passes: slips at most 1 a seed on either set; probe slips pooled over 82, 83 and 91 to 93 are 1 (at most 8);
  recall pooled at 91 to 93 not below v6 at the same seeds (probe 288 against 286, `hard_dev` 244 against 238).
- R-102's seed-91-to-93 items pass: held-out corrections at least 24.5 (probe) and 18.5 (`hard_dev`) every seed;
  phone probe every seed within 4 of v6's 89; phone `hard_dev` three-seed mean 74.3 against v6's 66.
- R-076's counted items pass: probe recall 288, `in_view` 125, `statement` 137 (needs 136), right decisions 239, 235
  and 239, false retrieval 0; `hard_dev` recall 244, false retrieval 5, `never_told` 140.

Against base, pooled over the three seeds: probe recall +220% (288 against 90), `hard_dev` recall +307% (244 against
60), held-out corrections +948% on the probe (283 against 27) and +946% on `hard_dev` (251 against 24).

**Judged** (`results/coherence/R-112/`, shuffle seeds 90534 to 90542; Sheet A against base's `tool_loop` replies,
Sheets B and `hard_dev` B against base's `three_exchanges`, as R-093; three fresh Sonnet judges a sheet type, each
marking its three seeds in its own folder under R-095's rubric and brief; judge 1 decides). Transcripts audited:
every judge read only its own folder's rubric and sheets, and its code wrote only marks it had listed line by line.
Two notes: the Sheet A judge 2 marked exactly 18 zeros on each of its three sheets (the marks differ on 34 and 36
lines, so they were not copied); the `hard_dev` judge 1 created an empty file one folder up and deleted it at once.

| Item | Judge 1 | Judge 2 | Judge 3 |
|---|---|---|---|
| 1f Sheet A confirm; older plus confirm, 6.2 vs base | 144 vs 141; 287 vs 237 | 144 vs 141; 288 vs 234 | 144 vs 141; 287 vs 238 |
| 1g Sheet B `statement`, seeds 91, 92, 93 | 47/46, **42/46**, 47/46 | 47/46, **42/46**, 47/46 | 47/45, **42/45**, 46/45 |
| 1g Sheet B `in_view`, seeds 91, 92, 93 | 41/34, 41/34, 44/34 | 43/36, 39/36, 42/36 | 43/35, 38/35, 42/35 |
| 6 `hard_dev` Sheet B, pooled `statement`; `in_view` | 135 vs 132; 132 vs 123 | 134 vs 132; 127 vs 114 | 135 vs 129; 132 vs 120 |

**6.2 fails R-076 item 1g at seed 92**, under all three judges: 42 coherent `statement` replies against base's 46 (the
rule needs at or above base at every seed). Every other item passes under every judge. The rule is not changed.

**What failed, read for diagnosis only.** 5 of seed 92's 6 judged `statement` failures and the 1 each at 91 and 93
are one shape: the friend states something with no question ("Hana forgot my birthday again", "i should really call my
barber"), 6.2 searches ("Hana born birthday month") and answers with an unrelated stored fact about that person ("Your
barber Hana grows prize zucchini."). Four of seed 92's are the "forgot my birthday" statement; its sixth is a reply
with no search ("It sounds like you're trying to remember something about your godfather."). v6 answered all 48
statements at every fresh seed. No row is built from these items (R-103 rule 1).

**What follows, as fixed before this result:**

1. 6.2 is not a base for 7 (R-111 rule 1).
2. 6.21 goes to 91 to 93 through 6.2's adapters there (R-110 rule 2); the write-up says two related candidates were
   read on the confirmation seeds. If 6.21 passes every line at 82, 83 and 91 to 93, it replaces v6 and is the base
   for 7 (R-111 rule 5).
3. To save time, 6.21 is trained at 91, 92 and 93 now, right after its 82 and 83 runs, and **not scored** until it has
   passed at 82 and 83 (R-108). Its held-out and phone runs at 82 and 83 were moved ahead of its control, which is
   reported and not gated. These change the order on the GPU, not any line of the gate.
4. 6.21's rows were built before this result and do not touch the statement shape; whether one gentle epoch on them
   moves it is read at 91 to 93, not assumed.

## R-113 · 2026-11-07 · SPRINT · 6.21 fails R-094 at 82 and 83; neither stone is a base for 7

**What ran** (R-110, unchanged): 6.21 = `fix17cs21`, one epoch at a peak of 1e-4 from `fix17cs2_82` and `_83` on 6.2's
970 rows plus R-110's 100 rows. Both train reports show 1,070 rows, `init_tensors_loaded` 504 and `adapter_changed`
true. Scored by 13:27 Saturday (`scripts/records/stone_report.py fix17cs21`, `scripts/records/gate_r086.py fix17cs21`).

| Measure (seeds 82, 83) | Base | v6 | 6.2 | 6.21 |
|---|---|---|---|---|
| Plain recall, probe | 30 | 96, 96 | 96, 96 | 96, 96 |
| Plain recall, `hard_dev` | 20 | 74, 83 | 85, 81 | 81, 74 |
| Slips, probe | 2 | 3, 4 | 0, 0 | 0, 0 |
| Slips, `hard_dev` | 1 | 0, 3 | 0, 0 | 0, 1 |
| Probe `statement` (of 48) | 31 | 48, 46 | 48, 47 | 48, 48 |
| Probe `in_view` (of 48) | 34 | 41, 45 | 45, 43 | 44, 46 |
| `hard_dev` misses: found, answered without the asked detail | | | 7, 11 | 9, 20 |

- R-086's unjudged gate passes (probe 51203 recall 96, statement 48; `hard_dev` recall pooled 155, at least 145).
- R-094's slip lines and probe recall line pass (slips 0 and 1; probe 192 against v6's 192).
- **R-094's `hard_dev` recall line fails: 155 against v6's 157.** The gate does not move. 6.21 is 11 below 6.2 at the
  same seeds (166).

**Read for diagnosis only.** R-110's rows targeted the "found the line, answered without the asked detail" kind. At these
seeds that kind rose from 18 misses (6.2) to 29 (6.21), 20 of them at seed 83. The rows did not fix the kind they aimed
at. The control (`fix17cs2x`, the same epoch on 6.2's rows alone) is running now and will show whether the epoch itself
or the added rows moved it. It is reported and not gated.

**What follows, as fixed before this result:**

1. 6.21 is not judged and does not go to 91 to 93 (R-108: a stone is scored at fresh seeds only after it passes at
   82 and 83). Its training at 91 was stopped at 13:35, and its eleven remaining lines (training at 91 to 93, held-out
   and phone forms at 82 and 83) were skipped. The control runs next, unchanged.
2. **Neither 6.2 nor 6.21 is a base for 7 (R-111 rule 5).** v6 stays the shipped model (R-093). The next step goes to
   a new panel, which is also the panel R-110 rule 4 requires before any 6.211 or 6.22.
3. The clock holds: model freeze Tuesday November 10; nothing starts after Monday 12:00.

## R-114 · 2026-11-07 · SPRINT · 6.3: one more try, from scratch; confirmation at 94 to 96

**Correction to R-113.** R-113 says 6.21's training at 91 was stopped at 13:35. It was not: a second copy of the
backlog runner, started on November 5 and still alive, restarted it at 13:29 and 13:35, next to the control's
training, and both ran on the card at once (steps of about 120 s instead of 1.2 s). The panel below found it. That
runner and its training were stopped at about 13:42 (by PID, processes this project started); the control's training
then ran at its normal 1.2 s a step. Its train report is checked before its result is read. The 6.21 seed-91 adapter
was deleted unfinished.

**The panel** (R-111 rule 5 and R-110 rule 4; four lanes, one arguing against; one agent; transcript audited: it read
`RECORDS.md`, the gate scripts, `runner.log`, the backlog and the training sets, opened no sealed or token file, and
wrote nothing in the repository. It tried to stop the second runner itself and was refused).

- **For trying again.** The failure is R-082's, R-085's and R-091's kind: a plain statement about a person read as a
  question. 6.2 has 150 statement rows of 970 (15.5%), against v6's 150 of 800 (18.8%); probe `statement` at seeds
  82, 83, 91, 92 and 93 is 48, 47, 47, 43 and 47 for 6.2, and 48, 46, 48, 48 and 48 for v6. This fits the failure,
  and does not prove its cause. Fix 19a's pair (R-083, R-086), built from that kind on November 5 from the train pool,
  held `hard_dev` recall where 18a's chat lines alone did not (R-085, R-089).
- **For training from scratch.** One-epoch steps at 1e-4 moved pooled `hard_dev` recall at 82 and 83 by +9, +3, −7
  and −11. That is wider than 6.2's lead over v6, and 19a's evidence comes from training from scratch.
- **Against (accepted as conditions).** Ten candidates have been read at 82 and 83 since R-093. A from-scratch draw
  puts every thin margin at risk again. The pair covers only the fact types `animals` to `race`. Re-reading 6.2 at new
  seeds would be seed shopping. So: one design, recorded before it trains; no branch picked after reading the control;
  on any fail v6 ships, unless a new panel fits a whole gate inside the clock.

**6.3 = `fix17cs3`** (`scripts/records/build_r114.py`; deterministic, two runs gave SHA-256 `d849a148c41a…`):

- 6.2's 970 rows (`data/screens/fix17cr11.jsonl`), byte for byte, first.
- The 57 `facts/statement_` rows of `data/screens/fix18a.jsonl`, byte for byte: a chat line naming a fact type,
  answered without a search.
- 52 of the 57 `indirect/older_` rows of `data/screens/fix19a.jsonl`: a question asked as a statement, answered from
  a search. 15 answers had the who-is-who slip shape and were rewritten to "Your <relation> <person>" as in R-094; all
  15 rewrites passed. 3 rows were skipped because their message or answer shares a four-word run with the probe or
  `hard_dev` pools (R-110's rule). One fresh Sonnet judge marked the 54 that were left under R-110's rubric
  (`results/vet/R-114/`; transcript audited, it read and wrote only its own folder): 52 right. 2 were rejected, each
  for adding a claim no passage makes ("someone at work brought up the furnace today"), and they were dropped. The
  panel's fallback (a scripted answer, judged again) was not built; dropping is the stricter choice.
- 1,079 rows; 207 statement rows (19.2%). Repeated last messages: 16 of the asks use a question wording that a 6.2
  row also uses, in a different conversation, as 6.2's own rows do; no row id repeats.
- Training: 6.2's recipe unchanged (3 epochs, peak 3e-4, rank 32 on attention and MLP, `--loss-on chat_decision`,
  every other setting as the runner's base), from no adapter. The train report must show 1,079 rows and
  `decision_rows` 207. Seeds 82 and 83; **seed 82 is the one to ship**.

**Confirmation seeds move to 94, 95 and 96.** Seeds 91 to 93 have been read (6.2's results there, and the failure
kind was diagnosed from seed 92). The eval items are the same at every training seed, so only the training seed can
be unread. 94 to 96 have never been trained. v6 is trained there for R-094's same-seed recall line. This is stricter
than R-110 and fixed before any result. R-102's fresh-seed thresholds are unchanged (they are anchored to v6's 82 and
83).

**Order on the GPU** (backlog lines 140 to 153; estimates):

1. The control `fix17cs2x` at 82 and 83, then 6.3 at 82 and 83 (about 17:30), then R-086's unjudged gate. A fail stops
   everything after it.
2. 6.3's held-out-correction and phone forms at 82 and 83 (8 runs), then v6 at 94 to 96 (about 21:30). R-086's judged
   sheets run on the CPU meanwhile.
3. Only if 6.3 passes every line at 82 and 83: 6.3 at 94 to 96 and its 12 stress runs, then R-076's Sheets A, B and h
   (about Sunday 06:00).
4. Last, as a reported control: 6.2 at 94 to 96. Old filler lines (6.111's messy forms, `fix17r`, `fix17p`) are
   dropped.

Cut-offs: 6.3 at 94 to 96 must start by Monday 04:00. A new panel's next try is allowed only if its training at 82 and
83 can start by Sunday 22:00. Nothing starts after Monday 12:00.

**Recorded before 6.3 trains:**

1. **Pass at 82 and 83:** all of R-086 (counts and judged sheets b82, h82, c82 and c83, judge 1 deciding); R-094's
   slips, and recall not below v6's 192 (probe) and 157 (`hard_dev`); R-097's stop rule; R-102's 82-and-83 items.
   Reported, not gated: `statement` and `st_cc` counts at each seed.
2. **Pass at 94 to 96:** R-076's rule with Sheets A, B and h, three fresh judges a sheet type, judge 1 deciding;
   R-094's slips each seed, probe slips pooled over 82, 83 and 94 to 96 at most 8; recall pooled at 94 to 96 not below
   v6's at the same seeds, on both sets; R-102's fresh-seed items.
3. **On any fail:** stop. Nothing is judged after an unjudged fail. v6 ships for the freeze. No 6.31 or 6.4 without a
   new panel inside the cut-offs, and a failed copy is never read again at new seeds.
4. **On a full pass:** 6.3 seed 82 replaces v6 and is the base for 7, as Kevin's ruling for 6.2 and 6.21 (R-111).
5. **The control `fix17cs2x`** is reported only: it shows whether 6.21's drop (166 to 155) came from the extra epoch
   or from R-110's rows. It was not used to design 6.3 and does not change any line above.
6. **The write-up discloses:** the candidates read at 82 and 83 since R-093 (fix 17w, 17y, 17z, 6.1, 6.11, 6.111, 6.2,
   6.21 and 6.3, with the controls `fix17crx` and `fix17cs2x`); the fresh-seed reads (17b and 17m at 85 to 87, 6.2 at
   91 to 93, and 6.3 at 94 to 96 if it gets there); that 6.3's rows come from failure kinds read on development data;
   that the pair covers some fact types only; the 15 rewritten answers and 2 dropped rows; and the second runner.
7. **The panel's estimates, judgements and not measurements:** about 35% that 6.3 passes every line at 82 and 83;
   about 40% that a pass there holds at 94 to 96; about 14% for both (the against lane says about 10%).

## R-115 · 2026-11-07 · SPRINT · the control: the extra epoch and the added rows each cost recall

**What ran** (R-110's control, unchanged): `fix17cs2x`, one epoch at a peak of 1e-4 from `fix17cs2_82` and `_83` on
6.2's 970 rows alone. Both train reports show 970 rows, `decision_rows` 150, `init_tensors_loaded` 504 and
`adapter_changed` true. Seed 82's training took 943 s against seed 83's 624 s; it shared the card with the second
runner until about 13:42 (R-114). Scored by 14:57 Saturday (`scripts/records/stone_report.py fix17cs2x`).

| Measure (seeds 82, 83) | v6 | 6.2 | control | 6.21 |
|---|---|---|---|---|
| Plain recall, probe | 96, 96 | 96, 96 | 96, 96 | 96, 96 |
| Plain recall, `hard_dev` | 74, 83 | 85, 81 | 82, 78 | 81, 74 |
| Slips, probe | 3, 4 | 0, 0 | 2, 0 | 0, 0 |
| Slips, `hard_dev` | 0, 3 | 0, 0 | 0, 1 | 0, 1 |
| Probe `statement` (of 48) | 48, 46 | 48, 47 | 48, 48 | 48, 48 |
| `hard_dev` misses: found, answered without the asked detail | | 7, 11 | 5, 16 | 9, 20 |

**Read as a control only** (R-114 item 5; it does not change any line). Pooled `hard_dev` recall: 6.2 166, the
control 160, 6.21 155. The extra epoch alone cost 6; R-110's rows cost 5 more. The "answered without the asked detail"
kind rose with the epoch alone (18 to 21) and further with the rows (29). Two seeds, so this is a direction, not a
measured size. It is consistent with R-114's choice to train 6.3 from scratch rather than add an epoch.

## R-116 · 2026-11-07 · SPRINT · 6.3 fails at 82 and 83; Kevin's ruling on the tree and on stopping

**What ran** (R-114, unchanged): 6.3 = `fix17cs3` from scratch at 82 and 83. Both train reports show 1,079 rows,
`decision_rows` 207, 3 epochs at a peak of 3e-4. Scored by 16:54 Saturday (`scripts/records/stone_report.py
fix17cs3`, `scripts/records/gate_r086.py fix17cs3`).

| Measure (seeds 82, 83) | v6 | 6.2 | 6.3 |
|---|---|---|---|
| Plain recall, probe | 96, 96 | 96, 96 | 96, 96 |
| Plain recall, `hard_dev` | 74, 83 | 85, 81 | 85, 80 |
| Slips, probe | 3, 4 | 0, 0 | 0, **7** |
| Slips, `hard_dev` | 0, 3 | 0, 0 | 0, 1 |
| Probe `statement` (of 48) | 48, 46 | 48, 47 | 47, 48 |
| Probe `in_view` (of 48) | 41, 45 | 45, 43 | 43, 47 |

- **R-094 fails: probe slips at seed 83 are 7 (at most 5).** Every other R-094 line passes (pooled probe slips 7, at
  most 8; recall 192 against v6's 192 and `hard_dev` 165 against 157).
- **R-086 fails: probe 51203 `statement` is 45 (at least 47).** Every other unjudged R-086 line passes.
- Not judged (R-114 item 3: nothing is judged after an unjudged fail). The runner's stop file skipped 6.3's eight
  stress runs and the guarded v6 lines.

**Read for diagnosis only.**

- All 7 slips at seed 83 are one shape no earlier copy produced at that seed (v6, 6.2, 6.21 and `fix17cs2x` each
  have 0): "Ayaan, who is my teammate, speaks fluent Korean." for "what can my teammate speak besides english". Seed 82
  answered the same item "Your teammate Ayaan speaks fluent Korean." No row of `fix17cs3`, `fix17cr11` or
  `strict_chat` has "who is my" in a tool result or ", who is" in an answer.
- All 3 `statement` misses at probe 51203 are "Esme forgot my birthday again": one answered with an unrelated stored
  fact ("Your godfather Esme grows prize asparagus."), the R-112 shape; two answered "I don't know that one yet." The
  57 added statement rows did not remove this shape.
- `hard_dev` recall (165) is the second highest at these seeds, after 6.2's 166.

**Kevin's ruling, 2026-11-07, given after R-115 and before this result was read:**

1. No more versions trained on top of an earlier version (no 6.211, no 6.22): R-115 showed each extra round lost
   `hard_dev` recall (166, 160, 155). Every new try trains from scratch.
2. A fail does not end the tries. This replaces R-114 item 3 ("on any fail ... v6 ships"), which was the panel's
   rule, not his. Tries continue while a version can finish the full gate before Monday 12:00. The gates do not move,
   and v6 stays the model that has passed them until another copy does.

**What follows.** v6 at 94, 95 and 96 (`fix17m`, `strict_chat.jsonl`) was queued at 16:56, unguarded: any candidate's
fresh-seed recall line needs it. A new panel (R-111 rule 5) designs the next from-scratch try; it is recorded before it
trains. R-114's cut-offs stand: its 82-and-83 training must start by Sunday 22:00, and its 94-to-96 training by Monday
04:00. 6.3 is not read at new seeds.

## R-117 · 2026-11-07 · SPRINT · 6.31's design, panelled and vetted before it trains

**The panel** (R-116; four lanes, one arguing against; one agent; transcript audited: it read `RECORDS.md`, the gate
and build scripts, `loss_masks.py`, `pool_hard_dev.py`, the training sets and the eval results, read `pools.py` only up
to line 451, opened no token file and wrote nothing. One `grep -l` over `src/aya_retrieval/*.py` searched every file in
that folder, the sealed `pool_independent.py` among them; it printed file names only, no content).

- **Checked and corrected.** The 7 seed-83 slips are 7 different items in 4 fact types, one shape. 6 of fix 19a's 52
  answers in 6.3's set answer in the friend's own voice, copying the stored line ("Marc is my roommate and they rent on
  the twelfth floor."; "Got it! Here's the updated response: My sister Yusuf only ever orders an Americano."), and
  `slip_shape` misses all 6. "<Name> forgot my birthday again" is every probe-51203 `statement` miss of 6.3 and most of
  6.2's and v6's at other seeds. No training row has another person forgetting or losing something with no search.
  `hard_dev` stores facts as "{person}, my {relation}, ..." (`pool_hard_dev.py`). R-114's against lane says ten
  candidates had been read at 82 and 83 since R-093; its own list (item 6) has nine, with 6.3. 6.31 is the tenth.
- **For.** Give all 52 indirect answers the pool's scripted answer, as C2 (R-098), and add contrast rows for the
  statement shape.
- **Other design.** Change the answers only. It changes least, but leaves the statement shape, which failed 3 of 9
  readings of the 6.2 line.
- **Against (accepted as conditions).** Seed noise is real (v6 had 14 slips at seed 87), but no 6.2-line seed went
  above 2 in 9 seeds, so 7 is a shift. The contrast rows target a kind read off one probe message, so the probe
  `statement` line is no longer independent evidence for that kind, and the write-up says so. Memory-word rows with no
  search may teach the model not to search on `hard_dev`'s "i've lost what..." questions (R-085's loss, 74 to 56); so
  the build stops unless the set has at least as many memory-word asks answered from a search as contrast rows.
  Scripted answers cost C2 recall once (R-101). **Leakage ruling:** no new stored-line forms. "<Name>, who is my
  <relation>" is the probe's form and "<Name>, my <relation>" is `hard_dev`'s; training on either only tests memory
  of the pattern. The fix is on the answer side.

**6.31 = `fix17cs31`** (`scripts/records/build_r117.py`; deterministic, two runs gave SHA-256 `3e257973adc3…`):

- 6.3's 1,079 rows (`data/screens/fix17cs3.jsonl`), in order. Every row but the 52 `indirect/older_` rows is byte
  for byte.
- The 52 `indirect/older_` rows keep their conversation and search; the answer becomes the pool's scripted answer
  (`TRAIN.facts[...].answer`) for the one fact value both the answer and the found line name, with the person and
  relation on that line. 16 were already that answer (R-114's 15 rewrites and one more), 36 change. Every scripted
  answer passes a voice check ("my <relation>", "I keep", "I should") and `slip_shape`.
- 24 `contrast/statement_` rows: three small-talk exchanges from the train pool's moods (random seed 117), then one of
  8 frames written in the build with a train-pool person or relation, 3 rows a frame, answered without a search with
  a fixed reply ("{person} left their keys at my place again" / "Oh no. At least they know where to find them."; "my
  {relation} lost their wallet on the bus"; "{person} keeps forgetting to text me back"; "{person} is planning a party
  for their fortieth"; "my {relation} forgot their umbrella and got soaked"; "{person} lost track of time and missed
  the train"; "{person} had a birthday dinner last night"; "my {relation} forgot about our lunch today"). No frame has
  "forgot my", "my birthday" or the speaker as the one who forgets. One reply was reworded before the final build
  because it shared a four-word run with the test pools ("that's rotten luck"); the build stops on any such row.
- 1,103 rows; 231 statement rows (20.9%); 33 memory-word asks answered from a search (at least 24 needed).
- **Vetted** (`results/vet/R-117/`): one fresh Sonnet judge, its own folder, marked the 52 scripted answers under
  R-110's rubric and the 24 contrast rows under a new statement rubric (written before marking). 52 of 52 and 24 of 24
  right; no row dropped. Transcript audited: it read and wrote only its own folder; its one shell command printed "1".
  It took 29 seconds and marked every item 1.
- Training: 6.3's recipe (3 epochs, peak 3e-4, rank 32 on attention and MLP, `--loss-on chat_decision`), from no
  adapter. The train report must show 1,103 rows and `decision_rows` 231. Seeds 82 and 83; **seed 82 is the one to
  ship**.

**Order on the GPU.** 6.31 at 82 and 83 goes right after v6's seed-94 training (about 18:00), then R-086's unjudged
gate (a fail stops 6.31's later lines), then v6 at 95 and 96, then 6.31's eight stress runs. R-086's judged sheets run
on the CPU once its plain sets are scored.

**Recorded before 6.31 trains:**

1. **Pass rules:** R-114 items 1 and 2, word for word (82 and 83, then 94 to 96).
2. **On a fail:** stop; nothing is judged after an unjudged fail; 6.31 is never read at new seeds. Under Kevin's
   ruling (R-116) a fail does not end the tries: a new panel may design another from-scratch try if its 82-and-83
   training can start by Sunday 22:00 and its 94-to-96 training by Monday 04:00.
3. **On a full pass:** 6.31 seed 82 replaces v6 and is the base for 7 (R-111).
4. **The write-up discloses:** candidate 10 at 82 and 83 since R-093; the statement kind read from probe misses, so
   the probe `statement` line is not independent evidence for it; the 36 changed answers and 24 contrast rows; the
   panel's `grep -l`; the judge's speed.
5. **The panel's estimates, judgements and not measurements:** about 35% that 6.31 passes every line at 82 and 83;
   about 40% that a pass holds at 94 to 96; about 14% for both (the against lane says about 9%). Most likely to fail:
   the probe `statement` line, `hard_dev` recall against v6's, and the judged `in_view` lines.

## R-118 · 2026-11-07 · SPRINT · 6.311 and 6.32: scripted in-view rows, on top and from scratch

**Why.** 6.31 at seed 82 (R-117) passed every counted line read so far, but answered fewer `in_view` items (the
fact is still in the chat, so no search is needed) than v6 at 82: `hard_dev` 32 against 37, probe 51203 42 against 45.
All 16 `hard_dev` misses have one shape: no search (right), then a reply of sympathy that names no fact ("It sounds
like you're feeling a bit lost or confused about your coach's job interview."). 7 of v6's 11 misses have the same
shape; v5 had it too (R-063). **Kevin's ask:** "that's why i want to do the 6.311 because it'll give us that extra
layer on top to take care of in view hopefuly". 6.311 is trained on top of 6.31, against R-116's ruling (no versions
on top of earlier ones), at Kevin's word.

**The panel** (four lanes, one arguing against; one agent; transcript audited: 25 tool calls, it read `RECORDS.md`,
the build, train and builder scripts, training sets and results, searched `src/` only with
`--exclude=pool_independent.py`, opened no sealed or token file, wrote only in scratch, used no GPU).

- **Checked and rejected: dilution.** My first diagnosis was that 6.31's 150 `in_view` rows (v6's own) are a smaller
  share of a larger set (13.6% of 1,103 against v6's 18.8% of 800). The share does not track the score: `hard_dev`
  `in_view` at 82 and 83 is 37, 37 for v6 (18.8%), 39, 40 for 6.2 (15.5%), 38, 34 for 6.3 (13.9%), and 32 at 82 for
  6.31 (13.6%). 6.3 and 6.31 have the same share.
- **More likely causes.** 26 of the 150 `in_view` targets, base's own replies kept since v6 because they name the
  value somewhere, open "It sounds like..." ("It sounds like you're trying to remember what your aunt ran. Was it a
  5k?"). R-117's 24 contrast rows pair a memory word with a reply that names no fact, 15 of them.
- **For 6.311.** Cheap at 82 and 83, keeps 6.31's lead (`hard_dev` recall 82 against 74 at seed 82, probe slips 0
  against 3), a narrow step.
- **Other: 6.32 from scratch.** Follows R-116; cheaper to confirm at 94 to 96 (6.311 there needs 6.31 trained there
  first).
- **Against.** Steps on top moved pooled `hard_dev` recall by +9, +3, −7 and −11, and the extra epoch alone cost 6
  (R-115). Twice before, changing the in-view rows gained 3 in-view answers and lost 5 or 6 found-fact answers (R-063,
  R-064). 6.3's `hard_dev` `in_view` moved 38 to 34 between seeds, so 6.31's drop is about 1.5 seed spreads. More rows
  that answer a memory-word ask from the chat may bring back R-112's shape. Base-written rows add more "It sounds like"
  targets, so the rows are scripted.
- **Ruling.** Build scripted rows on the CPU; train both; fix which copy goes forward now.

**The rows** (`scripts/records/build_r118.py`; deterministic, two runs gave the same SHA-256 for both sets): 72 fresh
train-pool conversations (seeds from 118,000,001, clear of every builder's), the fact among the last exchanges,
asked in an indirect form (the template's own or `train_phrasings.MORE_INDIRECT`), answered with the pool's scripted
answer ("Your sister Greta broke a forearm.") and no search. 1 conversation was skipped for sharing a four-word run
with the probe or `hard_dev` pools. Every answer names the value and passes `slip_shape` and R-117's voice check; no
row repeats one of 6.31's. **Vetted** (`results/vet/R-118/`): one fresh Sonnet judge, its own folder, marked the 72 answers under a new in-view rubric written before marking: 72 of 72 right; it noted that 2 leave out a detail the question did not ask ("from an auction") and 1 gives all the chat holds ("opened a vintage shop" for what the shop sells). Transcript audited: it read and wrote only its own folder. It took 39 seconds.

- **6.32 = `fix17cs32`:** 6.31's 1,103 rows byte for byte, then the 72: 1,175 rows, `in_view` 222 (18.9%). 6.31's
  recipe from no adapter. The train report must show 1,175 rows and `decision_rows` 231.
- **6.311 = `fix17cs311`:** 216 of 6.31's rows (19.6% of each kind, largest remainder, random seed 311), then the 72:
  288 rows. One epoch at peak 5e-5 (half of 6.21's) on top of `fix17cs31_<seed>`, `--loss-on chat_decision`, at 82
  on 6.31's seed-82 adapter and at 83 on its seed-83 one. The train report must show 288 rows, `init_tensors_loaded`
  504 and `adapter_changed` true.

**Order on the GPU** (backlog lines 168 to 189): after 6.31's eight stress runs, 6.311 at 82 and 83, then 6.32 at 82
and 83, then R-086's unjudged gate for each (a fail stops that copy's later lines), then each copy's eight stress
runs. R-086's judged sheets run on the CPU once a copy's plain sets are scored.

**Recorded before either trains:**

1. **Pass rules:** R-114 items 1 and 2, word for word, for each copy.
2. **Which goes to 94 to 96:** of 6.31, 6.311 and 6.32, the copies that pass R-114 item 1; of those, the one with the
   highest pooled `hard_dev` recall at 82 and 83; a tie goes to the copy with fewer changes, in the order 6.31, 6.32,
   6.311. Only that copy is read at 94 to 96. If it is 6.311, 6.31 is trained at 94 to 96 first. The 94-to-96
   training starts by Monday 04:00.
3. **On a full pass:** that copy's seed 82 replaces v6 and is the base for 7 (R-111).
4. **The write-up discloses:** candidates 11 and 12 since R-093; that 6.311 goes against R-116's ruling, at Kevin's
   word, and its replay share; that the in-view kind was read from `hard_dev`, probe and screen misses, so those
   `in_view` lines are not independent evidence for it; the rejected dilution diagnosis; that the scripted in-view
   answers are new; the pick among copies at 82 and 83.
5. **The panel's estimates, judgements and not measurements,** pass at 82 and 83: 6.32 about 30%; 6.311 about 20%
   (the against lane says 12%); `in_view` up by 4 or more for either copy about 50%.

## R-119 · 2026-11-07 · SPRINT · 6.31 fails R-094's probe recall line by one

Both train reports show 1,103 rows and `decision_rows` 231. R-086's unjudged gate passes every line (probe 51203
recall 95, `statement` 48; `hard_dev` `never_told` at 82 48; `hard_dev` recall pooled 163; probe recall pooled 191
against its floor of 189; false retrieval at 82 0). R-094:

| Line (seeds 82, 83) | v6 | 6.31 | Rule | |
|---|---|---|---|---|
| probe slips | 3, 4 | 0, 0 | at most 5 a seed, 8 pooled | PASS |
| `hard_dev` slips | 0, 3 | 0, 0 | at most 3 a seed | PASS |
| `hard_dev` recall pooled | 157 | 163 | not below v6's | PASS |
| **probe recall pooled** | **192** | **191** | **not below v6's** | **FAIL** |

The one miss is probe item `58_older_00` at seed 83, "drawing a blank on my daughter's tattoo": no search and a
reply of sympathy ("That can be frustrating. Maybe you could try to remember the details..."). This is the shape
R-118's panel traced to the in-view targets and R-117's contrast rows. Reported, not gated: `hard_dev` `in_view` 32
and 38 (v6 37, 37); probe `in_view` 42 and 43 (v6 41, 45).

**Under R-117 item 2:** 6.31 stops. Its eight stress lines are skipped (`r117_stop`), nothing of it is judged, and
it is never read at new seeds. It drops out of R-118's pick; R-118's lines and rules are otherwise unchanged. 6.311
still trains on 6.31's adapters, as R-118 recorded, and if 6.311 is the copy picked, 6.31 is trained at 94 to 96 only
as its parent. With the stress lines skipped, 6.311 starts after v6 at 95 and 96 (about 21:30).

## R-120 · 2026-11-07 · SPRINT · 6.311 fixes in-view and loses `hard_dev` recall

Both train reports show 288 rows, `init_tensors_loaded` 504 and `adapter_changed` true.

| Line (seeds 82, 83) | v6 | 6.31 | 6.311 |
|---|---|---|---|
| probe `in_view` | 41, 45 | 42, 43 | 48, 48 |
| `hard_dev` `in_view` | 37, 37 | 32, 38 | 42, 37 |
| probe recall | 96, 96 | 96, 95 | 96, 95 |
| `hard_dev` recall | 74, 83 | 82, 81 | 65, 57 |
| slips, probe and `hard_dev` | 7, 3 | 0, 0 | 0, 0 |

R-086's unjudged gate fails one line (`hard_dev` recall pooled 122, floor 145); R-094 fails two (probe recall pooled
191 against v6's 192; `hard_dev` recall pooled 122 against 157). The 39 `hard_dev` recall misses at seed 83 (6.31: 15)
mostly search and then answer with the fact type but not the detail ("Your housemate Gideon hosted dinner.", "Your
housemate Joaquin got a job interview."); 3 do not search. This is R-115's and R-063's pattern: the step on top bought
in-view answers and cost found-fact recall.

**Under R-118:** 6.311 stops; its gate line (backlog line 172) stops its stress lines, and nothing of it is judged.
6.32 (from scratch, the same 72 rows) is training at 82 now and goes on as recorded.

## R-121 · 2026-11-08 · SPRINT · 6.32 fails: the scripted in-view rows cost found-fact detail

Both train reports show 1,175 rows and `decision_rows` 231.

| Line (seeds 82, 83) | v6 | 6.31 | 6.311 | 6.32 |
|---|---|---|---|---|
| probe `in_view` | 41, 45 | 42, 43 | 48, 48 | 43, 44 |
| `hard_dev` `in_view` | 37, 37 | 32, 38 | 42, 37 | 32, 39 |
| probe recall | 96, 96 | 96, 95 | 96, 95 | 96, 94 |
| `hard_dev` recall | 74, 83 | 82, 81 | 65, 57 | 57, 76 |
| probe slips | 3, 4 | 0, 0 | 0, 0 | 6, 0 |
| `hard_dev` slips | 0, 3 | 0, 0 | 0, 0 | 0, 0 |

R-086's unjudged gate fails one line (`hard_dev` recall pooled 133, floor 145); R-094 fails three (probe slips at 82,
6 against 5; probe recall pooled 190 against v6's 192; `hard_dev` recall pooled 133 against 157). Of the 39 `hard_dev`
recall misses at seed 82, 33 search, find the line and answer with the fact's event but not the asked detail ("Your
coach Lorcan hosted dinner." for what was in the pot, borscht; "Your plumber Nadia collected keys." for the noisy
creatures, canaries); at 83, 8 of 20.

**What this shows.** 6.311 (on top) and 6.32 (from scratch) share only the 72 scripted in-view rows, and both lose
the asked detail on found facts; 6.31, without them, does not (163). So the cost comes from the rows, not from
training on top. Their one-sentence "Your {relation} {person} {fact}." answers, given with no search, teach a short
answer shape that the model also uses after a search, where it keeps the event and drops the detail. In-view answers
rose for neither copy on `hard_dev` (6.32 32 and 39 against 6.31's 32 and 38).

**Under R-118:** 6.32 stops; its gate line stopped its stress lines, and nothing of it is judged. None of 6.31, 6.311
and 6.32 passes R-114 item 1, so none goes to 94 to 96. A further
from-scratch try is panelled next (R-122).

## R-122 · 2026-11-08 · SPRINT · 6.33 to 6.35: removals from 6.31, from scratch

**Why.** 6.31 missed by one probe question (R-119); 6.311 and 6.32 added 72 scripted in-view rows and lost found-fact
detail (R-120, R-121). These tries add nothing and only remove rows from 6.31.

**The panel** (four lanes, one arguing against; one agent; transcript audited: 19 tool calls, it read `RECORDS.md`,
training sets, results and `stone_report.py`, did not search `src/`, opened no sealed or token file, wrote nothing,
ran no git, GPU or eval).

- **For removing the 15 memory-word contrast rows (A).** The probe recall miss "drawing a blank on my daughter's
  tattoo" at seed 83 is the first no-search probe recall miss in the 6.2 line (96 in all 11 files of 6.2, 6.21, 6.2x
  and 6.3). Every copy with R-117's contrast rows misses it at 83: 6.31, 6.311 and 6.32, two of them separate
  trainings. The contrast rows teach that a memory word with another person in it gets no search ("Tomas keeps
  forgetting to text me back -> That can be annoying. Maybe they've just been busy."). A keeps 9 contrast rows,
  among them the two frames nearest the Esme statement line ("left their keys at my place again", "had a birthday
  dinner last night").
- **For removing the 22 "It sounds like" in-view rows (B, or both = C).** 13 of 6.31's 16 `hard_dev` `in_view`
  misses at 82 open "It sounds like". Against: v6 and 6.2 carry the same 22 rows; 6.31's `hard_dev` `in_view` 32 sits
  inside the earlier spread (32 to 37); the line is not gated; B does not touch the gated miss; in-view edits moved
  found-fact recall before (R-063, R-064).
- **Against.** A still needs no probe recall miss in 192 (v6 had one in 2 of 14 seeds). The exposure is the probe
  51203 statement line: 6.3, which had no contrast rows, scored 45 (floor 47), searching on all 3 "Esme forgot my
  birthday again" lines. About 4 of 20 earlier candidates missed a "forgot my birthday" line. `hard_dev` should not
  move: its no-search misses are the "cuppa" items in every model.
- **Ruling.** Train A first; then C, or B instead if A fails only the statement line (B keeps the contrast rows).
  A third try (the other of B and C, or dropping only the 6 contrast rows whose reply has "Maybe") only if time
  allows and none has passed.

**The sets** (`scripts/records/build_r122.py`; 6.31's other rows byte for byte, in order; the build stops if a
group's count is not 15 or 22; two runs of 6.33 gave the same SHA-256):

| Copy | Set | Rows | Removed | SHA-256 |
|---|---|---|---|---|
| 6.33 (A) | `fix17cs33` | 1,088 | 15 memory-word contrast rows | `23f50ed7...` |
| 6.34 (C) | `fix17cs34` | 1,066 | both groups | `fa0f5e12...` |
| 6.35 (B) | `fix17cs35` | 1,081 | 22 "It sounds like" in-view rows | `8f8059f6...` |

6.31's recipe from no adapter. **Order on the GPU** (backlog lines 190 to 211): 6.33 at 82 and 83 (from 00:15), its
gate (R-086 unjudged and R-094; a fail stops its stress lines), then 6.34 or 6.35 at 82 and 83 as ruled, its gate,
then each copy's eight stress runs.

**Recorded before any result:**

1. **Pass rules:** R-114 items 1 and 2, word for word, for each copy.
2. **Which goes to 94 to 96:** of the copies that pass R-086's unjudged gate and R-094 at 82 and 83, the one with the
   highest pooled `hard_dev` recall; a tie goes to fewer changes, in the order 6.33, 6.34, 6.35. Only that copy is
   read at 94 to 96. Nothing starts after Monday 12:00.
3. **On a full pass:** that copy's seed 82 replaces v6 and is the base for 7 (R-111).
4. **The write-up discloses:** candidates 13 and 14 (15 if a third runs) since R-093; that R-117's contrast rows were
   a patch fitted to one probe line; that the 6.31 miss is a "drawing a blank" form no training row has; the pick
   among copies at 82 and 83.
5. **The panel's estimates, judgements and not measurements,** of a full pass at 82 and 83: 6.33 about 45%; 6.34
   about 38%; 6.35 about 25%; at least one of 6.33 and 6.34 about 60%; a pass here holding at 94 to 96 about 40%.

## R-123 · 2026-11-08 · SPRINT · 6.33 fails R-094's probe recall line by one, on a new question

Both train reports show 1,088 rows and `decision_rows` 216. R-086's unjudged gate passes every line (probe 51203
recall 96, `statement` 48; `hard_dev` `never_told` at 82 45; `hard_dev` recall pooled 160; probe recall pooled 191
against its floor of 189; false retrieval at 82 3). R-094:

| Line (seeds 82, 83) | v6 | 6.31 | 6.33 | Rule | |
|---|---|---|---|---|---|
| probe slips | 3, 4 | 0, 0 | 0, 0 | at most 5 a seed, 8 pooled | PASS |
| `hard_dev` slips | 0, 3 | 0, 0 | 0, 0 | at most 3 a seed | PASS |
| `hard_dev` recall pooled | 157 | 163 | 160 (73, 87) | not below v6's | PASS |
| **probe recall pooled** | **192** | **191** | **191 (96, 95)** | **not below v6's** | **FAIL** |

6.31's miss ("drawing a blank on my daughter's tattoo", no search, sympathy) is gone at 83. The one miss is a new
question, probe `58_older_17` at seed 83, "what freaks my stepsister out the most": it searched "sister steps out",
found nothing and said it did not know (answer: deep water). This is a query that splits "stepsister", not the
no-search shape R-122 removed. v6 has no probe recall miss at 83. Reported, not gated: `hard_dev` `in_view` 44 and
34 (v6 37, 37); probe `in_view` 42 and 40 (v6 41, 45).

**Under R-122:** 6.33 stops; its stress lines are skipped (`r122_stop_33`), nothing of it is judged. It failed a line
other than the statement line, so 6.34 (both removals) trains next (from 02:13), as ruled.

## R-124 · 2026-11-08 · SPRINT · 6.36, the third removal try, chosen after 6.33's result

**Why.** R-122 left the third try open ("the other of B and C, or dropping only the 6 contrast rows whose reply has
'Maybe'"). 6.33's result (R-123) came in before 6.34's, so the choice was panelled again now.

**The panel** (four lanes, one arguing against; one agent; transcript audited: 16 tool calls, it read `RECORDS.md`
from R-116, `fix17cs31.jsonl`, `fix17cs33.jsonl` and probe results, opened no sealed or token file, did not search
`src/`, ran no git, GPU or eval). Against its brief it wrote 9 short analysis scripts into the session's scratch
folder, none in the repo; I read them (no sealed, token or pool reads, no writes) and deleted them.

- **Against 6.35 (B).** B keeps all 15 memory-word contrast rows. The tattoo question is missed at seed 83 by 6.31,
  6.311 and 6.32, three separate trainings that have those rows, and by none of the other 38 probe files of the 6.x
  line. B changes only in-view rows.
- **For 6.36 (D2).** Its 6 rows (`contrast/statement_0006` to `0008`, "keeps forgetting to text me back -> That can
  be annoying. Maybe they've just been busy.", and `0021` to `0023`, "forgot about our lunch -> That's a letdown.
  Maybe you can pick another day.") are the nearest in shape to 6.31's miss. It keeps the "left their keys" and
  "birthday dinner" frames nearest the Esme statement line and the 22 in-view rows. Risk: 9 memory-word rows stay;
  the tattoo miss may come back.
- **Against.** Probe recall sits at its ceiling: v6 has 96 in 10 of 12 files, and each miss since has been a
  different question. Even a clean copy fails this line by chance about a quarter of the time, so a third small
  removal is a new draw, not a fix. 6.33's `hard_dev` margin is 3 (160 against 157).
- **The stepsister miss is one question, not a pattern.** Across 792 stepsister recall queries in the 6.x line, 3
  dropped the word, all on `58_older_17` ("what freaks my stepsister out"), 3 files in 72. Stepsister items miss 4
  of 418 against 16 of 3,230 for the rest, not a significant gap. The training set has no step-, in-law or half-
  relation and no query with one, so there is no row to duplicate; new rows cost detail (R-121).
- **Ruling.** 6.36 = D2.

**The set** (`scripts/records/build_r122.py`, group `maybe_contrast`, count 6): `fix17cs36`, 1,097 rows, SHA-256
`349c9d32...`; 6.31's other rows byte for byte, in order. Rebuilding 6.33 to 6.35 after adding the group gave the
same SHA-256 for each. 6.31's recipe from no adapter.

**Order on the GPU** (backlog lines 196 to 198, 215 to 222): after 6.34's gate, 6.36 at 82 and 83 only if 6.34 failed,
then its gate (a fail stops its stress lines). If 6.34 passed, 6.36 is not trained.

**Recorded before its result:** R-122's pass rules and pick rule hold, with 6.36 last in the tie order (6.33, 6.34,
6.35, 6.36). Candidates 13 to 15 since R-093. The write-up adds that 6.36 was chosen after 6.33's result, that 6.31's
and 6.33's misses are different questions on a line at its ceiling, and that the training set has no step-relation
rows. The panel's estimates, judgements and not measurements: 6.36 passes at 82 and 83 about 33%; 6.35 about 12%; a
pass here holding at 94 to 96 about 40%.

## R-125 · 2026-11-08 · SPRINT · 6.34 fails the statement line and probe recall by one

Both train reports show 1,066 rows. R-086's unjudged gate fails one line and R-094 one:

| Line (seeds 82, 83) | v6 | 6.33 | 6.34 | Rule | |
|---|---|---|---|---|---|
| **probe 51203 `statement`** | 48 | 48 | **45** | **at least 47** | **FAIL** |
| **probe recall pooled** | **192** | 191 | **191 (95, 96)** | **not below v6's** | **FAIL** |
| `hard_dev` recall pooled | 157 | 160 | 163 (80, 83) | not below v6's | PASS |
| probe slips | 3, 4 | 0, 0 | 0, 1 | at most 5 a seed, 8 pooled | PASS |
| `hard_dev` slips | 0, 3 | 0, 0 | 0, 0 | at most 3 a seed | PASS |

**The statement misses** are the shape R-117's contrast rows were added for, and the risk R-122's panel named for
removing all 15 memory-word rows: "Esme forgot my birthday again" (twice) and "Ayaan forgot my birthday again" each
got a search ("Esme born birthday month") and a found fact as the reply ("Your godfather Esme is terrified of
clowns."). 6.33 had the same 15 rows removed and scored 48, so the line moved with the second removal or with the
seed draw; one pair of copies cannot say which.

**The probe recall miss** is `58_older_20` at seed 82, "what's growing behind my stepsister's house": it searched
"sister house colour painted", found nothing and said it did not know (answer: chillies). R-124's panel had counted
the stepsister query split on one question only (`58_older_17`, 3 files in 72); this is a second question, so the
split is not confined to one question. The training set has no step-relation rows (R-124).

**Under R-122 and R-124:** 6.34 stops; its stress lines are skipped (`r122_stop_next`), nothing of it is judged.
6.36 began training at 82 at 04:06, as queued.

## R-126 · 2026-11-08 · SPRINT · 6.36 fails: the tattoo miss returns and the statement line falls

Both train reports show 1,097 rows. R-086's unjudged gate fails one line and R-094 one:

| Copy (removed from 6.31) | probe recall | probe 51203 `statement` | `hard_dev` recall | Probe recall miss |
|---|---|---|---|---|
| v6 | 96, 96 (192) | 48 | 74, 83 (157) | none |
| 6.31 (none) | 96, 95 (191) | 48 | 82, 81 (163) | tattoo, no search |
| 6.33 (15 memory-word contrast rows) | 96, 95 (191) | 48 | 73, 87 (160) | stepsister query split |
| 6.34 (those 15 and 22 "It sounds like") | 95, 96 (191) | 45 | 80, 83 (163) | stepsister query split |
| 6.36 (6 "Maybe" contrast rows) | 96, 95 (191) | **40** | 83, 76 (159) | tattoo, no search |

Floors: probe recall pooled not below 192, `statement` at least 47, `hard_dev` recall pooled not below 157. Slips:
probe 1 and 0, `hard_dev` 0 and 0 (pass).

**The tattoo miss** ("drawing a blank on my daughter's tattoo", seed 83, no search, "That can be a bit of a bummer.
Do you have any other ideas for a tattoo?") came back. Every copy that keeps the "lost" and "forgot" contrast rows
misses it at 83 (6.31, 6.311, 6.32, 6.36), and both copies without them (6.33, 6.34) answer it.

**The statement line** fell to 40: 8 "X forgot my birthday again" lines (Esme, Ayaan, Chidi, Kofi) got a search
("Esme born birthday month") and a found fact as the reply ("Your godfather Esme grows prize asparagus."). The 6 rows
removed include the 3 "forgot about our lunch" rows (another person forgot a plan with the speaker), the frame nearest
"forgot my birthday"; R-124's panel had named the "left their keys" and "birthday dinner" frames as the nearest. I
did not check that claim against the rows before queuing 6.36.

**Under R-122 and R-124:** 6.36 stops; its stress lines are skipped (`r122_stop_36`), nothing of it is judged. The
next try is panelled (R-127).

## R-127 · 2026-11-08 · SPRINT · 6.37: 6.31 less the wallet, umbrella and lost-track rows

**The panel** (four lanes, one arguing against; one agent; transcript audited: 14 tool calls, it read `RECORDS.md`,
`build_r122.py`, `fix17cs31.jsonl` and results, wrote no file, opened no sealed or token file (one glob skips names
with "token"), did not search `src/`, ran no git, GPU or eval). I checked its 9 row ids against the set before the
build.

- **The data.** The 24 contrast rows are 8 frames of 3: keys (0-2), lost wallet (3-5), keeps forgetting to text
  (6-8), party (9-11), forgot umbrella (12-14), lost track of time (15-17), birthday dinner (18-20), forgot lunch
  (21-23). The tattoo question is missed at seed 83 by all four copies that keep wallet, umbrella and lost-track
  (6.31, 6.311, 6.32, 6.36) and by none of v6 (12 files), the 6.2 line (11), 6.33 or 6.34, which drop them. On the
  statement line the only items that fail are 8 "X forgot my birthday again" lines; copies with the text and lunch
  rows (6.31, 6.311, 6.32) fail none; copies without them fail 3 (6.3), 0 (6.33), 3 (6.34), 8 (6.36), 4 (`fix17r`).
- **For 6.37.** It is the one cell left: 6.31 has both groups (tattoo miss, `statement` 48), 6.36 only wallet,
  umbrella and lost-track (miss, 40), 6.33 neither (no tattoo miss, 48); 6.37 keeps text and lunch (with keys,
  party and dinner) and drops the other three.
- **Other.** Dropping 12 and keeping only lunch, or doubling lunch: the same bet with less statement cover.
- **Against.** Every edit is a new draw. The tattoo evidence is 4 misses against 0 at one seed, and the replies
  differ ("Maybe you could...", "bit of a problem", "bit of a bummer"), so the mechanism is not shown. The statement
  line moved 48 to 45 and 48 to 40 on small edits. Stepsister query splits cost 6.33 and 6.34 a point each (7 of 39
  near-v6 files without contrast rows miss a stepsister item). The `hard_dev` margin is 3 to 6.
- **Base rate.** A copy with no real defect misses at least one of the 96 probe recall questions in 11% to 20% of
  files, so about 21% to 36% for the pair at 82 and 83 (central 28%), close to R-124's "about a quarter".
- **Ruling.** 6.37.

**The set** (`build_r122.py`, group `wallet_umbrella_time`, count 9: `contrast/statement_0003` to `0005` and
`0012` to `0017`): `fix17cs37`, 1,094 rows, SHA-256 `04df294a...`; 6.31's other rows byte for byte, in order; 6.33
to 6.36 rebuild to the same SHA-256. 6.31's recipe from no adapter. Backlog lines 223 to 233: 82 and 83 (from 06:05),
its gate (a fail stops its stress lines), its eight stress runs.

**Recorded before its result:** R-122's pass rules and pick rule hold (6.37 is the only copy still in it). The
panel's estimates, judgements and not measurements: tattoo answered 0.65, no other probe recall miss 0.72,
`statement` at least 47 0.78, `hard_dev` at least 157 0.82, all four about 0.30; a pass holding at 94 to 96 about
0.4. The panel's view that further edits after 6.37 are mostly draws is recorded; under Kevin's ruling (R-116) the
tries go on while a copy can finish the full gate before Monday 12:00, and the next step is panelled with 6.37's
result. The write-up adds candidate 16, the 2x2 of frames, and the base rate.

## R-128 · 2026-11-08 · SPRINT · 6.37 passes R-086 whole, R-094 and R-097 at 82 and 83

Both train reports show 1,094 rows and `decision_rows` 222 (6.31's 231 less the 9 dropped contrast rows).

**R-086's unjudged lines** all pass: probe 51203 recall 94 (needs 94), `statement` 48 (47); `hard_dev` `never_told`
at 82 48 (44); `hard_dev` recall pooled 163 (145); probe 73157 recall pooled 192 (189); false retrieval at 82 1 (at
most 6). **R-094** passes: slips 0 at every seed on both sets; probe recall pooled 192 against v6's 192, `hard_dev`
163 against 157. **R-097's stop rule** passes: probe `in_view` 44 and 44 (below 41 stops).

| Line (seeds 82, 83) | base | v6 | 6.37 |
|---|---|---|---|
| probe recall | 30 | 96, 96 | 96, 96 |
| probe `in_view` | 34 | 41, 45 | 44, 44 |
| probe `statement` | 31 | 48, 46 | 48, 48 |
| `hard_dev` recall | 20 | 74, 83 | 73, 90 |
| `hard_dev` `in_view` | 33 | 37, 37 | 42, 40 |
| slips, probe and `hard_dev` (both seeds summed; base one run) | 2, 1 | 7, 3 | 0, 0 |

The tattoo question (`58_older_00`) is answered at both seeds, the first copy that keeps the text and lunch contrast
rows to do so; no stepsister question is split. Against base, pooled over both seeds: probe recall +220% (192 against
60), `hard_dev` recall +308% (163 against 40).

**Judged** (`results/coherence/R-128/`, shuffle seeds 90543 to 90546; sheets built as R-109's, which I rebuilt from
its inputs byte for byte to confirm the method; three fresh Sonnet judges, each marking all four sheets in its own
folder under R-095's rubric; base is `three_exchanges`; judge 1 decides). Transcripts audited: each judge read only
its rubric and four sheets, covered every line, and wrote only its four marks files, by heredoc; judges 2 and 3 ran
one count over their own marks files afterwards.

| Sheet | Judge 1: base, 6.37 | Judge 2 | Judge 3 |
|---|---|---|---|
| Probe Sheet B `statement` | 46, 48 | 46, 48 | 45, 48 |
| Probe Sheet B `in_view` | 34, 39 | 35, 41 | 34, 40 |
| `hard_dev` Sheet B `statement` | 44, 44 | 44, 44 | 44, 46 |
| `hard_dev` Sheet B `in_view` | 35, 46 | 39, 46 | 35, 46 |
| Check set, seed 82 | 45, 48 | 45, 47 | 45, 48 |
| Check set, seed 83 | 45, 48 | 45, 48 | 45, 48 |

**6.37 passes every judged item under all three judges**, the first copy to do so since 6.2 (R-109), where judge 2
split. `hard_dev` Sheet B `statement` is a tie at 44 under judges 1 and 2; the rule is "at or above base".

**Under R-122's pick rule** 6.37 is the only copy that passed R-086 unjudged and R-094, so it goes to 94 to 96.
**Still to read at 82 and 83:** R-102's items, from the eight stress runs on the GPU now (backlog lines 226 to 233).
Queued after them (lines 234 to 248): 6.37 at 94, 95 and 96, then held-out corrections and the phone form at each. A
fail on R-102 at 82 and 83 touches `r128_stop_37` and stops every line from 234 on. At 94 to 96 R-114 item 2 decides:
R-076's rule with Sheets A, B and h (three fresh judges a sheet type, judge 1 deciding), R-094's slips, recall pooled
not below v6's at 94 to 96, and R-102's fresh-seed items. On a full pass 6.37 seed 82 replaces v6 and is the base for
7 (R-111).

The write-up discloses that 6.37 is candidate 16 since R-093 and that it was picked by R-122's rule among five copies
read at 82 and 83; at 82 and 83 its rows came from failure kinds read on development data, so these lines are not
independent evidence for it; 94 to 96 are.

## R-129 · 2026-11-08 · SPRINT · 6.37 passes R-102 at 82 and 83

The eight stress runs (backlog lines 226 to 233) finished at 08:45. Pooled over 82 and 83, of 192:

| Line | base (one run) | v6 | 6.37 | Rule | |
|---|---|---|---|---|---|
| Held-out corrections, probe | 9 | 1 (1, 0) | 192 (96, 96) | at least v6 + 48, above v6 each seed | PASS |
| Held-out corrections, `hard_dev` | 8 | 5 (5, 0) | 167 (81, 86) | at least v6 + 32, above v6 each seed | PASS |
| Phone typing recall, probe | 32 | 178 (88, 90) | 176 (87, 89) | not below v6 by more than 8 | PASS |
| Phone typing recall, `hard_dev` | 20 | 132 (58, 74) | 147 (67, 80) | not below v6 by more than 16 | PASS |

Slips are 0 in all eight runs (v6: 3 and 5 on held-out corrections, probe). **Every line registered for 82 and 83
passes** (R-086 counts and judged sheets, R-094, R-097, R-102), so `r128_stop_37` is not touched and 6.37 trains at
94 from 08:45, then 95 and 96, then its twelve stress runs. Reported, not gated: of 6.37's `hard_dev` recall misses,
19 of 23 at seed 82 and 3 of 6 at 83 found the line and answered without the asked detail.

## R-130 · 2026-11-08 · SPRINT · 6.37 at 94 to 96: R-076's rule and R-094 pass

The three train reports show 1,094 rows and `decision_rows` 222. Training ran from 08:45 to 11:22 (backlog lines 234
to 236). v6 at 94 to 96 was trained earlier as the comparison (R-116); it was not itself gated here.

**R-094** passes:

| Line (seeds 94, 95, 96) | v6 | 6.37 | Rule | |
|---|---|---|---|---|
| probe recall | 96, 96, 95 (287) | 96, 95, 96 (287) | pooled not below v6's | PASS |
| `hard_dev` recall | 74, 81, 82 (237) | 77, 87, 83 (247) | pooled not below v6's | PASS |
| probe slips | | 0, 0, 1 (corrected, R-131) | at most 5 a seed | PASS |
| `hard_dev` slips | | 0, 0, 0 (corrected, R-131) | at most 3 a seed | PASS |
| probe slips pooled over 82, 83, 94 to 96 | | 1 (corrected, R-131) | at most 8 | PASS |

`hard_dev` slips at 94 were first written here as 3, at the limit; that count took every kind of question, not R-094's `older` and `confirm` (R-131). Reported, not gated: probe `in_view` 45, 39, 42 (v6 41, 47, 42);
`hard_dev` `in_view` 43, 36, 39 (v6 40, 36, 38). Against base, pooled over the three seeds: probe recall +219% (287
against 90), `hard_dev` recall +312% (247 against 60).

**R-076's rule** (`scripts/records/rule_r076.py fix17cs37 R-130 <judge> 94 95 96`). The counted items all pass:
recall pooled 287 (above 252 and at least 273), `in_view` pooled 126 (110), `statement` 144 (136), right decisions
240, 239, 240 (200 each seed), false retrieval 0 (39); `hard_dev` recall 247 (172), false retrieval 6 (20),
`never_told` 138 (132).

**Judged** (`results/coherence/R-130/`, shuffle seeds 90547 to 90555, in the order A, B, h for each of 94, 95, 96;
sheets built as R-112's, which I rebuilt from its inputs byte for byte to confirm the method; Sheet A against base's
`tool_loop` replies, Sheets B and `hard_dev` B against base's `three_exchanges`; three fresh Sonnet judges a sheet
type, each marking its three seeds in its own folder under R-095's rubric; judge 1 decides). Transcripts audited: each
of the nine read only its own folder's rubric and three sheets, covered every line of each, and wrote only its three
marks files, by heredoc; some ran one count over their own marks files afterwards. The three Sheet A judges gave the
same mark on every one of the 576 lines; none opened another judge's folder.

| Item | Judge 1 | Judge 2 | Judge 3 |
|---|---|---|---|
| Sheet A `confirm`, pooled: 6.37, base | 144, 141 | 144, 141 | 144, 141 |
| Sheet A `older` + `confirm`, pooled | 287, 231 | 287, 231 | 287, 231 |
| Sheet B `statement` at 94, 95, 96: 6.37 / base | 48/44, 48/44, 46/44 | 48/46, 48/46, 46/46 | 48/45, 48/45, 46/45 |
| Sheet B `in_view` at 94, 95, 96: 6.37 / base | 39/34, 38/34, 39/34 | 40/34, 36/34, **34/34** | 42/35, 41/35, 40/35 |
| `hard_dev` Sheet B `statement`, pooled | 136, 132 | 139, 129 | 143, 132 |
| `hard_dev` Sheet B `in_view`, pooled | 129, 105 | 130, 105 | 131, 105 |
| **R-076's rule** | **PASS** | **PASS** | **PASS** |

Judge 2's Sheet B `in_view` at 96 is a tie, which the rule ("at or above base every seed") passes. Sheet B at every
seed is the item 6.2 failed at 92 (R-112).

**Still to read:** R-102's fresh-seed items, from the twelve stress runs on the GPU now (backlog lines 237 to 248):
each seed at least 24 of 96 (probe) and 16 of 96 (`hard_dev`) above v6's 82-and-83 mean on held-out corrections, and
the phone guard. If they pass, R-114 item 2 is met in full and 6.37 seed 82 replaces v6 and is the base for 7 (R-111).

**Kevin, 2026-11-08 about 08:55,** on what follows a fail: "yeah run it by the panel and shit. you guys can choose the
best candidate to train". If 6.37 fails, a panel picks the next candidate, from scratch or on top, and it trains
without a further check with him; seeds 94 to 96 are then spent and a copy designed after reading them is confirmed
at fresh seeds.

## R-131 · 2026-11-08 · SPRINT · 6.37 passes R-102 at 94 to 96 and replaces v6

The twelve stress runs (backlog lines 237 to 248) ran from 11:22 to 12:58. Read with
`PYTHONPATH=src python scripts/records/fresh_report.py fix17cs37 94 95 96`; the script now takes its fresh seeds as
arguments (91 to 93 when none are given, so earlier reads are unchanged).

**R-102's fresh-seed items** (R-102 items 5 and 6, anchored to v6's 82-and-83 mean) all pass:

| Item (seeds 94, 95, 96, of 96) | v6, 82-and-83 mean | 6.37 | Rule | |
|---|---|---|---|---|
| held-out corrections, probe | 0.5 | 96, 95, 93 | each seed at least 24 above | PASS |
| held-out corrections, `hard_dev` | 2.5 | 83, 83, 77 | each seed at least 16 above | PASS |
| phone typing, probe | 89 | 91, 85, 85 | each seed within 4 | PASS |
| phone typing, `hard_dev` | 66 | 60, 77, 72 (mean 69.7) | three-seed mean within 8 | PASS |

Phone typing on the probe at 95 and 96 is 85, on the line (89 less 4). Against base (one run each, seed 73157, so
three times base's count), pooled over the three seeds: held-out corrections probe +952% (284 against 27), `hard_dev`
+913% (243 against 24); phone typing probe +172% (261 against 96), `hard_dev` +248% (209 against 60).

**R-114 item 2 is met in full:** R-076's rule and R-094 (R-130) and R-102's fresh-seed items (here). With R-128 and
R-129 at 82 and 83, **6.37 seed 82 (`fix17cs37_82`) replaces v6 and is the base for 7 (R-111).** 7's design is not
fixed; the model freeze (Tuesday November 10) and "nothing starts after Monday 12:00" hold.

**Correction to R-130.** R-130's slip counts took `slip_shape` over every kind of question in the run. R-094 registers
the count on `older` and `confirm` (of 96). On R-094's count 6.37's slips at 94 to 96 are probe 0, 0, 1 and
`hard_dev` 0, 0, 0, and probe pooled over 82, 83 and 94 to 96 is 1 (R-130 wrote 0, 0, 2; 3, 0, 1; 2). Every line passes
on both counts, so no verdict changes. R-130's rows are corrected in place and marked. R-128's counts at 82 and 83 (0
at every seed) were already R-094's. Reported, not gated: v6 at 94 to 96 on R-094's count, probe 7, 2, 7 and
`hard_dev` 2, 2, 6, above R-094's per-seed lines at three of the six; v6 was the comparison here, not a candidate.

## R-132 · 2026-11-08 · SPRINT · Panel on 7: no 7, 6.37 ships

R-111 makes the copy that replaces v6 the base for 7 and leaves 7's design open. Under Kevin's ruling of 08:55 (R-130)
the panel picks without a further check with him. Kevin allowed the panel to start over the usage line (2026-11-08
about 13:10: "Start it now").

**Panel** (one Opus agent, four lanes in turn: design, rule integrity, schedule, against; it wrote nothing).
Transcript audited: 22 read-only calls (record ranges, result files, the training set, `build_r122.py`,
`run_recall_train.py`, the article's open items, `fresh_r131.txt`). One `grep -rn` over `src` and `scripts` was
filtered after the fact for the independent pool; I checked that the searched word occurs in neither sealed file nor
in `pools.py`, so no sealed line reached it.

**Verdict: no 7.** The reasons, with the numbers I recounted:

1. **`hard_dev` in-view.** 6.37 misses 40 of 240 `hard_dev` in-view items over seeds 82, 83 and 94 to 96, and 32 of
   the 40 replies open "It sounds like". `fix17cs37.jsonl` has 150 in-view rows; 22 open that way. Removing those 22
   rows is R-122's `sounds_like` group, already run as 6.34 (6.33 less those rows, R-125): over 82 and 83 the opener
   went from 18 and 16 replies to 0 and 1, but `hard_dev` in-view correct fell from 78 to 69 (6.37: 82); the misses
   moved to searches and to denials of the fact in view, R-063's and R-064's pattern. Probe in-view: 6.33 82, 6.34 82,
   6.37 88.
2. **Found fact, detail left out.** The panel counts this as 25 of 6.37's 41 `hard_dev` recall misses at 94 to 96.
   The one targeted try (R-110's rows) cost recall (R-115), and a rule built from these replies would be fitted to
   the `hard_dev` items it is then confirmed on.
3. **Against lane's strongest point**, which decided it: the only design the data supports has been run and made the
   target line worse; any other change is a new draw (candidate 17 since R-093) that must beat 6.37's `hard_dev`
   recall at the same seeds, where 6.37 ranges 73 to 90 a seed. The schedule lane found a full 7 gate (with 6.37 and v6
   trained at 97 to 99 for the same-seed lines) would finish about 07:00 to 09:45 Monday, so the clock is not the
   reason.

**What follows.** 6.37 seed 82 ships for the freeze. Its remaining battery forms at 82 and 83 (asked-before, plain
corrections, lower-case typing; backlog lines 249 to 260, finishing about 15:05) are reported in the write-up. If one
shows a failure not seen before, a new panel may reopen 7, in time for its 82-and-83 training to start by Sunday
22:00 (R-114's cut-off, restated in R-116). The write-up adds the in-view result above as an open item.

## R-133 · 2026-11-08 · SPRINT · 6.37's battery; a new in-view gap; Kevin's panel of experts

The twelve battery runs (backlog lines 249 to 260) ran from 13:05 to 14:48. Read with
`PYTHONPATH=src python scripts/records/battery_report.py <name>` (new; R-099 item 3's trigger: messy minus plain, same
adapter and items, tool arm, pooled over 82 and 83; a gap is at least 8 of 192 recall or 4 of 96 on `in_view`,
`never_told` or `statement`). Run on `fix17m` it reproduces R-102's battery table for v6 line for line.

| Form | probe recall /192 | probe `in_view`, `never_told`, `statement` /96 | `hard_dev` recall /192 | `hard_dev` `in_view`, `never_told`, `statement` /96 |
|---|---|---|---|---|
| lower-case typing (`user_style`) | -3 (v6 -3) | **-8**, 0, 0 (v6 -1, +2, -1) | +3 (v6 -2) | **-5**, 0, 0 (v6 -3, -1, -1) |
| phone typing (held out) | **-16** (v6 -14) | **-5**, 0, 0 (v6 0, +2, -6) | **-16** (v6 -25) | -3, +1, 0 (v6 -3, +1, -1) |
| fact corrected later | 0 (v6 -187) | recall only | -1 (v6 -146) | recall only |
| earlier question in view | 0 (v6 -2) | -1, 0, -1 (v6 -1, +2, -3) | -4 (v6 -7) | 0, -1, 0 (v6 **-4**, 0, 0) |

New against v6: lower-case typing now costs facts in view on both pools, and phone typing costs them on the probe.
Gone: the correction gap (R-129's held-out result, here on training's wordings too) and asked-before on `hard_dev`.
The lower-case in-view answers lost (19 over the four runs, 6 gained) are all unsearched; they deflect ("You can ask
your godfather about it.") or open "It sounds like" (11 of 19), the same failure as R-132's `hard_dev` in-view misses.
Reported for the write-up; R-099 trained no arm on lower-case typing, and the battery is not a gate.

**Kevin, 2026-11-08,** after R-132: "you have my permission, once this last battery of tests finishes to assemble an
extensive and varied panel of experts to discuss fixes"; "then repanel the panel with the new information from the
panel"; "all the agents vote on the chairs fix. unanimity required". The permission covers the agents' usage.

**The panel, registered before it runs:**
1. **Round 1:** six Opus experts, in parallel, each from one field, each writing nothing: training data; retrieval
   and tool use; training recipe (loss masking, epochs, rates); dialogue and coherence; evaluation and statistics;
   and one arguing that 6.37 ships unchanged. Each gets the same brief (the state above, the gates, the clock, the
   sealed files) and returns a reading, one concrete fix or none, the line it moves, the line it risks, and a
   probability that it replaces 6.37.
2. **Round 2:** each expert reads all six round-1 reports and revises or defends its proposal.
3. **Chair:** one fresh Opus agent reads the six round-2 reports and picks one fix, or none.
4. **Vote:** the six experts vote on the chair's pick; it trains only on six yes votes. On a split vote the chair
   revises against the objections and the six vote again, while 82-and-83 training can still start by Sunday 22:00
   (R-114). No unanimous pick by then: no 7, and 6.37 ships (R-132).
5. Every transcript is audited before its output is used. A unanimous pick is registered here before its rows are
   built, then gated as R-114 at 82 and 83 and at unread seeds 97 to 99, with 6.37 trained at 97 to 99 for the
   same-seed lines.

## R-134 · 2026-11-08 · SPRINT · The panel of experts: 6.38, registered before any row is built

Run as R-133 registered. Everything the panel read and wrote is in `results/panels/R-134/`: the shared brief, the six
round-1 and six round-2 reports, the chair's design and the six votes. Transcripts audited, every agent: all calls
read-only; none opened a sealed file or a seed 97 to 99 result. The recipe expert's glob matched
`probe2_base_tokens_seed_73157.json`, an eval results file the brief's over-broad "token" rule named; it printed four
counts from it and used none. One retrieval read was `sed -n 1,451p src/aya_retrieval/pools.py`, inside the allowed
range.

**Round 1** (independent): training data, a rewrite of 28 deflecting in-view targets (about 20%); dialogue, a rewrite
of 44 by base resampling (15%); retrieval, a swap of 40 found-fact rows for "event, then value" lines (15%); recipe,
no recipe change helps, the fault is the targets (5%); statistics, no 7 (about 3% for an exact clone of 6.37 to pass
the full gate); against, no 7 (5%), but the deflecting in-view targets at full loss are the probable source.
**Round 2** (each read all six): five converged on the 28-row rewrite; retrieval kept its swap. Corrections the
experts found in each other's reports: dialogue's 44 rows included 12 targets that already state the value; at 82
and 83, 12 of 14 `hard_dev` in-view misses open "It sounds like" (not 11). **Chair** (fresh Opus): read all 150
in-view targets; all 28 deflect (about 22 name the value, but inside a hint request, a puzzle, a feeling, "lost" read
as losing a thing, a referral or a denial); 0124 and 0143 are bad targets but their wording is in none of the 66
in-view misses, so they and 0105 and 0110 stay. **Vote: 6 of 6 yes.** Retrieval dropped its swap-only condition (its
rows were shaped on three `hard_dev` fact types that 97 to 99 score again). Estimates at the vote: 5% to 7% that 6.38
replaces 6.37.

**The copied-phrase evidence** (training data and chair, checked by statistics): five phrases occur only in `in_view`
targets, in 1 to 4 rows each, and appear 10, 9, 14, 4 and 8 times in 6.37's 66 in-view misses (probe and
`hard_dev`, seeds 82, 83, 94 to 96); "a bit lost or confused" comes from one row (0122) and appears in 9.

**6.38 (`fix17cs38`), registered:**
1. **Rows.** The final assistant turn of `in_view_` 0000 0015 0027 0036 0057 0058 0059 0060 0064 0077 0079 0085 0086
   0088 0094 0098 0099 0103 0120 0121 0122 0130 0132 0134 0136 0139 0145 0146, and nothing else; 1,094 rows, same
   order, ids and kinds, 150 `in_view`. Built by `scripts/records/build_r134.py` from `fix17cs37.jsonl` (sha256
   `04df294a...`).
2. **Targets** hand-written by the main session in a dictionary in the script (id to value and target). The writer
   has read the `hard_dev` and battery misses, and those items are scored again. The build stops on any target that
   breaks a rule: the value (case ignored) is in the row's fact turn and in the first sentence, with the person's
   name; it opens with the name or the value, never "Your" or "My"; no "?"; none of hint, remember, recall, feeling,
   lost, confused, "ask ", "tell me more", "something else", "it sounds like", "it seems like", "tough one", "i
   don't", "didn't", "you can"; at most one more sentence, word for word in another `in_view` target; `slip_shape`
   false; no four-word run shared with the probe or `hard_dev` pools (`build_r110.TEST_GRAMS`); the row at most
   1,024 tokens.
3. **Vetting.** One fresh blind Sonnet judge marks the 28 new targets under `results/vet/R-118/rubric.txt`, with the
   28 old targets shuffled in as hidden controls (reported, not gated). A rejected target is rewritten once and
   marked by a second fresh judge; if it fails again the old target stays, and the build report names it. The set is
   frozen (sha256 recorded and committed) before training.
4. **Recipe:** 6.37's exactly, from scratch, through the runner's same `train` line (rank 32, attention and MLP, 3e-4,
   3 epochs, epoch-2 save, `--loss-on chat_decision`). The train report must show 1,094 rows and `decision_rows` 222.
5. **Comparison.** At 82 and 83 the recall reference is 6.37's 192 (probe) and 163 (`hard_dev`), stricter than v6's
   192 and 157. At 97 to 99: 6.37 retrained from its byte-identical set (training since 14:50, queued first and alone
   on the card); pooled three-seed sums on probe and `hard_dev` recall, ties pass; 6.37's files there are scored by
   script and not read until 6.38's are done; if they do not finish by Monday 12:00, 6.38 fails; they do not
   re-decide 6.37's shipping.
6. **Gates.** At 82 and 83: R-086 whole (unjudged lines and judged sheets, three fresh judges, judge 1 deciding),
   R-094 (slips, recall against item 5's reference), R-097, R-102's 82-and-83 items. At 97 to 99: R-076's rule with
   Sheets A, B and h, R-094's slips (probe pooled over 82, 83 and 97 to 99 at most 8), item 5's recall line, R-102's
   fresh-seed items. **Any failed line stops the try; there is no 6.39.** On a full pass 6.38 seed 82 replaces 6.37.
7. **Clock.** 82-and-83 training starts before 22:00 (latest safe start for 82: 21:08); fresh-seed training before
   Monday 04:00; nothing after Monday 12:00. Reported, not gated: `hard_dev` found-but-wrong at 82 and 83 against
   6.37's 22 (retrieval's request), in-view and lower-case in-view against 6.37's own seeds, with no gain claimed below
   +3 a seed (statistics).
8. **Write-up:** candidate 17 since R-093; targets hand-written after reading misses on items that 82, 83 and 97 to 99
   score again, so in-view gains are not independent evidence (only the sealed pool after the freeze is); the
   copied-phrase evidence; the four bad rows left unchanged; the in-view and lower-case results whatever they show; on
   a fail, 6.37 ships and the deflecting targets are the probable cause.

## R-135 · 2026-11-08 · SPRINT · 6.38's set: built, vetted, frozen

`PYTHONPATH=src python scripts/records/build_r134.py --vet results/vet/R-134` from `fix17cs37.jsonl` (sha256
`04df294a...`): 1,094 rows (`confirm` 230, `in_view` 150, `never_told` 160, `older` 332, `statement` 222), 28 final
answers changed, every other line byte-identical (the build checks it; sha256 of the 1,066 unchanged lines
`61729f2c...`). Out: `data/screens/fix17cs38.jsonl`, sha256
`572623ca702e33a78003786276c7265064e58f8fb544d8474ecf142f960b4c18` as first written; that file was broken and was
rebuilt to `f4daff77e63b33db7268be155ef850e07e255dfb564064cc6dad945fbe180edc` (R-136).

**The rules were checked against known-bad input first:** run on the 28 old targets, `check` rejects all 28 (18 with
the value not in the first sentence, 8 not opening with the name or value, 2 with a question), and it rejects a
"Your brother Ivan ..." opener, a reply without the value, an added question and an added sentence not found in
another in-view target. All 28 new targets passed on the first build; none was rewritten.

The new targets are one plain sentence stating the fact as the chat gives it ("Priya writes fantasy novels at
night.", "Tomas rents on the twentieth floor."), three with one more sentence copied from another in-view target
("5k is a solid achievement.", "That's a big promotion.", "That's a pretty cool prize!").

**Vetted** (`results/vet/R-134/`: `items.txt`, `key.json`, `marks.json`, `rubric.txt` = R-118's): one fresh Sonnet
judge, its own folder, the 28 new and 28 old answers shuffled together (random seed 134), blind to which is which.
New: 28 of 28 marked 1. Old (hidden controls, reported only): 0 of 28. Transcript audited: it read its rubric and
sheet and wrote only `marks.json`, by heredoc.

**Queued** (backlog lines 264 on): 6.38 at 82 and 83 (`cand`, the runner's same `train` line as 6.37), then
`decide_r134.py` (R-086 unjudged, R-094 with item 5's 6.37 reference, R-097, and R-102 once scored; a FAIL stops every
later 6.38 line), the eight R-102 stress runs, `decide_r134.py` again, 6.37's plain scoring at 97 to 99, then 6.38 at
97 to 99 with its stress runs, and the four lower-case runs at 82 and 83 (reported only). R-086's judged sheets run on
the CPU once 82 and 83 are scored; a judged fail stops the 97-to-99 lines by the same stop file.

## R-136 · 2026-11-08 · SPRINT · 6.38's set: doubled line endings, rebuilt

6.37's training at 97 to 99 ran 34 minutes a seed (not the 52 assumed in R-134), so 6.38 at 82 started at 16:33. All
three tries at 82, and the first two at 83, stopped at once: `run_recall_train.py` reads `--data` with
`read_text().splitlines()`, and line 1 of what it got was empty. No adapter was made and nothing was scored.

**Cause.** `fix17cs37.jsonl`'s working copy is CRLF (git stores it LF, `core.autocrlf` true). `build_r134.py` kept each
unchanged line with its own `\r\n` and wrote with `Path.write_text`, which on Windows turns `\n` into `\r\n`: the
1,066 unchanged lines ended `\r\r\n` and read back as 2,160 lines, 1,066 of them blank. The 28 changed rows were
written correctly. The build's own checks compared lines in memory and did not read the file back.

**Fix.** The build now drops line endings on reading, writes `\n` bytes, and stops unless the written file reads back
as 1,094 lines. It accepts 6.37's set as checked out (sha256 `04df294a...`) or as git stores it (`7b0183de...`). Rebuilt
with the same 28 answers: 1,094 lines, none blank, no CR; exactly 28 rows differ from 6.37's, each in its final turn
only; sha256 `f4daff77e63b33db7268be155ef850e07e255dfb564064cc6dad945fbe180edc`; the vet sheet rebuilt byte for byte,
so R-135's marks stand. `tests/test_screen_sets.py` (new) reads every `data/screens/*.jsonl` as the trainer does and
fails on a blank line or a non-JSON line; checked first against the broken file, which it rejects.

**Queue.** Line 265 (6.38 at 83) was waiting for a clean tree on its third try and trains on the rebuilt set once this
is committed. R-134's later 6.38 lines (266 to 297) are stopped by `r134_stop_38`, touched by hand at 16:37 so they
cannot run out of order; 6.37's plain scoring at 97 to 99 (lines 276 to 278) is unguarded and runs. 6.38's lines are
queued again after them, in R-134's order, with the stop file `r136_stop_38`. The timeline still meets R-134's clock:
82-and-83 training before 22:00, fresh-seed training before Monday 04:00.

## R-137 · 2026-11-08 · SPRINT · Prompted-baseline control, registered before it runs

**Why.** An outside reviewer (passed on by Kevin) asked how much of the gain comes from the LoRA and how much a better
prompt alone could buy. Checked first: base and every adapter run on identical items (240 of 240 match on message,
answer and view, probe and `hard_dev`), the same system prompt, tool, result format and decoding (greedy, 60 tokens);
the prompt and tool code did not change between base's runs and 6.37's. Split by search (seed 73157 items): base
searches 37 of 96 probe recall questions and is right on 30 of those 37, 0 of the 59 it does not search; 6.37 at 94 to
96 searches 287 of 288 and is right on all 287. `hard_dev`: base searches 58 of 96 and is right on 20; 6.37 searches 283
of 288 and is right on 247. Base with no tool: 1 and 0 of 96. No prompt-only baseline was ever run.

**Kevin, 2026-11-08:** "yeah add the prompted baseline control". The reviewer's conditions, all taken: keep the tool,
decoding, token budget and test cases identical; the same prompt variants on both test sets, fixed before any result;
general instructions and a few representative examples from outside the evaluation set, not tuned to its questions.

**The control.** `scripts/run_recall_eval.py --system-prompt-file` (new; default unchanged) replaces only the tool
arm's opening line ("You are chatting with a friend. You can search the earlier conversation."); the tool schema and
calling format follow it unchanged. Two prompts, written once, committed here before any run:
- **A, rules** (`results/control/R-137/prompt_a.txt`, sha256 of the stripped text
  `333b7319bae3940c4485ad8536bfec948a516226284fffed551f1a2d21296ee0`): five general rules: search when a fact told
  earlier is not in view; answer the exact detail and whose it is; say plainly when nothing is found; answer from view
  without searching; reply naturally to plain chat.
- **B, rules and examples** (`prompt_b.txt`, `d4d81aaa814654b11c4425db18624fbd49df720cf13303c2a4928c170a4dc4f0`): A and
  four worked examples with made-up names and facts (a search and its answer, a fact in view, a search that finds
  nothing, plain chat), in the harness's exact call and result formats. Neither prompt shares a four-word run with the
  probe or `hard_dev` pools (`build_r110.TEST_GRAMS`); two phrases in B that did ("that's a lovely", "hope the rest
  of") were reworded before this record.

**Runs** (base, no adapter, `--arms tool_loop`, probe and `hard_dev`, seed 73157, 24 items a kind: the same 240 items
each as every recall result): four runs, queued before 6.38's judged hold so the card works while the judges mark.
**Reported, not gated:** per kind, searched and right-when-searched for recall, and right decisions on `in_view`,
`never_told` and `statement` (a prompt that buys searches by over-searching shows there), against base's default
prompt and 6.37. Base's runs are deterministic (greedy, one model), so one run each.

**Statistics, adopted for the write-up** (the reviewer's last point): pooled counts over training seeds are three or
five runs over the same questions, not independent cases; every pooled count is reported with its per-run scores and
their spread.

## R-138 · 2026-11-08 · SPRINT · 6.38 is the last try; break tests, registered before they run

**Kevin, 2026-11-08 ~19:00:** "alright we're calling this the last try then we're going to start adding comparison
tests so we can break it and if we find anything specific we can target that". So no 6.39 from the old route: after
6.38, a new training try exists only as a targeted fix for a break these tests find.

**Conditions** (`run_recall_eval.py`, existing options only, `--arms tool_loop`, 24 items a kind, probe and
`hard_dev`, discovery seed 74001, never used before):
- `plain`: the reference at this seed.
- `d4`: `--decoys 4`. Training puts 0 to 2 decoys in recall chats and 1 to 3 in `never_told`
  (`run_build_training_set.DECOY_CHOICES`), so 4 is outside training for every kind; it is also the crowded
  condition of the registered final test (R-065). `--decoys 5` cannot build on probe (a fact type has too few values).
- `long`: `--sizes 1000 2000`, chats two and five times the longest tested.
- `longfixh`: `--corrections-heldout --kinds older confirm --sizes 1000 2000`: old and new value both somewhere in a
  long chat; does it answer the stale one?
- `askd4`: `--asked-before --decoys 4`: a declined question in view and four decoys; does it skip the search or name
  the wrong person?
All 2,112 items were built on the CPU first (counts only, no content read): none fails.

**Models.** 6.37 (seed 82) first, queued before 6.38's judged hold so its results are in by about 23:30; then 6.38
at 97 to 99 as R-136 queued; then 6.38 seed 82 (only if its judged sheets pass) and base with recall kinds only.
One queue, one card, in that order. Labels `brk_<condition>_<probe|hd>_<model>_seed_74001`.

**What counts as a break.** For each adapter, against its own reference at 74001: a net loss of at least 8 of 192 on
recall (older and confirm pooled over the two sizes; 96 for `longfixh`'s pairs) or 4 of 96 on another kind, and, where
the items are paired, losses at least twice the gains. Paired: `d4` and `askd4` against `plain` (decoys come from a
separate generator, so the rest of each chat is the same), `askd4` against `d4`, `longfixh` against `long`. `long`
against `plain` is not paired (the chat size enters the item seed), so the net rule alone applies there. Also a break:
recall below base in the same condition. Then I read the misses and name the failure.

**A targeted fix**, only after the break is confirmed: the broken condition rerun on 6.37 at confirm seed 75001, with
its reference, meets the same rule. The fix's rows come from the TRAIN pool only, never from probe or `hard_dev`
items; it trains from scratch at 82 and 83; it must pass every existing gate unchanged (R-076, R-086, R-094, R-097,
R-099, R-102) against 6.37, and beat 6.37 in the broken condition at seed 75002 pooled over 82 and 83 (ties fail),
on a held-out form of the condition where one exists (trained on train-wording corrections, judged on the held-out
wordings). **Go/no-go: fix rows ready by Mon 09:00**, training started before 12:00 (R-134's clock); otherwise the
break goes in the write-up as a measured limit, and 6.37 (or 6.38 if it wins R-134's test) ships.

**Panel** (one Opus agent, three lanes, one arguing against; transcript audited: one flagged call matched only on the
word it excluded, and no line came from a sealed file). Adopted, all ten: check the training decoy range (done:
decoys 4, not 3); split the stacked condition into single questions (`longfixh`, `askd4`); paired flips in the
trigger; below-base on recall only (base rarely searches, so it is near full on the other kinds); confirm a break at
75001 before building a fix; judge at a third seed on a held-out form; compare at matching seeds 82 and 83; base on
recall kinds only; one ordered queue; a go/no-go time. Its case against, recorded: a fix built from the generator
that found the break is fitted to that generator, and an honestly written limit is worth more than a rushed fix.
That is why the confirm seed, the held-out form and the go/no-go time exist.

Reported per run with spread beside pooled counts (R-137).

## R-139 · 2026-11-08 · SPRINT · Rigor additions, registered before any is computed

**Why.** Kevin passed my R-138 plan and the project's numbers to a different model and asked how to add rigor. Its
main points: generalization beyond the generator's structure is the biggest gap; report answer and search behaviour
separately; break failures into stages; a primary comparison fixed in advance with a correction on the rest; a
human blind check of the scorer; resample at the right unit. My reply corrected two points: each test question has
its own chat, so the dependent unit in our sets is the fact template, not the conversation; and the prompted-baseline
claim waits for R-137's runs. **Kevin, 2026-11-08 ~19:25:** "fine".

**Disclosure.** The development counts below (6.37 and base on probe and `hard_dev`) have been read in aggregate many
times. This record fixes the analysis before its tests and breakdowns are computed; it does not make those sets
blind. The independent set (item 4) is the only part no one has seen.

**1. Primary development comparison.** Recall (`older` and `confirm`, 96 items at each of 58 and 419 messages) of
the shipping copy, 6.37 seed 82, against base, `tool_loop`, on `hard_dev` at seed 73157 (`hd_fix17cs37_82`,
`hd_base`): R-016's two-sided exact sign test on the items where they differ, significant below 0.01 (R-016's level).
One fixed system against another on the same items, the case the sign test (exact McNemar) is for.
**Secondary family, Holm at 0.05,** the same test, 6.37 seed 82 against base on the same items: probe recall
(`probe2_base`); held-out corrections, probe and `hard_dev` (`st_fixh_*`); phone-style recall, probe and `hard_dev`
(`st_phone_*`); right search decision on `in_view`, `never_told` and `statement`, probe and `hard_dev` pooled per kind
(three tests, two-sided, so a loss counts as much as a gain). Nine tests in all, the primary and eight secondary (corrected before any was computed: the first text of this record said ten).
**Across training seeds, descriptive, no test:** per-seed counts, minimum and maximum, the pooled gain with a 95%
percentile interval from `stats.bootstrap_gain_interval`, resampling **fact templates**, not items (items that share a
template are not independent; with one question a chat, the conversation is not the right unit). The template of
each item is recomputed from its seed by the generator's own first draw; results name templates by index only. Seeds
82, 83 and 94 to 99: 6.38's comparison was read at 19:32 (R-140), which lifted the hold on 97 to 99. The
corrections and phone conditions were never scored at 97 to 99; those twelve runs are queued, and until they land
each table names the seeds it used.

**2. Failure breakdown** of every wrong recall answer, per model and seed, mechanical from the result rows: (a) did
not search; (b) searched, no query found the fact (`found_fact` false); (c) found it, the reply names a decoy or other
forbidden value; (d) found it, wrong in another way (missing or garbled detail); (e) ran out of calls, counted
separately. Descriptive.

**3. Distance and crowding.** Recall by the number of exchanges between the fact and the question (quarters within
each chat size), and by decoys a chat (1 at 73157 and 74001, 4 from R-138's `d4` runs). Descriptive.

**4. Independent development set, report only.** A fresh agent with no access to the repo, the templates, the pools or
any example from them writes about 40 chats from a behaviour spec only, with questions, gold answers and the values a
wrong answer would name. The spec asks for same-name people and near relations (a sister and a sister-in-law), facts
never told, facts still in view, corrections and plain chat, in ordinary typing. The spec goes to one adversarial
panel before the writer sees it; the writer's transcript is audited. A loader turns the chats into the harness's items
(last 3 exchanges in view, the rest searchable); its scorer is the existing one, checked on gold-as-answer and on the
wrong values. Run once on base, 6.37 seed 82, and 6.38 seed 82 if it replaces 6.37, appended after R-138's runs.
**Primary on this set:** recall, 6.37 seed 82 against base, exact sign test, with a paired bootstrap interval
resampling conversations (several questions share a chat here). **Never a source for a fix,** whatever it shows: a
break found here goes in the write-up as a limit.

**5. Kevin's blind check.** 50 scored answers, drawn by `random.Random(139)` in strata (scored right, scored wrong,
named a decoy, other) from base and 6.37 seed 82 on probe and `hard_dev`, shuffled, model names removed. Kevin marks
each right or wrong from the chat, question and gold answer. Reported: agreement with the script (count and Cohen's
kappa) and every disagreement listed. Claude marks none.

**6. Deferred, stated as limits in the write-up:** LoCoMo (R-100, on its own registered clock), other languages,
two facts in one question, and a provenance test (the model repeats a fact wrongly and the user corrects it).

**Why each part** (added before any part was computed, at Kevin's request to explain the reasons):
- *One primary test, named first:* with many tables, the one that looks best can be picked afterwards and reported
  as the result. Naming it first removes that choice. It repeats R-016's measure and test, so the development result
  and the sealed result answer the same question.
- *Holm on the rest:* nine tests at 5% each would give a false "significant" by chance more often than 5% of the
  time. Holm keeps the whole family at 5% and is never weaker than testing each one alone at 5% divided by nine.
- *Per seed, with the range:* a training seed changes the adapter, not the questions. Pooling three or eight seeds
  over the same 192 questions is not 576 or 1,536 independent cases. The range shows how much training alone moves
  the score.
- *Resampling templates:* questions built from one fact template share wording, so a model that learned that
  template gets all of them right or all wrong together. Resampling single questions would treat them as
  independent and make the interval too narrow.
- *Failure stages:* "wrong" can mean it never searched, searched badly, found the fact and named someone else's, or
  found it and garbled it. Each has a different cause, and only some could be fixed by training.
- *Distance and crowding:* a model can look good on average while failing on facts told long ago or among many
  look-alike facts. These tables show whether it does.
- *The independent set:* every development test so far comes from the same generator as the training data. Separate
  names and wordings do not remove shared structure: where facts sit, how questions are phrased, how decoys look.
  A writer who has never seen the generator tests whether the gain is real recall or learned structure.
- *Kevin's check:* the script decides "right" by finding the answer string and no wrong value. It can miss a right
  answer worded oddly, or pass one that names the answer while saying something false. A person reading a blind
  sample measures how often the script is wrong.

**Timing.** Items 1 to 3: CPU, tonight. Item 4: spec and panel tonight, writer overnight, GPU after R-138's runs
(Monday morning). Item 5: whenever Kevin has an hour, before the write-up (Nov 12). None moves a gate or the clock.

## R-140 · 2026-11-08 · SPRINT · 6.38 fails R-134; 6.37 ships

**Result** (`decide_r134.py fix17cs38`, 19:31, on R-134's registered lines, unchanged): 6.38 passes sixteen of
seventeen. It fails one: `hard_dev` recall pooled over seeds 82 and 83 is 157 of 192 against 6.37's 163 (R-134: not
below 6.37, ties pass). Probe recall ties 6.37 at 192; slips are 0 at every seed; probe `in_view` is 44 and 46
(R-097's floor is 41). So the rewrite of the 28 deflecting in-view targets kept everything it was built to keep and
cost six recall answers on the harder set; R-134 counts any loss as a fail.

**Decision, by rule, not by judgment:** R-134 said any fail ships 6.37. R-138 recorded Kevin's word that 6.38 is the
last try. **6.37 (fix17cs37 seed 82) is the frozen candidate.** 6.38's judged sheets were not built: R-134 needed
them only for a candidate that passed the unjudged lines. The stop file `r136_stop_38` was touched by the decision
script; it skips 6.38's training at 97 to 99 and every later 6.38 line. Four 6.38 user-style lines at the end of the
queue had no guard and were given one by hand.

**Freed GPU time** (about three and a half hours) goes to R-139: 6.37's held-out corrections and phone runs at seeds
97 to 99 (twelve runs), so every condition has eight training seeds. R-138's break tests run as queued: 6.37's, then
base's; 6.38's are skipped by the same stop file.

## R-141 · 2026-11-08 · SPRINT · R-139's development analysis, items 1 to 3

`scripts/records/rigor_r139.py`, output `results/analysis/R-139/dev_rigor.json`, run once at 19:50 after R-139's
amendment was committed. Nothing in R-139 was changed after this run.

**Primary** (`hard_dev` recall, 6.37 seed 82 against base, 96 items): base alone right on 4, 6.37 alone right on 57;
exact sign test p = 4.9e-13, below R-016's 0.01.

**Secondary** (Holm at 0.05, all eight significant, each 6.37 seed 82 against base on the same items):

| Test | Base alone right | 6.37 alone right | Items | p |
|---|---|---|---|---|
| probe recall | 0 | 66 | 96 | 2.7e-20 |
| held-out corrections, probe | 0 | 87 | 96 | 1.3e-26 |
| held-out corrections, `hard_dev` | 2 | 75 | 96 | 4.0e-20 |
| phone typing, probe | 0 | 55 | 96 | 5.6e-17 |
| phone typing, `hard_dev` | 2 | 49 | 96 | 1.2e-12 |
| right decision, `in_view` (both sets) | 0 | 20 | 96 | 1.9e-06 |
| right decision, `never_told` (both sets) | 0 | 48 | 96 | 7.1e-15 |
| right decision, `statement` (both sets) | 0 | 29 | 96 | 3.7e-09 |

**The finding that limits all of the above: few fact templates.** The 96 recall questions on probe are built from 5
fact templates, and those on `hard_dev` from 8. The sign test treats each question as independent; questions from
one template are not, so **the p-values above overstate the evidence** and are reported as computed, with this
caveat beside them. The template-resampled intervals are the measure that respects the dependence. With 5 and 8
groups a percentile bootstrap is itself rough, and it is reported as rough, not as exact coverage.

**Across training seeds** (recall of 96; gain = 6.37's rate pooled over the seeds minus base's, 95% interval
resampling templates):

| Condition | Base | 6.37 per seed (82, 83, 94 to 99) | Range | Gain [interval] | Templates |
|---|---|---|---|---|---|
| probe | 30 | 96, 96, 96, 95, 96, 96, 95, 96 | 95 to 96 | +0.685 [+0.578, +0.845] | 5 |
| `hard_dev` | 20 | 73, 90, 77, 87, 83, 79, 80, 76 | 73 to 90 | +0.632 [+0.521, +0.759] | 8 |
| held-out corrections, probe | 9 | 96, 96, 96, 95, 93 (82 to 96 only) | 93 to 96 | +0.898 [+0.791, +0.986] | 5 |
| held-out corrections, `hard_dev` | 8 | 81, 86, 83, 83, 77 (82 to 96 only) | 77 to 86 | +0.771 [+0.650, +0.870] | 8 |
| phone typing, probe | 32 | 87, 89, 91, 85, 85 (82 to 96 only) | 85 to 91 | +0.577 [+0.501, +0.673] | 5 |
| phone typing, `hard_dev` | 20 | 67, 80, 60, 77, 72 (82 to 96 only) | 60 to 80 | +0.533 [+0.389, +0.681] | 8 |

The seed spread on `hard_dev` is 17 answers of 96 (73 to 90): training seed alone moves the score that much. **The
shipping copy, seed 82, is the lowest of the eight on `hard_dev` recall.** It was chosen before seeds 94 to 99 existed,
because the gates are set at 82 and 83. Reported, not acted on: picking a seed by its development score would be
selection on the development set, and which adapters enter the sealed run is R-016's and Kevin's call.

**Failure stages of wrong recall answers** (R-139 item 2; plain sets):
- probe: base 66 wrong (59 never searched, 3 searched and missed, 1 named a wrong value, 3 found and still wrong);
  6.37 at eight seeds: 2 wrong in all (one never searched, one search missed).
- `hard_dev`: base 76 wrong (38 never searched, 7 missed, 9 named a wrong value, 21 found and still wrong, 1 ran out of
  calls). 6.37 at seed 82: 23 wrong, of which **18 found the fact and still answered wrong**, 3 missed, 1 never
  searched, 1 named a wrong value. Over the eight seeds the same stage leads at six of them (3 to 18 a seed). So
  6.37's remaining `hard_dev` gap is mostly not search; it is reading or wording the answer from a result that holds
  it. This set cannot be a source of training rows (R-138), so it is reported as the main limit, and R-139's
  independent set will show whether the same stage leads there.

**Distance** (R-139 item 3; quarter 0 = told earliest): on probe 6.37 is at or near full in every quarter at both
sizes. On `hard_dev`, 419-message chats, the earliest quarter is the weakest at most seeds (7 to 10 of 13, against 11
to 13 of 14 in the latest); in 58-message chats there is no such pattern. A mild fall with distance in long chats,
descriptive, on 10 to 15 items a cell. Crowding (1 against 4 decoys) waits for R-138's `d4` runs.

## R-142 · 2026-11-08 · SPRINT · The independent set and Kevin's sheet, set up before any chat is read

**Why this set exists.** Every development result so far comes from the generator that also made the training data
(R-141: the recall questions come from 5 fact templates on probe and 8 on `hard_dev`). A model can learn that structure
(where facts sit, how questions are worded, how decoys look) and score well without recalling in general. Chats
written by someone who never saw the generator test whether the gain survives a change of structure.

**The brief** (`data/blind_dev/brief.md`, the text each writer got, with its four settings): behaviour only, no
template, pool, example or result from the project. Each conversation 20 to 30 exchanges, at least five people, a
pair of look-alike people (same first name, or a sister and a sister-in-law) with facts of one type, one correction,
facts placed anywhere, typing varied from tidy to rough; six alternative final questions (two `older`, one of them
about a look-alike; `confirm`; `in_view`; `never_told`; `statement`), each with its answer, the wrong values a careless
reply would give, and the exchange that holds the answer. Four writers (fresh Opus agents, one at a time, no access
to anything but their brief and Write), ten conversations each, settings: family and neighbours; work and clients;
friends, hobbies and travel; a move to a new city.

**Panel on the brief** (one Opus agent, three lanes, one arguing against; transcript audited: it read only the
brief). Taken, nine edits: half the confirm questions name a wrong value (the old one or the look-alike's) and the
right reply gives the true one, so echoing the user cannot pass; one question in each conversation targets the
corrected fact; questions may not reuse the fact sentence's words, so search cannot match on copied wording;
answers and wrong values spelled correctly, one word or a proper name, at least 4 letters; the look-alike question
names the person by relation; a statement mentions nothing from before the last 3 exchanges; a third of
conversations state a target fact indirectly (a pronoun, a roundabout phrase); the example values removed and at
least six fact types asked for. **Declined, one:** whole-word matching in the scorer. R-139 registered the existing
scorer, every other result uses it, and a different scorer on one set would make the sets incomparable; the 4-letter
minimum removes most short-substring matches, and Kevin's check (below) measures what is left. **Its case against,
recorded as a limit:** four writers of one model family share habits (names, fact types, phrasing), so this is
closer to one writer with four settings than to four independent writers; about 40 items a kind gives roughly plus
or minus 15 points, so only large gaps mean anything; numbers and dates are not covered. Human-written chats would be
more independent still; none are planned before the freeze.

**Loader** (`src/aya_retrieval/dev_set.py`, `tests/test_dev_set.py`, commit `9f2de4d`): each question becomes a
`RecallItem` on its conversation, so the harness, search tool, view (last 3 exchanges) and scorer are the ones every
result uses. A question that breaks a brief rule is dropped with its reason and never repaired: repairing it would
mean editing the writer's material. The drop list and a sha256 over every file are written into each result.
`run_recall_eval.py --items-dir` scores the written chats and refuses every stress option; without it the loop
builds the same items in the same order as before (the loop body moved into a generator, unchanged).

**Runs** (queued after R-138's and the twelve 6.37 runs of R-140, behind `$S/blind_ready`, touched once the 40 files
are checked and committed to `data/blind_dev/chats/`; not ready by Mon 09:00, the lines skip): base; base with R-137's
prompt A and prompt B; 6.37 at all eight seeds. Labels `blind_<model>_seed_0`. **Primary** (R-139): recall, 6.37 seed
82 against base, exact sign test, with a paired bootstrap interval resampling conversations. Also reported: per kind,
per writer, per seed with its range, and the R-137 prompts beside base, each prompt on its own. **Report only:**
nothing found here becomes training data or a reason to change the frozen model.

**Kevin's sheet** (`scripts/records/build_human_check_r139.py`, `results/human_check/R-139/sheet.json` and
`key.json`, commit `d3b8d53`). Restratified before anyone marked a line, from R-139's "scored right, scored wrong,
named a decoy, other": drawn by verdict alone, 47 of 50 lines would have been base, mostly replies with no search
and no answer, where the scorer cannot be wrong. Now by model and verdict: 6.37 scored right 12, 6.37 scored wrong
15 (of its 33 wrong at seed 82), base scored right 10, base scored wrong after a search 13. Kinds `older`, `confirm`,
`in_view`, `never_told` (a statement is scored on the search alone). Each line shows the question, what was told, the
right answer, the wrong values and the reply; no model name. Kevin marks right or wrong; Claude marks none and does
not read the key until he has.

## R-143 · 2026-11-08 · SPRINT · The independent set is written and frozen

**Written.** Four fresh Opus agents, one at a time (R-142's brief, settings w1 to w4), ten conversations each:
`data/blind_dev/chats/w1_01.json` to `w4_10.json`, 20 to 30 exchanges each. **Frozen here:** sha256 over every file's
name and bytes in name order (`dev_set.load_dev_set`) `9919a24ca1cab8a982ff73a010559a632370170644c137e754c6ac5bd8aa302c`.
No one has read a chat: the checks below are mechanical and print counts only.

**Writer audit** (each transcript, every tool call): each read only its own brief and wrote only its own ten files
into the set folder; none ran a command or searched. Writer 2 wrote two of its files twice and writer 4 all ten twice
(each rewriting its own material). Writer 3 used Edit once on its own `w3_06.json` to reword one question, which its
brief did not list as allowed; it reported this itself. It changes only that writer's own text, so the file stays.

**Loader** (R-142's rules): 240 questions kept, 0 dropped: `older` 80, `confirm` 40, `in_view` 40, `never_told` 40,
`statement` 40, 60 a writer. **Scoring limit found here:** 60 of the 160 questions that carry an answer list no
wrong values (`older` 15, `confirm` 17, `in_view` 28), because the writer's chat held no other value of that type.
On those the scorer checks only that the answer is present, so a reply that also says something false is not caught.
Reported beside every result on this set, not repaired (repair would mean editing the writers' material).

**The reshaped eval loop builds the same items** (R-142's change to `run_recall_eval.py`): `hd_base_promptb` ran on
commit `8e3f7ac`, which includes the change, and `hd_base_prompta` on `58e2afb`, before it; their 240 rows have the
same id, size, kind, message, answer and view, in the same order.

**Runs** go as R-142 queued them, released by `$S/blind_ready`, touched after this commit.

## R-144 · 2026-11-08 · SPRINT · Kevin's blind check of the scorer, and the shape of the wrong replies

**Why.** Every recall number in this project comes from one rule: a reply is right when it contains the answer and
no wrong value. If the rule is wrong in one direction, every gain is wrong with it. Kevin marked R-142's 50 lines
right or wrong without seeing the model or the verdict; his marks were saved to
`results/human_check/R-139/marks.json` before `key.json` was read. `scripts/records/score_human_check_r139.py`
compares them and writes `agreement.json`.

**Agreement: 47 of 50, Cohen's kappa 0.88.** Kevin right and scorer right 22, both wrong 25, Kevin right and scorer
wrong 3, Kevin wrong and scorer right 0. By stratum: 6.37 scored right 12/12, 6.37 scored wrong 14/15, base scored
right 10/10, base scored wrong after a search 11/13. **The scorer never passed a reply Kevin failed**, so no reported
gain is inflated by a lenient scorer. The three disagreements, all scorer stricter than Kevin:

- Line 6 (base, confirm): the reply names the answer and the look-alike's value side by side ("the cockatoos (or
  cockatiels)"). The scorer fails a reply that hedges between the two; Kevin passed it.
- Line 29 (base, confirm): the reply gives the right dish and then, correctly attributed, another person's dish.
  The scorer cannot tell a wrong value said as the answer from one said about someone else.
- Line 37 (6.37, in_view): the reply asks Kevin to say more and gives no subject at all. Kevin marked it right. It
  is recorded as he marked it; it is likely a slip, and it does not change the direction of the finding.

**Kevin's note after marking, on line 42** (base, `probe2_base`, scored right by both): the reply printed the raw
search result ("Tool result for search_corpus: [chunk_id=...]") before the answer. He marked it right on its content.
The scorer does not look for leaked tool text, so it passes such a reply when the answer is in it. Counted over the
full runs (240 replies each): `probe2_base` 5 replies with tool text, 2 scored right; `hd_base` 3, 0 scored right;
`probe_fix17cs37_82` 0; `hd_fix17cs37_82` 0. This leniency favours base only, by 2 of 480 replies; 6.37 never leaks
tool text.

**Size of the strict-scorer effect.** The two real cases (6 and 29) are replies that hold the answer and a wrong value
together. Counted over the full runs at seed 82's settings (`older` and `confirm`): `hd_base` 9 of its 76 wrong,
`hd_fix17cs37_82` 0, `probe2_base` 0, `probe_fix17cs37_82` 0. If all 9 were fair, base's `hard_dev` recall would
move from 20/96 to at most 29/96, against 6.37's 73/96. The bias runs against base only, so it is disclosed beside
every base number; it does not reverse any result.

**The shape of the wrong replies (Kevin's 25 wrong lines, then the full `hard_dev` run).** On the sheet, 6.37's 14
wrong replies: 9 found the right exchange and restated its main clause, stopping before the answer ("Your coach Rhys
hosted a big dinner." for "...the dish everyone fought over seconds of was the minestrone"); 4 did not search and
made small talk (3 of them `in_view`); 1 searched and said it could not see the fact. None named a false value.
Base's 11: 6 named a false value (the look-alike's, or a value for a question never told), 3 went off topic, 2
looped on the search and printed the tool call. Over all 96 `older` and `confirm` items of `hd_fix17cs37_82`
(73 right, 23 wrong), grouped by fact template with the person's role removed: 1 of the 23 misses names a false
value; the "collected the keys ... ready for the parrots" template holds 9 misses (6/15 right) and the "hosted dinner
... the dish was the chowder" template 6 (7/13 right), 15 of 23 between them; the "job interview booked for Monday"
template 4 (10/14). The other five templates are 51 of 54. In all three weak templates the sentence's main clause is
about another event and the answer sits in a later clause. On probe, where every template is one short clause
("who is my tutor, is terrified of spiders"), 6.37 is 96/96.

**What this is and is not.** It is one failure, specific enough to target: 6.37 answers from the first clause of a
long sentence. It was found on `hard_dev`, a development pool, so a fix built to match these templates would be fit
to the set that judges it. The independent set (R-143, written by four writers who never saw the generator) runs
tonight; whether the same shape appears there decides whether it is general. Nothing here changes the frozen model.

## R-145 · 2026-11-08 · SPRINT · A second, independent marker for the scorer check

**Why.** R-144 rests on one person's marks. A second person marking the same lines blind tests the marks
themselves: if two people agree with each other, a disagreement with the scorer is about the scorer, not one
marker's reading or attention.

**How.** `results/human_check/R-139/second_marker_sheet.txt` (commit `7d8ae71`): the same 50 lines in the same order,
each with the question, what the reply should say (the right answer, or "that it was never told this") and the
reply, and a three-line instruction; no model, verdict, wrong-value list or key. Kevin gave it to one person, who
marked it independently (Kevin's word, 2026-11-08); her filled sheet is kept as `second_marker_filled.txt` and parsed
to `marks_second.json`. She wrote one note, on line 42: "(tool call?)", the leaked search text R-144 counts.
`score_human_check_r139.py` compares her marks with the scorer and with Kevin's.

**Result.** With the scorer: 48 of 50, kappa 0.92; she never passed a reply the scorer failed or failed one it
passed except lines 6 and 29, where she, like Kevin, passed a reply the scorer failed. With Kevin: 49 of 50, kappa
0.96; the one difference is line 37 (Kevin R, she W), the reply that gives no subject. **Reading.** The two
disagreements both people share are R-144's strict-scorer case (the answer and a wrong value in one reply), so that
case is a property of the scorer; R-144's bound on it stands (base's `hard_dev` recall at most 9 of 96 higher, 6.37
unaffected). The sheet she marked carried less than Kevin's (no fact sentence, no wrong values), so the two sheets
are not identical conditions; both were blind to model and verdict.

## R-146 · 2026-11-09 · SPRINT · The independent set, the prompted-baseline control and the break tests, read

All runs finished 2026-11-08 23:49; this record was written from 05:13 (the card was idle in between: nothing was
queued behind the last run).

### The independent set (R-142's report, as registered)

`scripts/records/blind_r146.py`, `results/analysis/R-146/blind.json`. Every run was scored on the frozen set (sha256
checked against R-143, nothing dropped): 240 questions on 40 chats.

**Primary (R-142): recall (`older` and `confirm`), 6.37 seed 82 against base: 39 of 120 against 26 of 120**, a
relative gain of +50%. Base alone right 12, 6.37 alone right 25, exact sign test p = 0.047. Paired bootstrap
resampling whole chats: difference +10.8 points, 95% interval +2.5 to +19.2; relative gain +50%, interval +9% to
+122%. The gain holds on chats the generator never made, but it is far smaller than on the generator's sets
(`hard_dev` 20 to 73 of 96, +265%) and recall is low for both models.

**Each training seed:** recall 39, 43, 57, 46, 48, 52, 46, 50 (seeds 82, 83, 94 to 99); the shipped seed 82 is the
lowest. Pooled over all eight against base: +18.0 points, interval +9.7 to +26.1 (relative +83%, +35% to +171%). As
R-137 adopted, the eight are runs over the same questions, not independent cases; the range is the honest spread.

**Each kind** (right of 80 `older`, 40 each other kind; base / seed 82 / the eight seeds' range): `older` 11 / 28 /
26 to 35; `confirm` 15 / 11 / 11 to 22; `in_view` 36 / 35 / 32 to 37; `never_told` 34 / 37 / 33 to 39; `statement` 38 /
37 / 33 to 39. **`confirm` at seed 82 is below base.** Right decisions (searched exactly when the answer is out of
view): `older` base 49, 6.37 79 to 80 of 80; `confirm` base 5, 6.37 2 to 21 of 40 (seed 82: 9); `never_told` base 25,
6.37 37 to 40.

**Each writer** (30 recall questions each; base / seed 82 / seeds' range): writer 1, 6 / 11 / 11 to 16; writer 2,
7 / 10 / 10 to 17; writer 3, 7 / 9 / 9 to 16; writer 4, 6 / 9 / 7 to 9. The gain is in every writer's chats.

**R-143's scoring limit:** on the 88 recall questions that list at least one wrong value, base 19, 6.37 31.

**Where 6.37's 81 wrong recall answers went wrong** (R-139's stages): no search 23, search missed the fact 38, named
a listed wrong value 6, found the fact but wrong otherwise 14. Read by hand (the chats are frozen and the runs done,
so reading them changes nothing scored), three failures, all specific:
- **A "..., right?" question does not trigger a search.** 23 of 29 `confirm` misses never searched; 6.37 replies with
  small talk and often accepts the user's wrong value ("That's a great story. I'm glad Annika picked marble in the
  end." for quartz). The generator's `confirm` questions are worded "did ... ever come up from me" or "have i ever
  mentioned"; the writers' are tag questions. The search habit is tied to the training wording.
- **Search queries reuse training wording.** Queries such as "aunt keeps animals yard", "brother car auction",
  "great uncle weekend hobby" and "stepmom race finished" carry words from the training templates, not the question,
  and miss the fact.
- **A fact said with a pronoun is not found.** Many missed facts name the person only in an earlier message ("he's
  out in Calgary now", "she has a cockatiel"); a search on "cousin" or "aunt" cannot match them. This is the search
  tool's limit as much as the model's: it matches words in one message.
- R-144's trailing-clause shape appears too ("Your stepmom Linda is not into racquet sports." for "...She does
  curling every Thursday.").

**A correction to R-144.** R-144 found that 6.37's `hard_dev` misses almost never state a false value. On this set
that does not hold: of the 81 misses, 8 say it does not know, 14 name a listed wrong value and 59 state something
else, usually another person's fact from the passage it found ("Your daughter-in-law has anemia." for vertigo).
Base: 1 leaked tool text, 13 named a listed wrong value, 80 state something else. R-144's finding is a property of
the generator's chats, not a general one.

### The prompted-baseline control (R-137)

Base, seed 73157, the same 240 items each (recall right of 96; searched; right decisions of 48 on `in_view`,
`never_told`, `statement`):

| run | probe recall | searched | in_view / never_told / statement | `hard_dev` recall | searched | in_view / never_told / statement |
|---|---|---|---|---|---|---|
| base, default prompt | 30 | 37 | 35 / 16 / 31 | 20 | 58 | 41 / 32 / 36 |
| base, prompt A (rules) | 11 | 14 | 46 / 8 / 39 | 3 | 9 | 46 / 3 / 45 |
| base, prompt B (rules and examples) | 1 | 0 | 48 / 0 / 46 | 0 | 0 | 48 / 0 / 48 |
| 6.37 seed 82 | 96 | 96 | 48 / 48 / 48 | 73 | 95 | 48 / 48 / 48 |

On the independent set: recall base 26, prompt A 19, prompt B 15 of 120. **Both prompts lower base's recall**: they
make base search less, and with prompt B it almost never searches. The right decisions that rise under the prompts
are the ones where not searching is right. So no prompt tried here buys any of 6.37's gain; a better prompt may
exist, and only these two, fixed before any result, were tried.

### The break tests (R-138's rule)

6.37 seed 82 at discovery seed 74001 (recall right of 96 per pool; probe then `hard_dev`): `plain` 95, 84; `d4` 95,
84 (paired against `plain`: no recall lost or gained); `long` 96, 75; `longfixh` 96, 89 (against `long`: 0 lost, 14
gained on `hard_dev`); `askd4` 95, 77 (against `plain`: probe 1 lost 1 gained, `hard_dev` 7 lost 0 gained; against
`d4` the same). Other kinds move by at most 3 either way, with gains beside the losses. Base, recall in the same
conditions: probe 30, 31, 37, 13, 18; `hard_dev` 16, 22, 22, 7, 19; 6.37 is above base everywhere.

**One break: `long` on `hard_dev`**, 84 to 75 of 96, a net loss of 9, at least R-138's 8 (pooled over the two pools
the loss is 8; either reading meets the rule). `long` is not paired with `plain`, so the net rule alone applies. Its
misses: found the fact but wrong otherwise 16 (7 in `plain`), search missed 2, no search 2, named a wrong value 1:
the trailing-clause failure of R-144, more often in longer chats. **Not a break:** `askd4` on `hard_dev` (7 lost, 0
gained: net 7, one short of the rule; pooled with probe, 8 lost and 1 gained, net 7). Recorded as the next weakest
condition. Every other condition is flat.

**Next, as R-138 registered:** `plain` and `long` rerun on 6.37 at confirm seed 75001 (`hard_dev` first, then probe),
queued 05:15. Only if the break meets the same rule there does a targeted fix start, from TRAIN-pool rows, under
R-138's conditions and its clock (rows by Mon 09:00, training before 12:00).

**What the independent set's failures mean for a fix.** R-142 registered that set as report only, so nothing it
found becomes training data or a reason to change the model; a fix chosen from it would also leave no independent
judge. Its three failures go in the write-up as measured limits.

## R-147 · 2026-11-09 · SPRINT · 6.39, registered before it trains

**Kevin, 2026-11-09 ~05:40,** after R-146's report (the `long` break not yet confirmed at 75001, and my
recommendation to keep R-138's rule and ship 6.37): "it wouldn't be a rush...". Training takes about two hours a
seed pair and the freeze is Tue Nov 10, so a try with every gate fits. This departs from R-138, which allowed a fix
only for a confirmed break; the departure is Kevin's and is recorded here before any 6.39 result exists.

**What it targets.** 6.37's commonest `hard_dev` miss: it finds the right line and answers from its first clause,
leaving out the asked detail when that sits later in a long line (R-144: 15 of 23 misses at seed 73157; R-146: 16
of 21 in `long` at 74001, 11 of 15 at 75001). On the independent set it is one failure among four (R-146); the three
others (tag questions, training-worded queries, pronoun facts) are not targeted, because R-142 made that set report
only.

**What was tried before.** R-110 built 100 train-pool rows for this shape and added them as one extra epoch on top of
6.2 (6.21). 6.21 lost `hard_dev` recall (R-113), and R-115's control split the loss between the extra epoch and the
rows; "found, answered without the asked detail" rose from 21 (the epoch alone) to 29 (with the rows). That is
evidence against these rows, with the epoch confounded; trained from scratch inside a full set, they have not been
tried. Kevin ruled after R-116 that no copy trains on top of an earlier one.

**The set** (`scripts/records/build_r147.py`, `data/screens/fix17cs39.jsonl`, sha256 `efef5f96...`): 6.37's 1,094
rows byte for byte and in order, then R-110's 100 rows byte for byte (`two` 40, `runon` 40, `never` 20); nothing
rewritten, nothing from probe, `hard_dev`, the independent set or the held-out pools. 1,194 rows.

**Training.** 6.37's recipe unchanged (`cand fix17cs39 <seed> data/screens/fix17cs39.jsonl --loss-on chat_decision`),
from scratch, seeds 82 and 83.

**Pass, in order; the first FAIL stops it and 6.37 ships:**
1. R-134's lines, unchanged, against 6.37 (`decide_r147.py`, a copy of `decide_r134.py`): R-086 unjudged, R-094 (probe
   and `hard_dev` recall pooled at 82 and 83 not below 6.37's 192 and 163), R-097 (probe `in_view` at least 41 each
   seed), and R-102's stress runs (held-out corrections and phone typing at 82 and 83).
2. R-086's judged sheets at 82 and 83, fresh judges, as for 6.37 (R-128).
3. **The target** (`target_r147.py`): at fresh seed 75002, never used, seeds 82 and 83 pooled, `hard_dev` recall
   over `plain` and `long` above 6.37's on the same items (ties fail), and probe `plain` recall not below 6.37's.
   R-138 asked for a held-out form of the condition: `hard_dev`'s fact templates never enter training, and R-110's rows
   share no four-word run with them, so the target is judged on wordings the fix never saw.
4. If 1 to 3 pass: 94 to 96, as 6.37 went (R-128), before the freeze. A pass there makes 6.39 the shipped model.

**Reported, not gated:** the independent set at 82 and 83 (R-142's report), and the count of found-but-incomplete
misses beside 6.37's.

**No new panel.** The weekly usage stands at 15% against the line of about 15% (R-146's morning), and the design adds
nothing new: R-110's rows were panelled when built, the gates and the target are R-134's and R-138's. **The case
against, written here:** R-115 is direct evidence that these rows push the targeted miss up, not down; four of the
last nine copies failed a gate by one probe question (R-127's base rate: about 28% per copy with no defect), so a
pass needs both the fix to work and a draw that clears the probe line; and a 75002 win on `hard_dev` is a win on the
generator that also made R-110's rows. That is why the target is fixed here and 6.37 ships on any fail.

## R-148 · 2026-11-09 · SPRINT · R-138's confirm runs at 75001

**Why.** R-138 lets a break found at discovery seed 74001 count only if it meets the same rule again at 75001, so
one seed's draw of items cannot start a fix. Run on 6.37 seed 82, 05:15 to 06:11 (recall right of 96 per pool).

**`long`, the one break at 74001: not confirmed.** probe `plain` 96, `long` 96; `hard_dev` `plain` 87, `long` 81. A
loss of 6 on `hard_dev` (6 pooled over both pools), below the rule's 8. By size, `hard_dev` `long` was 36 of 48 at
1,000 exchanges and 45 of 48 at 2,000, so chat length is not what drives it; of its 15 misses, 11 found the fact and
answered without the asked detail, again in the "collected the keys" and "hosted dinner" templates. Other kinds:
`in_view` probe 47 and 46, `hard_dev` 36 and 39; `never_told` and `statement` 48 throughout.

**`d4` and `askd4` on `hard_dev`, run as the next weakest (R-146):** `d4` recall 89 (against `plain`: 2 gained, 0
lost; `never_told` 2 lost). `askd4` recall 81: against `plain` 7 lost and 1 gained, net 6; **against `d4` 8 lost and 0
gained, which meets R-138's rule** (net 8, losses at least twice the gains). At 74001 the same pair was 7 lost and 0
gained, one short. So `askd4` met the rule at one seed of two and is not a confirmed break under R-138's order (find
at 74001, confirm at 75001); over both seeds it is 15 lost and 0 gained against `d4`, a consistent weakness, recorded
as a measured limit. Of the 15, 13 found the fact and answered without the asked detail (`hosted dinner`,
`collected the keys`), and 2 did not search: a question asked and declined earlier makes the same failure more
frequent; it is not a different one.

**Reading.** Every weakness the break tests found is the one failure R-144 named, in the same two templates. 6.39
(R-147) is judged on it at 75002; nothing here changes R-147's lines.

## R-149 · 2026-11-09 · SPRINT · 6.39 fails

**What ran** (R-147, unchanged): `cand fix17cs39` at 82 and 83 (1,194 rows, from scratch, 6.37's recipe; seed 82's
training 2,237 s), scored by 08:07; `decide_r147.py` touched `r147_stop`, so R-147's remaining 6.39 lines skip.

**Lines.** Pass: probe 51203 recall 94 (at least 94) and `statement` 48 (at least 47); `hard_dev` `never_told` 48;
probe 73157 recall pooled 192 (6.37 192); no slips at either seed on either pool; `hard_dev` false retrieval 0; probe
`in_view` 43 and 44 (at least 41). **Fail: `hard_dev` recall pooled 147** (71 and 76) against 6.37's 163 (73 and 90),
and against v6's 157. Two FAIL lines, both this one count. 6.37 stays frozen (R-140).

**The targeted miss went up, not down.** `hard_dev` misses at seed 73157 by stage (R-139), seeds 82 and 83:

| | right | no search | search missed | wrong value | found, answered without the asked detail |
|---|---|---|---|---|---|
| 6.37 | 73, 90 | 1, 1 | 3, 2 | 1, 0 | 18, 3 |
| 6.39 | 71, 76 | 1, 2 | 6, 3 | 0, 0 | 18, 15 |

Seed 83 is where 6.39 loses: the found-but-incomplete miss rises from 3 to 15. This is the third reading of R-110's
rows (R-113 and R-115 on top of 6.2, now from scratch inside 6.37's set), and in each the miss they were built for
rises. Two seeds, so a direction, not a measured size; but the direction has not changed in three tries. These rows
are not used again.

**Next.** R-147 allowed one try; Kevin's rule of 2026-11-08 lets a panel pick a further candidate without asking him,
within the clock (training before 12:00 today, R-138). The panel waits until the weekly usage line catches up (17%
used at 08:10 against a line of about 16%, rule of 2026-11-08: no new agents over the line), about 09:45, which still
leaves time to train before 12:00. 6.37's 75002 runs (R-147 item 3) go on meanwhile as the reference for whatever is
judged there.

## R-150 · 2026-11-09 · SPRINT · The 6.4 panel: no 6.4

**Why a panel.** Kevin's rule of 2026-11-08: after a fail, a panel picks the next candidate without asking him. At
08:20 Kevin exempted this session from the usage line ("you're the exempt one. keep going"), so the panel ran at once
instead of at 09:45. Three separate Opus agents, one lane each, the same brief (`$S/panel_64_brief.md`: the facts of
R-138 to R-149, the hard limits, 12:00 to start training, every 6.37 gate unchanged, then a win at 75002). Transcripts
audited: none opened a sealed file or a file named for a token; the method lane read `pools.py` only to line 451;
the sources lane listed, and did not open, 6.37's first 75002 result; none wrote a file.

**Method lane: one design.** Keep 6.37's 1,094 rows; in the 562 rows whose last turn answers from a search, prefix
the answer with the asked value ("Hugo. Your cousin Dana named the baby Hugo."), the old answer kept byte for byte;
nothing added. Reason: every found-fact target restates the line from its start (about 7.5 words), which works on
TRAIN's one-clause lines and fails when the first clause is another event; a value-first token makes the answer pick
the asked slot. Its own estimate: about 30% to pass every gate, about 50% then to win at 75002, about 15% in all.
Biggest risk: dropping the "Your {relation} {person}" lead may cost who-is-who choices, and probe recall is at its
ceiling.

**Sources lane: no 6.4.** Across the record nothing has lowered the found-but-incomplete miss except a training seed
(3 to 18 a seed at 6.37's recipe, R-141); every change to answer length or shape raised it (R-115, R-121, R-149).
R-110's rows reward picking the matching clause and dropping the rest of the line, which trains the miss itself (a
reading of `build_r110.py`, not a measurement). Value-first answers are untried, but TRAIN's lines cannot show the
long-line case, and building such lines would copy `hard_dev`'s templates.

**Against lane: no 6.4.** The `hard_dev` line's bar, 163, is 73 plus 90, and 90 is the best of 6.37's eight seeds:
of the 28 pairs the eight seeds form, 13 reach 163, so a copy exactly as good as 6.37 clears that line about half the
time; with the probe line (about 72%, R-127) and a 75002 win with ties failing (under half), a copy with no effect
passes all three about 15% of the time. A win at 75002 is also a win on the two templates that prompted the design.
Least-bad design if overruled: the method lane's.

**Decision: no 6.4.** A pass rate of about 15% for the design and about 15% for a copy with no effect means a pass
could not tell a fix from a draw, and a pass would ship. Value-first answers also read less naturally, and no gate
marks how a recall answer reads (R-086's judged sheets mark `statement` and `in_view` replies and the check set).
**The case for trying, recorded:** the card is otherwise idle and 6.37 ships on any fail, so the cost is time. That
did not outweigh shipping on a draw. **6.37 (fix17cs37 seed 82) is the model the sealed final run will score**, on
Kevin's go after the freeze (Tue Nov 10). The found-but-incomplete miss goes in the write-up as a measured limit, with
R-144, R-146, R-148 and R-149 as its evidence.

## R-151 · 2026-11-09 · SPRINT · The freeze moves to Wednesday; a 7, and a second independent set to judge it

**Kevin, 2026-11-09 ~09:00:** "hold up.. it's monday.. we have litearlly 5 more days", then, on moving the model
freeze from Tue Nov 10 to Wed Nov 11 night to build a 7: "yeah lets do it. the freeze was already super early
anyway". The clock of R-134 and R-138 (training before Mon 12:00) existed only for the Tuesday freeze; it is replaced
by: 7's training starts by Tue Nov 10 12:00, its confirmation seeds (94 to 96) finish by Wed Nov 11, then the freeze.
Write-up Nov 12, demo Nov 13, submission by Nov 14, unchanged. The sealed final run is unchanged: once, on the shipped
model, on Kevin's go after the freeze. 6.37 seed 82 stays the shipped model unless 7 passes everything below.

**Why a 7 and not a 6.4.** R-150 found no change to 6.37's set the record supports, and a pass that could not be
told from a draw. A 7 is built from scratch on a new training set, so it can address the failures that cost the most
on chats the generator never made (R-146): a "..., right?" question does not trigger a search; search queries reuse
training wording; a fact told with a pronoun is not found; and the found-but-incomplete answer.

**The first independent set's status changes, disclosed here.** R-142 registered it as report only, so that a gain on
it could be trusted. Designing 7 from its failures uses it, so it can no longer judge 7: from this record it is a
development set. 6.37's R-146 result on it stands, as it was measured before this change. **A second independent set
judges 7:** four new blind Opus writers, given R-142's writer spec unchanged with four new settings (a parent and the
school; planning a big family event; a shared house in a busy neighbourhood; a community group), ten chats each,
written before any 7 design exists (`$S/indep2/`, `fill_briefs.py`). It is loaded, frozen and committed by R-142's
loader before 7's design is registered, and nobody reads a chat until 7's runs on it are done. It is report only for
every model except as named in 7's registration.

**The seed average, measured and dropped.** The idea (Kevin's "6.371", 08:45): average the eight 6.37 seeds' weight
changes into one adapter, no training, to cancel the seed spread. Two lanes (method and against, separate Opus agents,
transcripts audited: no sealed file, no token file, CPU reads of the adapter and base weights only) measured the
eight adapters independently and agree: mean pairwise cosine of the weight changes 0.03 to 0.06 by module type, and the
mean change's norm 0.39 to 0.42 of a single seed's (0.35 if fully orthogonal); over the whole model the mean's energy is 0.166 of a single seed's (0.125 if
unrelated); a layer-0 function proxy gives cosine 0.02 to 0.10. The A matrices stay close to their random start, so
each seed found its own solution in its own subspace. The average is mostly cancellation,
most of the way back toward base, and a pass rule against seed 82 would mostly test "is not seed 82". The method lane would allow one
screening pass with a harder bar (beat both 82 and 83 at 75002); the against lane would not run it. Dropped, to
keep the card and the day for 7; the
cosine measurement goes in the write-up beside the seed spread (R-141).

## R-152 · 2026-11-09 · SPRINT · The second independent set is written and frozen

**Why.** R-151: designing 7 from the first independent set's failures uses that set up, so 7 needs a fresh judge
written by writers who never saw the generator, the project or the first set's results.

**Written.** Four fresh Opus agents, in parallel, each given R-142's writer spec unchanged with its own setting
(`data/blind_dev2/brief.md` lists the four), ten conversations each: `data/blind_dev2/chats/x1_01.json` to
`x4_10.json`. **Writer audit** (every tool call): each read only its own brief and wrote only its own ten files, each
file twice (a rewrite of its own text); none ran a command or searched. Writer 1 noted that its answers keep the
user's lower case; the scorer compares case-blind.

**Frozen here:** sha256 over every file's name and bytes in name order (`dev_set.load_dev_set`)
`3a91c34b2183ec8e3a74a5481540e6873307488b4f89d742f8ec91bd5c3dfe65`, checked in the writers' folder and again in the
repo. Loader (R-142's rules): 240 kept, 0 dropped: `older` 80, `confirm` 40, `in_view` 40, `never_told` 40,
`statement` 40, 60 a writer. **R-143's scoring limit again:** 55 of the 160 answer-bearing questions list no wrong
value (`confirm` 26, `in_view` 19, `older` 10). Counts only were printed: no one has read a chat.

**Use.** It judges 7 as R-151 and 7's registration set out; for every other model it is report only. No design
choice for 7 reads it, and the panel lanes designing 7 were told never to open it.

## R-153 · 2026-11-09 · SPRINT · 7, registered before it trains

**The panel** (R-151's plan; three separate Opus agents, one lane each, brief `$S/panel_70_brief.md`; transcripts
audited: none opened the second set, a 75002 result or a token file; `pools.py` read only to line 451, except one
line printed past it by the against lane's grep for "TRAIN", line 802, which names the three pools and holds no
content, disclosed by the lane itself; two greps ran over the source folder with the sealed file's lines filtered
out of their output). What each found, measured on the first independent set (a development set since R-151) by
replaying the real search in memory:
- **Tag questions (failure 1):** all three lanes support it. Every TRAIN `confirm` wording is "did i ..." or "have i
  ..."; on the first set all 40 `confirm` questions are tags, and seed 82 searched 9 of them. When it searches, it
  finds the fact 78 times in 79, and a search in the question's own words finds all 40: a trigger failure only.
- **Queries from the question's words (failure 2):** ruled out. A question-words query finds 42 to 43 of the 80
  `older` facts; 6.37's own queries find 38 to 43. No room to gain, and fix 7 (R-050) and 7b (R-054), which taught it,
  cost `never_told` and `statement`.
- **Pronoun facts (failure 3):** the method lane found the current tool can already read the next exchange (a bare
  number query returns that exchange: 79 of 80 on the first set, 100 of 100 on TRAIN chats, checked by the against
  lane), and proposed a two-search hop. The against lane's case, taken: it would be the first two-search habit since
  fix 4 (R-032: recall 74 to 62); the model sees `doc_id=exchange_0009` and must turn it into "10"; a hop on
  `never_told` repeats fix 7's false retrievals (R-050); no gate can show a gain and every gate can show a loss; and
  stacked on the tag change, a fail could not be blamed on either. **Left out of 7; a candidate 7.1 of its own.**
- **Found but incomplete (failure 4):** nothing in the record has lowered it except a seed draw; R-110's rows raised
  it three times. Left out.

**7's set** (`scripts/records/build_r153.py`, `data/screens/fix17cs7.jsonl`, sha256 `7cb7a5cb...`, the same on two
builds): 6.37's 1,094 rows in order; 140 rows changed in one user message only, everything else byte for byte.
`confirm` 100 of 230: the question becomes the row's own scripted answer restated as the user's claim with a tag
("my neighbour Marc only orders a cortado yeah?"); 63 name the true value, 37 a value another person in the search
result holds or a value the chat never mentions (a row whose result holds no other value names the true one); the
search, its result and the answer stand, and the answer already states the true value. `never_told` 20 (of those
written with a `confirm` wording; 9 skipped, no single template matched): a claim about the asked relation, then the
same search and decline. `in_view` 20: a claim of the visible fact's true value, no search, the answer unchanged, so a
tag question about a fact in view needs no search. Tags: ", right?", " right?", " right", ", isn't that right?",
" yeah?", ", yeah", " correct?". Checks: no claim shares a four-word run with the probe or `hard_dev` pools; no answer
names the wrong value a claim states; every row at most 1,024 tokens. Nothing comes from probe, `hard_dev`, either
independent set or the held-out pools.

**Training.** 6.37's recipe unchanged, from scratch, at **five seeds: 82, 83, 94, 95, 96**, so 7 is compared with
6.37 at the same five seeds and not against 6.37's best pair. The panel's against lane showed why: R-094's
`hard_dev` bar, 163, is 73 plus 90, and 90 is 6.37's best of eight seeds; a copy as good as 6.37 clears it with about
13 of 28 seed pairs.

**Pass, in order; the first FAIL stops 7 and 6.37 seed 82 ships:**
1. R-086's unjudged lines and R-094's slips as registered at 82 and 83 (`gate_r086.py`, `stone_report.py`, unchanged).
   **R-094's pooled recall lines are replaced, for 7 only, by the same lines over five seeds:** probe and `hard_dev`
   recall at 73157 over 82, 83, 94, 95, 96 not below 6.37's at the same seeds (probe 479, `hard_dev` 410; checked against the result files). Probe
   `in_view` at least 41 at each of the five seeds (R-097). `decide_r153.py`.
2. R-102's stress runs (held-out corrections and phone typing) at 82 and 83 against 6.37's, as registered.
3. R-086's judged sheets at 82 and 83, three fresh Sonnet judges, judge 1 deciding, as for 6.37 (R-128).
4. **The target** (`target_r153.py`): on the second independent set (R-152), recall over the five seeds pooled above
   6.37's at the same five seeds (ties fail). Reported beside it, as readings: `confirm` right and searched, and
   searches on `in_view` questions (a tag habit that spreads to facts in view shows there).
5. On a pass, 7 seed 82 is the shipped model (the seed fixed now, before any result). 94 to 96 are already inside
   items 1 and 4, so no further confirmation runs.

**Reported, not gated:** the first independent set at the five seeds; `hard_dev` failure stages; `statement` and
`never_told` searches.

**The case against, recorded:** the tag change targets about 20 discriminating `confirm` questions per set (the other
20 name the true value and pass by agreeing), worth about +10 a seed if every one is searched and read as well as
6.37 reads them; diluting the "did i" wordings every generator `confirm` uses may cost probe recall at its ceiling;
a tag that names a look-alike's value invites a who-is-who slip. **Order on the GPU:** the second set's reference
runs (base, 6.37 at all eight seeds, queued 10:00) first, then 7. Their results are not read before 7's target is
computed.

## R-154 · 2026-11-09 · SPRINT · The scorer and the judge are frozen with the model

**Request.** Advice Kevin passed on (pasted, about 10:20): "freeze the scorer with the model, including the judge
model and version if it's LLM-based. A sealed run scored by a different judge isn't sealed." Then four points: pin
the judge (model and version, prompt, decoding, system message); hash the scorer and the sealed set beside the model
fingerprint; score one fixed sample twice before sealing; archive the human check so it can be rebuilt. Kevin: "Yes,
register it".

**What was not pinned.** The recall scorer is plain code and every results file records its commit, but nothing
named the files the sealed run must use. The coherence gate, a hard part of the sealed pass rule (R-016, R-038), is
marked by Claude judges, and every record says only "a fresh Sonnet judge": no version, and the judges' brief lived
only in the prompt, not in the repo. The transcripts show what ran: the 135 agent transcripts since Nov 1 that read a
rubric and are judges all replied as `claude-sonnet-5-5` (the 8 others that read one were Opus panel lanes); R-128's
three judges ran under Claude Code 2.1.309.

**The freeze** (`scripts/records/freeze_r154.py`):

1. `write` records SHA-256 digests of the 17 files that build the items, run the model and score it (the item
   builder, search tool, loop, decoding, tool prompt, model pin, stress forms, scorer, coherence sheets and rubric,
   statistics, the eval and sheet scripts, the CuratorKIT check, `gate_r086.py`, `stone_report.py`); the sealed pools
   (`pools.py` and `pool_independent.py` whole, and `docs/independent_pool/` as one digest over its 3 files, hashed by
   the script and never shown); the judge's brief (R-128 judge 1's, copied verbatim from its transcript to
   `results/freeze/R-154/judge_brief_r128_j1.txt`) and rubric (R-128's, identical to `coherence.RUBRIC` and to
   R-109's); the human check folder; CuratorKIT `dd9e835` with threshold 0.7; the base model and revision, greedy
   decoding, and the adapter's weights and config. The adapter folder's tokenizer files are left out (no file whose
   name contains "token" is opened); they are not the trained weights.
2. `check` runs before the sealed run; any difference stops it. Known-bad test: pointed at seed 83's adapter it failed
   on the adapter name and both weight digests; on seed 82 it passed.
3. `judges` reads every judge transcript of the sealed run; a judging whose replies came from any model but
   `claude-sonnet-5-5` is void. Known-bad test: an Opus panel transcript fails. The agent tool takes only the family
   name ("sonnet"), so if that name points to a newer model by the sealed run, the judging runs through the API pinned
   to `claude-sonnet-5-5` or waits for Kevin's call; it is never run on another model. The judge's brief may change
   only in its folder path, sheet names and line counts. The Claude Code version (it supplies part of the judge's
   system message, and it updates itself) is recorded and any change reported in the write-up.
4. Decoding: Tiny Aya is greedy (`do_sample` False, 60 new tokens). The judge's temperature cannot be set through the
   agent tool, so its spread is measured instead (below), and the rule stays R-128's: three fresh judges, each in its
   own folder, judge 1 decides, judges 2 and 3 reported.

**Scored twice.**

- **Recall scorer:** five stored 6.37 runs (probe 73157 at 82 and 83, `hard_dev` 73157 at 82 and 83, probe 51203 at
  82), 1,200 rows. The items were rebuilt on the CPU and the stored replies scored twice: the same verdicts both
  times, identical to the stored verdicts on every row.
- **Generation:** no record shows a repeated GPU run giving the same replies (R-137's "base's runs are deterministic"
  is stated, not measured). One repeat of 6.37 seed 82's probe 73157 run is queued after 7's seed 83 training
  (`rep_probe_fix17cs37_82`), to be compared reply by reply with the stored run. Pending.
- **Judge:** R-128's three fresh judges (same model, brief, rubric and sheets) are three scorings of the same 576
  replies. They split on 13 (2.3%): pairs agree on 186 to 190 of 192 lines on Sheets B and h, and 95 to 96 of 96 on
  the check sets; counts of 1s differ by at most 4 on a sheet (`results/freeze/R-154/judge_spread_r128.json`). That
  is the judge's measured spread, recorded before the sealed run.

**Human check archive.** `results/human_check/R-139/` holds the 50 replies with their questions and right and wrong
values (`sheet.json`), each reply's model and scorer verdict (`key.json`), Kevin's marks, the second marker's sheet
and marks, and the agreement. Rerunning `scripts/records/score_human_check_r139.py` from the archive rewrote
`agreement.json` byte for byte. The folder is in the manifest.

**Now and at the freeze.** `results/freeze/R-154/manifest_fix17cs37_82.json` is a dry run on 6.37 seed 82 (commit
`f3aee06`). At the freeze (Wed Nov 11) `write` runs once on the shipped model (6.37 seed 82, or 7 seed 82 on a full
pass) to `results/freeze/sealed_manifest.json`, committed and pushed; after that nothing it lists changes. The sealed
run starts with `check` on it and ends with `judges` on every judge transcript; both outputs go in its record.

## R-155 · 2026-11-09 · SPRINT · 7 fails at 82 and 83; 6.37 stays the shipped model

**Result** (`scripts/records/gate_r086.py`, `stone_report.py` and R-153's lines through `decide_r153.py`, run at
11:01 as soon as seed 83 was scored). Two lines fail, so `r153_stop` is touched:

- probe 51203 recall at seed 82: **92** (at least 94; 6.37 94);
- probe 73157 recall pooled at 82 and 83: **189** (not below v6's 192, R-094; 6.37 192).

Every other line passes: probe 51203 `statement` 48; `hard_dev` `never_told` at 82 48; `hard_dev` recall pooled 166
(at least 145); probe recall pooled 189 (at least 189); false retrieval at 82 1; slips 0 at both seeds on both sets;
probe `in_view` 46 and 44 (at least 41).

| Line (seeds 82, 83) | 6.37 | 7 |
|---|---|---|
| probe recall | 96, 96 | 94, 95 |
| probe 51203 recall (82) | 94 | 92 |
| probe `in_view` | 44, 44 | 46, 44 |
| `hard_dev` recall | 73, 90 | 81, 85 |
| `hard_dev` `in_view` | 42, 40 | 40, 37 |
| `statement`, `never_told` (probe and `hard_dev`) | 47 to 48 | 48 |

**The misses.** Six of 7's seven missed probe questions (four at 51203, two at 73157 seed 82) are one probe
template's indirect wording, "drawing a blank on my {relation}'s tattoo": no search, and a reply about tattoo design
("That can be frustrating. Maybe you can try a different design or color."). 6.37 misses that wording once in the
same runs (51203, seed 82). The seventh (seed 83, "what freaks my stepsister out the most") is a search call with a
missing brace, which does not parse. The TRAIN pool (`pools.py` lines 1 to 451) never uses "drawing a blank", so the
wording is one of the probe's unseen indirect forms. 7 changed only `confirm`, `never_told` and `in_view` rows, none
of them `older`; which part of the change moved the `older` decision is not shown (no ablation was run). R-153 named
the risk of a cost to probe recall at its ceiling; it fell on `older`, not on the reworded `confirm`.

**Decision.** R-153's rule as registered: 7 fails, **6.37 (fix17cs37 seed 82) stays the shipped model**. R-086's
judged sheets for 7 are not run. Every guarded line skips: 7's stress runs, seeds 94 to 96, its runs on both
independent sets, and `target_r153.py`. The second set's reference runs (base, 6.37 at all eight seeds) still run,
as a second independent report on the shipped model, report only. `hard_dev` recall pooled 166 against 163 is inside
6.37's seed spread (73 to 90 a seed) and is not a finding.

**Disclosure.** While counting the wording, a grep over the whole of `pools.py` printed line 646, past line 451: the
probe template line holding "drawing a blank on my {relation}'s tattoo", the wording every probe results file already
shows. Nothing else past line 451 was shown, and nothing from the held-out pool. The count was then run on lines 1 to
451 only.

## R-156 · 2026-11-09 · SPRINT · 7.1 registered: 7 without its `in_view` tag rows; R-155 corrected

**The panel** (three Opus lanes reading `$S/panel_71_brief.md`, transcripts audited: none opened a sealed file, the
second independent set or a `blind2` or 75002 result; the one search of `pools.py` was `head -n 451 ... | grep`, which
found nothing; none wrote a file).

- **Diagnosis.** Every search 7 lost against 6.37, on probe, screen and `hard_dev` at 82 and 83, is on one probe
  wording, "drawing a blank on my {relation}'s tattoo", counting `never_told` items too (they score right when the
  model declines without a search, so R-155's count hid half of it): no search on **10 of 14** such items against
  6.37's **1 of 14**. Every other wording shape is searched as before (0 no-search of 92 other `older` and
  `never_told` items a probe run), `confirm` is searched 48 of 48 in every run by both, and `hard_dev` `older`
  searches are unchanged. Across 34 earlier probe runs of the 6.3x family the wording was searched 129 of 136 times;
  7's two seeds (0 and 2 of 4) have a chance of about 0.4% at that rate, so the cost is real. Neither training set
  contains "blank", "drawing" or "tattoo". Of the 140 rewordings only the 20 `in_view` claims teach "a statement-like
  message about a person's fact, no search", and 7 of them kept chit-chat answers written for the old forget-wordings
  ("It sounds like you're trying to remember something..."), the register of 7's misses. The lane's weights:
  `in_view` 50%, `confirm` 35%, `never_told` 15%; no ablation separates them.
- **Design** recommends 7.1 = 7 without the 20 `in_view` tag rows, as a one-factor removal whose result also shows
  which part of 7 moved the `older` decision.
- **Against** recommends no 7.1: R-153's five-seed lines are so strict that 6.37 fails them at its own seeds (probe
  `in_view` 39 at seed 95 and at 97; at least 41 is needed at each of five); a design chosen after reading 7's probe
  misses makes the probe development evidence for it; a fourth registered fail adds little. If overruled, the least
  bad design is the same removal, with one added line: `confirm` right and searched on the second set above 6.37's.

**Decision: 7.1 runs**, with the against lane's added line and its disclosure. Two lanes for and the third naming the
same design as the only one worth running; the card is otherwise idle after the second set's reference runs; a full
pass cannot be a draw (below); a fail at 82 and 83 costs about 3 GPU hours and still answers R-155's open question.

**7.1 = `fix17cs71`** (`scripts/records/build_r156.py`): 7's set with the 20 rows where 7 changed an `in_view`
question put back as 6.37 had them, byte for byte. 1,094 rows, each 6.37's or 7's; 120 differ from 6.37 (100
`confirm`, 20 `never_told`, identical to 7's). Nothing is added, so 7's checks (no four-word run shared with the probe
or `hard_dev` pools, at most 1,024 tokens, no answer naming a wrong claimed value) hold row for row. Deterministic:
two builds gave SHA-256 `f7dbcb9881758067...`. Trained from scratch with 6.37's recipe at 82, 83, 94, 95, 96.

**Pass rule, fixed before training.** R-153's lines as registered (item 1 through `$S/decide_r156.py`; R-102's
stress runs and R-086's judged sheets at 82 and 83; the target), plus:

- the target (`$S/target_r156.py`) also needs `confirm` right and searched, pooled over the five seeds on the second
  independent set, above 6.37's (ties fail), so a recall win is credited to tag questions only if they did it;
- any FAIL ends it and 6.37 seed 82 ships; on a full pass 7.1 seed 82 ships.

**Diagnostic reading, registered.** "Drawing a blank" not searched on 3 or more of the 14 items (probe 73157 at 82 and
83, probe 51203 at 82) means the cost is in the `confirm` or `never_told` rows; then no tag design is tried before
the freeze.

**Chance a copy with no effect passes in full**, by lane: about 1% to 2% (against; 200,000 five-seed resamples of
6.37's eight seeds), about 4% (design; 35 probe files of the 6.3x family), about 15% (diagnosis; it leaves out the
five-seed `in_view` line). All three put a full pass below or near R-150's 15% for a draw, and the design lane puts
a copy with a real tag gain at only about 8%: R-153's item 1 mostly measures seed draws at the ceiling, which goes in
the write-up's limits.

**Disclosure.** 7.1 was chosen after reading 7's probe misses, so for 7.1 the probe lines are development evidence;
the second independent set, frozen and unread (R-152), is the test that was not used to design it.

**Correction to R-155.** R-153 item 1 replaced, for 7, R-094's pooled recall lines against v6 at 82 and 83 by the
five-seed lines, but `decide_r153.py` still printed `stone_report.py`'s "probe recall pooled 189 not below v6's 192",
and R-155 counted it as one of 7's two fails. It was not one of 7's lines. The verdict stands: probe 51203 at 92 fails
on its own (at least 94), and the five-seed probe line cannot be met (189 at 82 and 83 plus at most 288 at 94 to 96 is
477, below 6.37's 479). `decide_r156.py` drops the replaced lines; run on 7 it prints one fail, 51203.

**R-154 follow-up: generation repeats.** The repeat of 6.37 seed 82's probe 73157 run (`rep_probe_fix17cs37_82`)
matched the stored run on all 240 rows: the same reply, queries, first reply and verdict on every one. With R-154's
rescoring (1,200 rows) and the judges' measured spread, every scorer the sealed run uses has now been run twice.

**Order on the GPU.** The second set's reference runs (base, 6.37 at eight seeds) first, as R-155 left them; then 7.1
at 82 and 83, `decide_r156.py`, and every later line guarded by `r156_stop`.

## R-157 · 2026-11-09 · SPRINT · 7.1 fails; 6.37 ships; the second independent set read; the records made complete

**Result** (`decide_r156.py`, run by the queue at 14:17 as soon as seed 83 was scored). One line fails, so
`r156_stop` is touched: **probe `in_view` at seed 83: 38** (at least 41, R-097). Every other line passes: probe
51203 recall 94 (at least 94), probe 51203 `statement` 48, `hard_dev` `never_told` at 82 47, `hard_dev` recall pooled
157 (at least 145), probe recall pooled 189 (at least 189), false retrieval at 82 3, slips 0 on both sets at both
seeds. The five-seed lines were not reached.

| Line (seeds 82, 83) | 6.37 | 7 | 7.1 |
|---|---|---|---|
| probe recall | 96, 96 | 94, 95 | 94, 95 |
| probe 51203 recall (82) | 94 | 92 | 94 |
| probe `in_view` | 44, 44 | 46, 44 | 44, **38** |
| `hard_dev` recall | 73, 90 | 81, 85 | 83, 74 |
| `hard_dev` `in_view` | 42, 40 | 40, 37 | 39, 37 |

**The registered diagnostic** (R-156). "Drawing a blank on my {relation}'s tattoo", `older` and `never_told` items on
probe 73157 at 82 and 83 and probe 51203 at 82: not searched on **6 of 14** (7: 10; 6.37: 1). That is 3 or more, so
by R-156's reading the cost is in the `confirm` or `never_told` tag rows, and no tag design is tried before the
freeze. Removing the 20 `in_view` rows took back 4 of 7's 9 extra no-search items, so they carried part of it, not
all.

**7.1's `in_view` misses at seed 83** (10 of 48): every one is an in-view forget-wording ("drawing a blank on my
daughter's tattoo", "i forget which language my barber knows") answered with chat and no use of the fact in view
("It sounds like you're feeling a bit down about it..."). 6.37 at its own seeds 95 and 97 scored 39 on this line
(R-156), so the line sits at the edge of its seed spread; R-156 recorded that the gate is this strict.

**Decision.** R-156's rule as registered: 7.1 fails, **6.37 (fix17cs37 seed 82) is the shipped model**, and no
candidate is left before the freeze (R-156's reading). Every guarded line skipped: 7.1's stress runs, seeds 94 to 96,
its runs on both independent sets and `target_r156.py`. R-086's judged sheets are not run.

**The second independent set, read as a report** (`scripts/records/blind2_r157.py`, R-146's measures unchanged;
`results/analysis/R-157/blind2.json`). R-155 and R-156 kept these runs unread until no 7.x target was left; 7.1's
fail leaves none. Every run was scored on the frozen set (sha256 `3a91c34b...`, R-152), 240 questions on 40 chats,
none dropped.

- **Recall (`older` and `confirm`), 6.37 seed 82 against base: 53 of 120 against 27 of 120**, +96%. Base alone right
  9, 6.37 alone right 35, exact sign test p = 0.0001. Resampling whole chats: difference +21.7 points (95% interval
  +13.3 to +30.0); relative gain +96% (+49% to +175%).
- The eight training seeds: 44 to 56 of 120 (82 and 83: 53). By writer, 6.37 is above base for all four (10 to 15
  of 30 against 4 to 9).
- By kind (6.37 seed 82 against base, right answers): `older` 34 of 80 against 12, `confirm` 19 of 40 against 15,
  `in_view` 37 of 40 against 34, `never_told` 36 of 40 against 32, `statement` (scored on the search alone) 35 of 40
  against 39: 6.37 searches on 5 statements where base searched on 1, the one kind where it is below base here.
  Right decisions: `confirm` searched 12 of 40 against 2 (R-146's tag-question gap, again), `older` 78 of 80
  against 40, `never_told` 40 of 40 against 20.
- 6.37's 67 wrong recall answers: 17 never searched, 36 searched and missed the fact, 5 named a wrong value, 9 found
  the fact and answered wrong. On the first set the leading stage was also a search that missed the fact (38 of 81).

Two independent sets, one generator-blind writer team each: recall +50% on the first (R-146) and +96% on the
second. Both are well below the generated pools' gains, and both are the numbers to read as generalization.

**The records made complete.** Kevin asked whether RECORDS.md holds everything. It did not: several records cite
files that lived only in scratch, outside the repository. Now copied in as run (content unchanged; git stores some with LF line endings where the
scratch copies had CRLF):

- `scripts/records/queue/`: the gate scripts the records name (`decide_r122.py`, `decide_r134.py`, `decide_r147.py`,
  `decide_r153.py`, `decide_r156.py`, `target_r147.py`, `target_r153.py`, `target_r156.py`), the queue runner
  (`runner2.sh`, `blind.sh`, `blind2.sh`) and the backlog as it stands after this run (`backlog.txt`, 491 lines).
  Where a record cites `$S/<file>`, the file is here. They are kept unformatted, as records (excluded from ruff).
- `results/panels/<record>/`: the panel briefs and round messages for R-088, R-094, R-097, R-099, R-100, R-102,
  R-138, R-150, R-151, R-153 and R-156, and the reviewed writer spec for R-142 (R-134's panel was already archived).

Still outside the repository: each panel lane's full answer, and each judge's and writer's transcript, which are
in Claude Code's agent transcripts on this machine. The records summarise every one; exporting them into the repo
waits for Kevin's word.

**Disclosure.** While checking the README (60d7c07), a grep over `src/aya_retrieval/*.py` printed line 817 of
`pools.py`, past line 451: `POOLS["wide"] = WIDE`, an assignment, no pool content. From now on `pools.py` is left
out of every grep that spans more than one file.

**README.** Status, the limits and the layout updated in this commit (the rule since 60d7c07: a record that changes
what ships updates the README in the same commit).

## R-158 · 2026-11-09 · SPRINT · 7.1 on the second independent set, report only, registered before it runs

**Why.** Kevin asked whether R-157 discards an improvement because the test got stricter. On every line
that was measured, 7.1 is at or below 6.37 (R-157's table; `hard_dev` recall pooled 157 against 163, the tattoo
wording unsearched 6 of 14 against 1), so no improvement was shown. But the gain 7 and 7.1 were built for, tag
questions ("..., right?") on chats the generator did not write, was never measured: the stop file skipped those
runs. The card is idle, and the runs take about 15 minutes.

**What runs.** `blind2_fix17cs71_82` and `blind2_fix17cs71_83`, as `blind2.sh` defines them, on the frozen second
set (sha256 `3a91c34b...`). 7.1 was designed before any second-set result was read (R-156), so the set is still
unseen by its design.

**What is reported**, each 7.1 seed against 6.37 at the same seed: recall (`older` and `confirm`, 120); `confirm`
right; `confirm` right and searched (R-156's added line); `confirm` searched; `statement` right.

**What it cannot do.** It does not change the shipped model: R-156's rule ended 7.1 on its registered fail, and that
rule stands. Two seeds are a report, not a test (R-156 asked for five). If 7.1 is above 6.37 here, the write-up says
so, as a tag-question gain that came with costs on the generated pools.

**Result** (runs finished 14:43; both on the frozen set, nothing dropped). Each seed, 7.1 against 6.37:

| Second set, seed | 6.37 82 | 7.1 82 | 6.37 83 | 7.1 83 |
|---|---|---|---|---|
| recall (`older` and `confirm`, of 120) | 53 | 51 | 53 | 52 |
| `older` right (of 80) | 34 | 33 | 36 | 34 |
| `confirm` right (of 40) | 19 | 18 | 17 | 18 |
| `confirm` right and searched | 6 | 18 | 4 | 18 |
| `confirm` searched | 12 | 40 | 7 | 39 |
| `statement` right (of 40) | 35 | 35 | 31 | 33 |

Half the 40 `confirm` questions claim the right value and half a wrong one. 6.37 gets its `confirm` score mostly by
agreeing: right on 16 and 16 of the 20 true claims, and it corrects only 3 and 1 of the 20 false ones, so it goes
along with a wrong claimed value 17 and 19 times in 20. Base is the same (15 right, 2 searched). 7.1 corrects 7 and 5
false claims and confirms 11 and 13 true ones; every one of its right answers came from a search.

**Reading.** 7.1 did what 7 was built for on chats the generator never made: it searches tag questions and grounds
its answers, and R-156's added target line (`confirm` right and searched above 6.37) would pass by a wide margin at
both seeds. It does not raise recall: the searches it now makes miss the fact or lose true claims about as often
as they catch false ones. Two seeds; a report, not a test. 6.37 ships under R-156's rule. For the write-up, 6.37
goes along with a wrong claimed value on most false `confirm` questions on the second independent set (the first
set was not counted this way), and this is named as a limit; 7.1 shows the behaviour can be trained, at a cost on the generated pools (R-157).

## R-159 · 2026-11-09 · SPRINT · The freeze panel; the prompted-baseline control on the second set

**Why.** Kevin, after R-158: freeze 6.37 "if the panel agrees knowing that i'm reluctant". Three Opus lanes read
`results/panels/R-159/panel_freeze_brief.md` (his reluctance stated in it as a reason to make the case for continuing
as strong as the facts allow). Audit of every tool call: none wrote a file or opened a sealed file, the second set's
chats or a file named for a token. One search listed file names matching a helper's name over `scripts` and `src`,
`pools.py` included, and filtered `pools.py` out of the printed list: no line of `pools.py` was shown.

- **Freeze** (for). 6.37 is the only copy since v6 that passed every registered line, and no measured candidate is
  above it on either independent set (7.1: 51 and 52 against 53 and 53, inside 6.37's seed spread of 44 to 56). Most
  `older` misses on the second set are a search that missed the fact (35 of 80 at seed 82), the frozen tool's limit;
  7.1's `confirm` searches missed the fact 20 and 15 times in 40, so it hit the same ceiling. A new candidate that
  both passes and helps: low single digits. Seed 82 stays: it was fixed before either set was read. Optional, report
  only: 7.1 at seeds 94 to 96 on the second set.
- **Against** (hostile judge). Shipping 7.1 has the most holes (a registered fail, a choice made after reading the
  second set). Another candidate breaks R-156's registered reading, needs a third set, and over about 19 tries a pass
  cannot be told from a draw. Freezing has the fewest: the second set was written after 6.37 was fixed and read by
  no decision about it. New count (checked): on the first set 6.37 seed 82 corrects 1 of 20 false tag claims (base 1)
  and its `confirm` score is 11 against base's 15; its gain there is all `older` (28 against 11). Disclose a candidate
  ledger, `older` and `confirm` split, the agreement with wrong claims on both sets. It names a gap: the
  prompted-baseline control (R-137) ran only on the first set.
- **Continue** (against freezing, at Kevin's reluctance). The cause of 7.1's tag-question misses is in the rows:
  `build_r153.py` reworded the 100 `confirm` messages but kept 6.37's queries (checked: 100 of 100 unchanged; 7 share
  no word with the new message), so the model searches with keywords for the fact type, not the claim. 7.2 would
  replace those 100 queries with the claim's own words (`demonstrations.message_words_query`, R-042) and their tool
  results with what the real search returns, keeping the answers. It needs a third independent set, written now, and
  a new pass rule fixed before training that replaces R-153's five-seed probe recall and `in_view` lines by margins
  below 6.37 set from its eight-seed spread, with a target of at least 16 above 6.37's five-seed recall on the third
  set. Its odds: a copy with no effect passes about 3% to 5%; the design about 20%. It names the cost: the "drawing a
  blank" loss stays, and the looser probe lines accept it. Only on Kevin's override of R-156's reading.

**Where it stands.** Two lanes for freezing, one for a 7.2 that needs Kevin to override a registered reading and
accept a rewritten rule. Overriding a registered rule is Kevin's decision, so nothing is frozen and nothing is built
until he answers. My recommendation to him: freeze.

**The prompted-baseline control on the second set, registered before it runs** (report only). R-137's two prompts
(`results/control/R-137/prompt_a.txt`, `prompt_b.txt`) on base, the second set, as run on the first: runs
`blind2_base_prompta` and `blind2_base_promptb`. Reported: recall (`older` and `confirm`) and each kind, against
base and 6.37 seed 82 on the same set. It changes nothing that ships.

## R-160 · 2026-11-09 · SPRINT · The model is frozen: 6.37 seed 82

**Decision.** Kevin, after R-159's panel (two lanes for freezing, one for a 7.2 only on his override of R-156's
reading): "Freeze 6.37". No 7.2 is built; R-156's reading stands. The freeze moves from Wednesday night (R-151) to
Monday 14:52.

**The sealed manifest** (`scripts/records/freeze_r154.py write`, the shipped adapter
`adapters/screens/fix17cs37_82`, at commit `2b04826` on a clean tree): `results/freeze/sealed_manifest.json`.
`check` on it against the adapter: "every frozen file and value matches". Compared with R-154's trial manifest
(`results/freeze/R-154/manifest_fix17cs37_82.json`, commit `f3aee06`), every entry is identical: the 17 scorer files,
the sealed pools (three digests, never printed), the judge pin (`claude-sonnet-5-5`, Claude Code 2.1.309, the R-128
brief and rubric), CuratorKIT's commit and threshold, the human check and the adapter's two weight files. Nothing
that builds, runs or scores the evaluation changed between the two.


**Line endings, fixed the same hour.** `digest` hashed each file's bytes as they sit on this Windows working copy,
where 8 frozen text files have CRLF line endings and git stores LF; a judge's clone would get other hashes and
`check` would fail on files that had not changed. `digest` now hashes text files with LF line endings (the
`.safetensors` weights unchanged), the manifest was written again (`check`: every frozen file and value matches),
and each of its 19 scorer and judge file hashes equals the SHA-256 of the file as committed (`git show HEAD:path`).
The only entries that changed were the CRLF files; the contents are the ones hashed at 14:52. R-154's trial
manifest is kept as written, under the old rule.
**From here.** The sealed final run on the held-out pools runs once, on Kevin's go, and starts with `check` on this
manifest; its judged sheets end with `judges` on every judge transcript (R-154). The report-only runs already
registered (R-159's prompted-baseline control on the second set) change nothing that ships. The write-up and model
card are rebuilt for 6.37, leading with the independent sets (R-157 limits, R-159's split of recall into `older` and
`confirm` and the candidate ledger).

## R-161 · 2026-11-09 · SPRINT · The prompted-baseline control on the second set

**Result** (R-159's registration; `blind2_base_prompta` and `blind2_base_promptb`, both on the frozen second set,
nothing dropped; finished 15:01). Recall (`older` and `confirm`, of 120), with the first set beside it (R-146):

| Run | First set | Second set |
|---|---|---|
| base | 26 | 27 |
| base, prompt A (rules) | 19 | 18 |
| base, prompt B (rules and four worked examples) | 15 | 20 |
| 6.37 seed 82 | 39 | 53 |

- On the second set the prompts make base search less, not more: `older` searched 7 and 4 of 80 against base's 40,
  and `older` right 2 and 3 against 12. `confirm` right moves little (16 and 17 against 15); `never_told` (37 and 35 against 32) and
  `statement` (40 and 40 against 39) rise a little, the kinds where not searching is right.
- 6.37 seed 82 against each prompt, recall: prompt A alone right on 4, 6.37 alone on 39 (exact sign test
  p = 3.1e-8); prompt B alone 5, 6.37 alone 38 (p = 2.5e-7). On the first set: 8 against 28 (p = 0.0012) and 8
  against 32 (p = 0.00018).

**Reading.** On both independent sets a written prompt alone does not buy the gain; both prompts lower base's recall.
The adapter's gain is not a prompting effect that a better system prompt would match, at least for these two prompts
(the limit: two fixed prompts, not a search over prompts). Report only; the frozen model is unchanged (R-160).

## R-162 · 2026-11-09 · SPRINT · The sealed final run, registered before it runs

**Kevin's go**, 2026-11-09 after R-161: "Start sealed run". Asked which 6.37 adapters enter it (R-141: "R-016's and
Kevin's call"), with the three seeds R-016 names (82, 83, 94) recommended: **"All eight seeds"**.

**Change from R-016, disclosed.** R-016 registered three adapters on three training seeds, the recall rule pooled
over the three. The sealed run uses all eight seeds trained on 6.37's set (82, 83, 94, 95, 96, 97, 98, 99), so no
seed is chosen after a development result: every 6.37 adapter that exists enters. Rules written "each adapter" now
apply to eight, so they have eight chances to fail; the pooled recall rule pools eight. Seed 82, the shipped model
(R-160), is also reported alone, as a description, not a rule.

**What runs** (`scripts/records/queue/final.sh`, sourced by the queue; nothing has been built or run on a sealed
pool before this record, beyond what R-038 lists as seen). First `freeze_r154.py check` on
`results/freeze/sealed_manifest.json`; a fail touches `r162_stop` and nothing runs. Then, each once, in this order:

| Condition | Pool | Decoys a chat |
|---|---|---|
| A (R-016) | `heldout` | 1 |
| B (R-038) | `heldout` | 4 |
| C (R-039) | `independent` | 1 |
| D (R-039) | `independent` | 4 |

Each condition: base, then the eight adapters, `run_recall_eval.py --final --items-per-kind 30` (30 conversations per
kind at each of 58 and 419 messages, 300 in all), `tool_loop` arm, greedy, item seed **90311** (fixed here; never used
before), identical conversations for every model. Results `results/recall_eval/final_<condition>_<model>_seed_90311.json`,
each committed as it lands. A try that crashes before writing its results is retried and the retry is reported; a
results file is never replaced.

**Pass rules, as registered and amended; every rule in every condition.**
1. **Recall** (`older` and `confirm`, 120 conversations): pooled over the eight adapters, at least 20 percentage
   points above base at each message size, and a paired exact sign test on the adapter-conversation pairs where base
   and adapter differ, p below 0.01 (R-016).
2. **Recall by source** (R-041): rule 1 must also hold when only retrieved answers count (`found_fact`), for base and
   adapters alike.
3. **False retrieval** (R-038): each adapter's false retrievals no more than base's on the same conversations.
4. **Coherence** (R-016, R-039): each adapter's coherent count at or above base's on the same conversations; in A on
   all 300, in B, C and D on a fixed sample of 120 (for each kind and size, `random.Random(39).sample` of 12 from the
   item ids sorted, drawn by code before any run). Judged under R-154's frozen rule: three fresh judges of
   `claude-sonnet-5-5`, each in its own folder with only the R-128 brief (paths, sheet names and line counts changed),
   the rubric and the sheets; judge 1 decides, judges 2 and 3 are reported; `freeze_r154.py judges` on every judge
   transcript, and a judging by any other model is void and redone.
   **Sheets:** one blind sheet per part, every model's reply to the same conversations shuffled together with the
   names removed (`make_multi_sheet.py`, R-090), so base is judged once per conversation by the same judge as every
   adapter. A: one sheet per kind (60 conversations, 540 lines each). B, C, D: two sheets each (`older`, `confirm`,
   `in_view`: 72 conversations, 648 lines; `never_told`, `statement`: 48 conversations, 432 lines). Shuffle seeds 90560
   onward, in the order A to D.

**Reported beside these, not gating:** each kind alone, right search decisions, clean calls, runs out of calls, recall
by source in full, each adapter alone, seed 82 alone with its sign test against base, a whole-conversation resampled
interval (the adapter-conversation pairs of rule 1 share conversations, so its p-value overstates independence), and
recall split into `older` and `confirm` (R-159). **Project result:** pass needs rules 1 to 4 in all four conditions;
otherwise the write-up says which failed and by how much. Every condition is reported in full either way.
