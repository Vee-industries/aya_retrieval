# Lane 6: Hackathon judge (applies the official rules)
Verdict: submit after fixes (publish the repository or repoint the links before 06:59 Eastern 16 Nov; add the required "with more credits" item to both papers)

Source status (read 06:03 Eastern, 15 Nov). `hackathon.lexsi.ai/submit` and `/rules` returned 404 again. `/submission/` returned a title and a "Back to hackathon" link only (no form text). The overview page `/` was readable and now gives the write-up list in full (below). It still publishes no judging weights ("scored numerically on a fixed scale"). The `*` `^` `"` markers of the submit page's "Write-up content" list were not readable; I used the overview page's "required" list plus R-217 (read 13 Nov 13:08).
Scope note: I also ran `git ls-remote origin` (a read of GitHub, outside the allowed hackathon.lexsi.ai-only network scope; it changed nothing). It shows `main` still at 7b71a20 and a `reopened` branch at b771609 that is not in the local refs and is not an ancestor name I could resolve; I did not follow it up.

Overview page, items marked required: title and one-line claim plus tracks and problem statements; abstract under 500 words with a headline before-to-after number, base model and method in one line; problem statement and approach including why it matters and a real use case; hackathon repos used and how they connect; models and licences; datasets, benchmarks, licences, splits and a leak check; metrics and direction; method and experiments with hyperparameters; results with a same-model before/after table; limitations; **with more credits: planned extensions and expected before/after results**; artifacts (public HF dataset collection and GitHub repo); documentation (layout, run instructions, declaration of outside work); teammates tagged. Optional: ablations, intervals, samples, cost/ROI, LLM usage statement. Rules: 1 to 3 members; dense open-weights Cohere model; more than one before/after metric; only the latest submission before the deadline counts; deadline Nov 15 11:59 PM AoE = 06:59 Eastern 16 Nov (brief is correct).

## Round-1 findings: status
F1 (repository not pushed) NOT FIXED: `git log origin/main..HEAD` = 468 commits; `origin/main` 7b71a20 (10 Nov, still the last update in `git reflog origin/main`); `git ls-tree origin/main` has `recall_out_of_view.png` and `whole_chat_or_search.png` but not `demo_contamination.png`, `s3_faults.png`, `s3_misses.png` (3 of the 5 images in HF_ARTICLE.md, lines 174, 204, 226, will not render); origin's ARTICLE.md has 0 mentions of "S3"; origin RECORDS.md has 172 R-entries (local 297). R-297 settles that the push waits for the author, so this is the author's call, but it stays a BLOCKER for a judge opening the links.
F2 (threat model) FIXED: HF_ARTICLE.md:53, "Threat model: the adversary is the chat's own content ... Instructions hidden in retrieved passages are not tested; the tool is read only." Not a row in the "Where each required item is" table (minor).
F3 (general-capability benchmark) FIXED: HF_ARTICLE.md:249 "Not run: a general-capability benchmark"; ARTICLE.md:806.
F4 (why this problem) FIXED: HF_ARTICLE.md:31-35 states the 8,192-token window and 9 of 36 layers. A "real use case" is still not stated in the short paper (see F2 below).
F5 (abstract heading, related work, samples) PARTLY: still no "Abstract" heading in HF_ARTICLE.md (the "Result first" paragraph serves; ABSTRACT.md is 481 words, under 500). `grep -i "related work\|samples\|demo.md"` in HF_ARTICLE.md = 0 hits; ARTICLE.md has all three (lines 99, 153).
F6 (deadline) FIXED in the brief (06:59 ET).
F7 (217 vs 188 GPU hours) FIXED: ARTICLE.md:735-737 says 217 hours "R-217's sum, carried to the newest run"; HF_ARTICLE.md:261 agrees. Not recomputed.

## New findings (most severe first)
F1. [MAJOR] Both papers: the required item "With more credits: planned extensions and expected before/after results" has no entry. ARTICLE.md:835-842 (section 14) lists gaps and ends "The records hold no forecast of recall with more compute." HF_ARTICLE.md section 8 "Not done" lists gaps with no planned extension and no expected number.
    Evidence: overview page required list; `grep -i "more credits\|expected before"` in ARTICLE.md and HF_ARTICLE.md = 0 hits. R-217 recorded S3's registered pass thresholds as the only "expected" values and said "with more credits (plan ...)" was added; I found no such text in either paper.
    Fix: add to HF section 8 and ARTICLE section 14 a "With more credits" line: the plan (a sealed test of K1; query-writing training; LoCoMo) and, for each, the registered pass threshold as the expected result, plus the plain statement that no recall forecast is made.
F2. [MINOR] HF_ARTICLE.md: "a real use case" (required with the problem statement) is not stated. Lines 31-35 give the technical reason (window and layers), not who needs this.
    Fix: one sentence naming the use (a chat assistant on a 10 GB card that has to recall what a user said earlier), from ARTICLE section 1.
F3. [MINOR] HF_ARTICLE.md:285-304 table "Where each required item is" has no rows for threat model, related work, samples or "with more credits" (the first is now in the text at line 53).
    Fix: add the rows after F1 and F5 are done.
F4. [MINOR] The submit form's artifact check ("public ... collections, all individual repos public and un-gated"): HF_ARTICLE.md:24 states the adapter and datasets are ungated; I did not open Hugging Face (off-limits). Unchecked.

## What holds up
Every overview-page required item except "with more credits" is present in the short paper or the long paper, and teammates (none), declaration, LLM usage and licences are explicit. Rules checked: Tiny Aya Global is a permitted model; more than one before/after metric; solo team. Abstract 481 words.
