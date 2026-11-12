import sys, json
from collections import Counter
sys.path[:0]=["scripts/records"]
import build_r199 as b, check_r199 as c
from aya_retrieval.pools import TRAIN
rows=[json.loads(l) for l in open("data/screens/k1_r178.jsonl",encoding="utf-8")]
G=[(t.statement,c.R196.grams(t.statement)) for t in TRAIN.facts.values()]
hit=Counter(); ex=[]
for r in rows:
    for i,t in enumerate(r["turns"]):
        if t["role"]!="assistant" or t["content"].startswith("[{"): continue
        rg=c.R196.grams(t["content"])
        for s,g in G:
            if g & rg:
                hit[(r["kind"], i==len(r["turns"])-1)]+=1
                if len(ex)<4: ex.append((r["id"],t["content"]))
                break
print(dict(hit)); print(ex)
