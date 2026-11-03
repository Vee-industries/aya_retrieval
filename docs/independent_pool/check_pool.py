"""Check an independently written pool before it joins the project. Prints PASS or the problems.

Usage (from the repository folder, with the project's Python):
    python <this file> <path to pool_independent.py> <path to avoid.json>
"""

import importlib.util
import json
import re
import string
import sys
from pathlib import Path

from aya_retrieval import pools
from aya_retrieval.conversations import ITEM_KINDS, build_item

problems: list[str] = []


def need(ok: bool, message: str) -> None:
    if not ok:
        problems.append(message)


def fields(text: str) -> set[str]:
    return {name for _, name, _, _ in string.Formatter().parse(text) if name}


def words(text: str) -> set[str]:
    return set(re.findall(r"[a-z']+", text.casefold()))


spec = importlib.util.spec_from_file_location("pool_independent", sys.argv[1])
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
pool = module.INDEPENDENT
avoid = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))

need(isinstance(pool, pools.Pool), "INDEPENDENT must be a pools.Pool")
need(len(set(pool.people)) >= 10, "at least 10 different people")
need(len(set(pool.relations)) >= 8, "at least 8 different relations")
need(len(pool.facts) >= 5, "at least 5 fact types")
need(len(set(pool.subjects)) >= 32, "at least 32 different small-talk subjects")
need(len(pool.moods) >= 3, "at least 3 moods")
need(len(pool.acknowledgements) >= 6, "at least 6 acknowledgements")
need(len(pool.statements) >= 6, "at least 6 statements")
need(len(pool.unknown_replies) >= 3, "at least 3 unknown replies")
need(all(" " not in p and p[:1].isupper() for p in pool.people), "people: one capitalised word each")
need(all(r == r.casefold() for r in pool.relations), "relations: lower case")

for kind, items in (("people", pool.people), ("relations", pool.relations), ("subjects", pool.subjects)):
    taken = {a.casefold() for a in avoid[kind]}
    clash = [x for x in items if x.casefold() in taken]
    need(not clash, f"{kind}: {len(clash)} already used by another pool, choose others")
taken_values = {a.casefold() for a in avoid["values"]}
for kind, items in (
    ("fact_type_names", list(pool.facts)),
    ("acknowledgements", pool.acknowledgements),
    ("unknown_replies", pool.unknown_replies),
):
    clash = [x for x in items if x in set(avoid.get(kind, []))]
    need(not clash, f"{kind}: {len(clash)} identical to another pool's, write different ones")

all_values = []
for name, t in pool.facts.items():
    vals = [v.casefold() for v in t.values]
    need(len(set(vals)) >= 6, f"fact {name}: at least 6 different values")
    need(not [v for v in vals if v in taken_values], f"fact {name}: some values already used elsewhere")
    for v in vals:
        others = [o for o in vals if o != v and v in o]
        need(not others, f"fact {name}: a value is inside another value")
    all_values += vals
    need(fields(t.statement) == {"person", "relation", "value"}, f"fact {name}: statement needs {{person}} {{relation}} {{value}}")
    need(fields(t.same_words) == {"person"}, f"fact {name}: same_words needs only {{person}}")
    for form in ("new_words", "indirect", "confirm"):
        need(fields(getattr(t, form)) == {"relation"}, f"fact {name}: {form} needs only {{relation}}")
    need(fields(t.query) == {"who"}, f"fact {name}: query needs only {{who}}")
    need({"person", "value"} <= fields(t.answer) <= {"person", "relation", "value"}, f"fact {name}: answer needs {{person}} and {{value}}")

small_talk = " ".join(
    [*pool.subjects, *pool.acknowledgements, *pool.unknown_replies]
    + [x for m in pool.moods for x in (*m.user_lines, *m.replies)]
    + [x for pair in pool.statements for x in pair]
).casefold()
need(not [v for v in all_values if re.search(rf"\b{re.escape(v)}\b", small_talk)], "a fact value appears in small talk")
for m in pool.moods:
    need(all(fields(x) == {"subject"} for x in m.user_lines), "mood user lines need exactly {subject}")
    need(all(fields(x) <= {"subject"} for x in m.replies), "mood replies may use only {subject}")
    need(len(m.user_lines) >= 5 and len(m.replies) >= 5, "each mood: at least 5 user lines and 5 replies")
for line, reply in pool.statements:
    need(fields(line) <= {"person", "relation"} and fields(line), "statements: line uses {person} and/or {relation}")
    need(not fields(reply), "statements: reply has no placeholders")
need(all(not fields(a) for a in pool.acknowledgements + pool.unknown_replies), "acknowledgements and unknown replies: no placeholders")

train_forms = {
    " ".join(getattr(t, f).split())
    for t in pools.TRAIN.facts.values()
    for f in ("statement", "same_words", "new_words", "indirect", "confirm")
}
need(
    not any(" ".join(getattr(t, f).split()) in train_forms for t in pool.facts.values()
            for f in ("statement", "same_words", "new_words", "indirect", "confirm")),
    "a question or statement form is identical to a training one",
)

if not problems:
    pools.POOLS["independent"] = pool
    failures = 0
    for size in (58, 419):
        for k, kind in enumerate(ITEM_KINDS):
            for decoys in (1, 2, 3, 4):
                for n in range(25):
                    seed = 900000 + size * 1000 + k * 100 + n + decoys * 10000
                    try:
                        item = build_item(f"{size}_{kind}_{n:02d}", seed, size, kind, "independent", decoys)
                    except Exception as error:  # noqa: BLE001
                        failures += 1
                        problems.append(f"building {kind} at {size} with {decoys} decoys: {type(error).__name__}: {error}")
                        continue
                    view = " ".join(u + " " + a for u, a in item.view()).casefold()
                    older = " ".join(u + " " + a for u, a in item.older()).casefold()
                    if kind == "older" or kind == "confirm":
                        need(item.answer.casefold() not in view and item.answer.casefold() in older, f"{kind}: answer must be told before the view only")
                        need(item.answer.casefold() not in item.message.casefold(), f"{kind}: the question gives the answer away")
                    if kind == "in_view":
                        need(item.answer.casefold() in view, "in_view: answer must be in view")
                    if kind == "never_told" and decoys == 1:
                        told = " ".join(u for u, _ in item.exchanges).casefold()
                        need(item.answer == "" and item.decoy.casefold() in told, "never_told: the decoy must be told and nothing answered")
                        need(not any(v.casefold() in told for v in item.forbidden if v != item.decoy), "never_told: a value other than the decoy appears in the chat")
                    if failures > 5:
                        break

if not problems:
    from collections import Counter

    long_chat = build_item("x", 3, 419, "older", "independent")
    top = Counter(r for _, r in long_chat.exchanges).most_common(1)[0][1]
    need(
        top <= len(long_chat.exchanges) * 0.08,
        "variety: in the project's 419-message test chat one reply makes up more than 8% of "
        "replies; write more mood replies and acknowledgements",
    )

problems = list(dict.fromkeys(p for p in problems if p))
print("PASS" if not problems else "PROBLEMS:\n- " + "\n- ".join(problems[:40]))
