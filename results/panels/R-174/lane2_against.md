Against lane, panel R-174. I read the brief, lane2_method.md, demo_transcripts.md, synthesis.md and repo files inside the brief's limits. I edited nothing, ran no model and ran no git write. One `find` over scratch ran too long, and I stopped it.

## New evidence the panel did not have
- **Both wrong answers used search queries copied word for word from 6.37's training set.** Command: `grep -c -i "<q>" data/screens/fix17cs37.jsonl`. "sister broke skiing injury" appears in 3 rows, each time as a `search_corpus` query. "brother new job" also appears in 3 rows. On "what did i fix under the sink", 6.37 sent the skiing query, a training query with nothing to do with the question. That is memorized output.
- **The two earlier adapters declined both of these questions.** `results/demo/v5_82.json` and `fix15_82.json`, turns 12 and 14: "I don't have that from you." 6.37 now gives an unrelated fact as the answer. Against its own ancestors on this demo, 6.37 has gone backwards.
- **The 05:05 output JSON is not in the repo.** `git status --porcelain --untracked-files=all` shows only 5 modified files, all from the R-173 edits. The raw JSON, with its provenance (10:05Z, 7b71a20), has to be found and committed byte for byte. A hand copy does not meet "a committed file behind every claim".
- **The working tree is dirty right now** (README, ABSTRACT, HF_ARTICLE, article_template, make_article.py). Any new GPU run or commit has to be sequenced after those edits.
- **The transcript does not record what each search returned.** The keys are only message, queries and reply. My guess is that the OR-match index (`match_all=False`, exchanges include the model's own replies) brought back turn 6, "Tobias... a new city". That guess is unverified and must be labelled as a guess if it is used.

## 1. The four wishes
- **(a) Showing the demo whole raises the scores more than it costs: wrong as framed.**
  - Its only fair headline: "searched on all 4 questions and none of the 11 other lines; 2 of 4 right; on the other 2 it searched with a query copied from its training data and gave an unrelated fact."
  - For a memory assistant, confident misattribution is the failure an industry judge weighs most. Base was right on the never-told question.
  - The honest expectation is a clarity gain and a usefulness loss. Those scores are not the decision rule, though. Now that the failure has been seen, it must be in the limits whether or not the block ships.
- **(b) The notebook works for a judge: not shown, and partly wrong.**
  - Part B needs a Hugging Face account, a licence click that shares contact details with Cohere, a token, and a Colab secret. The default pick of a "read-only fine-grained token" fails with a gated-repo error unless "read access to public gated repos" is ticked.
  - The design never names `accelerate`. `load_model` uses `device_map={"":0}`, which needed accelerate in transformers 4.x (unconfirmed for 5.22.1). The recorded environment had accelerate 1.15.0 (`pip list` in ../venv).
  - Nothing on a T4 can be checked before the push.
- **(c) CI is worth its time before Nov 15: mostly holds.** About 1 to 1.5 h, every pinned version exists (all installed in ../venv), and the CI design is sound. Its gain is small, a badge and a green Actions run. The real risk is only a red public run.
- **(d) Running before registering is a minor slip: wrong.** Pre-registration exists to fix the publish and grading choices before the result is known. Disclosure tells the truth about the order but does not bring that guard back. Every choice still open (ship, drop, add a set, grade) is now made with the result in hand.

## 2. The demo
**Honest way to present it:**
- Show all 15 turns of both models, built by a script from the committed JSONs.
- Add the v5 and fix 15 rows for turns 12 and 14. Their transcripts are already committed, and README line 195 points to that folder.
- Use the grading rule the method lane wrote before it saw the result, unchanged, so the sink answer "a leaky faucet" counts as wrong for base too.
- State the training-query finding with its file and counts.

**Dropping the block now is selective reporting.** It was planned as "published whatever it shows" (lane2_method.md), and the author has been told it cannot be cut. Dropping it after a mixed result is withholding a result that has already been seen.

**A second demo set is honest only if all of these hold:**
- The chats are not written now by anyone who has seen this failure. Draw them by a committed seed from an existing committed set the author did not write (blind_dev or blind_dev2 outside-writer chats).
- The draw rule, the commands and the publish-whole promise are committed before any run.
- Demo 1 stays first and whole.
- The text says set 2 was added after demo 1's result was read.

With about 3 days left I would not add one. The sealed numbers are the measurement, and a second set added now reads as diluting the first.

**Disclosure sentence on the run order:** "I ran this demo once for 6.37 and once for base on 2026-11-12 at 05:05 Eastern, read the result, and only then registered it (R-175); the transcript is shown whole, as run, with no rerun of 6.37 and no change to the script." If the method lane's "publish whatever it shows" was not written before 05:05, add: "The decision to publish it whole was made after the run."

## 3. The notebook
- **bf16 on a T4.** The T4 (sm_75) has no bf16 tensor cores. I expect `load_model`'s bf16 to run without error, but with no tensor-core use and attention on PyTorch's slower math path. I would expect it to be several times slower than fp16, though decoding is mostly limited by memory bandwidth, so the method lane's 10 to 15 minutes is plausible. None of this is verified, and it cannot be checked here.
- **fp16 safety: unknown.** config.json says `"torch_dtype": "bfloat16"`, Cohere2, vocabulary 262,144. That is the same vocabulary size as Gemma 3, a family known to overflow in fp16, but that is no proof for Cohere2. Before shipping the fp16 cell, run it on the 3080 and compare all 30 replies with the bf16 transcripts.
- **Different transcripts on Colab.** Greedy decoding on a different GPU, dtype or torch can give a different transcript. If a judge's run differs from the README table, it can look like the table was cherry-picked. The comparison column is required, not optional.
- **Is it worth more than Part A alone?** Only for the few judges who will log in. Part A on its own just prints JSON the README already shows.
- **What breaks on a fresh Colab that the design misses:**
  - The `accelerate` and `safetensors` pins are missing.
  - There is no `torch.cuda.is_available()` check, so a CPU runtime fails inside the frozen code.
  - No Python 3.12 check, though AgentTune requires it.
  - The free tier does not always grant a T4.
  - Colab's own packages will print pip conflict warnings.
  - The notebook must save its runs outside `results/demo/`, or it overwrites the tracked file it is compared against.
  - E402 on `sys.path.insert` before an import in the same cell.

## 4. CI
- **Versions:** they exist; this holds. Only the `2.11.0+cpu` wheel is unverified.
- **fetch-depth 0:** correct. AgentTune builds with setuptools_scm, and without tags it would record a version other than the recorded 1.1.3.
- **Editable install:** fine. `2.11.0+cpu` satisfies `torch==2.11.*`.
- **Secrets on pull requests from forks:** safe on `pull_request`; never use `pull_request_target`.
- **Ruff and vendor:** vendor sits in `../vendor`, outside the scan; this holds.
- **The `--ignore` of test_inference:** not a change to any test, but the badge then covers less than all tests. Without the token, the tokenizer tests in test_loss_masks skip as well. I would reverse the method lane's drop order: keep the HF_TOKEN step, since it is about 5 minutes of Kevin's time and it is the only way the stop-token tests run in CI. If it is dropped, the README must say "24 of 25 test files".
- **Red first run:** worth telling Kevin before the push. A run on a branch is still visible in the public Actions tab, so the first push should be one he expects might fail.

## 5. Ranking
1. **Demo block** (about 1 h). It is already run, and its limit sentence is now required whether or not the block ships. First, find and commit the raw JSON.
2. **CI with the token step** (about 1.5 h).
3. **Notebook:** Part A, then Part B only after a 3080 dry run, the fixes above, and Kevin's Colab pass.

If one must go, drop notebook Part B. If a whole addition must go, drop the notebook: most judges cannot get past the gate, and the T4 path cannot be tested before it is public.
