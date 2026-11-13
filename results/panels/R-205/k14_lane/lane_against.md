# K1.4 draft: against lane

Date 2026-11-12. Read-only. No model, no GPU, no repo edits, no git. Scripts and outputs are in
`C:/Users/Gaming/scratch/claude/C--Users-Gaming--claude-spares-spare-wcSF8M/3f7d989b-d009-44ac-9f86-64e88058f022/scratchpad/r204_lane/`
(`rebuild_k1.py`, `new_queries.py`, `dev_replay.py`, `evidence.py`, `grounding.py`, `reading.py`, each with a `.out`).

**Verdict: not ready.** Change 1, as written, brings back the never_told failure of fix 7 and 7b (R-050, R-054): 41
of 160 never_told rows get an empty search and the passage gap is 0.91, so the draft's own line (c) fails. Its best
case on the outside writers' older questions is +28 facts found over 6 seed-sets (paired +47 / -19), against the 210
misses it is meant to fix. Change 2 repeats 7 and 7.1 (R-153 to R-158) without citing them. Neither change touches
Demo2's 0 of 6 (R-204). On the outside writers and hard_dev, the loss that training can still reach is reading, and
the draft does not address it.

## How the counts were made

- `rebuild_k1.py` runs build_r178's own steps (builder sources, R-102 rows, F2, F3, the fresh never_told rows) and
  keeps each row's template-wording chat. Of K1's 722 search rows, **669 rebuild with a search output equal to
  k1_r178.jsonl byte for byte**. The other 53 have no chat: the 52 spliced `indirect/older_*` rows (no seed) and
  `corr_0060` (F2 not applied; it keeps 6.37's turns).
- New query, by the draft's rule: `who` (K1's query minus the template suffix; this is `_query`'s choice), then the
  message's R-176 content words (`demo_overlap_r176.STOP`, possessive 's stripped, `who` removed), in order, each
  word once. A second variant also drops `demonstrations.FILLER` (R-042's list). Search: the plain OR keyword search
  (`match_all=False`, top 5) over the row's chat, as K1 decided retrieval.
- Dev replay (`dev_replay.py`): the same search with the question's content words on the outside-writer chats
  (`data/blind_dev`, `data/blind_dev2`, via `load_dev_set`) and on rebuilt hard_dev and probe items, compared with
  K1, K1.3 (seeds 82, 83, 94) and base191 result rows.

## The draft's open questions

### Q1. Does a question-word query still find the fact in the training chats?

Yes, every time, but mostly because of the name or relation, not the question's words.

| 509 found-side rows (older 279, confirm 230) | K1's query | Draft query | FILLER variant |
|---|---|---|---|
| fact in the top 5 | 509 | 509 | 509 |
| fact ranked first | 473 | 422 | 436 |

- In **238 of 509** found rows, no word of the new query except `who` is in the fact line. Every fact line names
  `who` (509 of 509). The training rows therefore never show a question word deciding a search. They show only that
  `who` plus any words finds the fact. On outside writers, a missing `who` or a `who` that does not match is the
  case that matters, and training would still never show it.
- The draft's line (b) ("found share within 5 points of K1.3's") cannot fail: both are 100% by construction.
- Replies stay grounded: in all 509 rows, every value K1's reply names is in the new top 5 (`grounding.py`;
  corrections 109 of 109).

### Q2. Does it create a new cue between found and never_told?

Yes. This is the main fault.

| | K1's query | Draft query | FILLER variant |
|---|---|---|---|
| mean passages, found side | 3.07 | 2.80 | 2.47 |
| mean passages, never_told | 2.74 | 1.89 | 1.54 |
| **gap** (line (c): at most 0.37) | 0.33 | **0.91** | 0.93 |
| **never_told rows with 0 passages** (line (c): none) | 0 of 160 | **41 of 160** | 47 of 160 |
| never_told rows with no same-type line returned | 16 | **91** | |
| found rows with exactly one same-type line | 162 | 256 | |

- The 41 empty rows come from the `same_type` (24) and `shared_word` (17) shares. In those shares the never_told
  person is not in the chat, and the generator's ask forms are written so they share no word with the statements
  ("uncle write" against "uncle novels genre"; "roommate send card" against "street address").
- This is R-050 again. Fix 7 used questions' own words, 77 of its 150 never_told rows came back empty, and never_told
  fell from 48 to 21 with 27 false retrievals. Fix 7b (R-054) kept only never_told rows that returned passages,
  which is what line (c) would force here. It still got never_told 36 of 48 and 13 false retrievals, and was dropped
  with the reading "training searches in the friend's own words teach the model that any line naming a person is a
  lookup". The draft cites neither record.
- The cue does not hold on test sets. With question words, outside-writer never_told searches return 2.85 and 2.75
  passages on average, with 0 empty out of 40 and 40; hard_dev returns 2.94 (5 empty of 48). So at test, never_told
  outputs look like training's found outputs.
- Query length is not a cue (found 3.78 words, never_told 3.68).

### Q3. Do the check forms put dev-set wording into training?

The forms are not written yet, so this cannot be counted. What can be counted:
- The draft was designed from outside-writer confirm questions and quotes them. Their last two words: "right" ends
  about 45 of 80, "isn't he/it/she" or "isnt" 12, "doesn't he" 3, "yeah" 2. A four-word-run check (line (d)) cannot
  see a two-word tag. Outside-writer recall is a line in R-191's pooled dev recall and in R-192's pick, so a
  candidate built to match those sets' tags is favoured in a pick that scores them.
- Line (d) names hard_dev and the check forms only. It should also cover probe forms and both outside-writer sets'
  questions and chats.

### Q4. Shortcuts that would not hold on S3

1. **Passage count and empty results** tell never_told apart (Q2).
2. **"The value I said is in the output, so confirm."** On the outside writers, 20 of 40 confirm questions per set
   state the true value. The other 20 state a false value. In 0 of those 40 false claims is the claimed value
   one of the question's listed `wrong` values, which are values present in the chat (examples: "viola" for cello,
   "iceland" for morocco). I did not check whether each claimed value appears elsewhere in its chat. The draft's "another value of the same type" does not say whether the false value is a value present in
   the chat. If it never is, training teaches "value word matched a returned line, so confirm", and that rule breaks
   whenever a false claim names a look-alike's value. R-153's against case named this slip. Fix: half the
   false-value rows use a same-type value another person holds in the chat, and so do half of the never_told check
   rows.
3. **Meta words in queries.** Under R-176's stop list, the commonest non-name query words would be say 75, tell 72,
   mention 69, told 58, ever 58, said 26, bring 21. Check forms add right, yeah, isn't. The model would learn to copy
   them. They are common in natural chats ("she told me"), where they pull in noise lines. Use FILLER plus the tag
   words, and a cap (R-042 used 4 words).

## Faults, most serious first

1. **Line (c) fails on the draft's own rule: 41 empty never_told rows, gap 0.91, and 91 of 160 never_told outputs
   with no same-type line.** This repeats R-050 and R-054, which the draft does not cite. Fix: either keep K1's
   template queries for never_told and confirm-form rows (but then line (a) and the change's premise go), or show
   first, on non-training rows, a never_told design under question-word queries that returns other people's same-type
   lines at K1's rate. F2's `shared_word` share is no help as built: it adds a line about the old query's last word,
   and only 78 of 221 `shared_word` rows keep that word in the new query. It would have to be rebuilt from the new
   query.
2. **The cause the draft names explains only a small part of the misses.** I recounted R-203's figures on K1.3's
   outside-writer older rows (seeds 82, 83, 94): 480 questions, 170 right, 210 searched and not found (matches), 162
   with a query word in neither the question nor the view (the draft says 152). Only **74** of those 162 words are
   anywhere in the searchable chat. A question-word query would have found the fact in only **36 of the 210**.
   Paired per question: K1.3 found and question words found 235; neither 179; question words only 47; K1.3 only 19.
   That is a net +28 found over 6 seed-sets, about +19 right at K1.3's 67% read rate, and only if the model copied
   the rule perfectly. R-153 had already measured it: "a question-words query finds 42 to 43 of the 80 older facts;
   6.37's own queries find 38 to 43. No room to gain." My replay gives 43 and 51 of 80. Fix: state this ceiling in the
   record before building, and cite R-042, R-050, R-054 and R-153.
3. **Change 2 is 7 and 7.1 again, uncited.** 7 (R-153, R-155) reworded 100 confirm rows into tag claims, 63 true and
   37 false. It failed probe recall at seed 82 (92, needed at least 94) and pooled (189 against 192). 7.1 (R-157,
   R-158) failed probe in_view (38). On the second outside set it searched 40 and 39 of 40 tags and still did not
   raise recall (51 and 52 against 53 and 53): it corrected more false claims (7 and 5 against 3 and 1) and confirmed
   fewer true ones (11 and 13 against 16 and 16). In fairness, one thing really is new: 7.1 kept template queries,
   whose confirm searches missed 20 and 15 of 40, while question-word queries find 40 of 40 and 38 of 40 confirm facts
   on the two outside sets (K1.3 searched 36 and 34 of 120). That is the one combination these sets do not rule out.
   Fix: cite R-153 to R-158, say what differs, and register a prediction on confirm-true kept and confirm-false
   corrected, separately.
4. **K1.3's quota code would silently stop working.** `build_r200.roles()` and `check_r199.roles()` call a returned
   line "asked type" only when `query.endswith(QUERIES[template])`. **634 of 669** new queries do not end with the
   template suffix, so almost every asked-type line would be classed as `*_other_type`. Step 2's (side, n) groups
   empty out, and check lines 4 and 5 would compare nearly empty groups. "K1.3's rewording and quotas applied
   unchanged" therefore does not hold. Fix: classify by the row's asked fact type (from the rebuilt item), and add a
   line asserting the role counts equal K1.3's (answers, found decoys, never_told decoys).
5. **53 search rows cannot be searched again.** The 52 spliced `indirect/older` rows and `corr_0060` have no chat,
   and their queries are template words ("sister keeps animals yard" for "the animals my sister keeps..."), so line
   (a) fails on them. Fix: rebuild them from a seed, or drop them, and say which.
6. **Line (d) is too narrow** (Q3). Add probe forms and both outside-writer sets' questions. Record that the tag
   choice was read off those sets, and keep their weight out of K1.4's pick or report it separately.
7. **The query rule is underspecified.** R-176's stop list keeps meta and tag words (Q4.3), there is no length cap,
   and the possessive and "next door" style relations are not handled. `demonstrations.message_words_query` already
   exists and is tested (R-042). Use it or say why not.
8. **The pick is noise-level anyway.** This would be the eighth candidate on the same dev sets, and the K1.3 lead was
   22 points against a three-seed sd of about 19 (R-203). Any K1.4 gain of the size in fault 2 (+19 right over 6
   seed-sets, where 3 of those 6 are in the pick) is smaller than that sd.

## The new evidence (R-204, Demo2) and what would touch it

What the files show (`results/demo2/branches.json`, `demo2/questions.json`): on the 6 older questions, K1's search
held the source on 6 and K1.3's on 5, and both got 0 right. Per question:
- Q1 "where do i work" (a fact about the user, at the aquarium): declined.
- Q2 "what does dev drive" (the source is "dev's saab broke down"; the query "Dev car auction" found it): declined.
- Q3 dog breed (the line holds both "whippet" and the name "Turnip"): both answered the name, which is training's
  only dog attribute.
- Q4 "where is my sister headed" (the source says "tessa just booked flights to tbilisi", naming Tessa but not as
  sister): found, declined.
- Q5 the ingredient the user avoids (the user, again): found, declined.
- Q6 wedding venue: found; K1 gave another line, K1.3 declined.

**Would the draft's changes touch this?** No. Change 1 changes the query, but finding was not the loss on 5 or 6
of the 6, and K1's Q1 query "where do i work" was already in question words. Change 2 touches confirm questions, and
Demo2's fact questions are all older. Expected effect on Demo2's 0 of 6: none.

**The same loss in the dev counts.** On K1.3's outside-writer older rows where the search found the fact (254 over
6 seed-sets), **84 were still wrong** (43 declined, 41 another line). Right by the number of content words the
question shares with the fact's line: 0 shared, 17 of 30 (57%); 1 shared, 87 of 140 (62%); 2 or more, 66 of 84
(79%). On hard_dev (R-203), found-and-wrong is 77 of 288 (41 declined, 36 other) against 16 not found. Reading a
fact worded unlike the templates is the larger loss there, and the draft does not address it.

**What the training rows lack, counted on K1 and K1.3:**
- 25 fact types and 99 statement wordings in all (3 or 4 per type). **All 99 name both a relation and a person in
  the same line**, and in all 509 found rows the fact line names the asked `who`. Outside writers often give one or
  the other: Tessa is called "sister" in a different message, and Dev has no relation at all.
- **0 fact types about the user.** No training row asks "where do i work". The `_query` and `who` machinery has no
  case for it.
- One attribute per type: dog means its name, city means a move. Demo2's breed, trip and venue are attributes or
  types training does not have, the same shape as hard_dev's hometown loss (R-196: 7 of 26).
- One caveat from the user's own sample: the rough regex finds only about 4 of 240 outside-writer fact questions
  about the user. The case for user facts rests on Demo2's 2 of 6, which is one chat.

**A training-row change that would touch it** (my outline, for the method lane to weigh, not a design):
1. Outside-written statements, as the coordinator suggests: a fresh writer who sees no dev or S3 material writes
   natural statement lines per fact type, many per type. That writer also writes **new attributes of existing types**
   (dog breed beside dog name; a trip beside a move) and **facts about the user** (job, allergy, school, home town),
   each with ask forms in other words. Fact lines naming only the person or only the relation, with the relation
   given in another exchange, should be about half.
2. Keep K1.3's rule that retrieval is decided on a template twin, so passage counts stay K1's and the never_told gap
   does not move (R-199). User facts need a template twin and a `who` rule of their own: a fixed token, or none.
3. Precedent to answer first: fix 8 (R-043, R-051) added 3 wordings per type and did not lower found-but-wrong (7
   against 5). The difference here would be an outside writer, many more wordings, split name and relation, and new
   attributes. Register a prediction on found-and-declined before training.
4. Gates: four-word runs against hard_dev, probe and both outside-writer sets' questions and chats: 0. Role-balanced
   template share (R-200's quotas, with fault 4 fixed). never_told rows must keep other people's same-type lines at
   K1's rate.

That change targets the 84 found-and-wrong outside-writer rows, the 77 on hard_dev, and Demo2's pattern. Change 1
targets about 28 found.

## Verdict

**Not ready.** Line (c) fails on the draft's own rule (41 empty never_told rows, gap 0.91). This is the fix 7 and 7b
failure, and neither record is cited. Change 1's best case is +28 found over 6 seed-sets against 210 misses.
Change 2 is 7.1 again, and its one new element (question-word confirm searches find 78 of 80) is not separated out
or predicted. The K1.3 quota code would not classify roles under the new queries. 53 rows cannot be searched again.
Neither change touches the reading loss that Demo2, hard_dev (77 found and wrong) and the outside writers (84 found
and wrong) show. If one piece is kept, the defensible one is the confirm half on its own: question-word queries for
confirm rows only, with check forms that use in-chat look-alike values, and never_told kept on K1's queries. It
needs its own panel and a registered prediction. The reading change above is the larger target.
