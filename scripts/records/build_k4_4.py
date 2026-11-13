"""K4.4's training set (R-212): K4.3's rows unchanged, plus wrong-person and contrast rows.

Usage: python scripts/records/build_k4_4.py

K4.2's hard_dev never_told misses (R-211) all named a different person's fact of the asked
category, the trap R-073 found and R-074's fix 15 closed with template rows. No natural K3 or K4
row shows it. Two writers added questions to the 64 K3 chats (``data/screens/k4_4_writers/``,
``docs/k4_4/WRITER_BRIEF.md``): other_person (person P asked a category X that the chat states only
for another person Q) and contrast (Q's own X fact). Rows are built by ``build_k3.chat_rows``'
rules, other_person as never_told and contrast as older. Kept (R-212 lane): an other_person row
only if the fact annotations give Q an X fact and P none, and one of its search outputs holds Q's
message; a contrast only if found. Then K3.1's three drops, the one-to-one cut per last-search
passage count (as K4), and the 1,024-token limit. Nothing in K4.3's rows changes.
``scripts/records/check_k3.py --set k4_4_r212`` then checks the set.
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
BASE = Path("data/screens/k4_3_r211.jsonl")
WRITERS = Path("data/screens/k4_4_writers")
OUT = Path("data/screens/k4_4_r212.jsonl")
AS_K3 = {"other_person": "never_told", "contrast": "older"}


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


K3 = load("build_k3")
K31 = load("build_k3_1")
K4 = load("build_k4")


def facts_of(chat: dict, person: str) -> list[dict]:
    return [
        m
        for m in chat["messages"][:21]
        if m.get("fact") and (m["fact"].get("person") or "").casefold() == person.casefold()
    ]


def main() -> None:
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    base = json.loads(BASE.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    meta, k4_questions = dict(base["meta"]), dict(base["k4_questions"])

    grouped, writer_hashes = defaultdict(list), {}
    for path in sorted(WRITERS.glob("*.json")):
        writer_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for q in json.loads(path.read_text(encoding="utf-8"))["questions"]:
            grouped[(q["file"], q["chat"])].append(q)

    built, questions, dropped = [], {}, Counter()
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        for (file, c), extra in sorted(grouped.items()):
            chat = json.loads((K3.WRITERS / file).read_text(encoding="utf-8"))["chats"][c]
            k3_questions = [{**q, "kind": AS_K3[q["kind"]]} for q in extra]
            writer = f"k44{Path(file).stem}"
            for row in K3.chat_rows(writer, c, {**chat, "questions": k3_questions}, Path(tmp)):
                if row["kind"] == "statement":
                    continue  # K3.2 already has this chat's statement rows
                j = int(row["id"].rsplit("_", 1)[1])
                q = extra[j]
                row["meta"]["k4_kind"] = q["kind"]
                questions[row["id"]] = k3_questions[j]
                if q["kind"] == "other_person":
                    stored = [
                        m["user"]
                        for m in facts_of(chat, q.get("stored_person") or "")
                        if m["fact"]["category"] == q.get("category")
                    ]
                    asked = [
                        m
                        for m in facts_of(chat, q.get("person") or "")
                        if m["fact"]["category"] == q.get("category")
                    ]
                    out = [
                        t["content"] for t in row["turns"] if t["content"].startswith("Tool result")
                    ]
                    if not stored or asked:
                        dropped["other_person invalid"] += 1
                        continue
                    if not any(s in o for s in stored for o in out):
                        dropped["other_person without the stored fact"] += 1
                        continue
                elif not row["meta"]["names_value"]:
                    dropped["contrast not found"] += 1
                    continue
                built.append(row)

    dev_runs = set().union(*(K31.CHECK.runs(q) for q in K31.CHECK.dev_questions()))
    s3 = set()
    for path in sorted(K31.OVERLAP.CHATS.glob("*.json")):
        s3 |= K31.runs(K31.OVERLAP.chat_text(json.loads(path.read_text(encoding="utf-8"))), 6)
    kept = []
    for r in built:
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
    balanced = K4.one_to_one(kept)
    added = K3.within_tokens(balanced)
    for r in added:
        meta[r["id"]] = r.pop("meta")
        k4_questions[r["id"]] = questions[r["id"]]

    out = rows + added
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_bytes(text.encode("utf-8"))
    kinds = Counter(meta[r["id"]]["k4_kind"] for r in added)
    report = {
        "provenance": provenance,
        "record": "R-212",
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "writer_files_sha256": writer_hashes,
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "new_rows_built": len(built),
        "cut_by_balance": len(kept) - len(balanced),
        "cut_over_tokens": len(balanced) - len(added),
        "new_rows_by_kind": dict(kinds),
        "new_rows_by_asked_category": dict(
            sorted(Counter(questions[r["id"]].get("category") for r in added).items())
        ),
        "dropped": dict(dropped),
        "k4_questions": k4_questions,
        "meta": meta,
    }
    report_text = json.dumps(report, indent=1)
    OUT.with_suffix(".provenance.json").write_bytes(report_text.encode("utf-8"))
    print(
        f"{OUT}: {len(out)} rows, {len(added)} new {dict(kinds)} (built {len(built)}, balance cut "
        f"{report['cut_by_balance']}, token cut {report['cut_over_tokens']}); dropped "
        f"{report['dropped']}; asked categories {report['new_rows_by_asked_category']}"
    )


if __name__ == "__main__":
    main()
