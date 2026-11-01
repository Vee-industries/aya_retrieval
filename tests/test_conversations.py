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


@pytest.mark.parametrize("kind", ITEM_KINDS)
def test_the_default_conversation_ignores_the_decoy_option(kind):
    assert astuple(build_item("x", 11, 58, kind, "probe")) == astuple(
        build_item("x", 11, 58, kind, "probe", decoys=1)
    )


@pytest.mark.parametrize("decoys", [0, 1, 2, 3])
@pytest.mark.parametrize("seed", range(20))
def test_decoys_add_facts_about_other_people(seed, decoys):
    item = build_item("x", seed, 58, OLDER, "train", decoys=decoys)
    template = next(fact for fact in TRAIN.facts.values() if item.answer in fact.values)
    told = [user for user, _ in item.older() for value in template.values if value in user]
    assert len(told) == decoys + 1
    assert item.answer in item.older()[item.fact_index][0]


def test_extra_decoys_are_forbidden_in_the_reply():
    item = build_item("x", 4, 58, OLDER, "train", decoys=3)
    assert len(item.forbidden) == 3
    assert item.answer not in item.forbidden


def test_the_confirm_wording_does_not_mean_the_fact_was_told():
    messages = [build_item("x", seed, 58, NEVER_TOLD, "train").message for seed in range(200)]
    confirms = [text for text in messages if text.startswith(("did i", "have i"))]
    assert 60 < len(confirms) < 140


def test_a_never_told_draw_leaves_the_conversation_unchanged():
    """The conversation is drawn first, so base and adapter runs stay comparable by seed."""
    told = build_item("x", 9, 58, OLDER, "train")
    never = build_item("x", 9, 58, NEVER_TOLD, "train")
    assert never.exchanges[-1] == told.exchanges[-1]


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


def opening_shape(statement):
    """Return how a statement sets out the person and relation, ignoring what it says of them."""
    positions = sorted((statement.index(mark), mark) for mark in ("{person}", "{relation}"))
    first, second = positions
    return statement[: second[0] + len(second[1])]


@pytest.mark.parametrize("sealed", [HELDOUT, PROBE])
def test_training_shares_no_way_of_stating_a_fact_with_the_test_pools(sealed):
    train_shapes = {opening_shape(fact.statement) for fact in TRAIN.facts.values()}
    sealed_shapes = {opening_shape(fact.statement) for fact in sealed.facts.values()}
    assert not train_shapes & sealed_shapes


@pytest.mark.parametrize("kind", [OLDER, CONFIRM, NEVER_TOLD])
@pytest.mark.parametrize("seed", range(30))
def test_a_demonstrated_query_uses_no_name_the_message_did_not_give(seed, kind):
    item = build_item("x", seed, 58, kind, "train")
    names = [name for name in TRAIN.people if name in item.query]
    assert all(name in item.message for name in names)
