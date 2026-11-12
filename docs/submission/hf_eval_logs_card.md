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
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval); record ids (R-162 and so
on) point into its `RECORDS.md`. The chats the runs read are in
[aya-retrieval-chats](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-chats).

**Access.** This dataset, the chats dataset and the adapter are public and un-gated (checked 2026-11-12, no login).
The base model CohereLabs/tiny-aya-global is gated: accept its licence on Hugging Face first.

## Files

| Path | What it holds |
|---|---|
| `recall_eval/` | Each eval run: every question, the model's searches, what each search returned, the reply and the scorer's verdict, with the run's provenance (commit, seed, settings). The sealed runs are `final_<condition>_<model>_seed_90311.json` (36 files: base and eight seeds in four conditions). |
| `coherence/` | The blind coherence sheets, their keys, and each judge's marks, including the sealed run (R-162). |
| `analysis/` | The computed results per record (R-139, R-146, R-157, R-162, R-164, R-168, R-170), aggregates only. |
| `analysis/R-170/` | LongMemEval-S: scores, judged accuracy, the judge sheets' key (no text), the marks of 18 judge runs (6 sheets x 3 judges) and the 50 lines I (the author) marked. |
| `human_check/R-139/` | The blind check of the recall scorer on 50 replies: my marks (R-144) and a second, independent marker's (R-145), with the key and the agreement. |
| `freeze/` | The digests that froze the model, scorer and judge before the sealed run (R-154, R-160). |
| `recall_train/` | Training logs per seed. |
| `curator/`, `audit/` | CuratorKIT's grounding gate (R-096, R-098) and AuditKIT's second-scorer runs. |
| `control/`, `panels/`, `vet/`, `demo/` and the rest | The prompted baseline's prompts and run logs, each panel's messages, the judges' vetting of training answers, the scripted demo's transcripts, and the other runs their records name. |

Each file names the record in `RECORDS.md` that registered it.

## Fields of a run file

A `recall_eval/*.json` file is one JSON object. Its top level holds the run's settings (`provenance`, `model`,
`model_revision`, `adapter`, `seed`, `pool`, `decoys`, `sizes`, `kinds`, the stress flags, `items_dir`,
`items_sha256`), `peak_vram_gib`, `seconds`, and `rows`, one per question and arm:
- `id`, `size` (messages in the chat), `kind`, `arm` (`tool_loop` is the model with the tool, `always_search` is
  code that searches every turn, `whole_chat_all` is the whole chat with no tool);
- `message`, `view` (the exchanges in view), `answer`, `reply`;
- `queries` (each search's query) and `passages` (how many passages each search returned);
- `tokens_read`, `tokens_written`, `whole_chat_tokens`;
- `ran_out_of_calls` (more than three searches in the turn), `first_reply` (the model's first output);
- `correct`, `right_decision` (searched exactly when the answer was out of view) and `found_fact` (a search
  returned the fact).

## Sample row

Row `w1_07_q1` of `recall_eval/blind_fix17cs37_82_seed_0.json` (6.37 seed 82 on outside-writer set 1):

```json
{"id": "w1_07_q1", "size": 42, "kind": "older", "arm": "tool_loop",
 "message": "wait what does mikael do for work",
 "view": [["dad might come too, his gout is acting up again tho", "Hopefully he can rest his foot and still enjoy dinner."],
          ["he'll complain the whole time lol", "That's part of the tradition, maybe."],
          ["pretty much", "At least the food will be good."]],
 "answer": "mechanic", "reply": "Your dad Mikael is a mechanic.",
 "queries": ["Mikael new job"], "passages": [2],
 "tokens_read": 1586, "tokens_written": 33, "whole_chat_tokens": 967, "ran_out_of_calls": false,
 "first_reply": "[{\"tool_name\": \"search_corpus\", \"parameters\": {\"query\": \"Mikael new job\"}}]",
 "correct": true, "right_decision": true, "found_fact": true}
```

## Loading

```python
import json
from datasets import load_dataset
from huggingface_hub import hf_hub_download

rows = load_dataset(
    "KevinVaillancourt/aya-retrieval-eval-logs",
    data_files="recall_eval/blind_fix17cs37_82_seed_0.json",
    field="rows",
    split="train",
)
path = hf_hub_download(
    "KevinVaillancourt/aya-retrieval-eval-logs", "analysis/R-162/A.json", repo_type="dataset"
)
condition_a = json.load(open(path, encoding="utf-8"))
```

Tested 2026-11-12 with `datasets` 5.1.0 and no login: 240 rows, 39 right on recall; `shipped_seed_82.recall` in
`analysis/R-162/A.json` reads 106. The analysis files are single JSON objects, so they load with `hf_hub_download`;
run files load with `field="rows"`.

## Headline numbers and the files that hold them

| Number | File |
|---|---|
| Sealed test recall, seed 82 91 to 107 of 120 against base's 13 to 32 | `analysis/R-162/A.json` to `D.json`: `shipped_seed_82.recall`, `shipped_seed_82.base_recall` |
| Sealed right search decisions (298, 296 against 180, 193) and clean first calls (180 of 180, 184 of 184 against 52 of 136, 49 of 107) | the same files, `behaviour` |
| Every registered rule in every condition | the same files, `rule_1_recall` to `rule_4_coherence`, `all_rules_pass` |
| Sealed pools after the run: code 14 to 32, base with the whole chat 21 to 33, seed 82 44 to 55 of 60 | `analysis/R-168/refs.json` |
| Outside-writer recall: base with the tool 26 and 27, 6.37 39 and 53 of 120 | `recall_eval/blind_base_seed_0.json`, `blind2_base_seed_0.json`, `blind_fix17cs37_82_seed_0.json`, `blind2_fix17cs37_82_seed_0.json`; summary in `analysis/R-164/writeup_numbers.json` |
| Outside-writer recall: code 42 and 47, base with the whole chat 71 and 65 | `recall_eval/as_blind_base_seed_0.json`, `as_blind2_base_seed_0.json`, `wca_blind_base_seed_0.json`, `wca_blind2_base_seed_0.json` |
| LongMemEval-S mechanical measures (declines 233 of 470, gold answer 51, 51 and 63 of 411, clean first calls) | `analysis/R-170/scores.json` |
| LongMemEval-S judged right (53, 34 and 40 of 248) and its p-values | `analysis/R-170/judged.json` |
| The 18 judge runs (6 sheets x 3 judges) | `analysis/R-170/judge/marks/marks_L1_j1.json` to `marks_L6_j3.json`, with each run's brief in `analysis/R-170/judge/` |
| My 50 blind LongMemEval-S lines (46 of 50 with each judge) | `analysis/R-170/judge/kevin_marks.json`, `human_key.json` |
| Scorer check: 47 of 50 (the author, R-144), 48 of 50 (the second marker, R-145) | `human_check/R-139/agreement.json` |
| CuratorKIT rejected 22 of v6's 350 found-fact answers | `curator/R-096/summary.json` |
| AuditKIT agreed 959 of 960 on v3 | `audit/v3_probe73157.json` |

## Human checks

Two people checked the recall scorer on the same 50 replies, drawn from the development pools `probe` and
`hard_dev`, not from the sealed or outside-writer chats. I (Kevin Vaillancourt, the author, not an independent
marker) agree with the scorer on 47 of 50 (R-144). A second, independent marker agrees with it on 48 of 50 and with
me on 49 of 50 (R-145). On LongMemEval-S I marked 50 judged lines blind before any judged number was read and agree
with each judge on 46 of 50; no second marker checked those lines (R-170). The coherence judges were never checked
against a person.

## The sealed pools

The sealed test's pools are not published as a dataset; they are public as source in the repository, and the
chats dataset's card gives the rebuild command (item seed 90311, `scripts/run_recall_eval.py --final`). Every
question, search, passage and reply of the sealed runs is here, in `recall_eval/final_*_seed_90311.json`.

## What is not here

The LongMemEval-S run files quote that dataset's chats and are not redistributed. The data is at
[xiaowu0162/longmemeval-cleaned](https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned) (MIT), and
`scripts/run_longmemeval.py` in the repository rebuilds the runs from it.

## Licence

CC-BY-NC-4.0. The replies were written by Tiny Aya Global (CC-BY-NC-4.0) and the 6.37 adapter trained from it.
