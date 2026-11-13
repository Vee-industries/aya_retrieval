"""Read-only: K1.4's question-word query (draft rule) on every rebuilt K1 search row.

For each search row: old query (K1's), new query (who + R-176 content words of the message, who
removed, in order), top-5 over the row's template-wording chat; found / passages / which roles.
Writes new_queries.json and prints a summary.
"""

import importlib.util
import json
import pickle
import re
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = Path.cwd()


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


R176 = load("r176", REPO / "scripts/records/demo_overlap_r176.py")
from aya_retrieval.conversations import NEVER_TOLD, NEEDS_SEARCH  # noqa: E402
from aya_retrieval.demonstrations import FILLER  # noqa: E402
from aya_retrieval.pools import TRAIN  # noqa: E402
from aya_retrieval.recall_tool import build_recall_tool, exchange_doc_id  # noqa: E402

INDEX = LANE / "idx2.sqlite"
SUFFIX = {t.query.replace("{who}", "").strip(): n for n, t in TRAIN.facts.items()}
NAMES = {w.casefold() for w in (*TRAIN.people, *TRAIN.relations)}


def tokens(text):
    return re.findall(r"[a-z']+", text.lower())


def who_of(query):
    for suf in sorted(SUFFIX, key=len, reverse=True):
        if query.endswith(suf):
            return query[: -len(suf)].strip(), suf
    return None, None


def draft_query(message, who, stop=R176.STOP):
    rest = []
    for t in tokens(message):
        t2 = t.removesuffix("'s")
        if t in stop or t2 in stop or t2 == who.lower() or t == who.lower():
            continue
        if t2 and t2 not in rest:
            rest.append(t2)
    return " ".join([who, *rest]), rest


def run(item, query):
    tool = build_recall_tool(item, INDEX, match_all=False)
    res = tool.backend.search(query, top_k=5)
    docs = [r.metadata["doc_id"] if hasattr(r, "metadata") else r["metadata"]["doc_id"] for r in res]
    return docs, res


def main():
    data = pickle.load(open(LANE / "k1_items.pkl", "rb"))
    items, share = data["items"], data["share"]
    k1 = [json.loads(l) for l in (REPO / "data/screens/k1_r178.jsonl").read_text(encoding="utf-8").splitlines()]
    out = []
    for row in k1:
        if row["kind"] not in NEEDS_SEARCH or row["id"] not in items:
            continue
        item = items[row["id"]]
        q_old = json.loads(row["turns"][-3]["content"])[0]["parameters"]["query"]
        who, suf = who_of(q_old)
        rec = {"id": row["id"], "kind": row["kind"], "q_old": q_old, "who": who,
               "share": share.get(row["id"]), "message": item.message}
        if who is None:
            rec["no_template_query"] = True
            out.append(rec)
            continue
        q_new, rest = draft_query(item.message, who)
        q_fill, _ = draft_query(item.message, who, stop=FILLER | R176.STOP)
        fact_doc = exchange_doc_id(item.fact_index)
        older = item.older()
        older_words = set(re.findall(r"[a-z']+", " ".join(u + " " + a for u, a in older).lower()))
        for label, q in (("old", q_old), ("new", q_new), ("fill", q_fill)):
            docs, res = run(item, q)
            rec[f"{label}_q"] = q
            rec[f"{label}_n"] = len(docs)
            rec[f"{label}_found"] = row["kind"] != NEVER_TOLD and fact_doc in docs
            rec[f"{label}_rank"] = docs.index(fact_doc) if rec[f"{label}_found"] else None
            rec[f"{label}_docs"] = docs
        # words of the new query (besides who) present in the fact exchange / anywhere older
        if row["kind"] != NEVER_TOLD:
            fu, fa = item.exchanges[item.fact_index]
            fw = set(re.findall(r"[a-z']+", (fu + " " + fa).lower()))
            rec["rest_in_fact"] = [w for w in rest if w in fw]
        rec["rest_in_chat"] = [w for w in rest if w in older_words]
        rec["rest"] = rest
        rec["qlen_old"] = len(q_old.split())
        rec["qlen_new"] = len(q_new.split())
        # does the new query still end with the template suffix (check_r199/build_r200 roles())
        rec["new_ends_with_template"] = q_new.endswith(suf)
        out.append(rec)
    (LANE / "new_queries.json").write_text(json.dumps(out, indent=0), encoding="utf-8")
    INDEX.unlink(missing_ok=True)

    recs = [r for r in out if not r.get("no_template_query")]
    print("search rows rebuilt", len(out), "with template query", len(recs),
          "without", sum(1 for r in out if r.get("no_template_query")))
    found_side = [r for r in recs if r["kind"] != NEVER_TOLD]
    nt = [r for r in recs if r["kind"] == NEVER_TOLD]
    for label in ("old", "new", "fill"):
        f = sum(r[f"{label}_found"] for r in found_side)
        by_kind = Counter((r["kind"], r[f"{label}_found"]) for r in found_side)
        print(f"{label}: found {f} of {len(found_side)}; by kind {dict(by_kind)}")
        fn = [r[f"{label}_n"] for r in found_side]
        tn = [r[f"{label}_n"] for r in nt]
        print(f"  passages found-side mean {st.mean(fn):.2f}, never_told mean {st.mean(tn):.2f}, gap "
              f"{st.mean(fn) - st.mean(tn):.2f}; never_told with 0 passages {sum(n == 0 for n in tn)} of {len(tn)}")
        print(f"  passage-count dist found {sorted(Counter(fn).items())} nt {sorted(Counter(tn).items())}")
        fr = [r[f"{label}_n"] for r in found_side if r[f"{label}_found"]]
        nf = [r[f"{label}_n"] for r in found_side if not r[f"{label}_found"]]
        if fr and nf:
            print(f"  among found-side: found rows mean {st.mean(fr):.2f} (n {len(fr)}), not-found mean {st.mean(nf):.2f} (n {len(nf)})")
        ranks = Counter(r[f"{label}_rank"] for r in found_side if r[f"{label}_found"])
        print(f"  rank of fact when found {sorted(ranks.items())}")
    print("query length old: found", st.mean(r["qlen_old"] for r in found_side), "nt", st.mean(r["qlen_old"] for r in nt))
    print("query length new: found", round(st.mean(r["qlen_new"] for r in found_side), 2), "nt", round(st.mean(r["qlen_new"] for r in nt), 2))
    print("qlen new dist found", sorted(Counter(r["qlen_new"] for r in found_side).items()))
    print("qlen new dist nt   ", sorted(Counter(r["qlen_new"] for r in nt).items()))
    print("new query that is who alone:", sum(r["qlen_new"] == 1 for r in recs))
    print("rows whose new query has a rest word in the fact line:",
          sum(bool(r["rest_in_fact"]) for r in found_side), "of", len(found_side))
    print("found (new) with no rest word in the fact line (found by who alone):",
          sum(r["new_found"] and not r["rest_in_fact"] for r in found_side))
    print("rows whose rest words appear nowhere in older chat:", sum(not r["rest_in_chat"] for r in recs), "of", len(recs))
    print("new query ends with template suffix:", sum(r["new_ends_with_template"] for r in recs), "of", len(recs))
    words = Counter(w for r in recs for w in r["rest"])
    print("most common rest words:", words.most_common(40))
    by_share = defaultdict(Counter)
    for r in found_side:
        by_share[r["share"]][r["new_found"]] += 1
    print("new found by F2 share:", {k: dict(v) for k, v in by_share.items()})
    print("not found by message form (first 25):")
    for r in [r for r in found_side if not r["new_found"]][:25]:
        print("   ", r["kind"], "|", r["message"], "|", r["new_q"], "| old:", r["q_old"])


if __name__ == "__main__":
    main()
