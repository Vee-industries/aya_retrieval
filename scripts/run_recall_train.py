"""Train the recall adapter on ``data/recall_train.jsonl`` through AgentTune's distillation trainer.

Training only: scoring is a separate process (``run_recall_eval.py``), so the card is free for it.
About 1 second a step on an RTX 3080 (R-029). The adapter goes outside the repository. The loss is
TRL's chunked cross-entropy without its float32 copies of the output layer (``lean_loss``), so
training leaves card memory for other programs.

Usage:
    python scripts/run_recall_train.py --seed 1234 --out-dir C:/scratch/recall_adapter

A quick screening run trains on part of the rows for fewer epochs, one row a step with two steps an
update so it leaves card memory for other programs, and writes its report under its own name:
    python scripts/run_recall_train.py --seed 1234 --out-dir C:/scratch/screen --fraction 0.5
        --epochs 1 --batch-size 1 --grad-accum 2 --report-name screen_fix01
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
from transformers import AutoTokenizer, TrainerCallback

from aya_retrieval.conversations import EXCHANGES_IN_VIEW
from aya_retrieval.demonstrations import as_event_log, kind_balanced_subset
from aya_retrieval.lean_loss import use_lean_loss
from aya_retrieval.loss_masks import decision_labels, demonstrated_labels, without_history_replies
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.tool_prompt import system_prompt_with_tools
from aya_retrieval.training_checks import adapter_moved

LOG = logging.getLogger("recall_train")

TRAIN_PATH = REPO_ROOT / "data" / "recall_train.jsonl"
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."
LORA_TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj"]


LOSS_ON = {
    "all": None,
    "demonstrated": demonstrated_labels,
    "no_history_replies": without_history_replies,
    # 17m (R-088): demonstrated turns, except plain-chat rows, which keep only the decision.
    "chat_decision": demonstrated_labels,
}
# The system turn, the exchanges in view and the friend's message come before what a row teaches.
FIRST_DEMONSTRATED = 1 + 2 * EXCHANGES_IN_VIEW + 1


class SystemPromptFactory:
    """Put the system prompt on every training row before AgentTune's default SFT factory runs.

    With ``loss_on`` other than ``"all"``, each row is also tokenized here with labels from
    ``aya_retrieval.loss_masks``; TRL keeps a dataset's own labels. The messages stay on the row
    because AgentTune's factory reads them before TRL drops the column.
    """

    def __init__(
        self,
        system: str,
        default_factory: _DefaultSFTTrainerFactory,
        loss_on: str = "all",
        decision_keys: set[tuple[str, str]] | None = None,
        callbacks: list | None = None,
    ) -> None:
        self.system = system
        self.default_factory = default_factory
        self.labels = LOSS_ON[loss_on]
        self.decision_keys = decision_keys or set()
        self.callbacks = callbacks or []

    def __call__(self, *, model, train_dataset, **kwargs):
        system_turn = {"role": "system", "content": self.system}
        rows = [{"messages": [system_turn, *row["messages"]]} for row in train_dataset]
        if self.labels:
            tokenizer = AutoTokenizer.from_pretrained(model)
            decided = 0
            for row in rows:
                messages = row["messages"]
                if messages[FIRST_DEMONSTRATED - 1]["role"] != "user":
                    raise ValueError("a row does not have the expected turns in view")
                labels = self.labels
                if row_key(messages[1:]) in self.decision_keys:
                    labels, decided = decision_labels, decided + 1
                row["input_ids"], row["labels"] = labels(tokenizer, messages, FIRST_DEMONSTRATED)
            if decided != len(self.decision_keys):
                raise ValueError(f"{decided} rows matched {len(self.decision_keys)} chat rows")
        trainer = self.default_factory(model=model, train_dataset=rows, **kwargs)
        for callback in self.callbacks:
            trainer.add_callback(callback)
        return trainer


def row_key(turns: list[dict]) -> tuple[str, str]:
    """Return a row's friend message and last reply, which name a plain-chat row."""
    return turns[FIRST_DEMONSTRATED - 2]["content"], turns[-1]["content"]


class SaveAtEpochs(TrainerCallback):
    """Save the adapter at the end of the named epochs, as ``<out-dir>/epoch-<n>`` (R-088)."""

    def __init__(self, out_dir: Path, epochs: list[int]) -> None:
        self.out_dir, self.epochs = out_dir, set(epochs)

    def on_epoch_end(self, args, state, control, model=None, **kwargs):
        epoch = round(state.epoch)
        if epoch in self.epochs:
            model.save_pretrained(str(self.out_dir / f"epoch-{epoch}"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--out-dir", type=Path, required=True, help="where the adapter goes")
    parser.add_argument("--epochs", type=float, default=3)
    parser.add_argument("--learning-rate", type=float, default=2e-4)
    parser.add_argument("--data", type=Path, default=TRAIN_PATH, help="training rows, .jsonl")
    parser.add_argument("--fraction", type=float, default=1.0, help="share of rows, same per kind")
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--grad-accum", type=int, default=1, help="steps per update")
    parser.add_argument("--lora-r", type=int, default=16, help="LoRA rank; alpha is twice it")
    parser.add_argument(
        "--lora-targets", nargs="+", default=LORA_TARGETS, help="modules the adapter trains"
    )
    parser.add_argument(
        "--loss-on",
        choices=sorted(LOSS_ON),
        default="all",
        help="tokens that carry loss: every one (TRL's default), only the demonstrated turns, "
        "or all but the scripted replies in view",
    )
    parser.add_argument(
        "--save-epochs",
        type=int,
        nargs="+",
        default=[],
        help="also save the adapter after these epochs, under <out-dir>/epoch-<n>",
    )
    parser.add_argument(
        "--max-vram-fraction",
        type=float,
        help="cap this process's share of card memory, so the card never spills to system memory",
    )
    parser.add_argument("--report-name", help="report file name, default seed_<seed>")
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    require_clean_tree(args.allow_dirty)
    report = {
        "provenance": run_metadata(),
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "seed": args.seed,
        "data": args.data.resolve().relative_to(REPO_ROOT).as_posix(),
        "epochs": args.epochs,
        "learning_rate": args.learning_rate,
        "fraction": args.fraction,
        "batch_size": args.batch_size,
        "grad_accum": args.grad_accum,
        "lora_r": args.lora_r,
        "lora_targets": args.lora_targets,
        "loss_on": args.loss_on,
        "save_epochs": args.save_epochs,
        **use_lean_loss(),
    }
    rows = [json.loads(line) for line in args.data.read_text(encoding="utf-8").splitlines()]
    if args.fraction < 1:
        rows = kind_balanced_subset(rows, args.fraction, args.seed)
    logs = [as_event_log(row["turns"]) for row in rows]
    decision_keys = None
    if args.loss_on == "chat_decision":
        decision_keys = {row_key(row["turns"]) for row in rows if row["kind"] == "statement"}
        report["decision_rows"] = len(decision_keys)
    report["rows"] = len(logs)

    started = time.time()
    if args.max_vram_fraction:
        # At 9.6 of 10 GB reserved, any other program's memory pushed training into system memory
        # and steps slowed from 1.3 s to 20 s (R-088); the peak in use is 7.8 GB.
        torch.cuda.set_per_process_memory_fraction(args.max_vram_fraction)
        report["max_vram_fraction"] = args.max_vram_fraction
    torch.manual_seed(args.seed)
    default_factory = _DefaultSFTTrainerFactory(
        lora_r=args.lora_r, lora_alpha=2 * args.lora_r, lora_targets=args.lora_targets
    )
    trainer = create_distill_trainer(
        student=snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True),
        trajectories=logs,
        trainer_factory=SystemPromptFactory(
            system_prompt_with_tools(SYSTEM_WITH_TOOL),
            default_factory,
            args.loss_on,
            decision_keys,
            [SaveAtEpochs(args.out_dir, args.save_epochs)] if args.save_epochs else None,
        ),
        output_dir=str(args.out_dir),
        num_train_epochs=args.epochs,
        learning_rate=args.learning_rate,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
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
    name = args.report_name or f"seed_{args.seed}"
    out = REPO_ROOT / "results" / "recall_train" / f"{name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    LOG.info("wrote %s: %s", out, {k: v for k, v in report.items() if k != "provenance"})


if __name__ == "__main__":
    main()
