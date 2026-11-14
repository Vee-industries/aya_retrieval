"""R-253: one seed's on-policy stage set: K1.3's rows plus balanced corrections from its own turns.

Usage: python scripts/records/build_onpolicy_rows.py SEED [START]
  START  ``k13`` (default, OP, R-253) or ``t6`` (OP2, R-256: T6's eval ``op_t6_SEED``, T6's own
         set K4.8 whole as rehearsal, out ``data/screens/k4_8op2_SEED_r256.jsonl``, hashed with
         "R-256"). The base set's ``meta`` and ``k4_questions`` are carried, and R-207's
         check_false line counts the base's natural rows too (K1.3 has none, so OP is unchanged).
         Or ``op`` (OP3, R-263: OP's eval ``op_op_SEED``, a second round whose rehearsal is OP's
         whole seed set, round 1's corrections included; out
         ``data/screens/k13op3_SEED_r263.jsonl``).
         An item that already has a row in the base set gets no second row (R-263).

Reads ``results/recall_eval/op_k13_SEED_seed_0.json`` (K1.3's seed adapter on the items in
``data/onpolicy/items``) and rebuilds each item's turns from the model's own queries, with the
tool's real outputs for them (the same search over exchanges 1 to 21). Rows:
- answer: an ``older`` item it got wrong whose last search returned the source message (its exact
  text, as ``build_k3.py``); the reply is the writer's.
- decline: a trap it got wrong by naming the stored fact's value; the reply is a decline from
  ``TRAIN.unknown_replies``.
- the decline side is filled with the model's own correct trap declines, then both sides are cut
  one to one (K4's rule, R-208), in the order of SHA-256("R-253|SEED|id").
A row whose queries break R-205's first-query rule is dropped. Writes
``data/screens/k13op_SEED_r253.jsonl`` (K1.3's 1,094 rows plus the corrections) and its
provenance, with ``meta`` and ``k4_questions`` for ``check_k3.py``, the counts by type, and the
item chats' overlap with every chat-based gate set (six-word runs; counts only, no text printed).
hard_dev and probe are generated from pools; ``check_k3.py``'s dev-question line covers them.
"""

from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

from aya_retrieval.provenance import run_metadata
from aya_retrieval.recall_tool import build_search_tool

HERE = Path(__file__).resolve().parent
ITEMS = Path("data/onpolicy/items")
META = Path("data/onpolicy/meta.json")
STARTS = {  # start: (record, rehearsal set, output stem)
    "k13": ("R-253", Path("data/screens/k1_3_r200.jsonl"), "k13op_{seed}_r253"),
    "t6": ("R-256", Path("data/screens/k4_8_r220.jsonl"), "k4_8op2_{seed}_r256"),
    "op": ("R-263", Path("data/screens/k13op_{seed}_r253.jsonl"), "k13op3_{seed}_r263"),
}
CHECKED = Path("data/screens/k4_8_r220.jsonl")  # K4.8, checked (R-220): its check_false rows
FALSE_SHARE = 0.15  # R-207's line
GATE_CHATS = ("data/blind_dev/chats", "data/blind_dev2/chats", "demo2", "demo3")


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


K31 = load("build_k3_1")
K3 = K31.K3
ITEMS_BUILD = load("build_onpolicy_items")


def as_list(value) -> list:
    return value if isinstance(value, list) else ast.literal_eval(value)


def cleaned(queries: list[str], question: str) -> list[str]:
    """Each of the model's queries cut to R-205's first-query rule (words of the question, no
    filler, at most 4), empty ones and repeats dropped; the search then runs on these (R-253)."""
    asked, out = set(K31.tokens(question)), []
    for query in queries:
        kept = [
            w
            for w in K31.tokens(query)
            if w in asked and w not in K31.FILLER and w not in K31.BRIEF_FILLER
        ][:4]
        text = " ".join(dict.fromkeys(kept))
        if text and text not in out:
            out.append(text)
    return out


def writer_question(row_id: str) -> dict:
    """A K4.8 natural row's question record, from K4.8's writer copies (``k3_wN_CC_QQ``)."""
    _, stem, c, q = row_id.split("_")
    chats = json.loads(
        Path(f"data/screens/k4_8/writers/k3/{stem}.json").read_text(encoding="utf-8")
    )
    return chats["chats"][int(c)]["questions"][int(q)]


def truthy(value) -> bool:
    return value is True or value == "True"


def gate_overlap() -> dict[str, int]:
    """Item chats sharing a six-word run with each chat-based gate set (0 expected; counts only)."""

    def chat_text(path: Path) -> str:
        """The conversation's words only: exchanges of a JSON chat, or the lines of chat.txt."""
        if path.suffix == ".txt":
            return path.read_text(encoding="utf-8")
        exchanges = json.loads(path.read_text(encoding="utf-8")).get("exchanges", [])
        return "\n".join(" ".join(pair) for pair in exchanges)

    items = [K31.runs(chat_text(p), K31.S3_RUN) for p in ITEMS.glob("*.json")]
    out = {}
    for folder in GATE_CHATS:
        gate = set()
        for p in Path(folder).glob("*"):
            if p.suffix == ".json" or p.name == "chat.txt":
                gate |= K31.runs(chat_text(p), K31.S3_RUN)
        out[folder] = sum(bool(runs & gate) for runs in items)
    return out


def main(seed: int, start: str = "k13") -> None:
    tag, base_path, stem = STARTS[start]
    base_path = Path(str(base_path).format(seed=seed))
    earlier = {  # R-263: items already corrected in an earlier round
        json.loads(line)["id"] for line in base_path.read_text(encoding="utf-8").splitlines()
    }
    provenance = run_metadata()
    eval_path = f"results/recall_eval/op_{start}_{seed}_seed_0.json"
    result = json.loads(Path(eval_path).read_text(encoding="utf-8"))
    meta_q = json.loads(META.read_text(encoding="utf-8"))
    rows_by_kind, dropped = {"answer": [], "decline": [], "correct_decline": []}, Counter()
    dev_runs = set().union(*(K31.CHECK.runs(x) for x in K31.CHECK.dev_questions()))
    s3 = set()
    for path in sorted(K31.OVERLAP.CHATS.glob("*.json")):
        s3 |= K31.runs(K31.OVERLAP.chat_text(json.loads(path.read_text(encoding="utf-8"))), 6)
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        for r in result["rows"]:
            if r["arm"] != "tool_loop":
                continue
            q = meta_q[r["id"]]
            chat = json.loads(
                (ITEMS / f"{r['id'].rsplit('_q', 1)[0]}.json").read_text(encoding="utf-8")
            )
            exchanges = [tuple(e) for e in chat["exchanges"]]
            queries = as_list(r["queries"])
            if not queries:
                dropped["no search"] += 1
                continue
            queries = cleaned(queries, q["question"])  # R-253: R-205's first-query rule kept
            if not queries:
                dropped["no query left after the rule"] += 1
                continue
            tool = build_search_tool(
                exchanges[: K3.IN_VIEW_FROM - 1], Path(tmp) / f"{r['id']}.sqlite", False
            )
            outputs = [(x, (o.output if (o := tool.execute(x)).success else "")) for x in queries]
            correct = truthy(r["correct"])
            if r["kind"] == "older":
                source = f"User: {exchanges[q['source_message'] - 1][0]}\n"
                if correct or source not in outputs[-1][1] + "\n":
                    dropped["older right, or source not returned"] += 1
                    continue
                side, reply, names_value = "answer", q["reply"], True
            else:
                trap = chat["questions"][int(r["id"].rsplit("_q", 1)[1])]["wrong"][0].casefold()
                if trap not in outputs[-1][1].casefold():
                    dropped["trap value not returned"] += 1
                    continue
                side = "correct_decline" if correct else "decline"
                reply, names_value = K3.unknown_reply(f"op{seed}_{r['id']}"), False
            turns = K3.view_turns(exchanges[K3.IN_VIEW_FROM - 1 :])
            turns.append({"role": "user", "content": q["question"]})
            for x, o in outputs:
                turns += K3.search_turns(x, o)
            turns.append({"role": "assistant", "content": reply})
            if K31.CHECK.runs(q["question"]) & dev_runs:  # K3.1's drops (R-206)
                dropped["dev or Demo2 question run"] += 1
                continue
            spoken = [t["content"] for t in turns if not t["content"].startswith("Tool")]
            if any(K31.runs(x, 6) & s3 for x in spoken):
                dropped["S3 six-word run"] += 1
                continue
            rid = f"k3_op{seed}_{r['id']}"
            if rid in earlier:
                dropped["item corrected in an earlier round"] += 1
                continue
            kind = "older" if r["kind"] == "older" else "never_told"
            m = {
                "kind": q["kind"] if r["kind"] == "older" else "never_told",
                "person": q.get("person"),
                "names_value": names_value,
                "searches": len(outputs),
                "passages": K3.passages(outputs[-1][1]),
            }
            record = {**q, "kind": m["kind"], "query": queries[0]}
            rows_by_kind[side].append(
                {"id": rid, "kind": kind, "turns": turns, "meta": m, "q": record}
            )
    key = lambda row: hashlib.sha256(f"{tag}|{seed}|{row['id']}".encode()).digest()  # noqa: E731
    answers = sorted(rows_by_kind["answer"], key=key)
    # R-205's user share: cut answer rows about someone else, in hashed order, to a third
    user = [r for r in answers if (r["meta"]["person"] or "me") == "me"]
    others = [r for r in answers if (r["meta"]["person"] or "me") != "me"]
    while others and 3 * len(user) < len(user) + len(others):
        others.pop()
    answers = sorted(user + others, key=key)
    declines = sorted(rows_by_kind["decline"], key=key) + sorted(
        rows_by_kind["correct_decline"], key=key
    )
    n = min(len(answers), len(declines))
    kept = K3.within_tokens(answers[:n] + declines[:n])
    new_answers = sum(r["meta"]["names_value"] for r in kept)  # R-263's stop rule reads this
    base_text = base_path.read_text(encoding="utf-8")
    out_rows = [json.loads(line) for line in base_text.splitlines()]
    base_prov = json.loads(base_path.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    base_meta, base_ids = base_prov.get("meta", {}), {r["id"] for r in out_rows}
    base_natural = sum(i.startswith("k3_") for i in base_ids)
    base_false = sum((m or {}).get("kind") == "check_false" for m in base_meta.values())
    # R-207's line: K4.8's natural check_false rows not already in the set, in hashed order,
    # until they are 15% of the set's natural rows
    checked = json.loads(CHECKED.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    falses = sorted(
        (
            json.loads(line)
            for line in CHECKED.read_text(encoding="utf-8").splitlines()
            if (checked["meta"].get(json.loads(line)["id"]) or {}).get("kind") == "check_false"
            and json.loads(line)["id"] not in base_ids
        ),
        # the user's own first, so the user share line holds (R-205); hashed within each
        key=lambda row: ((checked["meta"][row["id"]].get("person") or "me") != "me", key(row)),
    )
    added = []
    while falses and base_false + len(added) < FALSE_SHARE * (
        base_natural + len(kept) + len(added)
    ):
        row = falses.pop(0)
        added.append({**row, "meta": checked["meta"][row["id"]], "q": writer_question(row["id"])})
    kept += added
    meta = {**base_meta, **{r["id"]: r.pop("meta") for r in kept}}
    questions = {
        **base_prov.get("k4_questions", {}),
        **{i: q for r in kept if (q := r.pop("q")) is not None for i in [r["id"]]},
    }
    out = out_rows + kept
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    path = Path(f"data/screens/{stem.format(seed=seed)}.jsonl")
    path.write_bytes(text.encode("utf-8"))
    report = {
        "provenance": provenance,
        "record": tag,
        "seed": seed,
        "base_set": base_path.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "eval": eval_path,
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "built_by_type": {k: len(v) for k, v in rows_by_kind.items()},
        "kept_each_side": n,
        "new_answer_rows": new_answers,
        "kept_by_kind": dict(Counter(meta[r["id"]]["kind"] for r in kept)),
        "dropped": dict(dropped),
        "gate_chat_overlap_six_word_runs": gate_overlap(),
        "item_chats_sharing_a_gate_answer_run": sum(
            ITEMS_BUILD.shares_gate_answer(
                json.loads(p.read_text(encoding="utf-8"))["exchanges"], ITEMS_BUILD.gate_answers()
            )
            for p in ITEMS.glob("*.json")
        ),
        "meta": meta,
        "k4_questions": questions,
    }
    path.with_suffix(".provenance.json").write_bytes(json.dumps(report, indent=1).encode("utf-8"))
    print(
        f"{path}: {len(out)} rows; built {report['built_by_type']}, kept {n} each side, "
        f"{len(kept)} after tokens; dropped {dict(dropped)}; "
        f"gate overlap {report['gate_chat_overlap_six_word_runs']}"
    )


if __name__ == "__main__":
    main(int(sys.argv[1]), *sys.argv[2:3])
