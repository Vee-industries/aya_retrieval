"""Ten GRPO steps on Tiny Aya: does the AgentTune to AuditKIT chain run, and does anything train?

The reward and data are stand-ins, so this checks the plumbing and yields no behavioural result.
Takes about 11 minutes on an RTX 3080. Model output and the search index go outside the repository.

Usage:
    python scripts/run_grpo_smoke.py --out-dir C:/scratch/smoke --index C:/scratch/smoke.sqlite
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import torch
from agenttune import create_rag_trainer
from auditkit.agent_eval import episodes_from_agenttune

from aya_retrieval.models import load_model
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME
from aya_retrieval.training_checks import adapter_moved

LOG = logging.getLogger("grpo_smoke")

SYSTEM_PROMPT = (
    "You are the assistant for staff at Bluewater Freight. You can search the company handbook."
)

CORPUS = [
    {
        "doc_id": "pay",
        "title": "Pay",
        "text": "Pay runs every second Friday. Late timesheets move to the next run.",
    },
    {
        "doc_id": "leave",
        "title": "Leave",
        "text": "Sick leave requests go to the shift lead before the shift starts.",
    },
    {
        "doc_id": "gear",
        "title": "Gear",
        "text": "Steel-toe boots are replaced once a year at the depot store.",
    },
    {
        "doc_id": "yard",
        "title": "Yard",
        "text": "The yard speed limit is 15 km/h. Reversing needs a spotter.",
    },
]

ROWS = [
    {"prompt": "when does pay run", "answer": "every second Friday", "kind": "lookup"},
    {"prompt": "Who do I tell if I am sick?", "answer": "the shift lead", "kind": "lookup"},
    {"prompt": "how often do we get new boots", "answer": "once a year", "kind": "lookup"},
    {"prompt": "What is the speed limit in the yard?", "answer": "15 km/h", "kind": "lookup"},
    {"prompt": "my pay came in late", "answer": "", "kind": "statement"},
    {"prompt": "I was off sick on Monday.", "answer": "", "kind": "statement"},
    {"prompt": "my boots are falling apart", "answer": "", "kind": "statement"},
    {"prompt": "I had to reverse across the whole yard today.", "answer": "", "kind": "statement"},
]


def searched_when_it_should(completions, kind, **_):
    """Reward 1 when the rollout's search matches the row's kind, else 0."""
    return [
        float((SEARCH_TOOL_NAME in str(completion)) == (row_kind == "lookup"))
        for completion, row_kind in zip(completions, kind, strict=True)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--steps", type=int, default=10)
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    require_clean_tree(args.allow_dirty)
    report = {"provenance": run_metadata()}
    model, tokenizer = load_model()

    trainer = create_rag_trainer(
        model=model,
        processing_class=tokenizer,
        train_dataset=ROWS,
        corpus=CORPUS,
        db_path=str(args.index),
        algorithm="grpo",
        backend="trl",
        reward_funcs=[searched_when_it_should],
        reward_weights=[1.0],
        system_prompt=SYSTEM_PROMPT,
        output_dir=str(args.out_dir),
        max_steps=args.steps,
        per_device_train_batch_size=2,
        gradient_accumulation_steps=1,
        num_generations=2,
        max_completion_length=96,
        max_steps_per_turn=2,
        learning_rate=1e-5,
        beta=0.0,
        gradient_checkpointing=True,
        use_vllm=False,
        peft_config=dict(r=16, lora_alpha=32, target_modules="all-linear", task_type="CAUSAL_LM"),
        report_to="none",
    )
    trainer.train()

    trajectories = args.out_dir / "trajectories.jsonl"
    report["peak_vram_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
    report["auditkit_episodes"] = len(episodes_from_agenttune(str(trajectories)))
    report["adapter_moved"] = adapter_moved(args.out_dir / "adapter_model.safetensors")

    out = REPO_ROOT / "results" / "grpo_smoke.json"
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    LOG.info("%s", {key: value for key, value in report.items() if key != "provenance"})


if __name__ == "__main__":
    main()
