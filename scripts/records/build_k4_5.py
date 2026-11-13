"""K4.5's training set (R-213): K4.4's whole build rerun with possessives taken out of every query.

Usage: python scripts/records/build_k4_5.py

The search tool quotes each query word as an FTS phrase, so a possessive ("marguerite's") becomes
the phrase "marguerite s" and finds only text with the same possessive (R-212). K1.3's template
queries hold no apostrophe; the writers' natural queries hold 59 in K4.4. K4.5 writes copies of the
three writer folders (K3, K4, K4.4) under ``data/screens/k4_5/writers/`` with "'s" and a trailing
"'" taken out of every ``query`` and ``second_query``, nothing else changed, and reruns each build
step on them, every search included: K3.1 (``build_k3_1``), K3.2, K4.1, K4.3 (``build_k4_2`` with
never_told kinds) and K4.4. Intermediate sets go to ``data/screens/k4_5/`` (their provenance
``record`` fields name the step's own record); the result is ``data/screens/k4_5_r213.jsonl``.
``scripts/records/check_k3.py --set k4_5_r213`` then checks it.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIR = Path("data/screens/k4_5")
WRITERS = DIR / "writers"
OUT = Path("data/screens/k4_5_r213.jsonl")
SOURCES = {
    "k3": Path("data/screens/k3_writers"),
    "k4": Path("data/screens/k4_writers"),
    "k4_4": Path("data/screens/k4_4_writers"),
}


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def strip(query: str) -> str:
    """Take "'s" and a trailing "'" off each word ("marguerite's" -> "marguerite")."""
    query = re.sub(r"['’]s\b", "", query)
    return re.sub(r"['’](?=\s|$)", "", query)


def strip_question(q: dict, changed: list[int]) -> dict:
    out = dict(q)
    for field in ("query", "second_query"):
        if out.get(field) and strip(out[field]) != out[field]:
            out[field] = strip(out[field])
            changed[0] += 1
    return out


def write_writers() -> int:
    changed = [0]
    for name, source in SOURCES.items():
        (WRITERS / name).mkdir(parents=True, exist_ok=True)
        for path in sorted(source.glob("*.json")):
            data = json.loads(path.read_text(encoding="utf-8"))
            if "chats" in data:
                for chat in data["chats"]:
                    chat["questions"] = [strip_question(q, changed) for q in chat["questions"]]
            else:
                data["questions"] = [strip_question(q, changed) for q in data["questions"]]
            text = json.dumps(data, ensure_ascii=False, indent=1) + "\n"
            (WRITERS / name / path.name).write_bytes(text.encode("utf-8"))
    return changed[0]


def main(record: str = "R-213", never_told_twice: bool = False, third_query=None) -> None:
    """Rerun the chain; ``never_told_twice`` (R-214) and ``third_query`` (R-226) apply to the K3
    writers' rows only."""
    print(f"queries changed: {write_writers()}")
    k3, k4, k4_4 = WRITERS / "k3", WRITERS / "k4", WRITERS / "k4_4"

    k31 = load("build_k3_1")
    k31.K3.WRITERS, k31.OUT = k3, DIR / "k3_1.jsonl"
    k31.K3.NEVER_TOLD_TWICE = never_told_twice
    k31.K3.THIRD_QUERY = third_query
    k31.main()

    k32 = load("build_k3_2")
    k32.BASE, k32.OUT = k31.OUT, DIR / "k3_2.jsonl"
    k32.main()

    k41 = load("build_k4_1")
    k41.K4.BASE, k41.K4.K3_WRITERS, k41.K4.WRITERS = k32.OUT, k3, k4
    k41.K4.main(out_path=DIR / "k4_1.jsonl", record=record, row_filter=k41.k3_1_drops)

    k42 = load("build_k4_2")
    k42.BASE, k42.K3.WRITERS, k42.K4_WRITERS = DIR / "k4_1.jsonl", k3, k4
    k42.main(out_path=DIR / "k4_3.jsonl", record=record, kinds={"never_told"})

    k44 = load("build_k4_4")
    k44.BASE, k44.WRITERS, k44.OUT, k44.K3.WRITERS = DIR / "k4_3.jsonl", k4_4, OUT, k3
    k44.main(record=record)


if __name__ == "__main__":
    main()
