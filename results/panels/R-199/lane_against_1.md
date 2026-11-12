# R-199 draft (K1.2, template twin): against lane

Reviewer: claude-opus-5-5, 2026-11-12. Read: the draft, RECORDS R-196 to R-198, results/panels/R-198/lane_against.md,
build_r199.py, check_r199.py, build_r196.py, build_r178.py, check_r196.py, conversations.py (build_item),
recall_tool.py, stress.py (_statement_pattern). Not run: build_r199.py, check_r199.py, any search, any row build.
Data read: k1_r178.jsonl and k1_1_r196.jsonl and their provenance files, with read-only scripts in
`scratchpad/r199/` (`est_roles.py`, `est_roles_cf.py`, `answer_class.py`, `answer_class_cf.py`, `k1_drawn.py`,
`est_best.py`). Every number below is from those two existing sets. They are estimates of K1.2, not K1.2.

## Verdict: do not build as written

The code mostly does what the draft says. I found no fault in the twin or in the text swap. But the set it builds is
very likely to fail check lines 4 and 5 by a wide margin. The cause is not the search. It is which rows can have drawn
wordings at all. 222 found rows (R-102's 170 and the 52 spliced `indirect/` rows) always keep template lines, and no
never_told row is one of them. Under the draft's own fixed rule ("if any line fails, there is no K1.2") the build
would be spent for nothing. The draft's prediction ("answers and decoys each about 75% drawn") ignores this, though
R-198's lane (finding 8) had already reported it. The same fact is also a real new cue that K1 does not have: a
search output with only template wordings means "found" much more often than in K1. Fix the registration first (the
changes are at the end). Whether a fixed K1.2 is worth the time before Saturday 16:00 is Kevin's call.

## Findings

**1. Lines 4 and 5 will most likely FAIL, from the set's make-up (design; blocks the build).**
In K1.2, the returned lines and their order are K1's, and each one is worded as in K1.1's chat. So I estimated K1.2's
role counts from K1's outputs. Each line takes K1.1's wording where K1.1 shows it. A line K1.1 does not show counts as
template in rows that cannot be drawn, and as drawn elsewhere (R-198: the lines K1.1 lost were drawn decoys).
Script: `est_best.py`, which uses `check_r199.roles`'s own rules.

| Role (check_r199 `roles`) | drawable rows | template-only rows | total drawn |
|---|---|---|---|
| answer lines, found rows | 272 drawn of 349 (78%) | 102, all template | 272 of 451 (60.3%) |
| decoys, found rows | 228 drawn of 298 (77%) | 277, all template | 228 of 575 (39.7%) |
| decoys, never_told rows | 197 drawn of 265 (74%) | 12, all template | 197 of 277 (71.1%) |

Estimated z: line 4 6.6 and line 5 -8.6, against |z| < 1.96. I also tried the two extreme guesses: all unseen
lines template (`est_roles_cf.py`) gives 14.4 and -4.8. All unseen lines drawn wherever the row shows a drawn line
gives 6.6 and -8.0. Both lines fail under every guess. Inside the drawable rows the three roles are 74% to 78%. So the
twin does what it is meant to do, and the failure comes only from the template-only rows. Those rows are all found
rows (`older` and `confirm`): R-102 rows keep their own fact lines by K1.1's design (build_r196.py:13-14), and the
spliced rows are kept as they were (build_r178.py:10-11).
Change: decide before the build what to do with the template-only rows. Then re-predict lines 4 and 5 from this
table. Options:
(a) Draw wordings for the fact lines in R-102's rebuilt rows and in the spliced rows too, so every searching row can
be drawn. This changes K1.1's set and needs its own sub-check.
(b) Keep them as template, run lines 4 and 5 on drawable rows only, and gate the all-template cue in finding 2
separately.
Option (b) on its own hides the cue in finding 2, so it is the weaker choice.

**2. A new found/never_told cue that K1 does not have, not disclosed (design).**
In K1 every fact line uses the template, so wording tells nothing. In the estimated K1.2, take the rows whose search
returns same-type lines. In 253 of 562 found rows every returned same-type line is template. In never_told rows it is
19 of 138 (`est_best.py`). So an all-template output roughly triples the odds of "found" over the base rate. At test
time, hard_dev's lines are never in a training wording (line 3 makes sure of that). A model that learned "template
wording means found" would lean toward "not found" there, which means more false declines on the main pick metric.
K1.1 has the same cue from the same rows. K1.2 inherits it, and since never_told rows get their drawn decoys back, it
may well get stronger.
Change: add a gated line: in searching rows, the share of rows whose returned same-type lines are all template,
found against never_told, |z| < 1.96 or a fixed difference. Or remove the cause with option (a). Disclose it either
way.

**3. Line 4's roles are wrong for R-102's correction rows (check code, check_r199.py:90-109).**
`roles` calls a returned line the answer only if its value is in the last reply (line 105). In K1, 110 of 562 found
rows have no returned same-type line whose value is in the reply. The examples are all R-102 rows (`corr_*`,
`corrcue_*`, `asked_*`) (`answer_class.py`). There the answer sits in a correction line ("oh wait i got that wrong
before, ..."). That line fullmatches no pattern, so `match` skips it, and the asked person's old, corrected value
line is counted as a "decoy". This puts about 277 template lines into `found_decoy` that are not decoys of another
person. It also pushes line 4 toward a fail that tells nothing about answer against decoy. One more found row
(older_0061) misses only on case: "fencing" in the line, "Fencing" in the reply. The match is case-sensitive.
Change: classify by person, not by value in the reply. Answer = the asked person's line with the row's answer
value. Old value = the asked person's line with another value, counted on its own and reported. Decoy = another
person. Compare values with casefold.

**4. Fresh never_told rows escape line 1, and their number is not gated (check code, check_r199.py:118-120).**
Line 1 skips any position where either set has a `k1/never_told_*` row. If the twin failed in a way that leaves more
never_told searches with no passages, those rows would be swapped for fresh rows. They would then leave line 1 without
any line failing, because the fresh count is only reported (K1 6, K1.1 15). By construction K1.2's fresh rows should
be K1's six, in the same places and from the same seeds (same `chunk_id=` test on the twin; only the token check
reads drawn text).
Change: gate "fresh never_told ids equal K1's six, in the same positions". Run line 1 on those rows too, against K1's
fresh rows (mapped output equals K1's).

**5. Line 1 cannot see a failed swap back to the chat's wording (check gap).**
`mapped_output` maps every "User:" line of K1.2's output to the template before it compares. So a row whose output
still shows the twin's template text, where the chat had a drawn wording, passes line 1. I found no way for the swap
to fail in the current code. Every passage is "User: X\nAssistant: Y" (recall_tool.py:36), one exchange per passage
(CHUNK_SIZE 400), and the swap matches "User: X\n" exactly (build_r199.py:72). But line 1 is there "to catch a code
fault", and this is the fault it would miss.
Change: add a line. For every passage (`chunk_id`) shown in both K1.1's and K1.2's output of the same row, K1.2's
"User:" line equals K1.1's byte for byte (K1.1 shows the chat's own wording). For every other drawn-capable line, the
mapped text differs from the shown text in at least the drawn share reported.

**6. Line 6b's allowance is loose (check_r199.py:149, 166).**
In K1.2 the search's found decision and the values it returns are K1's. So the forbidden values and every last reply
should be K1's (K1.1 had 0 such rows). The bound "at most the build's scripted-target rows" counts every scripted
target, including K1's own, and allows that many changed replies.
Change: gate rows whose last reply differs at 0, outside line 6a's three rows.

**7. Lines 4 and 5 test for a difference, not for sameness (check design).**
A |z| below 1.96 means only that no difference was found. A small role imbalance would pass and still be learnable.
At these sizes (450 to 575 lines) the test has fair power for a 10-point gap, so this matters less than findings 1 to
3.
Change, optional: add a fixed largest allowed difference (for example 5 points), as R-198's lane suggested, fixed now.

**8. The code checks I could do found nothing wrong (for the record, not a reason to build).**
- `template_line` against `check_r196.mapped`: they agree on every fact line and user turn of K1 and K1.1. No line
  matches two patterns with different templates. K1 holds no drawn-wording line in any row, so the twin of an R-102
  or spliced row is the row itself (`k1_drawn.py`).
- Drawn wordings add no pool person or relation word that the template lacks, and drop none. They hold no value text
  the template lacks. So `add_other_facts`' `said` and `free` lists, and with them F2's choices of people, relations
  and slots, are the same with or without drawing. The twin should be K1's conversation on every path.
- The patch covers every path. `K1.search` is a module global that `rebuilt_turns`, `found_before`, `k1_turns`, the
  F3 re-ask test and `k1_1_fresh_never_told` all look up at call time. `k1_search` keeps the original. R-102's
  rebuild test calls `build_recall_tool` directly and stays K1's. On template rows the twin equals the row, so the
  rebuild and `found_before` are K1's.
- The output swap: one exchange per passage, and the "User: ...\n" form always holds, so the swap is exact.

**9. Smaller points on the draft text (disclosure).**
- "Template lines always match their query": not so. Decoys about other people share only the type's words, and K1
  had 6 never_told rows whose search returned nothing.
- Outputs now show BM25 scores computed on the template text beside drawn text that may share no word with the query.
  A real keyword search cannot return a line that shares no word with the query. Say so in the disclosure that the
  outputs are "richer". I see no found/never_told cue in it beyond K1's, since the scores are K1's.
- The test-time effect of training on these outputs: I found no harm beyond K1's. The queries, the passage counts and
  the found decisions are K1's, so the model learns nothing new about how the search behaves except finding 2's cue.
  The one gap is that the model never sees a real keyword search miss a fact because of its wording. K1 never showed
  that either.
- Predictions: "answers and decoys each about 75% drawn" should read about 60%, 40% and 71% (finding 1). Say they
  were made before this table.

## Changes wanted before the build, in order

1. Decide on the template-only rows (finding 1, option (a) or (b)), and register the choice and its prediction from
   this table.
2. Gate the all-template cue, found against never_told (finding 2).
3. Fix `roles`: classify by person, give old values their own count, compare with casefold (finding 3).
4. Gate the fresh rows: K1's six ids in place, and include them in line 1 (finding 4).
5. Add the K1.1 byte-for-byte check of the shown wording (finding 5).
6. Gate changed last replies at 0 outside the three listed rows (finding 6).
7. Optional: a fixed largest difference for lines 4 and 5 (finding 7). Correct the draft text (finding 9).
