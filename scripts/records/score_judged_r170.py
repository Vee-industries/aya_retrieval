"""R-170, measure 4: judged accuracy from the three judges' marks, after Kevin's 50 lines.

Usage:
    python -I scripts/records/score_judged_r170.py

Why: R-170 registered judged accuracy, labelled "not the official score", by LongMemEval's own judge
prompts and R-154's method: judge 1 decides, judges 2 and 3 are reported. Kevin marks 50 lines blind
before any judged number is read, so this stops unless his marks
(results/analysis/R-170/judge/kevin_marks.json, line number to "yes" or "no") are in. Written
before any mark was read. Per arm, a question is right when judge 1 answered "yes" on its line
(LongMemEval's rule, ``longmemeval_judge.judged_correct``); a question the arm failed on has no
line and counts as wrong. Read on the 148 single-session-user and knowledge-update questions, on
the fixed random 100 of the rest, and on all 248; again on the questions every full arm completed.
Paired exact sign tests and question-resampled 95% intervals (``score_r170.paired``): 6.37 against
base with the tool, and against code that always searches. Beside them: each judge's counts, the
judges' agreement with each other, and Kevin's agreement with each judge (with Cohen's kappa).
Writes results/analysis/R-170/judged.json (aggregates only).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from aya_retrieval.longmemeval_judge import judged_correct
from aya_retrieval.provenance import REPO_ROOT, run_metadata

sys.path.insert(0, str(Path(__file__).parent))
from score_r170 import FULL_ARMS, paired  # noqa: E402

JUDGE = REPO_ROOT / "results" / "analysis" / "R-170" / "judge"
OUT = REPO_ROOT / "results" / "analysis" / "R-170" / "judged.json"
CORE = ("single-session-user", "knowledge-update")
JUDGES = ("j1", "j2", "j3")
DECIDING = "j1"


def kappa(a: list[bool], b: list[bool]) -> float | None:
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b, strict=True)) / n
    pa, pb = sum(a) / n, sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    return None if expected == 1 else round((observed - expected) / (1 - expected), 3)


def load_marks(lines: list[dict]) -> dict[str, dict[int, bool]]:
    """Return each judge's verdict per line, after checking every line is marked once."""
    marks = {}
    for judge in JUDGES:
        verdicts = {}
        for sheet in sorted({line["sheet"] for line in lines}):
            path = JUDGE / "marks" / f"marks_{sheet}_{judge}.json"
            raw = json.loads(path.read_text(encoding="utf-8"))
            if any(v not in ("yes", "no") for v in raw.values()):
                raise ValueError(f"{path}: a mark is neither yes nor no")
            verdicts |= {int(n): judged_correct(v) for n, v in raw.items()}
        if sorted(verdicts) != [line["line"] for line in lines]:
            raise ValueError(f"{judge}'s marks do not cover every line exactly once")
        marks[judge] = verdicts
    return marks


def by_arm(lines: list[dict], verdicts: dict[int, bool]) -> dict[str, dict[str, int]]:
    """Return, per arm, each judged question id mapped to 1 (right) or 0."""
    table: dict[str, dict[str, int]] = {}
    for line in lines:
        table.setdefault(line["arm"], {})[line["id"]] = int(verdicts[line["line"]])
    return table


def share(hits: int, total: int) -> dict:
    return {"hits": hits, "of": total, "rate": round(hits / total, 4) if total else None}


def main() -> None:
    kevin_path = JUDGE / "kevin_marks.json"
    if not kevin_path.exists():
        raise SystemExit(
            "Kevin's 50 marks come first (R-170): no judged number is read before them"
        )
    key = json.loads((JUDGE / "key.json").read_text(encoding="utf-8"))
    lines, questions = key["lines"], key["questions"]
    kinds = {line["id"]: line["type"] for line in lines}
    core = [i for i in questions if kinds.get(i) in CORE]
    rest = [i for i in questions if i not in set(core)]
    marks = load_marks(lines)
    tables = {judge: by_arm(lines, marks[judge]) for judge in JUDGES}
    completed = set(questions)
    for name in FULL_ARMS:
        completed &= set(tables[DECIDING].get(name, {}))
    sets = {"core_148": core, "rest_100": rest, "all_248": questions}

    report = {"provenance": run_metadata(), "record": "R-170", "label": "not the official score"}
    report["judges"] = {}
    for judge in JUDGES:
        report["judges"][judge] = {
            arm: {
                name: share(sum(table.get(i, 0) for i in ids), len(ids))
                for name, ids in sets.items()
            }
            | {"lines": len(table)}
            for arm, table in sorted(tables[judge].items())
        }
    deciding = tables[DECIDING]
    report["completed_by_every_full_arm"] = len(completed)
    report["deciding_on_completed"] = {
        arm: {
            name: share(
                sum(table.get(i, 0) for i in ids if i in completed),
                sum(i in completed for i in ids),
            )
            for name, ids in sets.items()
        }
        for arm, table in sorted(deciding.items())
        if arm in FULL_ARMS
    }
    report["paired"] = {}
    for other in ("base_tool", "always_search"):
        for name, ids in sets.items():
            report["paired"][f"637_tool_vs_{other}_{name}"] = {
                "failures_wrong": paired(deciding["637_tool"], deciding[other], ids),
                "completed_by_every_arm": paired(
                    deciding["637_tool"], deciding[other], [i for i in ids if i in completed]
                ),
            }

    numbers = [line["line"] for line in lines]
    report["judge_agreement"] = {
        f"{a}_{b}": {
            "same": sum(marks[a][n] == marks[b][n] for n in numbers),
            "of": len(numbers),
            "kappa": kappa([marks[a][n] for n in numbers], [marks[b][n] for n in numbers]),
        }
        for a, b in (("j1", "j2"), ("j1", "j3"), ("j2", "j3"))
    }
    human = json.loads((JUDGE / "human_key.json").read_text(encoding="utf-8"))["lines"]
    kevin_raw = json.loads(kevin_path.read_text(encoding="utf-8"))
    if sorted(kevin_raw, key=int) != sorted(human, key=int):
        raise ValueError("Kevin's marks must cover exactly his 50 lines")
    kevin = {human[n]: judged_correct(v) for n, v in kevin_raw.items()}
    shown = sorted(kevin)
    report["kevin_agreement"] = {
        judge: {
            "same": sum(kevin[n] == marks[judge][n] for n in shown),
            "of": len(shown),
            "kappa": kappa([kevin[n] for n in shown], [marks[judge][n] for n in shown]),
        }
        for judge in JUDGES
    }
    report["kevin_yes"] = share(sum(kevin.values()), len(kevin))
    report["deciding_judge_yes_on_kevins_lines"] = share(
        sum(marks[DECIDING][n] for n in shown), len(shown)
    )
    OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "provenance"}, indent=1))


if __name__ == "__main__":
    main()
