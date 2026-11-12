import sys, json, re, itertools
from collections import Counter
sys.path[:0]=["scripts/records"]
import build_r199 as b, check_r199 as c
from aya_retrieval.pools import TRAIN
# 1. mapping round trip on every possible template line
bad=Counter(); n=0
for t in TRAIN.facts.values():
    for rel,per,val in itertools.product(TRAIN.relations,TRAIN.people,t.values):
        line=t.statement.format(relation=rel,person=per,value=val); n+=1
        for w in (t.statement,*b.WORDINGS.get(t.statement,())):
            dl=w.format(relation=rel,person=per,value=val)
            got=c.match(dl)
            if not got or got[1]!=t.statement or got[2]!={"relation":rel,"person":per,"value":val}:
                bad[(t.statement[:30],w[:40])]+=1
        r=b.reworded(line)
        if c.R196.mapped(r)!=line: bad["roundtrip"]+=1
print("template lines",n,"bad",dict(list(bad.items())[:10]), sum(bad.values()))
# 2. K1: lines already in MORE wording or LEFT_OUT
rows=[json.loads(l) for l in open("data/screens/k1_r178.jsonl",encoding="utf-8")]
more=Counter()
for r in rows:
    for l in c.R196.fact_lines(r):
        g=c.match(l)
        if g and g[0]=="more": more[r["id"].split("_")[0]]+=1
print("K1 lines already in MORE wording", dict(more))
# 3. search rows whose query matches no template query, by kind
from aya_retrieval.conversations import NEEDS_SEARCH, NEVER_TOLD
qc=Counter()
for r in rows:
    if r["kind"] not in NEEDS_SEARCH: continue
    q,out,rep=c.search_turns(r)
    ok=any(q.endswith(v) for v in c.QUERIES.values())
    qc[(r["kind"],ok)]+=1
print(sorted(qc.items()))
