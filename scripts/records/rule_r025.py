"""R-025's rule: fix 1b (probe4) against v2 (probe3), pooled over seeds, probe seed 73157."""

import json
import sys

R = sys.argv[1]
seeds = [int(s) for s in sys.argv[2:]] or [82, 83, 84]


def load(label):
    rows = json.load(open(f"{R}/{label}_seed_73157.json", encoding="utf-8"))["rows"]
    return [r for r in rows if r.get("arm", "tool_loop") == "tool_loop"]


def stats(rows):
    rec = sum(r["correct"] for r in rows if r["kind"] in ("older", "confirm"))
    iv = sum(r["correct"] for r in rows if r["kind"] == "in_view")
    return rec, iv, sum(r.get("right_decision", 0) for r in rows)


base = stats(load("probe2_base"))
print("base rec, in_view, decisions", base)
tot = {}
for v, lab in (("v2", "probe3_tuned"), ("1b", "probe4_tuned")):
    acc = [0, 0]
    for s in seeds:
        st = stats(load(f"{lab}{s}"))
        print(v, s, st)
        acc[0] += st[0]
        acc[1] += st[1]
    tot[v] = acc
n = len(seeds)
for v in tot:
    rec_gain = (tot[v][0] / n / base[0] - 1) * 100
    iv_gain = (tot[v][1] / n / base[1] - 1) * 100
    print(
        v,
        f"pooled rec {tot[v][0]}/{96 * n} in_view {tot[v][1]}/{48 * n}",
        f"rec above base {rec_gain:+.0f}%",
        f"in_view above base {iv_gain:+.0f}%",
    )
rec_change = (tot["1b"][0] / tot["v2"][0] - 1) * 100
iv_change = (tot["1b"][1] / tot["v2"][1] - 1) * 100
print(f"1b vs v2: rec {rec_change:+.1f}%, in_view {iv_change:+.1f}%")
