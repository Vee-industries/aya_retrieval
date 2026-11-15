# Audit of a39473f (diff 56db55d to a39473f, R-304 to R-306)

Date 2026-11-15, 11:08 Eastern. Repo unchanged, Hugging Face unchanged. Read: `git diff 56db55d a39473f` (24 files), R-304,
R-305, R-306, `results/panels/R-305/`, the five built documents, README, both dataset cards, PUBLISH.md, HANDOFF.md.
Never-open list kept (the scratch copy was made with `git archive`, the sealed folders were not read by me).

Result: **0 HIGH, 3 MEDIUM, 6 LOW.** No wrong count found. Both HIGH findings of the 809855c audit are closed.

## Checks run (all passed unless a finding says otherwise)

- The five built documents (ARTICLE, HF_ARTICLE, ABSTRACT, MODEL_CARD, MODEL_CARD_C1) rebuilt from a clean `git archive a39473f`
  with the venv python and `make_article.py`: byte for byte identical (exit 0). Ruff check, ruff format check, pytest:
  "All checks passed!", "186 files already formatted", "1790 passed".
- Counts, whitespace / `\w+`: HF_ARTICLE 2,761 / 3,015; long paper Abstract 452 / 495; ABSTRACT.md with title 465 / 495
  (body 450 / 481). All under 500 both ways. `make_article.py` now refuses ABSTRACT.md over 500 by either count.
- ABSTRACT.md carries: 6.37 stays shipped; C1 failed "by 1.3 points"; 195 of 894 (21.8%) against 11 of 298 (3.7%) and 286 of 708
  (40.4%) against 14 of 236 (5.9%); the demo-change order ("two demo-test changes, both after its demo readings, the second also
  after K1.3's Demo5 reading"). The long paper's Abstract carries the verdict, 1.3 points, both fault rates and C1's 5 of 894 and
  51 of 708; it does not carry the demo-change order (it never did, see L4).
- New query-writing numbers recomputed from the S3 run files with my own script (`rc.py`, not the builder's): seed 82 did not search
  on 67 recall questions, code's search found the fact on 53; C1 seed 82: 11 and 6; 88 against 22 (p 1.6e-10) and 100 against 29
  (p 2.5e-10) unchanged. `ship_rule.json`: (a) pass on every line, (b) pass, (c) fails only "not above base's" (0.072 against 0.059),
  so "(a) pass, (b) pass, (c) fail by 1.3 points" is right.
- README typed numbers against `results/analysis/R-170/scores.json`: base declines 2 of 30 and 22 of 470; 6.37 declines 21 of 30 and
  233 of 470. Right. README line 4's wording, the S3 ship-rule line (README line 145) and the generated gap agree.
- Voice (kv_voice_v2): 0 em or en dashes and 0 we/our/us in all eight public documents; the added lines hold no hedge word. The
  remaining "much" (ARTICLE 879, "how much text was generated"; eval-logs card 66, a quoted chat line) and "very" (README 287, a
  quoted model reply) are not the author's prose.
- Privacy: `privacy_check.py` on the repo, 0 hits over 3,341 tracked files, planted checks passed; the same names, counted in the
  five live Hugging Face files, 0.
- Live copies: the 6.37 README and ARTICLE.md, the C1 README and both dataset READMEs, fetched logged out from `resolve/main`,
  match `docs/MODEL_CARD.md`, `docs/submission/HF_ARTICLE.md`, `docs/MODEL_CARD_C1.md`, `hf_data_card.md`, `hf_eval_logs_card.md`
  at a39473f byte for byte. `origin/main` is a39473f. The eval-logs dataset holds every tracked file of `results/` except
  `longmemeval/` (2,395 of 2,395, plus `.gitattributes` and README). The chats dataset holds all of `screens/`; it does not hold
  `onpolicy/` (127 files), `heldout3/` (S3's chats, 60), `check/`, `pilot_train.jsonl`, `first_test_items.jsonl`, none of which its
  card or PUBLISH.md names (S3's chats are said to be on GitHub, and are).
- Links, logged out: all 21 absolute URLs in the eight documents return 200 (GitHub, Hugging Face, Colab, the three Lexsi repos,
  raw figures); every relative link target in README and ARTICLE exists and opens on GitHub `main` (17 paths); the anchor
  `#11-how-637-was-chosen-the-candidate-ledger` exists at 3a2754e (heading "11. How 6.37 was chosen: the candidate ledger"); both
  collections list their repos (models: 6.37, base, C1; datasets: chats, eval-logs); `figures/s3_misses.png` on GitHub has the same
  SHA-256 as the committed file.
- eval-logs card rows: `s3/` holds the 15 `s3_*.json` run files named (base tool, code, whole chat, 6.37 at 82, 83, 94, C1 at 82, 83,
  94, K1, K1.3, K2.1 at 82 and 83), `ship_rule.json`, `coherence_sample.json` and `coherence/` (key, rubric, sheet, three judges);
  `demo2/` to `demo5/` hold `branches_*.json`, 25 `judge_*` in `demo2/`, and `overlap.json` or `contamination.txt` in `demo3/` to
  `demo5/`; `scrub/` holds `R-304_commit_map.tsv` (477 rows plus header). Row text matches except L5.
- Commit ids changed by R-304 (477 old ids from the map) searched in every tracked file outside `results/`, `RECORDS.md`, `data/`,
  `demo*`: one hit (L3). The long paper's link to 7b71a20 now reads 3a2754e and opens.
- Dates in the changelogs: R-290 to R-293 are 14 November, R-294 to R-306 are 15 November, matching the record headings. R-294
  is a three-lane panel; R-295 is ten reviewers; R-298 "the same ten lanes"; R-301 13 lanes; R-303 13 lanes. The changelog wording
  matches.
- Fixed as R-305 says (items of the 809855c audit): H1 (pushed, uploaded, 200), H2, M1, M2, M3 at the first place, M4, M5 wording
  (but see M2 below), M6, L1, L2, L3, L4, L5 (figure read: teal, rose, ochre, grey; four hues), L6 carried as Kevin's call.

## MEDIUM

### M1. The "outside timestamp" for S3's seal now needs the force push said

R-181 says GitHub's activity API records the `reopened` branch's creation at b771609 at 2026-11-12 12:13:03 UTC, and that is the
outside proof that S3 was public before any screening result. R-304 force-pushed `reopened` on 15 November (b771609 became
52a872b). The activity API today lists two events: `branch_creation 0000000 -> b771609` at 2026-11-12T12:13:03Z (still there) and
`force_push b771609 -> 52a872b` at 2026-11-15T14:49:34Z. R-304 does not say the proof changed, and no paper does. Kevin also plans
to ask GitHub Support to purge the old commits, which would remove the object the creation event names.

Where: `docs/ARTICLE.md` 114 to 117 ("public on the GitHub repository's `reopened` branch since 12 November, pushed as an outside
timestamp of the seal before any result (R-181)"), deviation row 23 (ARTICLE 737, "time proof for S3 only (R-181)"), and
the long-paper sentences that cite R-181 as a timestamp (ARTICLE 281, 511). Template: `docs/article_template.md`.

Fix: add after the sentence at 117: "R-304 rewrote the branch's commit ids and force-pushed it on 15 November; the activity record of
the 12 November creation still names the old id b771609, which is 52a872b in `results/scrub/R-304_commit_map.tsv` (every commit date
is unchanged)." Add to row 23: "the branch was force-pushed after a history scrub (R-304)". If Kevin has Support purge the old
commits, the activity record may go; say so in his request or keep a saved copy of the API output in `results/scrub/`. Both
the papers and R-181 depend on it.

### M2. "The adapter up to three" is wrong for 6.37 seed 82, and the hedge now misdescribes the comparison

R-305 added "(code runs one search, the adapter up to three)" after "Query writing is the likeliest cause; the counts do not isolate
it". Search counts per S3 item, from the run files: code 828 one, 4 two, 1 three, 1 four (834 items); **6.37 seed 82: 572 one, 262
none, never more than one**; C1 seed 82: 620 one, 125 none, 19 two, 1 three, 69 four. So for 6.37 the 88-against-22 comparison is
one search against one search, and "up to three" is untrue of it; for C1 seed 82 the multi-search point holds (89 of 834 items,
69 with four).

Where: `docs/ARTICLE.md` 824 to 826 (K1's S3 report arm paragraph), 1072 to 1073 (Appendix C), `docs/submission/HF_ARTICLE.md` 187
to 188; templates `article_template.md` ("Query writing is the likeliest cause of lost recall; the counts do not isolate it (code runs
one search, the adapter up to three)" twice) and `hf_article_template.md`.

Fix: "code runs one search; 6.37 seed 82 ran one search or none on every S3 item, so its comparison is one search against one;
C1 seed 82 ran more than one on {{n}} of 834 items". Generate the 89 in `s3_round2_numbers` from the run files. The claim then
"not isolated" holds for C1 only, and for 6.37 the remaining differences are the query text and the choice of what to search for.

### M3. The long paper's Abstract no longer says K1.3 failed (c)

809855c's long-paper Abstract said K1.3 "failed (c) like C1". R-305 cut it, and the sentence now reads "Two report arms, K1 and K2.1
(earlier candidates run on S3 outside the rule; exploratory), met every measured line." Three report arms ran (README, ARTICLE
body, HF_ARTICLE all say so; K1.3 failed (c) on 37 of 472, 7.8%). "Two report arms" reads as if only two ran, and the one that
failed is the one missing. Not wrong, but a clause that does not help the claim was the one cut.

Where: `docs/ARTICLE.md` Abstract (last paragraph of the Abstract, built lines about 38 to 40); `docs/article_template.md` the
same sentence.

Fix, word-neutral: "Of three report arms (exploratory), K1 and K2.1 met every measured line; K1.3 failed (c) like C1." (the
parenthesis shortens by 8 words, the added clause adds about 8; check `\w+` stays under 500, it is 495 now).

## LOW

### L1. README and MODEL_CARD "when the chat fits" advice omits the S3 whole-chat weakness the papers state

README 305 to 316 ("that is the better choice" at 307; "show base the whole chat and leave the adapter out" at 313) and
`docs/MODEL_CARD.md` 201 to 206 give the advice without the S3 caveat that `docs/ARTICLE.md` 92 to 94 and `HF_ARTICLE.md` 30 to 31
give: on S3 base with the whole chat names a listed value on 57 of 236 (24.2%) N-hit questions against base-with-tool's 14 of 236
(5.9%), and names no listed value on 89 of 120 (74.2%) plain never-told questions against 111 of 120 (92.5%). README's S3 table
shows the 24.2%, the card does not. Fix: add one sentence to both, using the generated keys already in `make_article.py`.

### L2. "Deadline extended" is still plain after the first place

R-305 item 4 asked for "reported extended (R-173)" at the first place in each document, and that is done. Three later places still
state it as fact: `docs/ARTICLE.md` 203 (chronology row, "deadline extended"), 215 ("When the deadline was extended, I saw
results I had missed") and 867 ("before the extended deadline"). R-173 says the site still showed 15 November. Fix: "reported
extended" in those three (template rows in `article_template.md`).

### L3. A test docstring cites a commit id that R-304 changed

`tests/test_r178.py` line 4: "(commit 8e73cf0)" is aea532f after the scrub (map row 9). Fix: change the id in the docstring (no test
reads it).

### L4. The long paper's Abstract does not carry the demo-change order

Informational. ABSTRACT.md does (as asked); the long paper's Abstract never did, in 56db55d or now; the order is in section 8
(ARTICLE 571 to 574: R-276 after C1's two demo readings and K1.3's Demo4 reading, R-278 after all four). If the check wants it in
both abstracts, it is a 20-word add against 495 `\w+`.

### L5. eval-logs card says "sealed in R-181"

`docs/submission/hf_eval_logs_card.md`, the `s3/` row: S3 was sealed in R-179 (stage 1); R-181 is the outside timestamp. Fix:
"(sealed in R-179, outside timestamp R-181, scored in R-287)". The card is live on Hugging Face, so the fix needs a one-file
upload of the README to `aya-retrieval-eval-logs`.

### L6. Figure 8 labels three pooled seeds "C1, published"

`figures/s3_misses.png` (n = 1242 for 6.37 and C1) labels the arm "C1, published", but the published adapter is seed 82 (n = 414). The
label comes from `ARM_NAMES` through `.replace("the pick", "published")` (`scripts/make_figures.py` 336). The caption of Figure 8
(`article_template.md` 962) gives no seeds. Fix: label "C1, three seeds" and add to the caption "6.37 and C1 pool seeds 82, 83 and 94;
report arms seeds 82 and 83" (STANDARD rule 9: a caption gives n and seeds). Rebuild the PNG, SVG, PDF.

## Not checked

The claim line of each cited record (only the R-ids named in the changed text, R-181, R-294, R-304 to R-306, were read); the judged
tables against `judged.json`; README commands and the notebook (unchanged since 809855c); the 6.37 and C1 weight files on
Hugging Face (not in the diff; the 6.37 repo lists 5 files and the C1 repo 4); the GitHub Support request.
