"""Turning a conversation into what the adapter should have done on its last message.

Targets are the base model's own replies wherever they pass the scorer, so training teaches tool
habits, leaves ordinary conversation as it was, and leaves no single answer sentence to memorise.
Calls are scripted, because the base model does not make them well enough to copy.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict

from agenttune.agentic.events import Event, EventKind, EventLog
from agenttune.agentic.rollout_engines.rollout_factory import DEFAULT_TOOL_RESULT_FORMAT

from aya_retrieval.conversations import NEEDS_SEARCH, NEVER_TOLD, RecallItem
from aya_retrieval.harness import turns_from
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME


def whole_sentences(reply: str) -> str | None:
    """Return ``reply`` up to its last finished sentence, or None if it has none.

    A reply cut off by the token limit would otherwise teach the adapter to stop mid-sentence.
    """
    ends = [reply.rfind(mark) for mark in ".?!"]
    return reply[: max(ends) + 1].strip() if max(ends) >= 0 else None


def search_call(query: str) -> str:
    """Return the text of a clean search call."""
    return json.dumps([{"tool_name": SEARCH_TOOL_NAME, "parameters": {"query": query}}])


def demonstration_turns(
    item: RecallItem, search_output: str, base_reply: str, found_fact: bool, unknown_reply: str
) -> list[dict]:
    """Return the chat turns of a demonstration, ending in the reply the model should give.

    Args:
        item: The conversation.
        search_output: What the tool returned for ``item.query``; unused when no search is needed.
        base_reply: The reply to teach: base's own, or a scripted one if base's failed the scorer.
        found_fact: Whether the search really returned the fact.
        unknown_reply: What to say when the search came back without it.
    """
    turns = [*turns_from(item.view()), {"role": "user", "content": item.message}]
    if item.kind not in NEEDS_SEARCH:
        return [*turns, {"role": "assistant", "content": base_reply}]

    # The demonstration must be true to what the tool returned, or it teaches making answers up.
    if item.kind == NEVER_TOLD:
        answer = item.reply
    else:
        answer = base_reply if found_fact else unknown_reply
    tool_turn = DEFAULT_TOOL_RESULT_FORMAT.format(name=SEARCH_TOOL_NAME, content=search_output)
    return [
        *turns,
        {"role": "assistant", "content": search_call(item.query)},
        {"role": "user", "content": tool_turn},
        {"role": "assistant", "content": answer},
    ]


def as_event_log(turns: list[dict]) -> EventLog:
    """Return turns as a full-tier trajectory that AgentTune renders back to the same turns.

    Only OBSERVATION and TEXT events are used: TOOL_CALL renders in tags that are not a clean call,
    and TOOL_RESULT renders as an empty turn on Tiny Aya's template.
    """
    log = EventLog(tier="full")
    for turn in turns:
        kind = EventKind.OBSERVATION if turn["role"] == "user" else EventKind.TEXT
        log.append(Event(kind, {"text": turn["content"]}))
    return log


def kind_balanced_subset(rows: list[dict], fraction: float, seed: int) -> list[dict]:
    """Return ``fraction`` of ``rows``, drawn the same share from each kind, in the original order.

    For quick screening runs. The training file is sorted by kind, so a prefix is one kind.
    """
    by_kind = defaultdict(list)
    for index, row in enumerate(rows):
        by_kind[row["kind"]].append(index)
    rng = random.Random(seed)
    keep = set()
    for indices in by_kind.values():
        keep.update(rng.sample(indices, round(len(indices) * fraction)))
    return [row for index, row in enumerate(rows) if index in keep]
