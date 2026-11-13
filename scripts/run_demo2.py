"""Demo2 (R-201): a fresh writer's chat and twelve questions, each asked on its own branch.

Every arm plays the 24 messages of ``demo2/chat.txt``, then asks each question in
``demo2/questions.json`` on a copy of that chat, so every question has the same history. Base's
arms run first; each adapter is then loaded onto a freshly loaded base model, so no two adapters
are ever on one model. Every model runs with the search tool and with an empty index (search finds
nothing). Saved per answer: the queries, each search's output, the reply, whether a search output
held the source message, whether the source is still in view, and, for an older question, whether a
reply to messages 22 to 24 already holds the key (R-201 lane, finding 5).

Usage:
    python scripts/run_demo2.py --adapter 6.37=../adapters/screens/fix17cs37_82 \\
        --adapter K1=../adapters/screens/k1_r178_82 \\
        --adapter K1.3=../adapters/screens/k1_3_r200_82 --out results/demo2/branches.json
"""

from __future__ import annotations

import argparse
import copy
import gc
import hashlib
import importlib.util
import json
import logging
from pathlib import Path

import torch
from peft import PeftModel

from aya_retrieval.chat import MAX_TOKENS
from aya_retrieval.conversations import EXCHANGES_IN_VIEW
from aya_retrieval.inference import GREEDY, generate_from_messages
from aya_retrieval.models import load_model
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata

SCRIPTS = Path(__file__).resolve().parent
MESSAGES = 24
IN_VIEW_FROM = MESSAGES - EXCHANGES_IN_VIEW + 1  # message 22: the first one still in view


def _load_script(name: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


Branch = _load_script("run_demo_branches").Branch  # R-176's chat with each search output kept


def run_arm(generate, name: str, searchable: bool, messages, questions, work: Path) -> dict:
    chat = Branch(generate, work / f"{name}.sqlite", searchable)
    prefix = [chat.send(m) for m in messages]
    in_view_replies = [t["reply"].casefold() for t in prefix[IN_VIEW_FROM - 1 :]]
    answers = []
    for number, q in enumerate(questions, 1):
        branch = copy.copy(chat)
        branch.exchanges = list(chat.exchanges)
        branch.index = work / f"{name}_q{number}.sqlite"
        turn = branch.send(q["question"])
        source = q["source_message"]  # None for never_told
        if source is not None:
            turn["found_source"] = any(messages[source - 1] in o for o in turn["search_outputs"])
            turn["source_in_view"] = source >= IN_VIEW_FROM
            turn["key_in_reply"] = q["key"].casefold() in turn["reply"].casefold()
            turn["key_in_view_replies"] = any(q["key"].casefold() in r for r in in_view_replies)
        answers.append({"number": number, **q, **turn})
        branch.index.unlink(missing_ok=True)
    chat.index.unlink(missing_ok=True)
    return {"prefix": prefix, "answers": answers}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--adapter", action="append", default=[], help="NAME=PATH, in run order")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--demo-dir",
        type=Path,
        default=REPO_ROOT / "demo2",
        help="folder with chat.txt and questions.json (R-229: demo3 is the held-out chat)",
    )
    args = parser.parse_args()
    script, questions_path = args.demo_dir / "chat.txt", args.demo_dir / "questions.json"
    logging.basicConfig(level=logging.WARNING)
    require_clean_tree()
    metadata = run_metadata()
    messages = [line for line in script.read_text(encoding="utf-8").splitlines() if line]
    questions = json.loads(questions_path.read_text(encoding="utf-8"))["questions"]
    if len(messages) != MESSAGES or len(questions) != 12:
        raise SystemExit(
            f"expected 24 messages and 12 questions: {len(messages)}, {len(questions)}"
        )
    adapters = [(n, Path(p)) for n, p in (a.split("=", 1) for a in args.adapter)]
    work = REPO_ROOT.parent / "demo2_work"
    work.mkdir(exist_ok=True)

    arms, hashes = {}, {}
    for name, path in [("base", None), *adapters]:
        model, tokenizer = load_model()
        if path is not None:
            weights = path / "adapter_model.safetensors"
            hashes[name] = {
                "path": str(path),
                "sha256": hashlib.sha256(weights.read_bytes()).hexdigest(),
            }
            model = PeftModel.from_pretrained(model, str(path))
            model.eval()

        def generate(chat_messages: list[dict], model=model, tokenizer=tokenizer) -> str:
            return generate_from_messages(model, tokenizer, chat_messages, GREEDY, MAX_TOKENS)

        for searchable in (True, False):
            arm = name if searchable else f"{name}_no_search"
            arms[arm] = run_arm(
                generate, arm.replace(".", ""), searchable, messages, questions, work
            )
            print(f"done {arm}", flush=True)
        del model, generate
        gc.collect()
        torch.cuda.empty_cache()
    work.rmdir()

    report = {
        "provenance": metadata,
        "record": "R-201",
        "adapters": hashes,
        "demo_dir": args.demo_dir.name,
        "chat_sha256": hashlib.sha256(script.read_bytes()).hexdigest(),
        "questions_sha256": hashlib.sha256(questions_path.read_bytes()).hexdigest(),
        "arms": arms,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
