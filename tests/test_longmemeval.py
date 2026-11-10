"""The LongMemEval converter (R-170) on a small made-up record, never the real file."""

import json

import pytest

from aya_retrieval.longmemeval import (
    DATA_SHA256,
    convert,
    exchange_index,
    load_longmemeval,
    pair_turns,
    passages,
)
from aya_retrieval.recall_tool import TOP_K, build_search_tool, exchange_doc_id


def turn(role, content, has_answer=None):
    out = {"role": role, "content": content}
    if has_answer is not None:
        out["has_answer"] = has_answer
    return out


# Session s1 opens the history with an assistant turn and has two user turns in a row; s2 opens
# with an assistant turn, which joins s1's last reply; s3 holds the answer and ends the history.
SESSIONS = [
    [
        turn("assistant", "Welcome back."),
        turn("user", "i got a new bike"),
        turn("assistant", "Nice."),
        turn("user", "it is red"),
        turn("user", "and fast"),
        turn("assistant", "Sounds fun."),
    ],
    [
        turn("assistant", "Here is the rest of that list."),
        turn("user", "thanks"),
        turn("assistant", "Any time."),
    ],
    [
        turn("user", "my sister moved to Lyon", has_answer=True),
        turn("assistant", "Big move!", has_answer=False),
        turn("user", "weather is nice"),
        turn("assistant", "Enjoy it."),
        turn("user", "going for a walk"),
        turn("assistant", "Have fun."),
        turn("user", "back now"),
        turn("assistant", "Welcome back."),
    ],
]
DATES = ["2023/05/01 (Mon) 10:00", "2023/05/02 (Tue) 11:00", "2023/05/03 (Wed) 12:00"]
IDS = ["s1", "s2", "answer_s3"]
RECORD = {
    "question_id": "q1",
    "question_type": "single-session-user",
    "question": "Where did my sister move?",
    "question_date": "2023/05/20 (Sat) 09:00",
    "answer": "Lyon",
    "answer_session_ids": ["answer_s3"],
    "haystack_dates": DATES,
    "haystack_session_ids": IDS,
    "haystack_sessions": SESSIONS,
}


def test_turns_pair_in_order_and_unpaired_turns_join_their_neighbour():
    pairing = pair_turns(SESSIONS, DATES, IDS)
    users = [user for user, _ in pairing.exchanges]
    replies = [reply for _, reply in pairing.exchanges]
    assert users[0] == "[2023/05/01 (Mon) 10:00]"  # the opening assistant turn has no user turn
    assert replies[0] == "Welcome back."
    assert users[1] == "[2023/05/01 (Mon) 10:00] i got a new bike"
    # Two user turns of one session in a row: one text, the date once.
    assert users[2] == "[2023/05/01 (Mon) 10:00] it is red\n\nand fast"
    # s2's opening assistant turn joins s1's last reply, across the session boundary.
    assert replies[2] == "Sounds fun.\n\nHere is the rest of that list."
    assert pairing.session_ids[2] == ("s1", "s2")
    assert users[3] == "[2023/05/02 (Tue) 11:00] thanks"
    assert len(pairing.exchanges) == 8
    assert (pairing.joined, pairing.joined_across_sessions, pairing.opened_by_assistant) == (
        2,
        1,
        1,
    )


def test_two_user_turns_from_two_sessions_each_keep_their_date():
    sessions = [[turn("user", "first")], [turn("user", "second"), turn("assistant", "ok")]]
    pairing = pair_turns(sessions, DATES[:2], IDS[:2])
    assert pairing.exchanges == (
        ("[2023/05/01 (Mon) 10:00] first\n\n[2023/05/02 (Tue) 11:00] second", "ok"),
    )
    assert pairing.joined_across_sessions == 1


def test_an_unknown_role_is_refused():
    with pytest.raises(ValueError, match="unknown role"):
        pair_turns([[turn("system", "x")]], DATES[:1], IDS[:1])


def test_the_question_carries_its_date_and_the_view_is_the_last_three_exchanges():
    item = convert(RECORD)
    assert item.message == "[2023/05/20 (Sat) 09:00] Where did my sister move?"
    assert item.question == "Where did my sister move?"
    assert item.view() == item.exchanges[-3:]
    assert item.older() == item.exchanges[:-3]
    assert item.answer == "Lyon" and item.kind == "single-session-user"


def test_evidence_marks_follow_the_has_answer_turn_and_its_session():
    item = convert(RECORD)
    assert item.evidence_indexes() == (4,)
    assert "Lyon" in item.exchanges[4][0]
    assert item.answer_session_indexes() == (4, 5, 6, 7)
    assert not item.evidence_in_view()
    late = convert(
        RECORD | {"haystack_sessions": [*SESSIONS[:2], SESSIONS[2][2:] + SESSIONS[2][:2]]}
    )
    assert late.evidence_in_view()


def test_the_evidence_only_view_holds_only_the_evidence_sessions():
    item = convert(RECORD)
    assert len(item.evidence_exchanges) == 4
    assert item.evidence_exchanges[0][0] == "[2023/05/03 (Wed) 12:00] my sister moved to Lyon"


def test_abstention_is_read_from_the_id():
    assert convert(RECORD | {"question_id": "q1_abs"}).abstention
    assert not convert(RECORD).abstention


def test_an_integer_answer_becomes_text():
    assert convert(RECORD | {"answer": 3}).answer == "3"


def test_a_file_that_is_not_r170s_is_refused(tmp_path):
    path = tmp_path / "longmemeval_s_cleaned.json"
    path.write_text(json.dumps([RECORD]), encoding="utf-8")
    with pytest.raises(ValueError, match=DATA_SHA256):
        load_longmemeval(path)


def test_passages_are_the_chunks_the_search_tool_indexes(tmp_path):
    long_reply = " ".join(f"Point {n} about bikes and gears." for n in range(40))
    exchanges = (("[d] hello", "Hi."), ("[d] tell me about bikes", long_reply), ("[d] ok", "Sure."))
    built = passages(exchanges)
    per_exchange = [sum(p["exchange"] == i for p in built) for i in range(3)]
    assert per_exchange[0] == 1 and per_exchange[1] > 1 and per_exchange[2] == 1
    tool = build_search_tool(exchanges, tmp_path / "index.sqlite", match_all=False)
    by_chunk = {p["chunk_id"]: p for p in built}
    hits = tool.backend.search("bikes gears", top_k=TOP_K)
    assert hits
    for hit in hits:
        chunk = by_chunk[hit["metadata"]["chunk_id"]]
        assert chunk["text"] == hit["content"]
        assert chunk["doc_id"] == hit["metadata"]["doc_id"] == exchange_doc_id(chunk["exchange"])
    assert exchange_index(exchange_doc_id(12)) == 12
