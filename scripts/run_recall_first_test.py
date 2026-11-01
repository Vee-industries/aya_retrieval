"""Recall first test: what can base Tiny Aya do on facts outside its view, with no training?

Measures how often plain search finds the fact, then runs base in three arms on the same long
conversations: the whole chat in view, three exchanges with nothing else, and three exchanges with
code searching the user's message and handing back the result. About 15 minutes on an RTX 3080.

Usage:
    python scripts/run_recall_first_test.py --seed 1234 --index C:/scratch/recall.sqlite
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path

import torch

from aya_retrieval.conversations import RecallItem, build_item
from aya_retrieval.inference import GREEDY, generate_from_messages
from aya_retrieval.models import MODEL_ID, MODEL_REVISION, load_model
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact
from aya_retrieval.scoring import answer_correct, check_scorer
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME, system_prompt_with_tools

LOG = logging.getLogger("recall_first_test")

SIZES = (58, 419)
ITEMS_PER_WORDING = 20
MAX_TOKENS = 60
SYSTEM = "You are chatting with a friend."
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."
TOOL_RESULT = "Tool result for {name}: {content}\nUse this result to answer the original question."


def as_turns(exchanges) -> list[dict]:
    """Return exchanges as chat turns."""
    turns = []
    for user, assistant in exchanges:
        turns += [{"role": "user", "content": user}, {"role": "assistant", "content": assistant}]
    return turns


def arm_messages(arm: str, item: RecallItem, tool) -> list[dict]:
    """Return the prompt for one arm, as AgentTune's rollout would render a tool result."""
    ask = {"role": "user", "content": item.question}
    if arm == "whole_chat":
        return [{"role": "system", "content": SYSTEM}, *as_turns(item.exchanges), ask]
    if arm == "three_exchanges":
        return [{"role": "system", "content": SYSTEM}, *as_turns(item.view()), ask]
    call = json.dumps([{"tool_name": SEARCH_TOOL_NAME, "parameters": {"query": item.question}}])
    result = tool.execute(item.question)
    content = result.output if result.success else result.error
    return [
        {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)},
        *as_turns(item.view()),
        ask,
        {"role": "assistant", "content": call},
        {"role": "user", "content": TOOL_RESULT.format(name=SEARCH_TOOL_NAME, content=content)},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    require_clean_tree(args.allow_dirty)
    check_scorer()
    report = {
        "provenance": run_metadata(),
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "seed": args.seed,
        "hit_rate": {},
        "rows": [],
    }

    items = []
    for size in SIZES:
        for wording, shares_words in (("same_words", True), ("new_words", False)):
            for number in range(ITEMS_PER_WORDING):
                item_id = f"{size}_{wording}_{number:02d}"
                seed = args.seed + size + number * 2 + int(shares_words)
                items.append((size, wording, build_item(item_id, seed, size, shares_words)))

    for match_all, mode in ((True, "and"), (False, "or")):
        for size in SIZES:
            for wording in ("same_words", "new_words"):
                chosen = [i for s, w, i in items if s == size and w == wording]
                hits = sum(
                    search_finds_fact(
                        build_recall_tool(item, args.index, match_all), item, item.question
                    )
                    for item in chosen
                )
                report["hit_rate"][f"{mode}_{size}_{wording}"] = {"hits": hits, "of": len(chosen)}
    LOG.info("hit rate %s", report["hit_rate"])

    started = time.time()
    model, tokenizer = load_model()
    for size, wording, item in items:
        tool = build_recall_tool(item, args.index, match_all=False)
        for arm in ("whole_chat", "three_exchanges", "always_search"):
            messages = arm_messages(arm, item, tool)
            reply = generate_from_messages(model, tokenizer, messages, GREEDY, MAX_TOKENS)
            report["rows"].append(
                {
                    "id": item.item_id,
                    "size": size,
                    "wording": wording,
                    "arm": arm,
                    "question": item.question,
                    "answer": item.answer,
                    "decoy": item.decoy,
                    "reply": reply,
                    "correct": answer_correct(reply, item.answer, item.decoy),
                }
            )

    report["peak_vram_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
    report["seconds"] = round(time.time() - started)
    args.index.unlink(missing_ok=True)
    out = REPO_ROOT / "results" / "recall_first_test" / f"seed_{args.seed}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")

    for arm in ("whole_chat", "three_exchanges", "always_search"):
        for size in SIZES:
            for wording in ("same_words", "new_words"):
                chosen = [
                    row
                    for row in report["rows"]
                    if (row["arm"], row["size"], row["wording"]) == (arm, size, wording)
                ]
                correct = sum(row["correct"] for row in chosen)
                LOG.info("%s %s %s: %d of %d", arm, size, wording, correct, len(chosen))
    LOG.info("wrote %s, peak VRAM %.2f GiB", out, report["peak_vram_gib"])


if __name__ == "__main__":
    main()
