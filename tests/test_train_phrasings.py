from aya_retrieval.conversations import build_item
from aya_retrieval.pools import HELDOUT, POOLS, PROBE, TRAIN
from aya_retrieval.train_phrasings import MORE_INDIRECT, MORE_STATEMENTS

PROBE_IDIOMS = ("blank", "tip of my tongue", "cannot think")


def test_every_train_template_has_three_more_phrasings_and_no_other_key():
    train = {t.indirect for t in TRAIN.facts.values()}
    assert set(MORE_INDIRECT) == train
    assert all(len(extra) == 3 for extra in MORE_INDIRECT.values())


def test_each_phrasing_names_the_relation_and_nothing_else():
    for extra in MORE_INDIRECT.values():
        for phrasing in extra:
            assert "{relation}" in phrasing
            assert phrasing.format(relation="aunt")


def test_no_phrasing_uses_a_probe_idiom():
    probe = " ".join(t.indirect for t in PROBE.facts.values())
    assert all(idiom in probe for idiom in PROBE_IDIOMS)
    for extra in MORE_INDIRECT.values():
        for phrasing in extra:
            assert not any(idiom in phrasing for idiom in PROBE_IDIOMS)


def test_more_indirect_changes_only_the_question():
    changed = 0
    for seed in range(200):
        plain = build_item("x", seed, 58, "older", "train")
        more = build_item("x", seed, 58, "older", "train", more_indirect=True)
        assert plain.exchanges == more.exchanges and plain.answer == more.answer
        assert plain.query == more.query and plain.reply == more.reply
        changed += plain.message != more.message
    assert 0 < changed < 200


def opening(statement):
    marks = sorted((statement.index(m), m) for m in ("{person}", "{relation}"))
    return statement[: marks[1][0] + len(marks[1][1])]


def test_every_train_fact_has_three_more_statements_with_every_placeholder():
    assert set(MORE_STATEMENTS) == {t.statement for t in TRAIN.facts.values()}
    for extra in MORE_STATEMENTS.values():
        assert len(extra) == 3
        for statement in extra:
            assert statement.format(person="Ann", relation="aunt", value="X").count("X") == 1


def test_new_statements_open_like_existing_train_statements_and_no_sealed_pool():
    train = {opening(t.statement) for t in TRAIN.facts.values()}
    sealed = {
        opening(t.statement)
        for p in (HELDOUT, PROBE, POOLS["independent"])
        for t in p.facts.values()
    }
    for extra in MORE_STATEMENTS.values():
        for statement in extra:
            assert opening(statement) in train
            assert opening(statement) not in sealed


def test_more_statements_change_only_the_wording_of_fact_lines():
    changed = 0
    for seed in range(100):
        plain = build_item("x", seed, 58, "older", "train")
        more = build_item("x", seed, 58, "older", "train", more_statements=True)
        assert plain.message == more.message and plain.answer == more.answer
        assert len(plain.exchanges) == len(more.exchanges)
        assert more.answer in more.exchanges[more.fact_index][0]
        changed += plain.exchanges != more.exchanges
    assert 0 < changed < 100
