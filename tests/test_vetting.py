import random

import pytest

from aya_retrieval.vetting import replace_rejected, statement_sheet


def row(row_id, kind, message, reply="Nice."):
    turns = [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "Hello!"},
        {"role": "user", "content": message},
        {"role": "assistant", "content": reply},
    ]
    return {"id": row_id, "kind": kind, "turns": turns}


DATA = [
    row("older_0000", "older", "what did Ann get"),
    row("statement_0000", "statement", "Ann was late again", "Ann is a great name."),
    row("statement_0001", "statement", "my aunt lent me a book"),
]
SPARE = [
    row("statement_0000", "statement", "my aunt lent me a book", "Any good?"),
    row("statement_0001", "statement", "Ann helped me fix my bike", "Is it riding well?"),
]


def marks_for(key, bad):
    return {e["line"]: 0 if (e["source"], e["id"]) in bad else 1 for e in key}


def test_sheet_holds_every_statement_target_once_and_hides_the_source():
    sheet, key = statement_sheet(DATA, SPARE, random.Random(1))
    assert len(sheet) == len(key) == 4
    assert {(e["source"], e["id"]) for e in key} == {
        ("data", "statement_0000"),
        ("data", "statement_0001"),
        ("spare", "statement_0000"),
        ("spare", "statement_0001"),
    }
    assert all(set(line) == {"line", "view", "message", "reply"} for line in sheet)
    assert sheet[0]["view"] == [("hi", "Hello!")]


def test_rejected_target_gets_a_coherent_spare_with_a_new_message():
    _, key = statement_sheet(DATA, SPARE, random.Random(1))
    rows, tally = replace_rejected(DATA, SPARE, key, marks_for(key, {("data", "statement_0000")}))
    assert [r["id"] for r in rows] == ["older_0000", "statement_0000_vetted", "statement_0001"]
    # The first spare repeats a kept message, so the second is used.
    assert rows[1]["turns"][-2]["content"] == "Ann helped me fix my bike"
    assert tally["rejected"] == tally["spares_used"] == 1


def test_spares_marked_incoherent_are_never_used():
    _, key = statement_sheet(DATA, SPARE, random.Random(1))
    bad = {("data", "statement_0000"), ("spare", "statement_0001")}
    rows, _ = replace_rejected(DATA, SPARE, key, marks_for(key, bad))
    assert rows[1]["turns"][-1]["content"] == "Any good?"


def test_running_out_of_spares_is_an_error():
    _, key = statement_sheet(DATA, SPARE, random.Random(1))
    bad = {("data", "statement_0000"), ("spare", "statement_0000"), ("spare", "statement_0001")}
    with pytest.raises(ValueError):
        replace_rejected(DATA, SPARE, key, marks_for(key, bad))
