"""Build the recall training set: demonstrations on the train pool, with base's own plain replies.

About 20 minutes on an RTX 3080. Writes ``data/recall_train.jsonl`` and a provenance file beside it.

Usage:
    python scripts/run_build_training_set.py --seed 1234 --index C:/scratch/train.sqlite
"""

from __future__ import annotations

import argparse
import json
import logging
import random
from collections import Counter, defaultdict
from pathlib import Path

from agenttune.agentic.rollout_engines.rollout_factory import DEFAULT_TOOL_RESULT_FORMAT

from aya_retrieval.conversations import (
    CONFIRM,
    IN_VIEW,
    ITEM_KINDS,
    NEEDS_SEARCH,
    NEVER_TOLD,
    OLDER,
    STATEMENT,
    RecallItem,
    build_item,
)
from aya_retrieval.demonstrations import demonstration_turns, search_call, whole_sentences
from aya_retrieval.harness import turns_from
from aya_retrieval.inference import GREEDY, generate_from_messages
from aya_retrieval.models import load_model
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact
from aya_retrieval.scoring import item_correct
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME, system_prompt_with_tools

LOG = logging.getLogger("build_training_set")

OUT_PATH = REPO_ROOT / "data" / "recall_train.jsonl"
SYSTEM = "You are chatting with a friend."
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."
MAX_TOKENS = 60
SIZE = 58
ROWS_PER_KIND = {OLDER: 200, CONFIRM: 150, NEVER_TOLD: 150, IN_VIEW: 150, STATEMENT: 150}
MAX_ROW_TOKENS = 1024
# Found and not-found rows must return the same numbers of passages, or the count gives the answer.
DECOY_CHOICES = {
    OLDER: (0, 1, 2),
    CONFIRM: (0, 1, 2),
    NEVER_TOLD: (1, 2, 3),
    IN_VIEW: (1,),
    STATEMENT: (1,),
}


def fit_to_copy(model, tokenizer, item: RecallItem, messages: list[dict]) -> str | None:
    """Return base's whole-sentence reply to ``messages``, or None if it is not fit to copy."""
    reply = whole_sentences(generate_from_messages(model, tokenizer, messages, GREEDY, MAX_TOKENS))
    if reply is None or SEARCH_TOOL_NAME in reply:
        return None
    if not item_correct(item.kind, reply, item.answer, item.forbidden, calls=0):
        return None
    return reply


def base_reply(model, tokenizer, item: RecallItem) -> str | None:
    """Return base's reply with no tool in sight, or None if it is not fit to copy."""
    messages = [
        {"role": "system", "content": SYSTEM},
        *turns_from(item.view()),
        {"role": "user", "content": item.message},
    ]
    return fit_to_copy(model, tokenizer, item, messages)


def base_answer(model, tokenizer, item: RecallItem, output: str) -> str | None:
    """Return base's reply to a real search result, or None if it is not fit to copy."""
    messages = [
        {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)},
        *turns_from(item.view()),
        {"role": "user", "content": item.message},
        {"role": "assistant", "content": search_call(item.query)},
        {
            "role": "user",
            "content": DEFAULT_TOOL_RESULT_FORMAT.format(name=SEARCH_TOOL_NAME, content=output),
        },
    ]
    return fit_to_copy(model, tokenizer, item, messages)


def hinted_reply(model, tokenizer, item: RecallItem) -> str | None:
    """Return base's reply with the fact restated in the system prompt, or None if not fit to copy.

    For `in_view` items base answered wrong. The training row leaves the hint out, so the adapter
    learns to read the fact from the turns in view rather than to search for it.
    """
    fact = item.exchanges[item.fact_index][0]
    messages = [
        {"role": "system", "content": f'{SYSTEM} Earlier your friend said: "{fact}"'},
        *turns_from(item.view()),
        {"role": "user", "content": item.message},
    ]
    return fit_to_copy(model, tokenizer, item, messages)


def longest_row(rows: list[dict], tokenizer) -> int:
    """Return the token length of the longest row as training will see it."""
    system = {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)}
    return max(
        len(
            tokenizer.apply_chat_template([system, *row["turns"]], tokenize=True, return_dict=True)[
                "input_ids"
            ]
        )
        for row in rows
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--out", type=Path, default=OUT_PATH, help="training rows, .jsonl")
    parser.add_argument(
        "--read-hint", action="store_true", help="keep in_view items base got wrong, via a hint"
    )
    parser.add_argument(
        "--hard-in-view",
        type=int,
        default=0,
        help="in_view rows kept for items base got wrong; needs --read-hint",
    )
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    if args.hard_in_view and not args.read_hint:
        parser.error("--hard-in-view needs --read-hint")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    require_clean_tree(args.allow_dirty)
    report = {
        "provenance": run_metadata(),
        "seed": args.seed,
        "read_hint": args.read_hint,
        "hard_in_view": args.hard_in_view,
    }
    rng = random.Random(args.seed)
    model, tokenizer = load_model()

    rows, tally, passages = [], Counter(), defaultdict(Counter)
    for kind in ITEM_KINDS:
        made = attempt = 0
        while made < ROWS_PER_KIND[kind]:
            seed, attempt = args.seed + kind_seed_offset(kind) + attempt, attempt + 1
            decoys = rng.choice(DECOY_CHOICES[kind])
            item = build_item(f"{kind}_{made:04d}", seed, SIZE, kind, "train", decoys)
            if kind in NEEDS_SEARCH:
                tool = build_recall_tool(item, args.index, match_all=False)
                output = tool.execute(item.query).output
                found = search_finds_fact(tool, item, item.query)
                tally[f"{kind}_found" if found else f"{kind}_missed"] += 1
                passages[kind][output.count("chunk_id=")] += 1
                reply = item.reply
                if found and kind != NEVER_TOLD:
                    reply = base_answer(model, tokenizer, item, output)
                    tally[f"{kind}_base_answer" if reply else f"{kind}_scripted_answer"] += 1
                    reply = reply or item.reply
            else:
                reply, output, found = base_reply(model, tokenizer, item), "", False
                if reply and kind == IN_VIEW and easy_full(tally, args.hard_in_view):
                    tally[f"{kind}_easy_skipped"] += 1
                    continue
                if reply is None and args.read_hint and kind == IN_VIEW:
                    reply = hinted_reply(model, tokenizer, item)
                    tally[f"{kind}_hinted_reply" if reply else f"{kind}_hinted_reply_rejected"] += 1
                elif reply and kind == IN_VIEW:
                    tally[f"{kind}_base_reply"] += 1
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
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report["rows"] = len(rows)
    report["tally"] = dict(tally)
    report["passages_per_kind"] = {kind: dict(counts) for kind, counts in passages.items()}
    report["longest_row_tokens"] = longest_row(rows, tokenizer)
    if report["longest_row_tokens"] > MAX_ROW_TOKENS:
        raise SystemExit(f"a row exceeds {MAX_ROW_TOKENS} tokens, so training would cut its answer")
    provenance_path = args.out.with_suffix(".provenance.json")
    provenance_path.write_text(json.dumps(report, indent=1), encoding="utf-8")
    LOG.info("wrote %d rows: %s", len(rows), {**tally, **report["passages_per_kind"]})


def easy_full(tally: Counter, hard_rows: int) -> bool:
    """Return True once `in_view` rows base answered unaided fill the share left for hard rows."""
    return tally[f"{IN_VIEW}_base_reply"] >= ROWS_PER_KIND[IN_VIEW] - hard_rows


def kind_seed_offset(kind: str) -> int:
    """Return a fixed seed offset per kind, so kinds use separate conversations."""
    return (ITEM_KINDS.index(kind) + 1) * 100_000


if __name__ == "__main__":
    main()
