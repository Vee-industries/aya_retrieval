"""The demo notebook pins the same toolkit commit and package versions as CI."""

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO_ROOT / "notebooks" / "demo_6_37.ipynb"
CI = REPO_ROOT / ".github" / "workflows" / "ci.yml"
SHARED = ("transformers", "peft", "accelerate", "safetensors", "huggingface_hub", "datasets")


def notebook_code() -> str:
    cells = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    return "\n".join("".join(c["source"]) for c in cells if c["cell_type"] == "code")


def pins(text: str) -> dict[str, str]:
    return dict(re.findall(r"([A-Za-z_\-]+)==([0-9][0-9.]*)", text))


def test_notebook_has_no_outputs():
    cells = json.loads(NOTEBOOK.read_text(encoding="utf-8"))["cells"]
    assert all(not c.get("outputs") for c in cells if c["cell_type"] == "code")


def test_agenttune_commit_matches_ci():
    commit = re.search(r"repository: Lexsi-Labs/AgentTune\s+ref: ([0-9a-f]{40})", CI.read_text())
    assert commit and commit.group(1) in notebook_code()


def test_package_versions_match_ci():
    in_ci, in_notebook = pins(CI.read_text()), pins(notebook_code())
    for name in SHARED:
        assert in_notebook[name] == in_ci[name], name


def test_notebook_checks_the_frozen_weights():
    code = notebook_code()
    assert "sealed_manifest.json" in code
    assert 'assert got == frozen, "adapter weights differ from the frozen model"' in code
