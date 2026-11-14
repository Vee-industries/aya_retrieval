"""R-271: one seed's OPT set: OP's seed set plus corrections from C1's own turns on pool items.

Usage: python scripts/records/build_onpolicy_template.py SEED [c1|op]

R-273 (OPO): with ``op`` the eval read is OP's seed adapter (``opt_op_SEED``), the hashed order is
SHA-256("R-273|SEED|id") and the output is ``data/screens/k13opo_SEED_r273.jsonl``; every other
step is the same. ``c1`` (the default) is R-271's OPT as written.

Reads ``results/recall_eval/opt_c1_SEED_seed_271071.json`` (C1's seed adapter on the training
pool, ``--pool train --seed 271071 --items-per-kind 24 --kinds older confirm never_told``) and
rebuilds each tool_loop row's item from its id, as the evaluation built it. The model's own
queries run again, unchanged and uncut, on the item's out-of-view exchanges, so each row holds
the tool's real outputs. Turns are shaped like K1.3's: the exchanges in view, the question, one
search call and result per query, the reply. Rows:
- answer: an ``older`` or ``confirm`` item it got wrong although a search found the fact, kept
  only if the answer's value is in the last output; the reply is the item's.
- decline: a never_told item whose reply names a value; the reply is a decline from
  ``TRAIN.unknown_replies``.
- correct_decline: a never_told item it declined after a search; the same decline reply.
A row with no search is dropped, and K3.1's drops apply (dev question run, S3 six-word run). The
balance is OP's (``build_onpolicy_rows.py``): both sides cut one to one in the order of
SHA-256("R-271|SEED|id"), the declines before the correct declines. The rehearsal is OP's whole
seed set ``data/screens/k13op_SEED_r253.jsonl``, its ``meta`` and ``k4_questions`` carried, and
R-207's check_false line fills it as OP does. Writes ``data/screens/k13opt_SEED_r271.jsonl`` and
its provenance. No row is marked with a loss mask.
"""

from __future__ import annotations

import hashlib
import importlib
import json
import sys
import tempfile
from collections import Counter
from pathlib import Path

from aya_retrieval.conversations import CONFIRM, NEVER_TOLD, OLDER, rebuild_eval_item
from aya_retrieval.provenance import REPO_ROOT, run_metadata
from aya_retrieval.recall_tool import build_search_tool
from aya_retrieval.report_data import EVAL_DIR, eval_rows

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
OPR = importlib.import_module("build_onpolicy_rows")  # OP's helpers and its check_false line
K31 = OPR.K31
K3 = OPR.K3
PROBE_SEED = 271071  # the eval's --seed
BASE = "data/screens/k13op_{seed}_r253.jsonl"
STARTS = {  # start adapter: (record, output stem); R-271's OPT from C1, R-273's OPO from OP
    "c1": ("R-271", "k13opt_{seed}_r271"),
    "op": ("R-273", "k13opo_{seed}_r273"),
}


def eval_label(seed: int, start: str = "c1") -> str:
    return f"opt_{start}_{seed}"


def source_first(answer: str, output: str) -> bool:
    """Whether the first passage of ``output`` is the one holding ``answer`` (casefold)."""
    found = output.split("[chunk_id=")[1:]
    return bool(found) and answer.casefold() in found[0].casefold()


def main(seed: int, start: str = "c1") -> None:
    TAG, STEM = STARTS[start]  # noqa: N806
    eval_path = EVAL_DIR / f"{eval_label(seed, start)}_seed_{PROBE_SEED}.json"
    if not eval_path.exists():
        sys.exit(f"no eval file {eval_path}")
    provenance = run_metadata()
    report_in = json.loads(eval_path.read_text(encoding="utf-8"))
    pool, decoys = report_in["pool"], report_in.get("decoys", 1)
    rows_by_kind, dropped = {"answer": [], "decline": [], "correct_decline": []}, Counter()
    dev_runs, s3 = OPR.gate_runs()
    with tempfile.TemporaryDirectory(dir=Path("..").resolve(), ignore_cleanup_errors=True) as tmp:
        for r in eval_rows(eval_label(seed, start), PROBE_SEED):
            if r["kind"] not in (OLDER, CONFIRM, NEVER_TOLD):
                dropped["kind not used"] += 1
                continue
            queries = OPR.as_list(r["queries"])  # the model's own, unchanged (no cut)
            if not queries:
                dropped["no search"] += 1
                continue
            item = rebuild_eval_item(r, PROBE_SEED, pool, decoys)
            tool = build_search_tool(item.older(), Path(tmp) / f"{r['id']}.sqlite", False)
            outputs = [(x, (o.output if (o := tool.execute(x)).success else "")) for x in queries]
            correct, rid = OPR.truthy(r["correct"]), f"opt{seed}_{r['id']}"
            first = None
            if r["kind"] in (OLDER, CONFIRM):
                if correct or not OPR.truthy(r["found_fact"]):
                    dropped["right, or fact not found"] += 1
                    continue
                if item.answer.casefold() not in outputs[-1][1].casefold():
                    dropped["answer value not in the last output"] += 1
                    continue
                side, reply, names_value = "answer", item.reply, True
                first = source_first(item.answer, outputs[-1][1])
            else:
                named = any(v.casefold() in r["reply"].casefold() for v in item.forbidden)
                if not correct and not named:
                    dropped["wrong without naming a value"] += 1
                    continue
                side = "correct_decline" if correct else "decline"
                reply, names_value = K3.unknown_reply(rid), False
            turns = K3.view_turns(list(item.view()))
            turns.append({"role": "user", "content": item.message})
            for x, o in outputs:
                turns += K3.search_turns(x, o)
            turns.append({"role": "assistant", "content": reply})
            if K31.CHECK.runs(item.message) & dev_runs:  # K3.1's drops (R-206)
                dropped["dev or Demo2 question run"] += 1
                continue
            spoken = [t["content"] for t in turns if not t["content"].startswith("Tool")]
            if any(K31.runs(x, 6) & s3 for x in spoken):
                dropped["S3 six-word run"] += 1
                continue
            m = {
                "kind": r["kind"],
                "person": getattr(item, "person", None),  # RecallItem names none
                "names_value": names_value,
                "searches": len(outputs),
                "passages": K3.passages(outputs[-1][1]),
            }
            row = {"id": rid, "kind": r["kind"], "turns": turns, "meta": m, "first": first}
            rows_by_kind[side].append(row)
    key = lambda row: hashlib.sha256(f"{TAG}|{seed}|{row['id']}".encode()).digest()  # noqa: E731
    answers = sorted(rows_by_kind["answer"], key=key)  # template items name no person (R-205's
    # user share reads natural rows)
    declines = sorted(rows_by_kind["decline"], key=key) + sorted(
        rows_by_kind["correct_decline"], key=key
    )
    n = min(len(answers), len(declines))
    kept = K3.within_tokens(answers[:n] + declines[:n])
    new_answers = sum(r["meta"]["names_value"] for r in kept)
    not_first = sum(r.pop("first") is False for r in kept)
    base_path = Path(BASE.format(seed=seed))
    base_text = base_path.read_text(encoding="utf-8")
    out_rows = [json.loads(line) for line in base_text.splitlines()]
    base_prov = json.loads(base_path.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    base_meta, base_ids = base_prov.get("meta", {}), {r["id"] for r in out_rows}
    added = OPR.check_false_fill(base_ids, base_meta, 0, key)  # the new rows are template rows
    new_meta = {r["id"]: r.pop("meta") for r in kept}
    kept += added
    meta = {**base_meta, **new_meta, **{r["id"]: r.pop("meta") for r in added}}
    questions = {**base_prov.get("k4_questions", {}), **{r["id"]: r.pop("q") for r in added}}
    out = out_rows + kept
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    path = Path(f"data/screens/{STEM.format(seed=seed)}.jsonl")
    path.write_bytes(text.encode("utf-8"))
    report = {
        "provenance": provenance,
        "record": TAG,
        "seed": seed,
        "base_set": base_path.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "eval": eval_path.relative_to(REPO_ROOT).as_posix(),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "built_by_type": {k: len(v) for k, v in rows_by_kind.items()},
        "kept_each_side": n,
        "new_answer_rows": new_answers,
        "source_not_first": not_first,
        "dropped": dict(dropped),
        "meta": meta,
        "k4_questions": questions,
    }
    path.with_suffix(".provenance.json").write_bytes(json.dumps(report, indent=1).encode("utf-8"))
    print(
        f"{path}: {len(out)} rows; built {report['built_by_type']}, kept {n} each side, "
        f"{len(new_meta)} after tokens, {new_answers} naming a value ({not_first} source not "
        f"first), {len(added)} check_false added; dropped {dict(dropped)}"
    )


if __name__ == "__main__":
    start = sys.argv[2:3]
    if len(sys.argv) > 3 or not sys.argv[1:2] or not sys.argv[1].isdigit():
        sys.exit(__doc__.split("\n\n")[1])
    if start not in ([], ["c1"], ["op"]):
        sys.exit(__doc__.split("\n\n")[1])
    main(int(sys.argv[1]), *start)
