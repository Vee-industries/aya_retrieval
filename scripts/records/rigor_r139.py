"""R-139's development analysis: the primary test, Holm family, seeds, failures, distance.

Usage: python scripts/records/rigor_r139.py

Why each part exists (R-139): the primary test is fixed in advance so the write-up cannot pick its
best comparison afterwards; Holm keeps the secondary family's error rate at 5% as a whole; the
seed table shows how much training alone moves the score; the intervals resample fact templates
because questions built from one template are not independent; the failure stages say where a
wrong answer goes wrong; the distance table checks that recall does not fade with how far back the
fact was told. Writes results/analysis/R-139/dev_rigor.json.
"""

import json
import random
from collections import Counter
from pathlib import Path

from aya_retrieval.conversations import ITEM_KINDS, rebuild_eval_item
from aya_retrieval.pools import POOLS
from aya_retrieval.scoring import right_decision
from aya_retrieval.stats import bootstrap_gain_interval, exact_sign_test

EVAL = Path("results/recall_eval")
OUT = Path("results/analysis/R-139/dev_rigor.json")
PROBE_SEED = 73157
RECALL = ("older", "confirm")
SHIP = "fix17cs37_82"
# Every training seed 6.37 was scored at; 97 to 99 joined once 6.38's comparison was read (R-140).
SEEDS = (82, 83, 94, 95, 96, 97, 98, 99)
POOL = {"probe": "probe", "hd": "hard_dev"}
BASE = {"probe": "probe2_base"}  # base on the plain probe was scored under this label


def load(label: str) -> dict[str, dict]:
    data = json.loads((EVAL / f"{label}_seed_{PROBE_SEED}.json").read_text(encoding="utf-8"))
    return {r["id"]: r for r in data["rows"] if r["arm"] == "tool_loop"}


def scored_seeds(condition: str) -> tuple[int, ...]:
    """The seeds 6.37 has a result for in this condition; each table names the seeds it used."""
    return tuple(
        s for s in SEEDS if (EVAL / f"{condition}_fix17cs37_{s}_seed_{PROBE_SEED}.json").exists()
    )


def base_label(condition: str) -> str:
    return BASE.get(condition, f"{condition}_base")


def template_of(item_id: str, kind: str, pool: str) -> int:
    """The fact template's index, from the generator's first draw on the item's seed."""
    size, number = int(item_id.split("_")[0]), int(item_id.rsplit("_", 1)[1])
    seed = PROBE_SEED + size * 1000 + ITEM_KINDS.index(kind) * 100 + number
    names = sorted(POOLS[pool].facts)
    return names.index(random.Random(seed).choice(names))


def outcome(row: dict, measure: str) -> int:
    return int(
        right_decision(row["kind"], len(row["queries"]))
        if measure == "decision"
        else row["correct"]
    )


def paired(base: dict, adapter: dict, kinds: tuple[str, ...], measure: str) -> tuple[int, int, int]:
    """Items base alone got right, the adapter alone got right, and the items compared."""
    ids = [i for i, r in base.items() if r["kind"] in kinds]
    if sorted(ids) != sorted(i for i, r in adapter.items() if r["kind"] in kinds):
        raise ValueError("base and adapter were scored on different items")
    only_base = sum(outcome(base[i], measure) > outcome(adapter[i], measure) for i in ids)
    only_adapter = sum(outcome(adapter[i], measure) > outcome(base[i], measure) for i in ids)
    return only_base, only_adapter, len(ids)


def test(name: str, pairs: list[tuple[dict, dict]], kinds: tuple[str, ...], measure: str) -> dict:
    only_base = only_adapter = n = 0
    for base, adapter in pairs:
        b, a, k = paired(base, adapter, kinds, measure)
        only_base, only_adapter, n = only_base + b, only_adapter + a, n + k
    return {
        "test": name,
        "items": n,
        "only_base": only_base,
        "only_adapter": only_adapter,
        "p": exact_sign_test(only_base, only_adapter),
    }


def holm(tests: list[dict], alpha: float = 0.05) -> None:
    """Mark each test significant or not under Holm's step-down rule, in place."""
    still = True
    for rank, t in enumerate(sorted(tests, key=lambda t: t["p"])):
        still = still and t["p"] < alpha / (len(tests) - rank)
        t["holm_significant"] = still


def across_seeds(condition: str) -> dict:
    """Per-seed recall, its range, and the pooled gain with a template-resampled interval."""
    pool = POOL[condition.rsplit("_", 1)[-1]]
    base = load(base_label(condition))
    ids = sorted(i for i, r in base.items() if r["kind"] in RECALL)
    seeds = scored_seeds(condition)
    runs = {s: load(f"{condition}_fix17cs37_{s}") for s in seeds}
    counts = {s: sum(runs[s][i]["correct"] for i in ids) for s in seeds}
    clusters = [template_of(i, base[i]["kind"], pool) for i in ids]
    interval = bootstrap_gain_interval(
        [int(base[i]["correct"]) for i in ids],
        [[int(runs[s][i]["correct"]) for i in ids] for s in seeds],
        clusters=clusters,
    )
    return {
        "condition": condition,
        "seeds": seeds,
        "items": len(ids),
        "templates": len(set(clusters)),
        "base": sum(base[i]["correct"] for i in ids),
        "per_seed": counts,
        "min": min(counts.values()),
        "max": max(counts.values()),
        "difference_and_95_interval": interval["difference"],
    }


def stage(row: dict, forbidden: tuple[str, ...]) -> str:
    """Where a wrong recall answer went wrong (R-139, item 2)."""
    if row["ran_out_of_calls"]:
        return "e_ran_out_of_calls"
    if not row["queries"]:
        return "a_no_search"
    if not row["found_fact"]:
        return "b_search_missed_the_fact"
    text = row["reply"].casefold()
    if any(value.casefold() in text for value in forbidden):
        return "c_named_a_wrong_value"
    return "d_found_but_wrong_otherwise"


def failures_and_distance(condition: str, label: str) -> tuple[Counter, dict]:
    pool = POOL[condition]
    stages, by_quarter = Counter(), {}
    for row in load(label).values():
        if row["kind"] not in RECALL:
            continue
        item = rebuild_eval_item(row, PROBE_SEED, pool)
        if not row["correct"]:
            stages[stage(row, item.forbidden)] += 1
        older_slots = len(item.exchanges) - 3
        quarter = min(3, item.fact_index * 4 // older_slots)  # 0 = told earliest
        key = f"{row['size']}_q{quarter}"
        right, total = by_quarter.get(key, (0, 0))
        by_quarter[key] = (right + row["correct"], total + 1)
    return stages, by_quarter


def main() -> None:
    report: dict = {"seeds": SEEDS, "shipping_copy": SHIP}

    hd = (load("hd_base"), load(f"hd_{SHIP}"))
    report["primary"] = test("hard_dev recall, 6.37 seed 82 vs base", [hd], RECALL, "correct")
    report["primary"]["significant_below_0.01"] = report["primary"]["p"] < 0.01

    secondary = [
        test("probe recall", [(load("probe2_base"), load(f"probe_{SHIP}"))], RECALL, "correct")
    ]
    for condition in ("st_fixh_probe", "st_fixh_hd", "st_phone_probe", "st_phone_hd"):
        pair = (load(base_label(condition)), load(f"{condition}_{SHIP}"))
        secondary.append(test(condition + " recall", [pair], RECALL, "correct"))
    plain = [(load("probe2_base"), load(f"probe_{SHIP}")), hd]
    for kind in ("in_view", "never_told", "statement"):
        secondary.append(test(kind + " right decision", plain, (kind,), "decision"))
    holm(secondary)
    report["secondary"] = secondary

    report["across_seeds"] = [
        across_seeds(c)
        for c in ("probe", "hd", "st_fixh_probe", "st_fixh_hd", "st_phone_probe", "st_phone_hd")
    ]

    report["failure_stages"], report["recall_by_distance"] = {}, {}
    for condition in POOL:
        labels = {"base": base_label(condition)} | {
            f"6.37_{s}": f"{condition}_fix17cs37_{s}" for s in scored_seeds(condition)
        }
        for name, label in labels.items():
            stages, quarters = failures_and_distance(condition, label)
            report["failure_stages"][f"{condition} {name}"] = dict(sorted(stages.items()))
            report["recall_by_distance"][f"{condition} {name}"] = dict(sorted(quarters.items()))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1), encoding="utf-8")

    for t in [report["primary"], *secondary]:
        held = {True: "Holm yes", False: "Holm no", None: "primary"}[t.get("holm_significant")]
        tally = f"base only {t['only_base']}, 6.37 only {t['only_adapter']} of {t['items']}"
        print(f"  {t['test']}: {tally}, p={t['p']:.2e}, {held}")
    for a in report["across_seeds"]:
        d, lo, hi = a["difference_and_95_interval"]
        print(f"  {a['condition']}: base {a['base']}/{a['items']}, per seed {a['per_seed']}")
        print(f"    gain {d:+.3f} [{lo:+.3f}, {hi:+.3f}] over {a['templates']} templates")
    for name, stages in report["failure_stages"].items():
        print(f"  failures {name}: {stages}")
    for name, quarters in report["recall_by_distance"].items():
        print(f"  distance {name}: " + " ".join(f"{k} {r}/{t}" for k, (r, t) in quarters.items()))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
