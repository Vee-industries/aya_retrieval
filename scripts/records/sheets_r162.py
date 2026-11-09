"""R-162: the sealed run's blind coherence sheets, every model's reply to a conversation together.

Usage:
    python scripts/records/sheets_r162.py CONDITION --out-dir results/coherence/R-162 \
        --judge-dirs DIR1 DIR2 DIR3

Why: R-016's hard coherence gate needs each adapter's coherent count at or above base's on the same
conversations, judged blind. R-162 fixed the sheets before any run: in condition A every one of the
300 conversations, one sheet per kind; in B, C and D a sample of 120 (for each kind and size,
``random.Random(39).sample`` of 12 from the sorted item ids), in two sheets. Each sheet holds base's
and all eight adapters' replies to the same conversations, shuffled with the names removed
(``make_multi_sheet.multi_sheet_lines``), so one judge marks every model on a conversation. Shuffle
seeds run from 90560 in the order of ``PARTS``. Writes each part's ``sheet.json``, ``key.json`` and
``runs.json`` under ``--out-dir``, and the text sheet and rubric each judge reads into every judge
folder.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
from pathlib import Path

from aya_retrieval.coherence import RUBRIC, SCORED_ARM

EVAL = Path("results/recall_eval")
SEED = 90311
MODELS = ("base",) + tuple(f"fix17cs37_{s}" for s in (82, 83, 94, 95, 96, 97, 98, 99))
SIZES = (58, 419)
SAMPLE_SEED, SAMPLE_PER_CELL = 39, 12
FIRST_SHUFFLE_SEED = 90560
PARTS = {
    "A": [("older",), ("confirm",), ("in_view",), ("never_told",), ("statement",)],
    "B": [("older", "confirm", "in_view"), ("never_told", "statement")],
    "C": [("older", "confirm", "in_view"), ("never_told", "statement")],
    "D": [("older", "confirm", "in_view"), ("never_told", "statement")],
}


def load_script(name: str):
    path = Path("scripts") / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rows_of(condition: str, model: str) -> list[dict]:
    path = EVAL / f"final_{condition}_{model}_seed_{SEED}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))["rows"]
    return [row for row in rows if row["arm"] == SCORED_ARM]


def sample_ids(rows: list[dict]) -> set[str]:
    """R-039's fixed coherence sample: 12 conversations per kind and size, by seed 39."""
    chosen = set()
    for kind in sorted({row["kind"] for row in rows}):
        for size in SIZES:
            ids = sorted(row["id"] for row in rows if row["kind"] == kind and row["size"] == size)
            chosen |= set(random.Random(SAMPLE_SEED).sample(ids, SAMPLE_PER_CELL))
    return chosen


def shuffle_seed(condition: str, part: int) -> int:
    earlier = sum(len(PARTS[c]) for c in PARTS if c < condition)
    return FIRST_SHUFFLE_SEED + earlier + part


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("condition", choices=sorted(PARTS))
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--judge-dirs", type=Path, nargs="+", required=True)
    args = parser.parse_args()
    multi_sheet_lines = load_script("make_multi_sheet").multi_sheet_lines
    render = load_script("render_judge_sheet").render

    runs = {model: rows_of(args.condition, model) for model in MODELS}
    keep = sample_ids(runs["base"]) if args.condition != "A" else {r["id"] for r in runs["base"]}
    for number, kinds in enumerate(PARTS[args.condition]):
        name = f"{args.condition}{number + 1}"
        part = {
            m: [r for r in rows if r["kind"] in kinds and r["id"] in keep]
            for m, rows in runs.items()
        }
        sheet, key = multi_sheet_lines(part, random.Random(shuffle_seed(args.condition, number)))
        folder = args.out_dir / f"sheet_{name}"
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "sheet.json").write_text(json.dumps(sheet, indent=1), encoding="utf-8")
        (folder / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
        sources = {m: str(EVAL / f"final_{args.condition}_{m}_seed_{SEED}.json") for m in MODELS}
        (folder / "runs.json").write_text(json.dumps(sources, indent=1), encoding="utf-8")
        for judge in args.judge_dirs:
            judge.mkdir(parents=True, exist_ok=True)
            (judge / f"sheet_{name}.txt").write_text(render(sheet), encoding="utf-8")
            (judge / "rubric.txt").write_text(RUBRIC, encoding="utf-8")
        conversations = len({line["id"] for line in key})
        print(f"sheet_{name}: {len(sheet)} lines, {conversations} conversations, kinds {kinds}")


if __name__ == "__main__":
    main()
