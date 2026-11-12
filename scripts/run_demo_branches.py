"""Ask the registered demo questions, each on its own branch of the scripted chat (R-176).

Every arm plays messages 1 to 14 of ``demo/chat.txt``, then asks each question in
``demo/questions_r176.json`` on a copy of that chat, so every question has the same history. Arms:
base and 6.37, each with the search tool and with an empty index (search finds nothing), so the
result shows how much each model answers without finding the fact. Each search's output is saved,
with whether it held the message the question is about.

Usage:
    python scripts/run_demo_branches.py --adapter ../adapters/screens/fix17cs37_82 \\
        --out results/demo/branches_r176.json
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import logging
from pathlib import Path

from peft import PeftModel

from aya_retrieval.chat import MAX_TOKENS, SYSTEM_WITH_TOOL
from aya_retrieval.conversations import EXCHANGES_IN_VIEW
from aya_retrieval.harness import run_turn
from aya_retrieval.inference import GREEDY, generate_from_messages
from aya_retrieval.models import load_model
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import build_search_tool
from aya_retrieval.tool_prompt import system_prompt_with_tools

SCRIPT = REPO_ROOT / "demo" / "chat.txt"
QUESTIONS = REPO_ROOT / "demo" / "questions_r176.json"
PREFIX = 14  # messages 1 to 14; message 15 closes the chat and is not asked


class Branch:
    """The chat as ``aya_retrieval.chat.Chat`` runs it, with each search's output kept."""

    def __init__(self, generate, index: Path, searchable: bool):
        self.generate, self.index, self.searchable = generate, index, searchable
        self.exchanges: list[tuple[str, str]] = []

    def send(self, message: str) -> dict:
        older = self.exchanges[: max(len(self.exchanges) - EXCHANGES_IN_VIEW, 0)]
        tool = build_search_tool(older if self.searchable else [], self.index, match_all=False)
        outputs = []

        def search(query: str) -> str:
            result = tool.execute(query)
            outputs.append(result.output if result.success else str(result.error))
            return outputs[-1]

        system = system_prompt_with_tools(SYSTEM_WITH_TOOL)
        view = self.exchanges[-EXCHANGES_IN_VIEW:]
        result = run_turn(self.generate, search, system, view, message)
        self.exchanges.append((message, result.reply))
        return {
            "message": message,
            "queries": result.queries,
            "search_outputs": outputs,
            "reply": result.reply,
        }


def run_arm(generate, name: str, searchable: bool, messages, questions, work: Path) -> dict:
    chat = Branch(generate, work / f"{name}.sqlite", searchable)
    prefix = [chat.send(m) for m in messages[:PREFIX]]
    answers = []
    for q in questions:
        branch = copy.copy(chat)
        branch.exchanges = list(chat.exchanges)
        number = q["source_message"]  # None for the never-told question
        branch.index = work / f"{name}_{number or 'never_told'}.sqlite"
        turn = branch.send(q["question"])
        if number is not None:
            source = messages[number - 1]
            turn["found_source"] = any(source in out for out in turn["search_outputs"])
            turn["source_in_view"] = number > PREFIX - EXCHANGES_IN_VIEW
        answers.append({**q, **turn})
        branch.index.unlink(missing_ok=True)
    chat.index.unlink(missing_ok=True)
    return {"prefix": prefix, "answers": answers}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--adapter", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    logging.basicConfig(level=logging.WARNING)
    require_clean_tree()
    metadata = run_metadata()
    messages = [line for line in SCRIPT.read_text(encoding="utf-8").splitlines() if line]
    questions = json.loads(QUESTIONS.read_text(encoding="utf-8"))["questions"]
    weights = args.adapter / "adapter_model.safetensors"
    work = REPO_ROOT.parent / "demo_branches_work"
    work.mkdir(exist_ok=True)

    model, tokenizer = load_model()

    def generate(chat_messages: list[dict]) -> str:
        return generate_from_messages(model, tokenizer, chat_messages, GREEDY, MAX_TOKENS)

    arms = {}
    for searchable in (True, False):  # base before the adapter wraps the model
        name = "base" if searchable else "base_no_search"
        arms[name] = run_arm(generate, name, searchable, messages, questions, work)
    model = PeftModel.from_pretrained(model, str(args.adapter))
    model.eval()
    for searchable in (True, False):
        name = "6.37" if searchable else "6.37_no_search"
        arms[name] = run_arm(generate, name.replace(".", ""), searchable, messages, questions, work)
    work.rmdir()

    report = {
        "provenance": metadata,
        "record": "R-176",
        "adapter": str(args.adapter),
        "adapter_weights_sha256": hashlib.sha256(weights.read_bytes()).hexdigest(),
        "questions_sha256": hashlib.sha256(QUESTIONS.read_bytes()).hexdigest(),
        "arms": arms,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
