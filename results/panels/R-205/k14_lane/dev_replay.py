"""Read-only: on the dev sets (outside writers 1 and 2, hard_dev, probe), replay the plain keyword
search with a question-word query (R-176 content words, possessive 's stripped) and compare with
what K1, K1.3 and base191 searched and found. No model runs.
"""

import importlib.util
import json
import re
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = Path.cwd()
spec = importlib.util.spec_from_file_location("r176", REPO / "scripts/records/demo_overlap_r176.py")
R176 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R176)

from aya_retrieval.conversations import rebuild_eval_item  # noqa: E402
from aya_retrieval.demonstrations import FILLER  # noqa: E402
from aya_retrieval.dev_set import load_dev_set  # noqa: E402
from aya_retrieval.recall_tool import build_search_tool, exchange_doc_id  # noqa: E402

INDEX = LANE / "idx3.sqlite"
EVAL = REPO / "results/recall_eval"


def qwords(message, stop):
    out = []
    for t in re.findall(r"[a-z']+", message.lower()):
        t2 = t.removesuffix("'s").removesuffix("’s")
        if t in stop or t2 in stop or not t2:
            continue
        if t2 not in out:
            out.append(t2)
    return " ".join(out)


def search(item, query):
    tool = build_search_tool(item.older(), INDEX, match_all=False)
    res = tool.backend.search(query, top_k=5) if query else []
    return [r["metadata"]["doc_id"] for r in res]


def runs(prefix, arm, seeds, seed_suffix):
    out = {}
    for s in seeds:
        name = f"{prefix}_{arm}_{s}_seed_{seed_suffix}.json" if s else f"{prefix}_{arm}_seed_{seed_suffix}.json"
        p = EVAL / name
        if p.exists():
            out[s] = {r["id"]: r for r in json.load(open(p, encoding="utf-8"))["rows"] if r["arm"] == "tool_loop"}
    return out


def main():
    sets = {}
    for name, folder in (("blind", "data/blind_dev/chats"), ("blind2", "data/blind_dev2/chats")):
        items = {i.item_id: i for i in load_dev_set(REPO / folder)[0]}
        sets[name] = (items, "0")
    for name, pool in (("hd", "hard_dev"), ("probe", "probe")):
        rows = json.load(open(EVAL / f"{name}_k1_3_r200_82_seed_73157.json", encoding="utf-8"))["rows"]
        items = {r["id"]: rebuild_eval_item(r, 73157, pool, 1) for r in rows if r["arm"] == "tool_loop"}
        sets[name] = (items, "73157")
    report = {}
    for name, (items, suf) in sets.items():
        arms = {a: runs(name, a, (82, 83, 94), suf) for a in ("k1_r178", "k1_3_r200")}
        arms["base191"] = runs(name, "base191", (None,), suf)
        per_kind = defaultdict(Counter)
        nt_pass = defaultdict(list)
        for iid, item in items.items():
            kind = item.kind
            if kind not in ("older", "confirm", "never_told"):
                continue
            for label, stop in (("r176", R176.STOP), ("filler", R176.STOP | FILLER)):
                q = qwords(item.message, stop)
                docs = search(item, q)
                if kind == "never_told":
                    nt_pass[label].append(len(docs))
                else:
                    per_kind[(kind, label)]["found"] += exchange_doc_id(item.fact_index) in docs
                    per_kind[(kind, label)]["n"] += 1
            for arm, by_seed in arms.items():
                for s, rows in by_seed.items():
                    r = rows.get(iid)
                    if r is None:
                        continue
                    if kind == "never_told":
                        nt_pass[f"{arm}"].append(sum(r.get("passages") or [0][:1]) if False else (r["passages"][0] if r.get("passages") else 0))
                    else:
                        c = per_kind[(kind, arm)]
                        c["n"] += 1
                        c["searched"] += bool(r.get("queries"))
                        c["found"] += bool(r.get("found_fact"))
                        c["right"] += bool(r["correct"])
        rep = {f"{k[0]}|{k[1]}": dict(v) for k, v in sorted(per_kind.items())}
        rep["never_told_passages"] = {k: (round(st.mean(v), 2), sum(x == 0 for x in v), len(v)) for k, v in nt_pass.items()}
        report[name] = rep
        print("==", name)
        for k, v in rep.items():
            print("  ", k, v)
    (LANE / "dev_replay.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    INDEX.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
