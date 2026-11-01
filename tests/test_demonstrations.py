"""A demonstration must show the right habit and stay true to what the tool returned."""

import json

import pytest

from aya_retrieval.conversations import CONFIRM, IN_VIEW, NEVER_TOLD, OLDER, STATEMENT, build_item
from aya_retrieval.demonstrations import as_event_log, demonstration_turns, search_call
from aya_retrieval.scoring import clean_call


def turns(kind, found=True):
    item = build_item("x", 5, 58, kind, "train")
    return item, demonstration_turns(
        item, "RESULT TEXT", "base's own reply", found, "I don't know."
    )


@pytest.mark.parametrize("kind", [STATEMENT, IN_VIEW])
def test_no_search_is_shown_when_none_is_needed(kind):
    item, result = turns(kind)
    assert result[-1] == {"role": "assistant", "content": "base's own reply"}
    assert result[-2] == {"role": "user", "content": item.message}


@pytest.mark.parametrize("kind", [OLDER, CONFIRM, NEVER_TOLD])
def test_a_search_is_a_clean_call_then_an_answer_from_the_result(kind):
    item, result = turns(kind)
    assert clean_call(result[-3]["content"])
    assert "RESULT TEXT" in result[-2]["content"]
    assert result[-1]["content"] == item.reply


def test_a_search_that_missed_never_shows_the_answer():
    item, result = turns(OLDER, found=False)
    assert result[-1]["content"] == "I don't know."
    assert item.answer not in result[-1]["content"]


def test_the_call_carries_the_query():
    assert json.loads(search_call("sister dog"))[0]["parameters"]["query"] == "sister dog"


@pytest.mark.parametrize("kind", [OLDER, STATEMENT])
def test_agenttune_renders_the_trajectory_back_to_the_same_turns(kind):
    _, result = turns(kind)
    assert as_event_log(result).as_dataset_rows("sft")[0]["messages"] == result
