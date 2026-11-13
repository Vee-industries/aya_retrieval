"""Miss-then-hit rows (R-223) are named by friend message, first call and reply, one row each."""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_recall_train.py"


@pytest.fixture(scope="module")
def train():
    spec = importlib.util.spec_from_file_location("run_recall_train", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def row(train, first_call: str, marked: bool) -> dict:
    view = [{"role": r, "content": f"{r} {i}"} for i in range(3) for r in ("user", "assistant")]
    turns = [*view, {"role": "user", "content": "where does ines work"}]
    turns += [{"role": "assistant", "content": first_call}, {"role": "user", "content": "Tool"}]
    turns += [{"role": "assistant", "content": "Ines works at the bakery."}]
    assert len(view) + 1 == train.FIRST_DEMONSTRATED - 1
    return {"turns": turns, "loss_from_second_call": True} if marked else {"turns": turns}


def test_a_marked_row_beside_its_plain_row_gets_one_key(train):
    rows = [row(train, "miss call", True), row(train, "hit call", False)]
    keys = train.first_call_keys(rows)
    assert keys == {("where does ines work", "miss call", "Ines works at the bakery.")}
    assert train.row_key(rows[0]["turns"]) == train.row_key(rows[1]["turns"])


def test_a_marked_row_sharing_its_key_is_refused(train):
    with pytest.raises(ValueError, match="shares its key"):
        train.first_call_keys([row(train, "same call", True), row(train, "same call", False)])
    with pytest.raises(ValueError, match="shares its key"):
        train.first_call_keys([row(train, "same call", True), row(train, "same call", True)])


def test_no_marked_rows_give_no_keys(train):
    assert train.first_call_keys([row(train, "hit call", False)]) == frozenset()
