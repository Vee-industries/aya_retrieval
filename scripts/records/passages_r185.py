"""R-185 evidence: passage counts in 6.37's and K1's training sets, and K1's dev misses by count.

For each set, the number of passages the row's search returns, split into found rows (older,
confirm) and never_told rows. For hard_dev at both seeds, older and confirm questions whose search
found the fact, right and wrong by passage count, for 6.37 and K1. Reads only committed files.

Usage:
    python scripts/records/passages_r185.py
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from aya_retrieval.conversations import NEEDS_SEARCH, NEVER_TOLD
from aya_retrieval.report_data import EVAL_DIR

REPO_ROOT = Path(__file__).resolve().parents[2]
SETS = {"6.37": "fix17cs37", "K1": "k1_r178"}
TOP = 5  # counts of 5 or more share a bin


def set_counts(name: str) -> dict[str, Counter]:
    out = {"found": Counter(), NEVER_TOLD: Counter()}
    path = REPO_ROOT / "data" / "screens" / f"{name}.jsonl"
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["kind"] not in NEEDS_SEARCH:
            continue
        n = sum(t["content"].count("chunk_id=") for t in row["turns"] if t["role"] != "assistant")
        out[NEVER_TOLD if row["kind"] == NEVER_TOLD else "found"][min(n, TOP)] += 1
    return out


def dev_counts(name: str) -> Counter:
    out = Counter()
    for seed in (82, 83):
        path = EVAL_DIR / f"hd_{name}_{seed}_seed_73157.json"
        for row in json.loads(path.read_text(encoding="utf-8"))["rows"]:
            if row["arm"] != "tool_loop" or row["kind"] not in ("older", "confirm"):
                continue
            if row["found_fact"]:
                n = min(row["passages"][0] if row["passages"] else 0, TOP)
                out[(n, "right" if row["correct"] else "wrong")] += 1
    return out


def main() -> None:
    for label, name in SETS.items():
        counts = set_counts(name)
        for group, c in counts.items():
            print(f"{label} training {group}: " + ", ".join(f"{k}: {c[k]}" for k in range(TOP + 1)))
    for label, name in SETS.items():
        c = dev_counts(name)
        cells = [f"{k}: {c[(k, 'right')]} right {c[(k, 'wrong')]} wrong" for k in range(1, TOP + 1)]
        print(f"{label} hard_dev found, seeds 82+83: " + "; ".join(cells))


if __name__ == "__main__":
    main()
