"""Measure generation speed for the cost comparison: one model call at several batch sizes.

Each prompt is a real probe conversation as the tool loop presents it (system prompt with the tool,
the last three exchanges, the friend's message), so prompts are the length the adapter actually
reads. Each call writes a fixed number of new tokens, the length of a typical reply. The adapter is
merged into the weights first, as a server would run it.

Usage:
    python scripts/run_throughput.py --adapter <adapter dir> --name v4_seed_82
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path

import torch
from peft import PeftModel

from aya_retrieval.conversations import ITEM_KINDS, build_item
from aya_retrieval.harness import turns_from
from aya_retrieval.models import MODEL_ID, MODEL_REVISION, load_model
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.tool_prompt import system_prompt_with_tools

LOG = logging.getLogger("throughput")
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."
OUT_DIR = REPO_ROOT / "results" / "throughput"


def prompts(count: int, probe_seed: int) -> list[list[dict]]:
    """Tool-loop prompts from probe conversations, both lengths and every kind in turn."""
    system = {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)}
    out = []
    for n in range(count):
        size = (58, 419)[n % 2]
        kind = ITEM_KINDS[(n // 2) % len(ITEM_KINDS)]
        item = build_item(f"t{n}", probe_seed + n, size, kind, "probe")
        out.append([system, *turns_from(item.view()), {"role": "user", "content": item.message}])
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--adapter", type=Path, required=True)
    parser.add_argument("--name", required=True, help="names the results file")
    parser.add_argument("--batch-sizes", type=int, nargs="+", default=[1, 4, 8, 16])
    parser.add_argument("--new-tokens", type=int, default=32, help="tokens written per call")
    parser.add_argument("--rounds", type=int, default=3, help="timed batches per batch size")
    parser.add_argument("--probe-seed", type=int, default=73157)
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    require_clean_tree(args.allow_dirty)

    model, tokenizer = load_model()
    model = PeftModel.from_pretrained(model, str(args.adapter)).merge_and_unload()
    model.eval()
    tokenizer.padding_side = "left"
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    pool = prompts(max(args.batch_sizes) * (args.rounds + 1), args.probe_seed)
    texts = [
        tokenizer.apply_chat_template(p, tokenize=False, add_generation_prompt=True) for p in pool
    ]

    report = {
        "provenance": run_metadata(),
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "adapter": str(args.adapter),
        "gpu": torch.cuda.get_device_name(0),
        "new_tokens": args.new_tokens,
        "rounds": args.rounds,
        "batches": [],
    }
    for batch in args.batch_sizes:
        timings, prompt_tokens = [], []
        for r in range(args.rounds + 1):  # the first round warms up and is not counted
            chunk = texts[r * batch : (r + 1) * batch]
            enc = tokenizer(chunk, return_tensors="pt", padding=True, add_special_tokens=False).to(
                0
            )
            torch.cuda.synchronize()
            start = time.perf_counter()
            with torch.no_grad():
                model.generate(
                    **enc,
                    do_sample=False,
                    max_new_tokens=args.new_tokens,
                    min_new_tokens=args.new_tokens,
                    pad_token_id=tokenizer.pad_token_id,
                )
            torch.cuda.synchronize()
            if r:
                timings.append(time.perf_counter() - start)
                prompt_tokens.append(int(enc["attention_mask"].sum()) / batch)
        seconds = sum(timings) / len(timings)
        row = {
            "batch_size": batch,
            "seconds_per_batch": round(seconds, 3),
            "mean_prompt_tokens": round(sum(prompt_tokens) / len(prompt_tokens)),
            "calls_per_hour": round(3600 * batch / seconds),
            "peak_vram_gib": round(torch.cuda.max_memory_allocated() / 2**30, 2),
        }
        report["batches"].append(row)
        LOG.info("%s", row)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{args.name}.json"
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    LOG.info("wrote %s", out)


if __name__ == "__main__":
    main()
