import json

import pytest

from aya_retrieval import report_data
from aya_retrieval.report_data import (
    by_kind,
    coherence_by_model_and_kind,
    eval_rows,
    percent_above,
    pooled,
    recall,
)


def row(kind, size=58, correct=True, arm="tool_loop"):
    return {"kind": kind, "size": size, "correct": correct, "arm": arm}


def test_recall_counts_only_the_search_kinds_at_the_chosen_length():
    rows = [
        row("older"),
        row("confirm", correct=False),
        row("older", size=419),
        row("statement"),
        row("in_view"),
    ]
    assert recall(rows) == (2, 3)
    assert recall(rows, 58) == (1, 2)
    assert recall(rows, 419) == (1, 1)


def test_by_kind_covers_every_kind_even_when_absent():
    result = by_kind([row("older"), row("older", correct=False)])
    assert result["older"] == (1, 2)
    assert result["statement"] == (0, 0)


def test_percent_above_is_relative_to_the_base_rate():
    assert percent_above((73, 100), (31, 100)) == pytest.approx(135.48, abs=0.01)
    assert pooled([(1, 2), (3, 4)]) == (4, 6)


def test_eval_rows_keeps_one_arm_and_treats_old_files_as_tool_loop(tmp_path, monkeypatch):
    monkeypatch.setattr(report_data, "EVAL_DIR", tmp_path)
    rows = [
        row("older"),
        row("older", arm="three_exchanges"),
        {"kind": "confirm", "size": 58, "correct": 1},
    ]
    (tmp_path / "x_seed_1.json").write_text(json.dumps({"rows": rows}))
    assert len(eval_rows("x", 1)) == 2
    assert len(eval_rows("x", 1, arm="three_exchanges")) == 1


def test_coherence_counts_each_model_and_kind(tmp_path):
    key = [
        {"line": 0, "model": "base", "kind": "older"},
        {"line": 1, "model": "tuned", "kind": "older"},
        {"line": 2, "model": "tuned", "kind": "older"},
    ]
    (tmp_path / "key.json").write_text(json.dumps(key))
    (tmp_path / "marks.json").write_text(json.dumps({"0": 0, "1": 1, "2": 1}))
    result = coherence_by_model_and_kind(tmp_path / "marks.json", tmp_path / "key.json")
    assert result == {"base": {"older": (0, 1)}, "tuned": {"older": (2, 2)}}


def test_coherence_pooled_adds_sheets(tmp_path, monkeypatch):
    monkeypatch.setattr(report_data, "COHERENCE_DIR", tmp_path)
    for name, mark in (("a", 1), ("b", 0)):
        (tmp_path / "R" / "judge").mkdir(parents=True, exist_ok=True)
        (tmp_path / "R" / f"sheet_{name}").mkdir()
        key = [{"line": 0, "model": "tuned", "kind": "older"}]
        (tmp_path / "R" / f"sheet_{name}" / "key.json").write_text(json.dumps(key))
        (tmp_path / "R" / "judge" / f"marks_{name}.json").write_text(json.dumps({"0": mark}))
    assert report_data.coherence_pooled("R", ["a", "b"]) == {"tuned": {"older": (1, 2)}}
