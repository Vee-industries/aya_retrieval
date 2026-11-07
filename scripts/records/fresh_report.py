"""A candidate's unjudged lines at the fresh seeds 91 to 93 (R-094, R-102, R-111).

Usage: python scripts/records/fresh_report.py <name>     e.g. fix17cs2 (6.2)

Prints recall (older + confirm), each kind and the who-is-who slips for the plain probe and
hard_dev sets and the messy forms at 91, 92 and 93, beside v6 (fix17m) at the same seeds where v6
ran; then R-094's slip gate (per seed, and the probe pooled over 82, 83, 91, 92 and 93) and recall
line against v6 at the same seeds, R-102's seed-91-to-93 items against v6's 82-and-83 mean, and
the hard_dev recall that R-111 compares. R-076's rule, with its judged sheets, is
scripts/records/rule_r076.py.
"""

import json
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.scoring import slip_shape

EVAL = Path("results/recall_eval")
RECALL = ("older", "confirm")
FRESH = (91, 92, 93)
GATE = (82, 83)
SETS = {
    "probe": "plain, probe",
    "hd": "plain, hard_dev",
    "st_fixh_probe": "held-out corrections, probe",
    "st_fixh_hd": "held-out corrections, hard_dev",
    "st_phone_probe": "phone typing, probe",
    "st_phone_hd": "phone typing, hard_dev",
}


def rows(label):
    path = EVAL / f"{label}_seed_73157.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return [r for r in data["rows"] if r["arm"] == "tool_loop"]


def counts(label):
    found = rows(label)
    if found is None:
        return None
    tally = Counter()
    for r in found:
        tally[r["kind"]] += bool(r["correct"])
        if r["kind"] in RECALL:
            tally["recall"] += bool(r["correct"])
            tally["slips"] += slip_shape(r["reply"], r["message"])
    return tally


def recall(stem, model, seed, key="recall"):
    tally = counts(f"{stem}_{model}_{seed}")
    if tally is None:
        raise SystemExit(f"{stem}_{model}_{seed} is not scored yet")
    return tally[key]


def line(text, ok):
    print(f"{'PASS' if ok else 'FAIL'}  {text}")


name = sys.argv[1]
for stem, title in SETS.items():
    print(f"\n{title}")
    for model in ("fix17m", name):
        for s in FRESH:
            tally = counts(f"{stem}_{model}_{s}")
            if tally:
                print(
                    f"  {model}_{s:<6d} " + "  ".join(f"{k} {v}" for k, v in sorted(tally.items()))
                )

print("\nR-094, slips (plain sets) and recall against v6 at the same seeds")
for stem, each_max in (("probe", 5), ("hd", 3)):
    for s in FRESH:
        slips = recall(stem, name, s, "slips")
        line(f"{stem} slips at seed {s} {slips} at most {each_max}", slips <= each_max)
pooled_slips = sum(recall("probe", name, s, "slips") for s in GATE + FRESH)
line(f"probe slips pooled over 82, 83, 91 to 93 {pooled_slips} at most 8", pooled_slips <= 8)
for stem in ("probe", "hd"):
    stone = sum(recall(stem, name, s) for s in FRESH)
    v6 = sum(recall(stem, "fix17m", s) for s in FRESH)
    line(f"{stem} recall pooled at 91 to 93 {stone} not below v6's {v6}", stone >= v6)

print("\nR-102 at 91 to 93, against v6's 82-and-83 mean (of 96)")
for stem, gain in (("st_fixh_probe", 24), ("st_fixh_hd", 16)):
    mean = sum(recall(stem, "fix17m", s) for s in GATE) / len(GATE)
    for s in FRESH:
        got = recall(stem, name, s)
        line(f"{stem} seed {s} {got} at least {mean:g} + {gain}", got >= mean + gain)
mean = sum(recall("st_phone_probe", "fix17m", s) for s in GATE) / len(GATE)
for s in FRESH:
    got = recall("st_phone_probe", name, s)
    line(f"st_phone_probe seed {s} {got} within 4 of {mean:g}", got >= mean - 4)
mean = sum(recall("st_phone_hd", "fix17m", s) for s in GATE) / len(GATE)
got = sum(recall("st_phone_hd", name, s) for s in FRESH) / len(FRESH)
line(f"st_phone_hd three-seed mean {got:.2f} within 8 of {mean:g}", got >= mean - 8)

hd = sum(recall("hd", name, s) for s in FRESH)
print(f"\nR-111: hard_dev recall pooled at 91 to 93: {hd} of 288")
