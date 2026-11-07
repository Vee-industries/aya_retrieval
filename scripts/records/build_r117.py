"""R-117: 6.31's set, 6.3's rows with the scripted ask answers and 24 contrast statements.

Usage: python scripts/records/build_r117.py [--vet results/vet/R-117]

6.3 failed at 82 and 83 (R-116): at seed 83 it answered 7 probe questions in the stored line's own
wording ("Ayaan, who is my teammate, speaks fluent Korean."), and at probe 51203 it searched or said
it did not know for "Esme forgot my birthday again". The panel (R-117) traced the first to fix 19a's
answers, some of which repeat the friend's own line, and the second to a gap: no training row has
another person forgetting or losing something with no question and no search. From 6.3's 1,079 rows:

- the 52 ``indirect/older_`` rows keep their conversation and search, and their answer becomes the
  pool's scripted "Your {relation} {person} ..." answer (as C2, ``splice_r098.py``). The value is
  the one fact value both the answer and the found line name; the person and relation are the ones
  on that line. A row stops the build unless each is found exactly once;
- 24 ``contrast/statement_`` rows are appended: three small-talk exchanges from the train pool's
  moods, then one of the 8 frames below with a train-pool person or relation, answered without a
  search. No frame has "forgot my", "my birthday" or the speaker as the one who forgets.

Every other row is kept byte for byte, in order. A contrast row whose message or reply shares a
four-word run with the probe or ``hard_dev`` pools (R-110), or which is over 1,024 tokens, stops the
build. The build also stops if a changed answer repeats the friend's voice ("my <relation>", "I
keep", "I should"), if a slip-shaped answer is left, if a row id repeats, or if the set has fewer
memory-word asks answered from a search than contrast rows.
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
from aya_retrieval.scoring import slip_shape

sys.path.insert(0, str(Path(__file__).parent))
from build_r110 import MAX_ROW_TOKENS, TEST_GRAMS, four_grams, row_tokens  # noqa: E402
from build_r114 import friend_message, read_rows, tool_result  # noqa: E402

DATA = Path("data/screens")
BASE_SET, OUT = DATA / "fix17cs3.jsonl", DATA / "fix17cs31.jsonl"
SEED = 117
# (message, reply): another person forgets, loses or has a birthday; no question, no search.
FRAMES = (
    ("{person} left their keys at my place again", "Oh no. At least they know where to find them."),
    ("my {relation} lost their wallet on the bus", "What bad luck. I hope someone hands it in."),
    (
        "{person} keeps forgetting to text me back",
        "That can be annoying. Maybe they've just been busy.",
    ),
    ("{person} is planning a party for their fortieth", "Fun! Forty is a big one."),
    ("my {relation} forgot their umbrella and got soaked", "Oof, that's a wet walk home."),
    (
        "{person} lost track of time and missed the train",
        "That happens. Hope the next one came soon.",
    ),
    ("{person} had a birthday dinner last night", "Sounds like a nice evening."),
    (
        "my {relation} forgot about our lunch today",
        "That's a letdown. Maybe you can pick another day.",
    ),
)
BARRED = re.compile(r"forgot my|my birthday|\bi (forgot|lost|keep forgetting)\b", re.IGNORECASE)
VOICE = re.compile(rf"\bmy (?:{'|'.join(TRAIN.relations)})\b|\bI keep\b|\bI should\b")
MEMORY_WORDS = re.compile(r"\b(forget|forgot|forgetting|remember|lost)\b", re.IGNORECASE)


def words(text: str, choices) -> set[str]:
    return {c for c in choices if re.search(rf"\b{re.escape(c)}\b", text)}


def one(found: set, what: str, row_id: str):
    if len(found) != 1:
        raise SystemExit(f"{row_id}: {what} found {len(found)} times: {sorted(found)}")
    return found.pop()


def scripted(row: dict) -> str:
    """The pool's scripted answer for the fact the row's answer and the found line both name."""
    turns = row["turns"]
    answer = turns[-1]["content"]
    relation = re.findall(r"\bmy ([a-z]+)", friend_message(turns).casefold())[0]
    lines = [
        line
        for line in tool_result(turns).splitlines()
        if line.startswith("User:") and re.search(rf"\b{relation}\b", line)
    ]
    line = one({x for x in lines if len(words(x, TRAIN.people)) == 1}, "found line", row["id"])
    person = one(words(line, TRAIN.people), "person", row["id"])
    fact, value = one(
        {
            (f, v)
            for f, t in TRAIN.facts.items()
            for v in t.values
            if v.casefold() in answer.casefold() and v.casefold() in line.casefold()
        },
        "value",
        row["id"],
    )
    return TRAIN.facts[fact].answer.format(relation=relation, person=person, value=value)


def contrast_rows() -> list[dict]:
    rng = random.Random(SEED)
    rows = []
    for f, (message, reply) in enumerate(FRAMES):
        for k in range(3):
            turns = []
            for _ in range(3):
                mood = rng.choice(TRAIN.moods)
                subject = rng.choice(TRAIN.subjects)
                turns += [
                    {
                        "role": "user",
                        "content": rng.choice(mood.user_lines).format(subject=subject),
                    },
                    {
                        "role": "assistant",
                        "content": rng.choice(mood.replies).format(subject=subject),
                    },
                ]
            text = message.format(
                person=rng.choice(TRAIN.people), relation=rng.choice(TRAIN.relations)
            )
            turns += [{"role": "user", "content": text}, {"role": "assistant", "content": reply}]
            rows.append(
                {"id": f"contrast/statement_{3 * f + k:04d}", "kind": "statement", "turns": turns}
            )
    return rows


def searched_memory_asks(rows: list[dict]) -> int:
    return sum(
        1
        for r in rows
        if r["kind"] in ("older", "confirm")
        and MEMORY_WORDS.search(friend_message(r["turns"]))
        and any(t["content"].startswith("Tool result") for t in r["turns"])
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=OUT, help="where to write the set")
    parser.add_argument("--vet", type=Path, help="folder for the vetting judge's two sheets")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    base_lines = [line for line in BASE_SET.read_text(encoding="utf-8").splitlines() if line]
    rows = read_rows(BASE_SET)
    changed = []
    out_lines = []
    for line, row in zip(base_lines, rows, strict=True):
        if row["id"].startswith("indirect/older_"):
            answer = scripted(row)
            if VOICE.search(answer) or slip_shape(answer, friend_message(row["turns"])):
                raise SystemExit(f"{row['id']}: the scripted answer fails the voice or slip check")
            changed.append({"id": row["id"], "from": row["turns"][-1]["content"], "to": answer})
            if answer != row["turns"][-1]["content"]:
                turns = [*row["turns"][:-1], {**row["turns"][-1], "content": answer}]
                line = json.dumps({**row, "turns": turns}, ensure_ascii=False)
        out_lines.append(line)
    if len(changed) != 52:
        raise SystemExit(f"expected 52 indirect rows, found {len(changed)}")
    added = contrast_rows()
    for row in added:
        text = row["turns"][-2]["content"] + " " + row["turns"][-1]["content"]
        if BARRED.search(text):
            raise SystemExit(f"{row['id']}: barred wording: {text}")
        if four_grams(text) & TEST_GRAMS:
            raise SystemExit(f"{row['id']}: shares a four-word run with the test pools: {text}")
        if row_tokens(row["turns"], tokenizer) > MAX_ROW_TOKENS:
            raise SystemExit(f"{row['id']}: over {MAX_ROW_TOKENS} tokens")
    all_rows = [json.loads(line) for line in out_lines] + added
    ids = [r["id"] for r in all_rows]
    if len(ids) != len(set(ids)):
        raise SystemExit("a row id repeats")
    left = sum(
        slip_shape(r["turns"][-1]["content"], friend_message(r["turns"]))
        for r in all_rows
        if r["kind"] in ("older", "confirm")
    )
    if left:
        raise SystemExit(f"{left} slip-shaped answers left")
    asks = searched_memory_asks(all_rows)
    if asks < len(added):
        raise SystemExit(f"{asks} memory-word asks answered from a search, fewer than {len(added)}")
    text = "".join(line + "\n" for line in out_lines)
    text += "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in added)
    args.out.write_text(text, encoding="utf-8")
    moved = {r["id"] for r, a, b in zip(rows, base_lines, out_lines, strict=True) if a != b}
    if moved != {c["id"] for c in changed if c["from"] != c["to"]}:
        raise SystemExit("a row other than the scripted answers changed")
    if args.vet:
        args.vet.mkdir(parents=True, exist_ok=True)
        by_id = {r["id"]: r for r in all_rows}
        asks_sheet = []
        for n, c in enumerate(changed):
            row = by_id[c["id"]]
            passages = tool_result(row["turns"]).removeprefix("Tool result for search_corpus: ")
            passages = passages.rsplit("\nUse this result", 1)[0]
            passages = re.sub(r"\[chunk_id=[^\]]*\]\n", "PASSAGE:\n", passages)
            asks_sheet.append(
                f"ITEM {n}\nQUESTION: {friend_message(row['turns'])}\nSEARCH RESULT:\n{passages}\n"
                f"ANSWER: {c['to']}\n"
            )
        (args.vet / "asks.txt").write_text("\n".join(asks_sheet), encoding="utf-8")
        chats = []
        for n, row in enumerate(added):
            lines = [f"{t['role'].upper()}: {t['content']}" for t in row["turns"][:-1]]
            chats.append(
                f"ITEM {n}\n" + "\n".join(lines) + f"\nREPLY: {row['turns'][-1]['content']}\n"
            )
        (args.vet / "statements.txt").write_text("\n".join(chats), encoding="utf-8")
    report = {
        "provenance": run_metadata(),
        "base_set": BASE_SET.as_posix(),
        "base_sha256": hashlib.sha256(BASE_SET.read_bytes()).hexdigest(),
        "out_sha256": hashlib.sha256(args.out.read_bytes()).hexdigest(),
        "rows": len(all_rows),
        "appended": len(added),
        "statement_rows": sum(r["kind"] == "statement" for r in all_rows),
        "memory_word_asks_searched": asks,
        "kinds": dict(sorted(Counter(r["kind"] for r in all_rows).items())),
        "rewritten": changed,
    }
    args.out.with_suffix(".provenance.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8"
    )
    print(
        f"{args.out}: {len(all_rows)} rows, {len(changed)} answers scripted, {len(added)} appended"
    )
    print(f"statement rows {report['statement_rows']}; memory-word asks searched {asks}")
    print(f"sha256 {report['out_sha256']}")


if __name__ == "__main__":
    main()
