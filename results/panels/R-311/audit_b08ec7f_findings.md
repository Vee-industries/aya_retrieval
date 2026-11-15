# Audit of b08ec7f (R-309, diff ca1af5d to b08ec7f)

Date 2026-11-15, 11:56 Eastern (HEAD had moved to 0fe68b1 by then; the audit is of b08ec7f). Repo and Hugging Face unchanged by me. Read: `git diff ca1af5d b08ec7f` (9 files), R-309 in
RECORDS.md, `results/panels/R-309/checked.md` and `review.md` (only through checked.md's account), `src/aya_retrieval/heldout3.py`
(`false_answer`, lines 536 to 556 only). Never-open list kept.

Result: **0 HIGH, 1 MEDIUM, 6 LOW.** No wrong number found.

## Checks run (all passed unless a finding says otherwise)

1. **Numbers in changed sentences.** Every generated key in a changed sentence was recomputed from the S3 run files with my own
   script (not the builder's):
   - `older` alone: base 30 of 356, 6.37 285 of 1,068, C1 292 of 1,068 (three seeds each). Right, and the builder's code fails if an
     `older` item holds its answer in the message.
   - Wider N-hit count: base 17 of 236, 6.37 402 of 708, C1 99 of 708 (listed-only counts 14, 286, 51 agree with the table).
   - K1.3 per seed: 9 and 28 of 236 (Appendix C line 1098 shows the same); base 14 of 236 gives 42.0 of 708, so a third seed needs
     5 or fewer to be at or under base's rate (37 + 5 = 42). "5 or fewer of 236" is right.
   - Section 9's six pairs (copies 5 of 894 against 195 of 894; N-hit 51 of 708 against 286 of 708; plain never-told 344 of 360
     against 238 of 360; statements 180 of 180 against 166 of 180; in view 161 of 180 against 160 of 180; base's plain never-told
     111 of 120) match the C1 card's table (a file this diff did not touch).
   - LongMemEval-S split (HF 124 to 128): 233 answerable plus 15 unanswerable is 248; 40 against 40, 23 right only for 6.37 and 23
     only for code, p = 1.0; 6.37's 53 against code's 40 leaves 13 on the unanswerable. The generator refuses to build if 6.37 differs
     from code or base on the answerable ones, or stops leading on the unanswerable ones.
   - Stage tables end R-309 in both papers; the changelog line and README line say R-307 and R-309.
2. **Claim strength.** Each changed claim is stated at or below its evidence except the points under L1 to L3 and M1.
   Specifically checked and fine: "above base, code and the whole chat at 58 messages, above base and code at 419" (R-166 out of
   memory at 419; R-168); "statements measure no gain over code" (code searches every turn, 0 of 40 left unsearched in README's own
   row); the K1.3 sentence ("it is not shown that what ships did not depend on the change", correct, and it names the third seed
   as not run); "6.37's plain never-told rate is under base's by more than the 5 points clause (a) allows" (66.1% against 92.5%, 26.4
   points); "6.37 stays shipped because no replacement passed the registered rule" (`ship_rule.json`, `pass: false`, (c) line only).
3. **Section 9 paragraph "6.37 and C1 against the same lines".** The direction is right: C1 is better than 6.37 on copies, N-hit
   and plain never-told, "no measured change in recall" (364 against 347 of 1,242 is the C1 card's line), 6.37 is higher on
   statements and in view. The reviewer's draft error (6.37 "below C1" on copies) is corrected. See L1 for one over-reading.
4. **N-hit term against `false_answer`.** The scorer flags a reply that names a value in `item.forbidden` (the writers' listed wrong
   values for the item) or `category_values` (the chat's values of the asked category), minus the item's answer and a confirm's
   claimed value; `None` for a statement. The new wording, "a value of the asked category listed for the chat", matches the second set
   and folds the first into it. See L3.
5. **Voice (kv_voice_v2).** Added lines in both templates, README and HANDOFF: 0 em or en dashes, 0 we/our/us, no hedge word from my
   list (may, might, perhaps, probably, seems, arguably, somewhat, roughly, quite, rather, just, simply, clearly, significant,
   robust, very, much, far, likely, appears). Whole files: ARTICLE, HF_ARTICLE, README 0 dashes and 0 we/our/us.
6. **Rebuild.** `git archive b08ec7f`, `make_article.py` with the venv python and `HF_HUB_OFFLINE=1`: exit 0. ARTICLE, HF_ARTICLE,
   ABSTRACT, MODEL_CARD, MODEL_CARD_C1 are byte for byte identical to the committed files. `git diff ca1af5d b08ec7f` shows no change
   to ABSTRACT.md, MODEL_CARD.md or MODEL_CARD_C1.md (Kevin's choice for the abstract holds), and the long paper's Abstract
   section is unchanged.
7. **Live copies**, fetched logged out from `resolve/main`: `aya-retrieval-6.37` ARTICLE.md (repo sha 91ab08f) = `HF_ARTICLE.md`;
   README = `MODEL_CARD.md`; `aya-retrieval-c1` README = `MODEL_CARD_C1.md`; `aya-retrieval-eval-logs` (repo sha 0fbc276)
   `panels/R-309/checked.md` and `review.md` = the repo files, and its README = `hf_eval_logs_card.md`. The dataset holds every
   tracked file of `results/` except `longmemeval/` (2,399 of 2,399, plus `.gitattributes` and README). `origin/main` is b08ec7f.
   Privacy: not rerun on the diff (no names in it that I read); the repo sweep of R-306 predates it. See "Not checked".
8. Tests: not rerun (the diff holds no code; the generator and tests are unchanged since a39473f, where I ran ruff, format and
   1,790 passed).

## MEDIUM

### M1. The 6.37 model card still says "above both references" at 58 and 419 messages

`docs/MODEL_CARD.md` 150 to 153, the sentence starts at 150 (template `docs/model_card_template.md`, live as the Hugging Face README of `aya-retrieval-6.37`):
"On the generated sealed pools this adapter is above both references on recall: 44 to 55 of 60 at each of 58 and 419 messages
against code's 14 to 32". The two references are code and the whole chat; the whole chat ran at 58 messages only (R-166 out of
memory at 419). R-309 item 1 fixed exactly this in the long paper (79 to 81, 613, 776) and the card was not changed, so the first
document a reader of the model page meets repeats the claim R-309 held as too strong. The numbers themselves are right (44 to 55 of
60 for seed 82, code 14 to 32).

Fix: "above code at 58 and 419 messages (44 to 55 of 60 against 14 to 32) and above the whole chat at 58 messages (46 to 55 against
21 to 33) (every sign test below 0.001; R-168)". Needs the template edit, a rebuild, a commit and a one-file upload of the README to
`aya-retrieval-6.37`. The card would no longer rebuild byte for byte against the old file, so say so in the record.

## LOW

### L1. Section 9 calls a one-question difference "better" for 6.37

`docs/ARTICLE.md` 666 to 673 (template `article_template.md`, the new paragraph): "6.37's are better on statements (180 of 180
against 166 of 180) and in view (161 of 180 (89.4%) against 160 of 180 (88.9%))". In view differs by one question and the same
paragraph calls recall (364 against 347 of 1,242) "no measured change". By the papers' rule ("no measured difference") in view is the
same kind of result as recall. Statements (7.8 points, 14 of 180) may be a measured difference but no interval is given in this
paragraph. Fix: "6.37's are better on statements (...) and level in view (161 of 180 against 160 of 180)".

### L2. The new LongMemEval-S sentence calls 53 against 40 a "lead", and two different 233s sit side by side

`docs/submission/HF_ARTICLE.md` 126 to 128: "its lead over code comes from the 15 unanswerable ones. 6.37 declines 233 of 470
answerable questions." The same document says 6.37 and code show no measured difference on answers (p = 0.12). A "lead" over code
that is not a measured difference reads as a claim. Also "the 233 answerable questions of the 248" and "declines 233 of 470" are
different counts that happen to match; a reader will see one number twice. Fix: "its higher total (53 against 40) comes from the 15
unanswerable ones" and "of the 248 judged, 233 are answerable; 6.37 ties code on those" (or move the "declines" sentence above the
split).

### L3. The N-hit Terms wording folds the writers' listed wrong values into "the asked category"

`docs/ARTICLE.md` 138, `HF_ARTICLE.md` 26, 175 ("names a listed value of the asked category"), 210 and ARTICLE 782. `false_answer`
reads two sets: `item.forbidden` (values the writers listed as wrong for the item) and `category_values` (other values of the asked
category in the chat). The C1 card (line 59 to 60) states both: "the asked category's values in that chat and the writers' listed
wrong values". The new wording is true if the writers' wrong values are always of the asked category, which no paper says. Fix
(Terms only): "a value listed for the chat: one of the item's listed wrong values or another value of the asked category in that
chat". Keep "asked category" in the other places only if that sentence is added once.

### L4. "On no outside set" cross-reference

`docs/ARTICLE.md` 672 to 673: "(sections 6.2, 6.3 and above)". The statement is true on the evidence I checked: outside-writer
recall below the whole chat and level with code; LongMemEval-S 53 against 40 (p 0.12), 40 against 40 on answerable; S3 code above
6.37. "and above" does not say where S3 is, and S3 is the one outside set where a baseline is measured above 6.37. Fix: "(sections
6.2, 6.3 and 9)".

### L5. The short paper grew 144 words

HF_ARTICLE.md is 2,927 words (2,783 at ca1af5d; R-305 held it at 2,761). R-309 states the change. Informational; length stays Kevin's
call (carried since R-305).

### L6. `older` alone is pooled over three seeds without saying so

`docs/submission/HF_ARTICLE.md` 179 to 180: "6.37 285 of 1,068 (26.7%), C1 292 of 1,068 (27.3%)" against base 30 of 356 (one run).
1,068 is three seeds of 356, the same pooling as Figure 3's caption, but the sentence does not say it. Fix: "6.37 and C1 pool seeds
82, 83 and 94".

## Not checked

The reviewer's `review.md` proposals other than through `checked.md`; the privacy sweep of the new diff (R-306's sweep predates
b08ec7f; the diff text contains no names I know of, and the live files are the repo's); the Appendix C figures not named in the
diff; whether 6.37's judged count on the 15 unanswerable questions is 13 and code's 0 (the generator's own checks hold it; the
LongMemEval files were not opened).
