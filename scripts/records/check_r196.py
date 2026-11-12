"""R-196's check before training: K1.1's set against the registered lines, with K1 for scale.

Lines (a FAIL on any one means nothing trains):
1. Of the fact lines in the builder rows that F2 changed (ids without "/", turns not 6.37's), the
   share in a ``MORE_STATEMENTS`` wording is 72% to 78%, counted over view turns and the "User:"
   lines of search outputs.
2. Four-word runs shared by the statement wordings the set uses and hard_dev's forms: 0.
3. never_told rows with passages: all of them; found against never_told mean passage gap at most
   0.37 (R-185's lines 3 and 4).
4. With each drawn wording mapped back to its template, every turn but the search output and the
   last reply equals K1's, in every row but the fresh never_told rows (``k1/never_told_*``); rows
   whose last reply differs are at most the build's now-missed and scripted-target rows.
Reported only: found rows, now-missed rows, never_told rows naming the asked person.

Usage:
    python scripts/records/check_r196.py
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from aya_retrieval.conversations import NEEDS_SEARCH, NEVER_TOLD
from aya_retrieval.pool_hard_dev import HARD_DEV
from aya_retrieval.pools import TRAIN
from aya_retrieval.stress import _statement_pattern

HERE = Path(__file__).resolve().parent
DATA = HERE.parents[1] / "data" / "screens"
SHARE = (0.72, 0.78)
MAX_GAP = 0.37
FIELDS = ("statement", "same_words", "new_words", "indirect", "confirm")


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


CHECK = load_module("check_r185")
WORDINGS = {
    statement: more
    for statement, more in load_module("build_r196").WORDINGS.items()
    if any(t.statement == statement for t in TRAIN.facts.values())
}
TEMPLATES = [
    (_statement_pattern(t.statement, TRAIN, t.values), t.statement, t.statement)
    for t in TRAIN.facts.values()
]
MORE = [
    (_statement_pattern(w, TRAIN, t.values), w, t.statement)
    for t in TRAIN.facts.values()
    for w in WORDINGS.get(t.statement, ())
]


def rows(name: str) -> list[dict]:
    text = (DATA / f"{name}.jsonl").read_text(encoding="utf-8")
    return [json.loads(line) for line in text.splitlines()]


def wording(line: str) -> tuple[str, str, str] | None:
    """Return (kind, wording, line mapped to its template) for a fact line, else None."""
    for kind, patterns in (("template", TEMPLATES), ("more", MORE)):
        for pattern, used, template in patterns:
            found = pattern.fullmatch(line)
            if found:
                return kind, used, template.format(**found.groupdict())
    return None


def mapped(text: str) -> str:
    got = wording(text)
    return got[2] if got else text


def grams(text: str, n: int = 4) -> set[tuple[str, ...]]:
    words = re.findall(r"[a-z']+", re.sub(r"\{\w+\}", " ", text.casefold()))
    return {tuple(words[i : i + n]) for i in range(len(words) - n + 1)}


def fact_lines(row: dict) -> list[str]:
    lines = []
    for turn in row["turns"]:
        if turn["content"].startswith("Tool result for"):
            lines += re.findall(r"^User: (.*)$", turn["content"], re.M)
        elif turn["role"] == "user":
            lines.append(turn["content"])
    return lines


def tool_output(turn: dict) -> bool:
    return turn["content"].startswith("Tool result for")


def main() -> None:
    ref, k1, k11 = rows("fix17cs37"), rows("k1_r178"), rows("k1_1_r196")
    tally = json.loads((DATA / "k1_1_r196.provenance.json").read_text(encoding="utf-8"))["tally"]
    ref_by_id = {r["id"]: r for r in ref}

    counts = {"template": 0, "more": 0}
    used = set()
    for row in k11:
        if "/" in row["id"] or row["turns"] == ref_by_id[row["id"]]["turns"]:
            continue
        for line in fact_lines(row):
            got = wording(line)
            if got:
                counts[got[0]] += 1
                used.add(got[1])
    share = counts["more"] / max(1, sum(counts.values()))

    hd_forms = [getattr(t, f) for t in HARD_DEV.facts.values() for f in FIELDS]
    hd_grams = set().union(*(grams(f) for f in hd_forms))
    shared = sorted({" ".join(g) for w in used for g in grams(w) if g in hd_grams})

    s = CHECK.stats(k11)
    gap = abs(s["found_mean"] - s["never_told_mean"])

    other, last, fresh = [], 0, 0
    for a, b in zip(k1, k11, strict=True):
        if a["id"].startswith("k1/never_told_") or b["id"].startswith("k1/never_told_"):
            fresh += a != b
            continue
        keep = [i for i, t in enumerate(b["turns"][:-1]) if not tool_output(t)]
        if len(a["turns"]) != len(b["turns"]) or any(
            mapped(a["turns"][i]["content"]) != mapped(b["turns"][i]["content"]) for i in keep
        ):
            other.append(b["id"])
        elif a["turns"][-1] != b["turns"][-1]:
            last += 1
    allowed = sum(v for k, v in tally.items() if k.endswith(("_now_missed", "_scripted_target")))

    low, high = SHARE
    checks = [
        (
            f"drawn wordings {counts['more']} of {sum(counts.values())} fact lines ({share:.1%}), "
            f"{low:.0%} to {high:.0%}",
            low <= share <= high,
        ),
        (f"four-word runs shared with hard_dev forms {len(shared)} {shared}", not shared),
        (
            f"never_told with passages {s['with_passages']} of {s['never_told']}",
            s["with_passages"] == s["never_told"],
        ),
        (f"mean passage gap {gap:.2f} at most {MAX_GAP}", gap <= MAX_GAP),
        (f"rows unlike K1 beyond wording and last reply {len(other)} {other[:5]}", not other),
        (f"rows whose last reply differs {last}, at most {allowed}", last <= allowed),
    ]
    for text, ok in checks:
        print(f"{'PASS' if ok else 'FAIL':5} {text}")
    found = [
        sum(r["kind"] in NEEDS_SEARCH and r["kind"] != NEVER_TOLD for r in s) for s in (k11, k1)
    ]
    now_missed = sum(v for k, v in tally.items() if k.endswith("_now_missed"))
    print(
        f"report: found rows {found[0]} (K1 {found[1]}), "
        f"now-missed {now_missed}, never_told naming the asked person {s['asked_person']} "
        f"(K1 {CHECK.stats(k1)['asked_person']}), fresh never_told rows that differ {fresh}"
    )
    print(f"== k1_1_r196 check: {sum(not ok for _, ok in checks)} FAIL (R-196 lines)")


if __name__ == "__main__":
    main()
