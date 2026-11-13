"""Blind judge sheet for Demo2's answers (R-201), and the tally by kind once both judges mark it.

``sheet`` writes ``results/demo2/judge/sheet.md`` (every arm's answers shuffled together with
``random.Random(201)``, no model names) and ``key.json``. ``tally`` reads ``marks_j1.txt`` and
``marks_j2.txt`` (one ``<item> | <LABEL> | <reason>`` line each), counts an answer right only when
both judges mark it RIGHT or RIGHT_INVENTED, and writes ``tally.json``: per arm and kind (older,
in_view, never_told plain 9-10, never_told sharing a word 11-12), never one total (R-201 lane,
finding 6), beside the arm that declines every question.

Usage:
    python scripts/records/demo2_judges.py sheet
    python scripts/records/demo2_judges.py tally
"""

from __future__ import annotations

import json
import random
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUN = REPO_ROOT / "results" / "demo2" / "branches.json"
OUT = REPO_ROOT / "results" / "demo2" / "judge"
BRIEF = REPO_ROOT / "results" / "panels" / "R-201" / "judge_brief_demo2.md"
LABELS = {"RIGHT", "RIGHT_INVENTED", "WRONG", "ABSTAINED"}
RIGHT = {"RIGHT", "RIGHT_INVENTED"}


def kind(answer: dict) -> str:
    if answer["kind"] != "never_told":
        return answer["kind"]
    return "never_told_plain" if answer["number"] <= 10 else "never_told_shared_word"


def sheet() -> None:
    arms = json.loads(RUN.read_text(encoding="utf-8"))["arms"]
    rows = [{"arm": arm, **a} for arm, run in arms.items() for a in run["answers"]]
    random.Random(201).shuffle(rows)
    lines = [BRIEF.read_text(encoding="utf-8").rstrip(), "", "## Items", ""]
    for n, r in enumerate(rows, 1):
        lines += [
            f"{n}. Question: {r['question']}",
            f"   Key: {r['key']}",
            f"   Same meaning: {', '.join(r['same_meaning'])}",
            f"   Reply: {r['reply']}",
            "",
        ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "sheet.md").write_text("\n".join(lines), encoding="utf-8")
    key = [
        {"item": n, "arm": r["arm"], "number": r["number"], "kind": kind(r)}
        for n, r in enumerate(rows, 1)
    ]
    (OUT / "key.json").write_text(json.dumps(key, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} items")


def marks(name: str) -> dict[int, str]:
    out = {}
    for line in (OUT / name).read_text(encoding="utf-8").splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 2 and parts[0].isdigit():
            if parts[1] not in LABELS:
                raise SystemExit(f"{name}: unknown label {parts[1]!r} on item {parts[0]}")
            out[int(parts[0])] = parts[1]
    return out


def tally() -> None:
    key = json.loads((OUT / "key.json").read_text(encoding="utf-8"))
    j1, j2 = marks("marks_j1.txt"), marks("marks_j2.txt")
    if set(j1) != set(j2) or len(j1) != len(key):
        raise SystemExit(f"marks cover {len(j1)} and {len(j2)} of {len(key)} items")
    right, total, rows = Counter(), Counter(), []
    for k in key:
        a, b = j1[k["item"]], j2[k["item"]]
        ok = a in RIGHT and b in RIGHT
        total[k["arm"], k["kind"]] += 1
        right[k["arm"], k["kind"]] += ok
        rows.append({**k, "judge_1": a, "judge_2": b, "counted_right": ok, "agree": a == b})
    arms = sorted({a for a, _ in total}, key=[k["arm"] for k in key].index)
    kinds = ("older", "in_view", "never_told_plain", "never_told_shared_word")
    per_arm = {a: {k: f"{right[a, k]} of {total[a, k]}" for k in kinds} for a in arms}
    per_arm["declines everything"] = {
        k: f"{total[arms[0], k] if k.startswith('never') else 0} of {total[arms[0], k]}"
        for k in kinds
    }
    report = {"per_arm": per_arm, "disagreements": sum(not r["agree"] for r in rows), "items": rows}
    (OUT / "tally.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(per_arm, indent=1), "disagreements:", report["disagreements"])


if __name__ == "__main__":
    {"sheet": sheet, "tally": tally}[sys.argv[1]]()
