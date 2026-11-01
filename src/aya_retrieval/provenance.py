"""Run provenance: the facts every results file records about how it was produced."""

from __future__ import annotations

import platform
import subprocess
import sys
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TOOLKIT_ROOT = REPO_ROOT.parent / "vendor"
TOOLKITS = ("AgentTune", "AuditKIT")
TRACKED_PACKAGES = (
    "aya-retrieval",
    "agenttune",
    "auditkit",
    "torch",
    "transformers",
    "trl",
    "peft",
    "huggingface_hub",
)


def _git(*args: str, cwd: Path = REPO_ROOT) -> str | None:
    """Run a git command; return its stripped output, or None on failure."""
    try:
        result = subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, check=True, timeout=10
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip()


def _package_version(name: str) -> str | None:
    try:
        return metadata.version(name)
    except metadata.PackageNotFoundError:
        return None


class DirtyTreeError(RuntimeError):
    """Raised when a results-producing run starts from code that is not committed."""


def require_clean_tree(allow_dirty: bool = False) -> None:
    """Refuse to run on uncommitted code, so every result's recorded commit reproduces it.

    Only tracked files count; untracked files are ignored.

    Args:
        allow_dirty: Skip the check, for development runs whose output is not kept.

    Raises:
        DirtyTreeError: If tracked files have uncommitted changes, or git is unavailable.
    """
    if allow_dirty:
        return
    status = _git("status", "--porcelain", "--untracked-files=no")
    if status is None:
        raise DirtyTreeError("git is unavailable, so the code version cannot be recorded")
    if status:
        raise DirtyTreeError(f"uncommitted changes to tracked files; commit first:\n{status}")


def run_metadata(argv: list[str] | None = None) -> dict:
    """Describe the current run: time, command, code and toolkit versions, and hardware.

    Call this when the run starts, so the record describes the code that actually ran.

    Args:
        argv: The command line to record. Defaults to ``sys.argv``.

    Returns:
        A JSON-serialisable dict. ``git_dirty`` is True when tracked files have uncommitted
        changes, which means the recorded commit alone does not reproduce the run.
    """
    status = _git("status", "--porcelain", "--untracked-files=no")
    return {
        "utc_time": datetime.now(UTC).isoformat(timespec="seconds"),
        "command": list(sys.argv if argv is None else argv),
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": None if status is None else bool(status),
        "toolkit_commits": {
            name: _git("rev-parse", "HEAD", cwd=TOOLKIT_ROOT / name) for name in TOOLKITS
        },
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": {name: _package_version(name) for name in TRACKED_PACKAGES},
    }
