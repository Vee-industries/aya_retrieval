"""R-153: 7's set, 6.37's 1,094 rows with 140 questions reworded as tag questions ("..., right?").

Usage: python scripts/records/build_r153.py [--vet PATH]

Why: on chats written by people who never saw the generator, a question that states a fact and asks
for agreement ("tomasz has a beagle right") rarely triggers a search (R-146: 23 of 29 `confirm`
misses never searched), and 6.37 then agrees with whatever the user said. Every TRAIN `confirm`
question is a "did i ..." or "have i ..." form, so the model never saw the other way people check
a fact. The panel (R-153) agreed on one change: reword some questions as tag questions and keep
everything else in the row byte for byte, so nothing but the trigger is taught.

- ``confirm`` (100 of 230): the last user message becomes the row's own answer restated as a
  claim with a tag. Half name the true value; a quarter a value another person in the search result
  holds (a decoy, or the old value of a correction); a quarter a value of that type the chat never
  mentions. The search, its result and the answer are unchanged; the answer already states the
  true value, so a claim with a wrong value is corrected without a new answer shape.
- ``never_told`` (20 of the 86 written with a ``confirm`` wording): the question becomes a claim
  about the asked relation with a tag; the search and the plain decline are unchanged.
- ``in_view`` (20 of 150): the question becomes a claim of the visible fact's true value with a
  tag; no search, the answer unchanged. A tag question about a fact in view needs no search.

The build stops if a reworded row breaks a rule: the answer names the value the claim states when
that value is wrong; the claim shares a four-word run with the probe or ``hard_dev`` pools; the row
exceeds 1,024 tokens. Rows are picked with random.Random(153). Writes data/screens/fix17cs7.jsonl.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

from transformers import AutoTokenizer

from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata

sys.path.insert(0, str(Path(__file__).parent))
from build_r110 import MAX_ROW_TOKENS, TEST_GRAMS, four_grams, row_tokens  # noqa: E402

DATA = Path("data/screens")
BASE_SET = DATA / "fix17cs37.jsonl"
BASE_SHA = ("04df294a", "7b0183de")  # 6.37's set as checked out with CRLF, and as git stores it
OUT = DATA / "fix17cs7.jsonl"
COUNTS = {"confirm": 100, "never_told": 20, "in_view": 20}
TAGS = (", right?", " right?", " right", ", isn't that right?", " yeah?", ", yeah", " correct?")
FIELDS = ("relation", "person", "value", "who")


def pattern(template: str) -> re.Pattern:
    text = re.escape(template)
    for field in FIELDS:
        text = text.replace(re.escape("{" + field + "}"), f"(?P<{field}>.+?)")
    return re.compile(f"^{text}$", re.IGNORECASE)


ANSWERS = {name: pattern(t.answer) for name, t in TRAIN.facts.items()}
CONFIRMS = {name: pattern(t.confirm) for name, t in TRAIN.facts.items()}
STATEMENTS = {name: pattern(t.statement) for name, t in TRAIN.facts.items()}


def match_one(patterns: dict, text: str) -> tuple[str, dict] | None:
    hits = [(name, m.groupdict()) for name, p in patterns.items() if (m := p.match(text.strip()))]
    return hits[0] if len(hits) == 1 else None


def claim(fact: str, relation: str, person: str, value: str, rng: random.Random) -> str:
    """The fact's scripted answer turned into the user's claim, in a casual form with a tag."""
    answer = TRAIN.facts[fact].answer
    form = rng.choice(("full", "full", "relation", "person"))
    if form == "relation":
        answer = answer.replace("{relation} {person}", "{relation}")
    elif form == "person":
        answer = answer.replace("Your {relation} {person}", "{person}")
    text = answer.format(relation=relation, person=person, value=value).rstrip(".")
    text = re.sub(r"^Your ", "my ", text)
    if rng.random() < 0.7:
        text = text[0].lower() + text[1:]
    return text + rng.choice(TAGS)


def result_values(row: dict, fact: str) -> set[str]:
    """Every value of the fact's type that the row's search result states."""
    found = set()
    for turn in row["turns"]:
        if turn["role"] == "user" and turn["content"].startswith("Tool result"):
            for line in turn["content"].splitlines():
                if line.startswith("User: ") and (m := STATEMENTS[fact].match(line[6:])):
                    found.add(m.group("value"))
    return found


def chat_text(row: dict) -> str:
    return " ".join(t["content"] for t in row["turns"]).casefold()


def reword_confirm(row: dict, n: int, rng: random.Random) -> tuple[str, str, str]:
    fact, fields = match_one(ANSWERS, row["turns"][-1]["content"])
    true = fields["value"]
    others = sorted(result_values(row, fact) - {true})
    spare = sorted(v for v in TRAIN.facts[fact].values if v.casefold() not in chat_text(row))
    if n % 4 == 2 and others:
        named = rng.choice(others)
    elif n % 4 == 3 and spare:
        named = rng.choice(spare)
    else:
        named = true
    return claim(fact, fields["relation"], fields["person"], named, rng), named, true


def reword_never(row: dict, rng: random.Random) -> tuple[str, str] | None:
    users = [i for i, t in enumerate(row["turns"]) if t["role"] == "user"]
    asked = row["turns"][users[-2]]["content"]
    hit = match_one(CONFIRMS, asked)
    if hit is None:
        return None
    fact, fields = hit
    value = rng.choice(TRAIN.facts[fact].values)
    answer = TRAIN.facts[fact].answer.replace("{relation} {person}", "{relation}")
    text = answer.format(relation=fields["relation"], value=value).rstrip(".")
    text = re.sub(r"^Your ", "my ", text)
    return text + rng.choice(TAGS), value


def reword_in_view(row: dict, rng: random.Random) -> tuple[str, str] | None:
    for turn in reversed(row["turns"][:-2]):
        if turn["role"] == "user" and (hit := match_one(STATEMENTS, turn["content"])):
            fact, fields = hit
            if fields.get("value", "").casefold() not in row["turns"][-1]["content"].casefold():
                return None
            return claim(fact, fields["relation"], fields["person"], fields["value"], rng), fields[
                "value"
            ]
    return None


def check(row: dict, message: str, named: str, true: str, tokenizer) -> str | None:
    answer = row["turns"][-1]["content"]
    if named.casefold() != true.casefold() and named.casefold() in answer.casefold():
        return "answer names the wrong value the claim states"
    if four_grams(message) & TEST_GRAMS:
        return "claim shares a four-word run with the probe or hard_dev pools"
    if row_tokens(row["turns"], tokenizer) > MAX_ROW_TOKENS:
        return "row too long"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--vet", type=Path, help="write every reworded row's old and new question here"
    )
    args = parser.parse_args()
    base_bytes = BASE_SET.read_bytes()
    if not hashlib.sha256(base_bytes).hexdigest().startswith(BASE_SHA):
        raise SystemExit(f"{BASE_SET} is not 6.37's set")
    lines = [line for line in base_bytes.decode("utf-8").splitlines() if line]
    rows = [json.loads(line) for line in lines]
    rng = random.Random(153)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    by_kind = {k: [i for i, r in enumerate(rows) if r["kind"] == k] for k in COUNTS}
    changed, vet, skipped = {}, [], Counter()
    for kind, count in COUNTS.items():
        for n, i in enumerate(rng.sample(by_kind[kind], len(by_kind[kind]))):
            if sum(1 for v in vet if v["kind"] == kind) == count:
                break
            row = json.loads(lines[i])
            users = [j for j, t in enumerate(row["turns"]) if t["role"] == "user"]
            slot = users[-2] if kind != "in_view" else users[-1]
            if kind == "confirm":
                message, named, true = reword_confirm(row, n, rng)
            else:
                made = (reword_never if kind == "never_told" else reword_in_view)(row, rng)
                if made is None:
                    skipped[f"{kind}: no single template matches"] += 1
                    continue
                message, named = made
                true = named if kind == "in_view" else ""
            old = row["turns"][slot]["content"]
            row["turns"][slot]["content"] = message
            if broken := check(row, message, named, true or named, tokenizer):
                skipped[f"{kind}: {broken}"] += 1
                continue
            changed[i] = json.dumps(row, ensure_ascii=False)
            vet.append(
                {
                    "id": row["id"],
                    "kind": kind,
                    "old": old,
                    "new": message,
                    "named_is_true": named == true,
                    "answer": row["turns"][-1]["content"],
                }
            )
    if any(sum(1 for v in vet if v["kind"] == k) != c for k, c in COUNTS.items()):
        raise SystemExit(f"could not reword enough rows: {skipped}")
    out = [changed.get(i, line) for i, line in enumerate(lines)]
    text = "\n".join(out) + "\n"
    OUT.write_text(text, encoding="utf-8", newline="\n")
    provenance = {
        **run_metadata(),
        "record": "R-153",
        "from": str(BASE_SET),
        "rows": len(out),
        "reworded": dict(Counter(v["kind"] for v in vet)),
        "named_true_in_confirm": sum(v["named_is_true"] for v in vet if v["kind"] == "confirm"),
        "skipped": dict(skipped),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }
    record = json.dumps(provenance, indent=1)
    OUT.with_suffix(".provenance.json").write_text(record, encoding="utf-8")
    if args.vet:
        args.vet.write_text(json.dumps(vet, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {OUT}: {len(out)} rows, reworded {provenance['reworded']}")
    print(f"skipped {dict(skipped)}")
    print(f"sha256 {provenance['sha256'][:8]}")


if __name__ == "__main__":
    main()
