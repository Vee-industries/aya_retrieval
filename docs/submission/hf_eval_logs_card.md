---
license: cc-by-nc-4.0
language:
- en
tags:
- evaluation
- tool-use
- retrieval
- long-context
pretty_name: aya_retrieval evaluation logs
---

# aya_retrieval: evaluation logs and judge marks

Every recorded run behind the numbers in the write-up for the 6.37 adapter (Tiny Aya Global), with the judges'
marks and the analysis files. Code, method and the dated log of every run are in
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval).

## Files

| Path | What it holds |
|---|---|
| `recall_eval/` | Each eval run: every question, the model's searches, what each search returned, the reply and the scorer's verdict, with the run's provenance (commit, seed, settings). |
| `coherence/` | The blind coherence sheets, their keys, and each judge's marks, including the sealed run (R-162). |
| `analysis/` | The computed results per record (R-146, R-157, R-162 to R-170), aggregates only. |
| `analysis/R-170/` | LongMemEval-S: scores, judged accuracy, the judge sheets' key (no text), the 18 judges' marks and the 50 lines Kevin marked. |
| `human_check/` | Kevin's blind check of the scorer on 50 replies (R-139). |
| `freeze/` | The digests that froze the model, scorer and judge before the sealed run (R-154). |
| `recall_train/` | Training logs per seed. |

Each file names the record in `RECORDS.md` that registered it.

## What is not here

The LongMemEval-S run files quote that dataset's chats and are not redistributed. The data is at
[xiaowu0162/longmemeval-cleaned](https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned) (MIT), and
`scripts/run_longmemeval.py` in the repository rebuilds the runs from it.

## Licence

CC-BY-NC-4.0. The replies were written by Tiny Aya Global (CC-BY-NC-4.0) and the 6.37 adapter trained from it.
