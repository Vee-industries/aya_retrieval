"""Build Kevin's blind check of the scorer (R-139, item 5): 50 scored answers, model names removed.

Usage: python scripts/records/build_human_check_r139.py

Why: the scorer calls a reply right when it contains the answer and no wrong value. It can miss a
right answer worded another way, or pass a reply that names the answer while saying something false.
A person marking a blind sample measures how often it does. The strata are by model and verdict, and
lean toward 6.37's wrong replies: R-141 found that most of 6.37's hard_dev misses found the fact and
still scored wrong, and a scorer that is too strict would show up there. Base's wrong replies are
drawn only where it searched, since a reply with no search and no answer tests nothing.

Writes results/human_check/R-139/sheet.json (what Kevin sees) and key.json (model, file, row id,
the scorer's verdict), drawn with random.Random(139).
"""

import json
import random
from pathlib import Path

from aya_retrieval.conversations import NEVER_TOLD, rebuild_eval_item

EVAL = Path("results/recall_eval")
OUT = Path("results/human_check/R-139")
PROBE_SEED = 73157
SOURCES = {  # label: (model, pool)
    "probe2_base": ("base", "probe"),
    "hd_base": ("base", "hard_dev"),
    "probe_fix17cs37_82": ("6.37", "probe"),
    "hd_fix17cs37_82": ("6.37", "hard_dev"),
}
KINDS = ("older", "confirm", "in_view", "never_told")  # statements are scored on the search alone
STRATA = {
    "6.37 scored right": 12,
    "6.37 scored wrong": 15,
    "base scored right": 10,
    "base scored wrong after a search": 13,
}


def stratum(row: dict, model: str) -> str | None:
    if row["correct"]:
        return f"{model} scored right"
    if model == "base":
        return "base scored wrong after a search" if row["queries"] else None
    return "6.37 scored wrong"


def main() -> None:
    pools = {name: [] for name in STRATA}
    for label, (model, pool) in SOURCES.items():
        data = json.loads((EVAL / f"{label}_seed_{PROBE_SEED}.json").read_text(encoding="utf-8"))
        for row in data["rows"]:
            if row["arm"] != "tool_loop" or row["kind"] not in KINDS:
                continue
            item = rebuild_eval_item(row, PROBE_SEED, pool)
            told = "" if row["kind"] == NEVER_TOLD else item.exchanges[item.fact_index][0]
            name = stratum(row, model)
            if name is None:
                continue
            pools[name].append(
                {
                    "model": model,
                    "label": label,
                    "id": row["id"],
                    "scorer": bool(row["correct"]),
                    "line": {
                        "kind": row["kind"],
                        "question": row["message"],
                        "what_was_told": told,
                        "right_answer": row["answer"] or "(never told: say so)",
                        "wrong_values": list(item.forbidden),
                        "reply": row["reply"],
                    },
                }
            )
    rng = random.Random(139)
    drawn = []
    for name, count in STRATA.items():
        group = sorted(pools[name], key=lambda e: (e["label"], e["id"]))
        drawn += [dict(e, stratum=name) for e in rng.sample(group, min(count, len(group)))]
    rng.shuffle(drawn)
    sheet = [{"n": n + 1, **e["line"]} for n, e in enumerate(drawn)]
    key = [
        {"n": n + 1, **{k: e[k] for k in ("model", "label", "id", "scorer", "stratum")}}
        for n, e in enumerate(drawn)
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "sheet.json").write_text(
        json.dumps(sheet, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    (OUT / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    sizes = {name: len(pool) for name, pool in pools.items()}
    print(f"drew {len(sheet)} lines from strata of {sizes}")


if __name__ == "__main__":
    main()
