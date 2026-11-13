"""R-191: screening with base as the standard to beat, for K1 and K2.1, and the pick for S3.

The recall lines of R-178 item 4 compare with base with the search tool (rerun for R-191 at the
current code, labels ``*_base191``) instead of 6.37: each candidate's recall must be above base's at
each seed, on probe, hard_dev, the outside-writer sets and the other-facts stress. Every other line
is R-178's, unchanged: in_view, statement and never_told minimums, false retrieval against 6.37,
and the failure-mode targets T3 and T2 against 6.37. A candidate that passes every line is
eligible; of the eligible ones, the higher pooled dev recall (probe, hard_dev and outside-writer)
over seeds 82, 83 and 94 (R-192) goes to S3 as the shippable arm.

Usage:
    python scripts/records/decide_r191.py
"""

from __future__ import annotations

import json

from aya_retrieval.report_data import EVAL_DIR, false_retrieval

CANDIDATES = {
    "K1": "k1_r178",
    "K2.1": "k2_1_r187",
    "K1.3": "k1_3_r200",
    "K4.1": "k4_1_r209",  # R-209; K1.2, K3, K3.1, K3.2 and K4 did not reach screening
    "K4.2": "k4_2_r210",  # R-210 (bombed Demo2)
    "K4.3": "k4_3_r211",  # R-211 (not trained)
    "K4.4": "k4_4_r212",  # R-212 (bombed Demo2)
    "K4.5": "k4_5_r213",  # R-213 (bombed Demo2)
    "K4.6": "k4_6_r214",  # R-214 (bombed Demo2)
    "K4.7": "k4_7_r215",  # R-215 (bombed Demo2)
    "K4.6e2": "k4_6e2_r214",  # R-219: K4.6 seeds read at epoch 2
}
REF = "fix17cs37"
BASE = "base191"
SEEDS = (82, 83)
PICK_SEEDS = (82, 83, 94)  # R-192: the pick uses a third seed; the lines stay at 82 and 83
RECALL = ("older", "confirm")


def rows(label: str, seed: int) -> list[dict] | None:
    path = EVAL_DIR / f"{label}_seed_{seed}.json"
    if not path.exists():
        return None
    return [
        r for r in json.loads(path.read_text(encoding="utf-8"))["rows"] if r["arm"] == "tool_loop"
    ]


def count(label: str, seed: int, kinds, field: str = "correct") -> int | None:
    got = rows(label, seed)
    return None if got is None else sum(bool(r.get(field)) for r in got if r["kind"] in kinds)


def total(*vals) -> int | None:
    return None if None in vals else sum(vals)


def screen(name: str) -> tuple[list[tuple[str, str]], int | None]:
    lines: list[tuple[str, str]] = []

    def line(text, value, ok):
        lines.append(("WAIT" if value is None else ("PASS" if ok else "FAIL"), text))

    recall_parts = []
    for s in SEEDS:
        for stem, probe_seed in (("probe", 73157), ("hd", 73157)):
            v = count(f"{stem}_{name}_{s}", probe_seed, RECALL)
            b = count(f"{stem}_{BASE}", probe_seed, RECALL)
            line(f"{stem} recall seed {s} {v} above base's {b}", total(v, b), total(v, b) and v > b)
            recall_parts.append(v)
        v = total(*(count(f"{p}_{name}_{s}", 0, RECALL) for p in ("blind", "blind2")))
        b = total(*(count(f"{p}_{BASE}", 0, RECALL) for p in ("blind", "blind2")))
        line(
            f"outside-writer recall seed {s} {v} above base's {b}",
            total(v, b),
            total(v, b) and v > b,
        )
        recall_parts.append(v)
        v = total(*(count(f"st_of_{p}_{name}_{s}", 73157, RECALL) for p in ("probe", "hd")))
        b = total(*(count(f"st_of_{p}_{BASE}", 73157, RECALL) for p in ("probe", "hd")))
        line(
            f"T2 other-facts recall seed {s} {v} above base's {b}",
            total(v, b),
            total(v, b) and v > b,
        )

        v = count(f"probe_{name}_{s}", 73157, ("in_view",))
        line(f"probe in_view seed {s} {v} at least 41", v, v is not None and v >= 41)
        v = count(f"probe_{name}_{s}", 73157, ("statement",))
        line(f"probe statement seed {s} {v} at least 44 of 48", v, v is not None and v >= 44)
        v = count(f"hd_{name}_{s}", 73157, ("never_told",))
        line(f"hard_dev never_told seed {s} {v} at least 44 of 48", v, v is not None and v >= 44)
        for stem in ("probe", "hd"):
            if rows(f"{stem}_{name}_{s}", 73157) is None:
                line(f"{stem} false retrieval seed {s}", None, False)
                continue
            fr = sum(h for h, _ in false_retrieval(f"{stem}_{name}_{s}", 73157).values())
            ref = sum(h for h, _ in false_retrieval(f"{stem}_{REF}_{s}", 73157).values())
            line(
                f"{stem} false retrieval seed {s} {fr} at most 6.37's {ref} plus 3",
                fr,
                fr <= ref + 3,
            )

    def stress(stem, label, field, kinds):
        return total(
            *(
                count(f"st_{stem}_{p}_{label}_{s}", 73157, kinds, field)
                for p in ("probe", "hd")
                for s in SEEDS
            )
        )

    c, c_ref = (
        stress("wb", n, "copied_wrong", ("older", "confirm", "in_view")) for n in (name, REF)
    )
    line(
        f"T3 copies {c} at most half of 6.37's {c_ref}",
        total(c, c_ref),
        total(c, c_ref) and c <= c_ref / 2,
    )
    f, f_ref = (stress("of", n, "false_answer", ("never_told",)) for n in (name, REF))
    line(
        f"T2 false answers {f} at most half of 6.37's {f_ref}",
        total(f, f_ref),
        total(f, f_ref) and f <= f_ref / 2,
    )
    return lines, total(*recall_parts)


def pick_recall(name: str) -> int | None:
    """Pooled dev recall over PICK_SEEDS: probe, hard_dev, and both outside-writer sets."""
    return total(
        *(
            count(f"{stem}_{name}_{s}", seed, RECALL)
            for s in PICK_SEEDS
            for stem, seed in (("probe", 73157), ("hd", 73157), ("blind", 0), ("blind2", 0))
        )
    )


def main() -> None:
    eligible = {}
    for label, name in CANDIDATES.items():
        lines, pooled = screen(name)
        for status, text in lines:
            print(f"{status:5} {label}: {text}")
        fails = sum(s == "FAIL" for s, _ in lines)
        waits = sum(s == "WAIT" for s, _ in lines)
        print(f"== {label}: {fails} FAIL, {waits} WAIT, pooled dev recall {pooled} (R-191)")
        if fails == 0 and waits == 0:
            eligible[label] = pick_recall(name)
            print(f"== {label}: pick recall over seeds {PICK_SEEDS}: {eligible[label]} (R-192)")
    if None in eligible.values():
        print("== pick waits on seed 94 results")
    elif eligible:
        pick = max(eligible, key=eligible.get)
        print(f"== shippable arm for S3: {pick} (pick recall {eligible[pick]})")
    else:
        print("== no candidate eligible")


if __name__ == "__main__":
    main()
