"""R-088: two of the panel's sets built from 17b's, by replacing rows, never adding to a pass.

Usage:
    python scripts/records/splice_r088.py replace    writes data/screens/fix17r.jsonl
    python scripts/records/splice_r088.py distinct   writes data/screens/fix17d.jsonl

``replace`` (item 8): 25 of 17b's 150 chat rows, drawn with seed 88, give way to one vetted
fact-word chat line a type, the same lines as fix 20 (R-087); 800 rows. ``distinct`` (item 7):
every chat target both R-078 judges accepted, each message and reply once, plus 17b's other rows
three times over, for one epoch; so each pass sees its search and in-view rows as before and no
chat target twice.
"""

import json
import random
import sys
from pathlib import Path

from aya_retrieval.conversations import STATEMENT
from aya_retrieval.provenance import run_metadata
from aya_retrieval.train_phrasings import MORE_CHAT_FACTS
from aya_retrieval.vetting import all_judges

DATA = Path("data/screens")
BASE_SET = DATA / "strict_chat.jsonl"
FACT_TYPES = [kind for kind, lines in MORE_CHAT_FACTS.items() for _ in lines]


def read_rows(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def accepted(vet: Path) -> set[tuple[str, str]]:
    key = json.loads((vet / "key.json").read_text(encoding="utf-8"))
    marks = all_judges(
        [
            {int(k): int(v) for k, v in json.loads(p.read_text()).items()}
            for p in sorted(vet.glob("judge*/marks.json"))
        ]
    )
    return {(e["source"], e["id"]) for e in key if marks[e["line"]]}


def fact_lines() -> list[dict]:
    """One vetted fact-word chat row a type: the first both R-083 judges accepted."""
    ok, chosen = accepted(Path("results/coherence/R-083V")), {}
    for row in read_rows(DATA / "chat_facts.jsonl"):
        kind = FACT_TYPES[int(row["id"].split("_")[1])]
        if ("data", row["id"]) in ok and kind not in chosen:
            chosen[kind] = {**row, "id": f"facts/{row['id']}"}
    return list(chosen.values())


def strict_targets() -> list[dict]:
    """Every chat row R-078's two judges accepted, each message and reply once, in file order."""
    ok = accepted(Path("results/coherence/R-078"))
    rows = [
        r
        for r in read_rows(DATA / "vetted_brief.jsonl")
        if r["kind"] == STATEMENT
        if ("data", r["id"]) in ok
    ]
    for path in sorted(DATA.glob("strict_spare_*.jsonl")):
        rows += [
            {**r, "id": f"{path.stem}/{r['id']}"}
            for r in read_rows(path)
            if r["kind"] == STATEMENT and ("spare", f"{path.stem}/{r['id']}") in ok
        ]
    seen, out = set(), []
    for row in rows:
        pair = (row["turns"][-2]["content"], row["turns"][-1]["content"])
        if pair not in seen:
            seen.add(pair)
            out.append(row)
    return out


mode = sys.argv[1]
base = read_rows(BASE_SET)
if mode == "replace":
    chat = [i for i, r in enumerate(base) if r["kind"] == STATEMENT]
    added = fact_lines()
    dropped = set(random.Random(88).sample(chat, len(added)))
    rows = [r for i, r in enumerate(base) if i not in dropped] + added
    out, detail = DATA / "fix17r.jsonl", {"dropped": sorted(base[i]["id"] for i in dropped)}
elif mode == "distinct":
    others = [r for r in base if r["kind"] != STATEMENT]
    chat = strict_targets()
    rows = [{**r, "id": f"{r['id']}/pass{n}"} for n in (1, 2, 3) for r in others] + chat
    out, detail = (
        DATA / "fix17d.jsonl",
        {"chat_rows": len(chat), "other_rows_per_pass": len(others)},
    )
else:
    raise SystemExit("mode is replace or distinct")

out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
report = {"provenance": run_metadata(), "mode": mode, "base_set": BASE_SET.as_posix(), **detail}
report["rows"] = len(rows)
out.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
print(f"{out}: {len(rows)} rows, {detail if mode == 'distinct' else len(detail['dropped'])}")
