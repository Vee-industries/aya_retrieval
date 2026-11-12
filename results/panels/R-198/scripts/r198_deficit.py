"""Read-only: per row, K1.1's passage count against K1's, by kind and share, on rows with the same id."""
import json, sys
from collections import Counter
from pathlib import Path
DATA = Path(sys.argv[1])
def rows(n): return [json.loads(x) for x in (DATA/f"{n}.jsonl").read_text(encoding="utf-8").splitlines()]
def out(row):
    t=row["turns"]; c=max(i for i,x in enumerate(t) if x["role"]=="assistant" and "tool_name" in x["content"])
    return t[c+1]["content"].count("chunk_id="), t
k1, k11 = rows("k1_r178"), rows("k1_1_r196")
d = {"found": Counter(), "never_told": Counter()}
same_turns_but_view = Counter()
for a,b in zip(k1,k11,strict=True):
    if a["kind"] not in ("older","confirm","never_told") or a["id"]!=b["id"] or a["id"].startswith("k1/"): continue
    side = "never_told" if a["kind"]=="never_told" else "found"
    na,_=out(a); nb,_=out(b)
    d[side][max(-3,min(3,nb-na))]+=1
for s,c in d.items():
    n=sum(c.values())
    print(s, n, "K1.1 minus K1:", dict(sorted(c.items())), "short:", sum(v for k,v in c.items() if k<0))
# K1 count distribution
for name in ("k1_r178","k1_1_r196"):
    c={"found":Counter(),"never_told":Counter()}
    for r in rows(name):
        if r["kind"] in ("older","confirm","never_told"):
            c["never_told" if r["kind"]=="never_told" else "found"][out(r)[0]]+=1
    print(name, {k:dict(sorted(v.items())) for k,v in c.items()})
