import sys, json, re
from collections import Counter
sys.path[:0]=["scripts/records"]
import build_r199 as b, check_r199 as c
from aya_retrieval.pools import TRAIN
rows=[json.loads(l) for l in open("data/screens/k1_r178.jsonl",encoding="utf-8")]
print(Counter((r["id"].split("_")[0].split("/")[0], r["kind"]) for r in rows))
corr=[r for r in rows if r["id"].startswith("corr")]
r=corr[0]
for t in r["turns"][-3:]: print(t["role"], t["content"][:900]); print('---')
# replies quoting template fixed words: found rows, last reply contains a 4-gram of the asked template's fixed text
def fixed_grams(s):
    return c.R196.grams(s)
q2t={v:t for t in TRAIN.facts.values() for v in [t.query.replace("{who}","").strip()]}
hit=Counter()
for r in rows:
    if r["kind"] not in ("older","confirm"): continue
    q,out,rep=c.search_turns(r)
    t=[t for v,t in q2t.items() if q.endswith(v)]
    if not t: continue
    g=fixed_grams(t[0].statement)
    rg=c.R196.grams(rep)
    hit[bool(g & rg)]+=1
print("found-side replies sharing a 4-gram with the template's fixed words:",dict(hit))
