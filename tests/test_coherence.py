"""The coherence sheet must be blind, and its count must leave no reply out."""

import json
import random

import pytest

from aya_retrieval.coherence import paired_counts, sheet_lines


def rows(reply):
    return [
        {
            "id": name,
            "arm": "tool_loop",
            "kind": "older",
            "view": [],
            "message": "m",
            "reply": f"{reply} {name}",
        }
        for name in ("a", "b")
    ]


def test_the_sheet_holds_no_model_names():
    sheet, _ = sheet_lines(rows("x"), rows("y"), random.Random(1))
    assert "base" not in json.dumps(sheet)
    assert "tuned" not in json.dumps(sheet)
    assert len(sheet) == 4


def test_the_shuffle_does_not_keep_the_models_apart():
    sheet_size = 40
    many = [{**rows("x")[0], "id": str(i)} for i in range(sheet_size)]
    _, key = sheet_lines(many, many, random.Random(1))
    first_half = [entry["model"] for entry in key[: sheet_size // 2]]
    assert len(set(first_half)) == 2


def test_runs_on_different_conversations_are_refused():
    with pytest.raises(ValueError, match="same conversations"):
        sheet_lines(rows("x"), rows("y")[:1], random.Random(1))


def test_paired_counts_track_disagreement():
    key = [
        {"line": 0, "model": "base", "id": "a"},
        {"line": 1, "model": "tuned", "id": "a"},
        {"line": 2, "model": "base", "id": "b"},
        {"line": 3, "model": "tuned", "id": "b"},
    ]
    assert paired_counts({0: 1, 1: 0, 2: 1, 3: 1}, key) == {
        "pairs": 2,
        "base_coherent": 2,
        "tuned_coherent": 1,
        "only_base_coherent": 1,
        "only_tuned_coherent": 0,
    }


def test_an_unmarked_line_is_an_error():
    key = [{"line": 0, "model": "base", "id": "a"}, {"line": 1, "model": "tuned", "id": "a"}]
    with pytest.raises(ValueError, match="every line"):
        paired_counts({0: 1}, key)
