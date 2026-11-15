# Lane 4: Reproducibility engineer (hostile)
Verdict: submit after fixes (N1 and N2 are one-sentence fixes; the push stays the author's call, R-297)

## Round-1 findings: status
F1 not fixed, settled (R-297): `git rev-list --count origin/main..main` = 468 (was 465). ARTICLE:97 still calls the eval-logs dataset "every trajectory", and `docs/submission/hf_eval_logs_card.md` still lists no S3 file. Both become true only after the upload that waits on the author.
F2 partly fixed: the sentence was reworded at README:489-490 and ARTICLE:846-847, but the new wording is also false (N1). `results/analysis/R-170/judge/judges_check.json` still begins with the torch `W1110 ... Redirects` line and does not parse.
F3 fixed: README:191-196 adds `hf download CohereLabs/tiny-aya-global --revision af89d219...`.
F4 fixed: README:491-494 and ARTICLE:847-849. I checked the claim by rescoring both tests (see "What holds up").
F5 fixed: `scripts/records/queue/qs3.sh` and `qs3_lock.py` are committed, and README:519-520 points to them. A small issue remains (N5).
F6 partly fixed: README:198-200 now says that CI's pins are the tested versions and that a newer local install is not the tested one. No constraints file was added, and pyproject.toml still gives `transformers>=5.15` with no peft or trl.
F7 not fixed: the list of typed numbers in section 15 (ARTICLE:856-858) is unchanged, and the fixes added more typed numbers (N6).
F8 partly fixed: ARTICLE:186 now cites `MAX_TOKENS` in `scripts/run_recall_eval.py`. `MAX_TOKENS = 60` is still defined separately in four modules: run_recall_eval.py:66, src/aya_retrieval/chat.py:20, scripts/run_build_training_set.py:61 and scripts/records/score_r170.py:67 (a copy under the card rule).
F9 fixed: README:536 says "other test files".
F10 partly fixed: README:198 gives the Linux path. Step 2 (README:498) still says it "reproduces" `hd_fix17cs37_82_seed_73157.json`, but step 1 trains into the same `../adapters/screens/fix17cs37_82` folder, and retrained weights differ (R-029).

## New findings (most severe first)
N1. [MAJOR] README:489-490, ARTICLE:846-847 (article_template:725): "each analysis file names the script that writes it" is false. 721 of 1,822 JSON files under `results/` (results/longmemeval left out) have no provenance block. Of those, 716 contain no `.py` name anywhere, among them the confirmatory `results/analysis/R-162/A.json` to `D.json` and `results/s3/ship_rule.json`, which holds only `record: R-281`. The other half of the sentence has one exception too: the run file `results/first_test/pre_repo_seed_24929.json` has no provenance.
    Evidence: `panel3/l04/prov_scan2.py`, which counts by folder: prov 1,101; no prov and no script 716; no prov but names a .py 4; unparsable 1.
    Fix: "each analysis folder's writing script is named in the README's results table". README:471 and 483 already name them.

N2. [MAJOR] STANDARD.md:12-13 (repository copy): "`src/aya_retrieval/provenance.py` writes this record into every file under `results/`" is false by the same count. It also contradicts the corrected README sentence. I missed this in round 1.
    Evidence: as N1.
    Fix: "into every run and training file under `results/`".

N3. [MINOR, card rule] scripts/make_article.py, `s3_panel_numbers`: the measured clauses (a) to (c) of the ship rule are written out inline a second time, copied from `score_s3.rule` (score_s3.py:184-216; for example `rate(copy) <= rate(old copy) / 2`), so that they can be applied to the report arms. The claim they support holds. I ran `score_s3.rule` itself on each arm, renamed to `pick`: K1 6 of 6 measured lines, K2.1 6 of 6, K1.3 5 of 6 failing (c), C1 5 of 6 failing (c). If the rule changes, though, the two copies can drift apart.
    Evidence: `panel3/l04/report_arms_rule.py`.
    Fix: give `score_s3.rule` an `arm` parameter and call it from make_article.py.

N4. [MINOR] The long paper's changelog (ARTICLE:885-897) ends at "14 November, audit fixes (R-289)" and still labels "14 November (R-287 on), this version". README:564 says the same. HF_ARTICLE:270-274 lists the 15 November changes (R-294 to R-297) and says "The long paper's changelog has each step's records". It does not.
    Fix: add a 15 November entry to the long paper's template and to the README.

N5. [MINOR] README:492 says C1 seed 82 is published but gives no link to it and no download line; the README links only aya-retrieval-6.37 (lines 13, 20, 220, 224). `docs/MODEL_CARD_C1.md` "How to use it" (lines 72-77) gives no load command. `qs3.sh:2` says "Usage: qs3.sh PICK (K1 or K1.3)", but the queue was run as `qs3_lock.py C1` (RECORDS:10347), and README step 7 does not give the argument.
    Fix: add the C1 link and `hf download KevinVaillancourt/aya-retrieval-c1 --local-dir ../adapters/screens/k13opc1_r263_82`; write `qs3_lock.py C1` in step 7.

N6. [MINOR] Section 15 says that every result number is filled from results files except the ones it lists. The R-297 fixes added typed numbers that are not on the list:
    - article_template:118 "236 of S3's 240 never-told items a run";
    - article_template:718 "chat at 419 messages", which is filled as `{{long_size}}` everywhere else;
    - article_template:58 "whole chat at 58 messages";
    - article_template:186 "60 tokens".
    Each matches its source: 236 and 240 are `n` values in ship_rule.json, 58 is a size key in `results/analysis/R-168/refs.json`, and 60 is `MAX_TOKENS`. The round-1 items are still typed and unlisted, for example "all 20 screening lines" (article_template:525, hf_article_template:185).
    Evidence: `panel/l04/literal_numbers.py`, run on the 0e8b421 and 8735c87 templates and diffed (`panel3/l04/lit_*.txt`).
    Fix: fill these numbers from results files, or add them to the section 15 list.

## What holds up
- Both confirmatory results rescore exactly from the committed files. `score_r162.py`, run in a scratch copy (`panel3/l04/rescore/`), gives A.json to D.json with 0 differences from the committed files. `score_s3.rule`, computed in memory with the committed tally, equals `results/s3/ship_rule.json` exactly, (c) FAIL included (`panel3/l04/rescore_s3.py`). The repository tree stayed clean.
- Every script named in README "Reproduce" and in section 15 exists, including qs3.sh, qs3_lock.py and draw_s3_sample.py, and each Python one has a usage docstring. The package versions recorded in all 15 S3 run files match CI's pins: transformers 5.22.1, peft 0.21.2, trl 1.7.1, huggingface_hub 1.33.0. All 15 have `git_dirty: false`.
- The README's S3 counts match ship_rule.json: 51/708, 286/708 and 14/236 on N-hit; 5 and 195 of 894 on copy; 364 and 347 of 1,242 on recall; 161 and 274 of 414.

Not done: ruff, pytest and a rebuild by make_article.py (each writes into the repository, or would read sealed data); any CI or network check.
