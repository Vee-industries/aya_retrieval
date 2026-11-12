"""R-198's check before training: K1.2's set against the registered lines, with K1 for scale.

Lines (a FAIL on any one means nothing trains):
1. Of the F2 fact lines as built (the build's count, before F3, lines out of view included), more
   than half are in a drawn wording, so the template wording no longer marks most fact lines.
2. Four-word runs shared by the statement wordings the set uses and hard_dev's forms: 0.
3. never_told rows with passages: all of them; found against never_told mean passage gap at most
   0.37 (R-185's lines 3 and 4).
4. With each drawn wording mapped back to its template, every turn but the search output and the
   last reply equals K1's, in every row but the fresh never_told rows, except at most 11 rows (1%
   of the set), each listed; rows whose last reply differs are at most the build's now-missed and
   scripted-target rows.
Reported only: the drawn share of the fact lines in search outputs, in found and in never_told rows;
the rows whose draw did not reach K1's passage count; the draws taken.

Usage:
    python scripts/records/check_r198.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.conversations import NEEDS_SEARCH, NEVER_TOLD
from aya_retrieval.pool_hard_dev import HARD_DEV

HERE = Path(__file__).resolve().parent
NAME = "k1_2_r198"
MAX_GAP = 0.37
MAX_OTHER = 11


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


R196 = load_module("check_r196")


def output_lines(rows: list[dict]) -> dict[str, Counter]:
    """Fact lines in search outputs by wording, for found rows and for never_told rows."""
    counts = {"found": Counter(), NEVER_TOLD: Counter()}
    for row in rows:
        if row["kind"] not in NEEDS_SEARCH:
            continue
        side = counts[NEVER_TOLD if row["kind"] == NEVER_TOLD else "found"]
        for turn in row["turns"]:
            if R196.tool_output(turn):
                for line in R196.re.findall(r"^User: (.*)$", turn["content"], R196.re.M):
                    got = R196.wording(line)
                    if got:
                        side[got[0]] += 1
    return counts


def main() -> None:
    k1, k12 = R196.rows("k1_r178"), R196.rows(NAME)
    report = json.loads((R196.DATA / f"{NAME}.provenance.json").read_text(encoding="utf-8"))
    tally = report["tally"]

    built = report["f2_fact_lines"]
    share = built.get("drawn", 0) / max(1, sum(built.values()))

    used = set()
    for row in k12:
        for line in R196.fact_lines(row):
            got = R196.wording(line)
            if got:
                used.add(got[1])
    hd_forms = [getattr(t, f) for t in HARD_DEV.facts.values() for f in R196.FIELDS]
    hd_grams = set().union(*(R196.grams(f) for f in hd_forms))
    shared = sorted({" ".join(g) for w in used for g in R196.grams(w) if g in hd_grams})

    s = R196.CHECK.stats(k12)
    gap = abs(s["found_mean"] - s["never_told_mean"])

    other, last = [], 0
    for a, b in zip(k1, k12, strict=True):
        if a["id"].startswith("k1/never_told_") or b["id"].startswith("k1/never_told_"):
            continue
        keep = [i for i, t in enumerate(b["turns"][:-1]) if not R196.tool_output(t)]
        if len(a["turns"]) != len(b["turns"]) or any(
            R196.mapped(a["turns"][i]["content"]) != R196.mapped(b["turns"][i]["content"])
            for i in keep
        ):
            other.append(b["id"])
        elif a["turns"][-1] != b["turns"][-1]:
            last += 1
    allowed = sum(v for k, v in tally.items() if k.endswith(("_now_missed", "_scripted_target")))

    checks = [
        (
            f"drawn wordings {built.get('drawn', 0)} of {sum(built.values())} F2 fact lines as "
            f"built ({share:.1%}), more than 50%",
            share > 0.5,
        ),
        (f"four-word runs shared with hard_dev forms {len(shared)} {shared}", not shared),
        (
            f"never_told with passages {s['with_passages']} of {s['never_told']}",
            s["with_passages"] == s["never_told"],
        ),
        (f"mean passage gap {gap:.2f} at most {MAX_GAP}", gap <= MAX_GAP),
        (
            f"rows unlike K1 beyond wording and last reply {len(other)}, "
            f"at most {MAX_OTHER}: {other}",
            len(other) <= MAX_OTHER,
        ),
        (f"rows whose last reply differs {last}, at most {allowed}", last <= allowed),
    ]
    for text, ok in checks:
        print(f"{'PASS' if ok else 'FAIL':5} {text}")
    for side, counts in output_lines(k12).items():
        total = sum(counts.values())
        print(
            f"report: {side} search-output fact lines drawn {counts['more']} of {total} "
            f"({counts['more'] / max(1, total):.1%})"
        )
    print(
        f"report: passages found {s['found_mean']:.2f}, never_told {s['never_told_mean']:.2f}; "
        f"draws {report['draws']}; rows not reaching K1 {len(report['rows_not_reaching_k1'])}"
    )
    print(f"== {NAME} check: {sum(not ok for _, ok in checks)} FAIL (R-198 lines)")


if __name__ == "__main__":
    main()
