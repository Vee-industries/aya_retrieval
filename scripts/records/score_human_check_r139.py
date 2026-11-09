"""Score Kevin's blind check of the scorer (R-139, item 5) against the scorer's verdicts.

Usage: python scripts/records/score_human_check_r139.py

Why: the scorer calls a reply right when it contains the answer and no wrong value. Kevin marked
50 replies right or wrong without seeing the model or the scorer's verdict (sheet.json). His marks
(marks.json) were saved before key.json was read. Agreement and Cohen's kappa say how far the
scorer's verdicts can be trusted; each disagreement is listed so its cause can be read.
A second person marked the same 50 lines on a plain sheet (second_marker_sheet.txt), independently
and without the key; marks_second.json holds her marks, compared with the scorer and with Kevin.

Writes results/human_check/R-139/agreement.json.
"""

import json
from collections import Counter
from pathlib import Path

DIR = Path("results/human_check/R-139")
SHOWN = ("kind", "question", "right_answer", "wrong_values", "reply")


def kappa(a: list[bool], b: list[bool]) -> float:
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b, strict=True)) / n
    pa, pb = sum(a) / n, sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    return (observed - expected) / (1 - expected)


def main() -> None:
    sheet = {e["n"]: e for e in json.loads((DIR / "sheet.json").read_text(encoding="utf-8"))}
    key = {e["n"]: e for e in json.loads((DIR / "key.json").read_text(encoding="utf-8"))}
    raw = json.loads((DIR / "marks.json").read_text(encoding="utf-8"))
    marks = {int(n): m.lower() == "r" for n, m in raw.items()}
    assert sorted(marks) == sorted(sheet) == sorted(key) == list(range(1, 51))
    ns = sorted(marks)
    kevin = [marks[n] for n in ns]
    scorer = [key[n]["scorer"] for n in ns]
    table = Counter((k, s) for k, s in zip(kevin, scorer, strict=True))
    by_stratum = Counter()
    for n in ns:
        by_stratum[(key[n]["stratum"], marks[n] == key[n]["scorer"])] += 1
    disagreements = [
        {
            "n": n,
            "kevin": "right" if marks[n] else "wrong",
            "scorer": "right" if key[n]["scorer"] else "wrong",
            **{k: key[n][k] for k in ("model", "label", "id", "stratum")},
            **{k: sheet[n][k] for k in SHOWN},
        }
        for n in ns
        if marks[n] != key[n]["scorer"]
    ]
    report = {
        "n": len(ns),
        "agree": sum(k == s for k, s in zip(kevin, scorer, strict=True)),
        "kappa": round(kappa(kevin, scorer), 3),
        "kevin_right_scorer_right": table[(True, True)],
        "kevin_right_scorer_wrong": table[(True, False)],
        "kevin_wrong_scorer_right": table[(False, True)],
        "kevin_wrong_scorer_wrong": table[(False, False)],
        "agree_by_stratum": {
            s: f"{by_stratum[(s, True)]}/{by_stratum[(s, True)] + by_stratum[(s, False)]}"
            for s in sorted({key[n]["stratum"] for n in ns})
        },
        "disagreements": disagreements,
    }
    second = json.loads((DIR / "marks_second.json").read_text(encoding="utf-8"))
    other = [second["marks"][str(n)] == "R" for n in ns]
    report["second_marker"] = {
        "agree_with_scorer": sum(o == s for o, s in zip(other, scorer, strict=True)),
        "kappa_with_scorer": round(kappa(other, scorer), 3),
        "agree_with_kevin": sum(o == k for o, k in zip(other, kevin, strict=True)),
        "kappa_with_kevin": round(kappa(other, kevin), 3),
        "differs_from_scorer": [n for n, o, s in zip(ns, other, scorer, strict=True) if o != s],
        "differs_from_kevin": [n for n, o, k in zip(ns, other, kevin, strict=True) if o != k],
        "notes": second["notes"],
    }
    text = json.dumps(report, indent=1, ensure_ascii=False)
    (DIR / "agreement.json").write_text(text, encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "disagreements"}, indent=1))
    for d in disagreements:
        print(d["n"], d["kevin"], d["scorer"], d["model"], d["kind"], "|", d["right_answer"])
        print("   ", d["reply"][:200].replace("\n", " "))


if __name__ == "__main__":
    main()
