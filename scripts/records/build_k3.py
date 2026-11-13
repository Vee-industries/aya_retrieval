"""K3's training set (R-205): K1.3's rows unchanged, plus rows built from writer agents' chats.

Usage: python scripts/records/build_k3.py

Each writer file in ``data/screens/k3_writers/`` holds chats of 18 user messages with an assistant
reply each, and 10 questions asked after message 18 (``docs/k3/WRITER_BRIEF.md``). Each question
becomes one row, shaped like K1.3's: the 3 exchanges in view (messages 16 to 18), the question,
then for a searching kind the search call with the writer's query, the real keyword search (OR, top
5) over exchanges 1 to 15, and the reply.

- older, check_true and check_false (kind ``confirm``): kept only when the search output holds the
  source message; the writer's reply.
- never_told: kept only when the search returns at least one passage (R-020); the reply is one of
  K1.3's never-told replies, picked by a hash of the row id.
- in_view: no search; the writer's reply.

``scripts/records/check_k3.py`` then checks the set before any training.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from agenttune.agentic.rollout_engines.rollout_factory import DEFAULT_TOOL_RESULT_FORMAT

from aya_retrieval.conversations import CONFIRM, IN_VIEW, NEVER_TOLD, OLDER
from aya_retrieval.demonstrations import search_call
from aya_retrieval.provenance import run_metadata
from aya_retrieval.recall_tool import build_search_tool
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME

BASE = Path("data/screens/k1_3_r200.jsonl")
WRITERS = Path("data/screens/k3_writers")
OUT = Path("data/screens/k3_r205.jsonl")
SALT = "R-205"
IN_VIEW_FROM = 16  # messages 16 to 18 are in view; 1 to 15 are searched
KINDS = {
    "older": OLDER,
    "check_true": CONFIRM,
    "check_false": CONFIRM,
    "never_told": NEVER_TOLD,
    "in_view": IN_VIEW,
}


def digest(*parts: str) -> int:
    return int.from_bytes(hashlib.sha256("|".join((SALT, *parts)).encode()).digest()[:8], "big")


def natural_rows(writer: str, chats: list[dict], never_told_replies: list[str], work: Path):
    """Yield (row or None, question, search output) for every question of one writer's chats."""
    for c, chat in enumerate(chats):
        exchanges = [(m["user"], m["assistant"]) for m in chat["messages"]]
        view = exchanges[IN_VIEW_FROM - 1 :]
        index = work / f"{writer}_{c:02d}.sqlite"
        tool = build_search_tool(exchanges[: IN_VIEW_FROM - 1], index, match_all=False)
        for q, question in enumerate(chat["questions"]):
            row_id = f"k3_{writer}_{c:02d}_{q:02d}"
            kind = KINDS[question["kind"]]
            turns = []
            for user, assistant in view:
                turns += [
                    {"role": "user", "content": user},
                    {"role": "assistant", "content": assistant},
                ]
            turns.append({"role": "user", "content": question["question"]})
            if kind == IN_VIEW:
                turns.append({"role": "assistant", "content": question["reply"]})
                yield {"id": row_id, "kind": kind, "turns": turns}, question, None
                continue
            result = tool.execute(question["query"])
            output = result.output if result.success else ""
            if kind == NEVER_TOLD:
                keep = "[chunk_id=" in output
                reply = never_told_replies[digest(row_id) % len(never_told_replies)]
            else:
                source = chat["messages"][question["source_message"] - 1]["user"]
                keep = f"User: {source}\n" in output + "\n"
                reply = question["reply"]
            turns += [
                {"role": "assistant", "content": search_call(question["query"])},
                {
                    "role": "user",
                    "content": DEFAULT_TOOL_RESULT_FORMAT.format(
                        name=SEARCH_TOOL_NAME, content=output
                    ),
                },
                {"role": "assistant", "content": reply},
            ]
            yield ({"id": row_id, "kind": kind, "turns": turns} if keep else None), question, output


def main() -> None:
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    never_told_replies = sorted(
        {r["turns"][-1]["content"] for r in rows if r["kind"] == NEVER_TOLD}
    )
    added, dropped = [], {}
    writer_hashes = {}
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        for path in sorted(WRITERS.glob("*.json")):
            writer_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            chats = json.loads(path.read_text(encoding="utf-8"))["chats"]
            for row, question, _output in natural_rows(
                path.stem, chats, never_told_replies, Path(tmp)
            ):
                if row is None:
                    dropped[question["kind"]] = dropped.get(question["kind"], 0) + 1
                else:
                    added.append(row)
    out = rows + added
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_text(text, encoding="utf-8")
    kinds = {}
    for row in added:
        kinds[row["kind"]] = kinds.get(row["kind"], 0) + 1
    report = {
        "provenance": provenance,
        "record": "R-205",
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "writer_files_sha256": writer_hashes,
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "natural_rows": len(added),
        "natural_rows_by_kind": kinds,
        "questions_dropped_by_kind": dropped,
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{OUT}: {len(out)} rows, {len(added)} natural, dropped {dropped}")


if __name__ == "__main__":
    main()
