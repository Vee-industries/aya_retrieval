"""R-203: fact questions (older, confirm) by outcome, K1 against K1.3, pooled over seeds 82, 83 and 94.

A wrong reply whose search output held the fact is split by a rough phrase match into declines and
other lines; this is for design only, not a judged result.

Usage: python results/panels/R-203/failure_types.py
"""

import json
import re
from collections import Counter

DECLINE = re.compile(
    r"don't|do not|not sure|guess|no idea|haven't|not told|didn't|can't|what is it", re.I
)
for pre, seed in (("hd", 73157), ("probe", 73157), ("blind", 0), ("blind2", 0)):
    for who in ("k1_r178", "k1_3_r200"):
        c, n = Counter(), 0
        for s in (82, 83, 94):
            path = f"results/recall_eval/{pre}_{who}_{s}_seed_{seed}.json"
            for r in json.load(open(path, encoding="utf-8"))["rows"]:
                if r["kind"] not in ("older", "confirm"):
                    continue
                n += 1
                if r["correct"]:
                    c["right"] += 1
                elif not r.get("queries"):
                    c["no_search"] += 1
                elif not r.get("found_fact"):
                    c["not_found"] += 1
                else:
                    c["found_declines" if DECLINE.search(r["reply"]) else "found_other_line"] += 1
        print(pre, who, n, dict(sorted(c.items())))
