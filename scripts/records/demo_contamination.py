"""R-254: check a demo chat against the training data; prints only PASS or FAIL and numbers.

Usage: python scripts/records/demo_contamination.py DEMO_DIR

R-253 and R-254 found Demo2 and Demo3 answers that are fact values in the training chats, some in
sentences that also stand there, so a model could name an answer it has learned as one instead
of retrieving it. Two lines, each failing with the question numbers it names:
1. No question's key is a training fact value: a value annotated in a writer chat or question under
   ``data/screens/``, or a template value of K1.3's pool (``TRAIN.facts``).
2. No six-word run shared between the chat and the training text holds a key as a whole word.
Reported, not a line: keys found anywhere in the training text as a whole word (ordinary words are),
and the count of six-word runs shared (stock phrases are). Never-told questions have no key. No chat
text is printed.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from aya_retrieval.pools import TRAIN

SCREENS = Path("data/screens")
RUN = 6


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.casefold())


def runs(text: str) -> set[tuple[str, ...]]:
    w = words(text)
    return {tuple(w[i : i + RUN]) for i in range(len(w) - RUN + 1)}


def writer_files():
    for path in sorted(SCREENS.rglob("*.json")):
        if "provenance" in path.name:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            yield data


def training_text() -> str:
    """All training text, lower case: set rows' turns and writer chats' messages and questions."""
    parts = []
    for path in sorted(SCREENS.rglob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            parts += [t["content"] for t in json.loads(line).get("turns", [])]
    for data in writer_files():
        for chat in data.get("chats", []):
            parts += [f"{m['user']} {m['assistant']}" for m in chat.get("messages", [])]
            parts += [q.get("question", "") for q in chat.get("questions", [])]
        parts += [q.get("question", "") for q in data.get("questions", []) if isinstance(q, dict)]
    return " \n ".join(parts).casefold()


def fact_values() -> set[str]:
    """Every training fact value: writer annotations and questions, and K1.3's template values."""
    values = {str(v).casefold() for t in TRAIN.facts.values() for v in t.values}
    for data in writer_files():
        for chat in data.get("chats", []):
            values |= {m["fact"]["value"].casefold() for m in chat["messages"] if m.get("fact")}
            values |= {q["value"].casefold() for q in chat.get("questions", []) if q.get("value")}
        for q in data.get("questions", []):
            if isinstance(q, dict) and q.get("value"):
                values.add(q["value"].casefold())
    return values


def main(folder: Path) -> int:
    questions = json.loads((folder / "questions.json").read_text(encoding="utf-8"))["questions"]
    chat = (folder / "chat.txt").read_text(encoding="utf-8")
    text, values = training_text(), fact_values()
    keyed = [
        (n, q["key"].casefold())
        for n, q in enumerate(questions, 1)
        if q.get("key") and q["key"] != "never told"
    ]
    shared = runs(chat) & runs(text)
    value_hits = [n for n, k in keyed if k in values]
    run_hits = [
        n for n, k in keyed if any(re.search(rf"\b{re.escape(k)}\b", " ".join(r)) for r in shared)
    ]
    anywhere = [n for n, k in keyed if re.search(rf"\b{re.escape(k)}\b", text)]
    fails = sum(bool(x) for x in (value_hits, run_hits))
    print(f"{'FAIL' if value_hits else 'PASS'}  keys that are a training fact value: {value_hits}")
    print(f"{'FAIL' if run_hits else 'PASS'}  keys in a shared six-word run: {run_hits}")
    print(f"report: keys found anywhere in training text as a whole word: {anywhere}")
    print(f"report: six-word runs shared with training text: {len(shared)}")
    print(f"== {folder.name} contamination check: {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1])))
