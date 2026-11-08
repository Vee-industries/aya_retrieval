"""R-122: 6.31's set with rows removed, for a from-scratch try.

Usage: python scripts/records/build_r122.py NAME --drop memory_contrast|sounds_like [...]

6.31 failed by one probe question (R-119): "drawing a blank on my daughter's tattoo" got no search
and a reply of sympathy ("That can be frustrating. Maybe you could try to remember..."). R-117's
contrast rows answer statements with a memory word in that same voice ("Tomas keeps forgetting to
text me back -> That can be annoying. Maybe they've just been busy."). 6.311 and 6.32 added 72
scripted in-view rows and lost found-fact detail (R-120, R-121), so this try adds nothing and only
removes. Two groups can be removed:

- ``memory_contrast``: the R-117 ``contrast/statement_`` rows whose message has a memory word
  (lost, forgetting, forgot); 15 rows;
- ``sounds_like``: the ``in_view`` rows whose answer opens "It sounds like"; 22 rows.

Every other row is kept byte for byte, in order. The build stops if a group's count differs from
the one recorded in R-122.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from aya_retrieval.provenance import run_metadata

DATA = Path("data/screens")
BASE_SET = DATA / "fix17cs31.jsonl"
MEMORY_WORD = re.compile(r"\b(lost|forgetting|forgot)\b")
GROUPS = {
    "memory_contrast": (
        15,
        lambda r: (
            r["id"].startswith("contrast/statement_")
            and MEMORY_WORD.search(r["turns"][-2]["content"])
        ),
    ),
    "sounds_like": (
        22,
        lambda r: r["kind"] == "in_view" and r["turns"][-1]["content"].startswith("It sounds like"),
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name", help="output set name, e.g. fix17cs33")
    parser.add_argument("--drop", nargs="+", choices=sorted(GROUPS), required=True)
    args = parser.parse_args()
    text = BASE_SET.read_text(encoding="utf-8")
    lines = [line for line in text.splitlines(keepends=True) if line]
    rows = [json.loads(line) for line in lines]
    dropped = Counter()
    kept = []
    for line, row in zip(lines, rows, strict=True):
        hit = [g for g in args.drop if GROUPS[g][1](row)]
        if hit:
            dropped[hit[0]] += 1
        else:
            kept.append(line)
    for group in args.drop:
        if dropped[group] != GROUPS[group][0]:
            raise SystemExit(f"{group}: {dropped[group]} rows, R-122 records {GROUPS[group][0]}")
    out = DATA / f"{args.name}.jsonl"
    out.write_text("".join(kept), encoding="utf-8")
    all_rows = [json.loads(line) for line in kept]
    report = {
        "provenance": run_metadata(),
        "base_set": BASE_SET.as_posix(),
        "base_sha256": hashlib.sha256(BASE_SET.read_bytes()).hexdigest(),
        "out_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
        "rows": len(all_rows),
        "dropped": dict(sorted(dropped.items())),
        "statement_rows": sum(r["kind"] == "statement" for r in all_rows),
        "kinds": dict(sorted(Counter(r["kind"] for r in all_rows).items())),
    }
    out.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{out}: {report['rows']} rows, dropped {report['dropped']}, kinds {report['kinds']}")
    print(f"sha256 {report['out_sha256']}")


if __name__ == "__main__":
    main()
