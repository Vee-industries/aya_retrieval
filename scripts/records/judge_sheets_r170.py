"""R-170, measure 4: the blind judge sheets, the judges' briefs, and Kevin's 50 lines.

Usage:
    python -I scripts/records/judge_sheets_r170.py \
        --data C:/Users/Gaming/Downloads/longmemeval/longmemeval_s_cleaned.json \
        --judge-root C:/Users/Gaming/scratch/.../scratchpad

Why: R-170 registered judged accuracy, labelled "not the official score": LongMemEval's own per-type
judge prompts (``aya_retrieval.longmemeval_judge``), given to three fresh Claude Sonnet judges blind
to arm, by R-154's method (each judge in its own folder, judge 1 decides, judges 2 and 3 reported).
The lines are every arm's reply on the single-session-user and knowledge-update questions (148),
plus a fixed random 100 of the rest (``random.Random(1704)``, from the sorted ids). An arm's line
exists where it ran the question to a reply, after the out-of-memory rerun; a failure or a skip has
no line. Each line is one filled prompt, shuffled with the arm's name removed
(``random.Random(1705)``), in sheets of at most 200. Kevin marks a random 50 of the lines blind
(``random.Random(1706)``) before any judged number is read, so the judges' brief asks for no counts.

Writes, without any chat, question or reply text: results/analysis/R-170/judge/key.json (each line's
question id, arm, type and sheet) and briefs. With text, outside git: the sheets into
``<judge-root>/judge_r170_j{1,2,3}/`` and Kevin's lines into results/longmemeval/human/sheet.json.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

from aya_retrieval.longmemeval import load_longmemeval
from aya_retrieval.longmemeval_judge import SOURCE, judge_prompt
from aya_retrieval.provenance import REPO_ROOT

sys.path.insert(0, str(Path(__file__).parent))
from score_r170 import ARMS, done, load_arm  # noqa: E402

OUT = REPO_ROOT / "results" / "analysis" / "R-170" / "judge"
HUMAN = REPO_ROOT / "results" / "longmemeval" / "human"
CORE = ("single-session-user", "knowledge-update")  # every arm's reply on these is judged
REST_SAMPLE, SELECT_SEED, SHUFFLE_SEED, HUMAN_SEED = 100, 1704, 1705, 1706
SHEET_SIZE, HUMAN_LINES, JUDGES = 200, 50, ("j1", "j2", "j3")

# ruff: noqa: E501 (the brief keeps one paragraph a line, as R-154's frozen brief does)
BRIEF = """You are a judge marking answers to questions about long chats. Read exactly this file and no others:

{sheet_path} ({lines} lines of work, LINE {first} to LINE {last}; about {text_lines:,} text lines, so read it in parts with offset and limit)

Do not open, list or search any other file or folder, and do not look for any key or answer file.

Each LINE is one complete judging prompt: its instructions, a question, the correct answer (or a rubric, or an explanation), and a model's response, ending in a question for you. Answer each LINE's question yourself, by reading it, exactly as its instructions say: yes or no. Judge every line on its own. Do not write or run code that decides answers; read and judge each line. Cover every line.

When the sheet is fully marked, write your answers as one JSON object mapping each line number (as a string) to "yes" or "no", covering every line of the sheet, into the same folder as the sheet:
{marks_path}
Example of the format: {{"0": "yes", "1": "no"}}
Write the file with a single Bash heredoc that contains the JSON you typed out (cat > file <<'EOF' ... EOF). Write no other files anywhere: no scripts, no notes, no temporary files.

Reply with only: the marks file you wrote, how many lines it covers, and a confirmation that you judged every line by reading it. Do not give counts of yes or no, or any reasons.
"""


def select(items) -> list[str]:
    """Return R-170's judged questions: every core-type question, then a fixed random 100 of the rest."""
    core = sorted(i.item_id for i in items if i.kind in CORE)
    rest = sorted(i.item_id for i in items if i.kind not in CORE)
    return core + sorted(random.Random(SELECT_SEED).sample(rest, REST_SAMPLE))


def build_lines(items, arms: dict[str, dict]) -> list[dict]:
    """Return one line per judged question and arm that ran it to a reply, shuffled, numbered."""
    by_id = {item.item_id: item for item in items}
    lines = []
    for item_id in select(items):
        item = by_id[item_id]
        for name, rows in arms.items():
            row = rows.get(item_id)
            if not done(row):
                continue
            prompt = judge_prompt(
                item.kind, item.question, item.answer, row["reply"], item.abstention
            )
            lines.append({"id": item_id, "arm": name, "type": item.kind, "prompt": prompt})
    random.Random(SHUFFLE_SEED).shuffle(lines)
    for number, line in enumerate(lines):
        line["line"] = number
        line["sheet"] = f"L{number // SHEET_SIZE + 1}"
        line["abstention"] = by_id[line["id"]].abstention
    return lines


def sheet_text(lines: list[dict]) -> str:
    return "".join(f"===== LINE {line['line']} =====\n{line['prompt']}\n\n" for line in lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, required=True, help="longmemeval_s_cleaned.json")
    parser.add_argument("--judge-root", type=Path, required=True, help="scratch folder for judges")
    args = parser.parse_args()

    items, digest = load_longmemeval(args.data)
    arms = {}
    for name in ARMS:
        arm = load_arm(name, digest, len(items))
        if not arm or arm["status"] != "completed":
            raise SystemExit(f"{name} did not complete; R-170's sheets need every arm")
        arms[name] = arm["rows"]
    lines = build_lines(items, arms)
    sheets = sorted({line["sheet"] for line in lines}, key=lambda s: int(s[1:]))

    OUT.mkdir(parents=True, exist_ok=True)
    key = {
        "record": "R-170",
        "data_sha256": digest,
        "prompts": SOURCE,
        "seeds": {"select": SELECT_SEED, "shuffle": SHUFFLE_SEED, "human": HUMAN_SEED},
        "questions": select(items),
        "lines": [
            {k: line[k] for k in ("line", "sheet", "id", "arm", "type", "abstention")}
            for line in lines
        ],
    }
    (OUT / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    for judge in JUDGES:
        folder = args.judge_root / f"judge_r170_{judge}"
        folder.mkdir(parents=True, exist_ok=True)
        for sheet in sheets:
            chosen = [line for line in lines if line["sheet"] == sheet]
            text = sheet_text(chosen)
            sheet_path = folder / f"sheet_{sheet}.txt"
            sheet_path.write_text(text, encoding="utf-8")
            brief = BRIEF.format(
                sheet_path=sheet_path,
                lines=len(chosen),
                first=chosen[0]["line"],
                last=chosen[-1]["line"],
                text_lines=round(text.count("\n"), -2),
                marks_path=folder / f"marks_{sheet}.json",
            )
            (OUT / f"brief_{sheet}_{judge}.txt").write_text(brief, encoding="utf-8")

    human = sorted(random.Random(HUMAN_SEED).sample(range(len(lines)), HUMAN_LINES))
    HUMAN.mkdir(parents=True, exist_ok=True)
    shown = [{"n": n + 1, "prompt": lines[i]["prompt"]} for n, i in enumerate(human)]
    (HUMAN / "sheet.json").write_text(
        json.dumps(shown, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "human_key.json").write_text(
        json.dumps({"record": "R-170", "lines": {n + 1: i for n, i in enumerate(human)}}, indent=1),
        encoding="utf-8",
    )
    counts = {s: sum(line["sheet"] == s for line in lines) for s in sheets}
    print(json.dumps({"lines": len(lines), "sheets": counts, "human": HUMAN_LINES}))


if __name__ == "__main__":
    main()
