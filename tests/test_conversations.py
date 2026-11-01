"""Conversations must be reproducible, varied, and honest about what is in view."""

from collections import Counter
from dataclasses import astuple
from itertools import combinations

import pytest

from aya_retrieval.conversations import (
    CONFIRM,
    EXCHANGES_IN_VIEW,
    IN_VIEW,
    ITEM_KINDS,
    NEVER_TOLD,
    OLDER,
    STATEMENT,
    build_item,
)
from aya_retrieval.pools import HELDOUT, PROBE, TRAIN

POOL_NAMES = ("train", "heldout", "probe")


@pytest.mark.parametrize("pool", POOL_NAMES)
@pytest.mark.parametrize("messages", [58, 419])
@pytest.mark.parametrize("seed", range(15))
def test_an_older_answer_is_only_outside_the_view(seed, messages, pool):
    item = build_item("x", seed, messages, OLDER, pool)
    in_view = " ".join(user + reply for user, reply in item.view())
    assert item.answer not in in_view
    assert item.decoy not in in_view
    assert item.answer in item.older()[item.fact_index][0]
    assert sum(item.answer in user for user, _ in item.older()) == 1
    assert sum(item.decoy in user for user, _ in item.older()) == 1


@pytest.mark.parametrize("seed", range(15))
def test_an_in_view_answer_is_in_view(seed):
    item = build_item("x", seed, 58, IN_VIEW, "train")
    assert item.answer in " ".join(user for user, _ in item.view())


@pytest.mark.parametrize("seed", range(15))
def test_a_never_told_conversation_does_not_hold_the_answer_to_its_question(seed):
    item = build_item("x", seed, 58, NEVER_TOLD, "train")
    told = " ".join(user for user, _ in item.exchanges)
    assert item.answer == ""
    assert item.decoy in told
    assert not any(value in told for value in item.forbidden if value != item.decoy)


@pytest.mark.parametrize("seed", range(15))
def test_a_statement_has_nothing_to_answer_or_search(seed):
    item = build_item("x", seed, 58, STATEMENT, "train")
    assert item.answer == ""
    assert item.query == ""


def test_a_confirm_message_does_not_give_the_answer_away():
    item = build_item("x", 2, 58, CONFIRM, "train")
    assert item.answer not in item.message


def test_the_view_is_the_last_three_exchanges():
    item = build_item("x", 1, 58, OLDER, "train")
    assert len(item.view()) == EXCHANGES_IN_VIEW
    assert len(item.older()) + EXCHANGES_IN_VIEW == len(item.exchanges) == 29


@pytest.mark.parametrize("kind", ITEM_KINDS)
def test_a_seed_rebuilds_the_same_conversation(kind):
    assert astuple(build_item("x", 7, 58, kind, "train")) == astuple(
        build_item("x", 7, 58, kind, "train")
    )


@pytest.mark.parametrize("pool", POOL_NAMES)
def test_no_reply_dominates_a_long_conversation(pool):
    item = build_item("x", 3, 419, OLDER, pool)
    replies = Counter(reply for _, reply in item.exchanges)
    assert replies.most_common(1)[0][1] <= len(item.exchanges) * 0.08


@pytest.mark.parametrize("first, second", list(combinations((TRAIN, HELDOUT, PROBE), 2)))
def test_the_pools_share_no_content(first, second):
    assert not set(first.people) & set(second.people)
    assert not set(first.relations) & set(second.relations)
    assert not set(first.subjects) & set(second.subjects)
    assert not set(first.facts) & set(second.facts)
    assert not set(first.acknowledgements) & set(second.acknowledgements)
    assert not set(first.unknown_replies) & set(second.unknown_replies)
    first_values = {value for fact in first.facts.values() for value in fact.values}
    second_values = {value for fact in second.facts.values() for value in fact.values}
    assert not first_values & second_values


@pytest.mark.parametrize("kind", [OLDER, CONFIRM, NEVER_TOLD])
@pytest.mark.parametrize("seed", range(30))
def test_a_demonstrated_query_uses_no_name_the_message_did_not_give(seed, kind):
    item = build_item("x", seed, 58, kind, "train")
    names = [name for name in TRAIN.people if name in item.query]
    assert all(name in item.message for name in names)
