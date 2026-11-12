import importlib.util, json, re, sys
from collections import Counter
from pathlib import Path
here = Path("scripts/records")
spec = importlib.util.spec_from_file_location("build_r200", here / "build_r200.py")
m = importlib.util.module_from_spec(spec); sys.modules["build_r200"] = m; spec.loader.exec_module(m)
CHECK = m.CHECK
rows = [json.loads(l) for l in Path("data/screens/k1_r178.jsonl").read_text(encoding="utf-8").splitlines()]
twopat = 0; per_side = Counter(); dup_lines = Counter(); other_out = Counter(); turn_multi = 0; tool_mismatch = 0
for row in rows:
    pats = {}
    for t in row["turns"]:
        if CHECK.R196.tool_output(t) != t["content"].startswith("Tool result for"): tool_mismatch += 1
        for text, rep in m.texts(t):
            g = m.fact(text)
            if g: pats.setdefault(g[0], set()).add(g[1].re.pattern)
            # more than one fact in one text?
            n = sum(1 for p, _ in m.K12.PATTERNS for _x in p.finditer(text))
            if n > 1: turn_multi += 1
    twopat += any(len(v) > 1 for v in pats.values())
    if row["kind"] not in m.NEEDS_SEARCH: continue
    side = "never_told" if row["kind"] == m.NEVER_TOLD else "found"
    ro = m.roles(row)
    for k, r in ro.items(): per_side[(side, r)] += 1
    q, out, rep = CHECK.search_turns(row)
    seen = Counter()
    for line in re.findall(r"^User: (.*)$", out, re.M):
        f = m.fact(line)
        if f:
            seen[f[0]] += 1
            if f[0] not in ro: other_out[side] += 1
    for k, c in seen.items():
        if c > 1: dup_lines[(side, ro.get(k, "other"))] += c - 1
print("rows w/ key under two patterns", twopat, "texts with >1 fact", turn_multi, "tool_output mismatch", tool_mismatch)
print("per side role (row,fact)", dict(per_side)); print("duplicate output lines", dict(dup_lines)); print("returned lines role=other by side", dict(other_out))
print("kinds", Counter(r["kind"] for r in rows))
