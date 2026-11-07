"""R-105: 6.11's set, 6.1's rows with fix C2's 41 rewritten answers swapped in, as fix17cr11.

Usage: python scripts/records/build_r105.py

6.1's set (fix17cr) is v6's 800 rows followed by 170 rows (R-102). Fix C2's set (fix17z) is v6's
800 rows with 41 older rows' final answers rewritten (R-098). This takes 6.1's set and, for each row
where fix17z differs from v6's, takes fix17z's row. The build stops unless every swapped row keeps
its id, kind and every turn but the last, and every other row is 6.1's byte for byte.
"""

import json
from pathlib import Path

from aya_retrieval.provenance import run_metadata

DATA = Path("data/screens")
V6, C2, STONE = DATA / "strict_chat.jsonl", DATA / "fix17z.jsonl", DATA / "fix17cr.jsonl"
OUT = DATA / "fix17cr11.jsonl"


def lines(path):
    return path.read_text(encoding="utf-8").splitlines()


v6, c2, stone = lines(V6), lines(C2), lines(STONE)
if len(v6) != len(c2) or stone[: len(v6)] != v6:
    raise SystemExit("6.1's set does not start with v6's rows, or fix17z is not v6's length")
out, swapped = list(stone), []
for i, (old, new) in enumerate(zip(v6, c2, strict=True)):
    if old == new:
        continue
    a, b = json.loads(old), json.loads(new)
    if (a["id"], a["kind"], a["turns"][:-1]) != (b["id"], b["kind"], b["turns"][:-1]):
        raise SystemExit(f"row {i + 1} ({a['id']}) changes more than its final answer")
    out[i] = new
    swapped.append(a["id"])
OUT.write_text("".join(line + "\n" for line in out), encoding="utf-8")
report = {
    "provenance": run_metadata(),
    "base_set": STONE.as_posix(),
    "answers_from": C2.as_posix(),
    "rows": len(out),
    "swapped": swapped,
}
OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print(f"{OUT}: {len(out)} rows, {len(swapped)} final answers from {C2}")
