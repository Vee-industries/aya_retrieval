# Lane 4: Reproducibility engineer (hostile)
Verdict: submit after fixes (F1 is a one-clause fix; the rest are minor)

## Round-2 findings: status (one line each)
N1 partly: README:466-467 and ARTICLE:743-744 were reworded, but the new sentence is still false (new F1).
N2 fixed: STANDARD.md:13-14 now says "every run and training file" and points to the README for analysis writers.
N3 not fixed: make_article.py:2461 still restates `rate(copy) <= rate(old copy) / 2` from score_s3.py:207.
N4 fixed in the long paper: a 15 November entry exists. Its range is wrong, and the README is behind (F3).
N5 partly: the C1 link, the download line (README:196) and `qs3_lock.py C1` (README:498) were added. qs3.sh:2 still says "PICK (K1 or K1.3)", and MODEL_CARD_C1 "How to use it" gives no load command.
N6 partly: section 15's list was extended. Typed and unlisted numbers remain (F2).
Older items, not fixed or carried: judges_check.json still does not parse; there is no constraints file (carried, R-298); `MAX_TOKENS = 60` is still defined in four modules; README:476 still says step 2 "reproduces" a file that step 1's retraining cannot reproduce (R-029).

## New findings (most severe first)
F1. [MAJOR] README:466-467, ARTICLE:743-744 (template:694-695): "the record that registered each analysis names the script that writes it" is false. `writeup_r164.py` is named in no record (`grep -c writeup_r164 RECORDS.md` = 0). `score_s3.py` first appears in R-282 (RECORDS:10198), not in R-281, which registered S3's analysis. `rigor_r139.py` appears in R-141 (RECORDS:5350), not in R-139. The first half also has one exception: `results/first_test/pre_repo_seed_24929.json` is a run file and has no provenance.
    Evidence: `panel4/l04/reg_names.py` (3 of 10 pairs NOT NAMED) and `panel3/l04/prov_scan2.py`, rerun on 48c6586 with the same counts as before.
    Fix: "the README's Reproduce steps and Layout table name the script that writes each analysis". Steps 3 to 7 already name all ten. Add "except the pre-repository first run".

F2. [MINOR] article_template:124 "236 of S3's 240 never-told items a run", :289 "30 a kind at each of 58 and 419 messages", and :615 and :790 "419 messages" are typed in. Section 15 lists only the 58-message size, and 419 is filled as `{{long_size}}` everywhere else.
    Evidence: `panel4/l04/lit_article_now.txt`, diffed against `panel3/l04/lit_article_template.txt`.
    Fix: fill these from `{{long_size}}` and ship_rule.json's `n`, or add them to the list.

F3. [MINOR] The changelog ranges. Template:762 says "15 November (R-290 to R-298)" but describes R-300's appendices and leaves out R-299's audit fixes. The README changelog ends at R-298, with no R-299 or R-300.
    Fix: "R-290 to R-300" in both, and name the audit (R-299).

F4. [MINOR] ARTICLE:763 says "the reopened work (12 to 14 November)". README:31 says "12 to 15 November", and RECORDS marks R-290 to R-300 as REOPENED on 15 November.
    Fix: "12 to 15 November".

F5. [MINOR] README step 3 names `final.sh` as if it runs alone. It is a fragment: it defines functions, needs `$VP` and `$W`, and is "sourced by a backlog line inside runner2.sh". runner2.sh hard-codes the author's paths. `qs3_lock.py` imports `msvcrt` (Windows only) and hard-codes `C:\Users\Gaming\scratch\card.lock`. Section 15's list of built documents leaves out the abstract and C1's card, which README step 6 includes.
    Fix: one clause, "final.sh is sourced by runner2.sh; both queues are kept as run, with the author's paths and Windows lock". Name the abstract and C1's card in section 15.

## What holds up
- R-300 removed no number. Every number token in ARTICLE.md at 83576b9 is still present at 48c6586 (2,712 to 2,737 tokens, only additions, and those are pointers). The abstract is identical (72 tokens). No built document has an unfilled `{{`. Every appendix pointer I checked (A: stages, LongMemEval; B: ledger; C: `re_ask`, other stored facts, report arms, Figure 8) lands on what it says.
- Every script in README "Reproduce" and section 15 exists, and every Python one has a usage line. Run files record `model_revision` af89d219 (55 of 55 sampled) and `git_dirty: false`. The package versions in the run files match CI's pins.
- Figures 1 to 8 run in order, and each image file exists.

Not done: ruff, pytest, make_article.py or make_figures.py (each writes into the repository); CI; network.
