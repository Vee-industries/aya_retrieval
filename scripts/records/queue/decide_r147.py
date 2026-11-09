"""R-147 queue step for 6.39 at 82 and 83 (R-134's lines, unchanged): R-086 unjudged + R-094 + R-102 (what is scored so far),
R-094's recall against 6.37's 192 and 163 (R-134 item 5), and R-097 (probe in_view at least 41 each seed).
Touches the stop file on any FAIL line.

Usage: decide_r134.py NAME STOPFILE
"""
import json, subprocess, sys
from pathlib import Path

S = Path(__file__).parent
VP = "../venv/Scripts/python.exe"
EVAL = Path("results/recall_eval")
name, stop = sys.argv[1], S / sys.argv[2]


def count(label, kinds):
    rows = json.loads((EVAL / f"{label}_seed_73157.json").read_text(encoding="utf-8"))["rows"]
    return sum(bool(r["correct"]) for r in rows if r["arm"] == "tool_loop" and r["kind"] in kinds)


out = ""
for script in ("scripts/records/gate_r086.py", "scripts/records/stone_report.py"):
    r = subprocess.run([VP, script, name], capture_output=True, text=True, encoding="utf-8")
    out += r.stdout + r.stderr
lines = [x for x in out.splitlines() if x.startswith(("PASS", "FAIL"))]
for pool, stem in (("probe", "probe"), ("hard_dev", "hd")):
    ref = sum(count(f"{stem}_fix17cs37_{s}", ("older", "confirm")) for s in (82, 83))
    got = sum(count(f"{stem}_{name}_{s}", ("older", "confirm")) for s in (82, 83))
    lines.append(f"{'PASS' if got >= ref else 'FAIL'}  {pool} recall pooled {got} not below 6.37's {ref} (R-134)")
for s in (82, 83):
    got = count(f"probe_{name}_{s}", ("in_view",))
    lines.append(f"{'PASS' if got >= 41 else 'FAIL'}  probe in_view at seed {s} {got} at least 41 (R-097)")
print("\n".join(lines))
fails = [x for x in lines if x.startswith("FAIL")]
if fails:
    stop.touch()
    print(f"== {name} fails (R-134): {len(fails)} lines; {stop.name} touched")
else:
    print(f"== {name} passes every line read so far (R-134)")
