"""R-267's reported lines (not gates) for one hard_dev result: searches per reply, false retrievals after a
second search, ran_out_of_calls. Usage: side_counts.py LABEL (e.g. hd_k13op4_r267_82)."""
import ast
import json
import sys
from collections import Counter

from aya_retrieval.conversations import rebuild_eval_item
from aya_retrieval.report_data import EVAL_DIR, eval_rows

label, seed = sys.argv[1], 73157
report = json.loads((EVAL_DIR / f"{label}_seed_{seed}.json").read_text(encoding="utf-8"))
c = Counter()
for row in eval_rows(label, seed, "tool_loop"):
    q = row["queries"]
    n = len(q if isinstance(q, list) else ast.literal_eval(q or "[]"))
    item = rebuild_eval_item(row, seed, report["pool"], report.get("decoys", 1))
    fr = any(v.casefold() in row["reply"].casefold() for v in item.forbidden)
    c["replies"] += 1
    c[f"searches {min(n, 2)}{'+' if n >= 2 else ''}"] += 1
    c["false retrieval"] += fr
    c["false retrieval after 2+ searches"] += fr and n >= 2
    c["ran_out_of_calls"] += str(row.get("ran_out_of_calls")) == "True"
print(label, dict(sorted(c.items())))
