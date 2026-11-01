"""Supervised pilot: can demonstrations teach Tiny Aya to search on lookups, not on statements?

Trains a LoRA adapter through AgentTune's distillation trainer on ``data/pilot_train.jsonl``, then
scores the adapter on ``data/first_test_items.jsonl``, a different company and different wording.
Takes about 15 minutes on an RTX 3080. The adapter goes outside the repository.

Usage:
    python scripts/run_supervised_pilot.py --seed 1234 --out-dir C:/scratch/pilot_adapter
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path

import torch
from agenttune import create_distill_trainer
from agenttune.agentic.distill_trainer import _DefaultSFTTrainerFactory
from huggingface_hub import snapshot_download
from peft import PeftModel

from aya_retrieval.inference import GREEDY, SAMPLING, generate_reply
from aya_retrieval.models import MODEL_ID, MODEL_REVISION, load_model
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.scoring import check_scorer, clean_call_count, search_counts, searched
from aya_retrieval.tool_prompt import system_prompt_with_tools
from aya_retrieval.training_checks import adapter_moved

LOG = logging.getLogger("supervised_pilot")

TRAIN_PATH = REPO_ROOT / "data" / "pilot_train.jsonl"
TEST_PATH = REPO_ROOT / "data" / "first_test_items.jsonl"
TRAIN_SYSTEM = (
    "You are the assistant for staff at Bluewater Freight. You can search the company handbook."
)
TEST_SYSTEM = (
    "You are the assistant for staff at Harbourline Logistics. You can search the company handbook."
)


def read_jsonl(path: Path) -> list[dict]:
    """Return the rows of a JSON-lines file."""
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class SystemPromptFactory:
    """Put the system prompt on every training row before AgentTune's default SFT factory runs.

    Hand-authored demonstrations carry only a user turn and a reply, so without this the model
    would learn on prompts that lack the tool schema it sees at inference.
    """

    def __init__(self, system: str, default_factory: _DefaultSFTTrainerFactory) -> None:
        self.system = system
        self.default_factory = default_factory

    def __call__(self, *, model, train_dataset, **kwargs):
        system_turn = {"role": "system", "content": self.system}
        rows = [{"messages": [system_turn, *row["messages"]]} for row in train_dataset]
        return self.default_factory(model=model, train_dataset=rows, **kwargs)


def train_adapter(args: argparse.Namespace) -> None:
    """Train the adapter and leave it in ``args.out_dir``."""
    demonstrations = [(row["text"], row["response"]) for row in read_jsonl(TRAIN_PATH)]
    default_factory = _DefaultSFTTrainerFactory(
        lora_targets=["q_proj", "k_proj", "v_proj", "o_proj"]
    )
    trainer = create_distill_trainer(
        student=snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True),
        demonstrations=demonstrations,
        trainer_factory=SystemPromptFactory(
            system_prompt_with_tools(TRAIN_SYSTEM), default_factory
        ),
        output_dir=str(args.out_dir),
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=2,
        gradient_checkpointing=True,
        seed=args.seed,
        save_strategy="no",
        logging_steps=30,
        report_to="none",
    )
    trainer.train()
    default_factory.sft_trainer.save_model(str(args.out_dir))
    del default_factory.model, default_factory.sft_trainer
    torch.cuda.empty_cache()


def score_adapter(adapter_dir: Path, samples: int, max_tokens: int) -> dict:
    """Return the adapter's scored replies to the first-test items."""
    model, tokenizer = load_model()
    model = PeftModel.from_pretrained(model, str(adapter_dir))
    model.eval()
    system = system_prompt_with_tools(TEST_SYSTEM)
    greedy, sampled = [], []
    for item in read_jsonl(TEST_PATH):
        reply = generate_reply(model, tokenizer, system, item["text"], GREEDY, max_tokens)
        greedy.append({**item, "reply": reply, "searched": searched(reply)})
        for _ in range(samples):
            reply = generate_reply(model, tokenizer, system, item["text"], SAMPLING, max_tokens)
            sampled.append({**item, "reply": reply, "searched": searched(reply)})
    return {
        "greedy": search_counts(greedy),
        "sampled": search_counts(sampled),
        "greedy_clean_calls": clean_call_count(greedy),
        "sampled_clean_calls": clean_call_count(sampled),
        "greedy_rows": greedy,
        "sampled_rows": sampled,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True, help="where the adapter goes")
    parser.add_argument("--epochs", type=int, default=6)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--samples", type=int, default=3, help="sampled replies per item")
    parser.add_argument("--max-new-tokens", type=int, default=80)
    parser.add_argument("--score-only", action="store_true", help="score an adapter in --out-dir")
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
        "epochs": args.epochs,
        "learning_rate": args.learning_rate,
    }
    started = time.time()
    torch.manual_seed(args.seed)

    if not args.score_only:
        train_adapter(args)
        report["train_peak_vram_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
        report["train_seconds"] = round(time.time() - started)
    report["adapter_moved"] = adapter_moved(args.out_dir / "adapter_model.safetensors")
    if not report["adapter_moved"]:
        raise RuntimeError("the adapter did not move, so this run cannot be reported")

    report["adapter"] = score_adapter(args.out_dir, args.samples, args.max_new_tokens)
    report["seconds"] = round(time.time() - started)

    suffix = "_rescored" if args.score_only else ""
    out = REPO_ROOT / "results" / "supervised_pilot" / f"seed_{args.seed}{suffix}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    summary = {key: report["adapter"][key] for key in report["adapter"] if "rows" not in key}
    LOG.info("wrote %s: %s", out, summary)


if __name__ == "__main__":
    main()
