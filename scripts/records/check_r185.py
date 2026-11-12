"""R-185's check before training: K2's set against the registered lines, with 6.37 and K1 for scale.

For each set: never_told rows whose search output names a person or relation the question names
(``asked_person``), never_told rows whose search returns passages, and the mean passages of found
rows (older, confirm) and never_told rows. For K2 also the rows that differ from K1, by kind. Prints
PASS or FAIL per registered line; nothing trains unless every line passes.

Usage:
    python scripts/records/check_r185.py [--set NAME]   (default k2_r185; R-187 uses k2_1_r187)
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.conversations import NEEDS_SEARCH, NEVER_TOLD
from aya_retrieval.pools import TRAIN

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA = REPO_ROOT / "data" / "screens"
CANDIDATE = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "k2_r185"
SETS = {"6.37": "fix17cs37", "K1": "k1_r178", "K2": CANDIDATE}
WORDS = tuple(w.casefold() for w in (*TRAIN.people, *TRAIN.relations))
ASKED_PERSON = (24, 30)
MAX_CHANGED = 35
MAX_GAP = 0.37


def words_in(text: str) -> set[str]:
    text = text.casefold()
    return {w for w in WORDS if re.search(rf"\b{re.escape(w)}\b", text)}


def search_parts(row: dict) -> tuple[str, str]:
    """Return the question and the search output of a row with a search."""
    turns = row["turns"]
    calls = [
        i for i, t in enumerate(turns) if t["role"] == "assistant" and "tool_name" in t["content"]
    ]
    call = max(calls)
    return turns[call - 1]["content"], turns[call + 1]["content"]


def stats(rows: list[dict]) -> dict:
    asked_person = with_passages = 0
    passages = {"found": [], NEVER_TOLD: []}
    for row in rows:
        if row["kind"] not in NEEDS_SEARCH:
            continue
        question, output = search_parts(row)
        n = output.count("chunk_id=")
        passages[NEVER_TOLD if row["kind"] == NEVER_TOLD else "found"].append(n)
        if row["kind"] == NEVER_TOLD:
            with_passages += n > 0
            asked_person += bool(words_in(question) & words_in(output))
    means = {k: sum(v) / len(v) for k, v in passages.items()}
    return {
        "asked_person": asked_person,
        "never_told": len(passages[NEVER_TOLD]),
        "with_passages": with_passages,
        "found_mean": means["found"],
        "never_told_mean": means[NEVER_TOLD],
    }


def load(name: str) -> list[dict] | None:
    path = DATA / f"{name}.jsonl"
    if not path.exists():
        return None
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def main() -> None:
    loaded = {label: load(name) for label, name in SETS.items()}
    for label, rows in loaded.items():
        if rows is None:
            print(f"{label}: no set yet")
            continue
        s = stats(rows)
        print(
            f"{label}: asked_person {s['asked_person']}, never_told with passages "
            f"{s['with_passages']} of {s['never_told']}, mean passages found "
            f"{s['found_mean']:.2f} never_told {s['never_told_mean']:.2f}"
        )
    k1, k2 = loaded["K1"], loaded["K2"]
    if k2 is None:
        return
    s = stats(k2)
    changed = Counter(b["kind"] for a, b in zip(k1, k2, strict=True) if a != b)
    gap = abs(s["found_mean"] - s["never_told_mean"])
    low, high = ASKED_PERSON
    lines = [
        (f"asked_person {s['asked_person']} in {low} to {high}", low <= s["asked_person"] <= high),
        (
            f"rows changed from K1 {dict(changed)}: all never_told, at most {MAX_CHANGED}",
            set(changed) <= {NEVER_TOLD} and sum(changed.values()) <= MAX_CHANGED,
        ),
        (
            f"never_told with passages {s['with_passages']} of {s['never_told']}",
            s["with_passages"] == s["never_told"],
        ),
        (f"mean passage gap {gap:.2f} at most {MAX_GAP}", gap <= MAX_GAP),
    ]
    for text, ok in lines:
        print(f"{'PASS' if ok else 'FAIL':5} {text}")
    print(f"== {CANDIDATE} check: {sum(not ok for _, ok in lines)} FAIL (R-185 lines)")


if __name__ == "__main__":
    main()
