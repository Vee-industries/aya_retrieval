"""K4.7's training set (R-215): K4.6's build with 64 more natural chats from 8 new writers.

Usage: python scripts/records/build_k4_7.py

K4.6 (``build_k4_6.py``) bombed Demo2 at 2 of 6 older and passed seed 82's hard_dev lines; on the
outside-writer sets its misses are mostly facts its searches never return, then facts it finds and
declines. The largest gain so far came from natural writer rows (K3, R-205). K4.7 keeps K4.6 whole
and adds 8 writer files (``data/screens/k4_7_writers/``, w9 to w16), written to the unchanged K3
brief (``docs/k3/WRITER_BRIEF.md``) by 8 new writers, to the K3 chats: their possessives are taken
out of the queries as for the rest, and K4.6's chain reruns over all 128 chats. The K4 and K4.4
questions cover the first 64 chats only. ``scripts/records/check_k3.py --set k4_7_r215`` checks it.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEW = Path("data/screens/k4_7_writers")

spec = importlib.util.spec_from_file_location("build_k4_5", HERE / "build_k4_5.py")
K45 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = K45
spec.loader.exec_module(K45)
K45_WRITE = K45.write_writers


def write_writers() -> int:
    """K4.5's writer copies, plus the new K3 writer files with the same query strip."""
    changed = [K45_WRITE()]
    for path in sorted(NEW.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for chat in data["chats"]:
            chat["questions"] = [K45.strip_question(q, changed) for q in chat["questions"]]
        text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
        (K45.WRITERS / "k3" / path.name).write_bytes(text.encode("utf-8"))
    return changed[0]


if __name__ == "__main__":
    K45.DIR, K45.WRITERS = Path("data/screens/k4_7"), Path("data/screens/k4_7/writers")
    K45.OUT = Path("data/screens/k4_7_r215.jsonl")
    K45.write_writers = write_writers
    K45.main(record="R-215", never_told_twice=True)
