"""Read-only: recompute the draft's evidence on K1.3's outside-writer older rows and test its cause.

Per not-found older row (seeds 82, 83, 94, sets blind and blind2): does the query hold a word in
neither question nor view (draft's count); is that word anywhere in the searchable chat; would the
question-word query have found the fact. Paired per item: K1.3 found vs question-word found.
Also: confirm questions, claim true / false / no value, searched, right.
Also: training never_told zero-passage rows by F2 share, and the shared_word link.
"""

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

LANE = Path(__file__).resolve().parent
REPO = Path.cwd()
spec = importlib.util.spec_from_file_location("dr", LANE / "dev_replay.py")
DR = importlib.util.module_from_spec(spec)
spec.loader.exec_module(DR)
from aya_retrieval.dev_set import load_dev_set  # noqa: E402
from aya_retrieval.recall_tool import exchange_doc_id  # noqa: E402

W = lambda s: set(re.findall(r"[a-z']+", s.lower()))  # noqa: E731


def main():
    tot = Counter()
    paired = Counter()
    confirm = Counter()
    for name, folder in (("blind", "data/blind_dev/chats"), ("blind2", "data/blind_dev2/chats")):
        items = {i.item_id: i for i in load_dev_set(REPO / folder)[0]}
        qw_found = {}
        for iid, it in items.items():
            if it.kind in ("older", "confirm"):
                qw_found[iid] = exchange_doc_id(it.fact_index) in DR.search(it, DR.qwords(it.message, DR.R176.STOP))
        for s in (82, 83, 94):
            rows = json.load(open(REPO / f"results/recall_eval/{name}_k1_3_r200_{s}_seed_0.json", encoding="utf-8"))["rows"]
            for r in rows:
                if r["arm"] != "tool_loop":
                    continue
                it = items[r["id"]]
                if r["kind"] == "older":
                    tot["older"] += 1
                    tot["older_right"] += bool(r["correct"])
                    paired[(bool(r.get("found_fact")), qw_found[r["id"]])] += 1
                    if r.get("queries") and not r.get("found_fact"):
                        tot["not_found"] += 1
                        qwords = set().union(*(W(q) for q in r["queries"]))
                        seen = W(r["message"]) | W(" ".join(a + " " + b for a, b in it.view()))
                        foreign = qwords - seen
                        older = W(" ".join(a + " " + b for a, b in it.older()))
                        fact = W(" ".join(it.exchanges[it.fact_index]))
                        if foreign:
                            tot["nf_with_foreign_word"] += 1
                            if foreign & older:
                                tot["nf_foreign_word_in_searchable_chat"] += 1
                            if foreign & fact:
                                tot["nf_foreign_word_in_fact_exchange"] += 1
                        tot["nf_qw_would_find"] += qw_found[r["id"]]
                        tot["nf_with_foreign_and_qw_would_find"] += bool(foreign) and qw_found[r["id"]]
                    if not r.get("queries"):
                        tot["older_no_search"] += 1
                if r["kind"] == "confirm":
                    msg = r["message"].casefold()
                    claim = "true" if it.answer.casefold() in msg else (
                        "false" if any(w.casefold() in msg for w in it.forbidden) else "no_value")
                    confirm[(claim, "n")] += 1
                    confirm[(claim, "searched")] += bool(r.get("queries"))
                    confirm[(claim, "found")] += bool(r.get("found_fact"))
                    confirm[(claim, "right")] += bool(r["correct"])
                    confirm[(claim, "qw_found")] += qw_found[r["id"]]
    print("older (both sets, 3 seeds):", dict(tot))
    print("paired older (K1.3 found, question-word found):", dict(paired))
    print("confirm by claim:", dict(sorted(confirm.items())))
    tails = Counter()
    for folder in ("data/blind_dev/chats", "data/blind_dev2/chats"):
        for it in load_dev_set(REPO / folder)[0]:
            if it.kind == "confirm":
                m = re.sub(r"[^a-z' ]", "", it.message.lower()).split()
                tails[" ".join(m[-2:])] += 1
    print("outside-writer confirm last two words:", tails.most_common(25))

    nq = json.loads((LANE / "new_queries.json").read_text(encoding="utf-8"))
    nt = [r for r in nq if r["kind"] == "never_told"]
    print("training never_told zero-passage rows by share:",
          dict(Counter(r["share"] for r in nt if r["new_n"] == 0)),
          "all never_told by share:", dict(Counter(r["share"] for r in nt)))
    print("training never_told zero-passage by message form sample:")
    for r in [r for r in nt if r["new_n"] == 0][:12]:
        print("   ", r["message"], "|", r["new_q"], "| old:", r["q_old"], r["old_n"])
    # shared_word: last ordinary word of old query; is it in the new query
    sw = [r for r in nq if r["share"] == "shared_word"]
    names = {"sister", "brother", "neighbour", "cousin", "coworker", "aunt", "uncle", "roommate"}
    keep = 0
    for r in sw:
        ordinary = [w for w in r["q_old"].split() if w.lower() not in names and not w.endswith("ed") and len(w) >= 3 and w[0].islower()]
        keep += bool(ordinary) and ordinary[-1] in r["new_q"].split()
    print("shared_word rows:", len(sw), "whose small-talk word is still in the new query:", keep)


if __name__ == "__main__":
    main()
