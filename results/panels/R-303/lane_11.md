# Lane 11: Graphic designer
Verdict: submit as is (the round-3 problems are fixed; six MINOR points remain, none blocks)

Opened all 8 PNGs at commit 125b902 (sizes match `figsize` x 200 dpi, so none is stale), read every function in `scripts/make_figures.py` and every caption. Did not run the script. Contrast ratios against `#fcfcfb`, computed: BASE_C 4.98, TUNED_C 6.46, SEED_C 2.96, C1_C 4.0, REPORT_C 5.89, MUTED 3.5.

## Round-3 findings: status
F1 (colour changes meaning) partly fixed: base grey, 6.37 blue, C1 orange, report arms purple in Figures 1-7; Figure 8 still reuses blue and orange for outcomes (new F1 below).
F2 (dot edge cuts interval) fixed: edge 0.8 pt plus end ticks; 0% rows show their ticks.
F3 (Figure 1 subtitle, divider, n per row) fixed.
F4 (contrast) fixed: BASE_C darkened, x ticks INK_2.
F5 (s3_faults size) fixed: 8.4 in, 10 pt, x-limits changed.
F6 (Figure 8 estimate marker) fixed: dot at the estimate.
F7 (report-arm names) partly fixed: Figure 6 caption now says seeds 82 and 83; the faults figure's own subtitle still says "report arms two" (F5 below).
F8 (Figure 2 no intervals) fixed by disclosure: subtitle says "point counts, no intervals".
F9 (Figure 4 title, gate label) fixed.
F10 (Figure 3 grey bar, alt text) partly fixed: x-label says "(red)"; alt text still equals the title.

## New findings (most severe first)
F1. [MINOR] `make_figures.py` lines 60-65 (Figure 8): "Right" is 6.37's blue, "Searched, fact not found" is C1's orange, while the rows are arms. The C1 row shows a blue bar, the 6.37 row an orange one; the comment on lines 45-47 promises one colour per model.
    Fix: draw outcomes from a hue family used for no model (for example teal, ochre, light grey, grey).
F2. [MINOR] `fig_s3_faults` line 430: "its false answers stay above base's" is a point comparison (7.2% against 5.9%, the rule's wording), but the figure shows C1's interval inside base's band.
    Fix: "...; its false-answer rate (7.2%) is above base's (5.9%)".
F3. [MINOR] `fig_s3_faults` lines 420-423: the panels use different x scales (left ends near 35%, right near 60%; 10 points are about 4 times longer on the left), so equal-looking intervals are not equal.
    Fix: one shared limit (`sharex=True`, xlim -3 to 62).
F4. [MINOR] `HF_ARTICLE.md` lines 98, 153, 168: alt text is the figure's title only ("Recall out of view", "S3 faults").
    Fix: one sentence with the finding, e.g. "Recall 11-27% untrained, 87-90% trained on the sealed sets, 40-43% on outside chats".
F5. [MINOR] `fig_s3_faults` line 434: "report arms two" does not say two what; "(report)" is never defined inside Figures 3 and 8 (Figure 8's caption points to Figure 5).
    Fix: "report arms pool two seeds" and put "report = K1, K1.3, K2.1" in the subtitle.
F6. [MINOR] Figure widths differ (8, 8.4, 8.6, 9 in): at one display width, Figure 4's 10 pt text is 11% smaller than Figure 1's.
    Fix: `figsize` width 8.4 in `fig_s3_misses` (line 449) and `fig_never_told_slide` (line 498).

## What holds up
No clipped or overlapping text in any figure; every figure states its interval type; counts in Figures 3 and 6 match the tables (195/894, 5/894, 59/414, 364/1242). Dark blue, orange, purple and grey separate by lightness for red-green colour blindness.
