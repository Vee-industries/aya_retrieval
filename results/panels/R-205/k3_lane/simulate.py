"""Read-only simulation of K3's natural rows on the outside-writer dev chats, and the same cues in
K1.3's rows. No model.

Query rule (the brief's): question words only, the brief's filler list and R-176's stop words
removed, at most 4 words, in question order. Search: build_search_tool over the chat's older
exchanges (OR, top 5), as build_k3 does. Kept as build_k3 keeps: fact rows only if the source
exchange is returned, never_told only with at least one passage.

Reports per side: kept share, passages, top score, score gap first-second, rank of source,
whether a returned passage holds the question's value word (check forms), and K1.3's same numbers.
Also K1.3's outcome on outside-writer rows whose search missed the fact (decline or a value).
"""

import importlib.util
import json
import re
import statistics as st
from collections import Counter, defaultdict
from pathlib import Path

LANE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r176", "scripts/records/demo_overlap_r176.py")
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)
from aya_retrieval.dev_set import load_dev_set  # noqa: E402
from aya_retrieval.recall_tool import build_search_tool, exchange_doc_id  # noqa: E402

BRIEF_FILLER = set("say tell told mention remember again know think what where which who does did is".split())
STOP = R.STOP | BRIEF_FILLER
INDEX = LANE / "idx.sqlite"
DECL = re.compile(r"don't|do not|not sure|guess|no idea|haven't|not told|didn't|can't|what is it|don't see", re.I)


def query(message):
    out = []
    for t in re.findall(r"[a-z']+", message.lower()):
        t2 = t.removesuffix("'s")
        if t in STOP or t2 in STOP or not t2 or t2 in out:
            continue
        out.append(t2)
    return " ".join(out[:4])


def run(exchanges, q):
    tool = build_search_tool(exchanges, INDEX, match_all=False)
    res = tool.backend.search(q, top_k=5) if q else []
    return [(r["metadata"]["doc_id"], r["score"]) for r in res]


def summarize(label, recs):
    if not recs:
        return
    n = [r["n"] for r in recs]
    top = [r["top"] for r in recs if r["n"]]
    gap = [r["gap"] for r in recs if r["n"] >= 2]
    print(f"  {label}: rows {len(recs)}, passages mean {st.mean(n):.2f} dist {sorted(Counter(n).items())}, "
          f"top score mean {st.mean(top):.2f} median {st.median(top):.2f}, "
          f"top-minus-second mean {st.mean(gap) if gap else 0:.2f}")


def main():
    kept = defaultdict(list)
    tally = Counter()
    for folder in ("data/blind_dev/chats", "data/blind_dev2/chats"):
        for it in load_dev_set(Path(folder))[0]:
            if it.kind not in ("older", "confirm", "never_told"):
                continue
            q = query(it.message)
            hits = run(it.older(), q)
            docs = [d for d, _ in hits]
            scores = [s for _, s in hits]
            rec = {"n": len(hits), "top": scores[0] if scores else 0,
                   "gap": scores[0] - scores[1] if len(scores) > 1 else 0, "qlen": len(q.split())}
            if it.kind == "never_told":
                tally["nt"] += 1
                if hits:
                    kept["never_told"].append(rec)
                    tally["nt_kept"] += 1
                continue
            src = exchange_doc_id(it.fact_index)
            tally[it.kind] += 1
            if src in docs:
                tally[f"{it.kind}_kept"] += 1
                rec["rank"] = docs.index(src)
                kept[it.kind].append(rec)
                tally[f"{it.kind}_src_top"] += docs.index(src) == 0
                if it.kind == "confirm":
                    claim_true = it.answer.casefold() in it.message.casefold()
                    tally["confirm_true_kept" if claim_true else "confirm_other_kept"] += 1
            else:
                tally[f"{it.kind}_dropped"] += 1
                ov = R.words(it.message) & R.words(it.exchanges[it.fact_index][0])
                tally[f"{it.kind}_dropped_overlap0"] += not ov
    print("outside-writer dev chats, brief's query rule:", dict(tally))
    for k, v in kept.items():
        summarize(k, v)
    fact = kept["older"] + kept["confirm"]
    summarize("fact rows kept (older+confirm)", fact)
    print("  found-side gap in passages:", round(st.mean(r["n"] for r in fact) - st.mean(r["n"] for r in kept["never_told"]), 2))

    # K1.3's own rows: passages and top score by side
    side = defaultdict(list)
    for line in open("data/screens/k1_3_r200.jsonl", encoding="utf-8"):
        row = json.loads(line)
        if row["kind"] not in ("older", "confirm", "never_told"):
            continue
        out = row["turns"][-2]["content"]
        sc = [float(x) for x in re.findall(r"score=([0-9.]+)\]", out)]
        side["never_told" if row["kind"] == "never_told" else "fact"].append(
            {"n": len(sc), "top": sc[0] if sc else 0, "gap": sc[0] - sc[1] if len(sc) > 1 else 0})
    print("K1.3 rows:")
    for k, v in side.items():
        summarize(k, v)

    # K1.3 on outside writers: what it says when its search missed the fact
    miss = Counter()
    for name in ("blind", "blind2"):
        for s in (82, 83, 94):
            for r in json.load(open(f"results/recall_eval/{name}_k1_3_r200_{s}_seed_0.json", encoding="utf-8"))["rows"]:
                if r["arm"] != "tool_loop" or r["kind"] not in ("older", "confirm"):
                    continue
                if r.get("queries") and not r.get("found_fact"):
                    miss[(r["kind"], "declined" if DECL.search(r["reply"]) else "names_something")] += 1
    print("K1.3 outside-writer searches that missed the fact, reply:", dict(miss))
    INDEX.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
