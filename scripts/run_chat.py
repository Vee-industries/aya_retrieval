"""Chat with Tiny Aya, with or without the adapter, in the harness it was tested in.

Usage:
    python scripts/run_chat.py --adapter ../adapters/screens/fix17cs37_82 --index chat.sqlite
    python scripts/run_chat.py --adapter ../adapters/screens/fix17cs37_82 --index chat.sqlite \\
        --script demo/chat.txt --out results/demo/fix17cs37_82.json

Without ``--script`` it reads messages from the keyboard until an empty line. With it, each line of
the file is one message, and ``--out`` saves every reply and search, so a recorded demo can be
replayed and checked. Each search the model makes is printed before its reply.
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from peft import PeftModel

from aya_retrieval.chat import MAX_TOKENS, Chat
from aya_retrieval.inference import GREEDY, generate_from_messages
from aya_retrieval.models import load_model
from aya_retrieval.provenance import run_metadata


def messages_from(script: Path | None):
    """Yield messages from the script file, or from the keyboard until an empty line."""
    if script:
        yield from (line for line in script.read_text(encoding="utf-8").splitlines() if line)
        return
    while line := input("you: ").strip():
        yield line


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--adapter", type=Path, help="adapter directory; omit for the base model")
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--script", type=Path, help="a file of messages, one per line")
    parser.add_argument("--out", type=Path, help="save the transcript here as JSON")
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING)

    model, tokenizer = load_model()
    if args.adapter:
        model = PeftModel.from_pretrained(model, str(args.adapter))
        model.eval()

    def generate(messages: list[dict]) -> str:
        return generate_from_messages(model, tokenizer, messages, GREEDY, MAX_TOKENS)

    chat = Chat(generate, args.index)
    turns = []
    for message in messages_from(args.script):
        result = chat.send(message)
        if args.script:
            print(f"you: {message}")
        for query in result.queries:
            print(f"  [search: {query}]")
        print(f"aya: {result.reply}\n")
        turns.append({"message": message, "queries": result.queries, "reply": result.reply})

    args.index.unlink(missing_ok=True)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        report = {
            "provenance": run_metadata(),
            "adapter": str(args.adapter) if args.adapter else None,
            "turns": turns,
        }
        args.out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
