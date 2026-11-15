# The ten lanes (each reviewer gets its own line; all read BRIEF.md first)

1. Retrieval and tool-use researcher (hostile). Does the work show what problem statement 4 asks: deciding when and
   what to retrieve, grounding answers in retrieved text, ignoring distracting documents? Do the measures show that,
   or something narrower? Are the baselines (base with the whole chat, code that searches every turn, base with the
   tool, the prompted baseline) the strongest simple ones, with an equal tuning budget? Is related work stated fairly
   and is anything relevant missing?
2. Statistician and experimental designer (hostile). Are the confirmatory claims supported: sealed tests opened once,
   pass rules registered before results, intervals (chat-resampled bootstrap, Wilson), seeds pooled or per seed, the
   test family and its handling, the S3 ship rule's reading choices (R-281), sample size and power? Recompute a sample
   of reported numbers from the results files with short read-only Python.
3. Evaluation and leakage specialist (hostile). The test chats are written by Claude agents and judged by Claude
   agents; the first sealed pools are generator-built; the demos were contaminated. Check the leakage table by Kapoor
   and Narayanan type, the contamination statement for the pretrained model, the scorer's validity (rule-based string
   matching), the coherence judges never checked against a person. Is any claim built on an instrument too weak for
   it, and are the limits stated in full?
4. Reproducibility engineer (hostile). Could a stranger rerun this from the README? Check setup, every command named in
   the README's "Reproduce the results" and the long paper's section 15 (that each script exists and documents its
   usage; do not run training, evaluation or `make_article.py`, which writes into the repository), provenance fields
   in a sample of results files, pinned versions and model revision, CI. Check that the numbers section 15 lists as
   typed from the record are the only ones not computed by `scripts/make_article.py`.
5. AI safety and alignment reviewer (hostile). This is an AI safety hackathon. Is the safety relevance concrete and
   true (declining when never told, not copying a wrong answer, not inventing a value after an unrelated search)?
   Is the threat model honest about what was not tested? Is anything about safety overclaimed? Are the reopening and
   the rule changes made after readings disclosed with full integrity?
6. Hackathon judge (applies the official rules). Read hackathon.lexsi.ai/submit, the "Write-up content" list (`*`
   required, `^` optional, `"` by track; Track 3 items count as required), and any judging criteria or rules pages
   on hackathon.lexsi.ai. Check every item against the short paper first (the write-up a judge is most likely to
   read), then the long paper and the abstract. List each item: present (where) or missing. If a page cannot be read,
   say so and use RECORDS.md R-217, which lists the items as read on 13 November.
7. Research-standard auditor. Read `C:\Users\Gaming\Desktop\Claude's House\STANDARD.md` rules 2, 3, 4, 8, 9, 13, 15,
   16, 18 to 22, 26, 29, 30 and 38. For each, does the long paper meet the report-side requirement (hypotheses and
   deviations tables, limits under rule 22's headings, every claim labelled confirmatory or exploratory, every
   difference with effect size, interval, n and test, controls, baselines, flow table, leakage table)? Name the rule
   and the location of each gap.
8. Voice editor. Read `C:\Users\Gaming\Desktop\papers\Paper 1\kv_voice_v2.md` in full. Then read the short paper, the
   abstract, and the long paper's Abstract, Submission summary and sections 1, 7, 8, 9, 12 and 14, line by line.
   Report every breach with its line and a replacement sentence. A scanner's raw hit list is at
   `C:\Users\Gaming\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\side-session-notes\local_f171c9ff-2a22-4e72-96cd-efd7d112faef\voice_hits_27f6906.md`;
   its hits are candidates, not breaches ("as often as" or "could not" can be plain statements of fact).
9. Against (hostile, the strongest case against submitting as is). Argue that the write-up should not be submitted in
   its present form, or that its headline misleads a judge. Attack the headline result (generated sealed chats where
   base is weak, against outside-writer chats where the whole chat and plain code beat the adapter), the reopening and
   the rule changes made after readings, the length and structure, and anything else that would cost it with a
   judge. For each point, name the change that would answer it.
10. Practitioner (critical). An engineer who builds chat assistants with memory. Read the short paper first, as a
   judge with ten minutes would. Is the story clear and in order? Can you tell what was built, what works, what does
   not, and what to use when? Is anything confusing, too dense or buried? Does the short paper stand without the long
   one? Then look at each figure the short paper shows (`figures/*.png`) and say whether it reads at a glance.
