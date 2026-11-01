"""First test: does base Tiny Aya call the search tool, and does it tell lookups from statements?

Runs the items in ``data/first_test_items.jsonl`` through two system prompts, greedily and with
sampling, and writes every reply with its provenance. Takes about 13 minutes on an RTX 3080.

Usage:
    python scripts/run_first_test.py --seed 1234
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path

import torch

from aya_retrieval.models import MODEL_ID, MODEL_REVISION, load_model
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.scoring import check_scorer, search_counts, searched
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME, system_prompt_with_tools

LOG = logging.getLogger("first_test")

ITEMS_PATH = REPO_ROOT / "data" / "first_test_items.jsonl"
SAMPLING = {"do_sample": True, "temperature": 0.7, "top_p": 0.95}
SYSTEM_PROMPTS = {
    "neutral": (
        "You are the assistant for staff at Harbourline Logistics. "
        "You can search the company handbook."
    ),
    "agenttune_default": (
        f"You are a research assistant. Call the `{SEARCH_TOOL_NAME}` tool to find relevant "
        "passages before answering. Cite the chunk_id you relied on, and put your final "
        "answer in <answer></answer> tags."
    ),
}


def generate_reply(model, tokenizer, system: str, user: str, options: dict, max_tokens: int) -> str:
    """Return the model's reply to one user message."""
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt", return_dict=True
    ).to(model.device)
    with torch.no_grad():
        output = model.generate(
            **inputs, max_new_tokens=max_tokens, pad_token_id=tokenizer.eos_token_id, **options
        )
    reply_tokens = output[0][inputs["input_ids"].shape[1] :]
    return tokenizer.decode(reply_tokens, skip_special_tokens=True).strip()


def run_arm(model, tokenizer, system: str, items: list[dict], samples: int, max_tokens: int):
    """Return the scored greedy and sampled rows for one system prompt."""
    greedy, sampled = [], []
    for item in items:
        reply = generate_reply(
            model, tokenizer, system, item["text"], {"do_sample": False}, max_tokens
        )
        greedy.append({**item, "reply": reply, "searched": searched(reply)})
        for _ in range(samples):
            reply = generate_reply(model, tokenizer, system, item["text"], SAMPLING, max_tokens)
            sampled.append({**item, "reply": reply, "searched": searched(reply)})
    return greedy, sampled


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--samples", type=int, default=3, help="sampled replies per item")
    parser.add_argument("--max-new-tokens", type=int, default=80)
    parser.add_argument("--out-dir", type=Path, default=REPO_ROOT / "results" / "first_test")
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
        "arms": {},
    }

    lines = ITEMS_PATH.read_text(encoding="utf-8").splitlines()
    items = [json.loads(line) for line in lines]
    started = time.time()
    model, tokenizer = load_model()
    torch.manual_seed(args.seed)

    for arm, system_prompt in SYSTEM_PROMPTS.items():
        system = system_prompt_with_tools(system_prompt)
        greedy, sampled = run_arm(
            model, tokenizer, system, items, args.samples, args.max_new_tokens
        )
        report["arms"][arm] = {
            "greedy": search_counts(greedy),
            "sampled": search_counts(sampled),
            "greedy_rows": greedy,
            "sampled_rows": sampled,
        }
        LOG.info("%s greedy %s sampled %s", arm, search_counts(greedy), search_counts(sampled))

    report["peak_vram_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
    report["seconds"] = round(time.time() - started)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / f"seed_{args.seed}.json"
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    LOG.info("wrote %s, peak VRAM %.2f GiB, %d s", out, report["peak_vram_gib"], report["seconds"])


if __name__ == "__main__":
    main()
