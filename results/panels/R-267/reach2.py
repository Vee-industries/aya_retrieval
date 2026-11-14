"""Count: of OP seed 82's older misses whose own search missed, how many the item's second_query reaches."""
import json, sys, tempfile
from collections import Counter
from pathlib import Path
sys.argv = ["x"]
sys.path.insert(0, "scripts/records")
import importlib.util
spec = importlib.util.spec_from_file_location("b", "scripts/records/build_onpolicy_rows.py")
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
m = json.load(open("data/onpolicy/meta.json"))
d = json.load(open("results/recall_eval/op_op_82_seed_0.json"))
c = Counter()
with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
    for r in d["rows"]:
        if r["arm"] != "tool_loop" or r["kind"] != "older" or B.truthy(r["correct"]) or B.truthy(r["found_fact"]):
            continue
        q = m[r["id"]]
        who = "user" if (q["person"] or "me") == "me" else "other"
        chat = json.loads((B.ITEMS / f"{r['id'].rsplit('_q', 1)[0]}.json").read_text(encoding="utf-8"))
        ex = [tuple(e) for e in chat["exchanges"]]
        tool = B.build_search_tool(ex[: B.K3.IN_VIEW_FROM - 1], Path(tmp) / f"{r['id']}.sqlite", False)
        src = f"User: {ex[q['source_message'] - 1][0]}\n"
        sq = q.get("second_query") or ""
        val = set(B.K31.tokens(q["value"]))
        if not sq:
            c[(who, "no second_query")] += 1; continue
        if val & set(B.K31.tokens(sq)):
            c[(who, "second_query holds value word")] += 1; continue
        o = tool.execute(sq); out = o.output if o.success else ""
        first = B.cleaned(B.as_list(r["queries"]), q["question"])
        fo = ""
        if first:
            x = tool.execute(first[0]); fo = x.output if x.success else ""
        tag = "reached" if src in out + "\n" else "not reached"
        c[(who, tag, "first cut has text" if fo.strip() else "first cut empty/none")] += 1
for k, v in sorted(c.items()): print(k, v)
