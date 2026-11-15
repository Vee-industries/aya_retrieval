# Round-4 build report (clone `scratchpad\ar` at 125b902, uncommitted)

Result: 51 of 51 FIXLIST items done; four done only in part in the short paper because of its word cap (listed under
the table). Every check passed: ruff check and ruff format --check on src scripts tests, pytest 1,790 passed. No
commit, push, stash or branch switch. Built 15 November, 09:16 Eastern.

## Items (FIXLIST.md numbering)

| # | Done | Files |
|---|---|---|
| 1 | done: the first demo change came after both of C1's readings and K1.3's Demo4 reading and ordered K1.3's Demo5 reading knowing C1's; only the second came after all four | article_template (section 8 disclosure; deviation 11, with a note under the table), hf_article_template section 5, abstract_template, model_card_c1_template |
| 2 | done: "do not use 6.37" when both faults matter; C1 lower than 6.37 but not below base on N-hit (7.2% against 5.9%); code's S3 fault rates (65 of 298, 121 of 236) beside the code advice, with "neither fault was measured past the window"; the whole chat's never-told numbers introduced as its cost, each against base named | hf_article_template, article_template, model_card_template ("Which to use when") |
| 3 | done: 88 against 22 where both searched (p 1.6e-10), 53 not searched; C1 seed 82 100, 29, 6; claim limited to the questions both searched | make_article.py, article_template (Appendix C, section 14), hf_article_template section 6 |
| 4 | done: code 714 of 834 right decisions against 682, 666, 670 | hf_article_template ("When") |
| 5 | done: pooled 288 of 480 against 158 of 260 marked as different questions; same questions: seed 82 65, code 84 of 119 (p = 0.0026); C1 seed 82 111, 93 of 154 (p = 0.038); the 59 of 347 all agreements with a true claim, no search (checked in code) | make_article.py, article_template (moved under the section 1 table), hf_article_template (seed 82 only) |
| 6 | done: 30 of 58 true claims hold the answer, no `older` item does (checked in code); base 28 of 59, 27 no search; `older` alone by arm | make_article.py, article_template (Terms, leakage row, section 12), hf_article_template section 1 |
| 7 | done: base 1 of 28, code 11, whole chat 4, 6.37 0 of 84 (seed 82 0 of 28), C1 32 of 84 (seed 82 11 of 28), K1 1 of 56, K2.1 4 of 56 | make_article.py, article_template section 9, hf_article_template table row |
| 8 | done: `--report-name fix17cs37_82_retrain`, `--out-dir ../adapters/retrain/fix17cs37_82`, `--save-epochs 2`, and why | README.md |
| 9 | done | hf_article_template |
| 10 | done | hf_article_template, article_template |
| 11 | done: seed 82 alone below 0.01 in every condition, largest p 1.5e-19 | make_article.py, article_template section 5 |
| 12 | done | article_template (section 9, Appendix C) |
| 13 | done | hf_article_template, article_template |
| 14 | done: base 1 and 0; too few to compare | article_template 6.2 |
| 15 | done: -1.3 points, interval -5.9 to +3.4 | make_article.py, model_card_c1_template |
| 16 | done | article_template (metrics table, section 8, Figure 4 caption), make_figures.py (Figure 4 title, axis), model_card_template, README.md |
| 17 | done: 202 four-word runs shared with C1's seed 82 set (same function as 6.37's 140); six-word drops cited (R-206, R-253) | make_article.py, article_template leakage row |
| 18 | done | article_template section 15 |
| 19 | done, through R-303 (see note 1) | article_template, hf_article_template, README.md, PUBLISH.md |
| 20 | done | README.md |
| 21 | done | PUBLISH.md |
| 22 | done (snippet not run: no network, no model loading) | model_card_template, model_card_c1_template |
| 23 | done | article_template section 9 |
| 24 | done | article_template (section 3 threat model; section 12 heading kept alone), hf_article_template (section 1 threat model; section 7 heading kept alone) |
| 25 | done | article_template (twice), model_card_template |
| 26 | done | article_template, README.md |
| 27 | done | hf_article_template, article_template, model_card_template, README.md |
| 28 | done | hf_article_template |
| 29 | done | article_template section 7 |
| 30 | done (row 21 and a note under the table) | article_template |
| 31 | done (RECORDS.md searched for Kevin's word on controls; none found) | article_template |
| 32 | done; Liu, Mallen, Packer, Schick and Yao removed from References (cited nowhere else) | article_template |
| 33 | done | article_template section 14, hf_article_template section 8 |
| 34 | done: "under 22 points, the 95% half-width of a difference between two rates near 50%" (make_article.py line 378 computes it) | article_template, model_card_template, README.md |
| 35 | done: 54 and 42 of 120 | model_card_template, README.md |
| 36 | done | model_card_template |
| 37 | done: 38 of 81 and 36 of 67 (checked as the largest stage in code) | make_article.py, article_template 6.2 |
| 38 | done (also README's two copies) | abstract_template, README.md |
| 39 | done | hf_article_template section 5 |
| 40 | done | model_card_c1_template |
| 41 | done | hf_article_template section 7 |
| 42 | done | hf_article_template section 4 |
| 43 | done | hf_article_template, article_template Appendix C |
| 44 | done | article_template |
| 45 | done: a list, kept before "Use this when" so N-hit and copy are defined before use | hf_article_template |
| 46 | done: leakage, chronology and grounds cells moved under their tables; deviation rows 11 and 21 given notes | article_template |
| 47 | done | hf_article_template |
| 48 | done: teals, ochre, light grey | make_figures.py |
| 49 | done: title "...its false-answer rate (7.2%) is above base's (5.9%)" from the results; "C1, published" in every S3 figure; shared x scale; report arms named | make_figures.py |
| 50 | done: short findings checked against the figures | hf_article_template |
| 51 | done | make_figures.py |

Partly done in the short paper because of its word cap (the long paper carries each in full):
- Item 5: C1 seed 82's same-question grounding pair (long paper section 1 only).
- Item 6: the base agreement counts (lane 3 asked for them in the long paper only).
- L1 F5: the related-work pointer did not fit; the baselines-ran-in-one-setting line is in (section 7).
- To meet 2,761 words, the short paper lost "the lines C1 passed are as unresolved (statements -4.4 points...)"
  (long paper section 9 keeps it), "9 of its 36 layers attend to all of them" (long paper section 1 keeps it), the
  K1.3 and OP definitions in Terms, and a few connecting words.

Not changed (the FIXLIST's last section): L6 F1 publication; L4's carried items outside the editable files (a
constraints file, `judges_check.json`, `MAX_TOKENS` copies, `qs3.sh` usage, make_article.py's restatement of
`score_s3.py`'s rule, which needs a change to `score_s3.py`); L7 rules 20, 21, 28, 30 (disclosed); L8 round-3 F3
(the author's wording); "S3" expansion (a name, R-178).

Notes:
1. The ranges end at R-303, assumed to be the record of this round. If the round is recorded under another id,
   change it in article_template (chronology, changelog), hf_article_template (chronology), README.md (Reopened,
   changelog) and PUBLISH.md.
2. One one-line edit to make_article.py was made with `sed` (the `s3_agree_base` format), not a heredoc; every other
   edit used the file-editing tool.
3. `ruff check .` from the repository root reports errors in the tracked `results/panels/R-198/scripts/r198_cue.py`;
   that file is unchanged at 125b902 and outside src scripts tests.
4. README.md is hand-written: its new numbers (54 and 42; 22) are copied from the built model card, where
   make_article.py generates them.

## New generated keys (`scripts/make_article.py`)

`sealed_ship_p_max`; `ow_missed_1`, `ow_missed_2`; `s3_runs_shared_c1`; `s3_nosearch_637`, `s3_nosearch_c1`;
`s3_conf_true`; `s3_agree_base`, `s3_agree_base_ns`; `s3_older_{base,as,wc,637,c1}`;
`s3_fc_{base,as,wc,637,ship82,c1,c182,k1,k21}`; `s3_qw_nosearch_{637,c1}`, `s3_qw_p_{637,c1}`;
`s3_gb_{n,own,code,p}_{637,c1}`; `c1s82_nhit_gap`. Changed meaning: `s3_qw_code_only_{637,c1}` now counts only
questions the seed searched (88 and 100, were 141 and 106). New stop checks: seed 82's sign test per condition is
collected; a missed search must stay the largest outside-set stage; 6.37's right-but-not-found answers must all be
no-search agreements; S3's true claims must hold the answer and no `older` item may; no 6.37 seed may correct a
false claim. New typed numbers added to section 15's list: the screening gates' thresholds, the 50 marked lines,
`hard_dev`'s 96.

## Checks

- Rebuild: `make_article.py` wrote all five documents; `make_figures.py` wrote all eight figures (a second run gave
  the same bytes).
- `ruff check src scripts tests`: all checks passed. `ruff format --check src scripts tests`: 186 files already
  formatted.
- pytest: `1790 passed, 14 warnings in 30.45s` (`panel5\pytest_build.txt`, last line).
- Figures opened: s3_faults, s3_misses, never_told_slide, s3_recall (changed), and recall_out_of_view and
  demo_contamination (to check the new alt texts). No clipped or overlapping text.
- `{{` in the five built documents: 0. Em or en dashes: 0. "we", "our", "us": 0.
- Words (`wc -w`): short paper 2,761 (was 2,761); ABSTRACT.md 498; long paper's Abstract section 499 (unchanged).

## `git diff --ignore-cr-at-eol --stat`

```
 README.md                              |  43 +-
 docs/ARTICLE.md                        | 199 ++++---
 docs/MODEL_CARD.md                     |  49 +-
 docs/MODEL_CARD_C1.md                  |  33 +-
 docs/article_template.md               | 199 ++++---
 docs/model_card_c1_template.md         |  33 +-
 docs/model_card_template.md            |  49 +-
 docs/submission/ABSTRACT.md            |   8 +-
 docs/submission/HF_ARTICLE.md          | 185 +++----
 docs/submission/PUBLISH.md             |   8 +-
 docs/submission/abstract_template.md   |   8 +-
 docs/submission/hf_article_template.md | 185 +++----
 figures/never_told_slide.pdf           | Bin 32369 -> 32319 bytes
 figures/never_told_slide.png           | Bin 85392 -> 90449 bytes
 figures/never_told_slide.svg           | 561 ++++++++++---------
 figures/s3_faults.pdf                  | Bin 35668 -> 38175 bytes
 figures/s3_faults.png                  | Bin 153709 -> 161900 bytes
 figures/s3_faults.svg                  | 962 ++++++++++++++++++++-------------
 figures/s3_misses.pdf                  | Bin 30727 -> 30724 bytes
 figures/s3_misses.png                  | Bin 98270 -> 97705 bytes
 figures/s3_misses.svg                  | 535 +++++++++---------
 figures/s3_recall.pdf                  | Bin 29996 -> 29786 bytes
 figures/s3_recall.png                  | Bin 105057 -> 105391 bytes
 figures/s3_recall.svg                  |  37 +-
 scripts/make_article.py                |  73 ++-
 scripts/make_figures.py                |  53 +-
 26 files changed, 1837 insertions(+), 1383 deletions(-)
```

The other four SVGs show as modified in `git status` by line endings only.
