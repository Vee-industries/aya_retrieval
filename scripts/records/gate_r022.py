"""R-022's rule on one results file. Exit 0 on a pass, 1 on a fail."""

import json
import sys

BASE_RECALL = 15  # of 48 at each size, from probe2_base_seed_73157.json
rows = json.load(open(sys.argv[1], encoding="utf-8"))["rows"]


def recall(size):
    return sum(
        r["correct"] for r in rows if r["size"] == size and r["kind"] in ("older", "confirm")
    )


def reading(kind):
    found = [r for r in rows if r["kind"] == kind and r["found_fact"]]
    return sum(r["correct"] for r in found), len(found)


gains = {size: 100 * (recall(size) - BASE_RECALL) / 48 for size in (58, 419)}
decisions = sum(r["right_decision"] for r in rows)
older, confirm = reading("older"), reading("confirm")
passed = (
    all(gain >= 20 for gain in gains.values())
    and decisions >= 200
    and older[0] * 2 >= older[1]
    and confirm[0] * 10 >= confirm[1] * 7
)
print({"gains": gains, "decisions": decisions, "older": older, "confirm": confirm, "pass": passed})
sys.exit(0 if passed else 1)
