"""Blind judge sheet and tally for R-182: R-176's 8 questions with K1 added, same brief and script.

Runs ``demo_judges_r176.py``'s own ``sheet`` and ``tally`` on a merged run: base and K1 arms from
``results/demo/branches_k1_r178_82.json`` (base rerun there, equal to R-176's), 6.37 arms from
``results/demo/branches_r176.json``. Every arm is judged again together by two fresh judges, so the
6.37 and base marks can be checked against R-176's. Output: ``results/demo/r182_judge/``.

Usage:
    python scripts/records/demo_judges_r182.py sheet
    python scripts/records/demo_judges_r182.py tally
"""

from __future__ import annotations

import json
import sys

import demo_judges_r176 as judges

DEMO = judges.REPO_ROOT / "results" / "demo"
judges.OUT = DEMO / "r182_judge"
judges.RUN = judges.OUT / "run_merged.json"
judges.ARMS = ("base_no_search", "6.37_no_search", "K1_no_search", "base", "6.37", "K1")


def merge() -> None:
    k1 = json.loads((DEMO / "branches_k1_r178_82.json").read_text(encoding="utf-8"))["arms"]
    old = json.loads((DEMO / "branches_r176.json").read_text(encoding="utf-8"))["arms"]
    arms = {name: (old if name.startswith("6.37") else k1)[name] for name in judges.ARMS}
    judges.OUT.mkdir(parents=True, exist_ok=True)
    text = json.dumps({"arms": arms}, indent=1, ensure_ascii=False)
    judges.RUN.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:] == ["sheet"]:
        merge()
    {"sheet": judges.sheet, "tally": judges.tally}[sys.argv[1]]()
