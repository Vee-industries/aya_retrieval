"""R-122 queue step: gate a copy (R-086 unjudged + R-094), stop its stress lines on a fail, pick the next set.

Usage: decide_r122.py NAME STOPFILE [--pick-next]
--pick-next (after 6.33 only): writes r122_next = fix17cs35 (B) if the only fail is the probe 51203
statement line, else fix17cs34 (C), as the R-122 panel ruled.
"""
import subprocess, sys
from pathlib import Path

S = Path(__file__).parent
VP = "../venv/Scripts/python.exe"
name, stop = sys.argv[1], S / sys.argv[2]
out = ""
for script in ("scripts/records/gate_r086.py", "scripts/records/stone_report.py"):
    r = subprocess.run([VP, script, name], capture_output=True, text=True, encoding="utf-8")
    out += r.stdout + r.stderr
print(out)
fails = [x for x in out.splitlines() if x.startswith("FAIL")]
if fails:
    stop.touch()
    print(f"== {name} fails (R-122): {len(fails)} lines; {stop.name} touched")
else:
    print(f"== {name} passes R-086 unjudged and R-094 (R-122)")
if "--pick-next" in sys.argv:
    only_statement = len(fails) == 1 and "probe 51203 statement" in fails[0]
    nxt = "fix17cs35" if only_statement else "fix17cs34"
    (S / "r122_next").write_text(nxt)
    print(f"== next set: {nxt}")
