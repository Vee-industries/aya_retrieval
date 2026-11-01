"""Checks on the provenance record written into every results file."""

import json

import pytest

from aya_retrieval import provenance
from aya_retrieval.provenance import DirtyTreeError, require_clean_tree, run_metadata


def test_uncommitted_changes_block_a_run_unless_allowed(monkeypatch):
    monkeypatch.setattr(provenance, "_git", lambda *a, **k: " M src/aya_retrieval/scoring.py")
    with pytest.raises(DirtyTreeError, match="commit first"):
        require_clean_tree()
    require_clean_tree(allow_dirty=True)


def test_a_clean_tree_passes_and_missing_git_blocks(monkeypatch):
    monkeypatch.setattr(provenance, "_git", lambda *a, **k: "")
    require_clean_tree()
    monkeypatch.setattr(provenance, "_git", lambda *a, **k: None)
    with pytest.raises(DirtyTreeError, match="unavailable"):
        require_clean_tree()


def test_run_metadata_is_complete_and_serialisable():
    meta = run_metadata(argv=["prog", "--flag"])
    assert meta["command"] == ["prog", "--flag"]
    for field in (
        "utc_time",
        "git_commit",
        "git_dirty",
        "toolkit_commits",
        "python",
        "platform",
        "packages",
    ):
        assert field in meta
    json.dumps(meta)
