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
import hashlib
import json
import logging
import time
from collections import Counter
from pathlib import Path

import torch
from peft import PeftModel

from aya_retrieval.conversations import ITEM_KINDS, OLDER, STATEMENT, build_item
from aya_retrieval.dev_set import load_dev_set
from aya_retrieval.harness import TurnResult, run_turn, turns_from
from aya_retrieval.inference import GREEDY, generate_from_messages, prompt_tokens
from aya_retrieval.models import MODEL_ID, MODEL_REVISION, load_model
from aya_retrieval.pools import POOLS, SEALED
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact
from aya_retrieval.scoring import check_scorer, item_correct, right_decision
from aya_retrieval.stress import (
    asked_before,
    corrected,
    corrected_heldout,
    phone_style,
    user_style,
)
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME, system_prompt_with_tools

LOG = logging.getLogger("recall_eval")

SIZES = (58, 419)
ARMS = (
    "whole_chat",
    "three_exchanges",
    "always_search",
    "tool_loop",
    "whole_chat_tool",
    "whole_chat_all",
)
MAX_TOKENS = 60
SYSTEM = "You are chatting with a friend."
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."


def run_arm(arm: str, item, generate, tool, with_tool: str = SYSTEM_WITH_TOOL) -> TurnResult:
    """Return one arm's result on one conversation; ``with_tool`` opens the tool arms' prompt."""

    def search(query: str) -> str:
        result = tool.execute(query)
        return result.output if result.success else str(result.error)

    if arm in ("whole_chat", "three_exchanges", "whole_chat_all"):  # _all: every kind (R-165)
        exchanges = item.view() if arm == "three_exchanges" else item.exchanges
        ask = {"role": "user", "content": item.message}
        reply = generate([{"role": "system", "content": SYSTEM}, *turns_from(exchanges), ask])
        return TurnResult(reply=reply, transcript=[reply])

    system = system_prompt_with_tools(with_tool)
    if arm == "always_search":
        call = json.dumps([{"tool_name": SEARCH_TOOL_NAME, "parameters": {"query": item.message}}])
        replies = iter([call])
        scripted = lambda messages: next(replies, None) or generate(messages)  # noqa: E731
        return run_turn(scripted, search, system, item.view(), item.message)
    if arm == "whole_chat_tool":  # R-165: every message in view and the tool offered
        return run_turn(generate, search, system, item.exchanges, item.message)
    return run_turn(generate, search, system, item.view(), item.message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--label", required=True, help="names the results file")
    parser.add_argument("--adapter", type=Path, help="adapter to score; omit for the base model")
    parser.add_argument(
        "--max-vram-fraction",
        type=float,
        help="cap this process's share of card memory, so the card never spills to system memory",
    )
    parser.add_argument("--arms", nargs="+", default=list(ARMS), choices=ARMS)
    parser.add_argument("--items-per-kind", type=int, default=12)
    parser.add_argument("--pool", default="train", choices=sorted(POOLS))
    parser.add_argument(
        "--decoys", type=int, default=1, help="same-type facts about other people in each chat"
    )
    parser.add_argument(
        "--sizes", type=int, nargs="+", default=list(SIZES), help="chat lengths, in messages"
    )
    parser.add_argument("--kinds", nargs="+", default=list(ITEM_KINDS), choices=ITEM_KINDS)
    parser.add_argument(
        "--user-style", action="store_true", help="friend lines typed as a real user types (R-067)"
    )
    parser.add_argument(
        "--phone-style",
        action="store_true",
        help="friend lines typed fast on a phone; held out of training (R-099)",
    )
    parser.add_argument(
        "--corrections",
        action="store_true",
        help="older and confirm facts corrected later, out of view (R-067)",
    )
    parser.add_argument(
        "--corrections-heldout",
        action="store_true",
        help="corrections in the held-out wordings, latest out-of-view slot (R-102)",
    )
    parser.add_argument(
        "--chat-check",
        type=Path,
        help="JSON list of chat lines; statement items take them in order (R-083)",
    )
    parser.add_argument(
        "--system-prompt-file",
        type=Path,
        help="text that replaces the tool arms' opening line, before the tool schema (R-137)",
    )
    parser.add_argument(
        "--asked-before",
        action="store_true",
        help="an earlier question, declined, as the newest exchange in view (R-081)",
    )
    parser.add_argument(
        "--items-dir",
        type=Path,
        help="score chats written blind to the generator instead of building items (R-139)",
    )
    parser.add_argument("--final", action="store_true", help="needed to read held-out items")
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    if args.pool in SEALED and not args.final:
        parser.error("sealed conversations need --final")
    changes = ("user_style", "phone_style", "corrections", "corrections_heldout", "asked_before")
    if args.items_dir and (args.chat_check or any(getattr(args, c) for c in changes)):
        parser.error("--items-dir scores the written chats as they are, with no changes")

    require_clean_tree(args.allow_dirty)
    check_scorer()
    report = {
        "provenance": run_metadata(),
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "adapter": str(args.adapter) if args.adapter else None,
        "seed": args.seed,
        "pool": args.pool,
        "decoys": args.decoys,
        "sizes": args.sizes,
        "kinds": args.kinds,
        "user_style": args.user_style,
        "phone_style": args.phone_style,
        "corrections": args.corrections,
        "corrections_heldout": args.corrections_heldout,
        "asked_before": args.asked_before,
        "chat_check": args.chat_check and args.chat_check.as_posix(),
        "rows": [],
    }
    if args.items_dir:
        written, dropped, digest = load_dev_set(args.items_dir)
        report |= {"items_dir": args.items_dir.as_posix(), "items_sha256": digest}
        report |= {"dropped": dropped, "pool": None, "sizes": None}
    with_tool = SYSTEM_WITH_TOOL
    if args.system_prompt_file:
        with_tool = args.system_prompt_file.read_text(encoding="utf-8").strip()
        report["system_prompt_file"] = args.system_prompt_file.as_posix()
        report["system_prompt_sha256"] = hashlib.sha256(with_tool.encode("utf-8")).hexdigest()

    started = time.time()
    if args.max_vram_fraction:
        # A full card spills into system memory and slows every step many times over (R-088).
        torch.cuda.set_per_process_memory_fraction(args.max_vram_fraction)
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

    check_lines = (
        [row["line"] for row in json.loads(args.chat_check.read_text(encoding="utf-8"))]
        if args.chat_check
        else []
    )

    def generated():
        """Yield (size, kind, item) for each item the generator builds, as earlier runs did."""
        for size_number, size in enumerate(args.sizes):
            for kind_number, kind in enumerate(ITEM_KINDS):
                if kind not in args.kinds:
                    continue
                for number in range(args.items_per_kind):
                    seed = args.seed + size * 1000 + kind_number * 100 + number
                    check = number + size_number * args.items_per_kind
                    item = build_item(
                        f"{size}_{kind}_{number:02d}",
                        seed,
                        size,
                        kind,
                        args.pool,
                        args.decoys,
                        chat_line=(check_lines[check % len(check_lines)], "")
                        if check_lines and kind == STATEMENT
                        else None,
                    )
                    if args.corrections:
                        item = corrected(item, seed, args.pool)
                    if args.corrections_heldout:
                        item = corrected_heldout(item, seed, args.pool)
                    if args.asked_before:
                        item = asked_before(item, seed, args.pool)
                    if args.user_style:
                        item = user_style(item, seed)
                    if args.phone_style:
                        item = phone_style(item, seed, args.pool)
                    yield size, kind, item
                LOG.info("%s %s done, %d s", size, kind, time.time() - started)

    # A written chat's size is its length in messages, as the generator's sizes are.
    source = ((2 * len(i.exchanges), i.kind, i) for i in written) if args.items_dir else generated()
    for size, kind, item in source:
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
            result = run_arm(arm, item, generate, tool, with_tool)
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
                        tool.execute(query).output.count("chunk_id=") for query in result.queries
                    ],
                    "tokens_read": spent["read"],
                    "tokens_written": spent["written"],
                    "whole_chat_tokens": whole_chat_tokens,
                    "ran_out_of_calls": result.ran_out_of_calls,
                    "first_reply": result.transcript[0],
                    "correct": item_correct(kind, result.reply, item.answer, item.forbidden, calls)
                    and not result.ran_out_of_calls,
                    "right_decision": right_decision(kind, calls),
                    "found_fact": any(
                        search_finds_fact(tool, item, query) for query in result.queries
                    ),
                }
            )

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
