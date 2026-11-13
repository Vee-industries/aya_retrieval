"""R-214, rejected: K4.5's build with second queries made of each category's telling words.

Usage: python scripts/records/telling_words_r214.py (rejected in R-214, kept as its record)

K4.5 (``build_k4_5.py``) passed hard_dev on seed 82 and bombed Demo2: of its four older misses,
three were never returned by any of its searches. The writers' second queries are guessed synonyms
("motor engine" for a car), not the words people use when they state that kind of fact. K4.6
keeps K4.5 whole and changes one thing: every natural question's ``second_query`` becomes the
person's words as the question writes them (at most 2) and the 3 most common telling words of the
asked category not already in the first query. Telling words come from the K3 training chats only:
the content words of each category's fact messages (not the value, not a person's name, not a stop
word), counted once per message, kept if at least 8 times as common in that category's messages as
in all fact messages, ranked by share. The vocabulary is written to
``data/screens/k4_6_rejected/telling_words.json``. Then K4.5's chain reruns, every search included.
Not checked or trained: it lowered second-search hits on the training chats.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DIR = Path("data/screens/k4_6_rejected")
OUT = DIR / "k4_6_telling_words.jsonl"
LIFT = 8
TELLING = 3
STOP = set(
    """a an the and or but so to of in on at for with from by is are was were be been am i im my me
    we our you your he she they them his her their it its this that just got get like really
    very lol haha ok okay yeah oh also too now then today yesterday week weekend last next new
    one two some all about up out over still going go went have has had do does did not no dont
    can cant will would could should finally actually kind sort pretty little bit much more most
    thing things time day days way back off say said tell told mention remember again know think
    what where which who whats whos shes hes theyre were ive youre""".split()
)

spec = importlib.util.spec_from_file_location("build_k4_5", HERE / "build_k4_5.py")
K45 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = K45
spec.loader.exec_module(K45)


def words(text: str) -> list[str]:
    return [w.removesuffix("'s").strip("'") for w in re.findall(r"[a-z']+", text.casefold())]


def vocabulary() -> dict[str, list[str]]:
    """Each category's telling words, from the K3 writer chats' fact messages 1 to 21."""
    by_cat, n_cat, overall, n_all = defaultdict(Counter), Counter(), Counter(), 0
    for path in sorted(K45.SOURCES["k3"].glob("*.json")):
        for chat in json.loads(path.read_text(encoding="utf-8"))["chats"]:
            names = set()
            for m in chat["messages"]:
                if m.get("fact") and (m["fact"].get("person") or "me") != "me":
                    names |= set(words(m["fact"]["person"]))
            for m in chat["messages"][:21]:
                fact = m.get("fact")
                if not fact:
                    continue
                drop = STOP | set(words(fact["value"])) | names
                keep = {
                    w for w in words(m["user"]) if w not in drop and len(w) > 2 and "'" not in w
                }
                by_cat[fact["category"]].update(keep)
                overall.update(keep)
                n_cat[fact["category"]] += 1
                n_all += 1
    vocab = {}
    for cat, counts in sorted(by_cat.items()):
        ranked = [
            w
            for w, c in counts.most_common()
            if c >= 2 and (c / n_cat[cat]) >= LIFT * overall[w] / n_all
        ]
        vocab[cat] = ranked[:8]
    return vocab


VOCAB = vocabulary()


def second_query(q: dict) -> str | None:
    if not q.get("query") or q.get("category") not in VOCAB:
        return q.get("second_query")
    first = set(words(q["query"]))
    asked = set(words(q["question"]))
    person = [] if (q.get("person") or "me") == "me" else words(q["person"])
    person = [w for w in person if w in asked and w not in STOP][:2]
    value = set(words(q.get("value") or ""))
    telling = [w for w in VOCAB[q["category"]] if w not in first and w not in value][:TELLING]
    return " ".join(person + telling) or q.get("second_query")


def strip_question(q: dict, changed: list[int]) -> dict:
    out = K45_STRIP(q, changed)
    new = second_query(out)
    if new != out.get("second_query"):
        out["second_query"] = new
        changed[0] += 1
    return out


K45_STRIP = K45.strip_question


def main() -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    text = json.dumps(VOCAB, indent=1) + "\n"
    (DIR / "telling_words.json").write_bytes(text.encode("utf-8"))
    K45.DIR, K45.WRITERS, K45.OUT = DIR, DIR / "writers", OUT
    K45.strip_question = strip_question
    K45.main(record="R-214")


if __name__ == "__main__":
    main()
