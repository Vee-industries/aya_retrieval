Method lane, panel R-174. Read-only: no file was edited, nothing was installed, no model was run. I ran ruff with `--no-cache`, an AST walk of AgentTune's import closure, and `git ls-remote` (to confirm the vendor repos are public).

## Facts found that shape the design
- `src/aya_retrieval/models.py`, `inference.py`, `harness.py`, `recall_tool.py` and `tool_prompt.py` are listed in `results/freeze/sealed_manifest.json` (frozen.scorer). `load_model()` cannot be edited. It hard-codes bf16, `device_map={"":0}` and `local_files_only=True`. `chat.py` and `scripts/run_chat.py` are not frozen.
- AgentTune cannot be avoided. `harness`, `tool_prompt`, `recall_tool`, `scoring`, `demonstrations` and `longmemeval` import it at module top. AgentTune's declared deps are very heavy: torch==2.11.0, langchain, chromadb, lm-eval, sentence-transformers, wandb, bitsandbytes and more.
- At pin d4db4c1, `agenttune.decide` loads lazily. So the static closure of what this repo actually imports needs only these third-party packages: torch, datasets, huggingface_hub, langchain_text_splitters, psutil and pyyaml (colorama and wandb only inside try blocks). This is unconfirmed until something imports it for real.
- `peft` is not in pyproject. It arrives only through AgentTune, but `run_chat.py`, `adapters.py`, `test_adapters` and `run_longmemeval` need it. `trl` is needed only by `test_lean_loss`/`lean_loss`. AuditKIT has zero deps and is needed by `test_stats` and `test_audit`. No test imports CuratorKIT.
- `provenance.REPO_ROOT` is `parents[2]` of the module, and toolkit commits are read from `../vendor/<name>`. If the repo is installed non-editable, git provenance comes back as None.
- Both Lexsi-Labs repos are public, and both pinned commits are on origin/main. There is no WSL distro and no docker on this machine, so GitHub Actions cannot be run locally. nbformat and jupyter are not installed.
- ruff check and ruff format --check pass today (188 files).
- Demo history:
  - `demo/chat.txt` was committed 723da40 on 2026-11-04 22:16. 6.37 was trained 2026-11-08 06:42 (81896dd), so the script was written before 6.37 existed.
  - The script was visible during development: R-076 (11-05) logged both earlier adapters failing turn 14 by re-searching "brother new job".
  - 3 rows of `data/screens/fix17cs37.jsonl` contain a pottery template ("X has taken up pottery on weekends", other names, other wording).
  - The harness has not changed since base.json's commit 052feab, apart from the run_chat docstring and two new optional args in conversations.py.

## 1. Notebook (`notebooks/demo_6_37.ipynb`)
Runtime: Colab free T4 GPU. Two parts, so that a judge who will not log in still sees the demo.

- **Cell 1, markdown:** what it shows, the T4 runtime, about 15 min for Part B, the limits link.
- **Cell 2, Part A (CPU, no login, under 30 s):**
  - `git clone` the repo and check out a pinned SHA (the commit that adds the 6.37 transcript).
  - Print `git log -1 --format=%ad` for demo/chat.txt beside the date of the 6.37 training commit.
  - Load `results/demo/base.json` and `results/demo/fix17cs37_82.json` and print every turn with stdlib only: message, each `[search: ...]`, reply, and the provenance (commit, GPU, package versions).
- **Cell 3, markdown, the gate:** accept the licence on the CohereLabs/tiny-aya-global page (gated=auto, so access is immediate). Then either add a read token as the Colab secret `HF_TOKEN` with notebook access, or run `huggingface_hub.notebook_login()`. The base model is not mirrored. Rehosting it to get around the gate would breach the licence terms.
- **Cell 4, install:**
  - Clone AgentTune into `/content/vendor/AgentTune` at d4db4c1, so provenance records its commit.
  - `pip install --no-deps /content/vendor/AgentTune`, non-editable.
  - `pip install transformers==5.22.1 peft==0.21.2 huggingface_hub==1.33.0 datasets langchain-text-splitters psutil pyyaml`.
  - Keep Colab's torch: `pip install -e .` would force torch 2.11 and a runtime restart.
  - Do not install the repo. Use `sys.path.insert(0, "/content/aya_retrieval/src")`. This keeps REPO_ROOT and git provenance right, and avoids Colab's restart-after-editable-install problem.
  - Skip AuditKIT, CuratorKIT and trl. Print all versions next to the recorded ones (torch 2.11.0+cu128, transformers 5.22.1).
- **Cell 5, downloads:**
  - `snapshot_download(MODEL_ID, revision=MODEL_REVISION)` (online once).
  - `snapshot_download("KevinVaillancourt/aya-retrieval-6.37", revision=<HF sha>)`.
  - SHA-256 the adapter files against `sealed_manifest.json` frozen.model.adapter_files. Stop on a weights mismatch, and report the config hash separately.
- **Cell 6, load:** `aya_retrieval.models.load_model()`, unchanged, in bf16 (the recorded dtype). Print the dtype and GPU name. A labelled fp16 fallback cell repeats the from_pretrained line with `dtype=torch.float16`, stated as a deviation. It cannot call `load_model`, which is frozen.
- **Cell 7, base run:** a loop line-for-line equal to `run_chat.main`, using `aya_retrieval.chat.Chat`, `MAX_TOKENS`, `inference.generate_from_messages` and `GREEDY` over `demo/chat.txt`. Save JSON with `provenance.run_metadata()`.
- **Cell 8, 6.37 run:** `PeftModel.from_pretrained(model, adapter_dir)`, then the same loop. Base must run first, because the wrap changes the model in place.
- **Cell 9, comparison:** a side-by-side table per turn (message, base search and reply, 6.37 search and reply). A column marks any turn that differs from the recorded 3080 transcript. Differences are possible because the GPU, dtype and torch differ, and the cell says so.
- **Cell 10, optional:** type your own messages with `Chat.send`, with base reachable through `model.disable_adapter()`.
- **Cell 11, markdown:** 4 recall questions are an illustration, not a measurement; the sealed numbers and limits.

Run time estimate (from the recorded 3080 rate, about 25 tok/s; T4 about 10 tok/s or less with emulated bf16): install 2-3 min, download 6.7 GB 2-4 min, load 1-2 min, base about 2-3 min, 6.37 about 1 min. About 10-15 min in all.

**Testable here:**
- ruff check and format on the .ipynb (ruff lints notebooks, so CI covers it).
- A new `tests/test_notebook.py` reads the ipynb JSON and asserts that its adapter hash equals the manifest and its revision equals `models.MODEL_REVISION`.
- Part A run on CPU with the Desktop Python.
- The lean install in a fresh scratch venv: `import aya_retrieval.chat, .harness, .scoring, .recall_tool`, which confirms the static closure.
- Part B code run as a script on the 3080 under the card rules. Its output should equal the canonical transcript.
- The fp16 path checked on the 3080 for NaN or garbage.

**Not testable here:**
- Colab's preinstalled versions, and whether the pins resolve against its torch.
- bf16 behaviour and speed on a T4.
- The secrets and login flow, and a new account's gate click.
- Colab RAM (12.7 GB) and disk.
- The Open-in-Colab badge, which needs a pushed commit.

Kevin opens it once in Colab after the push (about 20 min).

## 2. CI (`.github/workflows/ci.yml`)
**Runs on CPU with no weights:**
- 23 of 25 files need only AgentTune (lean), AuditKIT, peft, trl and transformers. `test_adapters` builds a tiny random Llama on CPU.
- `test_loss_masks`'s tokenizer tests already skip ("Tiny Aya is not in the local cache").
- No test uses CUDA, the network, or hashes of repo files. Line endings are safe because `.gitattributes` stores LF.

**Needs the gated tokenizer:** `test_inference.py`. It has no skip, so it would error. It needs no GPU and no weights.

**Workflow:**
1. on: push to main, pull_request, workflow_dispatch; `permissions: contents: read`; `timeout-minutes: 30`; ubuntu-24.04.
2. Check out this repo to `aya_retrieval/`. Check out Lexsi-Labs/AgentTune@d4db4c12d52342227c4113a70183d0f64aa2f345 to `vendor/AgentTune` with fetch-depth 0 (setuptools_scm), and Lexsi-Labs/AuditKIT@71316da345784ff220d5ed59337441a59ab31526 to `vendor/AuditKIT`. This layout keeps vendor out of `ruff check .` and matches provenance's `../vendor`. Set `working-directory: aya_retrieval`.
3. `actions/setup-python@v5` with python-version 3.12 and cache pip.
4. `pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cpu` (`2.11.0+cpu` satisfies `torch==2.11.*`).
5. `pip install --no-deps ../vendor/AgentTune ../vendor/AuditKIT`
6. `pip install transformers==5.22.1 peft==0.21.2 trl==1.7.1 accelerate==1.15.0 huggingface_hub==1.33.0 safetensors==0.8.0 datasets==5.1.0 langchain-text-splitters==1.1.3 psutil pyyaml ruff==0.17.3 pytest==9.2.0`, then `pip install -e .`
7. An import smoke step: `python -c "import aya_retrieval.harness, aya_retrieval.scoring, aya_retrieval.recall_tool, aya_retrieval.audit"`.
8. `ruff check .` and `ruff format --check .`
9. Tokenizer step: set job env `HF_TOKEN: ${{ secrets.HF_TOKEN }}` and use `if: env.HF_TOKEN != ''`. Secrets cannot go in `if` directly. Call `snapshot_download(MODEL_ID, revision=MODEL_REVISION, allow_patterns=["tokenizer*","special_tokens_map.json","config.json","generation_config.json"])`, about 21 MB.
10. `HF_HUB_OFFLINE=1 pytest -ra`. Without the token, use `--ignore=tests/test_inference.py`, with an echo and a workflow comment stating that it needs the gated tokenizer and runs locally. `-ra` prints the existing skip reasons.

No test file changes, and nothing is loosened. Adding the secret is a GitHub settings change Kevin makes himself, with a read-only fine-grained token. First run: push to a branch with Kevin's yes, before main.

**Repo changes:** the workflow; a CI badge and one line in README "Checks" saying what CI runs and leaves out; optionally `tests/test_notebook.py`. Adding peft to pyproject is optional. It is not a frozen file, but leaving it out keeps the change minimal.

Estimate: about 5 min per run, and 1-1.5 h including two fix rounds. The first real check of the AST finding is CI's own import step. The runner's SQLite FTS5 is confirmed by `test_recall_tool` and `test_chat` passing.

## 3. Demo block
**Which demo:** `demo/chat.txt`, all 15 messages. It covers 3 out-of-view recall questions, 1 never-told question and 11 plain-chat lines (including the "call my mum" no-search turn).

**How to keep it from being cherry-picked:**
- Before the run, commit a RECORDS entry, R-175. It states: one run of 6.37 seed 82, `scripts/run_chat.py --adapter ../adapters/screens/fix17cs37_82 --script demo/chat.txt --out results/demo/fix17cs37_82.json`, greedy, 60 tokens, a clean tree, HF_HUB_OFFLINE=1, the card lock. It also says the whole transcript is published whatever it shows, with no rerun and no script edit.
- Rerun base at the same commit to a new file, `results/demo/base_r175.json` (do not replace base.json), and state whether it matches base.json. The two-run GPU job is about 5 min.
- Build the table with a committed script (for example `scripts/make_demo_table.py`) from the JSONs, not typed by hand.

**Disclosures under the table:**
- The script was written on 2026-11-04 (723da40), before 6.37 was trained (2026-11-08).
- It was visible during development. R-076 logged the earlier adapters' turn-14 failure, so it is not a held-out test.
- 3 training rows hold a different pottery fact.
- 4 questions is an illustration; the numbers come from the sealed run.
- Grading rule: the expected answer is the fact as written in the script.

**Placement:**
- README: the full table, uncollapsed, in "Chat with it", plus one pointer line under the status block.
- Short write-up: a new "What a chat looks like" section after "What was built".
  - A 2-line count of where each model searched.
  - Then the full both-model table in `<details>`, so the article stays short.
  - Whether HF renders `<details>` must be checked on the HF preview.
- The HF article re-upload needs Kevin's yes.

## 4. Order and time
1. R-175 entry, then the GPU run of 6.37 and base: 30-45 min, depending on the card being free. It goes first because everything else uses the transcript.
2. CI: 1-1.5 h.
3. Demo table script and both blocks: about 1 h.
4. Notebook, with local tests (static, Part A, lean venv, Part B on the 3080): 3-4 h, plus Kevin's Colab pass of about 20 min after the push.
5. Badges, the Layout table entry for `notebooks/`, the `test_notebook.py` pin test: 30 min.

Total is about 7-8 h, which fits before Nov 15 AoE with a margin.

**Drop first, in order:**
1. The HF_TOKEN CI step (keep the stated `--ignore`).
2. Notebook cell 10 (interactive).
3. The fp16 fallback cell.
4. Notebook Part B. Ship Part A only, labelled as a viewer of recorded runs.

Never drop the pre-registration, the whole-script table or the disclosures.

**Main risks:**
- The lean AgentTune install is inferred from a static walk. CI's import step and the local scratch venv confirm it.
- T4 bf16 can only be confirmed by Kevin's Colab pass.
- No file was written for this report.
