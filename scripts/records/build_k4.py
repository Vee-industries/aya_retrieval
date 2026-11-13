"""K4's training set (R-208): K3.2's rows unchanged, plus near-miss and contrast rows.

Usage: python scripts/records/build_k4.py

Two writers added questions to the 64 K3 chats (``data/screens/k4_writers/``,
``docs/k4/WRITER_BRIEF.md``): near_miss (a person with a stored fact of category X, asked a close
category never stated for them) and contrast (that stored fact itself). Rows are built by
``build_k3.chat_rows``' rules, near_miss as never_told and contrast as older. Kept (R-208 lane):
a near_miss only if the fact annotations give the asked person a stored-category fact and none of
the asked category, and its last search output holds that stored message; a contrast only if
found. Then, at each last-search passage count, the larger side is cut in a hashed order to the
size of the smaller (value and decline equal), then the 1,024-token limit.
``scripts/records/check_k3.py --set k4_r208`` then checks the set.
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
BASE = Path("data/screens/k3_2_r207.jsonl")
K3_WRITERS = Path("data/screens/k3_writers")
WRITERS = Path("data/screens/k4_writers")
OUT = Path("data/screens/k4_r208.jsonl")
AS_K3 = {"near_miss": "never_told", "contrast": "older"}


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


K3 = load("build_k3")


def by_category(rows, questions, meta) -> dict[str, list[bool]]:
    out = defaultdict(list)
    for r in rows:
        out[questions[r["id"]].get("category", "?")].append(meta[r["id"]]["names_value"])
    return out


def one_to_one(rows: list[dict]) -> list[dict]:
    """At each last-search passage count, cut the larger side (value or decline) to the smaller."""
    sides = defaultdict(lambda: {True: [], False: []})
    for r in rows:
        sides[r["meta"]["passages"]][r["meta"]["names_value"]].append(r)
    keep = set()
    for pair in sides.values():
        n = min(len(pair[True]), len(pair[False]))
        for side in pair.values():
            order = sorted(side, key=lambda r: hashlib.sha256(f"R-208|{r['id']}".encode()).digest())
            keep.update(r["id"] for r in order[:n])
    return [r for r in rows if r["id"] in keep]


def main(out_path: Path = OUT, record: str = "R-208", row_filter=None) -> None:
    """Build the set; ``row_filter`` (R-209) drops new rows before the one-to-one cut."""
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    base_meta = json.loads(BASE.with_suffix(".provenance.json").read_text(encoding="utf-8"))["meta"]

    grouped, writer_hashes = defaultdict(list), {}
    for path in sorted(WRITERS.glob("*.json")):
        writer_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        for q in json.loads(path.read_text(encoding="utf-8"))["questions"]:
            grouped[(q["file"], q["chat"])].append(q)

    built, questions, dropped = [], {}, Counter()
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        for (file, c), extra in sorted(grouped.items()):
            stem = Path(file).stem
            chat = json.loads((K3_WRITERS / file).read_text(encoding="utf-8"))["chats"][c]
            k3_questions = [{**q, "kind": AS_K3[q["kind"]]} for q in extra]
            writer = f"k4{stem}"
            for row in K3.chat_rows(writer, c, {**chat, "questions": k3_questions}, Path(tmp)):
                if row["kind"] == "statement":
                    continue  # K3.2 already has this chat's statement rows
                j = int(row["id"].rsplit("_", 1)[1])
                q = extra[j]
                row["meta"]["k4_kind"] = q["kind"]
                questions[row["id"]] = k3_questions[j]
                person = (q.get("person") or "").casefold()
                facts = [
                    m
                    for m in chat["messages"][:21]
                    if m.get("fact") and (m["fact"].get("person") or "").casefold() == person
                ]
                if q["kind"] == "near_miss":
                    stored = [
                        m["user"]
                        for m in facts
                        if m["fact"]["category"] == q.get("stored_category")
                    ]
                    asked = [m for m in facts if m["fact"]["category"] == q.get("category")]
                    out = [
                        t["content"] for t in row["turns"] if t["content"].startswith("Tool result")
                    ]
                    if not stored or asked:
                        dropped["near_miss invalid", person == "me"] += 1
                        continue
                    if not (out and any(s in out[-1] for s in stored)):
                        dropped["near_miss without the stored fact", person == "me"] += 1
                        continue
                elif not row["meta"]["names_value"]:
                    dropped["contrast not found", person == "me"] += 1
                    continue
                built.append(row)
    if row_filter:
        built = row_filter(built, questions, dropped)
    balanced = one_to_one(built)
    added = K3.within_tokens(balanced)
    meta = {**base_meta, **{r["id"]: r.pop("meta", None) for r in added}}

    out = rows + added
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    out_path.write_bytes(text.encode("utf-8"))
    kinds = Counter(meta[r["id"]]["k4_kind"] for r in added)
    report = {
        "provenance": provenance,
        "record": record,
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "writer_files_sha256": writer_hashes,
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "new_rows_built": len(built),
        "cut_by_balance": len(built) - len(balanced),
        "cut_over_tokens": len(balanced) - len(added),
        "new_rows_by_kind": dict(kinds),
        "dropped": {f"{k} ({'user' if me else 'other'})": v for (k, me), v in dropped.items()},
        "decline_share_by_asked_category": {
            c: round(sum(not v for v in vals) / len(vals), 2)
            for c, vals in sorted(by_category(added, questions, meta).items())
        },
        "k4_questions": {r["id"]: questions[r["id"]] for r in added},
        "meta": meta,
    }
    out_path.with_suffix(".provenance.json").write_bytes(
        json.dumps(report, indent=1).encode("utf-8")
    )
    print(
        f"{out_path}: {len(out)} rows, {len(added)} new {dict(kinds)} "
        f"(built {len(built)}, balance cut "
        f"{report['cut_by_balance']}, token cut {report['cut_over_tokens']}); dropped "
        f"{report['dropped']}"
    )


if __name__ == "__main__":
    main()
