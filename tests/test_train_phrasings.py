from aya_retrieval.conversations import build_item
from aya_retrieval.pools import HELDOUT, POOLS, PROBE, TRAIN
from aya_retrieval.train_phrasings import (
    MORE_CHAT,
    MORE_CHAT_FACTS,
    MORE_CHAT_PLAIN,
    MORE_INDIRECT,
    MORE_STATEMENTS,
)

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


def four_word_runs(line):
    words = line.split()
    return {tuple(words[i : i + 4]) for i in range(len(words) - 3)}


def test_more_chat_lines_are_new_and_well_formed():
    assert len(MORE_CHAT) == 48
    assert len({line for line, _ in MORE_CHAT}) == 48
    train = {line for line, _ in TRAIN.statements}
    for line, reply in MORE_CHAT:
        assert line not in train and reply
        assert ("{person}" in line) != ("{relation}" in line)
        assert line.format(person="Ann", relation="aunt")


def test_no_more_chat_line_shares_four_words_with_the_probe_or_a_sealed_pool():
    others = set()
    for pool in (PROBE, HELDOUT, POOLS["independent"]):
        for line, _ in pool.statements:
            others |= four_word_runs(line)
    for line, _ in MORE_CHAT:
        clash = bool(four_word_runs(line) & others)
        assert not clash, line


def test_more_chat_changes_only_statement_lines():
    changed = 0
    for seed in range(200):
        for kind in ("older", "statement"):
            plain = build_item("x", seed, 58, kind, "train")
            more = build_item("x", seed, 58, kind, "train", more_chat=True)
            assert plain.exchanges == more.exchanges
            if kind == "older":
                assert plain == more
            else:
                changed += plain.message != more.message
    assert changed > 100


# Each train fact type's topic, as fix 18's chat lines name it (R-083).
TOPIC_WORDS = {
    "animals": "animals",
    "baby": "baby",
    "band": "band",
    "birth": "born",
    "boat": "boat",
    "car": "car",
    "cat": "cat",
    "city": "city",
    "coffee": "coffee",
    "dog": "dog",
    "festival": "festival",
    "floor": "floor",
    "genre": "novel",
    "hobby": "hobby",
    "injury": "injury",
    "job": "job",
    "motorbike": "motorbike",
    "paint": "paint",
    "phone": "phone",
    "prize": "prize",
    "promotion": "promotion",
    "race": "race",
    "shop": "shop",
    "street": "street",
    "subject": "class",
}


def chat_lines():
    return [line for lines in MORE_CHAT_FACTS.values() for line in lines], list(MORE_CHAT_PLAIN)


def test_fact_chat_has_three_lines_per_train_fact_type_each_naming_its_topic():
    assert sorted(MORE_CHAT_FACTS) == sorted(TRAIN.facts) == sorted(TOPIC_WORDS)
    for kind, lines in MORE_CHAT_FACTS.items():
        assert len(lines) == 3
        for line, _ in lines:
            assert TOPIC_WORDS[kind] in line.replace("kitten", "cat").replace("babysit", "baby ")


def test_plain_chat_names_no_fact_topic_of_any_open_pool():
    topics = set(TOPIC_WORDS.values()) | set(PROBE.facts) | set(POOLS["hard_dev"].facts)
    for line, _ in MORE_CHAT_PLAIN:
        assert not set(line.replace(",", "").split()) & topics, line


def test_fix18_chat_lines_are_new_well_formed_and_state_no_value():
    facts, plain = chat_lines()
    assert len(facts) == len(plain) == 75
    lines = [line for line, _ in facts + plain]
    known = {line for line, _ in (*TRAIN.statements, *MORE_CHAT)}
    assert len(set(lines)) == 150 and not set(lines) & known
    values = {
        value.casefold()
        for pool in (TRAIN, PROBE, POOLS["hard_dev"])
        for fact in pool.facts.values()
        for value in fact.values
    }
    for line, reply in facts + plain:
        assert ("{person}" in line) != ("{relation}" in line) and reply
        assert "?" not in line and "remember" not in line
        assert line.format(person="Ann", relation="aunt")
        assert not set(line.split()) & values, line
    assert sum("{person}" in line for line in lines) in range(70, 81)


def test_no_fix18_chat_line_shares_four_words_with_a_test_or_sealed_pool():
    others = set()
    for pool in (PROBE, POOLS["hard_dev"], HELDOUT, POOLS["independent"]):
        for line, _ in pool.statements:
            others |= four_word_runs(line)
    facts, plain = chat_lines()
    for line, _ in facts + plain:
        assert not four_word_runs(line) & others, line
