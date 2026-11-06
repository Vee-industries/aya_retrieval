"""Reading a reply: did the model call the search tool? Parsing is AgentTune's own."""

from __future__ import annotations

import json
import re

from agenttune.agentic.rollout_engines.rollout_factory import extract_tool_calls_from_text

from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME


def searched(reply: str) -> bool:
    """Return True if AgentTune's parser finds a call to the search tool in ``reply``."""
    calls = extract_tool_calls_from_text(reply) or []
    return any(call.get("function", {}).get("name") == SEARCH_TOOL_NAME for call in calls)


def clean_call(reply: str) -> bool:
    """Return True if the whole reply is one search call, with nothing written after it.

    A model that stops here waits for the real result. Anything after the call is text the model
    wrote in place of that result.
    """
    try:
        calls = json.loads(reply)
    except json.JSONDecodeError:
        return False
    return (
        isinstance(calls, list)
        and len(calls) == 1
        and isinstance(calls[0], dict)
        and calls[0].get("tool_name") == SEARCH_TOOL_NAME
    )


def answer_correct(reply: str, answer: str, decoy: str) -> bool:
    """Return True if the reply gives the planted answer and does not also give the decoy.

    The decoy rule fails a reply that dumps every passage it was handed, which a plain substring
    check would pass.
    """
    text = reply.casefold()
    return answer.casefold() in text and decoy.casefold() not in text


def item_correct(
    kind: str, reply: str, answer: str, forbidden: tuple[str, ...], calls: int
) -> bool:
    """Return True if the reply does what a message of ``kind`` calls for.

    A statement needs no search. A question about something never told must not name any value of
    that kind, since any it names is made up or belongs to someone else. The rest must give the
    planted answer and no forbidden value.
    """
    text = reply.casefold()
    names_forbidden = any(value.casefold() in text for value in forbidden)
    if kind == "statement":
        return calls == 0
    if kind == "never_told":
        return not names_forbidden
    return answer.casefold() in text and not names_forbidden


def right_decision(kind: str, calls: int) -> bool:
    """Return True if the model searched exactly when the answer was out of its view."""
    return (calls > 0) == (kind in ("older", "confirm", "never_told"))


def check_scorer() -> None:
    """Raise unless the scorer accepts a real call and rejects text that only looks like one."""
    call = f'[{{"tool_name": "{SEARCH_TOOL_NAME}", "parameters": {{"query": "meal allowance"}}}}]'
    known_bad = [
        "Sure, I can help with that.",
        f"I would use {SEARCH_TOOL_NAME} for that.",
        '[{"tool_name": "other_tool", "parameters": {}}]',
    ]
    if not searched(call):
        raise AssertionError("scorer missed a well-formed call")
    for reply in known_bad:
        if searched(reply):
            raise AssertionError(f"scorer accepted a known-bad reply: {reply}")


def search_counts(rows: list[dict]) -> dict[str, dict[str, int]]:
    """Return, per item kind, how many rows searched out of how many there were."""
    counts = {}
    for kind in sorted({row["kind"] for row in rows}):
        chosen = [row for row in rows if row["kind"] == kind]
        counts[kind] = {"searched": sum(row["searched"] for row in chosen), "of": len(chosen)}
    return counts


def clean_call_count(rows: list[dict]) -> dict[str, int]:
    """Return how many searching rows were a clean call, out of how many searched."""
    searching = [row for row in rows if row["searched"]]
    return {"clean": sum(clean_call(row["reply"]) for row in searching), "of": len(searching)}


def slip_shape(reply: str, message: str) -> bool:
    """Return True if the reply pins the friend's relation on the wrong person or on the speaker.

    The who-is-who slip (R-094): "Hana's barber is scared of clowns." for "what is my barber scared
    of", where the barber is Hana. The relation is the word after "my" in the friend's message; the
    shapes are "<Name>'s <relation>" (not counted when the friend's message has the same words), a
    sentence that opens "My <relation>", and "who is my". The scorer passes such replies when they
    name the value, so this counts them apart.
    """
    said = message.casefold()
    if re.search(r"\bwho is my\b", reply, re.IGNORECASE):
        return True
    for relation in re.findall(r"\bmy ([a-z]+)", said):
        if re.search(rf"(?:^|[.!?]\s+)My {relation}\b", reply):
            return True
        for hit in re.finditer(rf"\b[A-Z][a-z]+'s {relation}\b", reply):
            if hit.group(0).casefold() not in said:
                return True
    return False
