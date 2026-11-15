# Lane 11: Graphic designer
Verdict: submit after fixes (no figure is wrong; the colour code changes meaning between figures, and the short paper's three figures lack a legend-level explanation of what they show)

Opened all 8 PNGs, read every function in `scripts/make_figures.py`, read every caption. Did not run the script. Numbers spot-checked against the text: 195/894, 5/894, 59/414, 364/1242 and OP 48 / C1 46 / C2 43 of 48 match.

## New findings (most severe first)
F1. [MAJOR] `make_figures.py` lines 51-53, 283-284, 378-382: the same two blues change meaning. Light blue (BASE_C) is "Tiny Aya, untrained" in Figures 1, 2; "6.37, shipped" in Figures 5, 6; "Training on top" in Figure 7; "answered wrong" in Figure 8. Dark blue is 6.37 in Figures 1, 2, "C1" in 5, 6 and "Right" in 8. Base is blue in Figure 1 and grey in Figures 5, 6. A reader moving from the short paper's Figure 1 to Figure 5 reads 6.37 as the untrained model.
    Fix: keep one colour a model across all figures. Give 6.37 its own hue (TUNED_C) in `ARM_COLOURS` and keep the untrained base grey in both families; give Figure 8 its own outcome palette (not blue).
F2. [MAJOR] `arm_points` lines 314-315 (Figure 5, short paper): the dot's 2 pt background-colour edge cuts the interval line, so narrow intervals (Base tool 11/298, K1 1/596, K2.1) show as dashes and the 0% rows show no visible interval.
    Fix: `linewidth=0.8` on the scatter edge, or draw the line at `zorder=4`.
F3. [MAJOR] `fig_recall_out_of_view` line 216-217 (short paper Figure 1): "sealed run R-163, both pools generator-built" reads as if it covers the outside-writer sets (which are not). The figure puts 22% to 40% rows and 27% to 87% rows on one axis with no divider, and gives no item count n per row.
    Fix: reword the subtitle to "sealed run R-163 (both pools generator-built)"; add a thin separator between rows 2 and 3 and put the item count in each label (line 195, 204).
F4. [MINOR] Contrast: BASE_C `#86b6ef` on `#fcfcfb` is about 2.0:1 (below 3:1 for graphics); MUTED `#898781` x-tick text is about 3.5:1. Light-blue interval lines in Figures 5, 6 are the hardest to see. Fix: darken BASE_C to about `#5b97dc`, XTICK to INK_2 (lines 51, 49, 65).
F5. [MINOR] `fig_s3_faults` line 347: width 9.6 in against 8 in for the others. At the same display width its 9 pt labels render about 17% smaller than Figure 1's. Left panel x-limit (line 360) leaves half the panel empty. Fix: figsize width 8.4, fonts 10, `set_xlim(-3, 35)` on the left panel only.
F6. [MINOR] `fig_s3_misses` line 401: the Wilson interval is a bare black line above the bar with no tick at the estimate, so it is not clear it belongs to the "Right" segment. Fix: add `ax.plot([100*counts[0]/len(asked)]*2, [y+0.30, y+0.42])` as a marker and caps.
F7. [MINOR] "(report)" arm names (Figures 5, 6, 8) are not explained in the figure; Figure 6's caption does not say K arms pool two seeds (828 against 1242 rows). Fix: add the Figure 5 caption sentence to Figure 6; in `S3.ARM_NAMES` use "K1 (seeds 82, 83)".
F8. [MINOR] Figure 2 (line 178): legend says "6.37, seed 82", Figure 1 "eight seeds pooled"; Figure 2 shows no interval yet carries the claim "no measured difference" (72/74, 65/70 on 80 questions, one seed). Same sets, different metric (older only, 14% to 35%, against recall, 22% to 40%, in Figure 1). Fix: add Wilson bars (line 118 `dumbbell`) or soften the subtitle to "similar".
F9. [MINOR] Figure 4 (`fig_never_told_slide` lines 430-452): y-axis starts at 35 of 48 and the title ("each repeat declined fewer") states a trend that four single runs with overlapping intervals do not show; the "the gate: at least 44" label (line 446) sits below the grey band it names. Fix: title "46, 48, 46, 43 of 48 never-told declined" ; label moved inside the band at y=45.
F10. [MINOR] Earns its place: Figure 3 (`demo_contamination`) is four numbers (6, 4, 0, 0 of 8); the grey bar's meaning is not in the legend. In the short paper it could be one sentence; if kept, add "grey: all keyed questions" to the x-label (line 473). The short paper's three figures have alt text equal to the title only.

## What holds up
Labels do not clip or overlap in any figure (Figure 2's x-label ends 43 px from the edge). Red against blue against grey separates for red-green colour blindness by lightness. Figures 5, 6, 8 state what their intervals resample (chats against rows).
