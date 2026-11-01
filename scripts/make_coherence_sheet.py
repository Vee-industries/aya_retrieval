"""Make a blind coherence sheet: replies from two runs, shuffled, with the model names removed.

A judge who cannot see which model wrote what marks each line in the sheet. The key stays in a
separate file until the marks are in.

Usage:
    python scripts/make_coherence_sheet.py results/recall_eval/base_seed_1.json \
        results/recall_eval/tuned_seed_1.json --seed 1234 --out-dir C:/scratch/sheet
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from aya_retrieval.coherence import NO_TOOL_ARM, SCORED_ARM, sheet_lines
from aya_retrieval.conversations import ITEM_KINDS


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("results", nargs=2, type=Path, help="base results, then adapter results")
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--base-arm", default=SCORED_ARM, choices=(SCORED_ARM, NO_TOOL_ARM))
    parser.add_argument("--kinds", nargs="+", choices=ITEM_KINDS, help="omit for every kind")
    args = parser.parse_args()

    runs = [json.loads(path.read_text(encoding="utf-8")) for path in args.results]
    sheet, key = sheet_lines(
        runs[0]["rows"],
        runs[1]["rows"],
        random.Random(args.seed),
        args.base_arm,
        tuple(args.kinds) if args.kinds else None,
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "sheet.json").write_text(json.dumps(sheet, indent=1), encoding="utf-8")
    (args.out_dir / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    print(f"{len(sheet)} lines written to {args.out_dir}")


if __name__ == "__main__":
    main()
