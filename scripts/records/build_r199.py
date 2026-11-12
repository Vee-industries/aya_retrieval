"""R-199: candidate K1.2's training set: K1's rows with every fact line in a wording drawn per line.

Usage: python scripts/records/build_r199.py

K1.2 = K1 (``data/screens/k1_r178.jsonl``) with one change: every fact, in the chat, in the search
outputs and in a reply that repeats it, is restated in its template wording or one of
``build_r196.WORDINGS``, drawn by a generator seeded from the fact's own words, so a fact has one
wording wherever it appears. The fact is found anywhere in a line, so R-102's corrections, which
wrap it in other words, are reworded too. Nothing else changes: which lines a search returns,
their order and scores, whether it finds the fact, and every reply's content stay K1's, because
they were decided on the template wording (the fact type's own statement, from which every query
is written). So answers and decoys face one retrieval rule, a line's wording cannot change whether
it is returned, and the draw is the same for every kind of row and every source of row (builder,
R-102, spliced, fresh never_told). Text that states no fact is left as it is.

This changes only the training rows. Every evaluation keeps the plain keyword search.
``scripts/records/check_r199.py`` then checks the set before any training.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import re
import sys
from pathlib import Path

from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.stress import _statement_pattern

HERE = Path(__file__).resolve().parent
BASE = Path("data/screens/k1_r178.jsonl")
OUT = Path("data/screens/k1_2_r199.jsonl")
SALT = "R-199"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


WORDINGS = load("build_r196").WORDINGS
PATTERNS = [
    (re.compile(_statement_pattern(t.statement, TRAIN, t.values).pattern, re.I), t.statement)
    for t in TRAIN.facts.values()
]


def reworded(text: str, reply: bool = False) -> str:
    """Return ``text`` with the fact it states in its drawn wording; text with no fact unchanged.

    The fact is found anywhere in the text (R-102's corrections wrap it in other words), and the
    draw is seeded from the fact's own words, so a reply that repeats the user's line gets the
    same wording. In a reply, a fact that opens the sentence keeps its capital letter.
    """
    for pattern, statement in PATTERNS:
        found = pattern.search(text)
        if found:
            span = found.group(0)
            key = f"{SALT}|{span.casefold()}".encode()
            seed = int.from_bytes(hashlib.sha256(key).digest()[:8], "big")
            wording = random.Random(seed).choice((statement, *WORDINGS.get(statement, ())))
            new = wording.format(**found.groupdict())
            if reply and found.start() == 0 and span[0].isupper():
                new = new[0].upper() + new[1:]
            return text[: found.start()] + new + text[found.end() :]
    return text


def reworded_turn(turn: dict) -> dict:
    content = turn["content"]
    if content.startswith("Tool result for"):
        content = re.sub(
            r"^User: (.*)$", lambda m: f"User: {reworded(m.group(1))}", content, flags=re.M
        )
    elif turn["role"] == "user":
        content = reworded(content)
    elif "tool_name" not in content:  # a reply, not a search call
        content = reworded(content, reply=True)
    return {**turn, "content": content}


def main() -> None:
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    out = [{**row, "turns": [reworded_turn(t) for t in row["turns"]]} for row in rows]
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_text(text, encoding="utf-8")
    report = {
        "provenance": provenance,
        "record": "R-199",
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "rows_changed": sum(a != b for a, b in zip(rows, out, strict=True)),
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{OUT}: {report['rows']} rows, {report['rows_changed']} changed")


if __name__ == "__main__":
    main()
