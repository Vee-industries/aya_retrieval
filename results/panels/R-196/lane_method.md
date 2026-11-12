# R-196 method lane (claude-opus-5-5; read limits kept; read-only Python)

"Overlap" = content words shared by the question and the fact's line, without names, relations, values, function
words and the endings -s, -es, -ed, -ing. Exact-word figures in brackets.

**1. hard_dev: the declines sit in low-overlap items, but overlap and fact type cannot be told apart.**
Rebuilt with `rebuild_eval_item` from `hd_{k1_r178,fix17cs37,k2_1_r187}_{82,83}_seed_73157.json`. Of 96 older
plus confirm items a seed, 32 have overlap 0. Right at overlap 0: K1 11 and 12, 6.37 26 and 27 (seeds 82, 83). Right
at overlap 1 or more (64): K1 46 and 53, 6.37 47 and 63.
Items 6.37 gets right that K1 found and declined (reply names no hard_dev value): 20 at 82, 23 at 83; 30 of these
43 are at overlap 0, against 32 of 96 overall. (Brief: 17 declined plus 3 other wrong at 82;
same total.)
Limit: each hard_dev type has one statement and fixed question forms, so overlap is a property of the type. The
zero-overlap types [exact] are hometown, interview_day, gift. Hometown: 6.37 24 right of 26 pooled, K1 7. On 15 of
the 18 hometown items K1 lost to a decline, its query shares words with TRAIN's `birth` query; TRAIN's birth fact is
"born in {month}", the passage says "grew up in Lyon". K1 sent 6.37's exact query on 11 of 20 and 12 of 23.
K2.1 (same_person never_told rows 53 to 27, R-190) lost as many to declines: 20 and 26. Halving that share did not move it.

**2. Training: other-words questions are common, also beside same-person passages; few are spliced.**
`fix17cs37.jsonl` and `k1_r178.jsonl` each have 562 found rows (older plus confirm).
- Overlap 0: 216 of 562 [260], above hard_dev's 32 of 96.
- K1 found rows whose passages include another-type fact about the asked person: 132, of which 60 [72] at
  overlap 0. 6.37: 0. (K1's tally: 170 same_person found rows; the rest miss the top 5
  or my value match.)
- Spliced: 124 = 52 `indirect/` older, 57 `facts/` and 15 `contrast/` statement rows. Overlap-0 found rows among
  them: 18 [23] of 216; the other 198 are rebuilt and get F2.
So A asks for rows K1 already has (60), and B's premise fails (18 of 216).

**3. The builder varies the question, never the fact's own line.**
- Questions: `ASK_FORMS` plus `confirm` and 75 `MORE_INDIRECT` forms (on in 6.37's builds). 6.37's found rows:
  confirm 230, indirect 137, new_words 102, same_words 93, all TRAIN forms.
- Fact lines in search outputs (older, confirm, never_told): 6.37 1,447 of 1,447 in the type's one template (120
  behind an R-102 correction prefix); K1 1,784 of 1,784. In a `MORE_STATEMENTS` wording: 0 in both.
- hard_dev forms not reused: four-word runs shared by hard_dev's 40 forms and the 275 training wordings (TRAIN
  fields, `MORE_INDIRECT`, `MORE_STATEMENTS`), placeholders removed: 2, "the name of the" (TRAIN dog same_words)
  and "the whole house is" (a `MORE_STATEMENTS` paint line; hard_dev interview_day statement). "came of age": 0.

**Reading.** In 6.37 a passage naming the asked person always meant answer (R-185). K1's same_person never_told rows
add a type check, and in training the type can be read off the line's fixed wording; a hard_dev line in new wording
fails it. Not proven: type and wording are one variable in hard_dev.

**Design: K1.1 = K1 with each F2 chat's fact lines worded by a draw.** `scripts/records/build_r196.py`, loading
`build_r178.py` as `build_r185.py` does:
1. `builder_item` and `fresh_never_told` pass `more_statements=True` only when a share is given, so the rebuild of
   6.37's rows and `found_before` stay K1's.
2. `conversations.add_other_facts` replaced by a copy whose one change is each added line's wording, drawn from the
   template's own and its `MORE_STATEMENTS` by `random.Random(seed + 8 + index)`.
3. The "whole house" paint line is left out of the draw.
R-102 rows keep their own fact lines; only their F2 lines change. Everything else is K1's; 1,094 rows. Training as K1; seeds 82, 83, 94.

**Check before training** (`check_r196.py`, no model, one build; a stop line fails, nothing trains):
1. Fact lines in the 800 builder rows' outputs and views in a `MORE_STATEMENTS` wording: 72% to 78%. The draw gives
   3 in 4 (2 in 3 for paint); about 3 standard deviations at roughly 1,500 lines, count printed. K1: 0.
2. Four-word runs shared with hard_dev forms, over the wordings drawn: 0.
3. never_told with passages 160 of 160; found against never_told mean passage gap at most 0.37 (R-185).
4. Every non-tool turn equal to K1's once each wording is mapped back to its template, except rows the tally names
   now-missed or scripted target.
5. Reported only: found rows (K1 562), now-missed (K1 0), never_told naming the asked person (K1 53).

**Predictions** (before any build): hard_dev recall pooled 135 (118 to 155; K1 122, 6.37 163); hometown stays low,
about 9 of 26, as no training wording says "grew up"; T3 copies about 68 (line 184); T2 false answers about 8 (line
26). Main risk, probe statement: fix 8 (`--more-statements`, fix 6 data, rank 32) scored 40 of 48 with 3 false
retrievals and was dropped (R-051); the line is 44.

**Do not build if** the check fails; the panel reads R-051 as a measured fail of this change (6.37 has `--more-chat`,
fix 8 did not, so I do not); or three seeds (about 5.4 card hours) cannot finish by Saturday 16:00 Eastern.
Disclose: designed from K1's and K2.1's hard_dev rows.
