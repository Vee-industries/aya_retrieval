# Lane 12: Layout judge
Verdict: submit after fixes (no blocker; five minor layout and pointer fixes, one of them touching a pointer to a section that does not hold the claim)

## Round-2 findings: status (one line each)
No round-2 report for this lane (new lane). Checked the appendix pointers added by R-300 instead:
- "Appendix A" (ARTICLE.md:374, 422, 431) holds what it names: false retrievals, coherence by judge, per-seed recall, R-016's two late references, R-139 stages, LongMemEval-S arm tables (lines 818-896). Holds.
- "Appendix B" (:482) is the 24-row ledger; I counted 24 rows and 6 "every line read". Holds.
- "Appendix C" (:564, 591, 594, 695) holds the shipped-seed lines, `re_ask`, other-stored-facts counts (:954), report arms by seed, Figure 8. Holds.
- Short paper pointers "long paper's section 4" (settings) and "section 15" (typed items) hold (ARTICLE.md:254, 741-757).
- No relative link in ARTICLE.md or README's first 150 lines points at a missing file (`docs/demo.md`, `docs/samples/`, notebook, RECORDS.md, STANDARD.md all exist). All 8 PNGs exist in `figures/`.

## New findings (most severe first)
F1. [MINOR] ARTICLE.md:73: the "For judges" bullet says outside chats "mostly" get another stored fact on never-told questions and points to "section 7". Section 7 holds only the demo's 2 of 4; the hand read of 8 is in 6.2 (:417) and the 402 of 708 count is in section 12 and Appendix C (:954).
    Evidence: `grep -n R-298 docs/ARTICLE.md` gives :417, :954, :755, :797; none in lines 438-471.
    Fix: change "(section 7)" to "(sections 6.2 and 12, Appendix C)".
F2. [MINOR] ARTICLE.md:172: "The work ran in five stages" but the table at :174-181 has six rows (Plan, Build, First sealed test, Faults, Push, S3).
    Fix: "six stages".
F3. [MINOR] ARTICLE.md first screen: title, byline, a 3-line pointer, a 100-word bold blockquote (:9), then Abstract (:11-40, last paragraph 273 words), Submission summary (:42-127: table, 7 bullets, "Use this when", Artifacts, Terms). The same claim appears four times before section 1 (blockquote, Abstract, Title and claim, one minute). Section 1 starts at line 129.
    Fix: no deletion needed; shorten the blockquote to its first sentence and move the C1 clause of the Abstract's last paragraph into its own paragraph (it holds 12 numbers in one block).
F4. [MINOR] ARTICLE.md figures: Figures 1, 2 and 7 are never cited in the body; Figure 5 is cited only by Figure 8's caption (:964). Only Figures 3, 4 and 6 are cited (:248, :498, :504, :578).
    Fix: add "(Figure 1)" at :374, "(Figure 2)" in 6.2, "(Figure 5)" at :560, "(Figure 7)" at :636.
F5. [MINOR] Tables with cells too long to read rendered: ARTICLE.md:141-146 (Track map, "when" cell about 70 words with 8 numbers), :242-252 (leakage table, cells to 300 characters), :647-666 (deviations, row 16 about 60 words), :362 (8 columns, header of 15 words), :902-927 (Appendix B, 8 columns, 26 rows, "Pick recall" filled on 3 rows). GitHub scrolls these sideways. Short paper S3 table (HF_ARTICLE.md:128-133, 6 columns) fits on desktop and wraps on a phone.
    Fix: drop the empty "Pick recall" column from Appendix B (put 720, 742, 775 in "How it ended"); split row 16 and the Track-map "when" cell into a sentence under the table.
F6. [MINOR] HF_ARTICLE.md figures (:69, :115, :135) have alt text only, no caption and no figure number, and the three use `raw.githubusercontent.com/.../main/figures/` URLs that resolve only after the planned push. Figure 1's plot shows eight seeds pooled while the sentence above it quotes seed 82's 91 to 107.
    Fix: add a one-line italic caption under each (say "eight seeds pooled"); after the push, open the HF page once to confirm the three images load.
F7. [MINOR] HF_ARTICLE.md:168-171 ("With more credits"): one paragraph of about 190 words mixing future work, a no-forecast statement and K1's S3 numbers. Section 7's bullets (:150-164) are 60 to 100 words each.
    Fix: split into "With more credits" (list) and "The expectation in hand" (own paragraph).
F8. [MINOR] docs/MODEL_CARD.md:17-29, the first screen on HF: leads with the outside-writer reading and "training's measured gain"; the S3 faults first appear at :43-57, below the first screen. The short paper and README open with both.
    Fix: add one sentence to the first paragraph: "On S3 it repeats its own wrong answers and names values on never-told questions more often than base (see Reopened)."
F9. [MINOR] ABSTRACT.md:6-8 cites "R-166" inside the abstract; the other record ids are absent from it. Reads as a stray pointer in 465 words.
    Fix: drop "(R-166)" or give it the short-paper phrasing.

## What holds up
- README's first 150 lines: summary, Reopened, Results at a glance, Setup in a sensible order; table widths 4 to 5 columns; links resolve.
- Heading depth is 2 to 3 levels in all long documents; no skipped levels; short paper is 8 numbered sections, 2,441 words.
- Short paper's first screen states result, use and links before section 1.
