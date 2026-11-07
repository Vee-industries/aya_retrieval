"""R-114: 6.3's set, 6.2's rows plus fix 19a's plain-statement and indirect-question pair.

Usage: python scripts/records/build_r114.py [--vet results/vet/R-114/items.txt]

6.2 failed one judged line at a fresh seed (R-112): told a plain statement about a person, it
searched and answered with an unrelated stored fact. Fix 19a's two row groups, built from that
failure kind on November 5 from the train pool (R-083, R-086), are added to 6.2's 970 rows:

- the 57 ``facts/statement_`` rows of ``fix18a.jsonl``: a chat line that names a fact type in
  passing, answered without a search; kept byte for byte;
- the 57 ``indirect/older_`` rows of ``fix19a.jsonl``: a question asked as a statement naming the
  topic, answered from a search. An answer with the who-is-who slip shape has its subject rewritten
  to "Your <relation> <person>" as in R-094 (``splice_r094.py``); a row whose rewrite fails, or
  whose answer does not name the found value, is dropped and counted.

A row over 1,024 tokens, or whose friend message or answer shares a four-word run with the probe or
``hard_dev`` pools (R-110), is skipped and counted. ``results/vet/R-114/items.txt`` holds the 54
answers one fresh judge marked under R-110's rubric, written by this build before ``VET_REJECTED``
was added; the two rows it rejected are dropped and counted. The build stops if 6.2's rows change,
a row id repeats, or a slip-shaped answer is left. 6.2's rows come first, byte for byte.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

from transformers import AutoTokenizer

from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.scoring import slip_shape

sys.path.insert(0, str(Path(__file__).parent))
from build_r110 import MAX_ROW_TOKENS, TEST_GRAMS, four_grams, row_tokens  # noqa: E402

DATA = Path("data/screens")
BASE_SET, OUT = DATA / "fix17cr11.jsonl", DATA / "fix17cs3.jsonl"
STATEMENTS, ASKS = DATA / "fix18a.jsonl", DATA / "fix19a.jsonl"
# The vetting judge's two rejections (results/vet/R-114): each answer adds a claim no passage makes.
VET_REJECTED = {"indirect/older_0009", "indirect/older_0014"}
PEOPLE = "|".join(sorted(TRAIN.people, key=len, reverse=True))
VALUES = sorted({v for fact in TRAIN.facts.values() for v in fact.values}, key=len, reverse=True)


def read_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def friend_message(turns: list[dict]) -> str:
    return next(
        t["content"]
        for t in reversed(turns[:-1])
        if t["role"] == "user" and not t["content"].startswith("Tool result")
    )


def tool_result(turns: list[dict]) -> str:
    return next(
        t["content"] for t in reversed(turns[:-1]) if t["content"].startswith("Tool result")
    )


def found_line(relation: str, result: str) -> tuple[str, str] | None:
    """The returned fact line naming the relation and one train person, and that person."""
    for line in result.splitlines():
        if not line.startswith("User:") or not re.search(rf"\b{relation}\b", line):
            continue
        names = set(re.findall(rf"\b({PEOPLE})\b", line))
        if len(names) == 1:
            return line, names.pop()
    return None


def rewritten(answer: str, relation: str, person: str) -> str:
    """The answer with its subject in the "Your <relation> <person>" shape (R-094)."""
    subject = rf"(?:\b[A-Z][a-z]+'s {relation}|\bMy {relation})(?:,? (?:{person})\b,?)?"
    text = re.sub(rf"(?<=[.!?] ){subject}|^{subject}", f"Your {relation} {person}", answer)
    text = re.sub(subject, f"your {relation} {person}", text)
    return re.sub(r"\bwho is my\b", "who is your", text, flags=re.IGNORECASE)


def ask_row(row: dict, tally: Counter, changed: list[dict]) -> dict | None:
    """The indirect-question row with a slip-free answer naming the found value, or None."""
    turns = row["turns"]
    answer, message = turns[-1]["content"], friend_message(turns)
    relation = re.findall(r"\bmy ([a-z]+)", message.casefold())[0]
    found = found_line(relation, tool_result(turns))
    if found is None:
        tally["ask_no_single_person"] += 1
        return None
    line, person = found
    if slip_shape(answer, message):
        fixed = rewritten(answer, relation, person)
        if slip_shape(fixed, message) or person not in fixed:
            tally["ask_rewrite_failed"] += 1
            return None
        changed.append({"id": row["id"], "from": answer, "to": fixed})
        answer = fixed
    values = [v for v in VALUES if v.casefold() in line.casefold()]
    if not any(v.casefold() in answer.casefold() for v in values):
        tally["ask_found_value_missing"] += 1
        return None
    return {**row, "turns": [*turns[:-1], {**turns[-1], "content": answer}]}


def vet_item(n: int, row: dict) -> str:
    """One item in R-110's vetting format."""
    passages = tool_result(row["turns"]).removeprefix("Tool result for search_corpus: ")
    passages = passages.rsplit("\nUse this result", 1)[0]
    passages = re.sub(r"\[chunk_id=[^\]]*\]\n", "PASSAGE:\n", passages)
    return (
        f"ITEM {n}\nQUESTION: {friend_message(row['turns'])}\nSEARCH RESULT:\n{passages}\n"
        f"ANSWER: {row['turns'][-1]['content']}\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=OUT, help="where to write the set")
    parser.add_argument("--vet", type=Path, help="write the question rows for the vetting judge")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    base_rows = read_rows(BASE_SET)
    statements = [r for r in read_rows(STATEMENTS) if r["id"].startswith("facts/statement_")]
    asks = [r for r in read_rows(ASKS) if r["id"].startswith("indirect/older_")]
    if len(statements) != 57 or len(asks) != 57:
        raise SystemExit(f"expected 57 and 57 rows, found {len(statements)} and {len(asks)}")
    tally, changed, added = Counter(), [], []
    for group, rows in (("statement", statements), ("ask", asks)):
        for row in rows:
            if row["id"] in VET_REJECTED:
                tally[f"{group}_vet_rejected"] += 1
                continue
            if group == "ask":
                row = ask_row(row, tally, changed)
                if row is None:
                    continue
            text = friend_message(row["turns"])
            if group == "ask":
                text += " " + row["turns"][-1]["content"]
            if four_grams(text) & TEST_GRAMS:
                tally[f"{group}_shares_test_wording"] += 1
                continue
            if row_tokens(row["turns"], tokenizer) > MAX_ROW_TOKENS:
                tally[f"{group}_too_long"] += 1
                continue
            tally[f"{group}_kept"] += 1
            added.append(row)
    ids = [r["id"] for r in base_rows + added]
    if len(ids) != len(set(ids)):
        raise SystemExit("a row id repeats")
    left = sum(
        slip_shape(r["turns"][-1]["content"], friend_message(r["turns"]))
        for r in added
        if r["kind"] in ("older", "confirm")
    )
    if left:
        raise SystemExit(f"{left} slip-shaped answers left")
    base = BASE_SET.read_text(encoding="utf-8")
    args.out.write_text(
        base + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in added), encoding="utf-8"
    )
    if not args.out.read_text(encoding="utf-8").startswith(base):
        raise SystemExit("6.2's rows changed")
    if args.vet:
        args.vet.parent.mkdir(parents=True, exist_ok=True)
        items = [r for r in added if r["kind"] == "older"]
        text = "\n".join(vet_item(n, r) for n, r in enumerate(items))
        args.vet.write_text(text, encoding="utf-8")
    report = {
        "provenance": run_metadata(),
        "base_set": BASE_SET.as_posix(),
        "base_sha256": hashlib.sha256(base.encode("utf-8")).hexdigest(),
        "out_sha256": hashlib.sha256(args.out.read_bytes()).hexdigest(),
        "appended": len(added),
        "statement_rows": sum(r["kind"] == "statement" for r in base_rows + added),
        "tally": dict(sorted(tally.items())),
        "rewritten": changed,
    }
    args.out.with_suffix(".provenance.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8"
    )
    print(f"{args.out}: {len(added)} rows appended; {report['tally']}")
    print(f"sha256 {report['out_sha256']}")


if __name__ == "__main__":
    main()
