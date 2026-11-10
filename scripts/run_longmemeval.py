"""LongMemEval-S outside check (R-170): run one arm on every question, or on a listed few.

Usage:
    python -I scripts/run_longmemeval.py --data C:/.../longmemeval_s_cleaned.json \
        --index C:/scratch/lme.sqlite --arm tool_loop --label lme_637_82_tool \
        --adapter C:/scratch/fix17cs37_82 --max-vram-fraction 0.8
    python -I scripts/run_longmemeval.py ... --arm tool_loop --label dry_637_82_tool \
        --ids-file results/analysis/R-170/dry_run_ids.json --allow-dirty

Why: R-170 registered five arms on LongMemEval-S, run one at a time: 6.37 seed 82 with the tool,
base with the tool, code that always searches first (its query is the question without the date),
base with three exchanges and no tool, and base reading only the evidence sessions (every message
in them in view, no tool) on questions whose evidence prompt is under 6,000 tokens. The tool arms
and the three-exchange arm are ``run_recall_eval.py``'s own: the same prompts, greedy decoding, 60
tokens a call and three calls. Each question is caught on its own, so an error (out of memory
included) is logged for that question and the run goes on. Nothing is scored here; the scorer is
``scripts/records/score_r170.py``. The results file is saved every 25 questions and says whether
the arm completed; R-170's hard stop (18:00 on 11 November) ends the arm as not completed.
Writes results/longmemeval/<label>.json.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

import torch
from peft import PeftModel

from aya_retrieval.harness import MAX_CALLS, TurnResult, run_turn, turns_from
from aya_retrieval.inference import GREEDY, generate_from_messages, prompt_tokens
from aya_retrieval.longmemeval import load_longmemeval
from aya_retrieval.models import MODEL_ID, MODEL_REVISION, load_model
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import TOP_K, build_search_tool
from aya_retrieval.scoring import check_scorer
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME, system_prompt_with_tools

sys.path.insert(0, str(Path(__file__).parent))
from run_recall_eval import MAX_TOKENS, SYSTEM, SYSTEM_WITH_TOOL, run_arm  # noqa: E402

LOG = logging.getLogger("longmemeval")

ARMS = ("tool_loop", "always_search", "three_exchanges", "evidence_only")
EVIDENCE_LIMIT = 6000  # R-170: evidence-only runs on prompts under this many tokens
HARD_STOP = "2026-11-11T18:00"  # R-170: an arm not finished by then is not completed
SAVE_EVERY = 25


def evidence_prompt(item) -> list[dict]:
    """Return the evidence-only arm's prompt: every message of the evidence sessions, no tool."""
    ask = {"role": "user", "content": item.message}
    return [{"role": "system", "content": SYSTEM}, *turns_from(item.evidence_exchanges), ask]


def run_question(arm: str, item, generate, tool) -> TurnResult:
    """Return one arm's result on one question."""

    def search(query: str) -> str:
        result = tool.execute(query)
        return result.output if result.success else str(result.error)

    if arm == "always_search":
        # As run_recall_eval's always_search, but the scripted query leaves the date out (R-170).
        query = {"tool_name": SEARCH_TOOL_NAME, "parameters": {"query": item.question}}
        replies = iter([json.dumps([query])])
        scripted = lambda messages: next(replies, None) or generate(messages)  # noqa: E731
        system = system_prompt_with_tools(SYSTEM_WITH_TOOL)
        return run_turn(scripted, search, system, item.view(), item.message)
    if arm == "evidence_only":
        reply = generate(evidence_prompt(item))
        return TurnResult(reply=reply, transcript=[reply])
    return run_arm(arm, item, generate, tool)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, required=True, help="longmemeval_s_cleaned.json")
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--arm", required=True, choices=ARMS)
    parser.add_argument("--label", required=True, help="names the results file")
    parser.add_argument("--adapter", type=Path, help="adapter to run; omit for the base model")
    parser.add_argument(
        "--ids-file",
        type=Path,
        help="JSON file with an 'ids' list: run only those questions (the dry run)",
    )
    parser.add_argument(
        "--max-vram-fraction",
        type=float,
        help="cap this process's share of card memory, so the card never spills to system memory",
    )
    parser.add_argument("--stop-at", default=HARD_STOP, help="local time the arm must end by")
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    require_clean_tree(args.allow_dirty)
    check_scorer()
    stop_at = datetime.fromisoformat(args.stop_at)
    items, digest = load_longmemeval(args.data)
    if args.ids_file:
        wanted = json.loads(args.ids_file.read_text(encoding="utf-8"))["ids"]
        known = {item.item_id: item for item in items}
        missing = [i for i in wanted if i not in known]
        if missing:
            parser.error(f"ids not in the data: {missing}")
        items = [known[i] for i in wanted]
    out = REPO_ROOT / "results" / "longmemeval" / f"{args.label}.json"
    report = {
        "provenance": run_metadata(),
        "record": "R-170",
        "data_sha256": digest,
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "adapter": str(args.adapter) if args.adapter else None,
        "arm": args.arm,
        "ids_file": args.ids_file and args.ids_file.as_posix(),
        "questions": len(items),
        "max_tokens": MAX_TOKENS,
        "completed": False,
        "rows": [],
    }

    def save() -> None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")

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

    for number, item in enumerate(items):
        if datetime.now() >= stop_at:
            LOG.info("hard stop %s reached: the arm is not completed", args.stop_at)
            report["stopped_at_hard_stop"] = True
            break
        row = {"id": item.item_id, "type": item.kind, "arm": args.arm}
        spent.clear()
        begun = time.time()
        try:
            if args.arm == "evidence_only":
                row["evidence_tokens"] = prompt_tokens(tokenizer, evidence_prompt(item))
                if row["evidence_tokens"] >= EVIDENCE_LIMIT:
                    row["skipped"] = f"evidence prompt of {EVIDENCE_LIMIT} tokens or more"
                    report["rows"].append(row)
                    continue
            tool = None
            if args.arm in ("tool_loop", "always_search"):
                tool = build_search_tool(item.older(), args.index, match_all=False)
            result = run_question(args.arm, item, generate, tool)
            # A query past the third is never run (harness.run_turn).
            hits = [tool.backend.search(q, top_k=TOP_K) for q in result.queries[:MAX_CALLS]]
            row |= {
                "reply": result.reply,
                "reply_tokens": len(tokenizer.encode(result.reply, add_special_tokens=False)),
                "first_reply": result.transcript[0],
                "queries": result.queries,
                "chunk_ids": [[h["metadata"]["chunk_id"] for h in hit] for hit in hits],
                "doc_ids": [[h["metadata"]["doc_id"] for h in hit] for hit in hits],
                "ran_out_of_calls": result.ran_out_of_calls,
                "error": None,
            }
        except Exception as error:  # R-170: each question is caught on its own
            if isinstance(error, torch.cuda.OutOfMemoryError):
                torch.cuda.empty_cache()
            row |= {"reply": None, "error": f"{type(error).__name__}: {error}"}
            LOG.info("%s failed: %s", item.item_id, row["error"])
        row |= {
            "tokens_read": spent["read"],
            "tokens_written": spent["written"],
            "seconds": round(time.time() - begun, 2),
        }
        report["rows"].append(row)
        if (number + 1) % SAVE_EVERY == 0:
            save()
            LOG.info("%d of %d, %d s", number + 1, len(items), time.time() - started)
    else:
        report["completed"] = True

    report["failures"] = sum(bool(row.get("error")) for row in report["rows"])
    report["peak_vram_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
    report["seconds"] = round(time.time() - started)
    args.index.unlink(missing_ok=True)
    save()
    LOG.info(
        "wrote %s: %d rows, %d failures, completed %s, peak VRAM %.2f GiB, %d s",
        out,
        len(report["rows"]),
        report["failures"],
        report["completed"],
        report["peak_vram_gib"],
        report["seconds"],
    )


if __name__ == "__main__":
    main()
