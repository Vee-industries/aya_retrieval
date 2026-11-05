"""R-083: add the vetted fix 18 chat rows to fix 17b's set, as 18a (fact lines) and 18c (control).

Usage: python scripts/records/splice_r083.py <vetting dir with key.json and judge*/marks.json>

A target is kept only if every judge accepted it. 18a and 18c get the same number of rows: the first
accepted rows of each set, in build order, so the two differ only in which lines they teach.
"""

import json
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.provenance import run_metadata
from aya_retrieval.train_phrasings import MORE_CHAT_FACTS
from aya_retrieval.vetting import all_judges

DATA = Path("data/screens")
BASE_SET = DATA / "strict_chat.jsonl"
SETS = {"data": ("facts", DATA / "chat_facts.jsonl"), "spare": ("plain", DATA / "chat_plain.jsonl")}
OUT = {"facts": DATA / "fix18a.jsonl", "plain": DATA / "fix18c.jsonl"}
FACT_TYPES = [kind for kind, lines in MORE_CHAT_FACTS.items() for _ in lines]


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


vet = Path(sys.argv[1])
key = json.loads((vet / "key.json").read_text(encoding="utf-8"))
mark_files = sorted(vet.glob("judge*/marks.json"))
judges = [{int(k): int(v) for k, v in json.loads(p.read_text()).items()} for p in mark_files]
marks = all_judges(judges)
accepted = {name: set() for name, _ in SETS.values()}
for entry in key:
    if marks[entry["line"]]:
        accepted[SETS[entry["source"]][0]].add(entry["id"])

kept = {}
for name, path in SETS.values():
    kept[name] = [row for row in read_rows(path) if row["id"] in accepted[name]]
size = min(len(rows) for rows in kept.values())
dropped_by_type = Counter(
    FACT_TYPES[int(row["id"].split("_")[1])]
    for row in read_rows(SETS["data"][1])
    if row["id"] not in accepted["facts"]
)

base_rows = read_rows(BASE_SET)
for name, rows in kept.items():
    added = [{**row, "id": f"{name}/{row['id']}"} for row in rows[:size]]
    out = OUT[name]
    lines = (json.dumps(row, ensure_ascii=False) for row in base_rows + added)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    report = {
        "provenance": run_metadata(),
        "base_set": BASE_SET.as_posix(),
        "added_from": SETS["data" if name == "facts" else "spare"][1].as_posix(),
        "marks": [p.as_posix() for p in mark_files],
        "accepted": {n: len(a) for n, a in accepted.items()},
        "added": size,
        "rows": len(base_rows) + size,
        "facts_rejected_by_type": dict(sorted(dropped_by_type.items())),
        "judges_agree": sum(len({j[line] for j in judges}) == 1 for line in judges[0]),
    }
    out.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{out}: {len(base_rows)} + {size} rows")
print("accepted:", {n: len(a) for n, a in accepted.items()})
print("rejected facts by type:", dict(dropped_by_type))
