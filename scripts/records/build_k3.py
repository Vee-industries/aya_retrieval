"""K3's training set (R-205): K1.3's rows unchanged, plus rows built from writer agents' chats.

Usage: python scripts/records/build_k3.py

Each writer file in ``data/screens/k3_writers/`` holds chats of 24 user messages with an assistant
reply each, and 11 questions asked after message 24 (``docs/k3/WRITER_BRIEF.md``). Rows are shaped
like K1.3's; the real keyword search (OR, top 5) runs over exchanges 1 to 21.

- Fact rows (older; check_true and check_false as ``confirm``): if the first query's output holds
  the source message, one search and the writer's reply. Else if the second query's does, both
  searches (miss, then hit) and the writer's reply. Else both searches and a reply from
  ``TRAIN.unknown_replies``.
- never_told: the first query; if it returns nothing, the second; kept only if the last search
  returns at least one passage (R-020); a reply from ``TRAIN.unknown_replies``.
- in_view: no search, the writer's reply. statement: each fact message in 22 to 24 as the last
  message, the 3 exchanges before it in view, the writer's reply.
- Balance: searching rows split into those whose reply names a value and those that decline. With
  r the overall ratio of declines to value rows, at each last-search passage count the larger side
  is cut, in a hashed order, until declines equal round(r x value rows) there.
- Rows over 1,024 tokens are dropped.

``scripts/records/check_k3.py`` then checks the set before any training.
"""

from __future__ import annotations

import hashlib
import json
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from agenttune.agentic.rollout_engines.rollout_factory import DEFAULT_TOOL_RESULT_FORMAT
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer

from aya_retrieval.chat import SYSTEM_WITH_TOOL
from aya_retrieval.conversations import CONFIRM, IN_VIEW, NEVER_TOLD, OLDER, STATEMENT
from aya_retrieval.demonstrations import search_call
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.recall_tool import build_search_tool
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME, system_prompt_with_tools

BASE = Path("data/screens/k1_3_r200.jsonl")
WRITERS = Path("data/screens/k3_writers")
OUT = Path("data/screens/k3_r205.jsonl")
SALT = "R-205"
IN_VIEW_FROM = 22  # messages 22 to 24 are in view; 1 to 21 are searched
MAX_ROW_TOKENS = 1024  # R-102's limit
KINDS = {
    "older": OLDER,
    "check_true": CONFIRM,
    "check_false": CONFIRM,
    "never_told": NEVER_TOLD,
    "in_view": IN_VIEW,
}


def digest(*parts: str) -> int:
    return int.from_bytes(hashlib.sha256("|".join((SALT, *parts)).encode()).digest()[:8], "big")


def unknown_reply(row_id: str) -> str:
    return TRAIN.unknown_replies[digest("reply", row_id) % len(TRAIN.unknown_replies)]


def passages(output: str) -> int:
    return output.count("[chunk_id=")


def view_turns(exchanges: list[tuple[str, str]]) -> list[dict]:
    turns = []
    for user, assistant in exchanges:
        turns += [{"role": "user", "content": user}, {"role": "assistant", "content": assistant}]
    return turns


def search_turns(query: str, output: str) -> list[dict]:
    result = DEFAULT_TOOL_RESULT_FORMAT.format(name=SEARCH_TOOL_NAME, content=output)
    return [
        {"role": "assistant", "content": search_call(query)},
        {"role": "user", "content": result},
    ]


def chat_rows(writer: str, c: int, chat: dict, work: Path) -> list[dict]:
    """Every row of one chat, each with ``meta`` (kept out of the written row) for the balance."""
    messages = chat["messages"]
    exchanges = [(m["user"], m["assistant"]) for m in messages]
    tool = build_search_tool(
        exchanges[: IN_VIEW_FROM - 1], work / f"{writer}_{c:02d}.sqlite", match_all=False
    )

    def search(query: str) -> str:
        result = tool.execute(query)
        return result.output if result.success else ""

    rows = []
    for m in range(IN_VIEW_FROM, len(messages) + 1):  # statement rows
        if messages[m - 1].get("fact"):
            turns = view_turns(exchanges[m - 4 : m - 1])
            turns += [
                {"role": "user", "content": messages[m - 1]["user"]},
                {"role": "assistant", "content": messages[m - 1]["assistant"]},
            ]
            rows.append({"id": f"k3_{writer}_{c:02d}_s{m}", "kind": STATEMENT, "turns": turns})
    view = view_turns(exchanges[IN_VIEW_FROM - 1 :])
    for q, question in enumerate(chat["questions"]):
        row_id = f"k3_{writer}_{c:02d}_{q:02d}"
        kind = KINDS[question["kind"]]
        turns = [*view, {"role": "user", "content": question["question"]}]
        meta = {"kind": question["kind"], "person": question.get("person")}
        if kind == IN_VIEW:
            turns.append({"role": "assistant", "content": question["reply"]})
            rows.append({"id": row_id, "kind": kind, "turns": turns, "meta": meta})
            continue
        first = search(question["query"])
        if kind == NEVER_TOLD:
            searches = [(question["query"], first)]
            if not passages(first):
                searches.append((question["second_query"], search(question["second_query"])))
            if not passages(searches[-1][1]):
                continue  # R-020: never_told rows only with passages
            reply, names_value = unknown_reply(row_id), False
        else:
            source = f"User: {messages[question['source_message'] - 1]['user']}\n"
            searches = [(question["query"], first)]
            if source not in first + "\n":
                second = search(question["second_query"])
                searches.append((question["second_query"], second))
            names_value = source in searches[-1][1] + "\n"
            reply = question["reply"] if names_value else unknown_reply(row_id)
        for query, output in searches:
            turns += search_turns(query, output)
        turns.append({"role": "assistant", "content": reply})
        meta |= {
            "names_value": names_value,
            "searches": len(searches),
            "passages": passages(searches[-1][1]),
        }
        rows.append({"id": row_id, "kind": kind, "turns": turns, "meta": meta})
    return rows


def balance(rows: list[dict]) -> list[dict]:
    """Cut the larger side at each passage count so declines match r x value rows there."""
    searching = [r for r in rows if "names_value" in r.get("meta", {})]
    value = sum(r["meta"]["names_value"] for r in searching)
    ratio = (len(searching) - value) / max(1, value)
    by_count = defaultdict(lambda: {True: [], False: []})
    for r in searching:
        by_count[r["meta"]["passages"]][r["meta"]["names_value"]].append(r)
    cut = set()
    for sides in by_count.values():
        values, declines = sides[True], sides[False]
        keep_declines = round(ratio * len(values))
        if len(declines) > keep_declines:
            order = sorted(declines, key=lambda r: digest("balance", r["id"]))
            cut.update(r["id"] for r in order[keep_declines:])
        else:
            keep_values = round(len(declines) / ratio) if ratio else len(values)
            order = sorted(values, key=lambda r: digest("balance", r["id"]))
            cut.update(r["id"] for r in order[keep_values:])
    return [r for r in rows if r["id"] not in cut]


def within_tokens(rows: list[dict]) -> list[dict]:
    """Return the rows of at most ``MAX_ROW_TOKENS`` tokens as training sees them."""
    tokenizer = AutoTokenizer.from_pretrained(
        snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True)
    )
    system = {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)}

    def tokens(turns: list[dict]) -> int:
        ids = tokenizer.apply_chat_template([system, *turns], tokenize=True, return_dict=True)
        return len(ids["input_ids"])

    return [r for r in rows if tokens(r["turns"]) <= MAX_ROW_TOKENS]


def main() -> None:
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    built, writer_hashes = [], {}
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        for path in sorted(WRITERS.glob("*.json")):
            writer_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            for c, chat in enumerate(json.loads(path.read_text(encoding="utf-8"))["chats"]):
                built += chat_rows(path.stem, c, chat, Path(tmp))
    balanced = balance(built)
    added = within_tokens(balanced)
    meta = {r["id"]: r.pop("meta", None) for r in added}

    out = rows + added
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_text(text, encoding="utf-8")
    report = {
        "provenance": provenance,
        "record": "R-205",
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "writer_files_sha256": writer_hashes,
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "natural_rows_built": len(built),
        "cut_by_balance": len(built) - len(balanced),
        "cut_over_tokens": len(balanced) - len(added),
        "natural_rows": len(added),
        "natural_rows_by_kind": dict(Counter(r["kind"] for r in added)),
        "meta": meta,
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(
        f"{OUT}: {len(out)} rows, {len(added)} natural (built {len(built)}, "
        f"balance cut {report['cut_by_balance']}, token cut {report['cut_over_tokens']})"
    )


if __name__ == "__main__":
    main()
