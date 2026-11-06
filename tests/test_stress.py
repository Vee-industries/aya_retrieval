import random
import re

import pytest

from aya_retrieval.conversations import CONFIRM, IN_VIEW, ITEM_KINDS, OLDER, build_item
from aya_retrieval.pools import POOLS
from aya_retrieval.stress import (
    asked_before,
    corrected,
    phone_style,
    phone_typed,
    typed,
    user_style,
)


def test_typed_lines_are_lower_case_with_sparse_punctuation():
    rng = random.Random(1)
    lines = [typed("Ann's Mum said, Hello! Isn't it Tuesday?", rng) for _ in range(200)]
    assert all(line == line.casefold() and "," not in line and "!" not in line for line in lines)
    assert any(line.endswith("?") for line in lines) and any(
        not line.endswith("?") for line in lines
    )
    assert any("isnt" in line for line in lines) and any("isn't" in line for line in lines)
    ends = [typed("I went out.", rng) for _ in range(600)]
    assert 50 < sum(e.endswith("...") for e in ends) < 150
    assert not any(e.endswith(".") and not e.endswith("...") for e in ends)


@pytest.mark.parametrize("pool", ["probe", "hard_dev"])
def test_user_style_changes_only_the_friends_lines(pool):
    item = build_item("x", 5, 58, OLDER, pool)
    styled = user_style(item, 5)
    assert [r for _, r in styled.exchanges] == [r for _, r in item.exchanges]
    assert all(u == u.casefold() for u, _ in styled.exchanges)
    assert styled.answer == item.answer and styled.message == styled.message.casefold()


@pytest.mark.parametrize("pool", ["probe", "hard_dev", "train"])
@pytest.mark.parametrize("kind", [OLDER, CONFIRM])
@pytest.mark.parametrize("seed", range(40))
def test_a_correction_comes_later_out_of_view_and_changes_the_answer(seed, kind, pool):
    item = build_item("x", seed, 58, kind, pool)
    fixed = corrected(item, seed, pool)
    old_line = fixed.exchanges[fixed.fact_index][0]
    assert item.answer in old_line and fixed.answer != item.answer
    assert item.answer in fixed.forbidden and fixed.answer not in fixed.forbidden
    older = [u for u, _ in fixed.older()]
    view = " ".join(u + " " + r for u, r in fixed.view())
    where = [i for i, u in enumerate(older) if fixed.answer in u]
    assert len(where) == 1 and where[0] > fixed.fact_index
    assert fixed.answer not in view and item.answer not in view
    assert fixed.message == item.message


def test_other_kinds_are_not_corrected():
    item = build_item("x", 3, 58, IN_VIEW, "probe")
    assert corrected(item, 3, "probe") == item


@pytest.mark.parametrize("pool", ["probe", "hard_dev", "train"])
@pytest.mark.parametrize("kind", ITEM_KINDS)
@pytest.mark.parametrize("seed", range(20))
def test_an_earlier_question_declined_sits_in_view_and_nothing_scored_changes(seed, kind, pool):
    item = build_item("x", seed, 58, kind, pool)
    asked = asked_before(item, seed, pool)
    changed = [
        i for i, (a, b) in enumerate(zip(item.exchanges, asked.exchanges, strict=True)) if a != b
    ]
    assert len(changed) == 1 and changed[0] >= len(item.exchanges) - 2
    assert changed[0] != item.fact_index
    question, reply = asked.exchanges[changed[0]]
    assert reply in POOLS[pool].unknown_replies
    assert (asked.message, asked.answer, asked.forbidden) == (
        item.message,
        item.answer,
        item.forbidden,
    )
    others = " ".join([item.message, *(u + " " + r for u, r in item.exchanges)]).casefold()
    assert not any(
        re.search(rf"\b{re.escape(v)}\b", question) for v in (item.answer, item.decoy) if v
    )
    assert asked.exchanges[item.fact_index] == item.exchanges[item.fact_index]
    assert question.casefold() not in others


def adjacent_swap(a: str, b: str) -> bool:
    diff = [i for i, (x, y) in enumerate(zip(a, b, strict=True)) if x != y]
    return (
        len(a) == len(b) and len(diff) == 2 and diff[1] == diff[0] + 1 and a[diff[0]] == b[diff[1]]
    )


def test_phone_typed_drops_apostrophes_shortens_you_and_swaps_one_pair():
    keep = frozenset({"dana", "sister", "pepper"})
    line = phone_typed(
        "Did you know Dana's sister named your puppy Pepper?", random.Random(3), keep
    )
    assert "'" not in line and " u " in line and " ur " in line
    expected = "Did u know Danas sister named ur puppy Pepper?"
    words, plain = line.split(), expected.split()
    changed = [(a, b) for a, b in zip(plain, words, strict=True) if a != b]
    assert len(changed) == 1 and adjacent_swap(*changed[0])
    assert changed[0][0].casefold() not in keep


def test_phone_typed_leaves_kept_and_short_words_alone():
    rng = random.Random(0)
    for _ in range(50):
        assert phone_typed("my sister Dana has a dog", rng, frozenset({"sister"})) == (
            "my sister Dana has a dog"
        )


@pytest.mark.parametrize("pool", ["probe", "hard_dev"])
@pytest.mark.parametrize("kind", ITEM_KINDS)
@pytest.mark.parametrize("seed", range(10))
def test_phone_style_keeps_the_answer_and_the_replies(seed, kind, pool):
    item = build_item("x", seed, 58, kind, pool)
    typed_item = phone_style(item, seed, pool)
    assert [r for _, r in typed_item.exchanges] == [r for _, r in item.exchanges]
    assert typed_item.answer == item.answer
    if item.answer:
        fact_line = typed_item.exchanges[item.fact_index][0] if item.fact_index is not None else ""
        assert item.answer in fact_line or item.fact_index is None


def test_shares_wording_catches_rewordings_and_passes_new_ones():
    from aya_retrieval.stress import TRAIN_CORRECTION_OPENINGS, content_words, shares_wording

    assert content_words("Wait, NO, it's...") == frozenset({"wait", "no", "s"})
    assert shares_wording("hang on, i said it WRONG", (" (i said it wrong last time)",))
    assert shares_wording("Scratch THAT, ", TRAIN_CORRECTION_OPENINGS)
    assert not shares_wording("hmm let me redo that one, ", ("wait no, ",))
