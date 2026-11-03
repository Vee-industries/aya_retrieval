"""Judge the coherence of base's own answers kept as training targets (fix 5, R-029).

Two steps, with a blind judge in between (D = results/coherence/R-029_fix5_targets):
    python scripts/run_target_coherence.py sheet data/screens/hard_in_view.jsonl D
    (a fresh judge marks D/sheet.txt with D/rubric.txt alone and writes D/marks.json)
    python scripts/run_target_coherence.py reject D data/screens/fix5_rejected.json

The sheet holds every ``older`` and ``confirm`` row whose search found the fact and whose answer is
not a tool call, shuffled with seed 5, showing the turns in view, the newest message and the answer.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

KINDS = ("older", "confirm")
SHUFFLE_SEED = 5


def found_fact_rows(rows: list[dict]) -> list[dict]:
    """Return the rows of KINDS whose search found the fact and whose last turn is an answer."""
    return [
        r
        for r in rows
        if r["kind"] in KINDS
        and not r["turns"][-1]["content"].startswith("{")
        and "No results" not in r["turns"][-2]["content"]
        and "chunk_id=" in r["turns"][-2]["content"]
    ]


def sheet(data: Path, out_dir: Path) -> None:
    rows = [json.loads(line) for line in data.read_text(encoding="utf-8").splitlines()]
    pick = found_fact_rows(rows)
    random.Random(SHUFFLE_SEED).shuffle(pick)
    lines, key = [], []
    for i, row in enumerate(pick):
        turns = row["turns"]
        view = turns[:-4]
        lines.append(f"LINE {i}")
        for j in range(0, len(view) - 1, 2):
            lines.append(f"  friend: {view[j]['content']}")
            lines.append(f"  you: {view[j + 1]['content']}")
        lines.append(f"  NEWEST MESSAGE: {turns[-4]['content']}")
        lines.append(f"  REPLY: {turns[-1]['content']}")
        lines.append("")
        key.append(row["id"])
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "sheet.txt").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "key.json").write_text(json.dumps(key), encoding="utf-8")
    print(f"{len(pick)} lines")


def reject(sheet_dir: Path, out: Path) -> None:
    marks = {int(k): int(v) for k, v in json.loads((sheet_dir / "marks.json").read_text()).items()}
    key = json.loads((sheet_dir / "key.json").read_text())
    if len(marks) != len(key):
        raise ValueError(f"{len(marks)} marks for {len(key)} lines")
    rejected = sorted(key[i] for i, mark in marks.items() if mark == 0)
    out.write_text(json.dumps(rejected, indent=0), encoding="utf-8")
    print(f"{len(rejected)} rejected")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="step", required=True)
    s = sub.add_parser("sheet")
    s.add_argument("data", type=Path)
    s.add_argument("out_dir", type=Path)
    r = sub.add_parser("reject")
    r.add_argument("sheet_dir", type=Path)
    r.add_argument("out", type=Path)
    args = parser.parse_args()
    if args.step == "sheet":
        sheet(args.data, args.out_dir)
    else:
        reject(args.sheet_dir, args.out)


if __name__ == "__main__":
    main()
