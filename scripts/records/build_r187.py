"""R-187: candidate K2.1's training set: K2's build, the moved rows' share picked by passages.

Usage: python scripts/records/build_r187.py --index C:/scratch/build_r187.sqlite

K2.1 = K2 (``build_r185.py``) with one change. K2 moved every second same_person never_told row to
``same_type``, and those rows return fewer passages, which opened the found against never_told
passage gap to 0.39 (R-186). Here each moved row tries ``same_type`` and then ``shared_word``, and
takes the first whose search returns at least as many passages as the same row with
``same_person`` (K1's version); if neither does, it takes the one that returns more. The choice
uses the row's own search only; no model runs. R-189: the pick also covers R-102's rows, which
are built through ``with_r102_change`` rather than ``builder_item``. Everything else is K2's
code unchanged.
``scripts/records/check_r185.py --set k2_1_r187`` then checks the set before any training.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path("data/screens/k2_1_r187.jsonl")
TRY = ("same_type", "shared_word")


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look the module up by name
    spec.loader.exec_module(module)
    return module


K2 = load("build_r185")
K1 = K2.K1
moved: set[str] = set()
picked: dict[str, str] = {}
k1_builder_item = K1.builder_item


def k2_1_shares(rows, rebuilt) -> dict[str, str]:
    """K2's shares, noting which rows K2 moved off same_person."""
    k1 = K2.k1_shares(rows, rebuilt)
    shares = K2.k2_shares(rows, rebuilt)
    moved.update(i for i, share in shares.items() if share != k1[i])
    return shares


def passages(item, index: Path) -> int:
    return K1.search(item, item.query, index)[0].count("chunk_id=")


def k2_1_builder_item(row_id, kind, source, share=None):
    """K1's builder_item, with a moved row's share picked by its search's passage count."""
    if row_id in moved and share == "same_type":
        if row_id not in picked:
            index = Path(sys.argv[sys.argv.index("--index") + 1])
            target = passages(k1_builder_item(row_id, kind, source, "same_person"), index)
            counts = {s: passages(k1_builder_item(row_id, kind, source, s), index) for s in TRY}
            reach = [s for s in TRY if counts[s] >= target]
            picked[row_id] = reach[0] if reach else max(TRY, key=counts.get)
        share = picked[row_id]
    last_built[0] = row_id if share is not None else last_built[0]
    return k1_builder_item(row_id, kind, source, share)


last_built = [None]  # the row f2_item built last; main replaces it right after, if it must
k1_fresh_never_told = K1.fresh_never_told
k1_build_item = K1.build_item
k1_with_r102_change = K1.with_r102_change
r102_args: dict[str, tuple] = {}  # the last F2 build_item call per item id
r102_picked: set[str] = set()  # moved R-102 rows, picked in k2_1_with_r102_change


def k2_1_build_item(item_id, *args, other_facts=None, **kwargs):
    """K1's build_item, keeping the arguments of each F2 call so an R-102 row can be rebuilt."""
    if other_facts is not None:
        r102_args[item_id] = (args, kwargs)
    return k1_build_item(item_id, *args, other_facts=other_facts, **kwargs)


def k2_1_with_r102_change(plain, changed, other):
    """K1's R-102 change, with a moved R-102 row's share picked by the same rule (R-189)."""
    row_id = changed.item_id
    if row_id in moved:
        if row_id not in picked:
            index = Path(sys.argv[sys.argv.index("--index") + 1])
            args, kwargs = r102_args[plain.item_id]

            def final(share):
                again = k1_build_item(plain.item_id, *args, other_facts=share, **kwargs)
                return k1_with_r102_change(plain, changed, again)

            target = passages(final("same_person"), index)
            counts = {s: passages(final(s), index) for s in TRY}
            reach = [s for s in TRY if counts[s] >= target]
            picked[row_id] = reach[0] if reach else max(TRY, key=counts.get)
            r102_picked.add(row_id)
        last_built[0] = row_id
        args, kwargs = r102_args[plain.item_id]
        other = k1_build_item(plain.item_id, *args, other_facts=picked[row_id], **kwargs)
    else:
        last_built[0] = row_id
    return k1_with_r102_change(plain, changed, other)


def k2_1_fresh_never_told(n, share, index, tokenizer):
    """K1's replacement never_told row, in the share picked for the row it replaces."""
    return k1_fresh_never_told(n, picked.get(last_built[0], share), index, tokenizer)


if __name__ == "__main__":
    K1.f2_shares = k2_1_shares
    K1.builder_item = k2_1_builder_item
    K1.fresh_never_told = k2_1_fresh_never_told
    K1.build_item = k2_1_build_item
    K1.with_r102_change = k2_1_with_r102_change
    if "--out" not in sys.argv:
        sys.argv += ["--out", str(OUT)]
    out = Path(sys.argv[sys.argv.index("--out") + 1])
    K1.main()
    unseen = moved - set(picked)
    if unseen:  # R-187: a moved row that skipped the pick stops the build; there is no K2.1
        out.unlink()
        raise SystemExit(f"moved rows that skipped the pick: {sorted(unseen)}")
    provenance = out.with_suffix(".provenance.json")
    report = json.loads(provenance.read_text(encoding="utf-8"))
    report["record"] = "R-187, R-189"
    report["picked_r102_rows"] = sorted(r102_picked)
    report["picked"] = dict(sorted(picked.items()))
    report["picked_counts"] = dict(Counter(picked.values()))
    # main's tally names K2's share for a moved row; these are the shares the moved rows got.
    report["note"] = "tally never_told_share_* counts moved rows under same_type; see picked"
    provenance.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"moved {len(moved)}, picked {report['picked_counts']}")
