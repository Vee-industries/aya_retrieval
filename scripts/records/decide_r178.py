"""R-178 item 4: K1's screening gates and targets against 6.37 at seeds 82 and 83, as registered.

Prints each line as PASS, FAIL or WAIT (a result file not written yet). K1 enters S3 only if every
line passes.

Usage:
    python scripts/records/decide_r178.py [NAME]
"""

from __future__ import annotations

import json
import sys

from aya_retrieval.report_data import EVAL_DIR, false_retrieval

NAME = sys.argv[1] if len(sys.argv) > 1 else "k1_r178"
REF = "fix17cs37"
SEEDS = (82, 83)
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


def pooled(stem: str, name: str, seed: int, kinds, field: str = "correct") -> int | None:
    vals = [count(f"{stem}_{name}_{s}", seed, kinds, field) for s in SEEDS]
    return None if None in vals else sum(vals)


lines: list[tuple[str, str]] = []


def line(text: str, value, ok) -> None:
    lines.append(("WAIT" if value is None else ("PASS" if ok else "FAIL"), text))


got, ref = pooled("probe", NAME, 73157, RECALL), pooled("probe", REF, 73157, RECALL)
line(
    f"probe recall pooled {got} at least 6.37's {ref} minus 4",
    got,
    got is not None and got >= ref - 4,
)
for s in SEEDS:
    v = count(f"probe_{NAME}_{s}", 73157, ("in_view",))
    line(f"probe in_view at seed {s} {v} at least 41", v, v is not None and v >= 41)
    v = count(f"probe_{NAME}_{s}", 73157, ("statement",))
    line(f"probe statement at seed {s} {v} at least 44 of 48", v, v is not None and v >= 44)
    v = count(f"hd_{NAME}_{s}", 73157, ("never_told",))
    line(f"hard_dev never_told at seed {s} {v} at least 44 of 48", v, v is not None and v >= 44)
    for stem in ("probe", "hd"):
        if rows(f"{stem}_{NAME}_{s}", 73157) is None:
            line(f"{stem} false retrieval at seed {s}", None, False)
            continue
        fr = sum(h for h, _ in false_retrieval(f"{stem}_{NAME}_{s}", 73157).values())
        fr_ref = sum(h for h, _ in false_retrieval(f"{stem}_{REF}_{s}", 73157).values())
        line(
            f"{stem} false retrieval at seed {s} {fr} at most 6.37's {fr_ref} plus 3",
            fr,
            fr <= fr_ref + 3,
        )
got, ref = pooled("hd", NAME, 73157, RECALL), pooled("hd", REF, 73157, RECALL)
line(
    f"hard_dev recall pooled {got} at least 6.37's {ref} minus 12",
    got,
    got is not None and got >= ref - 12,
)
blind = [count(f"{p}_{NAME}_{s}", 0, RECALL) for p in ("blind", "blind2") for s in SEEDS]
blind_ref = [count(f"{p}_{REF}_{s}", 0, RECALL) for p in ("blind", "blind2") for s in SEEDS]
b = None if None in blind else sum(blind)
line(
    f"outside-writer recall pooled {b} at least 6.37's {sum(blind_ref)} minus 10",
    b,
    b is not None and b >= sum(blind_ref) - 10,
)


# Targets on the dev stresses (pooled over probe and hard_dev and both seeds).
def stress_total(kind_stem: str, name: str, field: str, kinds) -> int | None:
    vals = [
        count(f"st_{kind_stem}_{p}_{name}_{s}", 73157, kinds, field)
        for p in ("probe", "hd")
        for s in SEEDS
    ]
    return None if None in vals else sum(vals)


c, c_ref = (
    stress_total("wb", n, "copied_wrong", ("older", "confirm", "in_view")) for n in (NAME, REF)
)
line(
    f"T3 copies of an earlier wrong value {c} at most half of 6.37's {c_ref}",
    c,
    c is not None and c_ref is not None and c <= c_ref / 2,
)
f, f_ref = (stress_total("of", n, "false_answer", ("never_told",)) for n in (NAME, REF))
r, r_ref = (stress_total("of", n, "correct", RECALL) for n in (NAME, REF))
line(
    f"T2 other-facts never_told false answers {f} at most half of 6.37's {f_ref}",
    f,
    f is not None and f_ref is not None and f <= f_ref / 2,
)
line(
    f"T2 other-facts recall {r} not more than 5 below 6.37's {r_ref}",
    r,
    r is not None and r_ref is not None and r >= r_ref - 5,
)

for status, text in lines:
    print(f"{status:5} {text}")
fails = sum(s == "FAIL" for s, _ in lines)
waits = sum(s == "WAIT" for s, _ in lines)
print(f"== {NAME}: {fails} FAIL, {waits} WAIT, {len(lines) - fails - waits} PASS (R-178 item 4)")
