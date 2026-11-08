**Panel 7, conversational language and dialogue pragmatics: report**

Transcript note: I read the brief, RECORDS (R-062 to R-064, R-110, R-114, R-115, R-117, R-120 to R-122, R-132, R-133), `run_recall_train.py`, `loss_masks.py`, part of `run_build_training_set.py`, the rubric, `fix17cs37.jsonl`, and the result files for seeds 82, 83 and 94 to 96 (plus `hd_base`). I opened no sealed, token or 97-to-99 file, and I wrote nothing.

**1. Reading**

The training set does not lack indirect phrasing as a class. 52 of its 150 in-view questions are indirect forgetting statements ("has gone out of my head", "escapes me", "i've lost which"). It does lack three specific shapes:
- The "my head has lost…" frame: 0 rows. On `hard_dev` these items score 33/50 (base 1/10).
- A question word in the middle of the sentence ("Anselm did what at uni again", "three years at uni on what exactly"): 0 rows. These score 1/10.
- Names typed in lower case: 0 of 5,098 user turns.

The probe's "drawing a blank / blanking / cannot think" forms are kept out on purpose by the four-word rule.

By shape over 5 seeds:
- Probe: indirect forgetting statements 44/65 right, plain direct questions 170/175.
- `hard_dev`: "my head has lost" 33/50, other shapes 167/190.

The bigger defect is the answers the model is taught to give. In-view rows get full loss (`chat_decision` masks only `statement` rows). Of the 52 indirect in-view rows, 23 have a target that does the misreading itself:
- reads the forgetting as a feeling: in_view_0122 "It sounds like you're feeling a bit lost or confused about…", which is word for word the opening of the eval misses;
- reads "lost" as losing a thing: in_view_0145 "If you lost the phone…", in_view_0094 "It sounds like you're a bit lost";
- sends the friend elsewhere: in_view_0103 "You can ask your cousin…";
- answers an older message: in_view_0086;
- gives a wrong fact: in_view_0114 "July is the 7th month", in_view_0124 "That's not true. You're a court reporter".

Several in-view targets also deny what the chat says (in_view_0015 "You didn't mention…", plus "I'm just a large language model", "I didn't know…"). Under the R-109 rubric, answering an older message and denying what was said both score 0, so these targets are incoherent as well as wrong.

Counted by opening words, 44 in-view targets are of this kind: the 22 that open "It sounds like", and 22 that open as a deflection, a puzzle or a denial (in_view_0015, 0038, 0057, 0059, 0076, 0077, 0080, 0085, 0098, 0103, 0112, 0114, 0120, 0124, 0130, 0131, 0133, 0135, 0139, 0143, 0145, 0146).

**2. Fix: change the answer, keep the row**

Keep all 1,094 rows, every question, and every no-search decision byte for byte. For each of the 44 in-view rows above, replace only the last assistant turn with a new reply from base, on the same three exchanges with no tool. Sample up to N candidates per row (N fixed before the build). Keep the first candidate that passes all of these:
- names the value (the existing scorer);
- does not open with "It sounds like you" or "It seems like you", "You can ask/try", "That's a tough one", or a denial;
- has no four-word run in common with the probe or `hard_dev` pools.

If a row has no such candidate, use the existing `hinted_reply` path, since that is still base's own voice. Then one fresh Sonnet judge marks every new target against R-118's in-view rubric and R-109's coherence rubric. A row that fails keeps its old target, and the build reports how many rows changed.

I propose no new rows in the missing shapes. They would be written after reading `hard_dev` misses, and `hard_dev` is scored on the same items at 97 to 99. Additions are also what cost R-118/R-121 and fix 13.

**Why this should not repeat the earlier trade-offs:**
- 6.34 removed 22 no-search rows, and its misses moved to searches and denials. Here the decision mix does not change at all.
- R-121's scripted "Your {relation} {person} {fact}." answers taught a short answer shape. These replies are base's own sentences, not scripted.
- Fix 12's brief targets led to declining. These replies are not shortened.
- Fix 13 changed how many questions were indirect. That share does not change here.

**3. Lines**

- **Should move:**
  - `hard_dev` in-view: 6.37 at 82 and 83 is 82/96.
  - Probe in-view: 88/96.
  - Misses that open "It sounds like": 32 of 40.
  - The lower-case typing in-view gap (−8 and −5): partly, as its losses are the same failure.
  - Judged `hard_dev` Sheet B in-view, R-110's tightest judged line, because rubric-0 targets are removed.
- **Most at risk:** `hard_dev` recall pooled against 6.37 at the same seeds (R-094). This is the R-063/R-064 pattern, where more confident in-view reading came with "I don't have that from you" after a found fact. Second risk is the probe `statement` line.

**4. Confidence**

About 15% that it replaces 6.37 under the full gate. The change is narrow and keeps the decision balance, so the opener should go without 6.34's shift to searches. But:
- the line it fixes is not gated;
- every earlier in-view edit cost 5 or 6 found-fact answers;
- 6.37's `hard_dev` recall ranges 73 to 90 a seed, which is wider than any gain this could buy;
- I could not measure how many of the 44 rows base can answer cleanly without running it.

### Critical Files for Implementation
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/data/screens/fix17cs37.jsonl
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/run_build_training_set.py (`base_reply`, `hinted_reply`)
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/vet_statement_targets.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/run_recall_train.py (in-view keeps full loss under `chat_decision`)
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/results/coherence/R-109/judge/rubric.txt