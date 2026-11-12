Method lane, R-178. I read the brief, R-175 to R-177, R-041/R-050/R-071/R-073 (earlier query and fact-type fixes), R-141, R-157 to R-163 and R-169. I also read the build, train and eval scripts, conversations.py, demonstrations.py, recall_tool.py, scoring.py, harness.py, stress.py, dev_set.py, loss_masks.py, pools.py to line 451, data/blind_dev2/brief.md and fix17cs37's provenance. I edited nothing and ran no model. My one script was a read-only count over data/screens/fix17cs37.jsonl.

**Facts from the code that shape the plan**
- All 722 search calls in 6.37's set are "{who}" plus one of 25 fixed keyword tails, so the query is chosen by fact type, never written from the message.
- Every training chat holds one fact type. Its other fact lines are the same type about other people (build_item). No row ever sees a passage of another fact type come back.
- No row has an earlier question and its answer among the 3 exchanges in view (0 of 1,094). History turns carry no loss (demonstrated_labels), so a scripted wrong reply in view teaches nothing wrong.
- History: queries in the friend's own words (fix 7, R-050) raised probe recall from 84 to 94. It also raised false retrieval from 0 to 27, all never_told. A wider set of fact types (fix 14/14c, R-071/R-073) raised hard_dev recall from 58 to 76–79 and false retrieval from 4 to 13–16. **Fixing weakness 1 alone has twice made weakness 2 worse.**

## 1. The new sealed test (S3)
- **Category lists, written by the lead before any writer starts**, with a keyword lexicon per category:
  - T: 12 broad categories that match existing training types (pet's name, a move, a job, a car, ...).
  - U: 18 categories found in no pool, train_phrasings or fix17cs37 row (home repairs, appointments, lost items, allergies, ...). A script confirms the lexicon words appear in none of them.
  - A-new: 20 categories for new training material only. Test writers never see this list.
- **Writers:** 6 fresh claude-opus-5-5 agents, not forks, with blind_dev2's spec adapted.
  - They see the brief only, with the T and U categories given ids and not labelled as T or U, and 6 new settings.
  - They must not see any repo file, training data, the demo chat, earlier sets, records or the weaknesses' words (no sink, pottery or skiing).
  - Each writes 10 chats: 60 chats, 20–30 exchanges, at least 5 people. At least 2 U facts and 2 T facts per chat, and a third of facts about the user themself.
  - The last 3 exchanges hold one earlier exchange where the user asks about an out-of-view fact. The writer gives two versions of the assistant's reply: wrong (another chat value of that category, not the answer to any question) and right.
- **Questions per chat (9):**
  - older on a T fact; older on two U facts; confirm (half true claims, half false); in_view; statement.
  - never_told, plain.
  - never_told, overlap: never told, but it shares a content word with an earlier exchange about something else. `wrong` lists that exchange's value.
  - re-ask: the fact the wrong reply got wrong. Scored in the wrong view only.
- **Run plan:** all 8 questions in the right view; older, never_told and re-ask also in the wrong view. That is about 840 turns per arm, about 25 minutes.
- **Conditions:**
  - Weakness 1: U recall, 120 questions.
  - Weakness 2: N-hit never_told items, named by registered model-free code at unsealing (message content words, OR search, at least 1 passage). Measured as the share that names a `wrong` value.
  - Weakness 3: copy rate, the share of non-re-ask questions whose reply contains the in-view earlier answer's value, wrong view against right view.
- **Scorer:** the frozen item_correct is primary. Two Sonnet judges (R-176 brief, models hidden, agreement needed) judge never_told and U recall at seed 82. R-154 coherence judging (three Sonnet judges, judge 1 decides) runs on a 120-question sample drawn by code before the run.
- **Sealing:** chats go in `data/heldout3/chats/`, so the existing "named heldout" read limit covers them.
  - Mechanical checks print counts and reasons only. The writer audit lists tool calls and paths only.
  - The load_dev_set sha256 and per-file hashes go in `results/freeze/heldout3_manifest.json` and a record, committed before any new template or row exists.
  - Code guard, committed before the writers start: `--items-dir` under a heldout path needs `--final`.
  - No person or agent reads the set. It is opened once, by the registered queue, after the ship rule and the candidate's seeds are committed.
- **Power** (my estimates; inputs are the seed spread of 44–56 of 120 in R-157 and 73–90 of 96 in R-141):
  - U recall, 3 seeds a side: seed error about 2.7 points, item and chat error about 6.5, total SE about 7 points.
  - With a rule of "difference at least +10 and lower 95% bound above 0", a true +25 passes about 95% of the time, +20 about 80%, +15 about 60%. No true effect passes about 2.5%.
  - N-hit (about 50 items): SE about 9.5 points; it detects 25–30 points.
  - Copy rate (60 chat clusters): SE about 7 points.
  - 5 seeds instead of 3 would cut the SE only from about 7.0 to 6.8, so 3 seeds (82, 83, 94).

## 2. The fix, ranked
1. **F3, earlier answer in view (weakness 3).** About 30% of rows of every kind get 1–2 in-view exchanges turned into an earlier question with a reply: half right, a quarter wrong, a quarter declined. The earlier value joins `forbidden`, so fit_to_copy rejects base replies that copy it. About 50 re-ask rows search and give the right value. Built as a training variant of `stress.asked_before` on the train pool. Cost: 2 h code, 0.5 h card build.
2. **F2, chats with several fact types (weakness 2).** build_item gets an `other_facts` option on a separate generator, so default items are unchanged. It adds 2–4 facts of other types, some about the asked person or relation. never_told rows are kept only when search returns passages, in three equal shares: same type other person, other type same person, a shared ordinary word. Values in returned passages other than the answer are forbidden. **F2 is required whenever F1 is used.** Cost: 3–4 h code and tests, 0.5 h card.
3. **F1, query writing (weakness 1).** `--message-queries` on all search rows and `--wide-share 0.5`. Optionally, first-person templates on A-new categories, written by a fresh agent that sees only that list. Checks: U lexicon count 0 on built rows, and the R-070 four-word overlap checker against test pools. Cost: 3 h code, 1 h writer (in parallel), 0.5 h card.

None of these reads S3. The lexicon and checks use the lead's lists only.

**Drop if behind:** the first-person writer pool, by Friday 13 Nov 08:00. **Drop outright:** harness changes (merging the model's query with the message words, hiding earlier replies). They change the system under test, break comparison with R-163, and leave the weights as they are.

## 3. Screening on already-read sets
- **Candidates, registered first:** K2 = F1+F2+F3; K1 = F2+F3. Seeds 82 and 83 against 6.37's existing adapters at the same seeds.
- **Sets:** probe, hard_dev, blind_dev, blind_dev2. Two new dev stresses on probe and hard_dev with only the relevant kinds: `--wrong-before` and `--other-facts`. The demo's 12 questions are report only.
  - The stresses share their mechanism with training, so their gains overstate. S3 exists for that reason.
- **Gates:**
  - probe recall, two seeds pooled, at least 6.37's minus 4.
  - probe in_view at least 41 each seed (R-097).
  - hard_dev recall pooled at least 6.37's 163 minus 12.
  - false retrieval at most 6.37's plus 3 each seed; hard_dev never_told at least 44 of 48.
  - probe statement at least 44 of 48.
  - blind recall, 480 pooled, at least 6.37's minus 10.
- **Targets:**
  - T3: copies of the earlier wrong value at most half of 6.37's.
  - T2: other-facts never_told false answers at most half of 6.37's, with recall not more than 5 below.
  - T1 (K2 only): found_fact on blind older questions (320) at least 6.37's plus 10.
- **Choice rule:** K2 if it passes everything; else K1 if it passes; else no candidate. The sealed run then measures 6.37 and the baselines only, as a report. Exactly one candidate enters S3.
- **Schedule (Eastern):**

| When | Work | Card |
|---|---|---|
| Thu 12, 06–09 | Lists, brief (against-lane check), loader and guard code, ship rule; all committed | — |
| Thu 12, 09–10:30 | Write, check, hash, seal S3 | — |
| Thu 12, 10:30–15 | F1–F3 code and stresses | 13–15: base and 6.37 at 82/83 on the stresses (1.5 h) |
| Thu 12, 15–17 | Builds and data checks | 1 h |
| Thu 17 to Fri 03 | 4 train-and-score jobs, about 2 h each | 8 h |
| Fri 13, 08 | Decide by script | — |
| Fri 13, 08–09 | Candidate at seed 94 | 0.7 h |
| Fri 13, 11–16 | Sealed run, 9 arms: base tool, always_search, whole_chat; 6.37 at 82/83/94; candidate at 82/83/94 | about 4.5 h |
| Fri evening | Judges, then score | — |
| Sat 14 – Sun 15 | Write-ups; a day and a half of slack for gaming and crashes | — |

Card total is about 16 h.

## 4. Ship rule (register in R-178, before screening)
On S3, the candidate pooled over 3 seeds replaces 6.37 pooled over 82/83/94 only if:
- **(a) No regression:** overall recall, in_view, statement and plain never_told each no more than 5 points below 6.37. Coherence count at or above 6.37's minus 5% under judge 1, on the fixed sample.
- **(b) No weakness line worse:** each of the three weakness lines is no more than 5 points worse than 6.37.
- **(c) Two of three pass:**
  - U recall at least +10 points, with the chat-resampled 95% bound above 0.
  - N-hit false answers at least 10 points lower, bound above 0, and not above base's.
  - Copy rate in the wrong view at most half of 6.37's and at least 10 points lower, bound above 0.

My lane's view: two of three is the right bar. Requiring all three would reject a real fix of two at this power. The against lane may argue for all three.

Always-search code and whole-chat lines are reported first, not gated. A crash is retried and reported; a results file is never replaced. Anything else is a fail. If nothing passes, 6.37 seed 82 ships unchanged, and S3's numbers go in as the measured weakness.

## 5. What the submission must say, and when
- **Now, in the next resubmission** (README status, short write-up, model card, docs/demo.md):
  - A dated "Reopened 12 November" section: caught by R-173, then R-175's demo and search replay, then R-176's blind 8 (base 2, 6.37 0).
  - The three weaknesses with their counts.
  - R-163 and every earlier number stand unchanged.
  - The order of work.
  - The submitted version must never claim a frozen model while work goes on.
- **At sealing:** the S3 hash and commit, and the ship rule's link.
- **With the result, in the same commit as its record** (before 15 Nov 11:59 PM AoE, nothing pushed without Kevin's yes):
  - S3's result whatever it shows, baselines first.
  - The candidate ledger: 40 earlier plus K1 and K2, with each fail.
  - Dev reuse, and that the stresses share their mechanism with training.
  - The demo is not evidence for the fix, since its questions were read during design.
  - If a new adapter ships, it gets a new name; 6.37 stays published.
