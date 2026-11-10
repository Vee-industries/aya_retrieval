"""R-170, amended: write each arm's out-of-memory failures, the questions its one rerun runs.

Usage:
    python -I scripts/records/rerun_ids_r170.py

Why: R-170's amendment reruns, once and at a 0.90 cap, every question an arm failed with
``OutOfMemoryError`` at 0.85, and says the ids are written by code from the run files before any
score is computed. This reads only each row's id and error, never a reply. Writes
results/analysis/R-170/rerun_ids/<label>.json, each an ``ids`` list for ``run_longmemeval.py
--ids-file``, and stops if an arm failed for any other reason.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from score_r170 import ARMS, OUT, RESULTS  # noqa: E402

OUT_OF_MEMORY = "OutOfMemoryError"


def main() -> None:
    folder = OUT / "rerun_ids"
    folder.mkdir(parents=True, exist_ok=True)
    for label, arm in ARMS.values():
        path = RESULTS / f"{label}.json"
        report = json.loads(path.read_text(encoding="utf-8"))
        if not report["completed"] or report["ids_file"]:
            raise SystemExit(f"{path} is not a completed full run")
        failed = [row for row in report["rows"] if row.get("error")]
        other = [row["id"] for row in failed if not row["error"].startswith(OUT_OF_MEMORY)]
        if other:
            raise SystemExit(f"{label}: failures other than out of memory: {other}")
        ids = [row["id"] for row in failed]
        written = {
            "record": "R-170",
            "arm": arm,
            "source": path.relative_to(RESULTS.parents[1]).as_posix(),
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "ids": ids,
        }
        (folder / f"{label}.json").write_text(json.dumps(written, indent=1), encoding="utf-8")
        print(f"{label}: {len(ids)} to rerun")


if __name__ == "__main__":
    main()
