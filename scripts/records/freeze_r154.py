"""R-154: freeze the scorer and the judge with the model, and check the freeze before a sealed run.

Usage:
    python scripts/records/freeze_r154.py write --adapter PATH --out MANIFEST
    python scripts/records/freeze_r154.py check MANIFEST [--adapter PATH]
    python scripts/records/freeze_r154.py rescore RESULTS [RESULTS ...]
    python scripts/records/freeze_r154.py judges TRANSCRIPT [TRANSCRIPT ...]
    python scripts/records/freeze_r154.py spread MARKS_DIR --out PATH

Why: a sealed run scored by a different scorer or judge is not sealed. ``write`` records the
SHA-256 of every file that builds, runs or scores the evaluation, of the sealed pools (hashed,
never printed), of the judge's brief and rubric, of the human scorer check (R-139) and of the
adapter's weights, beside the judge model, the harness version and the decoding. ``check`` stops
the sealed run if any of them changed. ``rescore`` rebuilds a stored run's items on the CPU and
scores its stored replies twice, to show the recall scorer gives the same verdicts each time.
``judges`` fails a judging whose transcript shows any model but the frozen one. ``spread`` measures
how far fresh judges of the frozen model, with the same brief and sheets, differ from each other:
the judge cannot be made deterministic (the agent tool sets no temperature), so its spread is
measured before the sealed run instead.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path

from aya_retrieval.conversations import ITEM_KINDS, build_item
from aya_retrieval.inference import GREEDY
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.provenance import REPO_ROOT, run_metadata
from aya_retrieval.scoring import item_correct

# Everything that builds the items, runs the model on them or scores what it says.
SCORER_FILES = (
    "src/aya_retrieval/conversations.py",
    "src/aya_retrieval/recall_tool.py",
    "src/aya_retrieval/harness.py",
    "src/aya_retrieval/inference.py",
    "src/aya_retrieval/tool_prompt.py",
    "src/aya_retrieval/models.py",
    "src/aya_retrieval/stress.py",
    "src/aya_retrieval/scoring.py",
    "src/aya_retrieval/coherence.py",
    "src/aya_retrieval/stats.py",
    "scripts/run_recall_eval.py",
    "scripts/make_coherence_sheet.py",
    "scripts/make_multi_sheet.py",
    "scripts/run_target_coherence.py",
    "scripts/run_curator_check.py",
    "scripts/records/gate_r086.py",
    "scripts/records/stone_report.py",
)
# The sealed pools; hashed whole, so their content is never shown.
SEALED_FILES = ("src/aya_retrieval/pools.py", "src/aya_retrieval/pool_independent.py")
SEALED_DIR = "docs/independent_pool"
JUDGE_FILES = (
    "results/freeze/R-154/judge_brief_r128_j1.txt",
    "results/coherence/R-128/judge/rubric.txt",
)
HUMAN_CHECK_DIR = "results/human_check/R-139"
# Only the weights and their config: the adapter folder's other files are not the model.
ADAPTER_FILES = ("adapter_config.json", "adapter_model.safetensors")
JUDGE = {
    "model": "claude-sonnet-5-5",
    "harness": "Claude Code",
    "harness_version": "2.1.309",
    "decoding": "the agent tool sets no temperature; the provider's default",
    "rule": "three fresh judges, each in its own folder with only the brief, rubric and sheets; "
    "judge 1 decides; judges 2 and 3 are reported",
    "brief_changes_allowed": "the folder path, sheet names and line counts only",
}
CURATORKIT = {"commit": "dd9e835", "threshold": 0.7}
STYLE_FLAGS = ("user_style", "phone_style", "corrections", "corrections_heldout", "asked_before")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def folder_digest(folder: Path) -> dict:
    """One SHA-256 over every file's relative path and digest, and the file count."""
    files = sorted(p for p in folder.rglob("*") if p.is_file())
    whole = hashlib.sha256()
    for path in files:
        whole.update(f"{path.relative_to(folder).as_posix()} {digest(path)}\n".encode())
    return {"files": len(files), "sha256": whole.hexdigest()}


def fingerprint(adapter: Path) -> dict:
    """Everything the freeze holds fixed, as digests and values."""
    return {
        "scorer": {name: digest(REPO_ROOT / name) for name in SCORER_FILES},
        "sealed": {
            **{name: digest(REPO_ROOT / name) for name in SEALED_FILES},
            SEALED_DIR: folder_digest(REPO_ROOT / SEALED_DIR),
        },
        "judge": {**JUDGE, "files": {name: digest(REPO_ROOT / name) for name in JUDGE_FILES}},
        "curatorkit": CURATORKIT,
        "human_check": folder_digest(REPO_ROOT / HUMAN_CHECK_DIR),
        "model": {
            "base": MODEL_ID,
            "revision": MODEL_REVISION,
            "decoding": GREEDY,
            "adapter": adapter.name,
            "adapter_files": {name: digest(adapter / name) for name in ADAPTER_FILES},
        },
    }


def differences(frozen: dict, now: dict, where: str = "") -> list[str]:
    if isinstance(frozen, dict) and isinstance(now, dict):
        found = []
        for key in sorted(set(frozen) | set(now)):
            found += differences(frozen.get(key), now.get(key), f"{where}/{key}")
        return found
    return [] if frozen == now else [f"{where}: frozen {frozen!r}, now {now!r}"]


def rescore(path: Path) -> dict:
    """Rebuild a stored run's items and score its stored replies twice."""
    report = json.loads(path.read_text(encoding="utf-8"))
    if report["pool"] == "heldout" or report.get("items_dir") or report.get("chat_check"):
        raise SystemExit(f"{path}: only generated development runs can be rescored")
    if any(report.get(flag) for flag in STYLE_FLAGS):
        raise SystemExit(f"{path}: rescoring a run with stress flags is not supported")
    items = {}
    per_kind = 1 + max(int(row["id"].rsplit("_", 1)[1]) for row in report["rows"])
    for kind_number, kind in enumerate(ITEM_KINDS):
        if kind not in report["kinds"]:
            continue
        for size in report["sizes"]:
            for number in range(per_kind):
                seed = report["seed"] + size * 1000 + kind_number * 100 + number
                item_id = f"{size}_{kind}_{number:02d}"
                items[item_id] = build_item(
                    item_id, seed, size, kind, report["pool"], report["decoys"]
                )
    passes = []
    for _ in range(2):
        verdicts = []
        for row in report["rows"]:
            item = items[row["id"]]
            if item.message != row["message"] or item.answer != row["answer"]:
                raise SystemExit(f"{path}: item {row['id']} did not rebuild as stored")
            calls = len(row["queries"])
            correct = item_correct(row["kind"], row["reply"], item.answer, item.forbidden, calls)
            verdicts.append(correct and not row["ran_out_of_calls"])
        passes.append(verdicts)
    stored = [row["correct"] for row in report["rows"]]
    return {
        "file": path.as_posix(),
        "rows": len(stored),
        "same_both_times": passes[0] == passes[1],
        "same_as_stored": passes[0] == stored,
        "correct": sum(passes[0]),
    }


def judge_models(path: Path) -> dict:
    """The models and harness versions a judge transcript's replies came from."""
    models, versions = set(), set()
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = json.loads(line)
        if entry.get("type") == "assistant":
            models.add(entry["message"].get("model"))
            versions.add(entry.get("version"))
    return {"file": path.name, "models": sorted(models), "versions": sorted(versions)}


def spread(folder: Path) -> dict:
    """Per sheet: each judge's count of 1s, pairwise agreement, and lines the judges split on."""
    sheets = {}
    for path in sorted(folder.glob("marks_*_j*.json")):
        sheet, judge = path.stem.removeprefix("marks_").rsplit("_", 1)
        sheets.setdefault(sheet, {})[judge] = json.loads(path.read_text(encoding="utf-8"))
    result = {}
    for sheet, judges in sheets.items():
        lines = sorted(next(iter(judges.values())), key=int)
        result[sheet] = {
            "lines": len(lines),
            "ones": {j: sum(m[k] for k in lines) for j, m in judges.items()},
            "agreement": {
                f"{a}-{b}": sum(judges[a][k] == judges[b][k] for k in lines)
                for a, b in combinations(sorted(judges), 2)
            },
            "split_lines": sum(len({m[k] for m in judges.values()}) > 1 for k in lines),
        }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    write = commands.add_parser("write")
    write.add_argument("--adapter", type=Path, required=True)
    write.add_argument("--out", type=Path, required=True)
    check = commands.add_parser("check")
    check.add_argument("manifest", type=Path)
    check.add_argument("--adapter", type=Path, help="defaults to the adapter the manifest names")
    commands.add_parser("rescore").add_argument("results", type=Path, nargs="+")
    commands.add_parser("judges").add_argument("transcripts", type=Path, nargs="+")
    marks = commands.add_parser("spread")
    marks.add_argument("folder", type=Path)
    marks.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if args.command == "write":
        manifest = {**run_metadata(), "record": "R-154", "adapter_path": args.adapter.as_posix()}
        manifest["frozen"] = fingerprint(args.adapter)
        args.out.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
        print(f"wrote {args.out}")
    elif args.command == "check":
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        adapter = args.adapter or Path(manifest["adapter_path"])
        found = differences(manifest["frozen"], fingerprint(adapter))
        print("\n".join(found) or "every frozen file and value matches")
        sys.exit(1 if found else 0)
    elif args.command == "rescore":
        reports = [rescore(path) for path in args.results]
        print(json.dumps(reports, indent=1))
        sys.exit(0 if all(r["same_both_times"] and r["same_as_stored"] for r in reports) else 1)
    elif args.command == "judges":
        reports = [judge_models(path) for path in args.transcripts]
        print(json.dumps(reports, indent=1))
        sys.exit(0 if all(r["models"] == [JUDGE["model"]] for r in reports) else 1)
    else:
        result = spread(args.folder)
        args.out.write_text(json.dumps(result, indent=1) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
