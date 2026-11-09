"""R-162: each sealed-run judge's brief, from R-154's frozen brief with only the allowed changes.

Usage: python scripts/records/briefs_r162.py JUDGE_DIR SHEET [SHEET ...]

Why: R-154 froze the judge's brief (R-128's judge 1) with the rule "the folder path, sheet names and
line counts only" may change. This takes the frozen text and replaces exactly those: the folder in
the file list, the list of sheets with their line counts, the marks files to write, and the count
of files to read. Everything else, the instructions, rubric reference, output format and reply,
stays byte for byte. Prints the brief, so it can be passed to the judge and kept with its marks.
"""

from __future__ import annotations

import sys
from pathlib import Path

FROZEN = Path("results/freeze/R-154/judge_brief_r128_j1.txt")
OLD_DIR = (
    r"C:\Users\Gaming\scratch\claude\C--Users-Gaming-Desktop-Claude-s-House"
    r"\389594c2-8513-47d9-80f1-1a28b96837f7\scratchpad\judge_r128_j1"
)
NUMBERS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}


def sheet_entry(number: int, folder_name: str, sheet: str, lines: int) -> str:
    text_lines = sum(1 for _ in (Path(folder_name) / f"sheet_{sheet}.txt").open(encoding="utf-8"))
    name = f"...\\{Path(folder_name).name}\\sheet_{sheet}.txt"
    entry = f"{number}. {name} ({lines} lines of work, LINE 0 to LINE {lines - 1}"
    if text_lines > 400:
        about = f"{round(text_lines, -2):,}"
        entry += f"; about {about} text lines, so read it in parts with offset and limit"
    return entry + ")"


def main() -> None:
    folder = Path(sys.argv[1])
    sheets = sys.argv[2:]
    frozen = FROZEN.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    counts = {}
    for sheet in sheets:
        text = (folder / f"sheet_{sheet}.txt").read_text(encoding="utf-8")
        counts[sheet] = sum(1 for line in text.split("\n") if line.startswith("LINE "))
    out = []
    for line in frozen:
        if line.startswith("You are a judge"):
            out.append(line.replace("these five files", f"these {NUMBERS[len(sheets) + 1]} files"))
        elif line.startswith("1. "):
            out.append(line.replace(OLD_DIR, str(folder)))
            out += [sheet_entry(n + 2, str(folder), s, counts[s]) for n, s in enumerate(sheets)]
        elif line[:3] in ("2. ", "3. ", "4. ", "5. "):
            continue
        elif line.startswith("marks_b82.json"):
            out.append(", ".join(f"marks_{s}.json" for s in sheets))
        else:
            out.append(line)
    print("\n".join(out), end="")


if __name__ == "__main__":
    main()
