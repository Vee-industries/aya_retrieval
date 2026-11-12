"""R-198: candidate K1.2's training set, K1.1's build with each row's draw picked by passages.

Usage: python scripts/records/build_r198.py --index C:/scratch/build_r198.sqlite

K1.2 = K1.1 (``build_r196.py``) with one change. K1.1's drawn wordings share fewer words with the
questions, so its searches return fewer passages, and never_told rows lose more than found rows:
the found against never_told passage gap opened to 0.57 (R-197). Here each row that gets F2 tries
up to ``TRIES`` draws of its added lines' wordings (``build_r196.DRAW_OFFSET`` = 0, 100, 200, ...;
draw 0 is K1.1's) and takes the first whose search returns at least as many passages as K1's same
row; if none does, it takes the first draw with the most. The choice uses the row's own search
only; no model runs. The rule is the same for every kind of row that searches, and covers the
three ways K1 builds an F2 row: rows rebuilt from the training builder, R-102's rows, and the
fresh never_told rows that replace a row whose search returns nothing. Rows of a kind with no
search keep K1.1's draw. Everything else is K1.1's code unchanged.

The provenance file gets each row's draw and a count of the F2 fact lines in a template wording
and in a drawn one, counted on the conversations as built (before F3), so lines out of view count
too. ``scripts/records/check_r198.py`` then checks the set before any training.
"""

from __future__ import annotations

import importlib.util
import json
import random
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.conversations import NEEDS_SEARCH
from aya_retrieval.pools import TRAIN

HERE = Path(__file__).resolve().parent
OUT = Path("data/screens/k1_2_r198.jsonl")
TRIES = 8
DRAW_STEP = 100  # well above the at most five added lines a row's draws are numbered by
VALUES = tuple(v for t in TRAIN.facts.values() for v in t.values)


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look the module up by name
    spec.loader.exec_module(module)
    return module


K11 = load("build_r196")
K1 = K11.K1
WORDINGS = K11.WORDINGS
k1_builder_item = K1.builder_item  # K1's own, with template wordings throughout
k1_build_item = K1.build_item
k1_with_r102_change = K1.with_r102_change
picked: dict[str, int] = {}  # row id -> the draw taken
reached: dict[str, bool] = {}  # row id -> whether that draw reached K1's passage count
lines = Counter()  # F2 fact lines as built, by wording
r102_args: dict[str, tuple] = {}  # the last F2 build_item call per item id, with its share


def index_path() -> Path:
    return Path(sys.argv[sys.argv.index("--index") + 1])


def passages(item) -> int:
    return K1.search(item, item.query, index_path())[0].count("chunk_id=")


def at_draw(make, draw: int | None):
    """Build with ``make`` at draw ``draw``; ``None`` builds K1's template wordings."""
    K11.WORDINGS = WORDINGS if draw is not None else {}
    K11.DRAW_OFFSET = DRAW_STEP * (draw or 0)
    try:
        return make(draw is not None)
    finally:
        K11.WORDINGS, K11.DRAW_OFFSET = WORDINGS, 0


def pick(row_id: str, make, plain, count: bool = True):
    """Return the row's F2 conversation at the first draw reaching K1's passages (R-198).

    ``make(drawn)`` builds the conversation, as K1 when ``drawn`` is false; ``plain`` is the same
    conversation without F2, used only to count the fact lines F2 added.
    """
    k1 = at_draw(make, None)
    if k1.kind not in NEEDS_SEARCH:  # a row with no search keeps K1.1's draw
        item = at_draw(make, 0)
    else:
        target = passages(k1)
        counts = {}
        for draw in range(TRIES):
            counts[draw] = passages(at_draw(make, draw))
            if counts[draw] >= target:
                break
        reach = [d for d in counts if counts[d] >= target]
        best = reach[0] if reach else max(counts, key=counts.get)
        item = at_draw(make, best)
        picked[row_id], reached[row_id] = best, bool(reach)
    if count:
        for before, ours, theirs in zip(plain.exchanges, item.exchanges, k1.exchanges, strict=True):
            if before != theirs and any(v in theirs[0] for v in VALUES):
                lines["template" if ours == theirs else "drawn"] += 1
    return item


def k1_2_builder_item(row_id, kind, source, share=None):
    """K1.1's builder_item, with the row's draw picked by its search's passage count."""
    if share is None:
        return k1_builder_item(row_id, kind, source)

    def make(drawn):
        build = K11.k1_1_builder_item if drawn else k1_builder_item
        return build(row_id, kind, source, share)

    return pick(row_id, make, k1_builder_item(row_id, kind, source))


def k1_2_build_item(item_id, *args, other_facts=None, **kwargs):
    """K1's build_item, keeping the arguments of each F2 call so an R-102 row can be rebuilt."""
    if other_facts is not None:
        r102_args[item_id] = (args, kwargs, other_facts)
    return k1_build_item(item_id, *args, other_facts=other_facts, **kwargs)


def k1_2_with_r102_change(plain, changed, other):
    """K1's R-102 change, with the row's draw picked by the same rule."""
    args, kwargs, share = r102_args[plain.item_id]

    def make(_drawn):
        again = k1_build_item(plain.item_id, *args, other_facts=share, **kwargs)
        return k1_with_r102_change(plain, changed, again)

    return pick(changed.item_id, make, changed)


def k1_2_fresh_never_told(n, share, index, tokenizer):
    """K1.1's fresh never_told row, with each tried seed's draw picked by the same rule."""
    seed = K1.FRESH_SEED + 1000 * n
    row_id = f"k1/never_told_{n:04d}"
    while True:
        seed += 1
        decoys = random.Random(seed).choice(K1.BUILDER.DECOY_CHOICES[K1.NEVER_TOLD])

        def make(drawn, seed=seed, decoys=decoys, other_facts=share):
            return k1_build_item(
                row_id,
                seed,
                K1.BUILDER.SIZE,
                K1.NEVER_TOLD,
                "train",
                decoys,
                True,
                drawn,
                True,
                other_facts=other_facts,
            )

        item = pick(row_id, make, make(False, other_facts=None), count=False)
        output, _ = K1.search(item, item.query, index)
        turns = K1.demonstration_turns(item, output, item.reply, False, item.reply)
        fits = K1.BUILDER.row_tokens(turns, tokenizer) <= K1.BUILDER.MAX_ROW_TOKENS
        if "chunk_id=" in output and fits:
            pick(row_id, make, make(False, other_facts=None))  # the kept seed counts its lines
            return {"id": item.item_id, "kind": K1.NEVER_TOLD, "turns": turns}


if __name__ == "__main__":
    K1.builder_item = k1_2_builder_item
    K1.build_item = k1_2_build_item
    K1.with_r102_change = k1_2_with_r102_change
    K1.fresh_never_told = k1_2_fresh_never_told
    sys.modules["aya_retrieval.conversations"].MORE_STATEMENTS = WORDINGS
    sys.modules["aya_retrieval.conversations"].add_other_facts = K11.k1_1_add_other_facts
    if "--out" not in sys.argv:
        sys.argv += ["--out", str(OUT)]
    out = Path(sys.argv[sys.argv.index("--out") + 1])
    K1.main()
    provenance = out.with_suffix(".provenance.json")
    report = json.loads(provenance.read_text(encoding="utf-8"))
    report["record"] = "R-198"
    report["tries"] = TRIES
    report["f2_fact_lines"] = dict(lines)
    report["draws"] = dict(Counter(picked.values()))
    report["rows_not_reaching_k1"] = sorted(r for r, ok in reached.items() if not ok)
    report["picked"] = dict(sorted(picked.items()))
    provenance.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(
        f"draws {report['draws']}, lines {dict(lines)}, short {len(report['rows_not_reaching_k1'])}"
    )
