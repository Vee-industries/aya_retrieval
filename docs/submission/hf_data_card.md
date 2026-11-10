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
pretty_name: aya_retrieval training and test chats
size_categories:
- 1K<n<10K
---

# aya_retrieval: training and test chats

The training set of the 6.37 adapter for Tiny Aya Global, every candidate set tried before it, and the two
outside-writer test sets. Code, method and every result are in
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval).

## Files

| Path | What it holds |
|---|---|
| `screens/fix17cs37.jsonl` | The shipped training set: 1,094 rows (`older` 332, `confirm` 230, `in_view` 150, `never_told` 160, `statement` 222). |
| `screens/fix17cs37.provenance.json` | The command, commit, toolkit commits and SHA-256 that built it. |
| `screens/` (other files) | Every candidate training set in the ledger (RECORDS.md), each with its provenance file. |
| `recall_train.jsonl` | The first training set (750 rows, R-016), kept for the history. |
| `blind_dev/`, `blind_dev2/` | The two outside-writer test sets: 40 chats each, written by four fresh Claude Opus agents a set from a brief (`brief.md`). The writers never saw the generator. |

## How the training rows were built

Each row is one chat from the project's generated training pool, ending in a message the model must answer. The
last three exchanges are in view; older exchanges are reachable only through the `search_corpus` tool. Targets are
the untrained model's own replies where they pass the scorer, vetted plain-chat replies, and scripted answers where
needed. CuratorKIT's grounding gate checked the training answers (R-096). No row comes from a sealed test pool;
tests in the repository enforce that no two pools share content.

## Licence

CC-BY-NC-4.0. The targets include replies written by Tiny Aya Global, which Cohere Labs releases under
CC-BY-NC-4.0. The outside-writer chats were written by Claude agents for this project.

## Limits

- Every chat is generated or agent-written. None comes from a real person.
- The generated pool repeats fixed small-talk lines. Base given the whole generated chat copies them (R-014).
