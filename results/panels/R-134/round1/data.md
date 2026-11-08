**Panel report: SFT data curation (read-only; I wrote nothing and opened no forbidden file)**

**1. The most fixable weakness, read from the rows**

The in-view deflection has a clear source in the training rows, and the "It sounds like" opener is only one sign of it.

- In `data/screens/fix17cs37.jsonl` I read all 150 `in_view` targets by hand. 28 of them do not give the value as the answer. Instead they ask for a hint, ask for more context, send the user to ask someone else or to search, treat the message as a feeling, or deny the fact. Only 10 of these 28 open "It sounds like".
- The trigger is the message form. 22 of the 28 sit on memory-word messages ("escapes me", "gone out of my head", "won't come to me"). That is 22 of 53 memory-word rows (42%), against 6 of 97 rows asked as plain questions (6%). The deflecting targets also run long: 31.9 words on average, against 19.5 for the other 122.
- The misses copy these rows nearly word for word. Over 6.37's hd and probe results at seeds 82, 83 and 94 to 96 there are 66 in-view misses. Five phrases appear in no training kind except `in_view`, each in only 1 to 4 rows: "give me a hint", "a bit lost or confused", "trying to remember", "Is there anything specific" and "something else?". Between them they appear 10, 9, 14, 4 and 8 times in those misses. "a bit lost or confused" comes from a single row (0122) and shows up in 9 `hard_dev` misses.
- 6.34 removed the opener but not the behaviour. Its `hard_dev` in-view misses at 82 and 83 (10 and 17) reuse the deflecting rows it kept: "That's a tough one. Maybe..." (rows 0098 and 0146), "Maybe you could ask Eamon" (0139), "It seems like you're trying to remember" (0130), "That's a bit of a bummer" (0135) and "That's a great question. Can you tell me more" (0085). Its 22 removed rows were also 12 good answers plus 10 deflections. That cut good no-search examples, which fits the 6 search-and-deny misses at seed 83.
- Lower-case typing (R-133) shows the same thing. Of 19 `st_style_hd` in-view misses at 82 and 83, 17 contain these deflection phrases.

**2. Proposed fix: 6.38, rewrite 28 targets and remove nothing**

- Start from `fix17cs37.jsonl`. Change only the final assistant turn of these 28 `in_view` rows: 0000 0015 0027 0036 0057 0058 0059 0060 0064 0077 0079 0085 0086 0088 0094 0098 0099 0103 0120 0121 0122 0130 0132 0134 0136 0139 0145 0146.
- Every other byte stays the same, including the 28 user messages. Totals stay at 1,094 rows and 150 `in_view` rows.
- Each new target is hand-written in a dictionary keyed by row id inside a build script modelled on `build_r122.py`, so the build is deterministic. Rules for each target:
  - The first sentence gives the value with every detail on its chat line (person, value and qualifiers such as "in a raffle" or "on Sunday").
  - It opens with the person's name or the value, the way the set's good in-view answers do ("Greta broke her thumb skiing.", "Esther. That's a lovely name.").
  - It may add at most one short closing comment from frames already in the set ("That's a pretty cool prize."). No question, and no sentence about the user's feelings.
  - It never opens "Your ...".
- Then vet the 28 with one fresh blind judge, as in R-118.
- **Why this should not repeat the earlier trade-offs:**
  - 6.34 removed 12 good answers and left 18 deflecting rows. This keeps every row and changes only the 28 deflecting targets.
  - 6.32 added 72 rows in the "Your {relation} {person} {fact}." frame. That frame is also the scripted frame of 231 of 332 `older` targets and all 230 `confirm` targets. No in-view target uses it today, and R-121 blames it for answers after a search dropping the asked detail. This fix adds no rows and avoids that frame.
  - R-115 cost came from an extra epoch. This keeps 6.37's recipe exactly, trained from scratch.
  - R-120's on-top training and fix 12/13 (all 150 in-view targets replaced, R-063/R-064) both changed far more. This is the smallest in-view edit tried so far.

**3. Lines it should move, and the gate line most at risk**

- **Should move:** `hard_dev` `in_view` (6.37: 42 and 40 at 82 and 83, 200 of 240 over five seeds). Also probe `in_view` (88 of 96 at 82 and 83) and R-133's lower-case in-view gap (probe −8, `hard_dev` −5).
- **Most at risk:** probe recall pooled 192 (R-094). Here any single miss fails, and R-127's base rate for one missed question is about 28%.
- **Next risk:** `hard_dev` recall against 6.37's 163. R-063 and R-064 show that changes to in-view rows can turn found facts into "I don't have that from you".

**4. Confidence**

About 20% that 6.38 replaces 6.37 under the full gate.

- **For:** the cause is measured, the change is the smallest yet, and it fits the clock. The build and vetting run on the CPU, so training at 82 and 83 can start well before 22:00.
- **Against:** the 28% probe base rate, two earlier in-view edits that cost `older` recall, and judged sheets plus three unread seeds still to clear.

### Critical files for implementation
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/data/screens/fix17cs37.jsonl
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/records/build_r122.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/run_recall_train.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/results/recall_eval/hd_fix17cs34_83_seed_73157.json
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/RECORDS.md (R-063, R-064, R-121)