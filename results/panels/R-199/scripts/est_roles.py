"""Read-only: estimate K1.2's line 4/5 role shares from K1's and K1.1's existing sets."""
import re, sys, json
from collections import Counter
sys.argv = [sys.argv[0]]
import check_r199 as C
R = C.R196
k1, k11 = R.rows("k1_r178"), R.rows("k1_1_r196")
NT = C.NEVER_TOLD
lo = {"answer": Counter(), "found_decoy": Counter(), "never_told_decoy": Counter()}
hi = {k: Counter() for k in lo}
unknown = Counter()
for a, b in zip(k1, k11):
    if a["id"] != b["id"] or a["id"].startswith(C.FRESH) or a["kind"] not in C.NEEDS_SEARCH:
        continue
    q, out, reply = C.search_turns(a)
    _, out11, _ = C.search_turns(b)
    # every fact line K1.1 shows anywhere in this row, mapped to template -> kind
    seen = {}
    for line in R.fact_lines(b):
        g = R.wording(line)
        if g:
            seen[g[2]] = g[0]
    drawn_row = any(v == "more" for v in seen.values())
    for line in re.findall(r"^User: (.*)$", out, re.M):
        got = C.match(line)
        if not got or not q.endswith(C.QUERIES[got[1]]):
            continue
        role = "never_told_decoy" if a["kind"] == NT else ("answer" if got[2] in reply else "found_decoy")
        if line in seen:
            lo[role][seen[line]] += 1; hi[role][seen[line]] += 1
        else:
            unknown[(role, drawn_row)] += 1
            lo[role]["template"] += 1
            hi[role]["more" if drawn_row else "template"] += 1
for name, r in (("all unknown template", lo), ("unknown drawn if row has a drawn line", hi)):
    print(name)
    for k, c in r.items():
        n = sum(c.values()); print(f"  {k}: drawn {c['more']} of {n} ({c['more']/max(1,n):.1%})")
    print(f"  z answer vs found decoy {C.z(r['answer'], r['found_decoy']):.2f}; z found vs nt decoy {C.z(r['found_decoy'], r['never_told_decoy']):.2f}")
print("unknown (role, row has a drawn line):", dict(unknown))
