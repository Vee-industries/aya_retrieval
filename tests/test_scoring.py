"""The scorer must separate a real search call from text that only looks like one."""

import pytest

from aya_retrieval import scoring
from aya_retrieval.scoring import check_scorer, search_counts, searched

CALL = '[{"tool_name": "search_corpus", "parameters": {"query": "meal allowance"}}]'


def test_a_well_formed_call_counts_as_a_search():
    assert searched(CALL)


def test_a_call_followed_by_invented_text_still_counts():
    assert searched(f"{CALL}\nTool result: the allowance is $40")


@pytest.mark.parametrize(
    "reply",
    [
        "Sure, I can help with that.",
        "I would use search_corpus for that.",
        '[{"tool_name": "other_tool", "parameters": {}}]',
        "",
    ],
)
def test_known_bad_replies_do_not_count(reply):
    assert not searched(reply)


def test_the_startup_check_passes_on_the_real_scorer():
    check_scorer()


@pytest.mark.parametrize("always", [True, False])
def test_the_startup_check_fails_on_a_scorer_that_cannot_tell(monkeypatch, always):
    monkeypatch.setattr(scoring, "searched", lambda reply: always)
    with pytest.raises(AssertionError):
        check_scorer()


def test_search_counts_groups_by_kind():
    rows = [
        {"kind": "lookup", "searched": True},
        {"kind": "lookup", "searched": False},
        {"kind": "statement", "searched": False},
    ]
    assert search_counts(rows) == {
        "lookup": {"searched": 1, "of": 2},
        "statement": {"searched": 0, "of": 1},
    }
