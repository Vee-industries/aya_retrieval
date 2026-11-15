# Review panel on the Lexsi hackathon write-up, round 2 (shared brief)

Round 2. The same ten lanes reviewed commit 0e8b421 earlier today (round 1); the author applied the panel's fixes
in commit 8735c87 (RECORDS.md R-294 to R-297; R-295's synthesis is `results/panels/R-295/synthesis.md`). Your round-1
report is named in your lane message. First check each of your round-1 findings against the current documents: fixed,
partly fixed, or not fixed, with the line that shows it. Then look for anything new, including errors the fixes
introduced (a number that no longer matches its source, a claim stronger than its evidence, a contradiction between
the papers). Two decisions are settled and are not findings: 6.37 seed 82 stays the shipped model (R-294), and the
GitHub push and Hugging Face updates wait for the author's word (R-297).

You are one reviewer on a panel of ten. Each reviewer has one lane, given in the message that sent you here. Most
lanes are hostile: your job is to find what is wrong, overstated, missing or unclear, not to praise. Agreement with
the author is not a goal. Plain words; no metaphors.

## What is under review

A solo submission to the Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning), problem statement 4
("Fine-tuning for retrieval-augmented generation: Train a model that decides when and what to retrieve, grounds its
answers in the retrieved text and ignores distracting documents"). A LoRA adapter (6.37) on Tiny Aya Global (3.35B)
that searches its own chat history with a keyword tool. The form is due 16 November 2026 06:59 ET.

Repository (read only): `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval`

The documents:
- `docs/ARTICLE.md`, the long paper (about 13,600 words). Built from `docs/article_template.md` by
  `scripts/make_article.py`, which fills every `{{name}}` from results files.
- `docs/submission/HF_ARTICLE.md`, the short paper (about 3,950 words; the author asked for about 5 pages, telling the
  same story and pointing to the long one for evidence).
- `docs/submission/ABSTRACT.md`, the form abstract (at most 500 words).
- `README.md`, `docs/MODEL_CARD.md` (6.37) and `docs/MODEL_CARD_C1.md` (C1, published), where your lane needs them.

Evidence you may use: `RECORDS.md` (the dated record, R-001 to R-297; it is 815 KB, so find entries with
`grep -n "^## R-NNN "` and print only the lines you need with `sed -n`), `results/` (results files; `results/s3/` holds
the second sealed test's runs and `ship_rule.json`), `scripts/`, `src/`, `figures/`. Python:
`C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\venv\Scripts\python.exe`, with `PYTHONPATH=src`.

## Rules for every reviewer

- Read only. Never edit, create or delete anything inside the repository. Never run git commands that change state
  (no commit, add, checkout, reset, stash). No GPU work and no model loading.
- Do not open: `src/aya_retrieval/pools.py` past line 451, `data/heldout*`, `data/*independent*`,
  `results/longmemeval/`, or Demo5's chat under `docs/demo5/`.
- Network: only the hackathon-judge lane may read web pages, and only hackathon.lexsi.ai.
- Check before you claim. A finding that says a number is wrong must name the results file or command that shows the
  right one. A finding that says something is missing must name what you searched for and where.
- Budget: about 60 tool calls. Write your report once, at the end.

## Your report

Write it to the file named in your lane message (a folder outside the repository), in this form, at most about 900
words not counting the status list:

```
# Lane N: <lane name>
Verdict: <one line: submit as is / submit after fixes / do not submit>
## Round-1 findings: status
F1 fixed / partly / not fixed: <line or evidence>
...
## New findings (most severe first)
F1. [BLOCKER | MAJOR | MINOR] <file>:<line or section>: <what is wrong, in one or two sentences>
    Evidence: <file, line, command or record id>
    Fix: <the smallest change that fixes it>
F2. ...
## What holds up
<at most three lines: claims you tried to break and could not>
```

BLOCKER: a judge would reject or mark down the submission for it, or a claim is false. MAJOR: a claim is overstated,
a required item is missing, or a number does not match its source. MINOR: wording, layout, clarity.

Your final message back is only: the report's path and its verdict line.
