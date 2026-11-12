"""Count the content words each registered demo question shares with its source message (R-176).

Shared words make a fact easier to find by full-text search, so the count is fixed before the run
and printed beside every result. Content words are lower-case letter runs, minus the stop words
below. Writes ``results/demo/overlap_r176.json``.

Usage:
    python scripts/records/demo_overlap_r176.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
STOP = set(
    "a about again all an and any anyway are at be been but did do does for go had has have he her "
    "his how i i'm i've if in into is it it's its just lately me my of on or out over really s she "
    "should so that the their them they this to up was we were what what's when where which who "
    "with you your".split()
)


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP}


def main() -> None:
    messages = [
        m for m in (REPO_ROOT / "demo" / "chat.txt").read_text(encoding="utf-8").splitlines() if m
    ]
    questions = json.loads((REPO_ROOT / "demo" / "questions_r176.json").read_text(encoding="utf-8"))
    rows = []
    for q in questions["questions"]:
        n = q["source_message"]
        shared = sorted(words(q["question"]) & words(messages[n - 1])) if n else []
        rows.append({"source_message": n, "question": q["question"], "shared_words": shared})
        print(n, len(shared), shared)
    out = REPO_ROOT / "results" / "demo" / "overlap_r176.json"
    out.write_text(json.dumps({"record": "R-176", "rows": rows}, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
