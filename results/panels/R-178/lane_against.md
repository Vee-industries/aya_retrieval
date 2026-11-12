AGAINST LANE, R-178. I read the brief, R-141/142/150 to 163, R-050/054/076, R-169, R-171 to R-177, pools.py to line 451 and docs/demo.md. I edited nothing and ran no model. I ran one CPU count on data/screens/fix17cs37.jsonl (script: C:\Users\Gaming\scratch\claude\C--Users-Gaming--claude-spares-spare-wcSF8M\3f7d989b-d009-44ac-9f86-64e88058f022\scratchpad\review\count_queries.py). It found 722 search queries, 288 of them distinct. Every query names a relation word or a TRAIN person, and none is about the speaker.

1. THE FOUR BELIEFS

(a) Sealing first makes the fix honest. Wrong. Sealing fixes the order of events. It does not make the test independent of the fix, because the person who designs the test already knows the failures.
- The orchestrator wrote demo/chat.txt, read its failures, and will write both the test brief and the training rows. R-151 says a set used to design a fix cannot judge it: "Designing 7 from its failures uses it, so it can no longer judge 7". A test built around the three named weaknesses is a test designed from the demo's failures.
- Same writers: the writers are Opus, the same family as the orchestrator. R-142: "closer to one writer with four settings than to four independent writers".
- Small test, large noise: on a test this size, seed noise (R-141: hard_dev 73 to 90 across seeds) is bigger than any gain that could be credited to the fix.

(b) Fixable with training data in about two days. Wrong on the record.
- Query wording: R-054 found that teaching queries from the user's own words teaches "any line naming a person is a lookup". R-050 measured the cost: never_told fell from 48 to 21, with 27 false retrievals. R-153 ruled the route out: "Queries from the question's words (failure 2): ruled out".
- Answers from search results: R-150 says "nothing in the record has lowered it except a seed draw".
- Every candidate after 6.37 failed a gate (R-155, R-157).
- The diagnosis is weak. It rests on 12 questions from one script, one writer and one seed. In R-176, 6.37 searched "sister car auction" and "sister shop opened", and car and shop are trained fact types. So weakness 1 is not shown to be "untrained fact type".
- What the data does show: no training query is about the speaker, and the sink fact and "what car i drive" are both about the speaker.
- R-176's own record says its branch design kept the earlier wrong answers in view. So weakness 3 is partly a product of the test design.
- Targeting all three at once breaks one-factor attribution. R-153: "a fail could not be blamed on either".

(c) A pass on the new sealed test can replace 6.37. Wrong as stated.
- The heldout and independent pools were read for 6.37 (R-163) and are now development sets. A replacement would have no sealed result on generated pools. The headline 91 to 107 of 120 would describe a model that is not shipped.
- The old gates have a high false-fail rate even for a copy of 6.37. R-156 says the five-seed lines "are so strict that 6.37 fails them at its own seeds".
- Only a pass on every old gate plus the new test can justify a swap. The odds of that are low (R-150: a fix and a draw both pass about 15%).

(d) Reopening strengthens the submission. Wrong if a new model ships; partly true if it does not.
- The strongest fact in the submission today is a frozen model with a sealed pass and a published weight hash (R-160, R-172). Swapping the model after a public demo failure is exactly the pattern a judge reads as moving the goalposts.
- The part that holds: running the new sealed test on 6.37, base and code that always searches, and reporting the result, strengthens the submission whether or not a fix passes.

2. HOW THE NEW TEST CAN LEAK OR BE STEERED, AND THE FIX FOR EACH

- Same writer family. Test writers, the outside-writer sets and the training-row author are all Opus. Fix: Kevin writes a share of the test chats by hand before any row exists (he has not seen the fix rows). Report his items separately. State the one-family limit.
- Fact types chosen with the weakness in mind. Fix: reuse R-142's writer spec unchanged, with new settings and no fact types named. Report results split by fact types inside and outside the new training rows. Before any row exists, commit a script that reads the sealed test and prints only counts: four-word runs and content words shared with the training rows (R-153's check).
- The orchestrator knows the demo. Fix: the writers never see the demo, R-175 to R-177 or the project. From now on the demo is development data and no demo improvement is reported as evidence.
- The never-told item can be gamed by wording. R-176 showed that "I don't see it, so I'd only be guessing." was marked ABSTAINED although the brief's own wording makes it RIGHT. A fix that only changes the decline phrase would gain points with no change in behaviour. Fix:
  - Settle that rubric line before sealing, and score 6.37 under the same rule.
  - Pair every never-told item with a told item in the same chat. Then a model that simply declines more cannot gain.
- Weakness 3 depends on the model. If the candidate's earlier answer happens to be right, the condition never arises. Fix: the code plants a fixed wrong earlier reply in the history, the same for every arm, fixed before sealing.
- Repeated looks and choosing among candidates. Fix:
  - One recipe enters, with every trained seed pooled and the shipped seed fixed before training (R-141: picking a seed by development score is selection).
  - One run per arm, all arms in one queued script committed before training. Nothing is read until every arm is done.
  - No second candidate is scored on the sealed test.
- Scorer, judge prompts and seeds. Fix:
  - Write a manifest like freeze_r154.py's at seal time: test files, loader, scorer, judge brief, rubric, judge model, shuffle seed and item order. Run `check` before the run; any change makes the run void.
  - Fresh Sonnet judges with no tools and the models hidden, each judge marking both arms on one shuffled sheet. Audit every transcript.
- A local timestamp proves nothing. Git dates can be set locally. Fix: with Kevin's yes, push the sealing commit, or post its hash, before the first training-row commit.
- The strongest baseline goes first. Base, base with the whole chat and code that always searches run on the new test before any candidate.

3. RISK TO WHAT THE OLD GATES MEASURE

- Weakness 3 against in-view answers. The fix trains the model to distrust what is in view. in_view trains it to trust what is in view. Probe in_view is already at the edge: 6.37 itself scored 39 at seeds 95 and 97 against a bar of 41, and 7.1 failed at 38.
- Weakness 2 against recall. Teaching "decline when the passage is unrelated" raises false denials where the fact was found but is phrased indirectly. On hard_dev, 18 of 23 misses were found-but-misread answers (R-141). A third of the outside-writer chats state facts indirectly (R-142).
- Weakness 1 against never_told and statements. Query changes cost never_told and statements before (R-050, R-054). Adding rows where the user states their own facts may make the model search on statements.
- Coherence: new reply wording is not covered by any gate on recall answers (R-150).

Gates a candidate must still pass, unchanged, at seeds 82 and 83 or pooled as registered (R-153 items 1 to 3):
- R-086's unjudged lines and R-094's slips.
- Probe and hard_dev recall at 73157.
- Probe in_view at least 41, probe 51203 recall at least 94 and statement at least 47, hard_dev never_told at least 44, false retrieval limits.
- R-102's stress runs.
- R-086's judged sheets with three Sonnet judges.

Also required:
- On both outside-writer sets, not below 6.37 seed 82: recall 39/53, in_view 35/37, never_told 37/36, statement 37/35, false retrievals, and agreement with false claims (R-158).
- R-169's comparison with code that always searches.
- R-162's four rules on heldout and independent, labelled as a second look. This is only honest if those pools stay out of development from now on.

4. DEADLINE

It is now Thu 12 Nov, 10:54 UTC. Submission closes Mon 16 Nov, 11:59 UTC, about 97 hours away. The card is shared with Kevin's games.

Rough cost:
- Write, load, audit and seal the test: about 4 h.
- Panel and row build: half a day.
- Five seeds of training: about 3 h on the card.
- Old gates plus judges: about 6 to 8 h on the card.
- Sealed run: about 2 h.
- Rebuild the write-up, new HF repository, notebook hash and CI: about a day.

So there is room for one attempt with no second try.

Cut first: a second candidate, then a fix for more than one weakness (do one, as a one-factor change), then notebook Part B re-verification. Never cut a registered gate. A gate that cannot run means the candidate does not ship.

Before any new work, Kevin submits the 6.37 version now. The latest submission counts, so 6.37 is on file if the attempt fails.

Last point to start new training: Sat 14 Nov, 12:00 UTC. The test must be sealed by Thu night. No model change after the 16th: shortlist slides can report the attempt but cannot swap the submitted model.

5. WHAT THE WRITE-UP MUST SAY

Order of events, with times and hashes:
1. Freeze, 9 Nov 14:52 (R-160).
2. Sealed pass (R-163).
3. Publication of weights e661a81c (R-172).
4. Demo run 12 Nov 05:05 Eastern, run before it was registered (R-175).
5. R-176 registered, result at 05:48: base 2, 6.37 0.
6. Reopening (R-177).
7. The sealed test's SHA-256, its commit and its outside timestamp.
8. The first training-row commit, after it.
9. The ship rule's commit, before the sealed run.

It must also say:
- The test was designed after the failures were seen. It measures the named weaknesses and nothing more general; claims about generality still rest on the outside-writer sets.
- The writer-family limit.
- The candidate ledger count: 40 sets screened before, so this is the 41st.
- What changed: training rows only, with recipe, scorer, judges and old gates unchanged.
- What did not change: 6.37's results and its published repository, which stay up and are not overwritten. A candidate goes to a new repository.
- Every old-gate number for both models, losses included.
- If no candidate passes: "6.37 ships; the attempt failed on <gate>".
