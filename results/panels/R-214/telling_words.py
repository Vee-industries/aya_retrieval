"""R-214: the words writers use to state each category's fact, from the K3 training chats only.

For each category, content words of the fact messages (not the value, not a person's name, not a
stop or filler word), counted once per message; reported with the share of that category's
messages holding each word, and how often first queries already hold the source message's words.

Usage: python results/panels/R-214/telling_words.py
"""

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

WRITERS = Path("data/screens/k4_5/writers/k3")
STOP = set(
    """a an the and or but so to of in on at for with from by is are was were be been am i im i'm
    my me we our you your he she they them his her their it its this that just got get gets
    getting like really very lol haha ok okay so yeah oh also too now then today yesterday week
    weekend last next new one two some all about up out over still been going go went have has
    had do does did not no dont don't can cant can't will would could should finally actually
    kind sort pretty little bit much more most thing things time day days way back off say said
    tell told mention remember again know think what where which who is""".split()
)


def words(text: str) -> list[str]:
    return [w.removesuffix("'s") for w in re.findall(r"[a-z']+", text.casefold())]


by_cat, n_cat = defaultdict(Counter), Counter()
for path in sorted(WRITERS.glob("*.json")):
    for chat in json.loads(path.read_text(encoding="utf-8"))["chats"]:
        names = set()
        for m in chat["messages"]:
            if m.get("fact") and m["fact"].get("person") and m["fact"]["person"] != "me":
                names |= set(words(m["fact"]["person"]))
        for m in chat["messages"][:21]:
            fact = m.get("fact")
            if not fact:
                continue
            value = set(words(fact["value"]))
            keep = {w for w in words(m["user"]) if w not in STOP | value | names and len(w) > 2}
            by_cat[fact["category"]].update(keep)
            n_cat[fact["category"]] += 1

for cat in sorted(by_cat):
    top = ", ".join(f"{w} {c / n_cat[cat]:.0%}" for w, c in by_cat[cat].most_common(6))
    print(f"{cat} ({n_cat[cat]} messages): {top}")
