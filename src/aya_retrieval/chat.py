"""A live chat in the harness the adapter was trained and tested in.

The model sees the last ``EXCHANGES_IN_VIEW`` exchanges. Everything older is indexed, one passage
per exchange, and reachable only through the search tool, exactly as in evaluation.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from aya_retrieval.conversations import EXCHANGES_IN_VIEW
from aya_retrieval.harness import TurnResult, run_turn
from aya_retrieval.recall_tool import build_search_tool
from aya_retrieval.tool_prompt import system_prompt_with_tools

# The evaluation's tool-loop system prompt and reply length (scripts/run_recall_eval.py).
SYSTEM_WITH_TOOL = "You are chatting with a friend. You can search the earlier conversation."
MAX_TOKENS = 60


@dataclass
class Chat:
    """One conversation: every exchange so far, and the search index over those out of view."""

    generate: Callable[[list[dict]], str]
    index: Path
    exchanges: list[tuple[str, str]] = field(default_factory=list)

    def send(self, message: str) -> TurnResult:
        """Answer ``message`` from the view and the search tool, then add the exchange."""
        older = self.exchanges[: max(len(self.exchanges) - EXCHANGES_IN_VIEW, 0)]
        tool = build_search_tool(older, self.index, match_all=False)

        def search(query: str) -> str:
            result = tool.execute(query)
            return result.output if result.success else str(result.error)

        view = self.exchanges[-EXCHANGES_IN_VIEW:]
        system = system_prompt_with_tools(SYSTEM_WITH_TOOL)
        result = run_turn(self.generate, search, system, view, message)
        self.exchanges.append((message, result.reply))
        return result
