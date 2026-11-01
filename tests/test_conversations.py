"""A recall item must be reproducible, and its answer must really be out of view."""

import pytest

from aya_retrieval.conversations import EXCHANGES_IN_VIEW, build_item


@pytest.mark.parametrize("messages", [58, 419])
@pytest.mark.parametrize("seed", range(20))
def test_the_answer_and_decoy_are_only_outside_the_view(seed, messages):
    item = build_item("x", seed, messages, shares_words=True)
    in_view = " ".join(user + reply for user, reply in item.view())
    assert item.answer not in in_view
    assert item.decoy not in in_view
    assert item.answer in item.older()[item.fact_index][0]
    assert sum(item.answer in user for user, _ in item.older()) == 1
    assert sum(item.decoy in user for user, _ in item.older()) == 1


def test_the_view_is_the_last_three_exchanges():
    item = build_item("x", 1, 58, shares_words=True)
    assert len(item.view()) == EXCHANGES_IN_VIEW
    assert len(item.older()) + EXCHANGES_IN_VIEW == len(item.exchanges) == 29


def test_a_seed_rebuilds_the_same_conversation():
    assert build_item("x", 7, 58, True) == build_item("x", 7, 58, True)
    assert build_item("x", 7, 58, True) != build_item("x", 8, 58, True)


@pytest.mark.parametrize("seed", range(20))
def test_a_new_words_question_names_nobody_and_never_the_answer(seed):
    item = build_item("x", seed, 58, shares_words=False)
    fact = item.older()[item.fact_index][0]
    person = fact.split()[2]
    assert person not in item.question
    assert item.answer not in item.question
