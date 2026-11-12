"""First stage of S3's seal: chats, brief, loader, scorer and judge brief, before any training row.

R-178 requires these sealed before training rows exist. The eval runner
(`scripts/run_recall_eval.py`) was still being given new options for the dev stresses at that
moment, so it is sealed in the second
stage (`scripts/records/seal_s3.py write`), before the one run that opens S3. This writes
``results/freeze/heldout3_stage1.json``; `check` stops on any difference.

Usage:
    python scripts/records/seal_s3_stage1.py write
    python scripts/records/seal_s3_stage1.py check
"""

from __future__ import annotations

import json
import sys

from seal_s3 import digest

from aya_retrieval.heldout3 import SAMPLE_SEED, SAMPLE_SIZE, SHUFFLE_SEED
from aya_retrieval.provenance import REPO_ROOT, run_metadata

OUT = REPO_ROOT / "results" / "freeze" / "heldout3_stage1.json"
CHATS = REPO_ROOT / "data" / "heldout3" / "chats"
FILES = (
    "docs/heldout3/BRIEF.md",
    "docs/heldout3/categories.md",
    "docs/heldout3/category_split.json",
    "src/aya_retrieval/heldout3.py",
    "src/aya_retrieval/scoring.py",
    "results/panels/R-178/judge_brief_s3.md",
)


def manifest() -> dict:
    return {
        "chats": {p.name: digest(p) for p in sorted(CHATS.glob("*.json"))},
        "files": {name: digest(REPO_ROOT / name) for name in FILES},
        "seeds": {"sample": SAMPLE_SEED, "sample_size": SAMPLE_SIZE, "shuffle": SHUFFLE_SEED},
    }


def main() -> None:
    if sys.argv[1:] == ["write"]:
        OUT.write_text(
            json.dumps({"provenance": run_metadata(), "record": "R-178", **manifest()}, indent=1)
            + "\n",
            encoding="utf-8",
        )
        print(f"wrote {OUT.relative_to(REPO_ROOT)}")
    elif sys.argv[1:] == ["check"]:
        sealed = json.loads(OUT.read_text(encoding="utf-8"))
        now = manifest()
        bad = [k for k in ("chats", "files", "seeds") if sealed[k] != now[k]]
        if bad:
            raise SystemExit(f"S3 stage 1 seal broken: {bad}")
        print(f"S3 stage 1 seal holds: {len(now['chats'])} chats, {len(now['files'])} files")
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
