"""Read-only, K1.1's existing set: wording of returned same-type lines, answer line against decoys."""
import json, re, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util
spec = importlib.util.spec_from_file_location("mech", Path(__file__).parent / "r198_mech.py")
DATA = Path(sys.argv[1])
from aya_retrieval.pools import TRAIN
WORDS = tuple(w.casefold() for w in (*TRAIN.people, *TRAIN.relations))
def words_in(t):
    t = t.casefold(); return {w for w in WORDS if re.search(rf"\b{re.escape(w)}\b", t)}
src = (Path(__file__).parent / "r198_mech.py").read_text()
head = src.split("k1, k11 = rows")[0]
ns = {"__file__": "x"}; sys.argv = [sys.argv[0], str(DATA)]
exec(head, ns)
for name in ("k1_r178", "k1_1_r196"):
    c = Counter()
    for row in ns["rows"](name):
        if row["kind"] not in ("older", "confirm", "never_told"): continue
        side = "nt" if row["kind"] == "never_told" else "found"
        t = row["turns"]; call = max(i for i,x in enumerate(t) if x["role"]=="assistant" and "tool_name" in x["content"])
        q = words_in(t[call-1]["content"])
        query, asked, out = ns["parts"](row)
        for line in re.findall(r"^User: (.*)$", out, re.M):
            n, k = ns["classify"](line)
            if k == "talk": continue
            who = "asked_who" if words_in(line) & q else "other_who"
            typ = "same_type" if n == asked else "other_type"
            c[(side, typ, who, k)] += 1
    print(name)
    for key in sorted(c): print("  ", key, c[key])
