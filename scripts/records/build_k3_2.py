"""K3.2's training set (R-207): K3.1's set with check_true rows cut until check_false is 15%.

Usage: python scripts/records/build_k3_2.py

K3.1 (``build_k3_1.py``) failed R-205's line 6: check_false was 14.4% of its natural rows, under
15%, after its drops and the balance. K3.2 takes K3.1's set as built and cuts check_true rows, in
a hashed order, until check_false rows are at least 15% of natural rows. Nothing else changes.
``scripts/records/check_k3.py --set k3_2_r207`` then checks the set.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from aya_retrieval.provenance import run_metadata

BASE = Path("data/screens/k3_1_r206.jsonl")
OUT = Path("data/screens/k3_2_r207.jsonl")
SALT = "R-207"
SHARE = 0.15
AT_LEAST_TRUE = False  # R-235: also cut until check_false rows are at least check_true rows


def main() -> None:
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    meta = json.loads(BASE.with_suffix(".provenance.json").read_text(encoding="utf-8"))["meta"]
    natural = [r for r in rows if r["id"] in meta]
    false = sum((meta[r["id"]] or {}).get("kind") == "check_false" for r in natural)
    true_rows = sorted(
        (r["id"] for r in natural if (meta[r["id"]] or {}).get("kind") == "check_true"),
        key=lambda i: hashlib.sha256(f"{SALT}|{i}".encode()).digest(),
    )
    cut = set()
    while false / (len(natural) - len(cut)) < SHARE or (
        AT_LEAST_TRUE and false < len(true_rows) - len(cut)
    ):
        cut.add(true_rows[len(cut)])
    out = [r for r in rows if r["id"] not in cut]
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_bytes(text.encode("utf-8"))
    report = {
        "provenance": provenance,
        "record": "R-207",
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "check_true_cut": sorted(cut),
        "natural_rows": len(natural) - len(cut),
        "meta": {i: m for i, m in meta.items() if i not in cut},
    }
    OUT.with_suffix(".provenance.json").write_bytes(json.dumps(report, indent=1).encode("utf-8"))
    print(
        f"{OUT}: {len(out)} rows, {len(cut)} check_true rows cut, {report['natural_rows']} natural"
    )


if __name__ == "__main__":
    main()
