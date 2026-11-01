"""The two-step tool loop: the model decides, the tool runs, the model answers from the result.

Base and adapter go through this one loop with identical prompts, so a difference between them comes
from the weights. Tool results fold into a user turn the way AgentTune's fallback does.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field

from agenttune.agentic.rollout_engines.rollout_factory import (
    DEFAULT_TOOL_RESULT_FORMAT,
    extract_tool_calls_from_text,
)

from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME

MAX_CALLS = 3


@dataclass
class TurnResult:
    """What happened on one message."""

    reply: str
    queries: list[str] = field(default_factory=list)
    transcript: list[str] = field(default_factory=list)
    ran_out_of_calls: bool = False


def turns_from(exchanges) -> list[dict]:
    """Return exchanges as chat turns."""
    turns = []
    for user, assistant in exchanges:
        turns += [{"role": "user", "content": user}, {"role": "assistant", "content": assistant}]
    return turns


def search_query(reply: str) -> str | None:
    """Return the query of the first search call in ``reply``, or None if it made no such call."""
    for call in extract_tool_calls_from_text(reply) or []:
        function = call.get("function", {})
        if function.get("name") != SEARCH_TOOL_NAME:
            continue
        arguments = function.get("arguments", {})
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except json.JSONDecodeError:
                return ""
        return str(arguments.get("query", ""))
    return None


def run_turn(
    generate: Callable[[list[dict]], str],
    search: Callable[[str], str],
    system: str,
    view,
    message: str,
) -> TurnResult:
    """Run one message through the loop and return the final reply and every search made."""
    messages = [
        {"role": "system", "content": system},
        *turns_from(view),
        {"role": "user", "content": message},
    ]
    result = TurnResult(reply="")
    for _ in range(MAX_CALLS + 1):
        reply = generate(messages)
        result.transcript.append(reply)
        result.reply = reply
        query = search_query(reply)
        if query is None:
            return result
        result.queries.append(query)
        if len(result.queries) > MAX_CALLS:
            break
        tool_turn = DEFAULT_TOOL_RESULT_FORMAT.format(name=SEARCH_TOOL_NAME, content=search(query))
        messages += [
            {"role": "assistant", "content": reply},
            {"role": "user", "content": tool_turn},
        ]
    result.ran_out_of_calls = True
    return result
