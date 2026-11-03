from aya_retrieval.conversations import build_item
from aya_retrieval.pools import PROBE, TRAIN
from aya_retrieval.train_phrasings import MORE_INDIRECT

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
