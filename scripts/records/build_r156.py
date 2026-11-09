"""R-156: 7.1's set, 7's set with its 20 reworded `in_view` rows put back as 6.37 had them.

Usage: python scripts/records/build_r156.py

Why: 7 stopped searching on one probe wording that 6.37 searched (R-155, R-156: no search on 10 of
14 such items against 1 of 14). Of 7's 140 reworded rows, only the 20 `in_view` claims teach that a
statement-like message about a person's fact gets no search, and they reply in the register of 7's
misses. This set removes that one part and keeps the 100 `confirm` and 20 `never_told` tag rows, so
the result also shows which part of 7 moved the `older` decision. Nothing is added: every row is
6.37's or 7's, byte for byte. Writes data/screens/fix17cs71.jsonl.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from aya_retrieval.provenance import run_metadata

DATA = Path("data/screens")
SETS = {"6.37": DATA / "fix17cs37.jsonl", "7": DATA / "fix17cs7.jsonl"}
SHAS = {"6.37": ("04df294a", "7b0183de"), "7": ("7cb7a5cb",)}  # checked out, and as git stores it
OUT = DATA / "fix17cs71.jsonl"
CHANGED = {"confirm": 100, "never_told": 20, "in_view": 20}


def lines(name: str) -> list[str]:
    data = SETS[name].read_bytes()
    if not hashlib.sha256(data).hexdigest().startswith(SHAS[name]):
        raise SystemExit(f"{SETS[name]} is not {name}'s set")
    return [line for line in data.decode("utf-8").splitlines() if line]


def main() -> None:
    old, new = lines("6.37"), lines("7")
    if len(old) != len(new):
        raise SystemExit("the two sets differ in length")
    differ = [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b]
    kinds = Counter(json.loads(new[i])["kind"] for i in differ)
    if kinds != Counter(CHANGED):
        raise SystemExit(f"7 differs from 6.37 in {dict(kinds)}, not {CHANGED}")
    reverted = [i for i in differ if json.loads(new[i])["kind"] == "in_view"]
    out = [old[i] if i in reverted else line for i, line in enumerate(new)]
    text = "\n".join(out) + "\n"
    OUT.write_text(text, encoding="utf-8", newline="\n")
    kept = Counter(json.loads(out[i])["kind"] for i in differ if out[i] != old[i])
    provenance = {
        **run_metadata(),
        "record": "R-156",
        "from": {name: str(path) for name, path in SETS.items()},
        "rows": len(out),
        "differ_from_6.37": dict(kept),
        "reverted_to_6.37": len(reverted),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    record = json.dumps(provenance, indent=1)
    OUT.with_suffix(".provenance.json").write_text(record, encoding="utf-8")
    print(f"wrote {OUT}: {len(out)} rows, differ from 6.37 {dict(kept)}, reverted {len(reverted)}")
    print(f"sha256 {provenance['sha256'][:8]}")


if __name__ == "__main__":
    main()
