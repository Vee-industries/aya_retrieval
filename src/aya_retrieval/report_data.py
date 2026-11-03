"""Numbers for the write-up and its figures, read from committed results files.

Every number in the write-up comes from these functions, so none is typed by hand.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from aya_retrieval.provenance import REPO_ROOT

EVAL_DIR = REPO_ROOT / "results" / "recall_eval"
COHERENCE_DIR = REPO_ROOT / "results" / "coherence"
KINDS = ("older", "confirm", "in_view", "never_told", "statement")
RECALL_KINDS = ("older", "confirm")
SIZES = (58, 419)


def eval_rows(label: str, probe_seed: int, arm: str = "tool_loop") -> list[dict]:
    """Return one results file's rows for one arm; files from before arms existed are tool loop."""
    path = EVAL_DIR / f"{label}_seed_{probe_seed}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))["rows"]
    return [r for r in rows if r.get("arm", "tool_loop") == arm]


def share(rows: list[dict], field: str = "correct") -> tuple[int, int]:
    """Return (rows where ``field`` is true, rows)."""
    return sum(bool(r[field]) for r in rows), len(rows)


def recall(rows: list[dict], size: int | None = None) -> tuple[int, int]:
    """Correct answers on the kinds that need a search, at one chat length or both."""
    return share([r for r in rows if r["kind"] in RECALL_KINDS and size in (None, r["size"])])


def by_kind(rows: list[dict]) -> dict[str, tuple[int, int]]:
    """Correct answers per kind."""
    return {kind: share([r for r in rows if r["kind"] == kind]) for kind in KINDS}


def pooled(parts: list[tuple[int, int]]) -> tuple[int, int]:
    """Add up (hits, total) pairs."""
    return sum(p[0] for p in parts), sum(p[1] for p in parts)


def percent_above(new: tuple[int, int], base: tuple[int, int]) -> float:
    """Relative increase of new's rate over base's rate, in percent."""
    return (new[0] / new[1]) / (base[0] / base[1]) * 100 - 100


def coherence_by_model_and_kind(
    marks_path: Path, key_path: Path
) -> dict[str, dict[str, tuple[int, int]]]:
    """Coherent lines per model ("base", "tuned") and kind on one blind sheet."""
    marks = {int(k): int(v) for k, v in json.loads(marks_path.read_text()).items()}
    key = json.loads(key_path.read_text())
    counts: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for entry in key:
        tally = counts[entry["model"]][entry["kind"]]
        tally[0] += marks[entry["line"]]
        tally[1] += 1
    return {
        model: {kind: (c[0], c[1]) for kind, c in kinds.items()} for model, kinds in counts.items()
    }
