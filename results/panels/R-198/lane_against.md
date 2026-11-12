# R-198 draft (K1.2): against lane

Reviewer: claude-opus-5-5, 2026-11-12. Read: the draft, RECORDS R-185 to R-197, build_r198.py, check_r198.py,
build_r196.py, check_r196.py, build_r178.py, build_r187.py, check_r185.py, conversations.py, recall_tool.py,
results/panels/R-196/. Not run: build_r198.py, check_r198.py, any search. Data read: k1_r178.jsonl and
k1_1_r196.jsonl and their provenance files only, with three read-only scripts in the scratchpad
(`r198_mech.py`, `r198_deficit.py`, `r198_cue.py`). Every number below is from K1's or K1.1's existing sets.

## Verdict: do not build as written

The redraw changes the wrong lines. In K1.1 all of the lost passages are same-type lines (decoys) that the
builder writes. The redraw changes only F2's added lines, and in the existing sets those are returned because they
name the asked person, whatever their wording. From K1.1's data the pick can lift very few of the rows that need it,
so line 3b most likely fails again (finding 1). The two re-registered lines (1 and 4) would pass K1.1's own set
unchanged, so they check nothing (findings 2 and 3). If a K1.2 is still wanted, it needs a new design and a new
registration (the end of this file), not this build. Otherwise K1 goes on alone, as the draft's fixed rule already
says for a fail.

## Findings

**1. The redraw cannot reach the lines that lost the passages (design; blocks the build).**
`build_r196.py:142-143` is the only place `DRAW_OFFSET` is used: the wording of F2's added lines in
`k1_1_add_other_facts`. The builder's own lines (answer, decoy, extra decoys) take their wording from
`phraser = random.Random(seed + 3)` inside `conversations.build_item` (`conversations.py:128-158`), which no
draw changes. Search-output lines in rows with the same id, K1 against K1.1 (`r198_mech.py`, `r198_cue.py`):

| Returned fact lines | found K1 | found K1.1 | never_told K1 | never_told K1.1 |
|---|---|---|---|---|
| same type, the asked person (answer line) | 562 | 562 | 0 | 0 |
| same type, another person (decoys, builder lines) | 464 | 346 | 287 | 188 |
| other type, the asked person (F2, same_person) | 250 | 250 | 77 | 80 |
| other type, another person (F2, the other shares) | 2 | 1 | 2 | 4 |

All of K1.1's loss is in decoys (found -118, never_told -99). F2 lines are returned when they name the asked person
(every wording holds `{relation}` and `{person}`, and the query holds one of them). F2 lines about other people are
returned almost never in either wording (4 in K1, 5 in K1.1, over 706 rows). So changing F2 wordings almost never
changes a row's count. In K1.1, 61 of 144 never_told rows and 104 of 562 found rows fall short of K1's count
(`r198_deficit.py`). In K1.1 an F2 wording change gained about 5 passages over the whole set, so 7 more draws a
row might lift a few rows, not 165. My estimate, from K1.1's data and not from any build: well over 100 rows reach
no K1 count (the draft predicts about 10), K1.2's set is K1.1's set with a handful of rows changed, and the gap stays
near K1.1's 0.57. Line 3b fails.
The draft also says "Line 3b is close to a pass by construction". That holds only where a redraw can reach K1's
count, and the data show it almost never can.
Change: do not build this design. A design that targets line 3b has to redraw the decoy lines (see the end).

**2. Line 1 cannot fail, and it cannot see the risk the draft names (check design).**
- With a draw rate of 3 in 4 (2 in 3 for paint), F2 lines as built at draw 0 are 74.7% drawn on average over the 25
  TRAIN types. K1.1's own set would pass ">50% of F2 fact lines as built". Given finding 1, K1.2 would show about
  the same.
- It pools every kind. In_view and statement rows (300 of about 970 F2 rows in K1's tally) are never redrawn, so
  they hold their lines at about 75%. Never_told rows (160) could fall to 0% drawn and the pooled share would still be
  about 62%. The draft's own disclosure (never_told outputs going back to template wording) is the case this line
  cannot catch.
- R-196's line 1 counted the builder's lines and the F2 lines in view and in outputs. This line counts F2 lines only,
  in the conversation as built. It is a different statistic, not a recalibration of the old one, and it was chosen
  after K1.1 failed the old one at 59.1%. "Half" has no source; the draft gives a reason, but not one from data.
Change: gate the drawn share for found rows and for never_told rows separately, over the search kinds only, and gate
the difference between them (for example, never_told at most 5 points below found, the number fixed now). Keep the
pooled number as a report line.

**3. Line 4 (at most 11) would pass K1.1, and it does not check what kind of difference it lets through (check design).**
K1.1 has 3 such rows (R-197). Draw 0 gives K1.1's row, so those 3 come back in K1.2 unless a redraw moves them.
11 is "my number". The allowance is justified by F3 picking a different row, but `check_r198.py:85-96` counts any
mapped turn that differs: a changed message, a changed fact line in view, or a changed earlier answer all pass up
to 11.
Change: each row counted by line 4 must differ from K1 only in the view exchanges that F3 writes, and the row's
question and last user message must equal K1's. Any other difference FAILs, whatever the count. Then the bound can
be the number of F3 moves, listed, with no fixed 11.

**4. The pick does not look at whether the fact is still found; line 4b's allowance grows with the harm (code).**
`pick` (`build_r198.py:84-97`) compares counts only. When a redraw takes a row from 4 matches to 6, the top 5 can
drop the answer passage, and `k1_turns` then gives the row a "not found" target (`build_r178.py:238-240`). Line 4b
allows last-reply changes up to the build's own now-missed plus scripted-target counts (`check_r198.py:97`). So every
row the pick turns into now-missed raises its own allowance. This is rare (count must be at the cap), but nothing
checks for it.
Change: a draw qualifies only if `search_finds_fact` gives the same answer as K1's row. Gate now-missed at 0 (K1 0,
K1.1 0).

**5. Fresh never_told rows: the K1 count at a seed K1 skipped is 0 (code).**
`k1_2_fresh_never_told` (`build_r198.py:157`) sets the target to K1's count at the same seed. At every seed K1
skipped for having no passages, the target is 0. Draw 0 is taken there without trying the others, and the row is
recorded as having reached K1's count (`reached[row_id] = True`). So "rows that reached no K1 count" leaves these
rows out. The draft's "each row is matched to its own K1 count" does not hold for them. Line 4 skips every fresh row
(`check_r198.py:87`), and no line bounds how many there are (K1 6, K1.1 15).
Change: record a target of 0 as "no K1 count", not as reached. Report the number of fresh rows and gate it (for
example, at most K1.1's 15, fixed now).

**6. The line count is by equality, not by wording, and counts rows that are not in the set (code).**
- `build_r198.py:99-101` labels an F2 slot "drawn" whenever the K1.2 slot differs from K1's in any way. A different
  slot, person, relation or acknowledgement would count as a drawn wording. R-197's 4a suggests these stay equal,
  but nothing checks it.
- Lines are counted for a never_told row that is then replaced by a fresh row (counted again), and for rows that end
  as `f2_not_applied`. Those lines are not in the set.
- `check_r198.py:69-70` takes the count from the build's own provenance and recounts nothing.
Change: classify each counted line with `check_r196.wording` and require its mapped template line to equal K1's
(stop the build otherwise). Count only rows kept in the final set. In the check, recount the lines that are visible
(view and outputs) per side and report the result beside the build's count.

**7. A cause from R-185 is no longer reported (check).**
check_r196 reported never_told rows whose output names the asked person (K1 53, R-185's cause). check_r198 dropped it.
Change: report it (`R196.CHECK.stats(k12)["asked_person"]`, K1 53).

**8. Two of the draft's disclosures are wrong or point at the wrong line (disclosure).**
- "Never_told rows depend on their F2 lines for every passage": false. Never_told rows always have 1 to 3 decoys
  (`run_build_training_set.py` `DECOY_CHOICES[NEVER_TOLD] = (1, 2, 3)`). In K1, decoys are 287 of the 366 fact lines
  returned in never_told rows. Of the 79 F2 lines, 77 name the asked person.
- "Template wording in the output = decline" as the cue to watch: in K1.1, F2 lines in outputs are drawn at about the
  draw rate (found 201 of 251, never_told 64 of 84). The wording split that differs by role is on same-type lines:
  answer lines 273 of 562 drawn (49%), decoys in found rows 110 of 346 (32%), decoys in never_told rows 94 of 188
  (50%). (Answer lines are drawn less than 75% of the time because R-102 rows and spliced rows keep template lines.)
  That split exists now and is not touched by this pick. Any design that does redraw decoys will move it.
- R-197's reading ("a never_told row's other facts in drawn wordings share fewer words with the query") needs a
  correction note: the lines that lost passages are same-type decoys, not other facts.
Change: correct both bullets and add the table from finding 1 to the record.

**9. The predictions do not follow from the data (disclosure).**
Line 1 about 65%: by finding 2 it should be about 74% to 75%. Line 3b about 0.25 and about 10 rows reaching no K1
count: by finding 1 the gap should be near 0.57, with over 100 such rows. Predictions are the author's to make, but
the record should say they were made without the table in finding 1.

**10. Smaller code points (none crashes).**
- Draw generators are shared across rows. Draw *d* of a row with seed *s* uses `Random(s + 8 + i + 100d)`, which is
  draw 0 of a row with seed *s* + 100*d*. Builder seeds are consecutive (`build_seed + offset + attempt`), so this
  happens. It is harmless to the pick, but the draws are not independent across rows. Note it.
- `index_path()` reads `--index` from `sys.argv` by position. `--index=PATH`, which argparse accepts, would raise
  ValueError. Use the parsed argument.
- `rows_not_reaching_k1` can list a row that was later replaced by a fresh row, or kept as it was.

**What I traced and found correct.** All four monkeypatches work: `main`, `builder_item`, `f2_item`,
`find_builder_sources` and `rebuilt_turns` look up `builder_item`, `build_item`, `with_r102_change` and
`fresh_never_told` as module globals of build_r178 at call time. `conversations.build_item` looks up
`add_other_facts` the same way. Draw None gives K1's row: K1's `builder_item` (more_statements False) with
`K11.WORDINGS = {}`, and the copied `k1_1_add_other_facts` uses `rng` exactly as the original does. Draw 0 gives
K1.1's row (`DRAW_OFFSET` 0, `WORDINGS` restored, `k1_1_builder_item`). The R-102 path stores its arguments under
`plain.item_id` immediately before `with_r102_change` reads them, and the keyword calls match the
`(item_id, *args, other_facts=None, **kwargs)` signature. No search runs on a kind with no search (the kind is checked
before `passages`), so a query of None never reaches the search. The three-way strict zips have equal lengths,
because F2 only overwrites slots. Each search rebuilds its database (`recall_tool.py:30`), so one draw's index cannot
leak into another.

## If a K1.2 is still wanted: what a new registration needs

1. The redraw covers the builder's same-type lines (decoy and extra decoys), each line from its own generator, not
   the shared `phraser`. The answer line keeps K1.1's wording, so no found row's answer is picked by count.
   This means copying `conversations.build_item` the way R-196 copied `add_other_facts`. Before building, test it on
   a handful of rows that are not training rows (not on K1.2's rows) to show that it moves counts.
2. Decoys come back when they share the query's type words, which mostly means the template wording. So the new
   pick will push returned decoys toward template while answer lines stay about half drawn. Gate the drawn share of
   returned decoys against returned answer lines, and decoys in found rows against decoys in never_told rows, each
   within a bound fixed now. Otherwise "a same-type line in a drawn wording is the answer" becomes the new cue, and on
   hard_dev, where every line is in new wording, it would show up as false retrieval.
3. Findings 2 to 7 applied: per-side drawn shares, F3-only differences for line 4, found status in the pick, a
   now-missed gate, a fresh-row gate, a wording-based count, and the asked-person report line.
4. A fresh against lane on that version before it is built.
