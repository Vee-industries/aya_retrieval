"""K5's training set (R-226): K4.8's build with a third search before a natural row declines.

Usage: python scripts/records/build_k5.py

Every K4 candidate answered the same 2 of Demo2's 6 older items; most misses are facts no search
returns, since the fact message uses words unlike the question, and a natural row whose two
searches miss teaches a decline (R-225's lane). K5 reruns K4.8's chain with one change to the K3
writers' rows (``build_k3.THIRD_QUERY``): a fact row whose two searches miss searches a third time,
and a never_told row that searched twice searches a third time and keeps it if it returns text;
then the reply. The third query is R-214's telling-words query (``telling_words_r214.second_query``:
the person's words and the asked category's 3 most telling words from the K3 training chats), used
only when it differs from both of the question's queries. The eval allows 3 searches
(``harness.MAX_CALLS``). With ``third_query=None`` it rebuilds K4.8 byte for byte.
``scripts/records/check_k3.py --set k5_r226`` checks it.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


TELLING = load("telling_words_r214")
K48 = load("build_k4_8")
K45 = K48.K45


def third_query(question: dict) -> str | None:
    """R-214's telling-words query for the question's asked category."""
    return TELLING.second_query(question)


def main(third=third_query, out: Path = Path("data/screens/k5_r226.jsonl")) -> None:
    K45.DIR = out.parent / out.stem.split("_r")[0]  # k5_r226 -> data/screens/k5
    K45.WRITERS, K45.OUT = K45.DIR / "writers", out
    K45.write_writers = K48.write_writers
    K45.main(record="R-226", never_told_twice=True, third_query=third)


if __name__ == "__main__":
    main()
