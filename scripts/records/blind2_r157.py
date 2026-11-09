"""Score the second independent set (R-152) as a report on the shipped model, with R-146's measures.

Usage: python scripts/records/blind2_r157.py

Why: R-155 kept the second set's reference runs (base, 6.37 at all eight seeds) as a second
independent report on the shipped model, read only once no 7.x target was left to compute; 7.1's
fail (R-157) leaves none. Four new writers who never saw the generator, the project or the first
set's results wrote these 40 chats (R-152). The measures are R-146's, fixed by R-142 before any
chat was scored: recall (`older` and `confirm`), 6.37 seed 82 against base, exact sign test, with a
paired bootstrap that resamples whole chats; each kind, each writer, each of the eight training
seeds. No prompted baselines were run on this set. Report only. Writes
results/analysis/R-157/blind2.json.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from aya_retrieval.dev_set import load_dev_set
from aya_retrieval.scoring import right_decision
from aya_retrieval.stats import bootstrap_gain_interval, exact_sign_test

EVAL = Path("results/recall_eval")
OUT = Path("results/analysis/R-157/blind2.json")
FROZEN = "3a91c34b2183ec8e3a74a5481540e6873307488b4f89d742f8ec91bd5c3dfe65"  # R-152
RECALL = ("older", "confirm")
KINDS = ("older", "confirm", "in_view", "never_told", "statement")
SEEDS = (82, 83, 94, 95, 96, 97, 98, 99)
BASES = ("blind2_base",)


def load(label: str) -> dict[str, dict]:
    data = json.loads((EVAL / f"{label}_seed_0.json").read_text(encoding="utf-8"))
    if data["items_sha256"] != FROZEN or data["dropped"]:
        raise ValueError(f"{label} was not scored on the frozen set")
    return {r["id"]: r for r in data["rows"] if r["arm"] == "tool_loop"}


def chat_of(item_id: str) -> str:
    return item_id.rsplit("_q", 1)[0]


def count(run: dict, ids: list[str], measure: str = "correct") -> int:
    if measure == "decision":
        return sum(right_decision(run[i]["kind"], len(run[i]["queries"])) for i in ids)
    return sum(bool(run[i]["correct"]) for i in ids)


def stage(row: dict, forbidden: tuple[str, ...]) -> str:
    """Where a wrong recall answer went wrong; the stages of R-139, item 2."""
    if row["ran_out_of_calls"]:
        return "e_ran_out_of_calls"
    if not row["queries"]:
        return "a_no_search"
    if not row["found_fact"]:
        return "b_search_missed_the_fact"
    if any(value.casefold() in row["reply"].casefold() for value in forbidden):
        return "c_named_a_wrong_value"
    return "d_found_but_wrong_otherwise"


def main() -> None:
    items = {i.item_id: i for i in load_dev_set(Path("data/blind_dev2/chats"))[0]}
    runs = {label: load(label) for label in BASES}
    runs |= {s: load(f"blind2_fix17cs37_{s}") for s in SEEDS}
    base, ship = runs["blind2_base"], runs[82]
    if any(sorted(r) != sorted(items) for r in runs.values()):
        raise ValueError("a run scored different questions")
    by_kind = {k: sorted(i for i in items if items[i].kind == k) for k in KINDS}
    recall = by_kind["older"] + by_kind["confirm"]

    only_base = sum(base[i]["correct"] and not ship[i]["correct"] for i in recall)
    only_ship = sum(ship[i]["correct"] and not base[i]["correct"] for i in recall)
    clusters = sorted({chat_of(i) for i in recall})
    cluster_ids = [clusters.index(chat_of(i)) for i in recall]
    primary_interval = bootstrap_gain_interval(
        [int(base[i]["correct"]) for i in recall],
        [[int(ship[i]["correct"]) for i in recall]],
        clusters=cluster_ids,
    )
    seeds_interval = bootstrap_gain_interval(
        [int(base[i]["correct"]) for i in recall],
        [[int(runs[s][i]["correct"]) for i in recall] for s in SEEDS],
        clusters=cluster_ids,
    )
    with_wrong = [i for i in recall if items[i].forbidden]
    writers = sorted({i[:2] for i in items})
    misses = [i for i in recall if not ship[i]["correct"]]
    report = {
        "items": len(items),
        "chats": len({chat_of(i) for i in items}),
        "primary": {
            "measure": "recall (older and confirm), 6.37 seed 82 against base",
            "items": len(recall),
            "base": count(base, recall),
            "ship": count(ship, recall),
            "only_base": only_base,
            "only_ship": only_ship,
            "p_exact_sign": exact_sign_test(only_base, only_ship),
            "chat_resampled_interval": primary_interval,
        },
        "per_kind_correct": {
            k: {str(label): count(run, ids) for label, run in runs.items()} | {"items": len(ids)}
            for k, ids in by_kind.items()
        },
        "per_kind_right_decision": {
            k: {str(label): count(run, ids, "decision") for label, run in runs.items()}
            | {"items": len(ids)}
            for k, ids in by_kind.items()
        },
        "recall_per_writer": {
            w: {
                "items": len(ids := [i for i in recall if i.startswith(w)]),
                "base": count(base, ids),
                "ship": count(ship, ids),
                "seeds_min": min(count(runs[s], ids) for s in SEEDS),
                "seeds_max": max(count(runs[s], ids) for s in SEEDS),
            }
            for w in writers
        },
        "recall_per_seed": {s: count(runs[s], recall) for s in SEEDS},
        "recall_eight_seeds_chat_resampled_interval": seeds_interval,
        "recall_on_questions_with_wrong_values": {
            "items": len(with_wrong),
            "base": count(base, with_wrong),
            "ship": count(ship, with_wrong),
        },
        "ship_recall_miss_stages": dict(
            sorted(Counter(stage(ship[i], items[i].forbidden) for i in misses).items())
        ),
        "ship_recall_misses": [
            {
                "id": i,
                "answer": items[i].answer,
                "wrong": list(items[i].forbidden),
                "reply": ship[i]["reply"],
                "stage": stage(ship[i], items[i].forbidden),
            }
            for i in misses
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "ship_recall_misses"}, indent=1))


if __name__ == "__main__":
    main()
