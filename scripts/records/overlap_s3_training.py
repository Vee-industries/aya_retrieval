"""Count word runs S3 shares with a training set, printing counts only (R-178, against lane).

A test written to probe training's gaps could still echo training rows. This counts, for each S3
chat file, the four-word runs that also occur in any user or assistant line of the training set,
and the total. It prints numbers only, never text, so running it does not open the sealed set to
the reader.

Usage:
    python scripts/records/overlap_s3_training.py --final [--train data/screens/fix17cs37.jsonl]
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CHATS = REPO_ROOT / "data" / "heldout3" / "chats"
RUN = 4


def runs(text: str) -> set[tuple[str, ...]]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(words[i : i + RUN]) for i in range(len(words) - RUN + 1)}


def training_runs(path: Path) -> set[tuple[str, ...]]:
    out: set[tuple[str, ...]] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        for turn in json.loads(line)["turns"]:
            if not turn["content"].startswith("Tool result"):
                out |= runs(turn["content"])
    return out


def chat_text(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return " ".join(chat_text(v) for v in value.values())
    if isinstance(value, list):
        return " ".join(chat_text(v) for v in value)
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--final", action="store_true", help="needed to open the sealed set")
    parser.add_argument("--train", type=Path, default=REPO_ROOT / "data/screens/fix17cs37.jsonl")
    args = parser.parse_args()
    if not args.final:
        parser.error("the sealed set needs --final")
    train = training_runs(args.train)
    total_runs = total_shared = 0
    for path in sorted(CHATS.glob("*.json")):
        chat = runs(chat_text(json.loads(path.read_text(encoding="utf-8"))))
        shared = len(chat & train)
        total_runs += len(chat)
        total_shared += shared
        print(f"{path.stem}: {shared} of {len(chat)} four-word runs shared")
    print(f"all: {total_shared} of {total_runs} shared; training runs {len(train)}")


if __name__ == "__main__":
    main()
