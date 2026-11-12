import sys, json, re
from collections import Counter
sys.path[:0]=["scripts/records"]
import build_r199 as b
rows=[json.loads(l) for l in open("data/screens/k1_r178.jsonl",encoding="utf-8")]
partial=Counter(); ex={}
asst=Counter(); exa={}
for r in rows:
    for i,t in enumerate(r["turns"]):
        c=t["content"]
        if c.startswith("Tool result for"):
            segs=[("tool-User",m) for m in re.findall(r"^User: (.*)$",c,re.M)]
            # any other lines in tool output containing a fact?
            other=[l for l in c.split("\n") if not l.startswith("User: ")]
            segs+=[("tool-other",l) for l in other]
        elif t["role"]=="user": segs=[("user",c)]
        else: segs=[("assistant",c)]
        for where,s in segs:
            for p,st in b.PATTERNS:
                if p.search(s) and not p.fullmatch(s):
                    partial[(where,r["id"].split("/")[0].split("_")[0])]+=1; ex.setdefault(where,[]).append((r["id"],s[:200]))
                    break
                if where=="assistant" and p.fullmatch(s):
                    asst["full"]+=1
print(partial); print(asst)
for k,v in ex.items():
    print(k,len(v))
    for e in v[:6]: print("  ",e)
