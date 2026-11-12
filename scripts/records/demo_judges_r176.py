"""Blind judge sheet for the R-176 demo answers, and the tally once both judges have marked it.

``sheet`` writes ``results/demo/r176_judge/sheet.md`` (items shuffled with ``random.Random(176)``,
no model names) and ``key.json`` (which arm and question each item is). ``tally`` reads the two
judges' marks (``marks_j1.txt``, ``marks_j2.txt``: one ``<item> | <LABEL> | <reason>`` line each),
counts an answer right only when both judges mark it RIGHT or RIGHT_INVENTED, and writes
``results/demo/r176_judge/tally.json``.

Usage:
    python scripts/records/demo_judges_r176.py sheet
    python scripts/records/demo_judges_r176.py tally
"""

from __future__ import annotations

import json
import random
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
RUN = REPO_ROOT / "results" / "demo" / "branches_r176.json"
OUT = REPO_ROOT / "results" / "demo" / "r176_judge"
BRIEF = REPO_ROOT / "results" / "panels" / "R-176" / "judge_brief.md"
LABELS = {"RIGHT", "RIGHT_INVENTED", "WRONG", "ABSTAINED"}
ARMS = ("base_no_search", "6.37_no_search", "base", "6.37")


def items() -> list[dict]:
    arms = json.loads(RUN.read_text(encoding="utf-8"))["arms"]
    rows = [
        {
            "arm": arm,
            "source_message": a["source_message"],
            "question": a["question"],
            "key": a["key"],
            "same_meaning": a["same_meaning"],
            "reply": a["reply"],
        }
        for arm in ARMS
        for a in arms[arm]["answers"]
    ]
    random.Random(176).shuffle(rows)
    return rows


def sheet() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = items()
    lines = [BRIEF.read_text(encoding="utf-8").rstrip(), "", "## Items", ""]
    for n, r in enumerate(rows, 1):
        lines += [
            f"{n}. Question: {r['question']}",
            f"   Key: {r['key']}",
            f"   Same meaning: {', '.join(r['same_meaning'])}",
            f"   Reply: {r['reply']}",
            "",
        ]
    (OUT / "sheet.md").write_text("\n".join(lines), encoding="utf-8")
    key = [
        {"item": n, "arm": r["arm"], "source_message": r["source_message"]}
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
    right = {"RIGHT", "RIGHT_INVENTED"}
    per_arm = {
        arm: {"facts_right": 0, "facts": 0, "never_told_right": 0, "never_told": 0} for arm in ARMS
    }
    rows = []
    for k in key:
        a, b = j1[k["item"]], j2[k["item"]]
        ok = a in right and b in right
        cell = per_arm[k["arm"]]
        kind = "facts" if k["source_message"] else "never_told"
        cell[kind] += 1
        cell[f"{kind}_right"] += ok
        rows.append({**k, "judge_1": a, "judge_2": b, "counted_right": ok, "agree": a == b})
    report = {"per_arm": per_arm, "disagreements": sum(not r["agree"] for r in rows), "items": rows}
    (OUT / "tally.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(per_arm, indent=1), "disagreements:", report["disagreements"])


if __name__ == "__main__":
    {"sheet": sheet, "tally": tally}[sys.argv[1]]()
