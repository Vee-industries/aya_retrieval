"""A demonstration must show the right habit and stay true to what the tool returned."""

import json
import re

import pytest

from aya_retrieval.conversations import CONFIRM, IN_VIEW, NEVER_TOLD, OLDER, STATEMENT, build_item
from aya_retrieval.demonstrations import (
    as_event_log,
    demonstration_turns,
    message_words_query,
    missing_words_query,
    search_call,
    whole_sentences,
)
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
def test_a_search_is_a_clean_call_then_a_reply_to_the_result(kind):
    _, result = turns(kind)
    assert clean_call(result[-3]["content"])
    assert "RESULT TEXT" in result[-2]["content"]


@pytest.mark.parametrize("kind", [OLDER, CONFIRM])
def test_a_found_fact_teaches_the_given_reply(kind):
    _, result = turns(kind)
    assert result[-1]["content"] == "base's own reply"


def test_never_told_teaches_saying_so_whatever_base_wrote():
    item, result = turns(NEVER_TOLD, found=False)
    assert result[-1]["content"] == item.reply


def test_a_cut_off_reply_is_trimmed_to_its_last_sentence():
    assert whole_sentences("That's nice. Did she like it? Maybe we could") == (
        "That's nice. Did she like it?"
    )
    assert whole_sentences("no sentence ends here") is None


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


def _rows():
    sizes = (("older", 8), ("confirm", 6))
    return [{"id": f"{kind}_{i}", "kind": kind} for kind, n in sizes for i in range(n)]


def test_kind_balanced_subset_takes_the_same_share_of_each_kind():
    from collections import Counter

    from aya_retrieval.demonstrations import kind_balanced_subset

    subset = kind_balanced_subset(_rows(), 0.5, seed=1)
    assert Counter(row["kind"] for row in subset) == {"older": 4, "confirm": 3}


def test_kind_balanced_subset_keeps_order_and_repeats_on_the_same_seed():
    from aya_retrieval.demonstrations import kind_balanced_subset

    rows = _rows()
    first = kind_balanced_subset(rows, 0.5, seed=1)
    assert first == kind_balanced_subset(rows, 0.5, seed=1)
    assert [rows.index(row) for row in first] == sorted(rows.index(row) for row in first)


@pytest.mark.parametrize("kind", [OLDER, CONFIRM, NEVER_TOLD])
def test_an_empty_first_search_comes_before_the_real_one(kind):
    item = build_item("x", 5, 58, kind, "train")
    result = demonstration_turns(
        item, "RESULT TEXT", "base's own reply", True, "I don't know.", ("lost words", "NONE")
    )
    assert json.loads(result[-5]["content"])[0]["parameters"]["query"] == "lost words"
    assert "NONE" in result[-4]["content"]
    assert json.loads(result[-3]["content"])[0]["parameters"]["query"] == item.query
    assert "RESULT TEXT" in result[-2]["content"]


def test_the_missing_words_query_uses_no_word_said_earlier():
    for seed in range(20):
        item = build_item("x", seed, 58, OLDER, "train")
        query = missing_words_query(item)
        earlier = " ".join(u + " " + a for u, a in item.older()).lower()
        assert query is None or not set(query.split()) & set(re.findall(r"[a-z']+", earlier))


def test_a_message_words_query_uses_only_the_message_and_leads_with_who_was_asked_about():
    for seed in range(40):
        for kind in (OLDER, CONFIRM):
            item = build_item("x", seed, 58, kind, "train", 1, True)
            query = message_words_query(item)
            words = query.split()
            assert words[0] == item.query.split()[0]
            message = {t.removesuffix("'s") for t in re.findall(r"[a-z']+", item.message.lower())}
            assert all(w.lower() in message for w in words)
            assert len(words) == len(set(words)) <= 4
