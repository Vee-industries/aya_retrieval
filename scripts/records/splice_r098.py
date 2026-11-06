"""R-098: fix C2, fix A's set with the 15 answers C1 dropped given the scripted answer, as fix17z.

Usage: python scripts/records/splice_r098.py

For each of the 15 found-fact rows R-097 dropped from ``fix17w.jsonl`` (``fix17y``'s provenance
lists them), the answer becomes the pool's scripted "Your {relation} {person} ..." answer. The value
is the one fact value the row's current answer names; the person and relation are the ones in the
search-result chunk that holds that value. A row stops the build unless each is found exactly once.
Every other row is kept byte for byte.
"""

import json
import re
from pathlib import Path

from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.scoring import slip_shape

DATA = Path("data/screens")
BASE_SET, OUT = DATA / "fix17w.jsonl", DATA / "fix17z.jsonl"
DROPPED = DATA / "fix17y.provenance.json"


def friend_message(turns):
    return next(
        t["content"]
        for t in reversed(turns[:-1])
        if t["role"] == "user" and not t["content"].startswith("Tool result")
    )


def tool_result(turns):
    return next(
        t["content"] for t in reversed(turns[:-1]) if t["content"].startswith("Tool result")
    )


def one(found, what, row_id):
    if len(found) != 1:
        raise SystemExit(f"{row_id}: {what} found {len(found)} times: {sorted(found)}")
    return found.pop()


def words(text, choices):
    return {c for c in choices if re.search(rf"\b{re.escape(c)}\b", text)}


def scripted(row):
    turns = row["turns"]
    values = {(f, v) for f, t in TRAIN.facts.items() for v in t.values}
    fact, value = one(
        {(f, v) for f, v in values if v in words(turns[-1]["content"], [v])}, "value", row["id"]
    )
    chunks = re.split(r"\[chunk_id=", tool_result(turns))
    chunk = one({c for c in chunks if words(c, [value])}, "chunk", row["id"])
    person = one(words(chunk, TRAIN.people), "person", row["id"])
    relation = one(words(chunk, TRAIN.relations), "relation", row["id"])
    return TRAIN.facts[fact].answer.format(relation=relation, person=person, value=value)


drop = json.loads(DROPPED.read_text(encoding="utf-8"))["dropped"]
rows = [json.loads(line) for line in BASE_SET.read_text(encoding="utf-8").splitlines() if line]
changed = {}
for row in rows:
    if row["id"] in drop:
        answer = scripted(row)
        changed[row["id"]] = {"before": row["turns"][-1]["content"], "after": answer}
        row["turns"][-1]["content"] = answer
if sorted(changed) != sorted(drop):
    raise SystemExit("a dropped id is not in the set")
left = sum(
    slip_shape(r["turns"][-1]["content"], friend_message(r["turns"]))
    for r in rows
    if r["kind"] in ("older", "confirm")
)
if left:
    raise SystemExit(f"{left} slip-shaped targets in the set")
OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
report = {
    "provenance": run_metadata(),
    "base_set": BASE_SET.as_posix(),
    "rewritten": changed,
    "rows": len(rows),
}
OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
for row_id, c in changed.items():
    print(f"{row_id}: {c['after']}")
print(f"{OUT}: {len(rows)} rows, {len(changed)} rewritten")
