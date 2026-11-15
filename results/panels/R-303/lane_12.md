# Lane 12: Layout judge
Verdict: submit after fixes (no blocker or major; four minor layout and pointer fixes, all optional in effect)

## Round-3 findings: status (one line each)
F1 fixed: ARTICLE.md:77 now reads "(sections 6.2 and 12, Appendix C; R-298)"; 402 of 708 is at :1012 and in section 12.
F2 fixed: :185 says "six stages"; the table (:187-194) has 6 rows.
F3 partly: the blockquote is 71 words (was about 100); the Abstract (:11-40, 434 words) and Submission summary (:46-137) still precede section 1 at :138, and the claim still appears four times before it.
F4 fixed: Figures 1 to 7 are each cited in body text (:374, 426, 520, 526, 598, 601, 660); Figure 8 is not (see F3 below).
F5 partly: Appendix B has 7 columns, no empty "Pick recall" column (:958-983); the deviations table's longest cell is 34 words (:700, was about 60); the leakage and Track-map cells are 49 words (:154, :262), still wide.
F6 fixed: HF_ARTICLE.md captions at :100, :155, :170; "eight seeds pooled" is stated.
F7 fixed: "With more credits" and "The expectation in hand" are separate paragraphs (:208-215).
F8 fixed: MODEL_CARD.md's first paragraph now states the S3 faults.
F9 fixed: no record id in ABSTRACT.md; 495 words by `wc -w`, title included, so no room to add text.

Checks run: all relative links and the 8 `figures/` PNGs resolve (ARTICLE, README first 150 lines, MODEL_CARD, HF_ARTICLE raw URLs); no ragged table rows; no skipped heading level; every "section N" and "Appendix A/B/C" pointer in ARTICLE.md and HF_ARTICLE.md read in context and holds, with the exception below.

## New findings (most severe first)
F1. [MINOR] ARTICLE.md:171: "A full ledger of the reopened search ... (section 8)". The full ledger is Appendix B (:504, :951); section 8 holds the summary.
    Evidence: `grep -n "Appendix B" docs/ARTICLE.md` gives :504, :951.
    Fix: "(section 8, Appendix B)".
F2. [MINOR] HF_ARTICLE.md:1-48: 48 lines before section 1, including a 166-word "Result first" paragraph and a 153-word "Terms" paragraph (:40). The reader reaches the first heading after about 560 words.
    Fix: move "Terms" to the end of section 1, or split it into a list.
F3. [MINOR] Figures without a body citation: ARTICLE.md Figure 8 (:1025; no "Figure 8" outside its caption), HF_ARTICLE.md Figures 1 and 3 (:100, :170; Figure 2 is cited at :144).
    Fix: add "(Figure 8)" in Appendix C at :1015; "(Figure 1)" and "(Figure 3)" in the sentences above the HF images.
F4. [MINOR] Cells still wide: ARTICLE.md:154 and :262 (49 words each), :194 (33), :700 (34).
    Fix: move the clause after the table's last number into a sentence under the table.

## What holds up
- Heading depth 2 to 3 levels everywhere; no paragraph in either paper longer than about 255 words except two lists; longest single list item 117 words.
- README's first 150 lines: summary, Reopened, Results at a glance, Setup; tables at 3 to 6 columns; links resolve.
- Appendix A, B and C hold what the body says they hold (R-139 stages, 24-row ledger, `re_ask`, other-stored-facts counts, report arms by seed).
