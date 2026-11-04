"""Vet training targets of one kind with a blind judge, then swap out the ones marked incoherent.

Usage:
    python scripts/vet_statement_targets.py sheet --data data/screens/more_chat.jsonl \
        --spare data/screens/more_chat_spare.jsonl --seed 90451 --out-dir C:/scratch/vet
    python scripts/render_judge_sheet.py C:/scratch/vet/sheet.json C:/scratch/vet/judge/sheet.txt
    (a fresh judge marks sheet.txt against rubric.txt)
    python scripts/vet_statement_targets.py apply --data data/screens/more_chat.jsonl \
        --spare data/screens/more_chat_spare.jsonl --key C:/scratch/vet/key.json \
        --marks C:/scratch/vet/marks.json --out data/screens/vetted_chat.jsonl
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from aya_retrieval.conversations import ITEM_KINDS, STATEMENT
from aya_retrieval.provenance import run_metadata
from aya_retrieval.vetting import replace_rejected, splice_kind, target_sheet


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="step", required=True)
    sheet = sub.add_parser("sheet", help="write the blind sheet and its key")
    sheet.add_argument("--seed", type=int, required=True)
    sheet.add_argument("--out-dir", type=Path, required=True)
    apply = sub.add_parser("apply", help="write the vetted training set")
    apply.add_argument("--key", type=Path, required=True)
    apply.add_argument("--marks", type=Path, required=True)
    apply.add_argument("--out", type=Path, required=True)
    apply.add_argument(
        "--into", type=Path, help="full training set whose rows of the kind the vetted rows replace"
    )
    for step in (sheet, apply):
        step.add_argument("--data", type=Path, required=True, help="training rows to vet")
        step.add_argument("--spare", type=Path, required=True, help="spare rows of the kind")
        step.add_argument("--kind", default=STATEMENT, choices=ITEM_KINDS, help="kind to vet")
    args = parser.parse_args()

    data, spare = read_rows(args.data), read_rows(args.spare)
    if args.step == "sheet":
        lines, key = target_sheet(data, spare, random.Random(args.seed), args.kind)
        args.out_dir.mkdir(parents=True, exist_ok=True)
        (args.out_dir / "sheet.json").write_text(json.dumps(lines, indent=1), encoding="utf-8")
        (args.out_dir / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
        print(f"{len(lines)} lines written to {args.out_dir}")
        return

    key = json.loads(args.key.read_text(encoding="utf-8"))
    marks = {int(k): int(v) for k, v in json.loads(args.marks.read_text()).items()}
    rows, tally = replace_rejected(data, spare, key, marks, args.kind)
    if args.into:
        rows = splice_kind(read_rows(args.into), rows, args.kind)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    lines = (json.dumps(row, ensure_ascii=False) for row in rows)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report = {
        "provenance": run_metadata(),
        "data": args.data.as_posix(),
        "spare": args.spare.as_posix(),
        "into": args.into and args.into.as_posix(),
        "marks": marks,
        "key": key,
        "rows": len(rows),
        "tally": tally,
    }
    args.out.with_suffix(".provenance.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8"
    )
    print(f"wrote {len(rows)} rows to {args.out}: {tally}")


if __name__ == "__main__":
    main()
