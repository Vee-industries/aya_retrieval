"""Read-only: K1 rows that already hold drawn-wording fact lines (which the twin would map to template),
and whether build_r199.template_line agrees with check_r196.mapped on every fact line of K1 and K1.1."""
import re, sys, json
from collections import Counter
sys.argv = [sys.argv[0]]
import check_r196 as R
import build_r199 as B
k1, k11 = R.rows("k1_r178"), R.rows("k1_1_r196")
c = Counter(); outc = Counter(); ex = []
for row in k1:
    cls = row["id"].split("/")[0] if "/" in row["id"] else row["id"].split("_")[0]
    more = [l for l in R.fact_lines(row) if (g := R.wording(l)) and g[0] == "more"]
    if more:
        c[cls] += 1
        if len(ex) < 4: ex.append((row["id"], more[:2]))
    if row["kind"] in R.NEEDS_SEARCH:
        out = [t["content"] for t in row["turns"] if R.tool_output(t)]
        for o in out:
            for l in re.findall(r"^User: (.*)$", o, re.M):
                g = R.wording(l)
                if g and g[0] == "more":
                    outc[cls] += 1
print("K1 rows with a drawn-wording fact line, by class:", dict(c))
print("K1 drawn-wording lines in search outputs, by class:", dict(outc))
for e in ex: print(e)
# agreement between build mapping and check mapping, and identity on template lines
dis = Counter(); dex = []
for name, rows in (("k1", k1), ("k11", k11)):
    for row in rows:
        lines = list(R.fact_lines(row))
        for t in row["turns"]:
            if t["role"] == "user" and not R.tool_output(t):
                lines.append(t["content"])
        for l in lines:
            b, m = B.template_line(l), R.mapped(l)
            if b != m:
                dis[name] += 1
                if len(dex) < 5: dex.append((name, row["id"], l, b, m))
print("lines where build mapping != check mapping:", dict(dis))
for e in dex: print(e)
# ambiguity: a line fullmatched by more than one pattern (template or drawn) with different templates
amb = Counter(); aex = []
allp = [(p, t) for p, _u, t in R.TEMPLATES] + [(p, t) for p, _u, t in R.MORE]
for rows in (k1, k11):
    for row in rows:
        for l in R.fact_lines(row):
            ts = {t.format(**m.groupdict()) for p, t in allp if (m := p.fullmatch(l))}
            if len(ts) > 1:
                amb["lines"] += 1
                if len(aex) < 3: aex.append((l, ts))
print("ambiguous lines:", dict(amb), aex)
