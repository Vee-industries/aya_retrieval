"""The recall tool must search only what left the view, and report a miss as a miss."""

from aya_retrieval.conversations import build_item
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact


def test_searching_the_fact_itself_finds_it(tmp_path):
    item = build_item("x", 3, 58, shares_words=True)
    tool = build_recall_tool(item, tmp_path / "index.sqlite", match_all=False)
    assert search_finds_fact(tool, item, item.older()[item.fact_index][0])


def test_a_query_with_nothing_in_common_is_a_miss(tmp_path):
    item = build_item("x", 3, 58, shares_words=True)
    tool = build_recall_tool(item, tmp_path / "index.sqlite", match_all=False)
    assert not search_finds_fact(tool, item, "zebra xylophone")


def test_a_rebuilt_index_holds_only_the_new_conversation(tmp_path):
    path = tmp_path / "index.sqlite"
    first = build_item("x", 3, 58, shares_words=True)
    second = build_item("x", 4, 58, shares_words=True)
    build_recall_tool(first, path, match_all=False)
    tool = build_recall_tool(second, path, match_all=False)
    assert not tool.backend.search(first.older()[first.fact_index][0].split()[-1] + "zz", top_k=5)
