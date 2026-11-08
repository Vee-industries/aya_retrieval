"""R-118: 72 in-view rows with scripted answers, for 6.32 (from scratch) and 6.311 (on top of 6.31).

Usage: python scripts/records/build_r118.py [--vet results/vet/R-118]

6.31 at seed 82 answered 16 ``hard_dev`` in-view questions with sympathy instead of the fact that
is still in the chat ("It sounds like you're trying to remember..."). The panel (R-118) found that
26 of the 150 in-view targets every copy since v6 trains on open the same way, base's own words
kept because they name the value somewhere. These rows teach the plain answer instead: fresh
train-pool conversations whose fact is among the last exchanges, asked in an indirect form (the
template's own or ``train_phrasings.MORE_INDIRECT``), answered with the pool's scripted "Your
{relation} {person} ..." answer and no search. Two sets are written:

- ``fix17cs32.jsonl``: 6.31's 1,103 rows byte for byte, then the 72 rows;
- ``fix17cs311.jsonl``: the 72 rows after 216 of 6.31's rows, drawn per kind in proportion
  (random seed 311), for one epoch on top of 6.31's adapter.

A row whose question, fact line or answer shares a four-word run with the probe or ``hard_dev``
pools (R-110), or which is over 1,024 tokens, is skipped and counted. The build stops if an answer
leaves out the value, has the who-is-who slip shape or the friend's voice (R-117), or if a row's
turns or id repeat one of 6.31's.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from pathlib import Path

from transformers import AutoTokenizer

from aya_retrieval.conversations import IN_VIEW, build_item
from aya_retrieval.demonstrations import demonstration_turns
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.scoring import slip_shape

sys.path.insert(0, str(Path(__file__).parent))
from build_r110 import MAX_ROW_TOKENS, SIZE, TEST_GRAMS, four_grams, row_tokens  # noqa: E402
from build_r117 import VOICE  # noqa: E402

DATA = Path("data/screens")
BASE_SET = DATA / "fix17cs31.jsonl"
FROM_SCRATCH, ON_TOP = DATA / "fix17cs32.jsonl", DATA / "fix17cs311.jsonl"
NEW_ROWS, REPLAY_ROWS = 72, 216
FIRST_SEED = 118_000_000  # clear of every builder's conversation seeds
REPLAY_SEED = 311


def fact_type(value: str) -> str:
    return "/".join(k for k, t in TRAIN.facts.items() if value in t.values)


def replay(rows: list[dict]) -> list[dict]:
    """REPLAY_ROWS of ``rows``, each kind in proportion (largest remainder), in their order."""
    kinds = Counter(r["kind"] for r in rows)
    share = {k: REPLAY_ROWS * n / len(rows) for k, n in kinds.items()}
    counts = {k: int(v) for k, v in share.items()}
    for k in sorted(share, key=lambda k: share[k] - counts[k], reverse=True)[
        : REPLAY_ROWS - sum(counts.values())
    ]:
        counts[k] += 1
    rng = random.Random(REPLAY_SEED)
    picked = set()
    for kind in sorted(kinds):
        picked |= set(
            rng.sample([i for i, r in enumerate(rows) if r["kind"] == kind], counts[kind])
        )
    return [r for i, r in enumerate(rows) if i in picked]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vet", type=Path, help="folder for the vetting judge's sheet")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    base_text = BASE_SET.read_text(encoding="utf-8")
    base_rows = [json.loads(line) for line in base_text.splitlines() if line]
    base_turns = {json.dumps(r["turns"], ensure_ascii=False) for r in base_rows}
    base_ids = {r["id"] for r in base_rows}
    rows, items, tally = [], [], Counter()
    seed = FIRST_SEED
    while len(rows) < NEW_ROWS:
        seed += 1
        item = build_item(
            f"view/in_view_{len(rows):04d}",
            seed,
            SIZE,
            IN_VIEW,
            "train",
            decoys=1,
            more_indirect=True,
            more_chat=True,
            force_indirect=True,
        )
        fact_line = item.exchanges[item.fact_index][0]
        if any(four_grams(text) & TEST_GRAMS for text in (item.message, fact_line, item.reply)):
            tally["shares_test_wording"] += 1
            continue
        turns = demonstration_turns(item, "", item.reply, False, TRAIN.unknown_replies[0])
        if row_tokens(turns, tokenizer) > MAX_ROW_TOKENS:
            tally["too_long"] += 1
            continue
        if item.answer not in item.reply:
            raise SystemExit(f"{item.item_id}: the answer leaves out the value")
        if slip_shape(item.reply, item.message) or VOICE.search(item.reply):
            raise SystemExit(f"{item.item_id}: the answer fails the slip or voice check")
        if json.dumps(turns, ensure_ascii=False) in base_turns or item.item_id in base_ids:
            raise SystemExit(f"{item.item_id}: repeats a row of 6.31's")
        tally["kept"] += 1
        rows.append({"id": item.item_id, "kind": IN_VIEW, "turns": turns})
        items.append(item)
    added = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    FROM_SCRATCH.write_text(base_text + added, encoding="utf-8")
    if not FROM_SCRATCH.read_text(encoding="utf-8").startswith(base_text):
        raise SystemExit("6.31's rows changed")
    replayed = replay(base_rows)
    ON_TOP.write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in replayed) + added,
        encoding="utf-8",
    )
    if args.vet:
        args.vet.mkdir(parents=True, exist_ok=True)
        sheet = []
        for n, (item, row) in enumerate(zip(items, rows, strict=True)):
            chat = [f"{t['role'].upper()}: {t['content']}" for t in row["turns"][:-2]]
            sheet.append(
                f"ITEM {n}\n" + "\n".join(chat) + f"\nQUESTION: {item.message}\n"
                f"ANSWER: {row['turns'][-1]['content']}\n"
            )
        (args.vet / "items.txt").write_text("\n".join(sheet), encoding="utf-8")
    for out, kinds in ((FROM_SCRATCH, None), (ON_TOP, Counter(r["kind"] for r in replayed))):
        all_rows = [json.loads(line) for line in out.read_text(encoding="utf-8").splitlines()]
        report = {
            "provenance": run_metadata(),
            "base_set": BASE_SET.as_posix(),
            "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
            "out_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "rows": len(all_rows),
            "appended": len(rows),
            "replayed": dict(sorted(kinds.items())) if kinds else None,
            "statement_rows": sum(r["kind"] == "statement" for r in all_rows),
            "kinds": dict(sorted(Counter(r["kind"] for r in all_rows).items())),
            "tally": dict(sorted(tally.items())),
            "fact_types": dict(sorted(Counter(fact_type(i.answer) for i in items).items())),
        }
        out.with_suffix(".provenance.json").write_text(
            json.dumps(report, indent=1), encoding="utf-8"
        )
        print(f"{out}: {report['rows']} rows, kinds {report['kinds']}")
        print(f"sha256 {report['out_sha256']}")
    print(f"tally {dict(tally)}")


if __name__ == "__main__":
    main()
