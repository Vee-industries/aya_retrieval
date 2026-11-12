"""S3 evaluation (R-178): run one arm over the sealed set S3 in both views and record every reply.

Arms (each run is one arm):
- ``tool``: the model with the search tool, through the same loop as every earlier result
  (``run_recall_eval.run_arm``'s ``tool_loop``). With ``--adapter`` this is the adapter's arm;
  without it, base with the tool.
- ``always_search``: code that searches every turn with the message, then the model answers.
- ``whole_chat``: base with the whole chat in view and no tool (``whole_chat_all``).

S3 is sealed: the script refuses to run without ``--final``, checks the seal manifest before it
loads the model, and stops on any difference. Each row records the item's kind, view, queries,
search outputs, reply, ``item_correct``, and the model-free flags from ``aya_retrieval.heldout3``:
copy (wrong view, every kind but re_ask), N-hit (an OR search with the question's content words
returns at least one passage), false answer, and the fixed never-told rubric's model-free part.

Usage:
    python scripts/run_s3_eval.py --final --arm tool --index C:/scratch/s3.sqlite --label base_tool
    python scripts/run_s3_eval.py --final --arm tool --adapter PATH --index C:/scratch/s3.sqlite \
        --label k1_seed_82
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import logging
import time
from collections import Counter
from pathlib import Path

from aya_retrieval.harness import TurnResult
from aya_retrieval.heldout3 import (
    CHATS_DIR,
    NEVER_TOLD_RUBRIC,
    RE_ASK,
    SPLIT_FILE,
    S3Item,
    copy_flag,
    false_answer,
    load_s3,
    load_split,
    n_hit_query,
    never_told_right,
)
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact
from aya_retrieval.scoring import item_correct, right_decision

LOG = logging.getLogger("s3_eval")
SCRIPTS = Path(__file__).resolve().parent
MANIFEST = REPO_ROOT / "results" / "freeze" / "heldout3_manifest.json"
OUT_DIR = REPO_ROOT / "results" / "s3"
# This script's arm names and the names ``run_recall_eval.run_arm`` knows them by.
ARMS = {"tool": "tool_loop", "always_search": "always_search", "whole_chat": "whole_chat_all"}


def _load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def n_hit(tool, s3: S3Item) -> bool:
    """Model-free: True if an OR search with the message's content words returns a passage."""
    query = n_hit_query(s3.item.message)
    return bool(query) and bool(tool.backend.search(query, top_k=5))


def score_row(s3: S3Item, arm: str, result: TurnResult, tool) -> dict:
    """Return one results row for ``s3`` answered as ``result`` under ``arm``."""
    item, calls = s3.item, len(result.queries)
    outputs = []
    for query in result.queries:
        found = tool.execute(query)
        outputs.append(found.output if found.success else str(found.error))
    # A re-ask's fact is out of view, as an older fact's is.
    decision_kind = "older" if item.kind == RE_ASK else item.kind
    return {
        "id": item.item_id,
        "chat": s3.chat_id,
        "writer": s3.writer,
        "question": s3.question,
        "kind": item.kind,
        "variant": s3.variant,
        "claim": s3.claim,
        "category": s3.category,
        "inside": s3.inside,
        "view": s3.view,
        "arm": arm,
        "message": item.message,
        "answer": item.answer,
        "queries": result.queries,
        "search_outputs": outputs,
        "reply": result.reply,
        "transcript": result.transcript,
        "ran_out_of_calls": result.ran_out_of_calls,
        "item_correct": item_correct(item.kind, result.reply, item.answer, item.forbidden, calls)
        and not result.ran_out_of_calls,
        "right_decision": right_decision(decision_kind, calls),
        "found_fact": item.fact_index >= 0
        and any(search_finds_fact(tool, item, query) for query in result.queries),
        "copy": copy_flag(s3, result.reply),
        "n_hit": n_hit(tool, s3),
        "false_answer": false_answer(s3, result.reply),
        "never_told_right": never_told_right(s3, result.reply),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--arm", required=True, choices=sorted(ARMS))
    parser.add_argument("--adapter", type=Path, help="adapter to score; tool arm only")
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--label", required=True, help="names the results file")
    parser.add_argument("--items-dir", type=Path, default=CHATS_DIR)
    parser.add_argument("--split", type=Path, default=SPLIT_FILE)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--max-vram-fraction", type=float)
    parser.add_argument("--final", action="store_true", help="needed: S3 is sealed")
    args = parser.parse_args(argv)
    if not args.final:
        parser.error("S3 is sealed: this run needs --final")
    if args.adapter and args.arm != "tool":
        parser.error("--adapter goes with the tool arm only")
    return args


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    require_clean_tree()
    seal = _load_script("seal_s3", SCRIPTS / "records" / "seal_s3.py")
    changed = seal.check(args.manifest, args.items_dir)
    if changed:
        raise SystemExit("seal check failed; the run is void:\n" + "\n".join(changed))

    import torch
    from peft import PeftModel

    from aya_retrieval.inference import GREEDY, generate_from_messages, prompt_tokens
    from aya_retrieval.models import MODEL_ID, MODEL_REVISION, load_model
    from aya_retrieval.scoring import check_scorer

    recall_eval = _load_script("run_recall_eval", SCRIPTS / "run_recall_eval.py")
    check_scorer()
    items, dropped, batch, digest = load_s3(args.items_dir, load_split(args.split))
    report = {
        "provenance": run_metadata(),
        "record": "R-178",
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "adapter": str(args.adapter) if args.adapter else None,
        "arm": args.arm,
        "harness_arm": ARMS[args.arm],
        "max_tokens": recall_eval.MAX_TOKENS,
        "items_dir": args.items_dir.as_posix(),
        "items_sha256": digest,
        "manifest": args.manifest.as_posix(),
        "dropped": dropped,
        "batch_problems": batch,
        "never_told_rubric": NEVER_TOLD_RUBRIC,
        "rows": [],
    }
    started = time.time()
    if args.max_vram_fraction:
        torch.cuda.set_per_process_memory_fraction(args.max_vram_fraction)
    model, tokenizer = load_model()
    if args.adapter:
        model = PeftModel.from_pretrained(model, str(args.adapter))
        model.eval()
    spent = Counter()

    def generate(messages: list[dict]) -> str:
        reply = generate_from_messages(model, tokenizer, messages, GREEDY, recall_eval.MAX_TOKENS)
        spent["read"] += prompt_tokens(tokenizer, messages)
        spent["written"] += len(tokenizer.encode(reply, add_special_tokens=False))
        return reply

    for number, s3 in enumerate(items):
        tool = build_recall_tool(s3.item, args.index, match_all=False)
        spent.clear()
        result = recall_eval.run_arm(ARMS[args.arm], s3.item, generate, tool)
        row = score_row(s3, args.arm, result, tool)
        row |= {"tokens_read": spent["read"], "tokens_written": spent["written"]}
        report["rows"].append(row)
        if number % 50 == 0:
            LOG.info("%d of %d items, %d s", number, len(items), time.time() - started)

    report["peak_vram_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
    report["seconds"] = round(time.time() - started)
    args.index.unlink(missing_ok=True)
    out = OUT_DIR / f"{args.label}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    correct, total = Counter(), Counter()
    for row in report["rows"]:
        correct[(row["view"], row["kind"])] += row["item_correct"]
        total[(row["view"], row["kind"])] += 1
    for key in sorted(total):
        LOG.info("%s: %d of %d", key, correct[key], total[key])
    LOG.info("wrote %s, %d s", out, report["seconds"])


if __name__ == "__main__":
    main()
