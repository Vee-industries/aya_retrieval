"""Compare screen adapters on probe seed 51203 by kind, decisions and in_view searches."""

import json
import sys

R = sys.argv[1]
labels = sys.argv[2:]


def load(label):
    rows = json.load(open(f"{R}/{label}_seed_51203.json", encoding="utf-8"))["rows"]
    return [r for r in rows if r.get("arm", "tool_loop") == "tool_loop"]


kinds = ("older", "confirm", "in_view", "never_told", "statement")
print("label".ljust(22), "recall", *kinds, "decisions", "inview_searched", "inview_nosearch_wrong")
for lab in labels:
    rows = load(lab)
    rec = sum(r["correct"] for r in rows if r["kind"] in ("older", "confirm"))
    per = [sum(r["correct"] for r in rows if r["kind"] == k) for k in kinds]
    dec = sum(r.get("right_decision", 0) for r in rows)
    iv = [r for r in rows if r["kind"] == "in_view"]
    srch = sum(1 for r in iv if r["queries"])
    nsw = sum(1 for r in iv if not r["queries"] and not r["correct"])
    print(lab.ljust(22), rec, *per, dec, srch, nsw, "| n", len(rows))
