"""R-229: K4.8's set without K1.3's 1,094 rows, for the stage tries on natural rows only.

Usage: python scripts/records/build_k4_8n.py

A row is dropped when its id is a K1.3 row's id; nothing else changes. The set is a subset of
K4.8's checked set (R-220).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path("data/screens/k4_8_r220.jsonl")
TEMPLATES = Path("data/screens/k1_3_r200.jsonl")
OUT = Path("data/screens/k4_8n_r229.jsonl")


def main() -> None:
    drop = {json.loads(line)["id"] for line in TEMPLATES.read_text(encoding="utf-8").splitlines()}
    lines = BASE.read_text(encoding="utf-8").splitlines()
    kept = [line for line in lines if json.loads(line)["id"] not in drop]
    text = "".join(line + "\n" for line in kept)
    OUT.write_bytes(text.encode("utf-8"))
    report = {
        "record": "R-229",
        "base_set": BASE.as_posix(),
        "dropped_template_rows": len(lines) - len(kept),
        "rows": len(kept),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{OUT}: {len(kept)} rows ({report['dropped_template_rows']} template rows dropped)")


if __name__ == "__main__":
    main()
