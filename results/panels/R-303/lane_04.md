# Lane 4: Reproducibility engineer (hostile)
Verdict: submit after fixes (F1 and F2 are one-line fixes; the rest are minor)

## Round-3 findings: status (one line each)
F1 fixed: README:484-486, ARTICLE:792-793 now say the Reproduce steps and Layout table name each writer, except the pre-repository run.
F2 partly: 419 and 236/240 are now filled; other typed numbers remain (new F3).
F3 partly: ranges now "R-290 to R-301" with R-299 named; R-302 is missing (new F4).
F4 fixed: ARTICLE:813 "12 to 15 November".
F5 fixed: final.sh sourced by runner2.sh, author's paths and Windows lock stated; section 15 names the abstract and C1's card.
Carried, not fixed: no constraints file (pyproject `transformers>=5.15`, peft unpinned; README:185-187 says so); `results/analysis/R-170/judge/judges_check.json` is captured console text, not JSON; `MAX_TOKENS = 60` in four modules; make_article.py:2499 restates score_s3.py:207; qs3.sh:2 usage names only K1/K1.3; neither model card has a load command.

## New findings (most severe first)
F1. [MAJOR] README:216-220: the training command, run as written, overwrites committed files. It has no `--report-name`, so run_recall_train.py:304-307 writes `results/recall_train/seed_82.json`, which is the committed report of v2's 2 November run. Its `--out-dir` is the folder the README's `hf download` fills, so it replaces the published weights that step 2 scores. It also drops `--save-epochs 2` from the recorded command. Per its help text, that flag only saves an extra checkpoint.
    Evidence: provenance command in `results/recall_train/fix17cs37_82.json` and `seed_82.json`.
    Fix: add `--report-name fix17cs37_82_retrain` and `--out-dir ../adapters/retrain/fix17cs37_82`.

F2. [MAJOR] HF_ARTICLE:216 "The README gives every command" is overstated. The README has no command for C1. C1 was trained in two passes on `k13op_82_r253.jsonl` with `--init-adapter`, starting from K1.3 seed 82, which is unpublished. Candidates and report arms have no commands either.
    Evidence: `results/recall_train/k13op_r253_82.json`, `k13opc1_r263_82.json`; `grep run_recall_train README.md` gives 1 hit.
    Fix: "The README gives 6.37's commands; every other run's command is in its run file's provenance."

F3. [MINOR] Numbers typed into templates that section 15 does not list: the 50 marked lines (article_template:703-704, 777; hf template:198; model_card_template:191, 241), "of 96" (article_template:294, 666), and the screening gate's thresholds (467-468). Section 15 does list R-015's thresholds.
    Fix: add these three to section 15's list.

F4. [MINOR] README:565 and template:799 say "R-290 to R-301, this version". This version is R-302 (S3 table, PDF figures, abstract cuts). PUBLISH.md:63 says "R-173 to R-301".
    Fix: "R-290 to R-302", and name R-302's audit.

F5. [MINOR] README:510 uses a bare `python`. Every other command uses `../venv/Scripts/python`.

F6. [MINOR] PUBLISH.md step 3 uploads only `results/s3/` and no data. Its own table sends all of `results/` and `data/screens/` to the datasets. The reopened runs and training sets would then be on GitHub only.

## What holds up
- The README's S3 table matches `ship_rule.json` (15 counts), and its LongMemEval table matches Appendix A.
- The training data for 6.37 and for C1 is unchanged since their training commits (`git diff --quiet`). C1's "26 minutes" is 764 + 770 s.
- The figures come out deterministic (`svg.hashsalt`, no timestamps). The appendix pointers I checked hold what they say.

Not done: ruff, pytest, CI, make_article.py, make_figures.py, network.
