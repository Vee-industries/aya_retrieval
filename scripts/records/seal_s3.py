"""R-178: seal S3, and check the seal before the one run that opens it.

Usage:
    python scripts/records/seal_s3.py write --judge-brief PATH [PATH ...] [--out MANIFEST]
    python scripts/records/seal_s3.py check [MANIFEST]

``write`` records the SHA-256 of every S3 chat file (by name), the set's load hash, the writer
brief, the category list and split, the loader, the eval script and every file it runs or scores
with (``scoring.py`` among them), the judge briefs named on the command line, and the fixed values:
the never-told rubric, the coherence sample's seed and size, and the judge sheets' shuffle seed.
``check`` recomputes all of it and exits non-zero on any difference. Both print file names, counts
and digests only, never chat text.

Training code that another stage edits (conversations.py, stress.py) is left out on purpose: S3
items do not pass through it, and ``heldout3.load_s3`` stops if the one value it takes from
conversations.py (the three exchanges in view) changes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

from aya_retrieval.heldout3 import (
    CHATS_DIR,
    NEVER_TOLD_RUBRIC,
    SAMPLE_SEED,
    SAMPLE_SIZE,
    SHUFFLE_SEED,
    VIEW,
)
from aya_retrieval.provenance import REPO_ROOT, run_metadata

MANIFEST = REPO_ROOT / "results" / "freeze" / "heldout3_manifest.json"
SEALED_FILES = (
    "docs/heldout3/BRIEF.md",
    "docs/heldout3/categories.md",
    "docs/heldout3/category_split.json",
    "src/aya_retrieval/heldout3.py",
    "src/aya_retrieval/dev_set.py",
    "src/aya_retrieval/scoring.py",
    "src/aya_retrieval/harness.py",
    "src/aya_retrieval/recall_tool.py",
    "src/aya_retrieval/inference.py",
    "src/aya_retrieval/models.py",
    "src/aya_retrieval/tool_prompt.py",
    "scripts/run_s3_eval.py",
    "scripts/run_recall_eval.py",
    "scripts/records/seal_s3.py",
    "scripts/records/check_s3.py",
    "scripts/records/draw_s3_sample.py",
)


def digest(path: Path) -> str:
    """SHA-256 of a text file with LF line endings, as git stores it, so a clone matches."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def set_hash(folder: Path) -> str:
    """The set's load hash, the same computation as ``heldout3.load_s3``'s."""
    whole = hashlib.sha256()
    for path in sorted(folder.glob("*.json")):
        whole.update(path.name.encode("utf-8") + b"\0" + path.read_bytes())
    return whole.hexdigest()


def _relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _resolve(name: str) -> Path:
    path = Path(name)
    return path if path.is_absolute() else REPO_ROOT / path


def fingerprint(items_dir: Path, judge_briefs: list[str], root: Path = REPO_ROOT) -> dict:
    """Everything the seal holds fixed, as digests and values."""
    chats = sorted(items_dir.glob("*.json"))
    if not chats:
        raise SystemExit(f"{items_dir}: no chat files to seal")
    return {
        "chats": {
            "folder": _relative(items_dir),
            "files": {path.name: digest(path) for path in chats},
            "count": len(chats),
            "load_sha256": set_hash(items_dir),
        },
        "code_and_docs": {name: digest(root / name) for name in SEALED_FILES},
        "judge_briefs": {name: digest(_resolve(name)) for name in judge_briefs},
        "values": {
            "never_told_rubric": NEVER_TOLD_RUBRIC,
            "coherence_sample_seed": SAMPLE_SEED,
            "coherence_sample_size": SAMPLE_SIZE,
            "judge_shuffle_seed": SHUFFLE_SEED,
            "exchanges_in_view": VIEW,
        },
    }


def differences(frozen, now, where: str = "") -> list[str]:
    """Every path at which ``now`` differs from ``frozen``."""
    if isinstance(frozen, dict) and isinstance(now, dict):
        found = []
        for key in sorted(set(frozen) | set(now)):
            found += differences(frozen.get(key), now.get(key), f"{where}/{key}")
        return found
    return [] if frozen == now else [f"{where}: sealed {frozen!r}, now {now!r}"]


def write(out: Path, items_dir: Path, judge_briefs: list[str]) -> dict:
    """Write the manifest and return it."""
    manifest = {
        **run_metadata(),
        "record": "R-178",
        "judge_brief_paths": judge_briefs,
        "sealed": fingerprint(items_dir, judge_briefs),
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8")
    return manifest


def check(manifest_path: Path, items_dir: Path | None = None) -> list[str]:
    """Return every difference between the manifest and the files as they are now."""
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    sealed = manifest["sealed"]
    folder = items_dir or _resolve(sealed["chats"]["folder"])
    if _relative(folder) != sealed["chats"]["folder"]:
        return [f"/chats/folder: sealed {sealed['chats']['folder']!r}, now {_relative(folder)!r}"]
    return differences(sealed, fingerprint(folder, manifest["judge_brief_paths"]))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    make = commands.add_parser("write")
    make.add_argument("--judge-brief", nargs="+", required=True, help="repo-relative paths")
    make.add_argument("--items-dir", type=Path, default=CHATS_DIR)
    make.add_argument("--out", type=Path, default=MANIFEST)
    test = commands.add_parser("check")
    test.add_argument("manifest", type=Path, nargs="?", default=MANIFEST)
    args = parser.parse_args()
    if args.command == "write":
        manifest = write(args.out, args.items_dir, args.judge_brief)
        sealed = manifest["sealed"]
        print(
            f"sealed {sealed['chats']['count']} chat files, {len(sealed['code_and_docs'])} code "
            f"and doc files, {len(sealed['judge_briefs'])} judge briefs; wrote {args.out}"
        )
    else:
        found = check(args.manifest)
        print("\n".join(found) or "every sealed file and value matches")
        sys.exit(1 if found else 0)


if __name__ == "__main__":
    main()
