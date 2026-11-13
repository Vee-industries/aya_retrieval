"""Read-only: rebuild every K1 row's template-wording chat (build_r178's own steps), check each
search row's output byte for byte against k1_r178.jsonl, and pickle {row_id: item}.

Run from the repo root. Writes only into this lane folder.
"""

import importlib.util
import json
import os
import pickle
import random
import sys
from collections import Counter
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
LANE = Path(__file__).resolve().parent
REPO = Path.cwd()
spec = importlib.util.spec_from_file_location("b178", REPO / "scripts/records/build_r178.py")
B = importlib.util.module_from_spec(spec)
sys.modules["b178"] = B
spec.loader.exec_module(B)

from transformers import AutoTokenizer  # noqa: E402

from aya_retrieval.conversations import ITEM_KINDS, NEEDS_SEARCH, NEVER_TOLD, build_item  # noqa
from aya_retrieval.demonstrations import demonstration_turns  # noqa: E402

INDEX = LANE / "idx.sqlite"


def fresh_item(n, share, tokenizer):
    seed = B.FRESH_SEED + 1000 * n
    while True:
        seed += 1
        decoys = random.Random(seed).choice(B.BUILDER.DECOY_CHOICES[NEVER_TOLD])
        item = build_item(f"k1/never_told_{n:04d}", seed, B.BUILDER.SIZE, NEVER_TOLD, "train",
                          decoys, True, False, True, other_facts=share)
        output, _ = B.search(item, item.query, INDEX)
        turns = demonstration_turns(item, output, item.reply, False, item.reply)
        if "chunk_id=" in output and B.BUILDER.row_tokens(turns, tokenizer) <= B.BUILDER.MAX_ROW_TOKENS:
            return item


def main():
    tokenizer = AutoTokenizer.from_pretrained(B.MODEL_ID, revision=B.MODEL_REVISION)
    rows = [json.loads(l) for l in B.BASE_SET.read_text(encoding="utf-8").splitlines()]
    by_id = {r["id"]: r for r in rows}
    tally = Counter()
    sources = B.find_builder_sources(rows, INDEX)
    r102 = {}
    for kind_name, seed, plain, fixed, turns in B.r102_rows(INDEX, tokenizer):
        row = by_id.get(fixed.item_id)
        if row and row["turns"] == turns:
            decoys = next(d for d in (0, 1, 2, 3)
                          if build_item(plain.item_id, seed, B.R102.SIZE, plain.kind, "train", d).exchanges
                          == plain.exchanges)
            r102[fixed.item_id] = (kind_name, seed, decoys, plain, fixed)
    found_before = dict.fromkeys(r102, True)
    for row in rows:
        if row["id"] in sources and row["kind"] in NEEDS_SEARCH:
            item = B.builder_item(row["id"], row["kind"], sources[row["id"]])
            found_before[row["id"]] = B.search(item, item.query, INDEX)[1]
    shares = B.f2_shares(rows, {*sources, *r102})

    def f2_item(row):
        if row["id"] in sources:
            share = shares[row["id"]]
            return B.builder_item(row["id"], row["kind"], sources[row["id"]], share), share
        if row["id"] in r102:
            _, seed, decoys, plain, fixed = r102[row["id"]]
            share = shares[row["id"]]
            other = build_item(plain.item_id, seed, B.R102.SIZE, plain.kind, "train", decoys,
                               other_facts=share)
            return B.with_r102_change(plain, fixed, other), share
        return None, None

    pick_rng = random.Random(B.SELECT_SEED)
    kinds = Counter(row["kind"] for row in rows)
    quota = {kind: round(B.F3_SHARE * kinds[kind]) for kind in ITEM_KINDS}
    order = {kind: pick_rng.sample([r["id"] for r in rows if r["kind"] == kind and r["id"] in sources],
                                   sum(1 for r in rows if r["kind"] == kind and r["id"] in sources))
             for kind in ITEM_KINDS}
    out, items, share_of, f2_items = {}, {}, {}, {}
    for row in rows:
        item, share = f2_item(row)
        if item is None:
            out[row["id"]] = row
            continue
        turns = B.k1_turns(row, item, (), found_before.get(row["id"], False), INDEX, tally)
        if turns is None and row["kind"] == NEVER_TOLD:
            n = tally["never_told_no_passages_replaced"]
            tally["never_told_no_passages_replaced"] += 1
            fi = fresh_item(n, share, tokenizer)
            items[fi.item_id] = fi
            share_of[fi.item_id] = share
            out[row["id"]] = {"id": fi.item_id}
            continue
        if turns is None or B.BUILDER.row_tokens(turns, tokenizer) > B.BUILDER.MAX_ROW_TOKENS:
            out[row["id"]] = row
            continue
        out[row["id"]] = {"id": row["id"]}
        items[row["id"]] = item
        share_of[row["id"]] = share
        if row["id"] in sources:
            f2_items[row["id"]] = item
    with_f3 = set()
    for kind in ITEM_KINDS:
        for reask, wanted in ((True, B.REASK_ROWS.get(kind, 0)), (False, quota[kind])):
            made = 0
            for row_id in order[kind]:
                if made == wanted:
                    break
                if row_id not in f2_items or row_id in with_f3:
                    continue
                changed = B.earlier_answers(f2_items[row_id], sources[row_id].seed, "train", reask)
                if changed is None:
                    continue
                item, used, earlier = changed
                if reask and not B.search(item, item.query, INDEX)[1]:
                    continue
                found = found_before.get(row_id, False)
                turns = B.k1_turns(by_id[row_id], item, earlier, found, INDEX, tally)
                if turns is None or B.BUILDER.row_tokens(turns, tokenizer) > B.BUILDER.MAX_ROW_TOKENS:
                    continue
                items[row_id] = item
                with_f3.add(row_id)
                made += 1

    # check against the K1 file: every search row's output, byte for byte
    k1 = [json.loads(l) for l in (REPO / "data/screens/k1_r178.jsonl").read_text(encoding="utf-8").splitlines()]
    check = Counter()
    for row in k1:
        if row["kind"] not in NEEDS_SEARCH:
            check["no_search"] += 1
            continue
        item = items.get(row["id"])
        if item is None:
            check["search_row_no_chat"] += 1
            continue
        q = json.loads(row["turns"][-3]["content"])[0]["parameters"]["query"]
        output, _ = B.search(item, q, INDEX)
        ok = B.tool_turn(output) == row["turns"][-2]["content"] and item.message == row["turns"][-4]["content"]
        check["output_equal" if ok else "output_differs"] += 1
    print(dict(check))
    with open(LANE / "k1_items.pkl", "wb") as f:
        pickle.dump({"items": items, "share": share_of}, f)
    INDEX.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
