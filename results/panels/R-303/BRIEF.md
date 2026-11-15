# Review panel on the Lexsi hackathon write-up, round 4, the final review (shared brief)

Round 4, the final review. Thirteen lanes review commit 125b902 (round 3's fixes, R-301, and an audit's fixes, R-302) after: the ten lanes of rounds 1 and 2 (on 0e8b421 and 8735c87; fixes in
RECORDS.md R-297 and R-298), an audit (R-299) and a shortening of the long paper that moved per-seed and per-arm detail
into Appendices A to C (R-300), plus three new lanes (a graphic designer, a layout judge and a cold reader). Your
round-3 report, it is named in your lane message: check its findings briefly (fixed / not fixed), then look
for anything new, including errors the recent edits introduced (a pointer to an appendix that does not hold what it
says, a number that moved, a broken sentence where text was cut). The author will push to GitHub and upload to Hugging
Face once, when the write-up is done; settled, not findings: 6.37 seed 82 stays shipped (R-294), and the push and
uploads wait for that single pass.

You are one reviewer on a panel of thirteen. Each reviewer has one lane, given in the message that sent you here. Most
lanes are hostile: your job is to find what is wrong, overstated, missing or unclear, not to praise. Agreement with
the author is not a goal. Plain words; no metaphors.

## What is under review

A solo submission to the Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning), problem statement 4
("Fine-tuning for retrieval-augmented generation: Train a model that decides when and what to retrieve, grounds its
answers in the retrieved text and ignores distracting documents"). A LoRA adapter (6.37) on Tiny Aya Global (3.35B)
that searches its own chat history with a keyword tool. The form is due 16 November 2026 06:59 ET.

Repository (read only): `C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval`

The documents:
- `docs/ARTICLE.md`, the long paper (about 11,800 words of story and 2,500 of appendices). Built from `docs/article_template.md` by
  `scripts/make_article.py`, which fills every `{{name}}` from results files.
- `docs/submission/HF_ARTICLE.md`, the short paper (about 2,750 words; the author asked for about 5 pages, telling the
  same story and pointing to the long one for evidence).
- `docs/submission/ABSTRACT.md`, the form abstract (at most 500 words).
- `README.md`, `docs/MODEL_CARD.md` (6.37) and `docs/MODEL_CARD_C1.md` (C1, published), where your lane needs them.

Evidence you may use: `RECORDS.md` (the dated record, R-001 to R-302; it is 815 KB, so find entries with
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

Write it to the file named in your lane message (a folder outside the repository), in this form, at most about 400
words in all; list only what still needs a change:

```
# Lane N: <lane name>
Verdict: <one line: submit as is / submit after fixes / do not submit>
## Round-3 findings: status (one line each)
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
