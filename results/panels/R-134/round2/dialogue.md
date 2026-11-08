**Round 2: dialogue and pragmatics expert**

I read the five other reports and wrote nothing. I opened no sealed, token or 97-to-99 file.

**Claims checked against the files**
- **Data: correct.** All 28 ids exist, and 10 of them open "It sounds like". The 28 deflecting targets average 31.9 words against 19.5 for the rest. The five deflection phrases appear only in `in_view` targets. "a bit lost or confused" comes only from in_view_0122 and appears in 9 `hard_dev` misses. There are 66 in-view misses over the two pools.
- **Against: correct.** 57 correct `hard_dev` replies open "It sounds like". 6 targets open "You can". Only 4 of the 40 misses searched. 17 of the 40 misses are "my head has lost" items.
- **Retrieval: one count is wrong.** It says 21 of the 40 `hard_dev` in-view misses are "my head has lost". The files give 17, from 10 items scoring 33 of 50. Its type counts check out: `degree` 9 of 20, `bird_pet` 33 of 35.
- **Against, overstated.** "Rewriting as direct answers is fix 12, 13, 6.311, 6.32" is not accurate:
  - fix 12 replaced all 150 targets with brief base replies;
  - fix 13 changed how many questions are indirect;
  - 6.311 and 6.32 added 72 rows in the "Your {relation} {person} {fact}." frame.
  None of them edited a few targets in place without that frame.
- **My own round 1 overreached.** Since 57 correct replies use the opener, the opener is not the fault, so I drop the 22 fact-stating "It sounds like your…" rows from my list.

**1. Final position: data's 6.38, with two rows added (30 targets)**
- Take data's 28 ids, plus in_view_0124 and in_view_0143. 0124 ("That's not true. You're a court reporter") gives the friend the coworker's job. 0143 ("I don't know much about Greta") denies what the chat says. R-109's rubric marks both 0.
- Change only the final assistant turn of those 30 rows. Every other byte stays the same: 1,094 rows, 150 in-view.
- Use data's hand-written target rules:
  - the value first, with all its details;
  - open with the name or the value, never "Your …";
  - at most one short comment taken from frames already in the set;
  - no question and no talk of feelings.
- Also check that no target shares a four-word run with the probe or `hard_dev` pools.
- One fresh judge marks each target under R-118's in-view rubric and R-109's rubric.
- I drop my base-resampling plan. Hand-writing is deterministic, needs no GPU, and cannot bring the opener back.

**2. Strongest objection: stats**
The in-view line is not gated, and a perfect copy of 6.37 passes the full gate only about 3% of the time. I accept that. My answer is that the cost is small: 30 targets change, and the deflection is the one failure seen in three places (plain `hard_dev`, lower-case typing, phone typing). The edit also lifts R-097 and the judged in-view sheets, which are gated. But it buys little gate probability.

**3. Probability**
I lower it from 15% to about 7%. Stats' per-line pass chances and the record (1 full pass in 16 candidates) are the better anchor.

**4. What I need in the chair's design to vote yes**
- the exact 30 ids, or data's 28, with every other byte checked unchanged (SHA-256);
- no "Your …" frame, and no target opening with a question or a feeling;
- the judge passes every target, and a row that fails keeps its old target;
- registered before any row is built, as stats asks:
  - the 82-and-83 reference: 6.37's 192 and 163, or v6's 192 and 157, chosen now;
  - 6.37 retrained at 97 to 99 first, alone on the card;
  - pooled three-seed comparisons, ties passing;
  - stop on any fail;
- the write-up says the 30 rows were chosen after reading `hard_dev` and battery misses, scored again on the same items.