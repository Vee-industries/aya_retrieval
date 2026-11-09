"""R-147: 6.39's set, 6.37's 1,094 rows and R-110's 100 rows, for training from scratch.

Usage: python scripts/records/build_r147.py

Why: 6.37's commonest hard_dev miss finds the right line and answers from its first clause,
leaving out the asked detail when it sits later in a long line (R-144, R-146). R-110 built 100
train-pool rows for exactly that shape (a found line that says more than the asked detail: a
second fact about the same person, or small talk joined before, around or after the fact), vetted
then, and added them as one extra epoch on top of an older model (6.21); that copy lost recall
(R-113), and R-115's control split the loss between the extra epoch and the rows. Kevin ruled
after R-116 that no copy trains on top of an earlier one. Trained from scratch inside 6.37's set,
the rows have not been tried. Both sets are kept byte for byte: 6.37's rows in order, then
R-110's, nothing rewritten. Writes data/screens/fix17cs39.jsonl and its provenance file.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from aya_retrieval.provenance import run_metadata

DATA = Path("data/screens")
BASE_SET = DATA / "fix17cs37.jsonl"
BASE_SHA = ("04df294a", "7b0183de")  # 6.37's set as checked out with CRLF, and as git stores it
R110_SET = DATA / "fix17cs21.jsonl"
OUT = DATA / "fix17cs39.jsonl"


def lines(path: Path) -> list[str]:
    # Endings dropped: the working copy may be CRLF; the set is written with "\n", as git stores it.
    return [line for line in path.read_bytes().decode("utf-8").splitlines() if line]


def main() -> None:
    if not hashlib.sha256(BASE_SET.read_bytes()).hexdigest().startswith(BASE_SHA):
        raise SystemExit(f"{BASE_SET} is not 6.37's set")
    base = lines(BASE_SET)
    added = [line for line in lines(R110_SET) if json.loads(line)["id"].startswith("r110_")]
    ids = [json.loads(line)["id"] for line in base + added]
    if len(added) != 100 or len(set(ids)) != len(ids):
        raise SystemExit("expected R-110's 100 rows and no repeated id")
    text = "\n".join(base + added) + "\n"
    OUT.write_text(text, encoding="utf-8", newline="\n")
    kinds = Counter(json.loads(line)["kind"] for line in base + added)
    provenance = {
        **run_metadata(),
        "record": "R-147",
        "from": {str(BASE_SET): len(base), f"{R110_SET} (r110_ rows)": len(added)},
        "rows": len(ids),
        "kinds": dict(sorted(kinds.items())),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    record = json.dumps(provenance, indent=1)
    OUT.with_suffix(".provenance.json").write_text(record, encoding="utf-8")
    print(f"wrote {OUT}: {len(ids)} rows, sha256 {provenance['sha256'][:8]}")


if __name__ == "__main__":
    main()
