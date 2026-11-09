"""R-147 target line: 6.39 against 6.37 at fresh seed 75002, seeds 82 and 83 pooled.

hard_dev recall (older and confirm) over `plain` and `long` must be higher than 6.37's on the same
items (ties fail); probe `plain` recall must not be lower. Touches the stop file on any FAIL.

Usage: target_r147.py STOPFILE
"""
import json, sys
from pathlib import Path

S = Path(__file__).parent
EVAL = Path("results/recall_eval")
stop = S / sys.argv[1]


def recall(cond, pool, model):
    total = 0
    for seed in (82, 83):
        rows = json.loads((EVAL / f"brk_{cond}_{pool}_{model}_{seed}_seed_75002.json").read_text(encoding="utf-8"))["rows"]
        total += sum(bool(r["correct"]) for r in rows if r["arm"] == "tool_loop" and r["kind"] in ("older", "confirm"))
    return total


hd = {m: recall("plain", "hd", m) + recall("long", "hd", m) for m in ("fix17cs37", "fix17cs39")}
pr = {m: recall("plain", "probe", m) for m in ("fix17cs37", "fix17cs39")}
lines = [
    f"{'PASS' if hd['fix17cs39'] > hd['fix17cs37'] else 'FAIL'}  hard_dev recall plain+long at 75002, 82+83: "
    f"6.39 {hd['fix17cs39']} above 6.37's {hd['fix17cs37']} (ties fail)",
    f"{'PASS' if pr['fix17cs39'] >= pr['fix17cs37'] else 'FAIL'}  probe recall plain at 75002, 82+83: "
    f"6.39 {pr['fix17cs39']} not below 6.37's {pr['fix17cs37']}",
]
print("\n".join(lines))
if any(x.startswith("FAIL") for x in lines):
    stop.touch()
    print(f"== 6.39 fails R-147's target; {stop.name} touched")
else:
    print("== 6.39 passes R-147's target")
