"""R-022's three-vs-three rule, pooled over seeds 82, 83, 84 on probe seed 73157."""

import json
import sys

R = sys.argv[1]


def load(label):
    return json.load(open(f"{R}/{label}_seed_73157.json", encoding="utf-8"))["rows"]


base = load("probe2_base")


def stats(rows):
    rec = sum(r["correct"] for r in rows if r["kind"] in ("older", "confirm"))
    cf = [r for r in rows if r["kind"] == "confirm" and r["found_fact"]]
    dec = sum(r.get("right_decision", 0) for r in rows) if "right_decision" in rows[0] else None
    n = sum(1 for r in rows if r["kind"] in ("older", "confirm"))
    return rec, n, sum(r["correct"] for r in cf), len(cf), dec


b = stats([r for r in base if r["arm"] == "tool_loop"] if "arm" in base[0] else base)
print("base", b)
tot = {}
for v, lab in (("v1", "probe2_tuned"), ("v2", "probe3_tuned")):
    acc = [0, 0, 0, 0]
    for s in (82, 83, 84):
        st = stats(load(f"{lab}{s}"))
        print(v, s, st)
        for i in range(4):
            acc[i] += st[i]
    tot[v] = acc
    print(v, "pooled recall", acc[0], "/", acc[1], "confirm read", acc[2], "/", acc[3])
br = b[0] / b[1]
for v in tot:
    print(v, f"recall above base: {(tot[v][0] / tot[v][1] / br - 1) * 100:+.0f}%")
print(f"v2 vs v1 recall: {(tot['v2'][0] / tot['v1'][0] - 1) * 100:+.1f}%")
read_v1 = 100 * tot["v1"][2] / tot["v1"][3]
read_v2 = 100 * tot["v2"][2] / tot["v2"][3]
print(f"confirm read v1 {read_v1:.1f}% v2 {read_v2:.1f}%")
