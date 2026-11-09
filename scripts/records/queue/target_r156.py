"""R-156 target: 7.1 against 6.37 on the second independent set, seeds 82, 83, 94, 95, 96 pooled.

Recall (older and confirm) pooled over the five seeds must be higher than 6.37's at the same seeds (ties fail), and confirm right and searched pooled must be higher than 6.37's (ties fail; R-156).
Also printed, registered as a reading, not a line: confirm right and confirm searched, and in_view right decisions
(searches on in_view questions), each pooled. Touches the stop file on a FAIL.

Usage: target_r153.py NAME STOPFILE
"""
import json, sys
from pathlib import Path

S = Path(__file__).parent
EVAL = Path("results/recall_eval")
SEEDS = (82, 83, 94, 95, 96)
name, stop = sys.argv[1], S / sys.argv[2]
FROZEN = "3a91c34b2183ec8e3a74a5481540e6873307488b4f89d742f8ec91bd5c3dfe65"


def rows(model, seed):
    data = json.loads((EVAL / f"blind2_{model}_{seed}_seed_0.json").read_text(encoding="utf-8"))
    assert data["items_sha256"] == FROZEN and not data["dropped"]
    return [r for r in data["rows"] if r["arm"] == "tool_loop"]


def tally(model):
    t = {"recall": 0, "confirm_right": 0, "confirm_searched": 0, "in_view_searched": 0, "confirm_right_searched": 0}
    for s in SEEDS:
        for r in rows(model, s):
            t["recall"] += r["kind"] in ("older", "confirm") and bool(r["correct"])
            t["confirm_right"] += r["kind"] == "confirm" and bool(r["correct"])
            t["confirm_searched"] += r["kind"] == "confirm" and bool(r["queries"])
            t["confirm_right_searched"] += r["kind"] == "confirm" and bool(r["correct"]) and bool(r["queries"])
            t["in_view_searched"] += r["kind"] == "in_view" and bool(r["queries"])
    return t


new, ref = tally(name), tally("fix17cs37")
line = (f"{'PASS' if new['recall'] > ref['recall'] else 'FAIL'}  second independent set recall over five seeds: "
        f"7.1 {new['recall']} above 6.37's {ref['recall']} (ties fail; 120 a seed)")
second = (f"{'PASS' if new['confirm_right_searched'] > ref['confirm_right_searched'] else 'FAIL'}  "
          f"confirm right and searched over five seeds: 7.1 {new['confirm_right_searched']} above 6.37's "
          f"{ref['confirm_right_searched']} (ties fail; R-156)")
print(line)
print(second)
print(f"reading: 7.1 {new}  6.37 {ref}")
if line.startswith("FAIL") or second.startswith("FAIL"):
    stop.touch()
    print(f"== {name} fails R-156's target; {stop.name} touched")
else:
    print(f"== {name} passes R-156's target")
