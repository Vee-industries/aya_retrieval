"""The live chat keeps evaluation's view, search and prompt."""

import json
from pathlib import Path

from aya_retrieval.chat import MAX_TOKENS, SYSTEM_WITH_TOOL, Chat
from aya_retrieval.conversations import EXCHANGES_IN_VIEW
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME

REPO = Path(__file__).resolve().parents[1]


def scripted_model(seen: list[list[dict]]):
    """Search once for 'cello' on the last message, then answer with what came back."""

    def generate(messages: list[dict]) -> str:
        seen.append(list(messages))
        last = messages[-1]["content"]
        if last.startswith("what instrument"):
            return json.dumps([{"tool_name": SEARCH_TOOL_NAME, "parameters": {"query": "cello"}}])
        if "Tool result" in last:
            return "cello" if "cello" in last else "I don't know."
        return "ok"

    return generate


def test_the_view_holds_only_the_last_exchanges_and_older_ones_are_searched(tmp_path):
    seen: list[list[dict]] = []
    chat = Chat(scripted_model(seen), tmp_path / "chat.sqlite")
    chat.send("my cousin Ines plays the cello")
    for n in range(EXCHANGES_IN_VIEW):
        chat.send(f"small talk {n}")
    result = chat.send("what instrument does Ines play")

    first = seen[-2]
    assert first[0] == {"role": "system", "content": first[0]["content"]}
    assert SYSTEM_WITH_TOOL in first[0]["content"]
    assert all("cello" not in m["content"] for m in first[1:])
    assert len(first) == 1 + 2 * EXCHANGES_IN_VIEW + 1
    assert result.queries == ["cello"]
    assert result.reply == "cello"
    assert len(chat.exchanges) == EXCHANGES_IN_VIEW + 2


def test_a_search_with_nothing_out_of_view_returns_the_tools_own_empty_result(tmp_path):
    seen: list[list[dict]] = []
    chat = Chat(scripted_model(seen), tmp_path / "chat.sqlite")
    result = chat.send("what instrument does Ines play")
    assert "No results found." in seen[-1][-1]["content"]
    assert result.reply == "I don't know."


def test_the_system_prompt_and_reply_length_are_the_evaluations():
    source = (REPO / "scripts" / "run_recall_eval.py").read_text(encoding="utf-8")
    assert f'SYSTEM_WITH_TOOL = "{SYSTEM_WITH_TOOL}"' in source
    assert f"\nMAX_TOKENS = {MAX_TOKENS}\n" in source
