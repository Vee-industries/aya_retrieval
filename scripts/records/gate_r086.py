"""R-086's gate, the items that need no judge: a candidate at seeds 82 and 83 against fix 17b.

Usage: python scripts/records/gate_r086.py <name>     e.g. fix19a

Reads screen_<name>_82 (probe 51203), hd_<name>_8x and probe_<name>_8x (seed 73157). Prints each
item and exits 0 if every one passes, 1 if not. The judged items (Sheet B, hard_dev Sheet B, the
chat check set) are counted apart, after this decides what the GPU does next.
"""

import json
import sys
from pathlib import Path

from aya_retrieval.report_data import false_retrieval

EVAL = Path("results/recall_eval")
RECALL = ("older", "confirm")


def count(label, seed, kinds):
    data = json.loads((EVAL / f"{label}_seed_{seed}.json").read_text(encoding="utf-8"))
    return sum(
        bool(r["correct"]) for r in data["rows"] if r["arm"] == "tool_loop" and r["kind"] in kinds
    )


def wrong_finds(label, seed):
    return sum(v[0] for v in false_retrieval(label, seed).values())


name = sys.argv[1]
screen, hd = f"screen_{name}_82", {s: f"hd_{name}_{s}" for s in (82, 83)}
items = {
    "probe 51203 recall at least 94": (count(screen, 51203, RECALL), 94),
    "probe 51203 statement at least 47": (count(screen, 51203, ("statement",)), 47),
    "hard_dev never_told at seed 82 at least 44": (count(hd[82], 73157, ("never_told",)), 44),
    "hard_dev recall pooled at least 145": (sum(count(hd[s], 73157, RECALL) for s in hd), 145),
    "probe 73157 recall pooled at least 189": (
        sum(count(f"probe_{name}_{s}", 73157, RECALL) for s in (82, 83)),
        189,
    ),
}
results = {item: (value, value >= floor) for item, (value, floor) in items.items()}
fr = wrong_finds(hd[82], 73157)
results["hard_dev false retrieval at seed 82 at most 6"] = (fr, fr <= 6)
for item, (value, ok) in results.items():
    print(f"{'PASS' if ok else 'FAIL'}  {item}: {value}")
sys.exit(0 if all(ok for _, ok in results.values()) else 1)
