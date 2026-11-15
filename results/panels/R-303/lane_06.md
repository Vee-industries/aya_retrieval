# Lane 6: Hackathon judge (applies the official rules)
Verdict: submit after fixes (publish to GitHub main before 06:59 Eastern 16 Nov; one MINOR pointer sentence)

Source status. hackathon.lexsi.ai/ read on 15 Nov: it lists every write-up item (legend: `*` required, `^` optional, `"` by track, `+` hiring). The page cannot confirm that /submit resolves (round 3: 404). No judging weights are published. Deadline "Nov 15, 11:59 PM AoE" = 06:59 Eastern 16 Nov; the latest submission counts. Rules: public HF collections and a write-up (HF article or README); Track 3 does not need two chained repos. No git command contacting a remote was run.

## Round-3 findings: status
F1 (datasets collection not in short paper) FIXED: HF_ARTICLE.md:20-26 links both adapters, both datasets, and the models and datasets collections.
F2 (metrics, data sources, trajectories only by pointer) NOT FIXED, still MINOR: HF_ARTICLE.md:22-26 says "holds every table and limit" and names none of them. `grep -n -i "metric\|direction" HF_ARTICLE.md` finds no metrics list. Long paper holds them: ARTICLE.md:214-216 (trajectories), :337 (metrics and direction), section 3 (data).
F3 (no "Abstract" heading) unchanged, optional; ABSTRACT.md is 495 words by `wc -w`, under 500 (close to the limit).
Round-1 F1 (push) NOT FIXED: `git for-each-ref` still shows origin/main 7b71a20; `git log origin/main..HEAD` = 473 commits; `git ls-tree -r origin/main` has none of demo_contamination, s3_faults, s3_misses. All three figures in HF_ARTICLE.md use raw.githubusercontent.com .../main/figures, and 2 of the 3 (Figures 2, 3) will not render until the push. The linked ARTICLE.md on main is the 10 Nov version. The author's plan is one push at the end; BLOCKER until done. The brief makes it a known step, not a new finding.

## New findings
F1. [MAJOR, conditional] Publication state: the rules require all artifacts public by the deadline. Until the push and the HF uploads happen, GitHub main and the links a judge opens do not match the submitted write-up. I could not read Hugging Face (off-limits), so the dataset and adapter links are unchecked.
    Fix: push, upload, then open every link in HF_ARTICLE.md from a logged-out browser before submitting.
F2. [MINOR] HF_ARTICLE.md:22-26: add one sentence to the pointer: "metrics and which direction is better (long paper section 5), data sources and splits (section 3), trajectories and their metrics (section 3, 'Trajectories')." Section numbers checked against ARTICLE.md headings (## 3 at line 204; metrics at 337 under ## 5).
F3. [MINOR] "How the repos connect" is one sentence (HF_ARTICLE.md, section 1 last paragraph). Required item; acceptable, but a judge scoring by checklist may want it as its own labelled line.

## Item check, required items in the short paper
Title and claim (1-12); tracks and problem statement (29-31); abstract (ABSTRACT.md); headline before to after (5-9); base model and method (69); problem and use (31-34); kits used and how they connect (section 1); models and licences (line 178 and section 1); data sources, splits and leak check (section 1, 46-49); training setup (rank 32, projections, section 1); results with same-model table (section 3 and 6); limitations and known weaknesses (section 7); with more credits, planned approach and expected before/after (section 8); artifacts: datasets collection, models collection, GitHub (20-26); reproduction (section 8); declaration of outside work (section 8); teammates (section 8). Long paper only: metrics list, trajectories, related work, extra tables, sample outputs, changelog, references.

## What holds up
Every `*` item is present in the short paper or, for metrics and trajectories, in the long paper. Appendix pointers resolve (A, B, C headings at ARTICLE.md:871, 951, 985). The "Not run: general-capability benchmark" statement is present.
