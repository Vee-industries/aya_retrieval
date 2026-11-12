import importlib.util, sys, re
from collections import Counter, defaultdict
spec = importlib.util.spec_from_file_location('c', 'scripts/records/check_r199.py'); m = importlib.util.module_from_spec(spec); sys.modules['c']=m; spec.loader.exec_module(m)
rows = m.R196.rows("k1_2_r199")
occ = defaultdict(Counter); kinds = {}
for row in rows:
    if row["kind"] not in m.NEEDS_SEARCH: continue
    q, out, reply = m.search_turns(row)
    side = "nt" if row["kind"] == m.NEVER_TOLD else "found"
    for line in re.findall(r"^User: (.*)$", out, re.M):
        got = m.match(line)
        if not got or not q.endswith(m.QUERIES[got[1]]): continue
        f = got[2].groupdict(); asked = m.has_word(q, f["person"]) or m.has_word(q, f["relation"])
        if asked: continue
        key = m.mapped(line); occ[side][key] += 1; kinds[key] = got[0]
for side, c in occ.items():
    d = len(c); dm = sum(kinds[k] == "more" for k in c)
    print(side, "occurrences", sum(c.values()), "distinct", d, "distinct drawn", f"{dm/d:.1%}", "max repeats", max(c.values()))
import build_r199 as b
from aya_retrieval.pools import TRAIN
name = {t.statement: n for n, t in TRAIN.facts.items()}
for side, c in occ.items():
    per = defaultdict(Counter)
    for k in c:
        per[name[m.match(k)[1]]][kinds[k]] += 1
    print(side, {n: f"{v['more']}/{sum(v.values())}" for n, v in sorted(per.items())})
# does the classification agree with the build's own draw?
bad = 0
for side, c in occ.items():
    for k in c:
        drawn = b.reworded(k); bad += (m.match(drawn)[0] == "more") != (drawn != k)
print("classification disagreements", bad)
for salt in ("R-199", "a", "b", "c", "d"):
    b.SALT = salt
    print(salt, {side: f"{sum(b.reworded(k) != k for k in c) / len(c):.1%}" for side, c in occ.items()})
