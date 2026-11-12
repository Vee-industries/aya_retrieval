"""Fingerprints of what the generator, the training builder and the evaluation make by default.

R-178 adds options to all three. ``test_r178.py`` checks these fingerprints against the ones the
code made before those options existed, so every default output is byte for byte as it was. The
builder and the evaluation run with a scripted stand-in for the model: no model, no card.

Kept import-free of anything R-178 added, so the same functions can fingerprint the older code.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
# The 6.37 set's base build (data/screens/brief_chat.provenance.json), at a small size, without
# --hard-in-view: the scripted model answers every in_view item, so no hard row would ever come.
BUILD_637 = [
    "--read-hint",
    "--scripted-answers",
    "confirm",
    "--more-indirect",
    "--more-chat",
    "--brief-chat",
]
BUILD_OTHER = [
    "--never-told-hits",
    "--second-search",
    "0.5",
    "--message-queries",
    "--more-statements",
]
BUILD_FLAGS = {"default": [], "fix637": BUILD_637, "other": BUILD_OTHER}
EVAL_FLAGS = {
    "train": ["--pool", "train"],
    "train_stressed": ["--pool", "train", "--asked-before", "--corrections"],
    "probe": ["--pool", "probe"],
    "hard_dev": ["--pool", "hard_dev", "--decoys", "2"],
}


def item_fingerprint() -> str:
    """Return a hash of default conversations over every pool, kind and the older options."""
    from aya_retrieval.conversations import ITEM_KINDS, build_item

    digest = hashlib.sha256()
    for pool in ("train", "wide", "probe", "hard_dev"):
        for kind in ITEM_KINDS:
            for seed in range(30):
                for decoys in (0, 1, 3):
                    item = build_item(f"{kind}_{seed}", seed * 7919, 58, kind, pool, decoys)
                    digest.update(repr(item).encode("utf-8"))
            for seed in range(30):
                item = build_item(f"{kind}_{seed}", seed, 58, kind, "train", 2, True, True, True)
                digest.update(repr(item).encode("utf-8"))
    return digest.hexdigest()


class FakeTokenizer:
    """Counts eight characters as one token."""

    def apply_chat_template(self, messages, tokenize=True, return_dict=True, **_):
        size = sum(len(m["content"]) for m in messages) // 8
        return {"input_ids": list(range(size))}

    def encode(self, text, add_special_tokens=False):
        return list(range(len(text) // 8))


def fake_generate(model, tokenizer, messages, config, max_tokens):
    """Name the first train-pool value the messages hold, else reply without one."""
    from aya_retrieval.pools import TRAIN

    text = " ".join(m["content"] for m in messages)
    for _, template in sorted(TRAIN.facts.items()):
        for value in template.values:
            if value in text:
                return f"I think it is {value}."
    return "Okay, good to know."


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def builder_fingerprint(tmp: Path, flags: list[str], scripts: Path = SCRIPTS) -> str:
    """Return a hash of a small training build's rows and provenance, with the model scripted."""
    module = _load(scripts / "run_build_training_set.py", "fingerprint_builder")
    out = tmp / "rows.jsonl"
    argv = ["build", "--seed", "71119", "--index", str(tmp / "build.sqlite"), "--out", str(out)]
    with (
        mock.patch.object(module, "ROWS_PER_KIND", dict.fromkeys(module.ROWS_PER_KIND, 4)),
        mock.patch.object(module, "load_model", lambda: (object(), FakeTokenizer())),
        mock.patch.object(module, "generate_from_messages", fake_generate),
        mock.patch.object(module, "run_metadata", dict),
        mock.patch.object(sys, "argv", [*argv, "--allow-dirty", *flags]),
    ):
        module.main()
    report = json.loads(out.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    report.pop("provenance")
    return hashlib.sha256(out.read_bytes() + json.dumps(report).encode("utf-8")).hexdigest()


def eval_fingerprint(tmp: Path, flags: list[str], scripts: Path = SCRIPTS) -> str:
    """Return a hash of a small evaluation's report, with the model scripted."""
    module = _load(scripts / "run_recall_eval.py", "fingerprint_eval")
    argv = ["eval", "--seed", "5", "--index", str(tmp / "eval.sqlite"), "--label", "fp"]
    argv += ["--items-per-kind", "3", "--sizes", "58", "--allow-dirty"]
    with (
        mock.patch.object(module, "load_model", lambda: (object(), FakeTokenizer())),
        mock.patch.object(module, "generate_from_messages", fake_generate),
        mock.patch.object(module, "run_metadata", dict),
        mock.patch.object(module, "REPO_ROOT", tmp),
        mock.patch.object(module.torch.cuda, "max_memory_allocated", lambda: 0),
        mock.patch.object(sys, "argv", [*argv, *flags]),
    ):
        module.main()
    report = json.loads((tmp / "results/recall_eval/fp_seed_5.json").read_text(encoding="utf-8"))
    for key in ("provenance", "seconds", "peak_vram_gib"):
        report.pop(key)
    return hashlib.sha256(json.dumps(report).encode("utf-8")).hexdigest()


def all_fingerprints(tmp: Path, scripts: Path = SCRIPTS) -> dict[str, str]:
    """Return every fingerprint, each run in its own folder under ``tmp``."""
    prints = {"items": item_fingerprint()}
    for name, flags in BUILD_FLAGS.items():
        (tmp / f"build_{name}").mkdir()
        prints[f"build_{name}"] = builder_fingerprint(tmp / f"build_{name}", flags, scripts)
    for name, flags in EVAL_FLAGS.items():
        (tmp / f"eval_{name}").mkdir()
        prints[f"eval_{name}"] = eval_fingerprint(tmp / f"eval_{name}", flags, scripts)
    return prints
