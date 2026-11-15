# Lane 6: Hackathon judge (applies the official rules)
Verdict: submit after fixes (push the repository or repoint the links; add a one-line threat model, why-this-problem and no-retention-benchmark statement to the short paper)

Source status. hackathon.lexsi.ai/submit returned 404 (also /submit/, /rules, /structure, /faqs, /tracks, /eligibility). Only the overview page `/` and `/submission/` (title only, no form text) could be read. So the exact "Write-up content" markers (`*` `^` `"`) were NOT read today; the item list below comes from R-217 (read 13 Nov 13:08, RECORDS.md) cross-checked against the overview page's summary of the write-up template. The site publishes no judging weights ("scored on a fixed numeric scale", no criteria).

## Findings (most severe first)
F1. [BLOCKER] HF_ARTICLE.md (lines 17-23, 92, 108, 151, 158, 181, 195) and the form point at GitHub `Vee-industries/aya_retrieval` `main`, which does not hold the current work. Local `origin/main` is the 10 Nov commit 7b71a20; the local branch is 465 commits ahead; RECORDS says "Nothing pushed" through R-293.
    Evidence: `git log origin/main..HEAD` = 465; `git reflog origin/main` last update 2026-11-10 13:31 by push; `git ls-tree origin/main figures/{demo_contamination,never_told_slide,s3_faults,s3_misses}.png` = 0 each (so 4 of the 6 images in the short paper will not render); `git show origin/main:RECORDS.md` has 172 R-entries (local 293); origin's ARTICLE.md has 0 mentions of S3, so the "full write-up" link is the pre-reopening paper. (Local refs only; I may not read GitHub, so a push from elsewhere is unchecked.) Judges are told public GitHub repo with README and reproduction notes is required.
    Fix: Kevin pushes before the deadline (R-217 notes the push also publishes sealed S3 chats and candidate-session commits; that is his call), then re-open the HF article and check the images load. If he will not push, replace the raw.githubusercontent figure links with images uploaded to the HF model repo.

F2. [MAJOR] HF_ARTICLE.md: "Threat model [T3]" has no place in the short paper (no row in the "Where each required item is" table, no text). It is only in ARTICLE.md line 180-182 (adversary = chat's own content; hidden instructions in retrieved passages not tested; tool read only).
    Evidence: `grep -c -i threat` HF_ARTICLE.md = 0, ARTICLE.md = 1.
    Fix: add two lines to HF section 1 and a table row.

F3. [MAJOR] No general-capability retention check, a [T3] item per R-217, and neither paper says it was not run. "Checks that nothing else got worse" exists only as in-task lines (in_view, statement, coherence, false retrieval). R-217 left item 5 "not done".
    Evidence: `grep -i "retention\|MMLU\|general capab"` in ARTICLE.md, HF_ARTICLE.md = 0 hits; limits (ARTICLE section 12; HF section 7) do not name it.
    Fix: one limits line: "No general-capability benchmark was run; only task-internal regression lines." (Running one is GPU work, outside this lane.)

F4. [MAJOR] "Problem statement and why this problem | top" in HF's required-item table is not true: the top gives the statement only. No real-world use case or motivation in the short paper; ARTICLE.md section 1 gives it (context window, LLE).
    Evidence: HF_ARTICLE.md lines 28-30, 254; the overview page lists "real-world use case" under problem statement and approach.
    Fix: add two sentences from ARTICLE section 1 (8,192-token window, 9 of 36 layers see all of it) to HF section 1, or correct the table cell.

F5. [MINOR] HF_ARTICLE.md has no "Abstract" heading; the "Result first" paragraph does the job (headline, base model, method are in it). Related work, acknowledgements wording and sample pointers are partial: related work absent (ARTICLE line 135 only); samples absent (ARTICLE line 83 only; links in HF would need `docs/demo.md`, `docs/samples/`, which also depend on F1); acknowledgements present (HF line 226).
    Fix: one sentence plus links in section 8; related work can stay in the long paper (table already points there for most items; add a row).

F6. [MINOR] Deadline in the shared brief is off by one hour. Overview page: submission due Nov 15, 2026 11:59 PM AoE (UTC-12) = 11:59 UTC Nov 16 = 06:59 EST Nov 16 (DST ended 1 Nov). Brief says 07:59 ET. `date` now: Sun 15 Nov 05:04 EST.
    Fix: treat 06:59 Eastern 16 Nov as the cut-off. R-217 (13:55) says the form is filed; the overview page says only the latest submission before the deadline counts, so a refiling is allowed.

F7. [MINOR] Compute figures differ across records: R-217 summed 188 GPU hours to 13 Nov; ARTICLE line 696 and HF line 220 say 217 hours (training 108.6 h over 186 runs). Plausibly later runs; not recomputed here. Another lane may check it.

## Item-by-item (R-217 list; HF = short paper, LP = long paper, AB = ABSTRACT.md; 435 words, under 500)
Present in HF: title and one-line claim (top; LP summary); tracks and problem-statement number (HF 28-30); abstract-level headline before-to-after and base model and method (HF 5-14, 46-51; AB); toolkit use and connection (HF 53-58); models, revision, licences (HF 50-51, 220); data, sizes, splits, leak checks done and not done (HF 60-68); languages (English only, HF 67, 210); tool environment and trajectories (HF 39-44, 67-68); metrics with direction (HF 70-72); hyperparameters (HF 50); hypotheses/ship rule (HF 129-132); results with same-model before/after, seeds (8 seeds, 3 seeds pooled), counts and intervals (HF 84-114, 172-186); strongest baselines (HF 94-108); ablations/candidate ledger (HF 134-165; LP section 8); negative results and errors (HF 115-123, 167-195); limits (HF 197-211); future work (HF 215-216); reproduce (HF 218-220); compute and cost, $0, no closed-model baseline (HF 51, 219-220); declaration of outside work, contributions, LLM usage, team none, acknowledgements, changelog (HF 222-232); artifacts and links (HF 16-26, but see F1); "for judges: one minute" (LP only, lines 35-103, not in HF).
Missing in HF, present in LP: threat model (F2); why this problem (F4); related work; samples pointer; "one minute" box.
Missing in both: general-capability retention benchmark (F3); embedding or MinHash leak check (stated as not run, HF 65-66); a forecast with more compute (stated as none, LP 14; HF says only "Next"); video or slides (shortlist stage, due 22 Nov); hosted demo (Colab notebook exists, link needs F1).
Not applicable: content warning (none found; chats are small-talk facts), optional cost/ROI vs closed API (declared none).
Rules checked from the overview page: dense open-weights Cohere model (Tiny Aya Global, yes); more than one before/after metric (yes); public HF model and dataset collections (linked, public and ungated per HF line 24; not opened, off-limits); team of 1 to 3 (solo); GitHub README with reproduction notes (exists locally; see F1).

## What holds up
The write-up covers every item on the R-217 list somewhere; the weak points are location (short vs long paper) and publication (F1). Claim labels, disclosures of the changed demo rule and of the 6.37-stays-shipped result are explicit. Counts in the HF headline match ARTICLE's summary table (spot-checked 8 numbers).
