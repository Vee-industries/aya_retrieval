"""R-086: add the indirect older rows to fix 18a's and 18c's sets, as 19a and 19b.

Usage: python scripts/records/splice_r086.py

Each set gets every row of ``data/screens/indirect_older.jsonl``, so 19a and 19b differ only in the
chat lines 18a and 18c added.
"""

import json
from pathlib import Path

from aya_retrieval.provenance import run_metadata

DATA = Path("data/screens")
ADDED = DATA / "indirect_older.jsonl"
SETS = {"fix18a": DATA / "fix19a.jsonl", "fix18c": DATA / "fix19b.jsonl"}


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


added = [{**row, "id": f"indirect/{row['id']}"} for row in read_rows(ADDED)]
for name, out in SETS.items():
    base_rows = read_rows(DATA / f"{name}.jsonl")
    lines = (json.dumps(row, ensure_ascii=False) for row in base_rows + added)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report = {
        "provenance": run_metadata(),
        "base_set": (DATA / f"{name}.jsonl").as_posix(),
        "added_from": ADDED.as_posix(),
        "added": len(added),
        "rows": len(base_rows) + len(added),
    }
    out.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{out}: {len(base_rows)} + {len(added)} rows")
