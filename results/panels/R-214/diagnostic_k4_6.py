"""R-214: K4.6 seed 82 against K1.3, K4.1 and K4.5 on hard_dev and the outside-writer sets.

Older and confirm rows of the tool_loop arm, split by outcome; never_told right; for hard_dev, false
retrieval as ``decide_r191`` counts it. A decline is a rough phrase match, for design only.

Usage: python results/panels/R-214/diagnostic_k4_6.py
"""

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

spec = importlib.util.spec_from_file_location("d", "scripts/records/decide_r191.py")
D = importlib.util.module_from_spec(spec)
sys.modules["d"] = D
spec.loader.exec_module(D)
DECLINE = re.compile(
    r"don't|do not|not sure|guess|no idea|haven't|not told|didn't|can't|nothing on|what is it", re.I
)


def outcomes(label: str, seed: int) -> Counter | None:
    path = Path(f"results/recall_eval/{label}_seed_{seed}.json")
    if not path.exists():
        return None
    c = Counter()
    for r in json.loads(path.read_text(encoding="utf-8"))["rows"]:
        if r["arm"] != "tool_loop":
            continue
        if r["kind"] == "never_told":
            c["never_told right"] += bool(r["correct"])
            continue
        if r["kind"] not in ("older", "confirm"):
            continue
        if r["correct"]:
            c["right"] += 1
        elif not r.get("queries"):
            c["no search"] += 1
        elif not r.get("found_fact"):
            c["never found"] += 1
        else:
            c["found, declined" if DECLINE.search(r["reply"]) else "found, other line"] += 1
    return c


for name in ("k1_3_r200", "k4_1_r209", "k4_5_r213", "k4_6_r214"):
    for pre, seed in (("hd", 73157), ("blind", 0), ("blind2", 0)):
        c = outcomes(f"{pre}_{name}_82", seed)
        if c is None:
            continue
        extra = ""
        if pre == "hd":
            fr = sum(h for h, _ in D.false_retrieval(f"hd_{name}_82", 73157).values())
            extra = f", false retrieval {fr}"
        print(f"{pre:6} {name}: {dict(sorted(c.items()))}{extra}")
