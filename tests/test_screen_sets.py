"""Every training set reads back the way the trainer reads it: one JSON row per line (R-136)."""

import json
from pathlib import Path

import pytest

SETS = sorted(Path("data/screens").glob("*.jsonl"))


def test_sets_exist():
    assert SETS


@pytest.mark.parametrize("path", SETS, ids=lambda p: p.name)
def test_set_is_one_row_per_line(path):
    # As scripts/run_recall_train.py reads --data: text mode, str.splitlines().
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines and all(lines), f"{path.name} has a blank line"
    for line in lines:
        assert isinstance(json.loads(line), dict)
