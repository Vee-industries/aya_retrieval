"""R-178's options: facts of other types (F2), earlier answers in view (F3) and the dev stresses.

Every default output must be byte for byte as before: the fingerprints below were made by
``default_fingerprints.py`` on the code before these options existed (commit 8e73cf0).
"""

import re

import pytest
from default_fingerprints import (
    BUILD_FLAGS,
    EVAL_FLAGS,
    builder_fingerprint,
    eval_fingerprint,
    item_fingerprint,
)

from aya_retrieval.conversations import (
    CONFIRM,
    EXCHANGES_IN_VIEW,
    IN_VIEW,
    ITEM_KINDS,
    NEVER_TOLD,
    OLDER,
    OTHER_FACT_SHARES,
    STATEMENT,
    add_other_facts,
    build_item,
)
from aya_retrieval.demonstrations import values_named
from aya_retrieval.pools import POOLS
from aya_retrieval.scoring import item_correct
from aya_retrieval.stress import earlier_answers, told_facts, wrong_before

BEFORE = {
    "items": "8dd3b1eabb02dac4927812d6eacb4dce324a1c8c65df98e2b072b8179b6feceb",
    "build_default": "514170b2fd22299f05504b65842092d6634781d34b72fd1d40d5912c4c1ed5f3",
    "build_fix637": "4f8a65454eebd087e5b74c4ee77f85ffe25ec0e85d185e33b1d2c0892dd293f6",
    "build_other": "1fc16ba443650df19b92b5955570e9299b8b74172f79e15da21cf63264559f7b",
    "eval_train": "3a0b86f1123a97c8c338723ea9607c2016e38965d3755e8bfafc934472df9d51",
    "eval_train_stressed": "18c5b760f7bdba7507ce4ec673b28354bebcdb3860a31de79798bbb44f94f450",
    "eval_probe": "499e9619f9fc9a43db2107a5e283f66aa385612a66e8d2bcb45ff7ddbe16236b",
    "eval_hard_dev": "55d13e8ff1379bef03c7a0592b447984ba8c346c079487e8e147c957036fac4d",
}
SEEDS = range(40)


def test_default_conversations_are_as_before():
    assert item_fingerprint() == BEFORE["items"]


@pytest.mark.parametrize("name", sorted(BUILD_FLAGS))
def test_a_default_training_build_is_as_before(tmp_path, name):
    assert builder_fingerprint(tmp_path, BUILD_FLAGS[name]) == BEFORE[f"build_{name}"]


@pytest.mark.parametrize("name", sorted(EVAL_FLAGS))
def test_a_default_evaluation_is_as_before(tmp_path, name):
    assert eval_fingerprint(tmp_path, EVAL_FLAGS[name]) == BEFORE[f"eval_{name}"]


@pytest.mark.parametrize(
    ("make", "flags", "known"),
    [
        (builder_fingerprint, ["--other-facts"], "build_default"),
        (builder_fingerprint, ["--earlier-answers", "1", "--reask-rows", "2"], "build_default"),
        (eval_fingerprint, ["--pool", "probe", "--wrong-before"], "eval_probe"),
        (eval_fingerprint, ["--pool", "probe", "--other-facts"], "eval_probe"),
    ],
)
def test_the_fingerprint_catches_a_changed_output(tmp_path, make, flags, known):
    # The check above is believed only because it fails when the output does change.
    assert make(tmp_path, flags) != BEFORE[known]


@pytest.mark.parametrize("flags", [["--wrong-before"], ["--other-facts"]])
def test_the_dev_stresses_refuse_the_training_pool(tmp_path, flags):
    with pytest.raises(SystemExit):
        eval_fingerprint(tmp_path, ["--pool", "train", *flags])


def free_slots_changed(before, after):
    pairs = zip(before.exchanges, after.exchanges, strict=True)
    return [i for i, (a, b) in enumerate(pairs) if a != b]


@pytest.mark.parametrize("pool", ["train", "probe", "hard_dev"])
@pytest.mark.parametrize("kind", ITEM_KINDS)
@pytest.mark.parametrize("share", OTHER_FACT_SHARES)
def test_other_facts_change_only_out_of_view_small_talk(pool, kind, share):
    values = [v for t in POOLS[pool].facts.values() for v in t.values]
    for seed in SEEDS:
        plain = build_item("x", seed, 58, kind, pool, 1)
        other = build_item("x", seed, 58, kind, pool, 1, other_facts=share)
        assert (other.message, other.answer, other.forbidden, other.query, other.reply) == (
            plain.message,
            plain.answer,
            plain.forbidden,
            plain.query,
            plain.reply,
        )
        assert other.view() == plain.view()
        changed = free_slots_changed(plain, other)
        assert 2 <= len(changed) <= 5
        for slot in changed:
            assert slot < len(plain.exchanges) - EXCHANGES_IN_VIEW
            assert not any(v in plain.exchanges[slot][0] for v in values)


def asked_pair(item, pool):
    """The relation and person of the item's final question, read from its fact or its message."""
    facts = told_facts(item, pool)
    own = [f for f in facts if f.slot == item.fact_index and f.value == item.answer]
    return (own[0].relation, own[0].person) if own else None


@pytest.mark.parametrize("kind", [OLDER, CONFIRM])
def test_the_same_person_share_states_another_type_about_the_asked_person(kind):
    for seed in SEEDS:
        item = build_item("x", seed, 58, kind, "train", 1, other_facts="same_person")
        who = asked_pair(item, "train")
        own_type = next(f.fact_type for f in told_facts(item, "train") if f.value == item.answer)
        about = [
            f
            for f in told_facts(item, "train")
            if (f.relation, f.person) == who and f.fact_type != own_type
        ]
        assert about


@pytest.mark.parametrize("kind", [OLDER, CONFIRM, NEVER_TOLD])
@pytest.mark.parametrize("share", ["same_type", "shared_word"])
def test_the_other_shares_state_nothing_more_about_the_asked_person(kind, share):
    for seed in SEEDS:
        plain = build_item("x", seed, 58, kind, "train", 1)
        other = build_item("x", seed, 58, kind, "train", 1, other_facts=share)
        added = [f for f in told_facts(other, "train") if f not in told_facts(plain, "train")]
        names = {f.person for f in told_facts(plain, "train")}
        assert added and not any(f.person in names for f in added)
        assert not any(f.person in other.message for f in added)


def test_the_first_added_type_is_stated_twice_so_a_wrong_value_exists():
    for seed in SEEDS:
        plain = build_item("x", seed, 58, OLDER, "train", 0)
        other = build_item("x", seed, 58, OLDER, "train", 0, other_facts="same_type")
        added = [f for f in told_facts(other, "train") if f not in told_facts(plain, "train")]
        types = [f.fact_type for f in added]
        assert any(types.count(t) == 2 for t in types)


@pytest.mark.parametrize("pool", ["train", "probe", "hard_dev"])
def test_the_shared_word_line_shares_a_query_word_and_names_no_one(pool):
    people = POOLS[pool].people
    values = [v for t in POOLS[pool].facts.values() for v in t.values]
    for seed in SEEDS:
        item = build_item("x", seed, 58, NEVER_TOLD, pool, 1, other_facts="shared_word")
        plain = build_item("x", seed, 58, NEVER_TOLD, pool, 1)
        changed = [item.exchanges[i][0] for i in free_slots_changed(plain, item)]
        (line,) = [line for line in changed if not any(v in line for v in values)]
        assert set(item.query.casefold().split()[1:]) & set(re.findall(r"[a-z]+", line.casefold()))
        assert not any(p in line for p in people)


def test_build_item_other_facts_is_add_other_facts_on_the_default_item():
    item = build_item("x", 11, 58, NEVER_TOLD, "train", 2)
    asked = ("cousin", "Dana")
    once = add_other_facts(item, 11, "train", "same_person", asked)
    assert once == add_other_facts(item, 11, "train", "same_person", asked)
    with pytest.raises(ValueError):
        add_other_facts(item, 11, "train", "nobody", asked)


def test_told_facts_finds_the_fact_and_the_decoys():
    for seed in SEEDS:
        item = build_item("x", seed, 58, OLDER, "train", 3)
        values = {f.value for f in told_facts(item, "train")}
        assert item.answer in values
        assert set(item.forbidden) <= values


@pytest.mark.parametrize("kind", ITEM_KINDS)
def test_earlier_answers_sit_in_view_and_their_values_are_forbidden(kind):
    built = 0
    for seed in SEEDS:
        item = build_item("x", seed, 58, kind, "train", 1, other_facts="same_person")
        result = earlier_answers(item, seed, "train")
        if result is None:
            continue
        built += 1
        changed, used, given = result
        slots = free_slots_changed(item, changed)
        assert 1 <= len(slots) <= 2 and len(used) == len(slots)
        assert all(s >= len(item.exchanges) - EXCHANGES_IN_VIEW for s in slots)
        assert item.fact_index not in slots
        assert set(given) <= set(changed.forbidden)
        assert item.answer not in given
        assert (changed.message, changed.answer, changed.query) == (
            item.message,
            item.answer,
            item.query,
        )
        assert set(used) <= {"right", "wrong", "declined"}
        if item.kind in (OLDER, CONFIRM, IN_VIEW):
            assert item_correct(kind, item.reply, item.answer, changed.forbidden, 1)
    assert built >= len(SEEDS) // 2


@pytest.mark.parametrize("kind", [OLDER, CONFIRM])
def test_a_reask_answers_the_items_own_question_with_a_wrong_value_from_the_chat(kind):
    for seed in SEEDS:
        item = build_item("x", seed, 58, kind, "train", 2)
        changed, used, given = earlier_answers(item, seed, "train", reask=True)
        assert used == ("wrong",) and len(given) == 1
        (slot,) = free_slots_changed(item, changed)
        _, reply = changed.exchanges[slot]
        assert given[0] in reply and given[0] in {f.value for f in told_facts(item, "train")}
        assert given[0] != item.answer and given[0] in changed.forbidden


@pytest.mark.parametrize("kind", [IN_VIEW, NEVER_TOLD, STATEMENT])
def test_a_reask_needs_an_older_or_confirm_item(kind):
    assert earlier_answers(build_item("x", 1, 58, kind, "train", 2), 1, "train", True) is None


def test_a_reask_needs_another_value_of_its_type_in_the_chat():
    item = build_item("x", 4, 58, OLDER, "train", 0)
    assert earlier_answers(item, 4, "train", reask=True) is None


@pytest.mark.parametrize("pool", ["probe", "hard_dev"])
@pytest.mark.parametrize("kind", [OLDER, CONFIRM, IN_VIEW])
def test_wrong_before_puts_the_own_question_answered_with_the_decoy_in_view(pool, kind):
    for seed in SEEDS:
        item = build_item("x", seed, 58, kind, pool, 1)
        changed = wrong_before(item, seed, pool)
        (slot,) = free_slots_changed(item, changed)
        assert slot >= len(item.exchanges) - EXCHANGES_IN_VIEW and slot != item.fact_index
        question, reply = changed.exchanges[slot]
        assert question == item.message and item.decoy in reply and item.answer not in reply
        assert item.decoy in changed.forbidden
        assert (changed.message, changed.answer, changed.forbidden) == (
            item.message,
            item.answer,
            item.forbidden,
        )


@pytest.mark.parametrize("kind", [NEVER_TOLD, STATEMENT])
def test_wrong_before_leaves_other_kinds_alone(kind):
    item = build_item("x", 3, 58, kind, "probe", 1)
    assert wrong_before(item, 3, "probe") is item


def test_values_named_reads_values_as_the_scorer_does_and_keeps_the_answer():
    text = "User: my sister Dana adopted a dog named Pepper; her cousin drives a red civic"
    assert values_named(text, "train") == ("red Civic", "Pepper")
    assert values_named(text, "train", keep="Pepper") == ("red Civic",)
    assert values_named("nothing here", "train") == ()
