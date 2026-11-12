"""Read-only: where K1.1 lost passages against K1, by line type, from the two existing sets.

Each returned "User:" line of a search output is classed as: the asked type (the answer line or a
decoy, from the builder, not touched by R-198's redraw), another type (an F2 line, the only lines
R-198's redraw changes), or small talk. Counts are per kind, K1 against K1.1, on rows with the same id.
"""

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

from aya_retrieval.pools import TRAIN
from aya_retrieval.stress import _statement_pattern
from aya_retrieval.train_phrasings import MORE_STATEMENTS

DATA = Path(sys.argv[1])
LEFT_OUT = "news from my {relation} {person}: the whole house is {value} this year"
PATTERNS = []
for name, t in TRAIN.facts.items():
    PATTERNS.append((_statement_pattern(t.statement, TRAIN, t.values), name, "template"))
    for w in MORE_STATEMENTS.get(t.statement, ()):
        if w != LEFT_OUT:
            PATTERNS.append((_statement_pattern(w, TRAIN, t.values), name, "more"))
QUERIES = {name: t.query.replace("{who}", "").strip() for name, t in TRAIN.facts.items()}


def rows(name):
    return [json.loads(x) for x in (DATA / f"{name}.jsonl").read_text(encoding="utf-8").splitlines()]


def classify(line):
    for p, name, kind in PATTERNS:
        if p.fullmatch(line):
            return name, kind
    return None, "talk"


def parts(row):
    turns = row["turns"]
    calls = [i for i, t in enumerate(turns) if t["role"] == "assistant" and "tool_name" in t["content"]]
    c = max(calls)
    query = json.loads(turns[c]["content"])[0]["parameters"]["query"]
    asked = [n for n, q in QUERIES.items() if query.endswith(q)]
    return query, (asked[0] if len(asked) == 1 else None), turns[c + 1]["content"]


def tally(row):
    query, asked, out = parts(row)
    c = Counter()
    for line in re.findall(r"^User: (.*)$", out, re.M):
        name, kind = classify(line)
        if kind == "talk":
            c["talk"] += 1
        elif name == asked:
            c[f"asked_type_{kind}"] += 1
        else:
            c[f"other_type_{kind}"] += 1
    return c, asked


k1, k11 = rows("k1_r178"), rows("k1_1_r196")
agg = defaultdict(lambda: [Counter(), Counter()])
unknown = 0
for a, b in zip(k1, k11, strict=True):
    if a["kind"] not in ("older", "confirm", "never_told") or a["id"] != b["id"]:
        continue
    if a["id"].startswith("k1/"):
        continue
    side = "never_told" if a["kind"] == "never_told" else "found"
    ca, asked = tally(a)
    cb, _ = tally(b)
    unknown += asked is None
    agg[side][0].update(ca)
    agg[side][1].update(cb)
    agg[side][0]["rows"] += 1
    agg[side][1]["rows"] += 1
print("rows with no single asked type:", unknown)
for side, (ca, cb) in agg.items():
    n = ca["rows"]
    print(f"\n{side}: {n} rows with the same id (fresh rows left out)")
    keys = sorted(set(ca) | set(cb) - {"rows"})
    for k in keys:
        if k == "rows":
            continue
        print(f"  {k:24} K1 {ca[k]:5} ({ca[k]/n:.2f}/row)   K1.1 {cb[k]:5} ({cb[k]/n:.2f}/row)")
