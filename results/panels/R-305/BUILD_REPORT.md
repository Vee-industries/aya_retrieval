# Build report: FIXLIST items 1 to 15 (2026-11-15, 10:10 Eastern)

All 15 items done in the clone `scratchpad\ar` (HEAD 04910da). Nothing committed or pushed; the real repo was not touched.

| # | Done | Note |
|---|---|---|
| 1 H2 | yes | README section retitled "give base the whole chat", audit text in; "much better than base" gone. MODEL_CARD "How to use it": base whole chat, adapter out; R-165 outside-writer only, one seed, not on S3 (worse on both faults) |
| 2 M1 | yes | ARTICLE: K1.3 clause, flags sentence, "push ran" clause cut; "base" defined once. ABSTRACT: flags sentence and "push ran" clause cut, "base" defined, last paragraph shortened. Both now add "by {{s3_gap_points}} points". make_article.py now fails ABSTRACT.md over 500 by `\w+` as well as whitespace |
| 3 M2 | yes | "(Claude agents)" at first use in all four |
| 4 M3 | yes | "reported extended (R-173)" at first place in ARTICLE, ABSTRACT, HF_ARTICLE, README, MODEL_CARD; no dates |
| 5 M4 | yes | README sentence replaced; deviation row 23 added; section 11 lead says rows 21 to 23 |
| 6 M5a | yes | new key `s3_qw_unsearched_*` (67; C1 11) from run files; wording in ARTICLE (two places) and HF |
| 7 M5b | yes | "made the difference" sentence dropped; "measured cause" changed in ARTICLE (3 places, plus changelog) and HF |
| 8 M6 | yes | README line under the S3 table. README is hand-written, so 1.3 is typed there; make_article.py now fails if README lacks "(c) fail by {s3_gap_points} points" (tested: 1.4 makes it exit 1) |
| 9 L1 | yes | both LongMemEval-S decline rows labelled, in make_article.py |
| 10 L2 | yes | "far" removed both places; 6.37's declines now give base's 2 and 22 (README's own table) |
| 11 L3 | yes | README and ARTICLE changelogs: 14 Nov to R-293, 15 Nov R-294 to R-305, panel lanes named, R-301 and R-303 as thirteen-lane rounds; both chronology tables end R-305 |
| 12 L4 | yes | "C1 seed 82 against base" |
| 13 L5 | yes | misread colour #74bdb4 to muted rose #b5739d (not a model hue). Least CIELAB distance to the other outcome colours, Machado 2009 simulation, my measurement: 26/13/6 before, 44/17/19 after (normal/deuteranopia/protanopia). Only s3_misses PNG, SVG, PDF changed |
| 14 | yes | 7b71a20 to 3a2754e, text and URL (map row 4; anchor exists at 3a2754e) |
| 15 | yes | R-304 line in ARTICLE chronology note and changelog, HF under its table, README changelog |

HF_ARTICLE kept at 2,761 by cutting: the "push ran" clause, K1 report-arm sentence in section 8, "rows A to D", a caption repeat, "the table below: seed 82", "the user can act on", a few words.

## Word counts (built files; whitespace / `\w+`)
- HF_ARTICLE: 2,761 / 3,015
- ARTICLE Abstract: 452 / 495
- ABSTRACT.md with title: 465 / 495 (body 450 / 481)

## Checks (logs in `scratchpad\`)
- make_article.py: exit 0, last line "wrote docs\MODEL_CARD_C1.md"
- make_figures.py: exit 0, last line "wrote figures/demo_contamination.png, .svg and .pdf" (other figures differed only in line endings; restored)
- ruff check: "All checks passed!"
- ruff format --check: "186 files already formatted"
- pytest: "1790 passed, 14 warnings in 31.09s"

Not checked: links; README `very` at line 287 is a quoted model reply; ARTICLE's pre-existing "how much text was generated" (section on LLM use) left as is.
