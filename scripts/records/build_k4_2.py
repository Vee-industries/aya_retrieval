"""K4.2's training set (R-210): K4.1's rows unchanged, plus declines after empty searches.

Usage: python scripts/records/build_k4_2.py

K4.1 (``build_k4_1.py``) failed screening on hard_dev never_told: with its first search empty it
searched again, and named what a second search brought back or kept searching until it ran out of
calls. In its training set an empty search output is followed by another search in every row (104
of 104), and no row replies after an empty output: R-020 drops never_told rows whose last search is
empty, and the balance cuts every decline at passage count 0, where no value row can exist (R-210
against lane). K4.2 adds to K4.1's rows, from the same writer files, rows not already in the set:

1. Searches as ``build_k3.chat_rows`` (the first query, the second if the first output does not
   hold the fact), never_told and near_miss rows built as never_told without R-020's drop
   (a near_miss kept only if the person has a stored-category fact and none of the asked one).
2. Kept: rows whose first search is empty and whose reply declines; that is, declines after two
   empty searches (R-020 changed for count 0: with no passage there is nothing to answer from), and
   declines after an empty then a non-empty search.
3. K3.1's drops (query rule, a four-word run with a dev or Demo2 question, a six-word run with S3).
4. At each last-search passage count above 0, new declines after an empty first search are cut, in
   a hashed order, to the number of value rows after an empty first search there, less the
   declines already there. Then the 1,024-token limit.

``scripts/records/check_k3.py --set k4_2_r210`` then checks the set.
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

HERE = Path(__file__).resolve().parent
BASE = Path("data/screens/k4_1_r209.jsonl")
K4_WRITERS = Path("data/screens/k4_writers")
OUT = Path("data/screens/k4_2_r210.jsonl")
SALT = "R-210"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


K3 = load("build_k3")
K31 = load("build_k3_1")
K4 = load("build_k4")


def outputs(row: dict) -> list[str]:
    return [t["content"] for t in row["turns"] if t["content"].startswith("Tool result")]


def first_empty(row: dict) -> bool:
    out = outputs(row)
    return bool(out) and not K3.passages(out[0])


def never_told_row(row_id: str, chat: dict, question: dict, work: Path) -> dict | None:
    """A never_told row as ``chat_rows`` builds it, without R-020's drop on an empty last search."""
    messages = chat["messages"]
    exchanges = [(m["user"], m["assistant"]) for m in messages]
    tool = K3.build_search_tool(
        exchanges[: K3.IN_VIEW_FROM - 1], work / f"{row_id}.sqlite", match_all=False
    )

    def search(query: str) -> str:
        result = tool.execute(query)
        return result.output if result.success else ""

    searches = [(question["query"], search(question["query"]))]
    if not K3.passages(searches[0][1]):
        searches.append((question["second_query"], search(question["second_query"])))
    turns = [*K3.view_turns(exchanges[K3.IN_VIEW_FROM - 1 :])]
    turns.append({"role": "user", "content": question["question"]})
    for query, output in searches:
        turns += K3.search_turns(query, output)
    turns.append({"role": "assistant", "content": K3.unknown_reply(row_id)})
    meta = {
        "kind": "never_told",
        "person": question.get("person"),
        "names_value": False,
        "searches": len(searches),
        "passages": K3.passages(searches[-1][1]),
    }
    return {"id": row_id, "kind": K3.NEVER_TOLD, "turns": turns, "meta": meta}


def near_miss_valid(chat: dict, q: dict) -> bool:
    person = (q.get("person") or "").casefold()
    facts = [
        m["fact"]["category"]
        for m in chat["messages"][:21]
        if m.get("fact") and (m["fact"].get("person") or "").casefold() == person
    ]
    return q.get("stored_category") in facts and q.get("category") not in facts


def main(out_path: Path = OUT, record: str = "R-210", kinds: set[str] | None = None) -> None:
    """Build the set; ``kinds`` (R-211) keeps only new rows of those kinds."""
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    base = json.loads(BASE.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    meta, k4_questions = dict(base["meta"]), dict(base["k4_questions"])
    have = {r["id"] for r in rows}

    built, questions, hashes = [], {}, {}
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        work = Path(tmp)
        chats = {}
        for path in sorted(K3.WRITERS.glob("*.json")):
            hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            chats[path.name] = json.loads(path.read_text(encoding="utf-8"))["chats"]
            for c, chat in enumerate(chats[path.name]):
                for row in K3.chat_rows(path.stem, c, chat, work):  # not-found fact rows
                    m = row.get("meta", {})
                    if m.get("kind") != "never_told" and m.get("names_value") is False:
                        built.append(row)
                for j, q in enumerate(chat["questions"]):
                    rid = f"k3_{path.stem}_{c:02d}_{j:02d}"
                    questions[rid] = q
                    if q["kind"] == "never_told":
                        built.append(never_told_row(rid, chat, q, work))
        for path in sorted(K4_WRITERS.glob("*.json")):
            hashes[f"k4/{path.name}"] = hashlib.sha256(path.read_bytes()).hexdigest()
            grouped = defaultdict(list)
            for q in json.loads(path.read_text(encoding="utf-8"))["questions"]:
                grouped[(q["file"], q["chat"])].append(q)
            for (file, c), extra in sorted(grouped.items()):
                chat = chats[file][c]
                for j, q in enumerate(extra):
                    rid = f"k3_k4{Path(file).stem}_{c:02d}_{j:02d}"
                    if q["kind"] != "near_miss" or not near_miss_valid(chat, q):
                        continue
                    questions[rid] = {**q, "kind": "never_told"}
                    row = never_told_row(rid, chat, questions[rid], work)
                    row["meta"]["k4_kind"] = "near_miss"
                    built.append(row)

    dropped = Counter()
    fresh = [r for r in built if r["id"] not in have and first_empty(r)]
    dropped["not new or first search not empty"] = len(built) - len(fresh)
    if kinds:
        dropped["kind not kept"] = sum(r["meta"]["kind"] not in kinds for r in fresh)
        fresh = [r for r in fresh if r["meta"]["kind"] in kinds]
    dev_runs = set().union(*(K31.CHECK.runs(q) for q in K31.CHECK.dev_questions()))
    s3 = set()
    for path in sorted(K31.OVERLAP.CHATS.glob("*.json")):
        text = K31.OVERLAP.chat_text(json.loads(path.read_text(encoding="utf-8")))
        s3 |= K31.runs(text, K31.S3_RUN)
    kept = []
    for r in fresh:
        q = questions[r["id"]]
        text = [t["content"] for t in r["turns"] if not t["content"].startswith("Tool result")]
        if not K31.query_ok(q):
            dropped["query rule"] += 1
        elif K31.CHECK.runs(q["question"]) & dev_runs:
            dropped["dev or Demo2 question run"] += 1
        elif any(K31.runs(t, K31.S3_RUN) & s3 for t in text):
            dropped["S3 six-word run"] += 1
        else:
            kept.append(r)

    room = Counter()  # per last count above 0: value rows less declines, both after an empty first
    for r in rows:
        m = meta.get(r["id"])
        if m and "names_value" in m and m["passages"] and first_empty(r):
            room[m["passages"]] += 1 if m["names_value"] else -1
    order = sorted(kept, key=lambda r: hashlib.sha256(f"{SALT}|{r['id']}".encode()).digest())
    added, used = [], Counter()
    for r in order:
        n = r["meta"]["passages"]
        if n == 0 or used[n] < room[n]:
            used[n] += bool(n)
            added.append(r)
    dropped["cut at two searches"] = len(kept) - len(added)
    fits = K3.within_tokens(added)
    dropped["over 1,024 tokens"] = len(added) - len(fits)
    for r in fits:
        meta[r["id"]] = r.pop("meta")
        if meta[r["id"]].get("k4_kind"):
            k4_questions[r["id"]] = questions[r["id"]]

    out = rows + fits
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    out_path.write_bytes(text.encode("utf-8"))
    cells = Counter()
    for r in out:
        if outputs(r):
            m = meta.get(r["id"]) or {}
            last = bool(K3.passages(outputs(r)[-1]))
            value = m.get("names_value", r["kind"] != K3.NEVER_TOLD)
            cells[f"first empty {first_empty(r)}, last has passages {last}, value {value}"] += 1
    report = {
        "provenance": provenance,
        "record": record,
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "writer_files_sha256": hashes,
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "new_rows": len(fits),
        "new_rows_ending_empty": sum(meta[r["id"]]["passages"] == 0 for r in fits),
        "new_rows_by_kind": dict(Counter(meta[r["id"]]["kind"] for r in fits)),
        "dropped": dict(dropped),
        "searching_rows_by_cell": dict(sorted(cells.items())),
        "k4_questions": k4_questions,
        "meta": meta,
    }
    report_text = json.dumps(report, indent=1)
    out_path.with_suffix(".provenance.json").write_bytes(report_text.encode("utf-8"))
    print(
        f"{out_path}: {len(out)} rows, {len(fits)} new "
        f"({report['new_rows_ending_empty']} ending empty, "
        f"{report['new_rows_by_kind']}); dropped {report['dropped']}"
    )
    for cell, n in report["searching_rows_by_cell"].items():
        print(f"  {cell}: {n}")


if __name__ == "__main__":
    main()
