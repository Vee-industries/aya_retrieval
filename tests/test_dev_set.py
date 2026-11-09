import json

from aya_retrieval.dev_set import NO_FACT, load_dev_set, question_problem
from aya_retrieval.scoring import item_correct

# A made-up chat: exchange 1 holds an older fact, exchange 5 (in view) holds another.
EXCHANGES = (
    ("hey hows it going", "Good, you?"),
    ("my cousin amara just started as a florist", "That sounds lovely."),
    ("and my coworker amara is a welder now", "Two Amaras, busy month."),
    ("weekend was quiet", "Quiet can be nice."),
    ("watched a film", "Anything good?"),
    ("my uncle bought a kayak yesterday", "Fun for the summer."),
)


def question(**fields):
    base = {"kind": "older", "message": "what does my cousin do again", "answer": "florist"}
    return base | {"wrong": ["welder"], "fact_exchange": 1} | fields


def test_a_sound_older_question_passes():
    assert question_problem(EXCHANGES, question()) is None


def test_each_brief_rule_rejects_a_question_that_breaks_it():
    cases = {
        "answer is not in its fact exchange": question(fact_exchange=2),
        "fact exchange is in view": question(answer="kayak", wrong=[], fact_exchange=5),
        "answer is in the question": question(message="is my cousin still a florist"),
        "a wrong value is not in the conversation": question(wrong=["plumber"]),
        "answer is under 4 letters": question(answer="as", wrong=[]),
        "a wrong value and the answer contain one another": question(wrong=["a florist"]),
        "in_view fact is out of view": question(kind="in_view"),
        "never_told item with no wrong values": question(kind="never_told", wrong=[]),
        "unknown kind 'recall'": question(kind="recall"),
    }
    for reason, case in cases.items():
        assert question_problem(EXCHANGES, case) == reason


def test_a_confirm_question_may_name_its_value():
    confirm = question(kind="confirm", message="amara's a florist now right")
    assert question_problem(EXCHANGES, confirm) is None


def test_the_loader_keeps_sound_questions_drops_the_rest_and_hashes_the_files(tmp_path):
    chat = {
        "id": "t_01",
        "exchanges": [list(pair) for pair in EXCHANGES],
        "questions": [
            question(),
            question(
                kind="in_view",
                message="what did my uncle get",
                answer="kayak",
                wrong=[],
                fact_exchange=5,
            ),
            question(
                kind="never_told",
                message="what does my aunt do",
                answer="",
                fact_exchange=None,
                wrong=["florist", "welder"],
            ),
            {
                "kind": "statement",
                "message": "anyway im off to bed",
                "answer": "",
                "wrong": [],
                "fact_exchange": None,
            },
            question(fact_exchange=2),
        ],
    }
    (tmp_path / "t_01.json").write_text(json.dumps(chat), encoding="utf-8")
    items, dropped, digest = load_dev_set(tmp_path)
    assert [i.kind for i in items] == ["older", "in_view", "never_told", "statement"]
    assert dropped == [("t_01_q4", "answer is not in its fact exchange")]
    assert items[2].fact_index == NO_FACT and items[2].answer == ""
    assert len(digest) == 64 and load_dev_set(tmp_path)[2] == digest
    # The existing scorer, unchanged: the gold answer passes, a wrong value fails.
    older, in_view, never_told, statement = items
    for item in (older, in_view):
        assert item_correct(item.kind, f"It's {item.answer}.", item.answer, item.forbidden, 1)
    assert not item_correct("older", "a welder", older.answer, older.forbidden, 1)
    assert item_correct("never_told", "you never said", "", never_told.forbidden, 1)
    assert not item_correct("never_told", "she's a florist", "", never_told.forbidden, 1)
    assert item_correct("statement", "night!", "", (), 0)
