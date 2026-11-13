"""K4.8's training set (R-220): K4.7's build with never-told questions written for its new chats.

Usage: python scripts/records/build_k4_8.py

K4.7 (``build_k4_7.py``) added 64 natural chats (w9 to w16) but the K4 near-miss and the K4.4
wrong-person questions covered the first 64 chats only, and K4.7 bombed Demo2 on never-told
(R-218). K4.8 keeps K4.7 whole and adds those two kinds of question for the new chats, written by
4 new writers to the unchanged briefs (``docs/k4/WRITER_BRIEF.md``, ``docs/k4_4/WRITER_BRIEF.md``)
into ``data/screens/k4_8_writers/k4/`` and ``.../k4_4/`` (c: w9 to w12, d: w13 to w16). Their
possessives are taken out of the queries as for the rest, and K4.7's chain reruns with them beside
the old files. With both folders empty it rebuilds K4.7 byte for byte.
``scripts/records/check_k3.py --set k4_8_r220`` checks it.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NEW = {
    "k4": Path("data/screens/k4_8_writers/k4"),
    "k4_4": Path("data/screens/k4_8_writers/k4_4"),
}

spec = importlib.util.spec_from_file_location("build_k4_7", HERE / "build_k4_7.py")
K47 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = K47
spec.loader.exec_module(K47)
K45 = K47.K45


def write_writers() -> int:
    """K4.7's writer copies, plus the new K4 and K4.4 question files with the same query strip."""
    changed = [K47.write_writers()]
    for name, source in NEW.items():
        for path in sorted(source.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            data["questions"] = [K45.strip_question(q, changed) for q in data["questions"]]
            text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
            (K45.WRITERS / name / path.name).write_bytes(text.encode("utf-8"))
    return changed[0]


if __name__ == "__main__":
    K45.DIR, K45.WRITERS = Path("data/screens/k4_8"), Path("data/screens/k4_8/writers")
    K45.OUT = Path("data/screens/k4_8_r220.jsonl")
    K45.write_writers = write_writers
    K45.main(record="R-220", never_told_twice=True)
