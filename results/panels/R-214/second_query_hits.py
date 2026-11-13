"""R-214: how often a second query finds the fact when the first missed, by how it is formed.

Training chats only (K4.5's stripped K3 writer copies): older, check_true and check_false
questions whose first query's top 5 lacks the source message. Variants: the writer's second query;
the asked category's top telling words (``telling_words_r214.VOCAB``); the person's words plus
those; the first query plus those. A hit is the source message in the top 5.

Usage: python results/panels/R-214/second_query_hits.py
"""

import importlib.util
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

HERE = Path("scripts/records")
spec = importlib.util.spec_from_file_location("telling_words_r214", HERE / "telling_words_r214.py")
K46 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = K46
spec.loader.exec_module(K46)
K3 = K46.K45.load("build_k3")

hits, n = Counter(), 0
with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
    for path in sorted(Path("data/screens/k4_5/writers/k3").glob("*.json")):
        for c, chat in enumerate(json.loads(path.read_text(encoding="utf-8"))["chats"]):
            ex = [(m["user"], m["assistant"]) for m in chat["messages"]]
            tool = K3.build_search_tool(
                ex[: K3.IN_VIEW_FROM - 1], Path(tmp) / f"{path.stem}_{c}.sqlite", False
            )

            def found(query: str, source: str, tool=tool) -> bool:
                r = tool.execute(query)
                return bool(query.strip()) and r.success and source in r.output + "\n"

            for q in chat["questions"]:
                if q["kind"] not in ("older", "check_true", "check_false"):
                    continue
                source = f"User: {chat['messages'][q['source_message'] - 1]['user']}\n"
                if found(q["query"], source):
                    continue
                n += 1
                telling = " ".join(K46.VOCAB.get(q["category"], [])[:3])
                person = "" if q["person"] == "me" else " ".join(K46.words(q["person"])[:2])
                for name, query in (
                    ("writer second query", q["second_query"]),
                    ("telling words", telling),
                    ("person + telling", f"{person} {telling}"),
                    ("first + telling", f"{q['query']} {telling}"),
                    ("first + writer second", f"{q['query']} {q['second_query']}"),
                ):
                    hits[name] += found(query, source)
print(f"fact questions whose first query missed: {n}")
for name, h in hits.items():
    print(f"  {name}: {h} ({h / n:.0%})")
