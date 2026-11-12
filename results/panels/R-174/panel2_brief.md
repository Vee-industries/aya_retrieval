# Panel R-174: a runnable notebook, CI, and a demo block for the hackathon submission

## The request
Kevin (the author), 2026-11-12. He asked "what can we do to get it past 74?" and was offered four levers. He
picked three: "Notebook, CI, demo". His standing order for this work is "make sure you're running everything
through a panel".

## Context
- The submission is a LoRA adapter, 6.37, on Tiny Aya Global (3.35B). It is for the Lexsi Labs hackathon (Track 3,
  Agentic Fine-tuning). It is due 2026-11-15, 11:59 PM AoE, and the latest resubmission counts.
- The judges score: write-up clarity /10, practical usefulness /10, code / notebook quality /10, overall /100.
  They are founders and industry people, and judging is double-blind.
- A blind reader scored the write-up 62/100 and could not see the code. Panel R-173 found that wording can lift
  clarity, but that usefulness is held down by the measured results (see synthesis.md in this folder).
- The model is frozen. The sealed test has run. No training and no change to the adapter are allowed.
- The repo is public on GitHub, and every push needs Kevin's yes. The adapter is public and un-gated on HF as
  KevinVaillancourt/aya-retrieval-6.37. Two datasets are public and un-gated. The base model
  CohereLabs/tiny-aya-global is gated (gated=auto, checked 2026-11-12 with no login).
- The machine has one RTX 3080 (10 GB), shared with Kevin's games. Rules for any GPU test: one project on the card
  at a time; do not start above 38% of card memory in use; hold the OS lock on byte 0 of
  C:\Users\Gaming\scratch\card.lock; run offline (HF_HUB_OFFLINE=1) once the weights are cached.
- Python: C:\Users\Gaming\Desktop\Python312\python.exe. The project venv sits beside the repo (..\venv).

## What exists (read-only)
Repo: C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval
- scripts/run_chat.py: chats in the tested harness (last three exchanges in view, a full-text search tool over
  older messages). With --script demo/chat.txt --out results/demo/<name>.json it records every reply and search.
- demo/chat.txt: a 15-message scripted demo, written earlier in the sprint. results/demo/ holds base.json,
  fix15_82.json and v5_82.json. There is NO transcript for 6.37 (fix17cs37_82).
- tests/: 25 test files. pyproject.toml: ruff and pytest under the [dev] extra. There is no CI workflow and no
  notebook.
- README.md lines about 225 to 245: the setup commands (Windows venv, cu128 torch, vendor clones of AgentTune,
  AuditKIT and CuratorKIT at pinned commits).
You must NOT open or grep: src/aya_retrieval/pools.py, anything under data/ named heldout or independent,
results/longmemeval/, any LongMemEval data, any token or credential file. Never grep across src/ as a whole.

## Fixed rules
- Never soften or hide a limitation, and never overstate. A demo must not be cherry-picked.
- Never loosen a test to make CI pass.
- No new training. No new claims without a committed file behind them.
- Voice spec (kv_voice_v2.md in this folder) for any prose: no em dashes, no "we" or "our", no marketing words,
  no hedges.
- Nothing is pushed or published without Kevin's yes.
