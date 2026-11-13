"""Read-only: on outside-writer older items, K1.3's outcome when the fact was found, split by how
many content words (R-176) the question shares with the fact exchange's user line; and the same
overlap in K1's training found rows (question vs fact line). Also first-person older questions."""
import importlib.util, json, re, pickle
from collections import Counter
from pathlib import Path
LANE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r176", "scripts/records/demo_overlap_r176.py")
R = importlib.util.module_from_spec(spec); spec.loader.exec_module(R)
from aya_retrieval.dev_set import load_dev_set
DECL = re.compile(r"don't|do not|not sure|guess|no idea|haven't|not told|didn't|can't|what is it", re.I)
def cw(t): return {w.removesuffix("'s") for w in R.words(t)}
first = re.compile(r"\b(i|me|my)\b")
c = Counter()
for name, folder in (("blind", "data/blind_dev/chats"), ("blind2", "data/blind_dev2/chats")):
    items = {i.item_id: i for i in load_dev_set(Path(folder))[0]}
    for s in (82, 83, 94):
        for r in json.load(open(f"results/recall_eval/{name}_k1_3_r200_{s}_seed_0.json", encoding="utf-8"))["rows"]:
            if r["arm"] != "tool_loop" or r["kind"] != "older" or not r.get("found_fact"):
                continue
            it = items[r["id"]]
            ov = len(cw(it.message) & cw(it.exchanges[it.fact_index][0]))
            b = "0" if ov == 0 else ("1" if ov == 1 else "2+")
            out = "right" if r["correct"] else ("declined" if DECL.search(r["reply"]) else "other")
            c[(b, out)] += 1
print("outside-writer older, K1.3 found rows, overlap bucket x outcome:", sorted(c.items()))
# first-person older questions on outside sets (no relation word / name possessive)
fp = Counter()
for folder in ("data/blind_dev/chats", "data/blind_dev2/chats"):
    for it in load_dev_set(Path(folder))[0]:
        if it.kind in ("older", "confirm"):
            fp["items"] += 1
            if re.search(r"\b(do i|did i|am i|i'm|im|was i|should i|my (job|work|allergy|doctor|class|school|car|flat|apartment|address|birthday|hometown))\b", it.message.lower()):
                fp["looks_about_user"] += 1
print("outside-writer older+confirm questions that look like facts about the user (rough regex):", dict(fp))
# training
items = pickle.load(open(LANE / "k1_items.pkl", "rb"))["items"]
nq = json.loads((LANE / "new_queries.json").read_text(encoding="utf-8"))
tc = Counter()
for r in nq:
    if r["kind"] == "never_told": continue
    it = items[r["id"]]
    who = r["who"].lower()
    ov = len((cw(it.message) & cw(it.exchanges[it.fact_index][0])) - {who})
    tc["0" if ov == 0 else ("1" if ov == 1 else "2+")] += 1
    tc["fact_line_names_who"] += who in it.exchanges[it.fact_index][0].lower()
    tc["n"] += 1
print("K1 training found rows: question/fact-line overlap beyond who:", dict(tc))
