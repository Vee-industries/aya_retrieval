import random

import pytest

from aya_retrieval.conversations import CONFIRM, IN_VIEW, OLDER, build_item
from aya_retrieval.stress import corrected, typed, user_style


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
