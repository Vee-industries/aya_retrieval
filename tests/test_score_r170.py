"""R-170's scorer and runner arms on small made-up data, never the real LongMemEval file."""

import importlib.util
import json
from pathlib import Path

from aya_retrieval.longmemeval import convert
from aya_retrieval.recall_tool import build_search_tool
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME

SCRIPTS = Path(__file__).parents[1] / "scripts"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


score = load("score_r170", SCRIPTS / "records" / "score_r170.py")
runner = load("run_longmemeval", SCRIPTS / "run_longmemeval.py")


def test_matching_is_on_word_boundaries():
    assert score.matches("I think it was 3.", "3")
    assert not score.matches("I think it was 13.", "3")
    assert not score.matches("It was 30 minutes", "3")
    assert not score.matches("We met in Lyonnais country", "Lyon")
    assert score.matches("She lives in Lyon now!", "Lyon")


def test_case_punctuation_articles_and_apostrophes_are_normalised():
    assert score.matches("it was MICHAELS engagement party", "Michael's engagement party")
    assert score.matches("You bought the Spitfire.", "a Spitfire")
    assert score.matches("It’s Michael’s party", "Michael's party")
    assert score.matches("about 25:50, i think", "25 minutes and 50 seconds (or 25:50)")


def test_number_words_map_to_digits():
    assert score.words("Twenty-five days and three hours") == ["25", "days", "and", "3", "hours"]
    assert score.matches("five days", "5 days")
    assert score.matches("5 days", "five days")
    assert score.matches("thirty", "30")
    assert not score.matches("fifteen", "5")


def test_alternatives_are_split_by_the_written_rule():
    assert score.alternatives("7 days. 8 days (including the last day) is also acceptable.") == [
        "7 days",
        "8 days",
    ]
    assert score.alternatives("11 days (or 12 days, if April 15th to 22nd is 8 days)") == [
        "11 days",
        "12 days",
    ]
    ranged = "One week. Answers ranging from 7 days to 9 days are also acceptable."
    assert score.alternatives(ranged) == ["One week", "7 days", "8 days", "9 days"]
    assert score.alternatives("Mod Podge or another sealant") == ["Mod Podge", "another sealant"]
    long_gold = "I replaced or fixed five items: the faucet, the mat and the toaster."
    assert score.alternatives(long_gold) == [long_gold]
    assert score.matches("8 days", "7 days. 8 days (including the last day) is also acceptable.")
    assert not score.matches(
        "9 days", "7 days. 8 days (including the last day) is also acceptable."
    )


def test_the_read_list_comes_from_the_golds_alone():
    assert score.answer_read("temporal-reasoning", "3 weeks ago", False) is None
    assert score.answer_read("temporal-reasoning", "First the party, then the trip to Lyon.", False)
    assert score.answer_read("single-session-preference", "The user would prefer", False)
    assert score.answer_read("single-session-user", "Lyon", True)
    assert (
        score.answer_read("multi-session", "I replaced or fixed five items: a, b.", False) is None
    )


def test_the_abstention_list_is_r170s_and_matches_whole_phrases():
    assert len(score.DECLINES) == 15
    assert "never mentioned" in score.DECLINES and "no record" in score.DECLINES
    assert score.declines("Sorry, I don't know where she moved.")
    assert score.declines("I don’t know.")
    assert score.declines("You never mentioned that.")
    assert not score.declines("She moved to Lyon.")
    assert not score.declines("I know: Lyon.")
    assert not score.declines(None)


def test_the_self_test_passes_golds_and_catches_a_scorer_that_would_pass_wrong_replies():
    golds = {"a": "Lyon", "b": "3", "c": "7 days. 8 days (whole) is also acceptable.", "d": "1/48"}
    assert score.check_answer_scorer(golds)["failed"] == []
    assert score.shifted("3 weeks") == "13 weeks"
    # "know" is in a known-wrong reply ("I don't know."), so the self-test must flag it.
    assert score.check_answer_scorer({"e": "know"})["failed"] == [("e", "known-wrong reply")]


def test_false_match_partners_never_pair_a_question_with_itself():
    ids = [f"q{n}" for n in range(9)]
    partners = score.false_match_partners(ids)
    assert sorted(partners) == sorted(ids) and sorted(partners.values()) == sorted(ids)
    assert all(partners[i] != i for i in ids)
    assert partners == score.false_match_partners(list(reversed(ids)))


def test_the_false_match_rate_scores_each_reply_against_its_partners_gold():
    golds = {"q0": "Lyon", "q1": "Lyon", "q2": "Oslo"}
    replies = {"q0": "Lyon", "q1": "Lyon", "q2": "Lyon"}
    partners = score.false_match_partners(list(replies))
    expected = sum(golds[partners[i]] == "Lyon" for i in replies)
    assert score.false_match_rate(replies, golds)["matches"] == expected == 2


def test_evidence_outcome_reads_turn_session_and_shown_text():
    found = score.evidence_outcome(
        [["exchange_0002", "exchange_0005"], ["exchange_0004"]],
        ["nothing here", "she moved to Lyon"],
        turn={4},
        session={4, 5},
        gold="Lyon",
    )
    assert found["searched"] and not found["first"] and found["any"]
    assert found["first_session"] and found["any_session"]
    assert not found["first_shown"] and found["any_shown"] and found["passages"] == 3
    assert not score.evidence_outcome([], [], {1}, {1}, "x")["searched"]


def test_paired_counts_discordant_questions_and_missing_ones_as_wrong():
    first, second = {"a": 1, "b": 1, "c": 0}, {"a": 0, "b": 1, "c": 1}
    out = score.paired(first, second, ["a", "b", "c", "d"])
    assert (out["first"], out["second"], out["only_first"], out["only_second"]) == (2, 2, 1, 1)
    assert out["p"] == 1.0 and len(out["difference_and_95_interval"]) == 3
    both = score.two_readings(first, second, ["a", "b", "c", "d"], completed={"a", "b"})
    assert both["completed_by_every_arm"]["n"] == 2 and both["failures_wrong"]["n"] == 4


RECORD = {
    "question_id": "q1",
    "question_type": "single-session-user",
    "question": "Where did my sister move?",
    "question_date": "2023/05/20 (Sat) 09:00",
    "answer": "Lyon",
    "answer_session_ids": ["s2"],
    "haystack_dates": ["2023/05/01 (Mon) 10:00", "2023/05/02 (Tue) 11:00"],
    "haystack_session_ids": ["s1", "s2"],
    "haystack_sessions": [
        [
            {"role": "user", "content": f"line {n}"}
            if r == 0
            else {"role": "assistant", "content": "ok"}
            for n in range(4)
            for r in range(2)
        ],
        [
            {"role": "user", "content": "my sister moved to Lyon", "has_answer": True},
            {"role": "assistant", "content": "Big move!"},
        ],
    ],
}


def test_always_search_queries_the_question_without_its_date(tmp_path):
    item = convert(RECORD)
    tool = build_search_tool(item.older(), tmp_path / "index.sqlite", match_all=False)
    seen = []

    def generate(messages):
        seen.append(messages)
        return "She moved to Lyon."

    result = runner.run_question("always_search", item, generate, tool)
    assert result.queries == ["Where did my sister move?"]
    assert json.loads(result.transcript[0])[0]["tool_name"] == SEARCH_TOOL_NAME
    assert seen[0][-3]["content"] == item.message  # the dated question, the call, its result
    assert result.reply == "She moved to Lyon."


def test_evidence_only_shows_every_evidence_message_and_no_tool():
    item = convert(RECORD)
    seen = []

    def generate(messages):
        seen.append(messages)
        return "Lyon."

    result = runner.run_question("evidence_only", item, generate, tool=None)
    assert result.reply == "Lyon." and not result.queries
    messages = seen[0]
    assert messages[0]["content"] == runner.SYSTEM
    assert [m["content"] for m in messages[1:]] == [
        "[2023/05/02 (Tue) 11:00] my sister moved to Lyon",
        "Big move!",
        item.message,
    ]
