"""R-241 (round 3, R3a): K4.6's rows that search twice and then name the value, for a stage on K4.6.

Usage: python scripts/records/build_k4_6tw.py

A row is kept when K4.6's provenance ``meta`` gives it 2 searches and ``names_value`` true; nothing
else changes. The rows are a subset of K4.6's checked set (R-214).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path("data/screens/k4_6_r214.jsonl")
OUT = Path("data/screens/k4_6tw_r241.jsonl")


def main() -> None:
    base = json.loads(BASE.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    meta = base["meta"]
    kept = [
        line
        for line in BASE.read_text(encoding="utf-8").splitlines()
        if (m := meta.get(json.loads(line)["id"]) or {}).get("searches") == 2
        and m.get("names_value")
    ]
    ids = {json.loads(line)["id"] for line in kept}
    text = "".join(line + "\n" for line in kept)
    OUT.write_bytes(text.encode("utf-8"))
    report = {
        "record": "R-241",
        "base_set": BASE.as_posix(),
        "rows": len(kept),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "meta": {i: meta[i] for i in ids},  # R-248: as check_k3.py reads it
        "k4_questions": {i: q for i, q in base.get("k4_questions", {}).items() if i in ids},
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{OUT}: {len(kept)} rows")


if __name__ == "__main__":
    main()
