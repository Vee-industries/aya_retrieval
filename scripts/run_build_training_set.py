"""Build the recall training set: demonstrations on the train pool, with base's own plain replies.

About 20 minutes on an RTX 3080. Writes ``data/recall_train.jsonl`` and a provenance file beside it.

Usage:
    python scripts/run_build_training_set.py --seed 1234 --index C:/scratch/train.sqlite
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import logging
import random
from collections import Counter, defaultdict
from pathlib import Path

from agenttune.agentic.rollout_engines.rollout_factory import DEFAULT_TOOL_RESULT_FORMAT

from aya_retrieval.conversations import (
    CONFIRM,
    IN_VIEW,
    ITEM_KINDS,
    NEEDS_SEARCH,
    NEVER_TOLD,
    OLDER,
    STATEMENT,
    RecallItem,
    build_item,
)
from aya_retrieval.demonstrations import (
    demonstration_turns,
    message_words_query,
    missing_words_query,
    search_call,
    whole_sentences,
)
from aya_retrieval.harness import turns_from
from aya_retrieval.inference import GREEDY, generate_from_messages
from aya_retrieval.models import load_model
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact
from aya_retrieval.scoring import item_correct
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME, system_prompt_with_tools

LOG = logging.getLogger("build_training_set")

OUT_PATH = REPO_ROOT / "data" / "recall_train.jsonl"
SYSTEM = "You are chatting with a friend."
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."
# Fix 11 (R-060): asked for base's statement replies only. The training row leaves it out, so the
# adapter learns short replies to chat without being told to.
BRIEF = "Reply briefly, in one or two sentences."
MAX_TOKENS = 60
SIZE = 58
ROWS_PER_KIND = {OLDER: 200, CONFIRM: 150, NEVER_TOLD: 150, IN_VIEW: 150, STATEMENT: 150}
MAX_ROW_TOKENS = 1024
# Found and not-found rows must return the same numbers of passages, or the count gives the answer.
DECOY_CHOICES = {
    OLDER: (0, 1, 2),
    CONFIRM: (0, 1, 2),
    NEVER_TOLD: (1, 2, 3),
    IN_VIEW: (1,),
    STATEMENT: (1,),
}


def fit_to_copy(model, tokenizer, item: RecallItem, messages: list[dict]) -> str | None:
    """Return base's whole-sentence reply to ``messages``, or None if it is not fit to copy."""
    reply = whole_sentences(generate_from_messages(model, tokenizer, messages, GREEDY, MAX_TOKENS))
    if reply is None or SEARCH_TOOL_NAME in reply:
        return None
    if not item_correct(item.kind, reply, item.answer, item.forbidden, calls=0):
        return None
    return reply


def base_reply(model, tokenizer, item: RecallItem, brief: bool = False) -> str | None:
    """Return base's reply with no tool in sight, or None if it is not fit to copy.

    With ``brief``, base is asked for a short reply; the instruction is not part of the row.
    """
    messages = [
        {"role": "system", "content": f"{SYSTEM} {BRIEF}" if brief else SYSTEM},
        *turns_from(item.view()),
        {"role": "user", "content": item.message},
    ]
    return fit_to_copy(model, tokenizer, item, messages)


def base_answer(model, tokenizer, item: RecallItem, output: str) -> str | None:
    """Return base's reply to a real search result, or None if it is not fit to copy."""
    messages = [
        {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)},
        *turns_from(item.view()),
        {"role": "user", "content": item.message},
        {"role": "assistant", "content": search_call(item.query)},
        {
            "role": "user",
            "content": DEFAULT_TOOL_RESULT_FORMAT.format(name=SEARCH_TOOL_NAME, content=output),
        },
    ]
    return fit_to_copy(model, tokenizer, item, messages)


def hinted_reply(model, tokenizer, item: RecallItem, brief: bool = False) -> str | None:
    """Return base's reply with the fact restated in the system prompt, or None if not fit to copy.

    For `in_view` items base answered wrong. The training row leaves the hint out, so the adapter
    learns to read the fact from the turns in view rather than to search for it.
    """
    fact = item.exchanges[item.fact_index][0]
    messages = [
        {
            "role": "system",
            "content": f'{SYSTEM} Earlier your friend said: "{fact}"'
            + (f" {BRIEF}" if brief else ""),
        },
        *turns_from(item.view()),
        {"role": "user", "content": item.message},
    ]
    return fit_to_copy(model, tokenizer, item, messages)


def empty_search(tool, item: RecallItem) -> tuple[str, str] | None:
    """Return a search in the message's own words and its empty result, or None if it finds any."""
    query = missing_words_query(item)
    if query is None:
        return None
    output = tool.execute(query).output
    return (query, output) if "chunk_id=" not in output else None


def row_tokens(turns: list[dict], tokenizer) -> int:
    """Return the token length of one row as training will see it."""
    system = {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)}
    return len(
        tokenizer.apply_chat_template([system, *turns], tokenize=True, return_dict=True)[
            "input_ids"
        ]
    )


def longest_row(rows: list[dict], tokenizer) -> int:
    """Return the token length of the longest row as training will see it."""
    return max(row_tokens(row["turns"], tokenizer) for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    parser.add_argument("--out", type=Path, default=OUT_PATH, help="training rows, .jsonl")
    parser.add_argument(
        "--read-hint", action="store_true", help="keep in_view items base got wrong, via a hint"
    )
    parser.add_argument(
        "--hard-in-view",
        type=int,
        default=0,
        help="in_view rows kept for items base got wrong; needs --read-hint",
    )
    parser.add_argument(
        "--never-told-rows",
        type=int,
        default=ROWS_PER_KIND[NEVER_TOLD],
        help="never_told rows to make",
    )
    parser.add_argument(
        "--second-search",
        type=float,
        default=0.0,
        help="share of search rows that first make a search that finds nothing",
    )
    parser.add_argument(
        "--reject-replies",
        type=Path,
        help="JSON list of row ids whose base answer was judged incoherent",
    )
    parser.add_argument(
        "--scripted-answers",
        nargs="+",
        default=[],
        choices=[OLDER, CONFIRM],
        help="kinds whose found-fact rows always get the scripted answer, not base's",
    )
    parser.add_argument(
        "--more-indirect",
        action="store_true",
        help="indirect questions also drawn from train_phrasings.MORE_INDIRECT",
    )
    parser.add_argument(
        "--message-queries",
        action="store_true",
        help="demonstrated searches use the friend's own words, not fixed keywords",
    )
    parser.add_argument(
        "--never-told-hits",
        action="store_true",
        help="never_told rows only where the search returns passages, all about someone else",
    )
    parser.add_argument(
        "--more-statements",
        action="store_true",
        help="facts also stated in train_phrasings.MORE_STATEMENTS wordings",
    )
    parser.add_argument(
        "--more-chat",
        action="store_true",
        help="statement rows also draw from train_phrasings.MORE_CHAT",
    )
    parser.add_argument(
        "--brief-chat",
        action="store_true",
        help="statement targets are base's reply when asked to be brief (not part of the row)",
    )
    parser.add_argument(
        "--brief-in-view",
        action="store_true",
        help="in_view targets (plain and hinted) are base's reply when asked to be brief",
    )
    parser.add_argument(
        "--kinds",
        nargs="+",
        default=list(ITEM_KINDS),
        choices=ITEM_KINDS,
        help="kinds to build; spare rows for vetting need only some",
    )
    parser.add_argument(
        "--statement-rows",
        type=int,
        default=ROWS_PER_KIND[STATEMENT],
        help="statement rows to make",
    )
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    if args.hard_in_view and not args.read_hint:
        parser.error("--hard-in-view needs --read-hint")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

    require_clean_tree(args.allow_dirty)
    report = {
        "provenance": run_metadata(),
        "seed": args.seed,
        "read_hint": args.read_hint,
        "hard_in_view": args.hard_in_view,
        "never_told_rows": args.never_told_rows,
        "second_search": args.second_search,
        "reject_replies": args.reject_replies and args.reject_replies.as_posix(),
        "scripted_answers": args.scripted_answers,
        "more_indirect": args.more_indirect,
        "message_queries": args.message_queries,
        "never_told_hits": args.never_told_hits,
        "more_statements": args.more_statements,
        "more_chat": args.more_chat,
        "brief_chat": args.brief_chat,
        "brief_in_view": args.brief_in_view,
        "kinds": args.kinds,
        "statement_rows": args.statement_rows,
    }
    rejected = set(json.loads(args.reject_replies.read_text())) if args.reject_replies else set()
    rows_per_kind = {
        **ROWS_PER_KIND,
        NEVER_TOLD: args.never_told_rows,
        STATEMENT: args.statement_rows,
    }
    rng = random.Random(args.seed)
    # Its own stream, so choosing second-search rows leaves every other row as it was.
    second_rng = random.Random(args.seed + 1)
    model, tokenizer = load_model()

    rows, tally, passages = [], Counter(), defaultdict(Counter)
    for kind in (kind for kind in ITEM_KINDS if kind in args.kinds):
        made = attempt = 0
        while made < rows_per_kind[kind]:
            seed, attempt = args.seed + kind_seed_offset(kind) + attempt, attempt + 1
            decoys = rng.choice(DECOY_CHOICES[kind])
            item = build_item(
                f"{kind}_{made:04d}",
                seed,
                SIZE,
                kind,
                "train",
                decoys,
                args.more_indirect,
                args.more_statements,
                args.more_chat,
            )
            if args.message_queries and item.query:
                item = dataclasses.replace(item, query=message_words_query(item))
            if kind in NEEDS_SEARCH:
                tool = build_recall_tool(item, args.index, match_all=False)
                output = tool.execute(item.query).output
                if args.never_told_hits and kind == NEVER_TOLD and "chunk_id=" not in output:
                    # An empty result makes declining easy; the case to teach is same-type facts
                    # about other people coming back (R-050).
                    tally[f"{kind}_empty_skipped"] += 1
                    continue
                found = search_finds_fact(tool, item, item.query)
                tally[f"{kind}_found" if found else f"{kind}_missed"] += 1
                passages[kind][output.count("chunk_id=")] += 1
                reply = item.reply
                if found and kind in args.scripted_answers:
                    tally[f"{kind}_scripted_answer"] += 1
                elif found and kind != NEVER_TOLD:
                    reply = base_answer(model, tokenizer, item, output)
                    if reply and item.item_id in rejected:
                        tally[f"{kind}_base_answer_judged_incoherent"] += 1
                        reply = None
                    tally[f"{kind}_base_answer" if reply else f"{kind}_scripted_answer"] += 1
                    reply = reply or item.reply
            else:
                brief = (args.brief_chat and kind == STATEMENT) or (
                    args.brief_in_view and kind == IN_VIEW
                )
                reply, output, found = base_reply(model, tokenizer, item, brief), "", False
                if reply and kind == IN_VIEW and easy_full(tally, args.hard_in_view):
                    tally[f"{kind}_easy_skipped"] += 1
                    continue
                if reply is None and args.read_hint and kind == IN_VIEW:
                    reply = hinted_reply(model, tokenizer, item, brief)
                    tally[f"{kind}_hinted_reply" if reply else f"{kind}_hinted_reply_rejected"] += 1
                elif reply and kind == IN_VIEW:
                    tally[f"{kind}_base_reply"] += 1
                if reply is None:
                    tally[f"{kind}_base_reply_rejected"] += 1
                    continue
            unknown = rng.choice(TRAIN.unknown_replies)
            turns = demonstration_turns(item, output, reply, found, unknown)
            if kind in NEEDS_SEARCH and second_rng.random() < args.second_search:
                miss = empty_search(tool, item)
                longer = miss and demonstration_turns(item, output, reply, found, unknown, miss)
                if longer and row_tokens(longer, tokenizer) <= MAX_ROW_TOKENS:
                    turns = longer
                tally[
                    f"{kind}_second_search" if turns is longer else f"{kind}_second_search_skipped"
                ] += 1
            rows.append({"id": item.item_id, "kind": kind, "turns": turns})
            made += 1
        LOG.info("%s done after %d attempts", kind, attempt)

    args.index.unlink(missing_ok=True)
    lines = (json.dumps(row, ensure_ascii=False) for row in rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report["rows"] = len(rows)
    report["tally"] = dict(tally)
    report["passages_per_kind"] = {kind: dict(counts) for kind, counts in passages.items()}
    report["longest_row_tokens"] = longest_row(rows, tokenizer)
    if report["longest_row_tokens"] > MAX_ROW_TOKENS:
        raise SystemExit(f"a row exceeds {MAX_ROW_TOKENS} tokens, so training would cut its answer")
    provenance_path = args.out.with_suffix(".provenance.json")
    provenance_path.write_text(json.dumps(report, indent=1), encoding="utf-8")
    LOG.info("wrote %d rows: %s", len(rows), {**tally, **report["passages_per_kind"]})


def easy_full(tally: Counter, hard_rows: int) -> bool:
    """Return True once `in_view` rows base answered unaided fill the share left for hard rows."""
    return tally[f"{IN_VIEW}_base_reply"] >= ROWS_PER_KIND[IN_VIEW] - hard_rows


def kind_seed_offset(kind: str) -> int:
    """Return a fixed seed offset per kind, so kinds use separate conversations."""
    return (ITEM_KINDS.index(kind) + 1) * 100_000


if __name__ == "__main__":
    main()
