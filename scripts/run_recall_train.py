"""Train the recall adapter on ``data/recall_train.jsonl`` through AgentTune's distillation trainer.

Training only: scoring is a separate process (``run_recall_eval.py``), so the card is free for it.
About 9 seconds a step on an RTX 3080. The adapter goes outside the repository.

Usage:
    python scripts/run_recall_train.py --seed 1234 --out-dir C:/scratch/recall_adapter
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

from aya_retrieval.demonstrations import as_event_log
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.tool_prompt import system_prompt_with_tools
from aya_retrieval.training_checks import adapter_moved

LOG = logging.getLogger("recall_train")

TRAIN_PATH = REPO_ROOT / "data" / "recall_train.jsonl"
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."
LORA_TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj"]


class SystemPromptFactory:
    """Put the system prompt on every training row before AgentTune's default SFT factory runs."""

    def __init__(self, system: str, default_factory: _DefaultSFTTrainerFactory) -> None:
        self.system = system
        self.default_factory = default_factory

    def __call__(self, *, model, train_dataset, **kwargs):
        system_turn = {"role": "system", "content": self.system}
        rows = [{"messages": [system_turn, *row["messages"]]} for row in train_dataset]
        return self.default_factory(model=model, train_dataset=rows, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True, help="where the adapter goes")
    parser.add_argument("--epochs", type=float, default=3)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    require_clean_tree(args.allow_dirty)
    report = {
        "provenance": run_metadata(),
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "seed": args.seed,
        "epochs": args.epochs,
        "learning_rate": args.learning_rate,
    }
    lines = TRAIN_PATH.read_text(encoding="utf-8").splitlines()
    logs = [as_event_log(json.loads(line)["turns"]) for line in lines]
    report["rows"] = len(logs)

    started = time.time()
    torch.manual_seed(args.seed)
    default_factory = _DefaultSFTTrainerFactory(lora_targets=LORA_TARGETS)
    trainer = create_distill_trainer(
        student=snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True),
        trajectories=logs,
        trainer_factory=SystemPromptFactory(
            system_prompt_with_tools(SYSTEM_WITH_TOOL), default_factory
        ),
        output_dir=str(args.out_dir),
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=2,
        gradient_checkpointing=True,
        seed=args.seed,
        save_strategy="no",
        logging_steps=50,
        report_to="none",
    )
    trainer.train()
    default_factory.sft_trainer.save_model(str(args.out_dir))

    report["train_peak_vram_gib"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
    report["train_seconds"] = round(time.time() - started)
    report["adapter_moved"] = adapter_moved(args.out_dir / "adapter_model.safetensors")
    if not report["adapter_moved"]:
        raise RuntimeError("the adapter did not move, so this run cannot be reported")
    out = REPO_ROOT / "results" / "recall_train" / f"seed_{args.seed}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    LOG.info("wrote %s: %s", out, {k: v for k, v in report.items() if k != "provenance"})


if __name__ == "__main__":
    main()
