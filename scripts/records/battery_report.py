"""A copy's messy-chat battery at seeds 82 and 83, read by R-099's registered trigger (R-102).

Usage: python scripts/records/battery_report.py <name>     e.g. fix17m (v6, R-102), fix17cs37 (6.37)

For each messy form and pool: messy minus plain, same adapter and items, tool arm, pooled over seeds
82 and 83: recall (older + confirm, of 192) and in_view, never_told and statement (of 96 each).
R-099 item 3: a form is a gap if it costs at least 8 of 192 recall answers, or at least 4 of 96 on
one of the other kinds. A form scored on recall only (corrections) shows "recall only".
"""

import json
import sys
from pathlib import Path

EVAL = Path("results/recall_eval")
SEEDS = (82, 83)
RECALL = ("older", "confirm")
OTHER = ("in_view", "never_told", "statement")
FORMS = {
    "st_style": "lower-case typing",
    "st_phone": "phone typing",
    "st_fix": "fact corrected later",
    "st_asked": "earlier question in view",
}
POOLS = {"probe": "probe", "hd": "hard_dev"}


def counts(label):
    path = EVAL / f"{label}_seed_73157.json"
    if not path.exists():
        raise SystemExit(f"{label} is not scored yet")
    rows = [
        r for r in json.loads(path.read_text(encoding="utf-8"))["rows"] if r["arm"] == "tool_loop"
    ]
    tally = {k: 0 for k in OTHER}
    tally["recall"] = 0
    kinds = {r["kind"] for r in rows}
    for r in rows:
        key = "recall" if r["kind"] in RECALL else r["kind"]
        if key in tally:
            tally[key] += bool(r["correct"])
    return tally, kinds


def pooled(stem):
    total, kinds = {}, set()
    for s in SEEDS:
        tally, seen = counts(f"{stem}_{s}")
        kinds |= seen
        for k, v in tally.items():
            total[k] = total.get(k, 0) + v
    return total, kinds


name = sys.argv[1]
any_gap = False
for form, title in FORMS.items():
    for pool, pool_title in POOLS.items():
        plain, _ = pooled(f"{pool}_{name}")
        messy, kinds = pooled(f"{form}_{pool}_{name}")
        diff = {k: messy[k] - plain[k] for k in plain}
        gap = diff["recall"] <= -8
        parts = [f"recall {diff['recall']:+d} /192"]
        if kinds & set(OTHER):
            for k in OTHER:
                parts.append(f"{k} {diff[k]:+d}")
                gap |= diff[k] <= -4
        else:
            parts.append("recall only")
        any_gap |= gap
        print(f"{'GAP ' if gap else 'ok  '} {title}, {pool_title}: " + ", ".join(parts))
print(f"\n{name}: {'at least one gap' if any_gap else 'no gap'} by R-099's trigger")
