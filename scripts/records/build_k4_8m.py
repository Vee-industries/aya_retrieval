"""R-235 (round 2, lever 1): K4.8's build with each natural row's searches merged into one.

Usage: python scripts/records/build_k4_8m.py

Every stage try so far misses the same Demo2 facts, mostly because the model's first query, made of
the question's words, never returns them and it stops after one search (R-223's recount: 65 of
K4.6's 108 outside-writer misses). This reruns K4.8's chain with ``build_k3.MERGED_QUERY`` on the
K3 writers' rows: the one search is the writer's ``query`` words then its ``second_query`` words not
already there (``build_k3.merged_query``), one OR call; the row then names the value if that search
returns the source, else declines (never_told rows: kept if it returns passages). No new writing.
With ``merged=False`` it rebuilds K4.8 byte for byte. ``check_k3.py --set k4_8m_r235`` checks it.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("build_k4_8", HERE / "build_k4_8.py")
K48 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = K48
spec.loader.exec_module(K48)
K45 = K48.K45


def main(merged: bool = True, out: Path = Path("data/screens/k4_8m_r235.jsonl")) -> None:
    K45.DIR = out.parent / out.stem.split("_r")[0]  # k4_8m_r235 -> data/screens/k4_8m
    K45.WRITERS, K45.OUT = K45.DIR / "writers", out
    K45.write_writers = K48.write_writers
    K45.main(record="R-235", never_told_twice=True, merged=merged)


if __name__ == "__main__":
    main()
