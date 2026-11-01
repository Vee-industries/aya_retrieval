"""Recall evaluation: score base, and optionally an adapter, on long conversations.

Every arm sees the same conversations. Tool arms run the real loop in ``harness.py``, so the model
decides for itself. ``heldout`` conversations need ``--final``, so nobody looks at them by accident.

Usage:
    python scripts/run_recall_eval.py --seed 1234 --index C:/scratch/eval.sqlite --label base
    python scripts/run_recall_eval.py --seed 1234 --index C:/scratch/eval.sqlite \
        --label tuned --arms tool_loop --adapter C:/scratch/recall_adapter
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from collections import Counter
from pathlib import Path

import torch
from peft import PeftModel

from aya_retrieval.conversations import ITEM_KINDS, OLDER, build_item
from aya_retrieval.harness import TurnResult, run_turn, turns_from
from aya_retrieval.inference import GREEDY, generate_from_messages, prompt_tokens
from aya_retrieval.models import MODEL_ID, MODEL_REVISION, load_model
from aya_retrieval.pools import POOLS
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact
from aya_retrieval.scoring import check_scorer, item_correct, right_decision
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME, system_prompt_with_tools

LOG = logging.getLogger("recall_eval")

SIZES = (58, 419)
ARMS = ("whole_chat", "three_exchanges", "always_search", "tool_loop")
MAX_TOKENS = 60
SYSTEM = "You are chatting with a friend."
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."


def run_arm(arm: str, item, generate, tool) -> TurnResult:
    """Return one arm's result on one conversation."""

    def search(query: str) -> str:
        result = tool.execute(query)
        return result.output if result.success else str(result.error)

    if arm in ("whole_chat", "three_exchanges"):
        exchanges = item.exchanges if arm == "whole_chat" else item.view()
        ask = {"role": "user", "content": item.message}
        reply = generate([{"role": "system", "content": SYSTEM}, *turns_from(exchanges), ask])
        return TurnResult(reply=reply, transcript=[reply])

    system = system_prompt_with_tools(SYSTEM_WITH_TOOL)
    if arm == "always_search":
        call = json.dumps([{"tool_name": SEARCH_TOOL_NAME, "parameters": {"query": item.message}}])
        replies = iter([call])
        scripted = lambda messages: next(replies, None) or generate(messages)  # noqa: E731
        return run_turn(scripted, search, system, item.view(), item.message)
    return run_turn(generate, search, system, item.view(), item.message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--label", required=True, help="names the results file")
    parser.add_argument("--adapter", type=Path, help="adapter to score; omit for the base model")
    parser.add_argument("--arms", nargs="+", default=list(ARMS), choices=ARMS)
    parser.add_argument("--items-per-kind", type=int, default=12)
    parser.add_argument("--pool", default="train", choices=sorted(POOLS))
    parser.add_argument("--final", action="store_true", help="needed to read held-out items")
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    if args.pool == "heldout" and not args.final:
        parser.error("held-out conversations need --final")

    require_clean_tree(args.allow_dirty)
    check_scorer()
    report = {
        "provenance": run_metadata(),
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "adapter": str(args.adapter) if args.adapter else None,
        "seed": args.seed,
        "pool": args.pool,
        "rows": [],
    }

    started = time.time()
    model, tokenizer = load_model()
    if args.adapter:
        model = PeftModel.from_pretrained(model, str(args.adapter))
        model.eval()

    spent = Counter()

    def generate(messages: list[dict]) -> str:
        reply = generate_from_messages(model, tokenizer, messages, GREEDY, MAX_TOKENS)
        spent["read"] += prompt_tokens(tokenizer, messages)
        spent["written"] += len(tokenizer.encode(reply, add_special_tokens=False))
        return reply

    for size in SIZES:
        for kind_number, kind in enumerate(ITEM_KINDS):
            for number in range(args.items_per_kind):
                seed = args.seed + size * 1000 + kind_number * 100 + number
                item = build_item(f"{size}_{kind}_{number:02d}", seed, size, kind, args.pool)
                tool = build_recall_tool(item, args.index, match_all=False)
                ask = {"role": "user", "content": item.message}
                whole_chat = [
                    {"role": "system", "content": SYSTEM},
                    *turns_from(item.exchanges),
                    ask,
                ]
                whole_chat_tokens = prompt_tokens(tokenizer, whole_chat)
                for arm in args.arms:
                    if arm == "whole_chat" and kind != OLDER:
                        continue
                    spent.clear()
                    result = run_arm(arm, item, generate, tool)
                    calls = len(result.queries)
                    report["rows"].append(
                        {
                            "id": item.item_id,
                            "size": size,
                            "kind": kind,
                            "arm": arm,
                            "message": item.message,
                            "view": item.view(),
                            "answer": item.answer,
                            "reply": result.reply,
                            "queries": result.queries,
                            "passages": [
                                tool.execute(query).output.count("chunk_id=")
                                for query in result.queries
                            ],
                            "tokens_read": spent["read"],
                            "tokens_written": spent["written"],
                            "whole_chat_tokens": whole_chat_tokens,
                            "ran_out_of_calls": result.ran_out_of_calls,
                            "first_reply": result.transcript[0],
                            "correct": item_correct(
                                kind, result.reply, item.answer, item.forbidden, calls
                            )
                            and not result.ran_out_of_calls,
                            "right_decision": right_decision(kind, calls),
                            "found_fact": any(
                                search_finds_fact(tool, item, query) for query in result.queries
                            ),
                        }
                    )
            LOG.info("%s %s done, %d s", size, kind, time.time() - started)

    report["peak_vram_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
    report["seconds"] = round(time.time() - started)
    args.index.unlink(missing_ok=True)
    out = REPO_ROOT / "results" / "recall_eval" / f"{args.label}_seed_{args.seed}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")

    correct, total = Counter(), Counter()
    for row in report["rows"]:
        key = (row["arm"], row["size"], row["kind"])
        correct[key] += row["correct"]
        total[key] += 1
    for key in sorted(total):
        LOG.info("%s: %d of %d", key, correct[key], total[key])
    LOG.info("wrote %s, peak VRAM %.2f GiB, %d s", out, report["peak_vram_gib"], report["seconds"])


if __name__ == "__main__":
    main()
