"""Read-only best estimate of K1.2's returned same-type lines: K1's returned lines, each in K1.1's
wording where K1.1 shows it; unseen lines template in template-only rows (R-102 ids corr/corrcue/asked,
spliced indirect/), drawn elsewhere (R-198: lost lines are drawn decoys)."""
import re, sys
from collections import Counter
sys.argv = [sys.argv[0]]
import check_r199 as C
R = C.R196
k1, k11 = R.rows("k1_r178"), R.rows("k1_1_r196")
TONLY = ("corr_", "corrcue_", "asked_", "indirect/")
roles = {"answer": Counter(), "found_decoy": Counter(), "never_told_decoy": Counter()}
alltemp = Counter(); rowsn = Counter(); bysrc = Counter()
for a, b in zip(k1, k11):
    if a["id"].startswith(C.FRESH) or a["kind"] not in C.NEEDS_SEARCH:
        continue
    q, out, reply = C.search_turns(a)
    seen = {g[2]: g[0] for l in R.fact_lines(b) if (g := R.wording(l))}
    tonly = a["id"].startswith(TONLY)
    kinds = []
    for line in re.findall(r"^User: (.*)$", out, re.M):
        got = C.match(line)
        if not got or not q.endswith(C.QUERIES[got[1]]):
            continue
        k = seen.get(line, "template" if tonly else "more")
        role = "never_told_decoy" if a["kind"] == C.NEVER_TOLD else ("answer" if got[2] in reply else "found_decoy")
        roles[role][k] += 1
        bysrc[(role, "template-only row" if tonly else "drawable row", k)] += 1
        kinds.append(k)
    side = "never_told" if a["kind"] == C.NEVER_TOLD else "found"
    if kinds:
        rowsn[side] += 1
        alltemp[side] += all(k == "template" for k in kinds)
for k, c in roles.items():
    n = sum(c.values()); print(f"{k}: drawn {c['more']} of {n} ({c['more']/max(1,n):.1%})")
print(f"z line 4 {C.z(roles['answer'], roles['found_decoy']):.2f}; z line 5 {C.z(roles['found_decoy'], roles['never_told_decoy']):.2f}")
print("rows with same-type lines returned, all of them template:", {s: f"{alltemp[s]} of {rowsn[s]}" for s in rowsn})
for k in sorted(bysrc): print(" ", k, bysrc[k])
