"""R-087: fix 20, fix 17b's set plus one vetted fact chat line and one indirect question a type.

Usage: python scripts/records/splice_r087.py

The chat line of each type is its first one, in build order, that both R-083 judges accepted. The
indirect questions are ``data/screens/indirect_all.jsonl``, one ``older`` row per type.
"""

import json
from pathlib import Path

from aya_retrieval.provenance import run_metadata
from aya_retrieval.train_phrasings import MORE_CHAT_FACTS
from aya_retrieval.vetting import all_judges

DATA = Path("data/screens")
VET = Path("results/coherence/R-083V")
BASE_SET, CHAT, ADDED = (
    DATA / "strict_chat.jsonl",
    DATA / "chat_facts.jsonl",
    DATA / "indirect_all.jsonl",
)
OUT = DATA / "fix20.jsonl"
FACT_TYPES = [kind for kind, lines in MORE_CHAT_FACTS.items() for _ in lines]


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


key = json.loads((VET / "key.json").read_text(encoding="utf-8"))
mark_files = sorted(VET.glob("judge*/marks.json"))
marks = all_judges(
    [{int(k): int(v) for k, v in json.loads(p.read_text()).items()} for p in mark_files]
)
accepted = {e["id"] for e in key if e["source"] == "data" and marks[e["line"]]}

chosen = {}
for row in read_rows(CHAT):
    kind = FACT_TYPES[int(row["id"].split("_")[1])]
    if row["id"] in accepted and kind not in chosen:
        chosen[kind] = {**row, "id": f"facts/{row['id']}"}
indirect = [{**row, "id": f"indirect/{row['id']}"} for row in read_rows(ADDED)]
missing = sorted(set(MORE_CHAT_FACTS) - set(chosen))
if missing or len(indirect) != len(MORE_CHAT_FACTS):
    raise SystemExit(f"types without a chat line: {missing}; indirect rows: {len(indirect)}")

base_rows = read_rows(BASE_SET)
rows = base_rows + list(chosen.values()) + indirect
OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
report = {
    "provenance": run_metadata(),
    "base_set": BASE_SET.as_posix(),
    "chat_lines": {kind: row["id"] for kind, row in sorted(chosen.items())},
    "indirect_from": ADDED.as_posix(),
    "marks": [p.as_posix() for p in mark_files],
    "rows": len(rows),
}
OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print(f"{OUT}: {len(base_rows)} + {len(chosen)} chat + {len(indirect)} indirect rows")
