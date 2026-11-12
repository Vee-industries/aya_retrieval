
## R-198 · 2026-11-12 · REOPENED · K1.2, registered before it is built: K1.1 with each row's draw picked by passages

**Decision.** Kevin, 12 November, after R-197: "Try K1.2". Under R-194 (any number of candidates, training done by
Saturday 14 November 16:00 Eastern). Named K1.2 because it is K1.1 with one change aimed at line 3b, the line R-197
reads as a real property of the set. Disclosed: K1.2 is designed after K1.1's check result (a property of the
training set, no model output), after K1's and K2.1's dev results (R-195), and after base's R-191 reruns.

**K1.2** (`scripts/records/build_r198.py`): K1.1's build with one change. Each row of a kind that searches (older,
confirm, never_told) and gets F2 tries up to 8 draws of its added lines' wordings (draw 0 is K1.1's; draw *d* seeds
each line's wording generator with K1.1's seed plus 100 *d*), and takes the first whose search returns at least as
many passages as K1's same row; if none does, the first draw with the most. The choice uses the row's own search only.
The rule is the same for found and never_told rows. It covers the builder rows, R-102's rows, and the fresh
never_told rows (K1.1's seed loop, with the pick at each seed tried). Rows of in_view and statement keep K1.1's draw.
`build_r196.py` gets a draw offset that is 0 by default (27d4c00), so K1.1's own build is unchanged. The build writes
each row's draw, the rows that reached no K1 count, and a count of the F2 fact lines in a template and in a drawn
wording, counted on the conversations as built, before F3 (lines out of view included). Training settings as K1.

**Check before training** (`scripts/records/check_r198.py`), six lines; a FAIL on any one means nothing trains:
1. More than half of the F2 fact lines as built are in a drawn wording. Changed from R-196's 72% to 78% of fact lines
   in view and in search outputs: R-197 showed that count measures the search's choice as well as the draw, and a
   draw that keeps passages must give back some drawn lines. Half is the point at which the template wording stops
   marking most fact lines, the cause R-196 targets.
2. Four-word runs shared with hard_dev forms: 0 (as R-196).
3. never_told rows with passages 160 of 160; found against never_told mean passage gap at most 0.37 (as R-196).
4. Rows unlike K1 beyond wording and last reply: at most 11 (1% of 1,094), each listed. Changed from 0: R-197's three
   rows were F3 choosing a different row, because the wording changed which facts F3 can ask about; the draws here
   change more rows, so more such rows are likely. 11 is my number. Rows whose last reply differs: at most the build's
   now-missed and scripted-target rows (as R-196).
Reported only: the drawn share of search-output fact lines in found and in never_told rows; the draws taken.

**Disclosures.**
- Line 3b is close to a pass by construction: each row is matched to its own K1 count, and K1's gap is 0.23. It stays
  a check, against rows that reach no K1 count.
- The pick favours wordings that share the question's words. Never_told rows depend on their F2 lines for every
  passage, so they are likely to need more redraws than found rows, and their returned lines may be in the template
  wording more often than found rows' lines. That would be a cue of its own (template wording in the output = decline).
  The report line measures it; it is not a gate.
- Picks are measured on each row's F2 conversation; rows that later get F3 may return a different count.
- Lines 1 and 4 are re-registered after K1.1's result.
- A seventh candidate on the same dev questions (R-196's against lane): the pick between K1 and K1.2 is close to the
  noise of one seed (pick sd about 19).

**Fixed in advance.**
- One build. If any line fails, there is no K1.2 and K1 goes on alone.
- Seeds 82 and 83 trained and scored before any K1.2 result is read; `decide_r191.py` with K1.2 added to its
  candidates, every line as R-191. If K1.2 is eligible, seed 94 trains and the pick is R-192's (pooled recall over
  82, 83 and 94).
- S3 once, after the pick: baselines first, the shippable arm at 82, 83 and 94, the others as report arms at 82 and
  83. Ship rule R-178's.
- Training finished by Saturday 14 November 16:00 Eastern (R-194).

**Predictions** (mine, before the build): line 1 about 65% (range 55% to 72%); line 3b about 0.25; line 4a about 5
rows; rows reaching no K1 count about 10. If it trains: hard_dev recall pooled over 82 and 83 about 130 (range 115 to
150; K1 122); T3 copies about 68; T2 false answers about 8.
