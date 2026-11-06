"""R-102: the correction arm, v6's set with about 170 messy rows appended, as fix17cr.

Usage: python scripts/records/build_r102.py --index C:/scratch/build_r102.sqlite

Every appended row is built from fresh train-pool conversations, searched with the real search
tool, and answered with the scripted answer; a row whose search does not return what its answer
needs is skipped, so no answer goes beyond what the tool returned. Three kinds of row:

- ``corr``: an ``older`` or ``confirm`` fact corrected later in training's own wordings
  (``stress.corrected_for_training``); the answer names the new value.
- ``corrcue``: an ``older`` or ``confirm`` fact left alone, while a same-type fact about another
  person is introduced by a training correction opening; the answer names the asked person's own
  value, so a correction opening alone does not decide the answer.
- ``asked``: an earlier question still in view (``stress.asked_before``), on ``older``, ``confirm``
  and ``never_told``.

v6's rows are kept byte for byte. The build stops if a changed line is not worded with training's
correction wordings, or a correction row carries the held-out correction; a row that training would
cut is skipped.
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import random
from collections import Counter
from pathlib import Path

from transformers import AutoTokenizer

from aya_retrieval.chat import SYSTEM_WITH_TOOL
from aya_retrieval.conversations import CONFIRM, NEVER_TOLD, OLDER, build_item
from aya_retrieval.demonstrations import demonstration_turns
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.recall_tool import build_recall_tool
from aya_retrieval.stress import (
    TRAIN_CORRECTION_ENDINGS,
    TRAIN_CORRECTION_OPENINGS,
    asked_before,
    corrected_for_training,
    corrected_heldout,
)
from aya_retrieval.tool_prompt import system_prompt_with_tools

DATA = Path("data/screens")
BASE_SET, OUT = DATA / "strict_chat.jsonl", DATA / "fix17cr.jsonl"
COUNTS = {"corr": 110, "corrcue": 30, "asked": 30}
SIZE = 58
MAX_ROW_TOKENS = 1024
# As the training builder: found and not-found rows return the same numbers of passages (R-020).
DECOY_CHOICES = {OLDER: (0, 1, 2), CONFIRM: (0, 1, 2), NEVER_TOLD: (1, 2, 3)}
FIRST_SEED = 910_000_000


def row_tokens(turns: list[dict], tokenizer) -> int:
    system = {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)}
    ids = tokenizer.apply_chat_template([system, *turns], tokenize=True, return_dict=True)
    return len(ids["input_ids"])


def cue_item(item, rng):
    """Return ``item`` with its same-type decoy fact introduced by a correction opening, or None."""
    slots = [i for i, (user, _) in enumerate(item.exchanges) if item.decoy and item.decoy in user]
    if len(slots) != 1 or slots[0] >= len(item.older()):
        return None
    exchanges = list(item.exchanges)
    user, reply = exchanges[slots[0]]
    exchanges[slots[0]] = (rng.choice(TRAIN_CORRECTION_OPENINGS) + user, reply)
    return dataclasses.replace(item, exchanges=tuple(exchanges))


def make(kind_name: str, n: int, seed: int, rng: random.Random):
    """Return one appended row's original item, its changed item and what the search must return."""
    if kind_name == "asked":
        kind = (OLDER, CONFIRM, NEVER_TOLD)[n % 3]
    else:
        kind = (OLDER, CONFIRM)[n % 2]
    decoys = rng.choice(DECOY_CHOICES[kind])
    item = build_item(f"{kind_name}_{n:04d}", seed, SIZE, kind, "train", decoys)
    if kind_name == "corr":
        fixed = corrected_for_training(item, seed, "train")
        return fixed and (item, fixed, [fixed.answer])
    if kind_name == "corrcue":
        fixed = cue_item(item, rng)
        return fixed and (item, fixed, [fixed.answer, fixed.decoy])
    fixed = asked_before(item, seed, "train")
    return item, fixed, [fixed.answer] if fixed.answer else []


def check_wording(kind_name: str, item, fixed, seed: int) -> None:
    """Stop the build unless every changed line is worded only with training's wordings."""
    changed = [
        new for old, (new, _) in zip(item.exchanges, fixed.exchanges, strict=True) if old[0] != new
    ]
    if kind_name == "asked":
        return
    line = changed[-1]
    trained = line.startswith(TRAIN_CORRECTION_OPENINGS) or line.endswith(TRAIN_CORRECTION_ENDINGS)
    if not trained:
        raise SystemExit(f"{item.item_id}: correction not in training's wordings: {line!r}")
    if kind_name == "corr":
        held = corrected_heldout(item, seed, "train")
        held_lines = {
            new
            for old, (new, _) in zip(item.exchanges, held.exchanges, strict=True)
            if old[0] != new
        }
        if line in held_lines:
            raise SystemExit(f"{item.item_id}: training row carries the held-out correction")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--index", type=Path, required=True, help="scratch search database")
    parser.add_argument("--out", type=Path, default=OUT, help="where to write the set")
    args = parser.parse_args()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    rng = random.Random(FIRST_SEED)
    rows, tally = [], Counter()
    seed = FIRST_SEED
    for kind_name, wanted in COUNTS.items():
        made = 0
        while made < wanted:
            seed += 1
            built = make(kind_name, made, seed, rng)
            if not built:
                tally[f"{kind_name}_unbuildable"] += 1
                continue
            item, fixed, needed = built
            output = (
                build_recall_tool(fixed, args.index, match_all=False).execute(fixed.query).output
            )
            if not all(value in output for value in needed):
                tally[f"{kind_name}_search_missed"] += 1
                continue
            turns = demonstration_turns(fixed, output, fixed.reply, True, TRAIN.unknown_replies[0])
            if row_tokens(turns, tokenizer) > MAX_ROW_TOKENS:
                tally[f"{kind_name}_too_long"] += 1
                continue
            check_wording(kind_name, item, fixed, seed)
            tally[f"{kind_name}_{fixed.kind}_passages_{output.count('chunk_id=')}"] += 1
            rows.append({"id": fixed.item_id, "kind": fixed.kind, "turns": turns})
            made += 1
    base = BASE_SET.read_text(encoding="utf-8")
    args.out.write_text(
        base + "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8"
    )
    args.index.unlink(missing_ok=True)
    report = {
        "provenance": run_metadata(),
        "base_set": BASE_SET.as_posix(),
        "appended": len(rows),
        "counts": COUNTS,
        "tally": dict(tally),
    }
    args.out.with_suffix(".provenance.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8"
    )
    print(f"{args.out}: {len(rows)} rows appended; {dict(tally)}")


if __name__ == "__main__":
    main()
