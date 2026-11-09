"""R-156 queue step for 7.1 (fix17cs71): R-153's lines as registered. R-086 unjudged at 82 and 83 (gate_r086.py) and
R-094's slip lines (stone_report.py); R-094's pooled recall lines against v6 are replaced (R-153 item 1) by the five-seed lines: probe and hard_dev recall over seeds 82, 83, 94, 95, 96 not below
6.37's at the same five seeds, and probe in_view at least 41 at each seed (R-097). Touches the stop file on any FAIL.
Lines for seeds not yet scored are skipped and printed as WAIT.

Usage: decide_r153.py NAME STOPFILE
"""
import json, subprocess, sys
from pathlib import Path

S = Path(__file__).parent
VP = "../venv/Scripts/python.exe"
EVAL = Path("results/recall_eval")
SEEDS = (82, 83, 94, 95, 96)
name, stop = sys.argv[1], S / sys.argv[2]


def count(label, kinds):
    path = EVAL / f"{label}_seed_73157.json"
    if not path.exists():
        return None
    rows = json.loads(path.read_text(encoding="utf-8"))["rows"]
    return sum(bool(r["correct"]) for r in rows if r["arm"] == "tool_loop" and r["kind"] in kinds)


out = ""
for script in ("scripts/records/gate_r086.py", "scripts/records/stone_report.py"):
    r = subprocess.run([VP, script, name], capture_output=True, text=True, encoding="utf-8")
    out += r.stdout + r.stderr
# R-153 item 1: the pooled recall lines against v6 are replaced by the five-seed lines below.
lines = [x for x in out.splitlines() if x.startswith(("PASS", "FAIL")) and "not below v6's" not in x]
for stem in ("probe", "hd"):
    got = [count(f"{stem}_{name}_{s}", ("older", "confirm")) for s in SEEDS]
    ref = [count(f"{stem}_fix17cs37_{s}", ("older", "confirm")) for s in SEEDS]
    if None in got:
        lines.append(f"WAIT  {stem} recall over five seeds: scored {sum(g is not None for g in got)} of 5")
        continue
    lines.append(f"{'PASS' if sum(got) >= sum(ref) else 'FAIL'}  {stem} recall over 82, 83, 94-96 {sum(got)} "
                 f"{got} not below 6.37's {sum(ref)} {ref} (R-153)")
for s in SEEDS:
    got = count(f"probe_{name}_{s}", ("in_view",))
    if got is not None:
        lines.append(f"{'PASS' if got >= 41 else 'FAIL'}  probe in_view at seed {s} {got} at least 41 (R-097)")
print("\n".join(lines))
fails = [x for x in lines if x.startswith("FAIL")]
if fails:
    stop.touch()
    print(f"== {name} fails (R-156): {len(fails)} lines; {stop.name} touched")
else:
    print(f"== {name} passes every line read so far (R-156)")
