"""A stepping stone's counts against v6 and base on every measure it was scored on (R-103, R-104).

Usage: python scripts/records/stone_report.py <name>     e.g. fix17cr (6.1)

Prints recall (older + confirm), each kind and the who-is-who slips (R-094) for the plain probe and
hard_dev sets and the messy forms (R-099, R-102), at seeds 82 and 83, beside v6 (fix17m) and base;
then R-102's held-out corrections bar and phone guard, R-094's slip gate and recall line, and how
the stone's hard_dev recall misses split. A stone is not gated (R-103); these are its targets.
"""

import json
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.scoring import slip_shape

EVAL = Path("results/recall_eval")
RECALL = ("older", "confirm")
SEEDS = (82, 83)
SETS = {
    "probe": "plain, probe",
    "hd": "plain, hard_dev",
    "st_fixh_probe": "held-out corrections, probe",
    "st_fixh_hd": "held-out corrections, hard_dev",
    "st_fix_probe": "training-worded corrections, probe",
    "st_phone_probe": "phone typing, probe",
    "st_phone_hd": "phone typing, hard_dev",
}
# Base on the plain probe at seed 73157 was scored under this label.
BASE_LABELS = {"probe": "probe2_base"}


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


def miss_kind(r):
    reply = r["reply"].lower()
    if not r["queries"]:
        return "did not search"
    if not r["found_fact"]:
        return "search missed"
    if r["answer"].lower() in reply:
        return "named the value and another"
    if reply.startswith("it sounds") or len(reply) > 150:
        return "summary"
    if "don't know" in reply:
        return "said unknown"
    return "found, answered without the asked detail"


name = sys.argv[1]
table = {}
for stem, title in SETS.items():
    table[stem] = {
        m: counts(BASE_LABELS.get(stem, f"{stem}_base") if m == "base" else f"{stem}_{m}")
        for m in ("base", *(f"{n}_{s}" for n in ("fix17m", name) for s in SEEDS))
    }
    print(f"\n{title}")
    for model, tally in table[stem].items():
        if tally:
            print(f"  {model:14s} " + "  ".join(f"{k} {v}" for k, v in sorted(tally.items())))


def pooled(stem, model, key="recall"):
    return sum(table[stem][f"{model}_{s}"][key] for s in SEEDS)


def line(text, ok):
    print(f"{'PASS' if ok else 'FAIL'}  {text}")


def scored(*stems):
    """Return True if every seed's file exists for these sets; otherwise say the section waits."""
    ready = all(table[st][f"{m}_{s}"] for st in stems for m in ("fix17m", name) for s in SEEDS)
    if not ready:
        print("  not scored at every seed yet; skipped")
    return ready


print("\nR-102, held-out corrections and phone guard (82 + 83 pooled, of 192)")
FIXH, PHONE = ("st_fixh_probe", "st_fixh_hd"), ("st_phone_probe", "st_phone_hd")
for stem, gain in zip(FIXH, (48, 32), strict=True) if scored(*FIXH) else ():
    stone, v6 = pooled(stem, name), pooled(stem, "fix17m")
    line(f"{stem} {stone} at least v6's {v6} + {gain}", stone >= v6 + gain)
    each = all(
        table[stem][f"{name}_{s}"]["recall"] > table[stem][f"fix17m_{s}"]["recall"] for s in SEEDS
    )
    line(f"{stem} above v6 at each seed", each)
for stem, room in zip(PHONE, (8, 16), strict=True) if scored(*PHONE) else ():
    stone, v6 = pooled(stem, name), pooled(stem, "fix17m")
    line(f"{stem} {stone} not below v6's {v6} by more than {room}", stone >= v6 - room)

print("\nR-094, slips and recall (plain sets)")
for stem, each_max in (("probe", 5), ("hd", 3)):
    for s in SEEDS:
        slips = table[stem][f"{name}_{s}"]["slips"]
        line(f"{stem} slips at seed {s} {slips} at most {each_max}", slips <= each_max)
probe_slips = pooled("probe", name, "slips")
line(f"probe slips pooled {probe_slips} at most 8", probe_slips <= 8)
for stem in ("probe", "hd"):
    stone, v6 = pooled(stem, name), pooled(stem, "fix17m")
    line(f"{stem} recall pooled {stone} not below v6's {v6}", stone >= v6)

print("\nhard_dev recall misses, by what the reply did")
for s in SEEDS:
    misses = [r for r in rows(f"hd_{name}_{s}") if r["kind"] in RECALL and not r["correct"]]
    print(
        f"  seed {s}: {len(misses)} -- "
        + ", ".join(f"{k} {v}" for k, v in Counter(map(miss_kind, misses)).most_common())
    )
