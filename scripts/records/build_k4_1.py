"""K4.1's training set (R-209): K4 with K3.1's three drops applied to its new rows.

Usage: python scripts/records/build_k4_1.py

K4 (``build_k4.py``) failed three of its check lines because its new near_miss and contrast rows
skipped K3.1's drops. K4.1 builds K4 the same way and, before the one-to-one cut, drops new rows
whose first query breaks the brief's rule, whose question shares a four-word run with a dev or
Demo2 question, or that share a six-word run with S3 (``build_k3_1``'s rules, counts only).
``scripts/records/check_k3.py --set k4_1_r209`` then checks the set.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path("data/screens/k4_1_r209.jsonl")


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


K4 = load("build_k4")
K31 = load("build_k3_1")


def k3_1_drops(rows: list[dict], questions: dict, dropped) -> list[dict]:
    dev_runs = set().union(*(K31.CHECK.runs(q) for q in K31.CHECK.dev_questions()))
    s3 = set()
    for path in sorted(K31.OVERLAP.CHATS.glob("*.json")):
        text = K31.OVERLAP.chat_text(json.loads(path.read_text(encoding="utf-8")))
        s3 |= K31.runs(text, K31.S3_RUN)
    kept = []
    for row in rows:
        question = questions[row["id"]]
        text = [t["content"] for t in row["turns"] if not t["content"].startswith("Tool result")]
        if not K31.query_ok(question):
            dropped["query rule", False] += 1
        elif K31.CHECK.runs(question["question"]) & dev_runs:
            dropped["dev or Demo2 question run", False] += 1
        elif any(K31.runs(t, K31.S3_RUN) & s3 for t in text):
            dropped["S3 six-word run", False] += 1
        else:
            kept.append(row)
    return kept


if __name__ == "__main__":
    K4.main(out_path=OUT, record="R-209", row_filter=k3_1_drops)
