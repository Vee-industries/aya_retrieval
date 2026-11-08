**Panel report: retrieval and tool use (search decision and answer grounding)**

Files read: `src/aya_retrieval/tool_prompt.py`, `harness.py`, `recall_tool.py`, `chat.py`, `inference.py`, `pool_hard_dev.py`, `pools.py` lines 1-451, `results/recall_eval/hd_fix17cs37_{82,83,94,95,96}_seed_73157.json` and the probe files for the same seeds, `data/screens/fix17cs37.jsonl`, `fix17cs21.jsonl` (R-110's rows), and RECORDS R-110, R-113, R-114, R-115, R-121, R-132. I wrote nothing.

**1. The most fixable weakness**

The fix should target the found fact whose detail is left out. Over 82, 83 and 94 to 96 there are 47 `hard_dev` recall misses where the search found the fact line. 45 of them come from three fact types:
- `bird_pet`: 17
- `interview_day`: 16
- `soup`: 12
- `tea`: 2
- the other four types: 0

Each of those three lines opens with an event and puts the value in a later clause, about 30 words in ("collected the keys ... ready for the {value}", "got a job interview booked for {value}"). Every wrong reply restates the event and stops: "Your sibling Petra collected the keys." The correct replies use the same restating shape and simply go on to the value.

Where this comes from in the training set:
- 461 of the 562 found-fact answers in `fix17cs37.jsonl` have the shape "Your {relation} {person} {the line restated}".
- No fact line in the training set is longer than 20 words. Median length is 11 words for `older` and `confirm` and 10 for `in_view`.
- Every TRAIN statement (`pools.py` lines 54-330) is one clause with the value as its object. So "restate the first clause" has always meant "name the value". The model has never seen a line where the first clause matches the topic but holds no value.

This miss also drives the seed-to-seed spread. Found-but-wrong misses are 19 at seed 82 and 3 at seed 83, while `hard_dev` recall is 73 and 90. That spread is what makes R-094's same-seed recall line risky.

**Search decision:**
- In-view deflections are not a mistake about where the fact is. 36 of the 40 `hard_dev` in-view misses made no search, which is the right decision; the model then failed to read the line in view. 21 of the 40 are "my head has lost..." messages. They also fall on different fact types: `degree` in-view is 9 of 20 correct, while `bird_pet` in-view is 33 of 35. So this is the wordplay and "It sounds like" failure, not a retrieval one, and my fix does not target it.
- "A search built from the wrong message" does not happen on the plain sets. Of 1,434 searches, 4 failed using words that were in view but not in the message. The bad queries reuse training query patterns from other fact types instead ("godson born birthday month" for "came of age").
- The tool-result format (`Use this result to answer the original question.`) does not restate the question, which is a standard RAG weakness. Changing it would change the base model's numbers too, which moves the gates, so I am not proposing it.

**2. Proposed fix: 6.38, a replacement, trained from scratch**

- Start from 6.37's 1,094 rows.
- Build 40 fresh TRAIN-pool rows with `build_r110.py`'s machinery: real search, R-020 decoy counts, scripted pool answer, vetting stops, four-word-run skip. That is 20 `older` and 20 `confirm`; 40 is R-110's registered count for one form.
- Each fact line uses a new "event, then value" form. The first clause names the topic with no value, for example "spent weeks visiting the shelter before bringing home a dog, and they named it {value}". The value never appears in the first clause.
- Keep `hard_dev`'s words out (keys, window, hosted, dish, served, booked, interview, weekdays).
- Remove 40 existing rows of the same kind and fact type, picked with a fixed seed. Row count, kind mix, the 222 statement rows and the answer shapes all stay as they are.

Why this should not repeat the earlier trade-offs:
- R-110's rows put the asked fact in the first clause in 20 of 40 `two` rows and about a third of the `runon` rows. That trains "restate the first clause and stop", which matches the detail miss rising from 21 (the control) to 29 (6.21). R-110 was also an extra epoch on top of 6.2, which cost 6 recall answers by itself (R-115).
- R-121 added a new answer shape given with no search; 6.38 adds no new answer shape.
- 6.34 removed rows the model needed; 6.38 changes only the evidence the answers are read from.

Contested point: R-110 deliberately left the "event first, value last" shape out to avoid fitting `hard_dev`, and R-132 objects for the same reason. That shape is the failure kind, so I would include it, keep the words out, and disclose it.

**3. Lines**

- Should move: `hard_dev` found-but-wrong misses, now 22 at 82 and 83, and `hard_dev` recall pooled, now 163 at 82 and 83.
- Most at risk: R-094's probe recall line, which 6.37 holds at exactly 192 (R-127: a copy with no defect misses one probe question 28% of the time). Second risk: `hard_dev` in-view, if longer found lines shift trust from the view toward the search (R-063 and R-064 in reverse).

**4. Confidence**

About 15% that 6.38 replaces 6.37 under the full gate. The cause is clear and the change is small and same-sized. But it is the 17th draw since R-093, it must clear the probe line at 192, the judged sheets and the unread seeds, and the past panels' estimates for a full pass were 10 to 14%.

### Critical files for implementation
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/records/build_r110.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/data/screens/fix17cs37.jsonl
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/src/aya_retrieval/pools.py (lines 1-451 only)
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/records/build_r122.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/src/aya_retrieval/harness.py