"""Read-only: Demo2 under the brief's query rule; K1.3's ack cue; value recurrence across the two
outside-writer sets (a stand-in for training-to-S3 overlap); the brief's example words in dev sets."""

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path

LANE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sim", LANE / "simulate.py")
SIM = importlib.util.module_from_spec(spec)
spec.loader.exec_module(SIM)
spec2 = importlib.util.spec_from_file_location("c199", "scripts/records/check_r199.py")
from aya_retrieval.dev_set import load_dev_set  # noqa: E402
from aya_retrieval.recall_tool import exchange_doc_id  # noqa: E402


def main():
    # Demo2: user lines with the arm-free assistant replies from branches.json prefix (K1's prefix)
    qs = json.loads(Path("demo2/questions.json").read_text(encoding="utf-8"))["questions"]
    br = json.loads(Path("results/demo2/branches.json").read_text(encoding="utf-8"))
    prefix = br["arms"]["base"]["prefix"]
    ex = [(p["message"], p["reply"]) for p in prefix]
    older = ex[:-3]
    print("Demo2:", len(ex), "exchanges")
    for n, q in enumerate(qs, 1):
        query = SIM.query(q["question"])
        hits = SIM.run(older, query)
        docs = [d for d, _ in hits]
        src = q.get("source_message")
        found = src is not None and exchange_doc_id(src - 1) in docs
        print(f"  Q{n} {q['kind']:<22} person={q.get('person')!s:<11} query={query!r:<32} passages={len(docs)} found_source={found}")

    # K1.3 ack cue: assistant lines of fact passages vs other passages in search outputs
    c199 = importlib.util.module_from_spec(spec2)
    spec2.loader.exec_module(c199)
    fact_acks, other_acks = Counter(), Counter()
    for line in open("data/screens/k1_3_r200.jsonl", encoding="utf-8"):
        row = json.loads(line)
        if row["kind"] not in ("older", "confirm", "never_told"):
            continue
        for user, asst in re.findall(r"^User: (.*)\nAssistant: (.*)$", row["turns"][-2]["content"], re.M):
            (fact_acks if c199.match(user) else other_acks)[asst] += 1
    shared = set(fact_acks) & set(other_acks)
    print(f"K1.3 search outputs: fact passages {sum(fact_acks.values())} with {len(fact_acks)} distinct acks; "
          f"other passages {sum(other_acks.values())} with {len(other_acks)} distinct; acks used on both: {len(shared)}; "
          f"fact passages whose ack is also used on another passage: {sum(fact_acks[a] for a in shared)}")
    print("  top fact acks:", fact_acks.most_common(6))

    # value recurrence across the two outside-writer sets
    sets = {f: load_dev_set(Path(f))[0] for f in ("data/blind_dev/chats", "data/blind_dev2/chats")}
    a1 = {i.answer.casefold() for i in sets["data/blind_dev/chats"] if i.answer}
    a2 = {i.answer.casefold() for i in sets["data/blind_dev2/chats"] if i.answer}
    text1 = " ".join(u + " " + a for i in sets["data/blind_dev/chats"] for u, a in i.exchanges).casefold()
    print(f"outside-writer answers: set1 {len(a1)}, set2 {len(a2)}; set2 answers that are set1 answers {len(a1 & a2)} "
          f"{sorted(a1 & a2)}; set2 answers found anywhere in set1 chats {sum(bool(re.search(rf'\\b{re.escape(v)}\\b', text1)) for v in a2)}")
    # the brief's example words
    words = ["anya", "winnipeg", "corolla", "priya", "landlord", "vet clinic", "sister-in-law"]
    alltext = {f: " ".join(u + " " + a + " " for i in its for u, a in i.exchanges).casefold() + " ".join(i.message.casefold() for i in its)
               for f, its in sets.items()}
    demo = " ".join(u + " " + a for u, a in ex).casefold() + " ".join(q["question"].casefold() for q in qs)
    for w in words:
        print(f"  brief example {w!r}: set1 {w in alltext['data/blind_dev/chats']}, set2 {w in alltext['data/blind_dev2/chats']}, demo2 {w in demo}")
    SIM.INDEX.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
