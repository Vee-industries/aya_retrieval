"""R-076's rule, as written, for any candidate at three seeds.

Usage: python scripts/records/rule_r076.py <name> <record> <judge> <seed> <seed> <seed>
    e.g. python scripts/records/rule_r076.py fix17b R-091 1 85 86 87

Counts come from probe_<name>_<seed> and hd_<name>_<seed>. R-074's items, with item 3 at v5's
172 (R-076). Coherence marks and keys are read from results/coherence/<record>:
judge/marks_<sheet><seed>_j<judge>.json and sheet_<sheet><seed>/key.json, for sheets a (Sheet A),
b (Sheet B) and h (hard_dev Sheet B). The judge named decides (R-089). A seed whose sheets are
not yet marked is reported as missing, and the rule is not decided.
"""

import json
import sys
from pathlib import Path

from aya_retrieval.report_data import false_retrieval

EVAL = Path("results/recall_eval")
COHERENCE = Path("results/coherence")
name, RECORD, JUDGE = sys.argv[1], sys.argv[2], sys.argv[3]
seeds = [int(s) for s in sys.argv[4:]]


def rows(label):
    data = json.loads((EVAL / f"{label}_seed_73157.json").read_text(encoding="utf-8"))
    return [r for r in data["rows"] if r["arm"] == "tool_loop"]


def count(label, kinds):
    return sum(bool(r["correct"]) for r in rows(label) if r["kind"] in kinds)


def coherent(record, sheet, seed):
    """Coherent replies per (model, kind) on one sheet, or None if not yet marked."""
    marks_path = COHERENCE / record / "judge" / f"marks_{sheet}{seed}_j{JUDGE}.json"
    if not marks_path.exists():
        return None
    marks = {int(k): int(v) for k, v in json.loads(marks_path.read_text()).items()}
    key = json.loads((COHERENCE / record / f"sheet_{sheet}{seed}" / "key.json").read_text())
    out = {}
    for entry in key:
        model = "base" if entry["model"] == "base" else "tuned"
        out[(model, entry["kind"])] = out.get((model, entry["kind"]), 0) + marks[entry["line"]]
    return out


probe = {s: f"probe_{name}_{s}" for s in seeds}
hd = {s: f"hd_{name}_{s}" for s in seeds}


def record(sheet, seed):
    return RECORD


items = {}
recall = sum(count(probe[s], ("older", "confirm")) for s in seeds)
items["1a recall pooled above 252"] = (recall, recall > 252)
in_view = sum(count(probe[s], ("in_view",)) for s in seeds)
items["1b in_view pooled at least 110"] = (in_view, in_view >= 110)
statement = sum(count(probe[s], ("statement",)) for s in seeds)
items["1c statement pooled at least 136"] = (statement, statement >= 136)
decisions = [sum(bool(r["right_decision"]) for r in rows(probe[s])) for s in seeds]
items["1d right decisions at least 200 every seed"] = (decisions, min(decisions) >= 200)
fr = sum(sum(v[0] for v in false_retrieval(probe[s], 73157).values()) for s in seeds)
items["1e false retrieval pooled at most 39"] = (fr, fr <= 39)

sheets_a = [coherent(record("a", s), "a", s) for s in seeds]
sheets_b = [coherent(record("b", s), "b", s) for s in seeds]
sheets_h = [coherent(record("h", s), "h", s) for s in seeds]
if None not in sheets_a:
    pooled = {k: sum(sheet[k] for sheet in sheets_a) for k in sheets_a[0]}
    base_c, tuned_c = pooled[("base", "confirm")], pooled[("tuned", "confirm")]
    base_r, tuned_r = base_c + pooled[("base", "older")], tuned_c + pooled[("tuned", "older")]
    ok = tuned_c >= base_c and tuned_r >= base_r
    items["1f Sheet A confirm and older+confirm at or above base"] = (
        f"confirm {tuned_c} vs {base_c}, older+confirm {tuned_r} vs {base_r}",
        ok,
    )
else:
    items["1f Sheet A"] = ("missing", None)
if None not in sheets_b:
    per = [
        (
            sheet[("tuned", "statement")],
            sheet[("base", "statement")],
            sheet[("tuned", "in_view")],
            sheet[("base", "in_view")],
        )
        for sheet in sheets_b
    ]
    ok = all(ts >= bs and ti >= bi for ts, bs, ti, bi in per)
    items["1g Sheet B statement and in_view at or above base every seed"] = (per, ok)
else:
    items["1g Sheet B"] = ("missing", None)

items["2 probe recall pooled at least 273"] = (recall, recall >= 273)
hd_recall = sum(count(hd[s], ("older", "confirm")) for s in seeds)
items["3 hard_dev recall pooled at least 172"] = (hd_recall, hd_recall >= 172)
hd_fr = sum(sum(v[0] for v in false_retrieval(hd[s], 73157).values()) for s in seeds)
items["4 hard_dev false retrieval pooled at most 20"] = (hd_fr, hd_fr <= 20)
hd_nt = sum(count(hd[s], ("never_told",)) for s in seeds)
items["5 hard_dev never_told pooled at least 132"] = (hd_nt, hd_nt >= 132)
if None not in sheets_h:
    pooled = {k: sum(sheet[k] for sheet in sheets_h) for k in sheets_h[0]}
    ts, bs = pooled[("tuned", "statement")], pooled[("base", "statement")]
    ti, bi = pooled[("tuned", "in_view")], pooled[("base", "in_view")]
    items["6 hard_dev Sheet B statement and in_view pooled at or above base"] = (
        f"statement {ts} vs {bs}, in_view {ti} vs {bi}",
        ts >= bs and ti >= bi,
    )
else:
    items["6 hard_dev Sheet B"] = ("missing", None)

for name, (value, ok) in items.items():
    print(f"{'PASS' if ok else 'open' if ok is None else 'FAIL'}  {name}: {value}")
verdicts = [ok for _, ok in items.values()]
decided = None not in verdicts and len(seeds) == 3
print("RULE:", ("PASS" if all(verdicts) else "FAIL") if decided else "not decided")
