import collections
import json
import re
import sys

rel = ("sister", "brother", "neighbour", "cousin", "coworker", "aunt", "uncle", "roommate")
pat = re.compile(r'"query"\s*:\s*"([^"]+)"')
qs = []
selfrows = 0
n = 0
for line in open(sys.argv[1], encoding="utf-8"):
    n += 1
    row = json.loads(line)
    text = json.dumps(row, ensure_ascii=False)
    # tool-call arguments may be nested JSON strings; unescape once
    flat = text.replace('\\"', '"')
    qs += pat.findall(flat)
    if re.search(r'"content":\s*"i (fixed|bought|started|finally)', flat):
        selfrows += 1
print("rows", n, "queries", len(qs), "distinct", len(set(qs)))
norel = [q for q in qs if not any(r in q.lower() for r in rel)]
print("queries without a relation word", len(norel), collections.Counter(norel).most_common(8))
print("rows with a user line starting 'i fixed/bought/started/finally'", selfrows)
print(collections.Counter(q.split()[0] for q in qs).most_common(10))
people = ("Dana", "Marc", "Priya", "Tomas", "Lena", "Omar", "Greta", "Yusuf", "Nell", "Ivan")
rest = [q for q in norel if not any(p in q for p in people)]
print("queries with neither a relation word nor a TRAIN name", len(rest), rest[:10])
