"""The scorer must separate a real search call from text that only looks like one."""

import pytest

from aya_retrieval import scoring
from aya_retrieval.scoring import (
    answer_correct,
    check_scorer,
    clean_call,
    clean_call_count,
    item_correct,
    right_decision,
    search_counts,
    searched,
)

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


def test_a_lone_call_is_clean():
    assert clean_call(CALL)


@pytest.mark.parametrize(
    "reply",
    [
        f"{CALL}\nTool result: the allowance is $40",
        f"Tool result\n{CALL}",
        '[{"tool_name": "other_tool", "parameters": {}}]',
        f"[{CALL[1:-1]}, {CALL[1:-1]}]",
        "Sure, I can help with that.",
    ],
)
def test_anything_more_or_other_than_one_search_call_is_not_clean(reply):
    assert not clean_call(reply)


def test_clean_call_count_is_out_of_the_rows_that_searched():
    rows = [
        {"reply": CALL, "searched": True},
        {"reply": f"{CALL}\nTool result: invented", "searched": True},
        {"reply": "Thanks for telling me.", "searched": False},
    ]
    assert clean_call_count(rows) == {"clean": 1, "of": 2}


@pytest.mark.parametrize(
    ("reply", "expected"),
    [
        ("Her dog is called pepper.", True),
        ("I don't know.", False),
        ("The dog is Rusty.", False),
        ("Passages: Pepper, Rusty.", False),
    ],
)
def test_answer_correct_needs_the_answer_and_not_the_decoy(reply, expected):
    assert answer_correct(reply, "Pepper", "Rusty") is expected


@pytest.mark.parametrize(
    ("kind", "reply", "calls", "expected"),
    [
        ("older", "It is Pepper.", 1, True),
        ("older", "Pepper or Rusty.", 1, False),
        ("older", "I don't know.", 1, False),
        ("never_told", "You haven't told me.", 1, True),
        ("never_told", "Probably Rusty.", 1, False),
        ("statement", "Nice.", 0, True),
        ("statement", "Nice.", 1, False),
    ],
)
def test_item_correct(kind, reply, calls, expected):
    assert item_correct(kind, reply, "Pepper", ("Rusty",), calls) is expected


@pytest.mark.parametrize(
    ("kind", "calls", "expected"),
    [
        ("older", 1, True),
        ("older", 0, False),
        ("confirm", 1, True),
        ("never_told", 2, True),
        ("in_view", 0, True),
        ("in_view", 1, False),
        ("statement", 0, True),
        ("statement", 1, False),
    ],
)
def test_right_decision(kind, calls, expected):
    assert right_decision(kind, calls) is expected


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


@pytest.mark.parametrize(
    ("reply", "message"),
    [
        ("Hana's barber is scared of clowns.", "i'm blanking on what my barber is scared of"),
        ("Chidi, who is my daughter, joined a water polo club.", "which club did Chidi join"),
        (
            "My godfather, Lucia, speaks fluent Turkish.",
            "what can my godfather speak besides english",
        ),
        ("It seems like Omar's aunt broke her forearm.", "my aunt hurt something skiing"),
    ],
)
def test_a_relation_pinned_on_the_wrong_person_is_a_slip(reply, message):
    assert scoring.slip_shape(reply, message)


@pytest.mark.parametrize(
    ("reply", "message"),
    [
        ("Your barber Hana is scared of clowns.", "i'm blanking on what my barber is scared of"),
        ("Your daughter Chidi joined a water polo club.", "which club did Chidi join"),
        ("Your godfather Lucia speaks Turkish.", "is it lucia's godfather or my godfather"),
        (
            "Not Lucia's godfather, yours.",
            "is it lucia's godfather who speaks turkish, or my godfather",
        ),
    ],
)
def test_the_right_shape_or_the_friends_own_words_are_not_a_slip(reply, message):
    assert not scoring.slip_shape(reply, message)
