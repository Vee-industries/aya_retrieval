"""Read-only: over the 64 K3 chats, for every fact in messages 1-21, would a near-miss query that
holds the person's reference return the person's stored fact (top 5, OR)? Person reference = the
fact's `person` as written (lower case); 'me' has none. Also K3.2's natural rows by kind/reply."""
import json, re
from collections import Counter
from pathlib import Path
from aya_retrieval.recall_tool import build_search_tool, exchange_doc_id
LANE = Path(__file__).resolve().parent
IDX = LANE / "idx.sqlite"
c = Counter()
cats = Counter()
for p in sorted(Path("data/screens/k3_writers").glob("*.json")):
    for chat in json.loads(p.read_text(encoding="utf-8"))["chats"]:
        msgs = chat["messages"]
        ex = [(m["user"], m["assistant"]) for m in msgs]
        tool = build_search_tool(ex[:21], IDX, match_all=False)
        per_person = Counter((m.get("fact") or {}).get("person", "").lower() for m in msgs[:21] if m.get("fact"))
        for i, m in enumerate(msgs[:21]):
            f = m.get("fact")
            if not f:
                continue
            who = f["person"].lower()
            cats[f["category"]] += 1
            if who == "me":
                c["me"] += 1
                continue
            c["named"] += 1
            words = re.findall(r"[a-z']+", who)
            in_line = all(w in m["user"].lower() for w in words)
            c["named_ref_in_fact_line"] += in_line
            res = tool.backend.search(" ".join(words), top_k=5)
            docs = [r["metadata"]["doc_id"] for r in res]
            hit = exchange_doc_id(i) in docs
            c["named_ref_query_returns_fact"] += hit
            c["person_has_2plus_facts"] += per_person[who] >= 2
            n_lines = sum(all(w in u.lower() for w in words) for u, _ in ex[:21])
            c["named_ref_in_over5_lines"] += n_lines > 5
IDX.unlink(missing_ok=True)
print(dict(c))
print("categories of stored facts (top):", cats.most_common(12))
rows = [json.loads(l) for l in open("data/screens/k3_2_r207.jsonl", encoding="utf-8")]
nat = [r for r in rows if r["id"].startswith("k3_")]
print("K3.2 natural rows:", len(nat), Counter(r["kind"] for r in nat))
