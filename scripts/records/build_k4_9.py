"""K4.9's training set (R-224): K4.8 plus miss-then-hit rows, their first call out of the loss.

Usage: python scripts/records/build_k4_9.py

R-220's lane: after a search that returns text, K4.7's natural rows mostly decline, and most dev
misses never find the fact after one search with passages (R-223's recount). Writers gave each
older and check_true question of the 128 K3 chats a ``miss_query`` (``docs/k4_8/WRITER_BRIEF.md``,
``data/screens/k4_9_writers/``). A row is built when the real search on the miss_query returns
passages without the source message and the question's own query then returns it: the miss, the
hit, the writer's reply. It is marked ``loss_from_second_call`` so the trainer keeps the first call
out of the loss (R-223). The miss_query follows the first-query rule (``build_k3_1.query_ok``), is
not the question's query and holds no word of the value; K3.1's dev and S3 drops apply.

Count, by the lane's rule: K4.8's natural searching rows are cut into cells by (searches, passages
of the last search); with r the ratio of declines to value rows over all of them, a cell takes new
value rows, in a hashed order, until its value rows reach round(declines / r). Rows over 1,024
tokens are dropped. ``scripts/records/check_k3.py --set k4_9_r224`` then checks the set.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from aya_retrieval.provenance import run_metadata
from aya_retrieval.recall_tool import build_search_tool

HERE = Path(__file__).resolve().parent
BASE = Path("data/screens/k4_8_r220.jsonl")
CHATS = Path("data/screens/k4_8/writers/k3")  # K4.8's stripped K3 writer copies
WRITERS = Path("data/screens/k4_9_writers")
OUT = Path("data/screens/k4_9_r224.jsonl")
SALT = "R-224"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


K31 = load("build_k3_1")
K3, K45 = K31.K3, load("build_k4_5")


def miss_ok(miss: str, question: dict) -> bool:
    """The first-query rule, not the question's own query, and no word of the value."""
    value = set(K31.tokens(question["value"]))
    same = K31.tokens(miss) == K31.tokens(question["query"])
    return (
        K31.query_ok({**question, "query": miss}) and not same and not value & set(K31.tokens(miss))
    )


def miss_rows(chat: dict, writer: str, c: int, misses: dict[int, str], work: Path, dropped) -> list:
    messages = chat["messages"]
    exchanges = [(m["user"], m["assistant"]) for m in messages]
    tool = build_search_tool(
        exchanges[: K3.IN_VIEW_FROM - 1], work / f"m_{writer}_{c:02d}.sqlite", match_all=False
    )

    def search(query: str) -> str:
        result = tool.execute(query)
        return result.output if result.success else ""

    view = K3.view_turns(exchanges[K3.IN_VIEW_FROM - 1 :])
    rows = []
    for q, miss in sorted(misses.items()):
        question = chat["questions"][q]
        if question["kind"] not in ("older", "check_true"):
            dropped["not older or check_true"] += 1
            continue
        if not miss_ok(miss, question):
            dropped["miss_query rule"] += 1
            continue
        source = f"User: {messages[question['source_message'] - 1]['user']}\n"
        first, second = search(miss), search(question["query"])
        if not K3.passages(first) or source in first + "\n":
            dropped["miss_query empty or finds the source"] += 1
            continue
        if source not in second + "\n":
            dropped["query does not find the source"] += 1
            continue
        turns = [*view, {"role": "user", "content": question["question"]}]
        turns += K3.search_turns(miss, first) + K3.search_turns(question["query"], second)
        turns.append({"role": "assistant", "content": question["reply"]})
        rows.append(
            {
                "id": f"k49m_{writer}_{c:02d}_{q:02d}",
                "kind": K3.KINDS[question["kind"]],
                "turns": turns,
                "loss_from_second_call": True,
                "question": question["question"],
                "cell": (2, K3.passages(second)),
            }
        )
    return rows


def cell_room(meta: dict) -> tuple[dict, float]:
    """Each (searches, passages) cell's room for value rows under the lane's rule, and r."""
    cells = defaultdict(lambda: {True: 0, False: 0})
    for m in meta.values():
        if m and "names_value" in m:
            cells[m["searches"], m["passages"]][m["names_value"]] += 1
    values = sum(c[True] for c in cells.values())
    ratio = sum(c[False] for c in cells.values()) / values
    return {k: max(0, round(c[False] / ratio) - c[True]) for k, c in cells.items()}, ratio


def main() -> None:
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    base_meta = json.loads(BASE.with_suffix(".provenance.json").read_text(encoding="utf-8"))["meta"]
    dev_runs = set().union(*(K31.CHECK.runs(q) for q in K31.CHECK.dev_questions()))
    s3 = set()
    for path in sorted(K31.OVERLAP.CHATS.glob("*.json")):
        s3 |= K31.runs(K31.OVERLAP.chat_text(json.loads(path.read_text(encoding="utf-8"))), 6)

    misses, writer_hashes = defaultdict(dict), {}
    for path in sorted(WRITERS.glob("*.json")):
        writer_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for m in json.loads(path.read_text(encoding="utf-8"))["miss_queries"]:
            misses[m["file"], m["chat"]][m["question"]] = K45.strip(m["miss_query"])

    built, dropped = [], Counter()
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        for (file, c), by_question in sorted(misses.items()):
            chat = json.loads((CHATS / file).read_text(encoding="utf-8"))["chats"][c]
            for row in miss_rows(chat, Path(file).stem, c, by_question, Path(tmp), dropped):
                text = [t["content"] for t in row["turns"] if not t["content"].startswith("Tool")]
                if K31.CHECK.runs(row["question"]) & dev_runs:
                    dropped["dev or Demo2 question run"] += 1
                elif any(K31.runs(t, 6) & s3 for t in text):
                    dropped["S3 six-word run"] += 1
                else:
                    built.append(row)

    room, ratio = cell_room(base_meta)
    by_cell = defaultdict(list)
    for row in built:
        by_cell[row["cell"]].append(row)
    kept = []
    for cell, cell_rows in sorted(by_cell.items()):
        order = sorted(cell_rows, key=lambda r: K3.digest("k49", r["id"]))
        kept += order[: room.get(cell, 0)]
    meta = {r["id"]: {"cell": list(r.pop("cell")), "question": r.pop("question")} for r in kept}
    added = K3.within_tokens(kept)
    meta = {r["id"]: meta[r["id"]] for r in added}

    out = rows + added
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_bytes(text.encode("utf-8"))
    report = {
        "provenance": provenance,
        "record": "R-224",
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "writer_files_sha256": writer_hashes,
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "miss_queries": sum(len(v) for v in misses.values()),
        "miss_rows_built": len(built),
        "dropped": dict(dropped),
        "decline_to_value_ratio": round(ratio, 4),
        "room_by_cell": {f"{s},{p}": n for (s, p), n in sorted(room.items())},
        "built_by_cell": {f"{s},{p}": len(v) for (s, p), v in sorted(by_cell.items())},
        "cut_by_cell_room": len(built) - len(kept),
        "cut_over_tokens": len(kept) - len(added),
        "miss_rows": len(added),
        "miss_rows_by_kind": dict(Counter(r["kind"] for r in added)),
        "meta": {**base_meta, **meta},
    }
    OUT.with_suffix(".provenance.json").write_bytes(json.dumps(report, indent=1).encode("utf-8"))
    print(
        f"{OUT}: {len(out)} rows, {len(added)} miss-then-hit (built {len(built)}, room cut "
        f"{report['cut_by_cell_room']}, token cut {report['cut_over_tokens']}); dropped "
        f"{dict(dropped)}; room {report['room_by_cell']}; built {report['built_by_cell']}"
    )


if __name__ == "__main__":
    main()
