---
license: cc-by-nc-4.0
language:
- en
task_categories:
- text-generation
tags:
- tool-use
- retrieval
- long-context
- memory
- lora
pretty_name: aya_retrieval training and outside-writer chats
size_categories:
- 1K<n<10K
---

# aya_retrieval: training and outside-writer chats

The training set of the 6.37 adapter for Tiny Aya Global, every candidate set tried before it, and the two sets of
outside-writer chats. Code, method and every result are in
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval); record ids (R-016 and so
on) point into its `RECORDS.md`. The run logs are in
[aya-retrieval-eval-logs](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-eval-logs).

**Access.** This dataset, the eval-logs dataset and the adapter are public and un-gated (checked 2026-11-12, no
login). The base model CohereLabs/tiny-aya-global is gated: accept its licence on Hugging Face first.

## Files

| Path | What it holds |
|---|---|
| `screens/fix17cs37.jsonl` | The shipped training set: 1,094 rows (`older` 332, `confirm` 230, `in_view` 150, `never_told` 160, `statement` 222). |
| `screens/fix17cs37.provenance.json` | The command, commit, toolkit commits and SHA-256 that built it. |
| `screens/` (other files) | Every candidate training set in the ledger (`RECORDS.md`), each with its provenance file. |
| `recall_train.jsonl` | An early training set in the same format: 800 rows (`older` 200, 150 of each other kind), built by `scripts/run_build_training_set.py --seed 71119`; its provenance file gives the command and commit. |
| `blind_dev/` | Outside-writer set 1: 40 chats (`chats/w1_01.json` to `w4_10.json`) by four fresh Claude Opus agents writing from `brief.md`, who never saw the generator. A development set since R-151, when candidate 7 was designed from 6.37's failures on it. Not a test set. |
| `blind_dev2/` | Outside-writer set 2: 40 chats by four new writers, same method. The test set for the 7.x candidates (R-151, R-156); no 7.x candidate passed, so its 6.37 run became a report on the shipped adapter, read by no decision that changed 6.37 (R-157). |

## Fields

Training rows (`screens/*.jsonl`, `recall_train.jsonl`), one JSON object a line:
- `id`: the row's id, named by kind.
- `kind`: one of `older` (a question about a fact now out of view), `confirm` ("..., right?" about such a fact),
  `in_view` (the answer is in the last three exchanges), `never_told` (the fact was never given, so the right reply
  declines) and `statement` (plain chat, where the right move is not to search).
- `turns`: the chat as a list of `{"role", "content"}` messages. A search is an assistant turn holding the
  `search_corpus` call as JSON text; the search result comes back as the next user turn, starting
  `Tool result for search_corpus:`.

Outside-writer chats (`blind_dev/chats/*.json`, `blind_dev2/chats/*.json`), one chat a file:
- `id`: writer and chat number (`w1_01`; set 2 uses `x1_01`).
- `exchanges`: the chat as a list of `[user message, assistant reply]` pairs.
- `questions`: the messages to answer at the end of the chat, each with `kind` (the five kinds above), `message`,
  `answer` (the expected value; empty for `never_told` and `statement`), `wrong` (values that make a reply wrong)
  and `fact_exchange` (the index of the exchange that tells the fact; null when there is none).

## Sample row

The first row of `screens/fix17cs37.jsonl`:

```json
{"id": "older_0000", "kind": "older", "turns": [
 {"role": "user", "content": "i'm actually pretty happy with the laundry lately"},
 {"role": "assistant", "content": "Good to hear the laundry is behaving."},
 {"role": "user", "content": "ugh, my knee is driving me up the wall"},
 {"role": "assistant", "content": "Sorry, my knee sounds like a real hassle."},
 {"role": "user", "content": "the fridge let me down this morning"},
 {"role": "assistant", "content": "That's frustrating. Is the fridge usually like that?"},
 {"role": "user", "content": "the creatures in my neighbour's yard escape me"},
 {"role": "assistant", "content": "[{\"tool_name\": \"search_corpus\", \"parameters\": {\"query\": \"neighbour keeps animals yard\"}}]"},
 {"role": "user", "content": "Tool result for search_corpus: [chunk_id=exchange_0023::0 doc_id=exchange_0023 score=6.708]\nUser: so Omar (my neighbour) keeps tortoises in the yard\nAssistant: Thanks for telling me.\n\n[chunk_id=exchange_0014::0 doc_id=exchange_0014 score=3.633]\nUser: so Yusuf (my brother) keeps rabbits in the yard\nAssistant: How are they finding it?\n\n[chunk_id=exchange_0002::0 doc_id=exchange_0002 score=3.557]\nUser: so Marc (my sister) keeps chickens in the yard\nAssistant: Oh, that's nice to hear.\n\n[chunk_id=exchange_0024::0 doc_id=exchange_0024 score=1.629]\nUser: funny how the mail keeps coming up\nAssistant: It does seem to come up a lot.\nUse this result to answer the original question."},
 {"role": "assistant", "content": "It sounds like your neighbour, Omar, keeps tortoises in the yard."}]}
```

## Loading

```python
from datasets import load_dataset

train = load_dataset(
    "KevinVaillancourt/aya-retrieval-chats", data_files="screens/fix17cs37.jsonl", split="train"
)
set1 = load_dataset(
    "KevinVaillancourt/aya-retrieval-chats", data_files="blind_dev/chats/*.json", split="train"
)
```

Tested 2026-11-12 with `datasets` 5.1.0 and no login: 1,094 rows (`id`, `kind`, `turns`) and 40 chats (`id`,
`exchanges`, `questions`). Pass `data_files` for one folder at a time: the folders mix training rows, chats, briefs
and provenance files.

## Headline numbers and the files that hold them

Paths below are in the eval-logs dataset unless marked "here".

| Number | File |
|---|---|
| 1,094 training rows and their kinds | `screens/fix17cs37.jsonl` (here) |
| Outside-writer recall, base with the tool: 26 and 27 of 120 | `recall_eval/blind_base_seed_0.json`, `recall_eval/blind2_base_seed_0.json` |
| Outside-writer recall, 6.37 with the tool: 39 and 53 of 120 | `recall_eval/blind_fix17cs37_82_seed_0.json`, `recall_eval/blind2_fix17cs37_82_seed_0.json`; summary in `analysis/R-164/writeup_numbers.json` |
| Outside-writer recall, code that searches every turn: 42 and 47 | `recall_eval/as_blind_base_seed_0.json`, `recall_eval/as_blind2_base_seed_0.json` |
| Outside-writer recall, base with the whole chat: 71 and 65 | `recall_eval/wca_blind_base_seed_0.json`, `recall_eval/wca_blind2_base_seed_0.json` |
| `in_view`, `never_told` and `statement` counts on the outside-writer sets | the same files, rows of those kinds |
| Sealed test recall, seed 82 91 to 107 of 120 against base's 13 to 32 | `analysis/R-162/A.json` to `D.json` |
| Sealed pools after the run: code, base with the whole chat, seed 82 | `analysis/R-168/refs.json` |
| LongMemEval-S measures and judged accuracy | `analysis/R-170/scores.json`, `analysis/R-170/judged.json` |

## The sealed test pools

The sealed test's pools, `heldout` and `independent`, are not in this dataset. They are public as source in the
repository: `src/aya_retrieval/pools.py` (`heldout`), `src/aya_retrieval/pool_independent.py` and
`docs/independent_pool/` (`independent`), with SHA-256 digests in `results/freeze/sealed_manifest.json`. The sealed
run (R-162) built each condition's 300 conversations from them at item seed 90311 and ran the model on them:

```bash
python scripts/run_recall_eval.py --final --pool heldout --decoys 1 --seed 90311 --items-per-kind 30 \
  --arms tool_loop --index eval_final.sqlite --label final_A_base
```

Condition B is `--pool heldout --decoys 4`, C `--pool independent --decoys 1`, D `--pool independent --decoys 4`;
`--adapter` scores an adapter. The command is the one in `scripts/records/queue/final.sh`. Every question, search,
passage and reply of the sealed runs is in the eval-logs dataset (`recall_eval/final_*_seed_90311.json`).

## Checks of the scorer

Two people marked the same 50 replies blind, drawn from the development pools `probe` and `hard_dev`, not from
these chats or the sealed pools: I (Kevin Vaillancourt, the author, not an independent marker) agree with the recall
scorer on 47 of 50 (R-144); a second, independent marker agrees with it on 48 of 50 and with me on 49 of 50 (R-145).
The sheets and marks are in the eval-logs dataset (`human_check/R-139/`). The LongMemEval-S judged accuracy rests on
18 judge runs (6 sheets x 3 judges), in `analysis/R-170/judge/marks/`.

## How the training rows were built

Each row is one chat from the project's generated training pool, ending in a message the model must answer. The
last three exchanges are in view; older exchanges are reachable only through the `search_corpus` tool. Targets are
the untrained model's own replies where they pass the scorer, vetted plain-chat replies, and scripted answers where
needed. CuratorKIT's grounding gate audited an ancestor set, v6's 350 found-fact answers, and rejected 22 (R-096);
the replacements it passed are in 6.37's lineage, and the rest of 6.37's rows were not gated by it. No row comes from
a sealed test pool; tests in the repository enforce that no two pools share content.

## Licence

CC-BY-NC-4.0. The targets include replies written by Tiny Aya Global, which Cohere Labs releases under
CC-BY-NC-4.0. The outside-writer chats were written by Claude agents for this project.

## Limits

- Every chat is generated or agent-written. None comes from a real person.
- The generated pool repeats fixed small-talk lines. Base given the whole generated chat copies them (R-014).
- Each outside-writer set has four writers, all one model family.
