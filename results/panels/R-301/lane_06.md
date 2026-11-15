# Lane 6: Hackathon judge (applies the official rules)
Verdict: submit after fixes (publish the repository before 06:59 Eastern 16 Nov; add the datasets-collection link to the short paper)

Source status. `hackathon.lexsi.ai/` was readable and lists every write-up item with its marker (required `*`, optional `^`, track `"`). `/submit` returned 404; I used the overview page. No judging weights are published ("score each team numerically on a fixed scale"). Deadline 15 Nov 23:59 AoE = 06:59 Eastern 16 Nov. I ran no git command that contacts a remote; push state comes from local refs.

## Round-2 findings: status
F1 ("With more credits" missing) FIXED: HF_ARTICLE.md:168 and ARTICLE.md:730 now state the plan, the expected result (S3's rule, pass or fail) and K1's S3 numbers (253 of 828; 12 of 472 vs base 14 of 236), and say no recall forecast is made.
F2 (real use case) FIXED: HF_ARTICLE.md:31 "The use: a chat assistant on a small model that must recall what a user said long ago".
F3 (checklist table in short paper) MOOT: the table was removed in the R-298 rewrite; see New F2.
F4 (artifacts public and ungated) not checked: Hugging Face is off-limits for this lane. The short paper does not say "ungated"; the long paper does (ARTICLE.md:104).
Round-1 F1 (push) NOT FIXED: `git for-each-ref` shows `origin/main` still 7b71a20; `git log origin/main..HEAD --oneline | wc -l` = 471. `git ls-tree origin/main figures/` lacks `demo_contamination.png`, `s3_faults.png`, `s3_misses.png`, so 3 of the 5 images in HF_ARTICLE.md will not render, and the linked ARTICLE.md on main is the 10 Nov version. The author's plan is one push at the end (brief); it stays a BLOCKER until done.

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md:20-26: the required artifact "HF datasets collection" is not linked in the short paper. It links the two adapters and GitHub only.
    Evidence: `grep -n "collections\|aya-retrieval-chats\|eval-logs" docs/submission/HF_ARTICLE.md` = 0 hits; the links exist in ARTICLE.md:97-100.
    Fix: add the models-collection, datasets-collection and the two dataset links (copy ARTICLE.md:96-100) to the "Adapters:" paragraph, and "public and ungated".
F2. [MINOR] HF_ARTICLE.md: several required items exist only by pointer to the long paper: metrics with direction (ARTICLE.md:323), datasets, sources and splits (section 3), Track 3 trajectories and trajectory metrics (ARTICLE.md:200-202), "Known weaknesses" is covered (section 7). The short paper names none of the first three; the pointer at lines 22-24 lists "hypotheses, deviations, leakage and flow tables and the limits" but not metrics or trajectories.
    Fix: one sentence in the line 22-24 pointer: "metrics and which direction is better (section 5), data sources and splits (section 3), trajectories and their metrics (section 6)". Check the section numbers against ARTICLE.md headings before writing.
F3. [MINOR] ABSTRACT.md and HF_ARTICLE.md have no "Abstract" heading in the short paper; ABSTRACT.md is 465 words by `wc -w` including the title, so under 500. The opening "Result first" paragraph serves. Optional only.

## Item check (overview page list; short paper first, then long paper)
Present in short paper: title and claim (1, 3-12); track and problem statement (29-31); abstract (ABSTRACT.md); headline before to after (5-9; table in ARTICLE.md:47); base model and method (44); problem and use (31-34); toolkits and how they connect (44-48); licences (line 178); leak check (46-49); hyperparameters (rank 32, pointer to long section 4; values at ARTICLE.md:266); results with same-model table (70-76); limitations (148-164); with more credits (168); declaration and teammates (181); LLM usage (180); reproduction (172).
Long paper only: metrics and direction, trajectories, related work (161), samples, appendix. Appendix pointers checked (A: ARTICLE.md:422, 431; B: 482; C: 564, 591, 594, 695, 964): each appendix holds what the pointer says.
Not run, stated: general-capability benchmark (HF 163).

## What holds up
Required "With more credits" and "real use case" now present in both papers. Rules: Tiny Aya Global is a permitted dense Cohere model; more than one before/after metric; solo team; only the latest submission counts. The appendix pointers after the R-300 shortening resolve.
