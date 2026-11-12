"""Rebuild the demo's search index from 6.37's transcript and replay its searches (R-175, no model).

The index files are written beside the repository and deleted after each search.

Usage:
    python scripts/records/replay_demo_search_r175.py
"""

import json
from pathlib import Path

from aya_retrieval.conversations import EXCHANGES_IN_VIEW
from aya_retrieval.recall_tool import build_search_tool

REPO = Path(__file__).resolve().parents[2]
HERE = REPO.parent
turns = json.loads((REPO / "results/demo/fix17cs37_82.json").read_text(encoding="utf-8"))["turns"]
exchanges = [(t["message"], t["reply"]) for t in turns]

CASES = [
    (12, "brother new job", "6.37's query"),
    (14, "sister broke skiing injury", "6.37's query"),
    (14, "fixed sink", "a plain query, for comparison"),
    (14, "kitchen sink leak", "a plain query, for comparison"),
]
for turn, query, label in CASES:
    older = exchanges[: max(turn - 1 - EXCHANGES_IN_VIEW, 0)]
    index = HERE / f"replay_{turn}.sqlite"
    index.unlink(missing_ok=True)
    tool = build_search_tool(older, index, match_all=False)
    result = tool.execute(query)
    print(f"--- turn {turn}, {label}: {query!r} (older exchanges indexed: {len(older)})")
    print(result.output if result.success else result.error)
    index.unlink(missing_ok=True)
