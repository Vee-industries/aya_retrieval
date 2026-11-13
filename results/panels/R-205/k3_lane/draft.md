# K3 draft (for the against lane; not registered)

**Evidence.** R-203 (dev counts) and R-204 (Demo2): K1 and K1.3 find the fact and do not read it when it is worded
unlike the templates (Demo2: source in the search output on 6 and 5 of 6 older questions, 0 of 6 recalled); queries
carry template words that are in no message (152 of 210 misses on outside-writer sets); check questions ("anya's in
winnipeg right") get no search (120 of 240 confirm questions); training has no facts about the speaker, and Demo2's
misses include "where do i work" and "which ingredient i should stay away from".

**Cause.** Every training fact is one of 4 wordings per type (template plus `build_r196.WORDINGS`), always about
"my {relation} {person}"; every query is the template's own words; no question states a value to check.

**K3 = K1.3's 1,094 rows plus about 500 natural rows**, built from chats written by fresh writer agents.

Writers (8 fresh agents, each with only the brief, Write as the one tool besides reading the brief; transcripts
audited; barred from the training data, dev sets, both demos, S3 and these records):
- Each writes 8 chats. A chat is 18 user messages with a short assistant reply to each, in casual chat style
  (mostly lower case, short, typos allowed), facts in passing; at least 5 people besides the user, one look-alike
  pair; at least a third of the facts about the user.
- Categories: list I only (the training categories, C01 to C40 as in the Demo2 brief), so S3's outside-training
  categories stay untrained.
- 10 questions per chat, all asked after message 18: 4 older (fact in messages 1 to 15), 2 check-true (states the
  right value and asks), 1 check-false (states a wrong value of the same category), 2 never-told (person and
  category never stated together; a category that comes up for other people), 1 in-view (messages 16 to 18).
- For every question except in-view: the query a good assistant would type, using only words in the question.
- For older and check: the reply a good assistant gives after finding the fact (states the stored value; corrects a
  wrong value). For in-view: the reply from what is in view.

Build (`scripts/records/build_k3.py`):
- Each question becomes one row: the 3 exchanges in view (messages 16 to 18), the question, then for a searching kind
  the tool call with the writer's query, the real keyword search (`build_search_tool`, OR, top 5) over exchanges 1 to
  15, and the reply. Rows look exactly like K1.3's.
- Older and check rows are kept only if the search output holds the source message; the writer's reply is used.
- Never-told rows are kept only if the search returns at least one passage (R-020); reply from K1's never-told
  replies, drawn by hash.
- In-view rows have no search.
- K1.3's rows unchanged.

Check before training (`scripts/records/check_k3.py`; a FAIL on any line means K3 does not train):
1. Every query word is in its question (casefolded): all rows.
2. Older and check rows: source in output, all; never_told rows with passages: all.
3. Passage gap, found against never_told, natural rows alone and the whole set: at most 0.37.
4. Four-word runs shared by natural rows' messages or questions and hard_dev forms, the outside-writer dev sets'
   chats and questions, Demo2's chat and questions: 0 (scripted, counts only).
5. S3 overlap: `scripts/records/overlap_s3_training.py` (counts only), 0 four-word runs with S3 messages.
6. Facts about the user at least a third of natural fact rows; check-false at least 10% of natural rows.
7. Every natural row's reply for older and check holds the source message's value (casefolded).

Disclosures to write: S3's speaker items and template-free queries are no longer untrained (R-178 said measured,
not trained); the natural rows are written by the same kind of agent as the outside-writer dev sets and S3, so dev
numbers on those sets get more optimistic and S3 is the measure; a candidate designed after Demo2's result.

Open questions for the lane: is 500 rows next to 1,094 enough, or should K1.3's rows be cut; does keeping only
found older rows teach a cue (natural fact rows always found, never-told rows always unfound by construction, so
nothing new?); do the writers' acks create a cue; anything a model could use as a shortcut that would not hold on S3.

## Changes after the K1.4 against lane (r204_lane_against.md)

K1.4 is dropped (not ready: change 1 empties 41 of 160 never_told searches, gap 0.33 to 0.91, the R-050/R-054
failure; change 2 repeats 7 and 7.1, R-153 to R-158; neither reaches Demo2's loss). K3 keeps K1.3's 1,094 rows exactly
as they are (no query rewrite on them, so `build_r200`'s role code is untouched) and adds natural rows only. In the
natural rows:
- The main target is reading, not finding: the lane counts 84 of K1.3's 254 found older facts wrong on the outside
  writers (right falls from 79% to 57% as the words shared by question and fact line fall to none), and 77 of 288
  found and wrong on hard_dev. Natural rows give: wordings by an outside writer, lines that name only the person or
  only the relation (about half), more than one attribute per category (a dog's name and its breed), facts about the
  user. Fix 8 (R-051) added three wordings per type and did not lower found-and-wrong, so a prediction is registered
  first.
- Queries: question words only, with filler words removed (say, tell, told, mention, remember, again, know, think,
  what, where, which, who, does, did, is, the stop list of R-176), 1 to 4 words. Never_told rows kept only with at
  least one passage; line 3 caps the gap. The lane measured question-word searches on outside-writer never_told
  questions at 2.85 and 2.75 passages with no empty result, so passages stay uninformative at test.
- check_false: when the chat has a same-category value for another person (the look-alike pair), the false value is
  that value, so "the value I said is in the output" does not mean "confirm". At least half of check_false rows.
- Line 4 also covers probe's and both outside-writer sets' questions.
- The case for facts about the user is thin on the dev sets (about 4 of 240 outside-writer questions) and rests on
  Demo2 (2 of 6) and S3's brief; disclosed.
