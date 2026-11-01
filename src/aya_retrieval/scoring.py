"""Reading a reply: did the model call the search tool? Parsing is AgentTune's own."""

from __future__ import annotations

from agenttune.agentic.rollout_engines.rollout_factory import extract_tool_calls_from_text

from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME


def searched(reply: str) -> bool:
    """Return True if AgentTune's parser finds a call to the search tool in ``reply``."""
    calls = extract_tool_calls_from_text(reply) or []
    return any(call.get("function", {}).get("name") == SEARCH_TOOL_NAME for call in calls)


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
