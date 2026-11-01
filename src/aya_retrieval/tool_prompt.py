"""The search tool as Tiny Aya sees it, rendered through AgentTune's own fallback prompt.

Tiny Aya's chat template ignores ``tools``, so the schema goes into the system prompt. Using
AgentTune's text keeps these prompts identical to what its training rollouts send.
"""

from __future__ import annotations

import json

from agenttune.agentic.rollout_engines.rollout_factory import DEFAULT_TOOLS_FALLBACK_PROMPT

SEARCH_TOOL_NAME = "search_corpus"

SEARCH_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": SEARCH_TOOL_NAME,
            "description": (
                "Search the document corpus for passages relevant to a query. "
                "Returns ranked chunks, each tagged with a chunk_id you can cite."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query — keywords or a natural-language question.",
                    }
                },
                "required": ["query"],
            },
        },
    }
]


def system_prompt_with_tools(system_prompt: str) -> str:
    """Return ``system_prompt`` followed by the search tool's schema and calling format."""
    tools = DEFAULT_TOOLS_FALLBACK_PROMPT.format(tools=json.dumps(SEARCH_SCHEMA, indent=2))
    return f"{system_prompt}\n\n{tools}"
