"""R-097: fix C1, fix A's set without the answers CuratorKIT's grounding gate rejected, as fix17y.

Usage: python scripts/records/splice_r097.py

Drops, from ``fix17w.jsonl``, every found-fact row whose answer at least two of R-096's three
judges' gate runs rejected and that fix A did not rewrite (14), and the one fix A rewrite the gate
rejected.
Nothing new is written; every other row is kept byte for byte.
"""

import json
from pathlib import Path

from aya_retrieval.provenance import run_metadata
from aya_retrieval.scoring import slip_shape

DATA = Path("data/screens")
BASE_SET, OUT = DATA / "fix17w.jsonl", DATA / "fix17y.jsonl"
REJECTED = Path("results/curator/R-096/rejected.json")


def friend_message(turns):
    return next(
        t["content"]
        for t in reversed(turns[:-1])
        if t["role"] == "user" and not t["content"].startswith("Tool result")
    )


rejected = json.loads(REJECTED.read_text(encoding="utf-8"))
majority = [r for r in rejected if r["judges_rejecting"] >= 2]
drop = sorted(
    {
        r["id"].split(":", 1)[1]
        for r in majority
        if r["id"].startswith("fix17w:") or (r["id"].startswith("v6:") and not r["slip_shape"])
    }
)
rows = [json.loads(line) for line in BASE_SET.read_text(encoding="utf-8").splitlines() if line]
kept = [r for r in rows if r["id"] not in drop]
if len(rows) - len(kept) != len(drop):
    raise SystemExit("a dropped id is not in the set")
left = sum(
    slip_shape(r["turns"][-1]["content"], friend_message(r["turns"]))
    for r in kept
    if r["kind"] in ("older", "confirm")
)
if left:
    raise SystemExit(f"{left} slip-shaped targets in the set")
OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in kept) + "\n", encoding="utf-8")
report = {
    "provenance": run_metadata(),
    "base_set": BASE_SET.as_posix(),
    "dropped": drop,
    "rows": len(kept),
}
OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print(f"{OUT}: {len(kept)} rows, {len(drop)} dropped: {drop}")
