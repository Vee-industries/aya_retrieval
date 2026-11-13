import json
from collections import Counter


def queries(row):
    out = []
    for t in row["turns"]:
        if t["role"] == "assistant" and '"tool_name"' in t["content"]:
            try:
                calls = json.loads(t["content"])
                out += [c["parameters"]["query"] for c in calls]
            except Exception:
                out.append("?")
    return out


for name in ("k1_3_r200", "k4_1_r209", "k4_4_r212"):
    c = Counter()
    for line in open(f"data/screens/{name}.jsonl", encoding="utf-8"):
        r = json.loads(line)
        nat = r["id"].startswith("k3_")
        for q in queries(r):
            c[("natural" if nat else "template", "'" in q)] += 1
    print(name, dict(c))

for who in ("k1_3_r200", "k4_1_r209"):
    c = Counter()
    for pre in ("hd", "probe"):
        for s in (82, 83, 94):
            path = f"results/recall_eval/{pre}_{who}_{s}_seed_73157.json"
            for r in json.load(open(path, encoding="utf-8"))["rows"]:
                for q, n in zip(r.get("queries") or [], r.get("passages") or []):
                    c[("apostrophe" if "'" in q else "plain", "empty" if n == 0 else "hit")] += 1
    print(who, dict(sorted(c.items())))
