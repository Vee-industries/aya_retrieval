"""R-110: 6.21's step rows, 6.2's set plus 100 train-pool rows whose found line says more.

Usage: python scripts/records/build_r110.py --index C:/scratch/build_r110.sqlite

Every passage in 6.2's set is one short fact line, so no row asks the model to pick the asked detail
out of a line that says more. Three kinds of row, all from fresh train-pool conversations, searched
with the real search tool and answered with the scripted answer; a row whose search does not return
the changed line is skipped:

- ``two``: the fact line also states a second, different fact about the same person; the question
  asks one of the two, the asked fact first in half the rows and second in the other half.
- ``runon``: the fact line is joined with one or two of the pool's small-talk lines, the fact first,
  in the middle or last.
- ``never``: a ``never_told`` question whose returned passages are such lines about other people,
  so a long passage is not a cue that the answer is there.

6.2's rows are kept byte for byte. The build stops if an answer leaves out the asked value or names
the line's other value, or if an answer has the who-is-who slip shape. A row whose changed line
shares a four-word run with the probe or ``hard_dev`` pools is skipped: two of the pool's small-talk
lines and three fact wordings already do, in 6.2's rows, and the step adds none. Coffee orders are
left out (the panel kept food and weekday values out of the step); no phone-typing or held-out
correction form is used.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import random
import re
from collections import Counter
from pathlib import Path

from transformers import AutoTokenizer

from aya_retrieval.chat import SYSTEM_WITH_TOOL
from aya_retrieval.conversations import CONFIRM, NEVER_TOLD, OLDER, POOLS, build_item
from aya_retrieval.demonstrations import demonstration_turns
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.recall_tool import build_recall_tool
from aya_retrieval.scoring import slip_shape
from aya_retrieval.tool_prompt import system_prompt_with_tools

DATA = Path("data/screens")
BASE_SET, OUT = DATA / "fix17cr11.jsonl", DATA / "fix17cs21.jsonl"
COUNTS = {"two": 40, "runon": 40, "never": 20}
SIZE = 58
MAX_ROW_TOKENS = 1024
# As the training builder: found and not-found rows return the same numbers of passages (R-020).
DECOY_CHOICES = {OLDER: (0, 1, 2), CONFIRM: (0, 1, 2), NEVER_TOLD: (1, 2, 3)}
FIRST_SEED = 920_000_000
LEFT_OUT = {"coffee"}
JOINERS = (", and ", ". also ", ", oh and ")
POSITIONS = ("first", "middle", "last")


def row_tokens(turns: list[dict], tokenizer) -> int:
    system = {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)}
    ids = tokenizer.apply_chat_template([system, *turns], tokenize=True, return_dict=True)
    return len(ids["input_ids"])


def words(text: str) -> list[str]:
    return "".join(c if c.isalnum() else " " for c in text.casefold()).split()


def four_grams(text: str) -> set[tuple[str, ...]]:
    w = words(text)
    return {tuple(w[i : i + 4]) for i in range(len(w) - 3)}


def pool_strings(pool) -> list[str]:
    """Every string a pool holds, its fact templates included."""
    out = [*pool.people, *pool.relations, *pool.subjects, *pool.acknowledgements]
    out += [*pool.unknown_replies, *(line for pair in pool.statements for line in pair)]
    for mood in pool.moods:
        out += [*mood.user_lines, *mood.replies]
    for fact in pool.facts.values():
        out += [fact.statement, fact.answer, fact.confirm, fact.query, *fact.values]
        out += [fact.same_words, fact.new_words, fact.indirect]
    return out


TEST_GRAMS = set().union(
    *(four_grams(s) for name in ("probe", "hard_dev") for s in pool_strings(POOLS[name]))
)


def relation_person(template, line: str) -> tuple[str, str]:
    """Return the relation and person a fact line written from ``template`` names."""
    pattern = re.escape(template.statement)
    for name in ("relation", "person", "value"):
        pattern = pattern.replace(re.escape("{" + name + "}"), f"(?P<{name}>.+?)", 1)
    found = re.fullmatch(pattern, line)
    if not found:
        raise SystemExit(f"fact line not in its template's wording: {line!r}")
    return found["relation"], found["person"]


def second_fact(rng: random.Random, asked_type: str, relation: str, person: str):
    """Return a fact line about the same person of another type, and its value."""
    other_type = rng.choice(sorted(set(TRAIN.facts) - LEFT_OUT - {asked_type}))
    template = TRAIN.facts[other_type]
    value = rng.choice(template.values)
    return template.statement.format(relation=relation, person=person, value=value), value


def small_talk(rng: random.Random) -> str:
    mood = rng.choice(TRAIN.moods)
    return rng.choice(mood.user_lines).format(subject=rng.choice(TRAIN.subjects))


def join(parts: list[str], rng: random.Random) -> str:
    line = parts[0]
    for part in parts[1:]:
        line += rng.choice(JOINERS) + part
    return line


def changed_line(kind_name: str, n: int, line: str, fact_type: str, rng: random.Random):
    """Return the longer line and the value that must not appear in the answer ('' for none)."""
    relation, person = relation_person(TRAIN.facts[fact_type], line)
    if kind_name == "two" or (kind_name == "never" and n % 2 == 0):
        other, value = second_fact(rng, fact_type, relation, person)
        parts = [line, other] if kind_name == "never" or n % 4 < 2 else [other, line]
        return join(parts, rng), value
    talk = [small_talk(rng) for _ in range(rng.choice((1, 2)))]
    where = POSITIONS[(n // 2) % 3] if kind_name == "runon" else rng.choice(POSITIONS)
    if where == "first":
        parts = [line, *talk]
    elif where == "last":
        parts = [*talk, line]
    else:
        parts = [talk[0], line, talk[1] if len(talk) == 2 else small_talk(rng)]
    return join(parts, rng), ""


def make(kind_name: str, n: int, seed: int, rng: random.Random):
    """Return one row's changed item, the changed line and the value it must not answer with."""
    kind = NEVER_TOLD if kind_name == "never" else (OLDER, CONFIRM)[n % 2]
    decoys = rng.choice(DECOY_CHOICES[kind])
    if kind == NEVER_TOLD and not decoys:
        return None
    fact_type = rng.choice(sorted(set(TRAIN.facts) - LEFT_OUT))
    item = build_item(
        f"r110_{kind_name}_{n:04d}", seed, SIZE, kind, "train", decoys, fact_type=fact_type
    )
    slot = item.fact_index
    if kind == NEVER_TOLD:
        slots = [i for i, (u, _) in enumerate(item.older()) if item.decoy in u]
        if len(slots) != 1:
            return None
        slot = slots[0]
    user, reply = item.exchanges[slot]
    line, other_value = changed_line(kind_name, n, user, fact_type, rng)
    exchanges = list(item.exchanges)
    exchanges[slot] = (line, reply)
    return dataclasses.replace(item, exchanges=tuple(exchanges)), line, other_value


def check(kind_name: str, fixed, line: str, other_value: str) -> None:
    """Stop the build unless the row's answer and changed line meet R-110's vetting."""
    if slip_shape(fixed.reply, fixed.message):
        raise SystemExit(f"{fixed.item_id}: answer has the who-is-who slip shape")
    if kind_name == "never":
        return
    if fixed.answer not in fixed.reply:
        raise SystemExit(f"{fixed.item_id}: answer leaves out the asked value")
    if other_value and other_value in fixed.reply:
        raise SystemExit(f"{fixed.item_id}: answer names the line's other value")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--index", type=Path, required=True, help="scratch search database")
    parser.add_argument("--out", type=Path, default=OUT, help="where to write the set")
    parser.add_argument("--vet", type=Path, help="write each row's question, line and answer here")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    rng = random.Random(FIRST_SEED)
    rows, vet, tally = [], [], Counter()
    seed = FIRST_SEED
    for kind_name, wanted in COUNTS.items():
        made = 0
        while made < wanted:
            seed += 1
            built = make(kind_name, made, seed, rng)
            if not built:
                tally[f"{kind_name}_unbuildable"] += 1
                continue
            fixed, line, other_value = built
            output = (
                build_recall_tool(fixed, args.index, match_all=False).execute(fixed.query).output
            )
            if line not in output:
                tally[f"{kind_name}_search_missed"] += 1
                continue
            if four_grams(line) & TEST_GRAMS:
                tally[f"{kind_name}_shares_test_wording"] += 1
                continue
            turns = demonstration_turns(fixed, output, fixed.reply, True, TRAIN.unknown_replies[0])
            if row_tokens(turns, tokenizer) > MAX_ROW_TOKENS:
                tally[f"{kind_name}_too_long"] += 1
                continue
            check(kind_name, fixed, line, other_value)
            tally[f"{kind_name}_{fixed.kind}_passages_{output.count('chunk_id=')}"] += 1
            rows.append({"id": fixed.item_id, "kind": fixed.kind, "turns": turns})
            vet.append(
                {
                    "id": fixed.item_id,
                    "question": fixed.message,
                    "found": output,
                    "answer": turns[-1]["content"],
                }
            )
            made += 1
    base = BASE_SET.read_text(encoding="utf-8")
    args.out.write_text(
        base + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8"
    )
    if not args.out.read_text(encoding="utf-8").startswith(base):
        raise SystemExit("6.2's rows changed")
    args.index.unlink(missing_ok=True)
    if args.vet:
        args.vet.write_text(json.dumps(vet, indent=1, ensure_ascii=False), encoding="utf-8")
    report = {
        "provenance": run_metadata(),
        "base_set": BASE_SET.as_posix(),
        "base_sha256": hashlib.sha256(base.encode("utf-8")).hexdigest(),
        "out_sha256": hashlib.sha256(args.out.read_bytes()).hexdigest(),
        "appended": len(rows),
        "counts": COUNTS,
        "tally": dict(tally),
    }
    args.out.with_suffix(".provenance.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8"
    )
    print(f"{args.out}: {len(rows)} rows appended; {dict(tally)}")


if __name__ == "__main__":
    main()
