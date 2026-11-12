# R-199 against lane (b), 2026-11-12

Nothing in the repo was run or changed. build_r199/check_r199 not run; no K1.2 set or statistics. Tests: scratchpad t199a-e.py (reworded() on single lines, mapping round trip, K1-only scans).

## Verdict: go with changes. Change 1 is required. Without it, the check cannot see the main source of the old cue.

## 1. Correction lines stay in template wording, and the check cannot see them (REQUIRED)
- build_r199.reworded uses `pattern.fullmatch`. R-102 correction lines wrap the template statement:
  "apparently my roommate Ivan rides a Kawasaki to work (i said it wrong last time)",
  "oh wait i got that wrong before, so Dana (my sister) keeps chickens in the yard".
  In K1 there are 140 such search-output lines: 110 in corr_* rows and 30 in corrcue_* rows. All 140 rows are older/confirm, so all are on the found side. Every one is left in the template wording.
- The stale line in the same row ("...rides a Yamaha to work") fullmatches, so it is drawn and is not in the template wording about 3 times in 4. In those 140 rows the answer is therefore always the line in template phrasing. That is the R-102 half of the cue the previous lane found, now limited to the answer line.
- Rough size, from the design and not measured on K1.2: 140 of 562 found search rows (25%). The template-phrase rate of answer lines rises from about 25% to about 44%, against about 25% for decoys. That is well over the 5-point bound.
- check_r199 cannot see it. `match()` also uses fullmatch, so these lines drop out of `roles()`. They are not counted in line 4 or line 5, and line 1 passes them unchanged. Lines 4 and 5 pass while the cue remains.
- Fix: in build, find the fact with `pattern.search` and replace only the matched span, seeding the draw on the matched span. In check, make `match`/`mapped` use search on the same span, so that correction lines map back for line 1 and count in lines 4 and 5. Then add a line: fact spans found by `search` but not by `fullmatch` and still in template wording = 0. The K1 scan found no other partial matches (no trailing punctuation, no capitalised variants, and no fact text in Assistant lines or assistant turns).

## 2. Replies that copy template wording (minor, recommended)
- 33 K1 assistant replies share a 4-word run with a template statement: 25 final replies in older rows and 8 in in_view rows. Some copy the user line verbatim:
  older_0007 "Talked to Omar today, my aunt, who plays bass in Night Bus."
  older_0000 "It sounds like your neighbour, Omar, keeps tortoises in the yard."
  After rewording, the line is often not in the context, so these rows teach the model to output text it was never shown. They are found side only and on the output side, so this is not an input cue.
- Fix: apply the same span rewording to those replies, or switch them to the template's `answer` form. Line 1 then needs to allow it.

## 3. Mapping (checked, clean)
- All 11,760 template lines (25 types x 8 relations x 10 people x 6 values) were tested in every wording. check.match maps each one back to its own template and fields, and reworded() round-trips, with no errors. No drawn wording fullmatches another type's pattern.
- K1 has no lines already in a MORE wording.
- Every search row's query ends with a template query (older 332, confirm 230, never_told 160), so the asked-type filter drops no rows.
- Line 1's "one wording per fact in a row" always passes, because the draw is seeded per line. It cannot fail.

## 4. Check design faults (fix or note)
- Line 5 mixes up wording with the number of lines. P(all template) = p^n, with p about 1/4 and n = asked-type lines returned. found and never_told differ in n (gap up to 0.37 is allowed), so line 5 can FAIL with no cue at all, or a cue in n can hide one in wording. Compare within equal n (strata by n), or compare line-level shares only.
- The asked test counts any line that shares the relation word as "asked". In found rows, other people with the same relation become asked_other, which no line compares. Not a hole while the draw stays per line, but asked_other should go into the line 4 comparison, or at least the report.
- z statistics treat every occurrence as independent, but the draw is per distinct line and lines repeat across rows. The z values overstate precision. They are reported only.

## 5. New cues
- Apart from item 1: the wording depends only on the line text, so it is independent of role, of found or never_told, and of the row source. No new cue between answer and decoy.
- Known side effect, not a cue: passages in a drawn wording often do not contain the query's words but keep the template-based scores. This is the same for every role. Training rows teach that the search can return lines that do not share the query's words, which the eval's plain keyword search never does.
