# Lane 4: Reproducibility engineer (hostile)
Verdict: submit after fixes (F1 must be done before the form goes in; F2 and F5 are one-sentence fixes)

## Findings (most severe first)
F1. [BLOCKER] Public GitHub repo vs README/ARTICLE "Reproduce": the repository a stranger clones is 465 commits behind local `main`. It has no `results/s3/`, `scripts/run_s3_eval.py`, `scripts/records/score_s3.py` or the rebuilt write-ups, so README step 7 and section 9 cannot be checked. The Colab link points at `main`. CI has never run on the state being submitted.
    Evidence: `git rev-list --count origin/main..main` = 465 (0 the other way); `origin/main` = 7b71a20, 2026-11-10 13:31, set by the last push (reflog); `.git/FETCH_HEAD` from 2026-11-13 14:01 still shows 7b71a20; `git diff --stat origin/main main -- results/s3 ...` adds all S3 files; HANDOFF.md:15 "Nothing pushed"; R-217 (RECORDS 8885). The HF eval-logs card (`docs/submission/hf_eval_logs_card.md`) lists no S3 file, yet ARTICLE:80 says the dataset holds "every trajectory". Not checked: the live GitHub/HF pages (no network in this lane).
    Fix: push `main` (Kevin's yes), upload `results/s3/` run files to aya-retrieval-eval-logs, re-upload HF_ARTICLE.md, and confirm CI is green on the pushed commit.

F2. [BLOCKER, false claim; the fix is one sentence] README "Reproduce the results" and ARTICLE section 15: "Every results file ... carries its provenance (command, commit, package versions)". 720 of 1,822 JSON files under `results/` (results/longmemeval left out) have no provenance block. These include 37 of the 41 files in `results/analysis/`, among them the confirmatory scores `results/analysis/R-162/A.json` to `D.json`, and `results/s3/ship_rule.json`. `results/analysis/R-170/judge/judges_check.json` is not valid JSON: a torch stderr warning line comes before the array.
    Evidence: `panel/l04/prov_scan.py` (counts by folder); `head -c 300 results/analysis/R-170/judge/judges_check.json`.
    Fix: reword to "every run and training file carries its provenance; each analysis file names the script that writes it". Alternatively, add `run_metadata()` to the score scripts. Strip the warning line from judges_check.json.

F3. [MAJOR] README "Setup": there is no step that downloads the base model, but `load_model` calls `snapshot_download(..., local_files_only=True)`. On a fresh machine every README command that loads the model fails. Only the notebook downloads it.
    Evidence: src/aya_retrieval/models.py:23; README:167-192 (licence and login only).
    Fix: add `../venv/Scripts/hf download CohereLabs/tiny-aya-global --revision af89d219b53ed9b13b8a4645f9c8028973510324`.

F4. [MAJOR] README steps 3 and 7: neither confirmatory test can be rerun by a stranger, and the README does not say so.
    - Sealed rule 1 pools eight seeds. S3 needs 6.37 at seeds 83 and 94 plus C1, K1, K1.3 and K2.1. Only seed 82 is published.
    - Retraining does not give the same weights (R-029), and only seed 82's hashes are sealed.
    - `final.sh` depends on `runner2.sh`, which hard-codes the author's paths and a session scratchpad.
    Evidence: the only HF model link in any document is aya-retrieval-6.37 (grep of README, ARTICLE, MODEL_CARD, submission/); runner2.sh:3-5; final.sh:4-5 and 20-21; docs/submission/PUBLISH.md:10.
    Fix: one sentence in README and section 15: the confirmatory results can be checked by rerunning `score_r162.py` and `score_s3.py` on the committed run files, but cannot be rerun from scratch; or publish the other adapters.

F5. [MAJOR, false pointer] README step 7: "the queue `qs3.sh` is in R-194 and R-280". R-194 never names it. R-280 says it was copied into session 77d169a0's scratchpad. It is not in the repository.
    Evidence: RECORDS 7820-7843 (R-194, no "qs3"); first mention at line 9393; R-280 at 10151-10152; `grep -rln qs3` outside data/ finds only docs, README, HANDOFF, RECORDS and score_s3.py.
    Fix: commit qs3.sh and qs3_lock.py as run into `scripts/records/queue/` (as R-157 did for the other queue scripts), or change the pointer to "described in R-280".

F6. [MAJOR] README "Setup": the local install does not pin the versions the results were made with. pyproject gives `transformers>=5.15` and `huggingface_hub>=1.4`, with no peft, trl or accelerate. `pip install -e ../vendor/AgentTune` resolves AgentTune's own dependencies to whatever is current. CI pins transformers 5.22.1, peft 0.21.2, trl 1.7.1 and the rest; every run file records them.
    Evidence: pyproject.toml dependencies; .github/workflows/ci.yml install step; provenance `packages` in hd_fix17cs37_82_seed_73157.json.
    Fix: commit a constraints file with CI's pins and add `-c constraints.txt` to the README install lines.

F7. [MINOR] ARTICLE section 15's list of typed numbers is incomplete. Other numbers are also typed into the templates:
    - "each in 3 rows of `data/screens/fix17cs37.jsonl`" (article_template:412, model card:213). Correct: grep gives 3 and 3.
    - "`check_k3.py`, 0 FAIL" (article_template:445).
    - "passed all 20 screening lines" (article_template:506, hf_article_template:164).
    - "every sign test below 0.001" (model_card_template:133).
    Evidence: `panel/l04/literal_numbers.py` over the four templates.
    Fix: add them to the section 15 list, or fill them in make_article.py.

F8. [MINOR] ARTICLE section 3 (template:168) says replies stop at 60 tokens and cites `src/aya_retrieval/harness.py`. The limit is `MAX_TOKENS = 60` in scripts/run_recall_eval.py:66, and the same constant is copied in src/aya_retrieval/chat.py:20 (a second copy, reported under the card rule).
    Fix: cite run_recall_eval.py; have one module import the other's constant.

F9. [MINOR] README "Checks": "runs the other 24 test files". `tests/` now holds 30 `test_*.py` files, so 29 other files. 24 was right for origin/main, which had 25.
    Fix: change it to 29, or drop the count.

F10. [MINOR] README step 2 says it "reproduces" hd_fix17cs37_82_seed_73157.json. That is only true with the published adapter, not one retrained in step 1 (R-029). All commands are Windows-only (`../venv/Scripts/`), and the provenance `command` fields hold absolute author paths. `freeze/heldout3_stage1.json` was written with `git_dirty: true`.
    Fix: add "with the published adapter" to step 2, and give the Linux path (`../venv/bin/`) once.

## What holds up
- All 31 scripts named in README "Reproduce" and section 15 exist, except qs3.sh (F5), and each Python one has a usage docstring (`panel/l04/usage_check.py`).
- Base revision af89d219 is pinned in models.py and recorded in all 18 run files sampled (15 S3, 3 sealed). Every run file with provenance has `git_dirty: false` except the one named in F10. The 4 sampled commits exist in history.
- README numbers sampled (7.83 GiB, 2,054 s training, 42/47 code recall, 233 of 470) match the results files and ARTICLE.

Not done: ruff and pytest (they would write caches into the repository), any network check, and AgentTune's own dependency pins (outside the repository).
