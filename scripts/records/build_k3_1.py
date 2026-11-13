"""K3.1's training set (R-206): K3's rows from the same writer files, three kinds of row dropped.

Usage: python scripts/records/build_k3_1.py

K3 (``build_k3.py``) failed three of R-205's check lines. K3.1 builds the same rows from the same
writer files, unchanged, then drops before the balance and token steps:

1. Rows whose first query breaks the brief's rule: a word not in the question (possessive "'s"
   removed on both sides), a filler word, or not 1 to 4 words.
2. Rows whose question shares a four-word run with a question of hard_dev, probe, either
   outside-writer set or Demo2.
3. Rows sharing any six-word run with S3 (decontamination; counts only, no S3 text is printed).

``scripts/records/check_k3.py --set k3_1_r206`` then checks the set.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
import tempfile
from collections import Counter
from pathlib import Path

from aya_retrieval.demonstrations import FILLER
from aya_retrieval.provenance import run_metadata

HERE = Path(__file__).resolve().parent
OUT = Path("data/screens/k3_1_r206.jsonl")
BRIEF_FILLER = set(
    "say tell told mention remember again know think what where which who does did is".split()
)
S3_RUN = 6


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


K3 = load("build_k3")
CHECK = load("check_k3")
OVERLAP = load("overlap_s3_training")


def tokens(text: str) -> list[str]:
    return [w.removesuffix("'s") for w in re.findall(r"[a-z0-9']+", text.casefold())]


def query_ok(question: dict) -> bool:
    query, words = tokens(question["query"]), set(tokens(question["question"]))
    return 1 <= len(query) <= 4 and all(
        w in words and w not in FILLER and w not in BRIEF_FILLER for w in query
    )


def runs(text: str, n: int) -> set[tuple[str, ...]]:
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(w[i : i + n]) for i in range(len(w) - n + 1)}


def main() -> None:
    provenance = run_metadata()
    base_text = K3.BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    dev_runs = set().union(*(CHECK.runs(q) for q in CHECK.dev_questions()))
    s3 = set()
    for path in sorted(OVERLAP.CHATS.glob("*.json")):
        s3 |= runs(OVERLAP.chat_text(json.loads(path.read_text(encoding="utf-8"))), S3_RUN)

    built, questions, writer_hashes = [], {}, {}
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        for path in sorted(K3.WRITERS.glob("*.json")):
            writer_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            for c, chat in enumerate(json.loads(path.read_text(encoding="utf-8"))["chats"]):
                built += K3.chat_rows(path.stem, c, chat, Path(tmp))
                for q, question in enumerate(chat["questions"]):
                    questions[f"k3_{path.stem}_{c:02d}_{q:02d}"] = question

    dropped, kept = Counter(), []
    for row in built:
        question = questions.get(row["id"])
        text = [t["content"] for t in row["turns"] if not t["content"].startswith("Tool result")]
        if question and question["kind"] != "in_view" and not query_ok(question):
            dropped["query rule"] += 1
        elif question and CHECK.runs(question["question"]) & dev_runs:
            dropped["dev or Demo2 question run"] += 1
        elif any(runs(t, S3_RUN) & s3 for t in text):
            dropped["S3 six-word run"] += 1
        else:
            kept.append(row)
    balanced = K3.balance(kept)
    tokenizer_rows = K3.within_tokens(balanced)
    meta = {r["id"]: r.pop("meta", None) for r in tokenizer_rows}

    out = rows + tokenizer_rows
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_text(text, encoding="utf-8")
    report = {
        "provenance": provenance,
        "record": "R-206",
        "base_set": K3.BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "writer_files_sha256": writer_hashes,
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "natural_rows_built": len(built),
        "dropped": dict(dropped),
        "cut_by_balance": len(kept) - len(balanced),
        "cut_over_tokens": len(balanced) - len(tokenizer_rows),
        "natural_rows": len(tokenizer_rows),
        "natural_rows_by_kind": dict(Counter(r["kind"] for r in tokenizer_rows)),
        "meta": meta,
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(
        f"{OUT}: {len(out)} rows, {len(tokenizer_rows)} natural (built {len(built)}, dropped "
        f"{dict(dropped)}, balance cut {report['cut_by_balance']}, token cut "
        f"{report['cut_over_tokens']})"
    )


if __name__ == "__main__":
    main()
