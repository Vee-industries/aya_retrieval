"""R-094: 17b's set with no slip-shaped fact answer, as fix17w.

Usage: python scripts/records/splice_r094.py

Each found-fact answer the slip check flags (``scoring.slip_shape``: "Hana's barber ...",
"My barber, Hana, ...", "who is my") has its subject rewritten to "Your <relation> <name>", the
person named in the fact the search returned, and the rest of the answer kept. The rewrite is kept
only if the slip check then passes and the person is named; otherwise the row stops the build, so
no slip-shaped target is left and nothing is written in by hand.
"""

import json
import re
from pathlib import Path

from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.scoring import slip_shape

DATA = Path("data/screens")
BASE_SET, OUT = DATA / "strict_chat.jsonl", DATA / "fix17w.jsonl"
PEOPLE = "|".join(sorted(TRAIN.people, key=len, reverse=True))


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


def person_for(relation, result):
    """The train person the returned fact names with the relation, or None."""
    for line in result.splitlines():
        if not line.startswith("User:") or not re.search(rf"\b{relation}\b", line):
            continue
        names = set(re.findall(rf"\b({PEOPLE})\b", line))
        if len(names) == 1:
            return names.pop()
    return None


def rewritten(answer, relation, person):
    """The answer with its subject in the "Your <relation> <person>" shape."""
    subject = rf"(?:\b[A-Z][a-z]+'s {relation}|\bMy {relation})(?:,? (?:{person})\b,?)?"
    text = re.sub(rf"(?<=[.!?] ){subject}|^{subject}", f"Your {relation} {person}", answer)
    text = re.sub(subject, f"your {relation} {person}", text)
    return re.sub(r"\bwho is my\b", "who is your", text, flags=re.IGNORECASE)


rows = [json.loads(line) for line in BASE_SET.read_text(encoding="utf-8").splitlines() if line]
changed, out = [], []
for row in rows:
    turns = row["turns"]
    answer, message = turns[-1]["content"], friend_message(turns)
    if row["kind"] in ("older", "confirm") and slip_shape(answer, message):
        relation = re.findall(r"\bmy ([a-z]+)", message.casefold())[0]
        person = person_for(relation, tool_result(turns))
        if person is None:
            raise SystemExit(f"{row['id']}: no single person for {relation!r} in the result")
        fixed = rewritten(answer, relation, person)
        if slip_shape(fixed, message) or person not in fixed:
            raise SystemExit(f"{row['id']}: rewrite failed: {fixed!r}")
        turns = [*turns[:-1], {**turns[-1], "content": fixed}]
        changed.append({"id": row["id"], "from": answer, "to": fixed})
    out.append({**row, "turns": turns})

left = sum(
    slip_shape(r["turns"][-1]["content"], friend_message(r["turns"]))
    for r in out
    if r["kind"] in ("older", "confirm")
)
if left or len(out) != len(rows):
    raise SystemExit(f"{left} slip-shaped targets left; {len(out)} rows of {len(rows)}")
OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out) + "\n", encoding="utf-8")
report = {"provenance": run_metadata(), "base_set": BASE_SET.as_posix(), "rewritten": changed}
report["rows"] = len(out)
OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print(f"{OUT}: {len(out)} rows, {len(changed)} answers rewritten, 0 slip-shaped left")
