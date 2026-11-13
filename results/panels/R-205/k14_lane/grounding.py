"""Read-only: does K1's reply stay grounded in the new query's top 5 (values it names present)?
Also: asked-type same-type lines returned per row, old vs new, found vs never_told."""
import json, pickle, re
from collections import Counter
from pathlib import Path
LANE = Path(__file__).resolve().parent
from aya_retrieval.demonstrations import values_named
from aya_retrieval.pools import TRAIN
items = pickle.load(open(LANE / "k1_items.pkl", "rb"))["items"]
nq = {r["id"]: r for r in json.loads((LANE / "new_queries.json").read_text(encoding="utf-8"))}
rows = {json.loads(l)["id"]: json.loads(l) for l in open("data/screens/k1_r178.jsonl", encoding="utf-8")}
c = Counter()
same = {"old": Counter(), "new": Counter()}
for rid, r in nq.items():
    it = items[rid]; row = rows[rid]
    reply = row["turns"][-1]["content"]
    own = next(n for n, t in TRAIN.facts.items() if it.decoy in t.values)
    vals = set(TRAIN.facts[own].values)
    for lab in ("old", "new"):
        idx = [int(d.split("_")[1]) for d in r[f"{lab}_docs"]]
        text = " ".join(" ".join(it.exchanges[i]) for i in idx)
        side = "nt" if r["kind"] == "never_told" else "found"
        n_same = sum(any(v in it.exchanges[i][0] for v in vals) for i in idx)
        same[lab][(side, n_same)] += 1
        if side == "found":
            named = values_named(reply, "train")
            ok = all(v.casefold() in text.casefold() for v in named)
            c[(lab, row["id"].split("_")[0], ok)] += 1
print(sorted(c.items()))
for lab in same:
    print(lab, sorted(same[lab].items()))
