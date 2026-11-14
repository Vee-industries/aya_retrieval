"""OP4 pool counts on OP seed 82's item eval (the lane's shapes): answer = older wrong, first cut search output
without the source, second_query output with it; decline = trap, first cut output without the trap value, second
output with it. Also: second_query words found in the source message but not in the question."""
import json, tempfile, importlib.util
from collections import Counter
from pathlib import Path
spec = importlib.util.spec_from_file_location("b", "scripts/records/build_onpolicy_rows.py")
B = importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
m = json.load(open("data/onpolicy/meta.json"))
d = json.load(open("results/recall_eval/op_op_82_seed_0.json"))
c, w = Counter(), Counter()
with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
    for r in d["rows"]:
        if r["arm"] != "tool_loop" or B.truthy(r["correct"]) and r["kind"] == "older":
            continue
        q = m[r["id"]]
        who = "user" if (q.get("person") or "me") == "me" else "other"
        chat = json.loads((B.ITEMS / f"{r['id'].rsplit('_q', 1)[0]}.json").read_text(encoding="utf-8"))
        ex = [tuple(e) for e in chat["exchanges"]]
        first = B.cleaned(B.as_list(r["queries"]), q["question"])
        if not first:
            c[(r["kind"] == "older" and "answer" or "decline", who, "no first call")] += 1; continue
        tool = B.build_search_tool(ex[: B.K3.IN_VIEW_FROM - 1], Path(tmp) / f"{r['id']}.sqlite", False)
        run = lambda x: (o.output if (o := tool.execute(x)).success else "")
        f1, f2 = run(first[0]), run(q["second_query"])
        if r["kind"] == "older":
            src = f"User: {ex[q['source_message'] - 1][0]}\n"
            ok = src not in f1 + "\n" and src in f2 + "\n"
            c[("answer", who, "ok" if ok else "no")] += 1
            if ok:
                sw, qw, srcw = set(B.K31.tokens(q["second_query"])), set(B.K31.tokens(q["question"])), set(B.K31.tokens(ex[q['source_message'] - 1][0]))
                hit = sw & srcw
                w["answer ok rows"] += 1
                w["second_query words in source"] += len(hit)
                w["  of which also in question"] += len(hit & qw)
                w["rows whose only source-matching words are absent from the question"] += bool(hit) and not (hit & qw)
        else:
            trap = chat["questions"][int(r["id"].rsplit("_q", 1)[1])]["wrong"][0].casefold()
            ok = trap not in f1.casefold() and trap in f2.casefold()
            c[("decline", who, "correct" if B.truthy(r["correct"]) else "wrong", "ok" if ok else "no")] += 1
for k, v in sorted(c.items()): print(k, v)
for k, v in w.items(): print(k, v)
