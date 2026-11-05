"""Make one blind coherence sheet from several runs, so one judge marks every model (R-090).

Two-run sheets put each model before a different judge, and judges differ by a line or two on the
same replies (R-085). Here every model's replies to the same conversations are shuffled together
with the names removed; the key restores them.

Usage:
    python scripts/make_multi_sheet.py --seed 90500 --out-dir results/coherence/R-090/sheet \
        --kinds statement base=results/recall_eval/st_cc_base_seed_73157.json:three_exchanges \
        17b=results/recall_eval/st_cc_fix17b_82_seed_73157.json ...

Each run is ``name=path``, with ``:arm`` to pick an arm other than the scored one.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from aya_retrieval.coherence import NO_TOOL_ARM, SCORED_ARM
from aya_retrieval.conversations import ITEM_KINDS


def multi_sheet_lines(runs: dict[str, list[dict]], rng: random.Random):
    """Return shuffled judging lines from several runs' rows, and the key naming each line's run.

    Raises:
        ValueError: If the runs did not score the same conversations.
    """
    ids = {name: {row["id"] for row in rows} for name, rows in runs.items()}
    if len({frozenset(v) for v in ids.values()}) != 1:
        raise ValueError("the runs did not score the same conversations")
    entries = [(name, row) for name, rows in runs.items() for row in rows]
    rng.shuffle(entries)
    sheet, key = [], []
    for line, (name, row) in enumerate(entries):
        sheet.append(
            {"line": line, "view": row["view"], "message": row["message"], "reply": row["reply"]}
        )
        key.append({"line": line, "model": name, "id": row["id"], "kind": row["kind"]})
    return sheet, key


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("runs", nargs="+", help="name=path[:arm]")
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--kinds", nargs="+", choices=ITEM_KINDS, required=True)
    args = parser.parse_args()

    runs = {}
    for spec in args.runs:
        name, _, rest = spec.partition("=")
        path, _, arm = rest.rpartition(":")
        if arm not in (SCORED_ARM, NO_TOOL_ARM):
            path, arm = rest, SCORED_ARM
        rows = json.loads(Path(path).read_text(encoding="utf-8"))["rows"]
        runs[name] = [r for r in rows if r["arm"] == arm and r["kind"] in args.kinds]
    sheet, key = multi_sheet_lines(runs, random.Random(args.seed))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "sheet.json").write_text(json.dumps(sheet, indent=1), encoding="utf-8")
    (args.out_dir / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    sources = {spec.partition("=")[0]: spec.partition("=")[2] for spec in args.runs}
    (args.out_dir / "runs.json").write_text(json.dumps(sources, indent=1), encoding="utf-8")
    print(f"{len(sheet)} lines from {len(runs)} runs written to {args.out_dir}")


if __name__ == "__main__":
    main()
