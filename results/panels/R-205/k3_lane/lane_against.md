# K3 draft: against lane

Date 2026-11-12. Read-only. No model, no GPU, no repo edits, no git, and nothing opened under S3. I read the draft,
the writer brief and `scripts/records/build_k3.py`. Scripts and outputs are in
`C:/Users/Gaming/scratch/claude/C--Users-Gaming--claude-spares-spare-wcSF8M/3f7d989b-d009-44ac-9f86-64e88058f022/scratchpad/r205_lane/`
(`simulate.py`, `more.py`, each with a `.out`).

The writer files do not exist yet, so the natural rows are simulated on the closest existing material:
- Material: the two outside-writer dev sets (`data/blind_dev`, `data/blind_dev2`, 240 fact and never_told questions)
  and Demo2.
- Query rule: the brief's. Question words only, the brief's filler list plus R-176's stop words removed, at most 4
  words, in the question's order.
- Search and keep rules: as in `build_k3` (OR, top 5; fact rows kept only when the source is returned, never_told
  only with a passage).
- Limit: real writers choose their own query words, so these are estimates.

**Verdict: not ready.** The keep-only-when-found filter removes the rows K3 is written for:
- facts about the user;
- facts where the question and the fact line refer to the person differently.

It keeps those questions on the never_told side, which creates a new cue: a question about the user means "not
told". The natural rows also probably fail the draft's own line 3, and the brief repeats outside-writer dev material.
Fixable, but the fixes change the design and should be registered before any writer runs.

## Findings, most serious first

### 1. The filter drops the user-fact and split-reference rows, so line 6 should fail, and what is left creates a cue (risk a)

- The brief forbids a question from reusing the fact sentence's words, apart from the person's name or relation. A
  question about the user has no name or relation; "i" and "my" are stop words. So its query can share a word with
  the source only by breaking the rule, and an OR keyword search cannot return an exchange that shares no word with
  the query.
- Dev simulation: 68 of 160 older questions are dropped. 64 of those 68 share no content word with the source line.
- Demo2 under the brief's rule: Q1 "where do i work" (user) gives the query `work lol`, and Q5 (user ingredient) gives
  `remind ingredient stay away`. Both are dropped. Q4 "where is my sister headed" (the source names only "tessa") is
  dropped too. Only Q2, Q3 and Q6 would be kept.
  - K1's Q1 search held the source only because the OR query "where do i work" matched the stop word "i".
- Never_told rows, which the brief allows about "the user", are kept whenever any passage returns: 80 of 80 on dev.
- Result: in the natural rows a question about the user is rarely an older row and often a never_told row. K1.3 has
  no user questions, so this cue is new. On S3, which by the draft's own disclosure has speaker items, it points
  toward "not told". Split-reference questions (relation in the question, name in the fact) are removed the same way,
  and the brief's "about half name only or relation only" is undone for older rows.
- Line 6 (user facts at least a third of kept fact rows) will most likely fail, or pass only through rows whose
  writer broke the no-reuse rule.
- What to change:
  - Before writing, register what happens to dropped fact rows. Recommended: keep them, with the search output as
    returned and a reply that says the search did not find it, as K1's `now_missed` rows did (R-178). The person and
    category mix then stays the same on both sides.
  - Report kept-by-person ("me" against others) and kept-by-reference (same against split) on each side.
  - State plainly that no question-word query can reach a zero-overlap user fact with this tool. K3 can train reading
    only for user facts the search actually returns.

### 2. Line 3 is likely to fail on the natural rows alone

- Dev simulation of kept rows: fact rows average 3.18 passages, never_told rows 2.79, a gap of **0.40** (line 3 allows
  at most 0.37).
  - Fact rows by passage count (1 to 5): 18, 41, 41, 30, 39.
  - Never_told rows by passage count (1 to 5): 12, 32, 13, 7, 16.
- The keep rule biases this. Found fact rows are a selected set (queries that matched), while every never_told row
  with one passage is kept.
- Fact rows also get higher top scores:

  | | Top score, fact rows | Top score, never_told rows | Top minus second, fact | Top minus second, never_told |
  |---|---|---|---|---|
  | natural (simulated) | 4.14 | 3.17 | 1.43 | 0.93 |
  | K1.3 | 5.19 | 3.43 | 2.02 | 0.67 |

  This is not new: K1.3's version is larger, and no check line looks at scores.
- What to change:
  - Register now how the natural set is balanced if the gap exceeds the line. For example, draw kept rows within each
    side so the passage-count distributions match, by a hashed order (as R-200 did), with a fixed rule. Do not choose
    after seeing the result.
  - Add a reported line for top score and top-minus-second, by side, for K1.3 and natural rows.

### 3. The brief copies outside-writer dev material, and line 4 would not catch it

- The brief's example "anya's in winnipeg now right" is outside-writer set 1's confirm question "anya's in winnipeg
  right" with one word added. It shares no four-word run with that question, so line 4 passes it.
- Other brief examples that appear in the dev sets or Demo2:

  | Example | Outside set 1 | Outside set 2 | Demo2 |
  |---|---|---|---|
  | winnipeg | yes | yes | yes |
  | priya | yes | yes | yes |
  | sister-in-law | yes | yes | yes |
  | corolla | yes | yes | no |
  | landlord | yes | yes | no |

- Writers copy brief examples, so natural rows would carry dev names and values into training. That moves the
  outside-writer lines, which are in R-191's pooled dev recall and R-192's pick.
- What to change:
  - Replace every example with names, values and wordings that occur in no dev set, demo or K1.3 row, and check the
    brief itself with line 4's script.
  - Add a single-word check: count natural answers and person names that are dev-set answers or names.

### 4. Writers converge on stock values; four-word runs do not measure this

- 36 of the 143 distinct answers in outside set 2 are also answers in outside set 1 (beagle, civic, shellfish, nurse,
  oaxaca, mcgill and others). Two writer groups with no contact still share about a quarter of their answers.
- Eight more writers of the same kind will most likely share a similar fraction with S3's answers. That gives the
  model value priors ("pup means beagle") and makes check_false look-alike values familiar. Lines 4 and 5 count
  four-word runs and cannot see it.
- What to change:
  - Report, by count only, natural answers that are also dev answers, and run the same count against S3 inside
    `overlap_s3_training.py` (numbers only).
  - Disclose this as an expected optimism on S3. If line 5 or the new count fails, K3 does not train. It must not be
    rewritten to pass, since that would tune training to S3.

### 5. No statement rows: in casual style, almost every final message means "search"

- Estimated kept mix from the simulation: older about 147, check about 185, never_told 128, in_view 64. So about 12%
  of natural rows have no search.
- K1.3 has (222 statement + 150 in_view) of 1,094 rows without a search, 34%.
- Each outside dev set has 40 statement items in casual style. R-054 (fix 7b) lost statements this way ("searches on
  statements of every opening").
- What to change: make statement rows from the writers' own fact and small-talk messages (the 3 messages before as
  view, the message as the last turn, the writer's reply, no search), so natural rows without a search match K1.3's
  share. Add the outside-writer statement line to the screen as reported.

### 6. Risk (b): rows kept only when found

- Nothing new in ratio. K1.3 already has every fact row found (562 of 562), and the only "fact absent" outputs are its
  160 never_told rows. Natural rows keep that pattern: about 332 found fact rows to 128 never_told, 2.6 to 1, against
  K1.3's 3.5 to 1.
- The habit it feeds is real and measured. On the outside writers, K1.3's searches missed the fact 213 times (210
  older, 3 confirm). Its reply named something on 69 of those (66 older, 3 confirm) instead of declining (144).
- The simulated question-word queries miss 68 of 160 older facts (42%) at test, so outputs without the answer will be
  common, and no training row shows a told-fact question whose search missed.
- What to change: the same as finding 1. Keep the dropped older and check rows with a "did not find it" reply. Then
  "the question sounds like a told fact" never implies "the output holds it".

### 7. Chats are shorter than the test chats, and each chat's view repeats

- Natural chats search 15 exchanges (`exchange_0000` to `exchange_0014`). The outside dev chats have 21 to 26
  exchanges, and K1.3's have about 26.
- About 10 facts in 18 messages is denser than either. So natural rows are shorter, with fewer competing passages,
  and can be told apart from K1.3's rows by the doc ids, which never pass 14.
- All rows of one chat share the same 3 viewed exchanges: up to 10 rows, 64 distinct views in all.
- What to change: chats of about 24 messages (searched 1 to 21), facts about a third of messages. Report effective
  size as 64 chats, not 500 rows.

### 8. The check-question mix leans toward agreeing

- Per chat: check_true 2, check_false 1, and one never_told check form. So a stated value means "confirm" in 2 of 4.
  The outside sets are 20 true to 20 false, and R-158 found 6.37 already goes along with 17 to 19 of 20 false claims.
- The never_told check form's value has no rule. It could be a look-alike's in-chat value or a value never said.
- What to change: check_true and check_false 1 to 1 (2 of each per chat if 10 questions stay). Give the never_told
  check form the check_false rule (another person's in-chat value when one exists), at least half.

### 9. Acks

- I found no writer-ack cue to measure, since the files do not exist. What I did find is a strong cue already in
  K1.3, which K3 keeps unchanged: in K1.3's search outputs, all 1,784 fact passages carry one of 6 fixed acks ("Good
  to know.", "Thanks for telling me.", ...). The 328 other passages carry 153 different replies, and no ack is used on
  both.
- A model can find the fact passage by its ack without reading. That cue does not hold in natural chats or S3.
- What to change:
  - Report it as an existing shortcut.
  - In `check_k3`, report fact and non-fact acks in the natural rows: distinct count, mean length, and any reply used
    on both.
  - Consider rewording K1.3's acks from a larger pool. That is a change to K1.3 rows and needs its own check.

### 10. Smaller items

- Lines 2 and 7 hold by construction (`build_k3` filters on them). They only catch code faults. Fine, but say so.
- `build_k3` has no row-token limit. K1.3 used `MAX_ROW_TOKENS`.
- Natural check-form never_told rows reuse K1.3's replies, such as "I don't have that from you. What is it?". That
  reply asks for a value the user just stated.
- The draft quotes 152 of 210; my recount was 162 (r204 report). On confirm, K1.3 searched 70 of 240 outside-writer
  confirm questions. The "120" is the wrong-and-unsearched count.
- No prediction is written in the draft, though it says one is registered first.
- Demo2 reach by category: the brief's list covers only 3 of Demo2's 6 older categories (C02, C17, C10). Under the
  query rule, 2 of those would be kept (Q2, Q3). The draft's motivation from Demo2 should say so.

## The open questions

- **500 rows next to 1,094.** Do not cut K1.3. That would make K3 a change to two things at once, and K1.3 is the
  passing base. The real size is 64 chats, and the kind mix should be fixed (findings 5 and 8) before size is
  discussed.
- **Does keeping only found rows teach a cue?** By ratio, no (finding 6). The selection does make the cue in
  finding 1 (user and split-reference questions fall on the never_told side).
- **Writers' acks.** Not measurable yet. The ack cue that exists is K1.3's (finding 9).
- **Shortcuts that would not hold on S3:**
  - user question means not told (finding 1);
  - fixed acks mark facts (finding 9);
  - casual final message means search (finding 5);
  - a stated value means confirm (finding 8);
  - stock answer values (finding 4).

## What K3 can move, stated plainly

The kept rows teach reading a natural fact line that the search returned because the question shared the person's
name or relation. That is the found-and-wrong loss: 84 of 254 on the outside writers, 77 of 288 on hard_dev, and
Demo2's Q2, Q3 and Q6. It is the right target. With this tool and question-word queries, K3 cannot reach user facts
or split-reference facts whose fact line shares no word with the question. The record should not claim it can.

## Verdict

**Not ready.**
- The keep rule removes the user-fact and split-reference rows (Demo2 Q1, Q4, Q5; 64 of 68 dropped dev questions
  share no content word with the source) and leaves a "user question means not told" cue.
- Line 3 is likely to fail at about 0.40.
- The brief seeds writers with dev-set names and a near-copy of a dev question.

**Ready with changes** once these are registered before any writer runs:
1. Dropped fact rows kept as "did not find it" rows, with kept-by-person and kept-by-reference reported per side.
2. A fixed passage-count balancing rule, and score lines reported.
3. Brief examples replaced and the brief checked, plus single-word answer and name overlap counts against dev (and S3,
   by count).
4. Statement rows at K1.3's no-search share.
5. Check true to false 1 to 1, with the never_told check value rule.
6. Longer chats.
7. A registered prediction.
