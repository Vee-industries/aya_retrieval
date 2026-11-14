"""R-237: K4.8's natural rows plus K1.3's 160 never_told rows, for a stage keeping its declines.

Usage: python scripts/records/build_k4_8nt.py

T4 (R-236), a stage on K4.8's natural rows only, passed Demo2 and Demo3 and failed hard_dev
(never_told 38, false retrieval 12); it had dropped K1.3's template rows, among them every
never_told row K1.3 trained on. This set is ``k4_8n_r229`` with K1.3's ``never_told`` rows added
back, unchanged; nothing else.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

NATURAL = Path("data/screens/k4_8n_r229.jsonl")
TEMPLATES = Path("data/screens/k1_3_r200.jsonl")
OUT = Path("data/screens/k4_8nt_r237.jsonl")


def main() -> None:
    natural = NATURAL.read_text(encoding="utf-8").splitlines()
    declines = [
        line
        for line in TEMPLATES.read_text(encoding="utf-8").splitlines()
        if json.loads(line)["kind"] == "never_told"
    ]
    text = "".join(line + "\n" for line in natural + declines)
    OUT.write_bytes(text.encode("utf-8"))
    report = {
        "record": "R-237",
        "natural_rows": len(natural),
        "k1_3_never_told_rows": len(declines),
        "rows": len(natural) + len(declines),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{OUT}: {report['rows']} rows ({len(natural)} natural, {len(declines)} K1.3 never_told)")


if __name__ == "__main__":
    main()
