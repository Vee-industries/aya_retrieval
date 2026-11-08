"""R-134: 6.37's set with the final answer of 28 deflecting in-view rows rewritten, for 6.38.

Usage: python scripts/records/build_r134.py [--vet results/vet/R-134] [--keep-old ID ...]

The panel of experts (R-134) traced 6.37's in-view misses ("It sounds like you're feeling a bit
lost or confused...", "Can you give me a hint?", "You can ask your cousin...") to 28 in-view
targets that are base's own deflections, trained at full loss. This build keeps all 1,094 rows,
their order, ids, kinds and every user turn, and replaces only the final assistant turn of those
28 rows with a plain answer that states the fact still in view. The targets are hand-written here
and stop the build if one breaks a rule registered in R-134 (value and name in the first
sentence, no question, no deflection word, at most one more sentence copied from another in-view
target, no who-is-who slip, no four-word run shared with the probe or hard_dev pools, at most
1,024 tokens).

``--vet DIR`` writes the blind judge's sheet: the 28 new answers and the 28 old ones shuffled
together (random seed 134), with the key kept apart. ``--keep-old`` leaves the named rows' old
answers in place (R-134 item 3: a target two judges reject).
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
from aya_retrieval.provenance import run_metadata
from aya_retrieval.scoring import slip_shape

sys.path.insert(0, str(Path(__file__).parent))
from build_r110 import MAX_ROW_TOKENS, TEST_GRAMS, four_grams, row_tokens  # noqa: E402

DATA = Path("data/screens")
BASE_SET = DATA / "fix17cs37.jsonl"
BASE_SHA = "04df294a"
OUT = DATA / "fix17cs38.jsonl"
# Row id suffix: (the value as the chat states it, the new final answer).
TARGETS = {
    "0000": ("5k", "Marc finished a 5k on Sunday. 5k is a solid achievement."),
    "0015": ("relay", "Ivan finished a relay on Sunday."),
    "0027": ("Harley", "Ivan rides a Harley to work."),
    "0036": ("Oslo", "Marc is moving to Oslo in the spring."),
    "0057": ("fantasy", "Priya writes fantasy novels at night."),
    "0058": ("Marble", "Dana just got a kitten called Marble."),
    "0059": ("Salt Road", "Dana plays bass in Salt Road."),
    "0060": ("Noodle", "Ivan just got a kitten called Noodle."),
    "0064": ("triathlon", "Greta finished a triathlon on Sunday."),
    "0077": ("Sea Otter", "Tomas's boat is called Sea Otter."),
    "0079": ("flat white", "Dana only ever orders a flat white."),
    "0085": ("director", "Priya was promoted to director. That's a big promotion."),
    "0086": ("telescope", "Priya won a telescope in a raffle. That's a pretty cool prize!"),
    "0088": ("Kawasaki", "Greta rides a Kawasaki to work."),
    "0094": ("iPhone", "Yusuf finally switched to an iPhone."),
    "0098": ("Pepper", "Ivan adopted a dog named Pepper last month."),
    "0099": ("Lady Grace", "Dana's boat is called Lady Grace."),
    "0103": ("Waffles", "Ivan adopted a dog named Waffles last month."),
    "0120": ("forearm", "Nell broke a forearm skiing."),
    "0121": ("Biscuit", "Nell adopted a dog named Biscuit last month."),
    "0122": ("half marathon", "Tomas finished a half marathon on Sunday."),
    "0130": ("twentieth", "Tomas rents on the twentieth floor."),
    "0132": ("Silas", "Greta had a baby and named them Silas."),
    "0134": ("Lollapalooza", "Omar got tickets to Lollapalooza."),
    "0136": ("seventh", "Greta rents on the seventh floor."),
    "0139": ("romance", "Nell writes romance novels at night."),
    "0145": ("Motorola", "Ivan finally switched to a Motorola."),
    "0146": ("Copper Moon", "Priya plays bass in Copper Moon."),
}
BANNED = (
    "hint", "remember", "recall", "feeling", "lost", "confused", "ask ", "tell me more",
    "something else", "it sounds like", "it seems like", "tough one", "i don't", "didn't",
    "you can",
)  # fmt: skip
SENTENCE = re.compile(r"(?<=[.!])\s+")


def check(row: dict, value: str, target: str, other_sentences: set[str]) -> str | None:
    """Return the first R-134 rule the target breaks, or None."""
    users = [t["content"] for t in row["turns"] if t["role"] == "user"]
    message = users[-1]
    fact = next((u for u in users[:-1] if value.casefold() in u.casefold()), None)
    if fact is None:
        return "value not in a fact turn"
    first, *rest = SENTENCE.split(target.strip())
    if value.casefold() not in first.casefold():
        return "value not in the first sentence"
    name = target.split()[0].removesuffix("'s")
    if name not in fact and not target.startswith(value):
        return "does not open with the person's name or the value"
    if target.startswith(("Your", "My")):
        return "opens with Your or My"
    if "?" in target:
        return "has a question"
    low = target.casefold()
    if hit := next((w for w in BANNED if w in low), None):
        return f"has {hit!r}"
    if len(rest) > 1 or (rest and rest[0] not in other_sentences):
        return "more than one sentence, or one not in another in-view target"
    if slip_shape(target, message):
        return "who-is-who slip"
    if four_grams(target) & TEST_GRAMS:
        return "shares a four-word run with the probe or hard_dev pools"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vet", type=Path, help="folder for the blind judge's sheet")
    parser.add_argument("--keep-old", nargs="*", default=[], choices=sorted(TARGETS))
    args = parser.parse_args()
    base_bytes = BASE_SET.read_bytes()
    if not hashlib.sha256(base_bytes).hexdigest().startswith(BASE_SHA):
        raise SystemExit(f"{BASE_SET} is not 6.37's set")
    lines = [line for line in base_bytes.decode("utf-8").splitlines(keepends=True) if line]
    rows = [json.loads(line) for line in lines]
    by_id = {r["id"]: r for r in rows}
    targets = {f"in_view_{k}": v for k, v in TARGETS.items() if k not in args.keep_old}
    if any(by_id[i]["kind"] != "in_view" for i in targets):
        raise SystemExit("a listed row is not in_view")
    other_sentences = {
        s
        for r in rows
        if r["kind"] == "in_view" and r["id"] not in targets
        for s in SENTENCE.split(r["turns"][-1]["content"].strip())
    }
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    out_lines, old = [], {}
    for line, row in zip(lines, rows, strict=True):
        if row["id"] not in targets:
            out_lines.append(line)
            continue
        value, target = targets[row["id"]]
        if broken := check(row, value, target, other_sentences):
            raise SystemExit(f"{row['id']}: {broken}: {target!r}")
        old[row["id"]] = row["turns"][-1]["content"]
        new = {**row, "turns": [*row["turns"][:-1], {**row["turns"][-1], "content": target}]}
        if row_tokens(new["turns"], tokenizer) > MAX_ROW_TOKENS:
            raise SystemExit(f"{row['id']}: over {MAX_ROW_TOKENS} tokens")
        out_lines.append(json.dumps(new, ensure_ascii=False) + "\n")
    OUT.write_text("".join(out_lines), encoding="utf-8")
    kept = [x for x, y in zip(lines, out_lines, strict=True) if x == y]
    if len(kept) != len(lines) - len(targets):
        raise SystemExit("a row outside the 28 changed")
    if args.vet:
        args.vet.mkdir(parents=True, exist_ok=True)
        items = [(i, "new", targets[i][1]) for i in targets] + [(i, "old", old[i]) for i in old]
        random.Random(134).shuffle(items)
        sheet, key = [], []
        for n, (i, which, answer) in enumerate(items):
            turns = by_id[i]["turns"]
            chat = [f"{t['role'].upper()}: {t['content']}" for t in turns[:-2]]
            sheet.append(
                f"ITEM {n}\n" + "\n".join(chat) + f"\nQUESTION: {turns[-2]['content']}\n"
                f"ANSWER: {answer}\n"
            )
            key.append({"item": n, "id": i, "answer": which})
        (args.vet / "items.txt").write_text("\n".join(sheet), encoding="utf-8")
        (args.vet / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    all_rows = [json.loads(line) for line in out_lines]
    report = {
        "provenance": run_metadata(),
        "base_set": BASE_SET.as_posix(),
        "base_sha256": hashlib.sha256(base_bytes).hexdigest(),
        "out_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
        "unchanged_sha256": hashlib.sha256("".join(kept).encode("utf-8")).hexdigest(),
        "rows": len(all_rows),
        "changed": sorted(targets),
        "kept_old": sorted(f"in_view_{k}" for k in args.keep_old),
        "statement_rows": sum(r["kind"] == "statement" for r in all_rows),
        "kinds": dict(sorted(Counter(r["kind"] for r in all_rows).items())),
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{OUT}: {report['rows']} rows, {len(targets)} answers changed, kinds {report['kinds']}")
    print(f"sha256 {report['out_sha256']}")


if __name__ == "__main__":
    main()
