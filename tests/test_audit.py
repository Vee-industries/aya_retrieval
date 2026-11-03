import pytest

from aya_retrieval.audit import audit_rows, compare, rebuild_item, verified
from aya_retrieval.conversations import ITEM_KINDS, build_item

PROBE_SEED = 73157


def row_for(kind, reply, queries=(), number=0, size=58):
    item_id = f"{size}_{kind}_{number:02d}"
    seed = PROBE_SEED + size * 1000 + ITEM_KINDS.index(kind) * 100 + number
    item = build_item(item_id, seed, size, kind, "probe")
    return {
        "id": item_id,
        "kind": kind,
        "message": item.message,
        "answer": item.answer,
        "reply": reply.format(answer=item.answer, wrong=item.forbidden[0]),
        "queries": list(queries),
    }


def outcomes(rows):
    return verified(audit_rows(rows, PROBE_SEED, "probe"))


def test_a_reply_with_the_answer_after_a_search_passes():
    row = row_for("older", "You told me it was {answer}.", ["tattoo"])
    assert outcomes([row]) == {row["id"]: 1.0}


def test_auditkit_matches_whole_words_only():
    row = row_for("older", "Was it {answer}ish?", ["tattoo"])
    assert outcomes([row]) == {row["id"]: 0.0}


def test_a_never_told_reply_fails_when_it_names_a_value():
    good = row_for("never_told", "You never mentioned that.", ["mentor grows"])
    bad = row_for("never_told", "They grow {wrong}.", ["mentor grows"], number=1)
    assert outcomes([good, bad]) == {good["id"]: 1.0, bad["id"]: 0.0}


def test_a_statement_fails_when_the_model_searched():
    quiet = row_for("statement", "Ha, that sounds long.")
    searched = row_for("statement", "Ha, that sounds long.", ["Lucia"], number=1)
    assert outcomes([quiet, searched]) == {quiet["id"]: 1.0, searched["id"]: 0.0}


def test_a_row_that_does_not_match_its_rebuilt_item_is_refused():
    row = row_for("older", "x")
    row["message"] = "something else"
    with pytest.raises(ValueError, match="does not match"):
        rebuild_item(row, PROBE_SEED, "probe")


def test_compare_pairs_by_case_id():
    result = compare({"a": 0.0, "b": 0.0, "c": 1.0}, {"c": 1.0, "a": 1.0, "b": 1.0})
    assert result["n"] == 3
    assert result["delta"] == pytest.approx(2 / 3, abs=1e-6)
