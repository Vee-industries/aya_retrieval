"""Write a blind coherence sheet as the text the judge reads, with the rubric beside it.

Usage:
    python scripts/render_judge_sheet.py <sheet dir>/sheet.json <judge dir>/sheet.txt [--prefix A]

The judge gets only ``sheet.txt`` and ``rubric.txt``; ``key.json`` stays beside ``sheet.json``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from aya_retrieval.coherence import RUBRIC


def render(rows: list[dict], prefix: str = "") -> str:
    """Each line's turns in view, the newest message and the reply, as the judge reads them."""
    out = []
    for row in rows:
        out.append(f"LINE {prefix}{row['line']}")
        for user, assistant in row["view"]:
            out.append(f"  friend: {user}")
            out.append(f"  you: {assistant}")
        out.append(f"  NEWEST MESSAGE: {row['message']}")
        out.append(f"  REPLY: {row['reply']}")
        out.append("")
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("sheet", type=Path, help="sheet.json from make_coherence_sheet.py")
    parser.add_argument("out", type=Path, help="text file for the judge")
    parser.add_argument("--prefix", default="", help="put before each line number, e.g. A")
    args = parser.parse_args()
    rows = json.loads(args.sheet.read_text(encoding="utf-8"))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(rows, args.prefix), encoding="utf-8")
    (args.out.parent / "rubric.txt").write_text(RUBRIC, encoding="utf-8")
    print(f"{len(rows)} lines written to {args.out}")


if __name__ == "__main__":
    main()
