"""R-247: K5's set with non-user fact rows cut, in a hashed order, until user facts are a third.

Usage: python scripts/records/build_k5f.py

K5's set (``k5_r226``), R2c's stage data, failed one R-205 line when first checked (R-247): facts
about the user were 32.9% of its natural fact rows, under a third. This cuts natural ``older`` and
``check_true`` rows about someone else (never ``check_false``, which has its own lines), in the
order of SHA-256("R-247|id"), until the user's share reaches a third, as K3.2 cuts for its line
(R-207). Nothing else changes. ``scripts/records/check_k3.py --set k5f_r247`` then checks it.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

BASE = Path("data/screens/k5_r226.jsonl")
OUT = Path("data/screens/k5f_r247.jsonl")
SALT = "R-247"
FACT_KINDS = ("older", "check_true", "check_false")


def main() -> None:
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    report = json.loads(BASE.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    meta = report["meta"]
    facts = [i for i, m in meta.items() if m and m.get("kind") in FACT_KINDS]
    user = sum(meta[i]["person"] == "me" for i in facts)
    others = sorted(
        (i for i in facts if meta[i]["person"] != "me" and meta[i]["kind"] != "check_false"),
        key=lambda i: hashlib.sha256(f"{SALT}|{i}".encode()).digest(),
    )
    cut = set()
    while 3 * user < len(facts) - len(cut):
        cut.add(others[len(cut)])
    out = [r for r in rows if r["id"] not in cut]
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_bytes(text.encode("utf-8"))
    report |= {
        "record": "R-247",
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "cut_for_user_share": sorted(cut),
        "meta": {i: m for i, m in meta.items() if i not in cut},
    }
    OUT.with_suffix(".provenance.json").write_bytes(json.dumps(report, indent=1).encode("utf-8"))
    print(f"{OUT}: {len(out)} rows, {len(cut)} cut; user facts {user} of {len(facts) - len(cut)}")


if __name__ == "__main__":
    main()
