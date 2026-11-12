"""Read-only: how many found rows in K1 have no returned same-type line whose value is in the reply,
and how many have two or more."""
import re, sys, json
from collections import Counter
sys.argv = [sys.argv[0]]
import check_r199 as C
R = C.R196
k1 = R.rows("k1_r178")
c = Counter(); ex = []
for row in k1:
    if row["kind"] not in C.NEEDS_SEARCH or row["kind"] == C.NEVER_TOLD:
        continue
    q, out, reply = C.search_turns(row)
    n = 0; same = 0
    for line in re.findall(r"^User: (.*)$", out, re.M):
        got = C.match(line)
        if not got or not q.endswith(C.QUERIES[got[1]]):
            continue
        same += 1
        n += got[2] in reply
    c[(row["kind"], n)] += 1
    if n != 1 and len(ex) < 6:
        ex.append((row["id"], row["kind"], row["turns"][6]["content"], q, reply, out[:300]))
print(sorted(c.items()))
for e in ex: print(e, "\n")
