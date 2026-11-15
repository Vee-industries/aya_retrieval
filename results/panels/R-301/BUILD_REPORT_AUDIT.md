# Build report: the audit of b10eb2a, fixes applied

Clone `scratchpad\ar` at b10eb2a; nothing committed, pushed, stashed or switched. Written 2026-11-15 13:18 Eastern.
Result: 14 of 14 briefed items done; every check passed (make_article, make_figures, ruff check, ruff format
--check, pytest 1790 passed, no `{{` in built docs, both abstracts under 500, figures viewed).

## Findings

| Finding | Done | Files (templates, README, PUBLISH, scripts; built files rebuilt only) |
|---|---|---|
| H2 long Abstract under 500 | Done: 515 to 499 words (built section, between "## Abstract" and "## Submission summary", `wc -w`). Cuts: the window/memory clause on the 419-message chats (still in "For judges" and section 6), "across the four conditions", the LME interval in the abstract only (now `{{lme_j_ship}} against {{lme_j_code}} of {{lme_judged_n}}`, the long form stays in the body), shorter demo-fault and S3 sentences | `docs/article_template.md` |
| H3 README S3 table | Done: 3-row table (recall with chat-resampled intervals, copies, N-hit false answers) for base with the tool, code, whole chat, 6.37 (three seeds), C1 (three seeds), numbers from the built ARTICLE section 9 table; one line on the report arms (K1 and K2.1 met every measured line, 12 and 14 of 472; K1.3 failed (c), 37 of 472) | `README.md` |
| M2 STANDARD v3 sentence | Done: one sentence at the top of section 11, where STANDARD is first cited: STANDARD v3 and rule numbers above 12 (rows 21, 22, sections 12, 13) refer to the author's research standard, version 3, not in this repository; `STANDARD.md` here is the earlier rules 1 to 12, the one row 16 cites | `docs/article_template.md` |
| M3 reopening reason | Done in all seven places: long Abstract, section 2, section 7, HF section 4, MODEL_CARD "Reopened", README "Reopened", ABSTRACT.md. Wording: "With the deadline extended, I saw results I had missed and judged the extra time enough to train further, so I reopened the project (R-177); the push to replace 6.37 ran inside the time that remained." The two abstracts say "the push ran in the time that remained". "The extra day allowed further training" is gone | article, hf_article, model_card, abstract templates; `README.md` |
| M4a Figure 5 base line | Done: thin line at base's rate on the right panel (`arm_points(base_line=True)` for `n_hit_false_answer` only); subtitle and both captions name the band "base's 95% interval" and the line as clause (c)'s | `scripts/make_figures.py`, article and hf_article templates |
| M4b Figure 2 overlap | Done: `dumbbell(close=6)` draws two dots under 6 points apart one above the other (set 1 whole chat 72/74, set 2 whole chat 65/70); labels follow their dots | `scripts/make_figures.py` |
| M4c point counts | Done by caption: Figure 1 and 2 captions (long paper) and Figure 1 (short paper) say point counts with no interval; Figure 2's subtitle says the same. No intervals added | article and hf_article templates, `scripts/make_figures.py` |
| M4d Figure 8 colours | Done: outcomes now dark blue (right), light blue (misread), orange (missed), grey (no search), from the other figures' colours; no red or green | `scripts/make_figures.py` |
| M4 PDF | Done, but not in one line: `save` now takes its metadata from one dict (png Software, svg Date, pdf CreationDate, all None) so the PDF holds no timestamp; net +2 lines with a comment. A second build wrote byte-identical PDFs and PNGs (md5 compared). 8 new untracked files `figures/*.pdf` | `scripts/make_figures.py` |
| M5 first-use terms | Done. Long Abstract: N-hit ("never-told questions whose search returned text (N-hit false answers)"), C1 ("trained on corrections of its own errors"), report arms ("earlier candidates run on S3 outside the rule"), K1 ("other fact types in every chat"), K2.1 ("K1 with other never-told traps"), K1.3 ("K1 with facts reworded, C1's starting point"). ABSTRACT.md uses only C1 of these: defined the same way. M5(b), "(Claude agents)" for outside writers, was not in the brief: not done | article and abstract templates |
| M6 PUBLISH.md | Done: four repos with C1, the short paper as the 6.37 repo's `ARTICLE.md`, abstract limit and make_article's refusal, order privacy sweep, push (`main`, which every link names), HF uploads (6.37 card and article, C1 card, `results/s3/` to eval-logs with its card, collections), link recheck, form; "Done" list with R-172, R-181, R-296 | `docs/submission/PUBLISH.md` |
| M7 README overstatement | Done: "On S3 it names a stored value on 402 of 708 (56.8%) never-told questions whose search returned text (R-298)", same number as the long paper's `s3_off_637` | `README.md` |
| M8 set 1 | Done: "names more listed values on `never_told` on set 2 (p = 0.0042); set 1 shows no measured difference (p = 0.11)" | `docs/article_template.md` |
| L1 tokens and exchanges | Done (R-170 holds "about 115k tokens" and the profile's median of 244 exchanges): README lines at "Results at a glance" and the LongMemEval-S section now give "244 exchanges, about 115,000 tokens, at the median". R-170's 115k figure was written beside the first, wrong exchange count (126); the profile corrected the exchanges and did not recount tokens. Not checked further | `README.md` |
| L2 stale README lines | Done: three review rounds (ten, ten, thirteen; R-295, R-298, R-301); PRE-SPRINT, SPRINT or REOPENED; `data/heldout3/` opened once for its run on 14 November (R-280); `docs/` row names ABSTRACT, HF_ARTICLE, MODEL_CARD_C1, PUBLISH; co-author line "every commit through R-301 (1,627)" (counted in the clone: 1,627 commits, 1,627 co-author lines) | `README.md` |
| L3 model card heading | Done: "Reopened, 12 to 15 November" | `docs/model_card_template.md` |
| L4 generalization line | Done: "(against base; code shows no measured difference from 6.37, and the whole chat recalls more)" | `README.md` |
| L5 short paper | Done: pinned revision in section 1 through the new key `model_revision`; a one-sentence **Claim** above "Result first" | `docs/submission/hf_article_template.md`, `scripts/make_article.py` |
| H1, M1, L6 | Not done: the author's calls, per the brief | |

## New generated keys

- `model_revision` (in `model_numbers`, from `aya_retrieval.models.MODEL_REVISION`), used in the short paper's section 1.
- Existing keys newly used in the long Abstract: `lme_j_ship`, `lme_j_code`, `lme_judged_n`.
- No new typed number in a template. The "6 points" in Figure 2's caption is the drawing threshold `close=6` in
  `make_figures.py`, not a result. README is hand-edited; its new numbers are copied from the built ARTICLE
  (section 9 table, Appendix C, `s3_off_637`), R-170 and the clone's git log.

## Checks

- `make_article.py`: wrote all five built files; `make_figures.py`: wrote all eight figures as PNG, SVG and PDF.
- `ruff check src scripts tests`: All checks passed. `ruff format --check src scripts tests`: 186 files already formatted.
- pytest (output in `scratchpad\panel4\pytest_audit.txt`): 1790 passed, 14 warnings.
- `{{` in ARTICLE, MODEL_CARD, MODEL_CARD_C1, HF_ARTICLE, ABSTRACT: 0 each.
- Word counts (`wc -w`): long Abstract section 499 (was 515); ABSTRACT.md 495 whole file, 480 body (was 497 and
  482); HF_ARTICLE 2,761 (was 2,665; +96 from the claim sentence, the revision, the reopening reason and the
  caption notes; L6 is the author's call); ARTICLE 15,508; README 7,844.
- Voice scan of every added line in the edited sources (180 lines): no em or en dash, no we/our/us, no hedge word;
  one "so far" removed (heading now "Done").
- Figures viewed: `whole_chat_or_search.png` (dots separated, labels whole), `s3_faults.png` (line at base's 5.9%
  on the right panel, subtitle on two lines, nothing clipped), `s3_misses.png` (blue/orange/grey, legend whole).
  The other five PNGs are byte-identical to b10eb2a; their SVGs differ only in line endings.

## Process notes

- One edit, the first replacement of the long Abstract, was written through a Python here-document in the shell, not
  the Edit tool. Its text holds no backslash; the template diff was checked and every later edit used Edit or Write.
- `docs/MODEL_CARD_C1.md` and `model_card_c1_template.md` were not changed.
- Not checked: the README "Results at a glance" S3 table renders on GitHub; the new PDFs open in a PDF reader.

## git diff --ignore-cr-at-eol --stat

```
 README.md                              |  39 ++-
 docs/ARTICLE.md                        |  76 +++---
 docs/MODEL_CARD.md                     |   5 +-
 docs/article_template.md               |  76 +++---
 docs/model_card_template.md            |   5 +-
 docs/submission/ABSTRACT.md            |  22 +-
 docs/submission/HF_ARTICLE.md          |  19 +-
 docs/submission/PUBLISH.md             |  67 ++++--
 docs/submission/abstract_template.md   |  22 +-
 docs/submission/hf_article_template.md |  19 +-
 figures/s3_faults.png                  | Bin 151608 -> 153709 bytes
 figures/s3_faults.svg                  | 428 ++++++++++++++++++---------------
 figures/s3_misses.png                  | Bin 98252 -> 98270 bytes
 figures/s3_misses.svg                  |  60 ++---
 figures/whole_chat_or_search.png       | Bin 96554 -> 99825 bytes
 figures/whole_chat_or_search.svg       | 113 ++++++---
 scripts/make_article.py                |   1 +
 scripts/make_figures.py                |  62 +++--
 18 files changed, 602 insertions(+), 412 deletions(-)
```

Untracked: `figures/{demo_contamination,never_told_slide,recall_out_of_view,s3_faults,s3_misses,s3_recall,training_memory,whole_chat_or_search}.pdf`.
