"""Build the recall training set: demonstrations on the train pool, with base's own plain replies.

About 10 minutes on an RTX 3080. Writes ``data/recall_train.jsonl`` and a provenance file beside it.

Usage:
    python scripts/run_build_training_set.py --seed 1234 --rows-per-kind 150 \
        --index C:/scratch/train.sqlite
"""

from __future__ import annotations

import argparse
import json
import logging
import random
from collections import Counter
from pathlib import Path

from aya_retrieval.conversations import ITEM_KINDS, NEEDS_SEARCH, RecallItem, build_item
from aya_retrieval.demonstrations import demonstration_turns
from aya_retrieval.harness import turns_from
from aya_retrieval.inference import GREEDY, generate_from_messages
from aya_retrieval.models import load_model
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact
from aya_retrieval.scoring import item_correct
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME

LOG = logging.getLogger("build_training_set")

OUT_PATH = REPO_ROOT / "data" / "recall_train.jsonl"
SYSTEM = "You are chatting with a friend."
MAX_TOKENS = 60
SIZE = 58


def base_reply(model, tokenizer, item: RecallItem) -> str | None:
    """Return base's reply with no tool in sight, or None if it is not fit to copy."""
    messages = [
        {"role": "system", "content": SYSTEM},
        *turns_from(item.view()),
        {"role": "user", "content": item.message},
    ]
    reply = generate_from_messages(model, tokenizer, messages, GREEDY, MAX_TOKENS)
    if SEARCH_TOOL_NAME in reply:
        return None
    if not item_correct(item.kind, reply, item.answer, item.forbidden, calls=0):
        return None
    return reply


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--rows-per-kind", type=int, default=150)
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    require_clean_tree(args.allow_dirty)
    report = {"provenance": run_metadata(), "seed": args.seed}
    rng = random.Random(args.seed)
    model, tokenizer = load_model()

    rows, tally = [], Counter()
    for kind in ITEM_KINDS:
        made = attempt = 0
        while made < args.rows_per_kind:
            seed, attempt = args.seed + kind_seed_offset(kind) + attempt, attempt + 1
            item = build_item(f"{kind}_{made:04d}", seed, SIZE, kind, "train")
            if kind in NEEDS_SEARCH:
                tool = build_recall_tool(item, args.index, match_all=False)
                output = tool.execute(item.query).output
                found = search_finds_fact(tool, item, item.query)
                tally[f"{kind}_found" if found else f"{kind}_missed"] += 1
                reply = ""
            else:
                reply, output, found = base_reply(model, tokenizer, item), "", False
                if reply is None:
                    tally[f"{kind}_base_reply_rejected"] += 1
                    continue
            turns = demonstration_turns(
                item, output, reply, found, rng.choice(TRAIN.unknown_replies)
            )
            rows.append({"id": item.item_id, "kind": kind, "turns": turns})
            made += 1
        LOG.info("%s done after %d attempts", kind, attempt)

    args.index.unlink(missing_ok=True)
    lines = (json.dumps(row, ensure_ascii=False) for row in rows)
    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report["rows"] = len(rows)
    report["tally"] = dict(tally)
    provenance_path = OUT_PATH.with_suffix(".provenance.json")
    provenance_path.write_text(json.dumps(report, indent=1), encoding="utf-8")
    LOG.info("wrote %d rows: %s", len(rows), dict(tally))


def kind_seed_offset(kind: str) -> int:
    """Return a fixed seed offset per kind, so kinds use separate conversations."""
    return (ITEM_KINDS.index(kind) + 1) * 100_000


if __name__ == "__main__":
    main()
