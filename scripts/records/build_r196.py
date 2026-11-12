"""R-196: candidate K1.1's training set, K1's build with F2 chats' fact lines in drawn wordings.

Usage: python scripts/records/build_r196.py --index C:/scratch/build_r196.sqlite

K1.1 = K1 (``build_r178.py``) with one change. In K1, and in 6.37, every fact line uses its type's
one template statement, so a passage's fact type can be read off its fixed wording; hard_dev's
lines use other wordings (R-196, method lane). Here each chat that gets F2 states its facts in
the template's own wording or one of ``train_phrasings.MORE_STATEMENTS``, drawn per line:

- Rows rebuilt from the training builder are built with ``more_statements`` when a share is
  given, so the rebuild check and ``found_before`` stay K1's. The same holds for the fresh
  never_told rows that replace a row whose search returns nothing.
- F2's added lines draw their wording from ``random.Random(seed + 8 + index)``, a generator of
  their own, so every slot, person and value is K1's. R-102's rows keep their own fact lines;
  only their F2 lines change.
- The paint wording "the whole house is" is left out of every draw: it shares four words with a
  hard_dev statement.

Everything else is K1's code unchanged. ``scripts/records/check_r196.py`` then checks the set
before any training.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import random
import sys
from pathlib import Path

from aya_retrieval import conversations
from aya_retrieval.conversations import OTHER_FACT_SHARES
from aya_retrieval.pools import POOLS
from aya_retrieval.train_phrasings import MORE_STATEMENTS

HERE = Path(__file__).resolve().parent
OUT = Path("data/screens/k1_1_r196.jsonl")
LEFT_OUT = "news from my {relation} {person}: the whole house is {value} this year"
WORDINGS = {
    statement: tuple(w for w in more if w != LEFT_OUT)
    for statement, more in MORE_STATEMENTS.items()
}
DRAW_OFFSET = 0  # R-198 redraws by changing this; at 0 every draw is R-196's


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look the module up by name
    spec.loader.exec_module(module)
    return module


K1 = load("build_r178")
k1_builder_item = K1.builder_item


def k1_1_builder_item(row_id, kind, source, share=None):
    """K1's builder_item, stating the chat's facts in drawn wordings when a share is given."""
    if share is None:
        return k1_builder_item(row_id, kind, source)
    item = K1.build_item(
        row_id,
        source.seed,
        K1.BUILDER.SIZE,
        kind,
        "train",
        source.decoys,
        True,
        True,
        True,
        other_facts=share,
    )
    return dataclasses.replace(item, query=source.query) if source.query else item


def k1_1_fresh_never_told(n, share, index, tokenizer):
    """K1's fresh never_told row, with the chat's facts in drawn wordings."""
    seed = K1.FRESH_SEED + 1000 * n
    while True:
        seed += 1
        decoys = random.Random(seed).choice(K1.BUILDER.DECOY_CHOICES[K1.NEVER_TOLD])
        item = K1.build_item(
            f"k1/never_told_{n:04d}",
            seed,
            K1.BUILDER.SIZE,
            K1.NEVER_TOLD,
            "train",
            decoys,
            True,
            True,
            True,
            other_facts=share,
        )
        output, _ = K1.search(item, item.query, index)
        turns = K1.demonstration_turns(item, output, item.reply, False, item.reply)
        fits = K1.BUILDER.row_tokens(turns, tokenizer) <= K1.BUILDER.MAX_ROW_TOKENS
        if "chunk_id=" in output and fits:
            return {"id": item.item_id, "kind": K1.NEVER_TOLD, "turns": turns}


def k1_1_add_other_facts(item, seed, pool_name, share, asked):
    """``conversations.add_other_facts``, with each added line's wording drawn (R-196).

    A copy of the original whose one change is the marked line pair; see its docstring.
    """
    if share not in OTHER_FACT_SHARES:
        raise ValueError(f"unknown share {share!r}")
    rng = random.Random(seed + 7)
    pool = POOLS[pool_name]
    own = next(name for name, t in sorted(pool.facts.items()) if item.decoy in t.values)
    values = [v for t in pool.facts.values() for v in t.values]
    exchanges = list(item.exchanges)
    older = len(exchanges) - conversations.EXCHANGES_IN_VIEW
    free = [
        i
        for i in range(older)
        if i != item.fact_index and not any(v in exchanges[i][0] for v in values)
    ]
    said = conversations._words(" ".join([item.message, *(u + " " + r for u, r in exchanges)]))
    people = [p for p in pool.people if p.casefold() not in said and p != asked[1]]
    unsaid = [r for r in pool.relations if r.casefold() not in said and r != asked[0]]
    reused = [r for r in pool.relations if r != asked[0]]

    count = rng.randint(2, 4)
    types = rng.sample([name for name in sorted(pool.facts) if name != own], count - 1)
    pair = rng.sample(pool.facts[types[0]].values, 2)
    plan = [(types[0], pair[0]), (types[0], pair[1])]
    plan += [(name, rng.choice(pool.facts[name].values)) for name in types[1:]]
    lines = []
    for index, (name, value) in enumerate(plan):
        about_asked = share == "same_person" and index != 1 and (index == 0 or rng.random() < 0.5)
        if about_asked:
            relation, person = asked
        elif people:
            relation = unsaid.pop(rng.randrange(len(unsaid))) if unsaid else rng.choice(reused)
            person = people.pop(rng.randrange(len(people)))
        else:
            continue
        # R-196's change: the wording is drawn, from a generator of its own.
        statement = pool.facts[name].statement
        draw = random.Random(seed + 8 + index + DRAW_OFFSET)
        wording = draw.choice((statement, *WORDINGS.get(statement, ())))
        line = wording.format(relation=relation, person=person, value=value)
        lines.append((line, rng.choice(pool.acknowledgements)))
    if share == "shared_word":
        names = {w.casefold() for w in (*pool.people, *pool.relations)}
        ordinary = [
            w
            for w in item.query.casefold().split()
            if w not in names and not w.endswith("ed") and len(w) >= 3
        ]
        if ordinary:
            mood = rng.choice(pool.moods)
            subject = f"the {ordinary[-1]}"
            reply = rng.choice(mood.replies).format(subject=subject)
            lines.append(
                (rng.choice(mood.user_lines).format(subject=subject), reply[0].upper() + reply[1:])
            )
    for slot, line in zip(rng.sample(free, min(len(free), len(lines))), lines, strict=False):
        exchanges[slot] = line
    return dataclasses.replace(item, exchanges=tuple(exchanges))


if __name__ == "__main__":
    conversations.MORE_STATEMENTS = WORDINGS
    conversations.add_other_facts = k1_1_add_other_facts
    K1.builder_item = k1_1_builder_item
    K1.fresh_never_told = k1_1_fresh_never_told
    if "--out" not in sys.argv:
        sys.argv += ["--out", str(OUT)]
    K1.main()
