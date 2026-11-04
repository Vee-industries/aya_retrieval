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


def train_report(name: str) -> dict:
    """One training run's report from ``results/recall_train``."""
    path = REPO_ROOT / "results" / "recall_train" / f"{name}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def weights_gib() -> float:
    """Size of the pinned model's weights in bf16, counted from its safetensors files."""
    from math import prod

    from huggingface_hub import snapshot_download
    from safetensors import safe_open

    from aya_retrieval.models import MODEL_ID, MODEL_REVISION

    folder = Path(snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True))
    params = 0
    for file in folder.glob("*.safetensors"):
        with safe_open(str(file), "pt") as tensors:
            params += sum(prod(tensors.get_slice(k).get_shape()) for k in tensors.keys())
    return params * 2 / 2**30


def coherence_pooled(record: str, sheets: list[str]) -> dict[str, dict[str, tuple[int, int]]]:
    """Coherent lines per model and kind, added up over several sheets of one record.

    Each name in ``sheets`` has its marks at ``judge/marks_<name>.json`` and its key at
    ``sheet_<name>/key.json`` under ``results/coherence/<record>``.
    """
    folder = COHERENCE_DIR / record
    total: dict[str, dict[str, list[int]]] = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for name in sheets:
        counts = coherence_by_model_and_kind(
            folder / "judge" / f"marks_{name}.json", folder / f"sheet_{name}" / "key.json"
        )
        for model, kinds in counts.items():
            for kind, (hits, lines) in kinds.items():
                total[model][kind][0] += hits
                total[model][kind][1] += lines
    return {model: {k: (c[0], c[1]) for k, c in kinds.items()} for model, kinds in total.items()}


def false_retrieval(
    label: str, probe_seed: int, arm: str = "tool_loop"
) -> dict[str, tuple[int, int]]:
    """Replies per kind that name a wrong value of the asked fact's type: false retrieval.

    A wrong value is a decoy, the same fact about someone else, or for a question never told, any
    value of that type.

    Each item is rebuilt from its seed, with the pool and decoy count its results file records.
    """
    from aya_retrieval.conversations import rebuild_eval_item

    report = json.loads((EVAL_DIR / f"{label}_seed_{probe_seed}.json").read_text(encoding="utf-8"))
    pool, decoys = report["pool"], report.get("decoys", 1)
    counts = {kind: [0, 0] for kind in KINDS}
    for row in eval_rows(label, probe_seed, arm):
        item = rebuild_eval_item(row, probe_seed, pool, decoys)
        text = row["reply"].casefold()
        counts[row["kind"]][0] += any(v.casefold() in text for v in item.forbidden)
        counts[row["kind"]][1] += 1
    return {kind: (c[0], c[1]) for kind, c in counts.items()}


def recall_sources(rows: list[dict]) -> dict[str, int]:
    """Where each answer to a question that needs a search came from.

    ``retrieved``: right, and the exchange holding the fact was in the results of a search the
    model made. ``searched_not_returned``: right, though no search it made returned the fact.
    ``no_search``: right without searching. ``wrong_though_retrieved``: the fact came back and the
    reply still missed it. The middle two are right answers the model could not have read.
    """
    asked = [r for r in rows if r["kind"] in RECALL_KINDS]
    return {
        "questions": len(asked),
        "retrieved": sum(bool(r["correct"] and r["found_fact"]) for r in asked),
        "searched_not_returned": sum(
            bool(r["correct"] and not r["found_fact"] and r["queries"]) for r in asked
        ),
        "no_search": sum(bool(r["correct"] and not r["queries"]) for r in asked),
        "wrong_though_retrieved": sum(bool(not r["correct"] and r["found_fact"]) for r in asked),
    }
