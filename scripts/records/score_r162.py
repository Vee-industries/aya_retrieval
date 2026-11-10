"""R-162: score the sealed final run against R-016's rules as amended (R-038, R-039, R-041).

Usage: python scripts/records/score_r162.py [CONDITION ...]

Why: R-162 registered, before any run, four rules that must hold in every condition: recall pooled
over the eight 6.37 adapters at least 20 points above base at each size with a paired exact sign
test below 0.01 (R-016); the same on retrieved answers alone (R-041); each adapter's false
retrievals no more than base's (R-038); each adapter's coherent count at or above base's, judge 1
deciding (R-016, R-039, R-154). Beside them it reports each kind, each adapter, right search
decisions, clean first calls, runs out of calls, recall answers found by search, seed 82 alone (the
shipped model), recall split into ``older`` and ``confirm``, and a whole-conversation resampled
interval, because rule 1's adapter-conversation pairs share conversations, and each run's cost (wall
seconds, seconds per conversation, card memory, tokens read and written per turn against the whole
chat, searches per conversation; Kevin asked for the times as a metric). Coherence is read from
``results/coherence/R-162`` when a condition's judge-1 marks are in; until then it is reported as
waiting. Writes results/analysis/R-162/<condition>.json.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.report_data import false_retrieval
from aya_retrieval.scoring import clean_call
from aya_retrieval.stats import bootstrap_gain_interval, exact_sign_test

EVAL = Path("results/recall_eval")
COHERENCE = Path("results/coherence/R-162")
OUT = Path("results/analysis/R-162")
SEED = 90311
ADAPTERS = tuple(f"fix17cs37_{s}" for s in (82, 83, 94, 95, 96, 97, 98, 99))
SHIPPED = "fix17cs37_82"
SIZES = (58, 419)
KINDS = ("older", "confirm", "in_view", "never_told", "statement")
RECALL = ("older", "confirm")
SHEETS = {
    "A": ("A1", "A2", "A3", "A4", "A5"),
    "B": ("B1", "B2"),
    "C": ("C1", "C2"),
    "D": ("D1", "D2"),
}


def load(condition: str, model: str) -> dict[str, dict]:
    path = EVAL / f"final_{condition}_{model}_seed_{SEED}.json"
    rows = json.loads(path.read_text(encoding="utf-8"))["rows"]
    return {row["id"]: row for row in rows if row["arm"] == "tool_loop"}


def cost(condition: str, model: str) -> dict:
    """Time and size of a run: wall seconds, per conversation, card memory, tokens per turn."""
    path = EVAL / f"final_{condition}_{model}_seed_{SEED}.json"
    report = json.loads(path.read_text(encoding="utf-8"))
    rows = [row for row in report["rows"] if row["arm"] == "tool_loop"]

    def mean(field: str) -> float:
        return round(sum(row[field] for row in rows) / len(rows), 1)

    return {
        "seconds": report["seconds"],
        "seconds_per_conversation": round(report["seconds"] / len(rows), 2),
        "peak_vram_gib": report["peak_vram_gib"],
        "tokens_read_per_turn": mean("tokens_read"),
        "tokens_written_per_turn": mean("tokens_written"),
        "whole_chat_tokens": mean("whole_chat_tokens"),
        "searches_per_conversation": round(sum(len(r["queries"]) for r in rows) / len(rows), 2),
    }


def behaviour(run: dict[str, dict]) -> dict:
    """Search decisions, clean first calls, runs out of calls, recall answers found by search."""
    rows = list(run.values())
    searching = [row for row in rows if row["queries"]]
    recall = [row for row in rows if row["kind"] in RECALL]
    return {
        "right_decisions": sum(bool(row["right_decision"]) for row in rows),
        "clean_calls": {
            "clean": sum(clean_call(row["first_reply"]) for row in searching),
            "of": len(searching),
        },
        "ran_out_of_calls": sum(bool(row["ran_out_of_calls"]) for row in rows),
        "recall_found_fact": sum(bool(row["found_fact"]) for row in recall),
        "recall_right_and_found": sum(right(row, retrieved_only=True) for row in recall),
    }


def right(row: dict, retrieved_only: bool) -> bool:
    return bool(row["correct"]) and (bool(row["found_fact"]) or not retrieved_only)


def recall_rule(base: dict, adapters: dict[str, dict], retrieved_only: bool) -> dict:
    """R-016's rule: pooled at least 20 points above base at each size, sign test below 0.01."""
    out, only_base, only_adapter = {"sizes": {}}, 0, 0
    for size in SIZES:
        ids = [i for i, r in base.items() if r["kind"] in RECALL and r["size"] == size]
        base_rate = sum(right(base[i], retrieved_only) for i in ids) / len(ids)
        pooled = [right(run[i], retrieved_only) for run in adapters.values() for i in ids]
        rate = sum(pooled) / len(pooled)
        out["sizes"][size] = {
            "base": round(100 * base_rate, 1),
            "adapters_pooled": round(100 * rate, 1),
            "points": round(100 * (rate - base_rate), 1),
            "pass": rate - base_rate >= 0.20,
        }
        for run in adapters.values():
            only_base += sum(
                right(base[i], retrieved_only) and not right(run[i], retrieved_only) for i in ids
            )
            only_adapter += sum(
                right(run[i], retrieved_only) and not right(base[i], retrieved_only) for i in ids
            )
    p = exact_sign_test(only_base, only_adapter)
    out["sign_test"] = {
        "only_base": only_base,
        "only_adapters": only_adapter,
        "p": p,
        "pass": p < 0.01,
    }
    out["pass"] = all(s["pass"] for s in out["sizes"].values()) and out["sign_test"]["pass"]
    return out


def coherence(condition: str) -> dict:
    """Coherent lines per model on judge 1's marks; every adapter must be at or above base."""
    counts: Counter = Counter()
    for sheet in SHEETS[condition]:
        marks_path = COHERENCE / "judge" / f"marks_{sheet}_j1.json"
        if not marks_path.exists():
            return {"status": "waiting for judge 1's marks", "missing": str(marks_path)}
        marks = json.loads(marks_path.read_text(encoding="utf-8"))
        key = json.loads((COHERENCE / f"sheet_{sheet}" / "key.json").read_text(encoding="utf-8"))
        if sorted(marks, key=int) != [str(line["line"]) for line in key]:
            raise ValueError(f"judge 1's marks on {sheet} do not cover every line")
        for line in key:
            counts[line["model"]] += marks[str(line["line"])]
    gate = {a: counts[a] >= counts["base"] for a in ADAPTERS}
    return {
        "coherent": dict(counts),
        "each_adapter_at_or_above_base": gate,
        "pass": all(gate.values()),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for condition in sys.argv[1:] or sorted(SHEETS):
        base = load(condition, "base")
        adapters = {a: load(condition, a) for a in ADAPTERS}
        if any(sorted(run) != sorted(base) for run in adapters.values()):
            raise ValueError(f"{condition}: a run scored different conversations")
        false = {
            m: sum(n for n, _ in false_retrieval(f"final_{condition}_{m}", SEED).values())
            for m in ("base",) + ADAPTERS
        }
        recall_ids = [i for i, r in base.items() if r["kind"] in RECALL]
        report = {
            "condition": condition,
            "conversations": len(base),
            "rule_1_recall": recall_rule(base, adapters, retrieved_only=False),
            "rule_2_recall_retrieved_only": recall_rule(base, adapters, retrieved_only=True),
            "rule_3_false_retrieval": {
                "counts": false,
                "pass": all(false[a] <= false["base"] for a in ADAPTERS),
            },
            "rule_4_coherence": coherence(condition),
            "per_kind_correct": {
                k: {
                    m: sum(bool(r["correct"]) for r in run.values() if r["kind"] == k)
                    for m, run in {"base": base, **adapters}.items()
                }
                for k in KINDS
            },
            "shipped_seed_82": {
                "recall": sum(bool(adapters[SHIPPED][i]["correct"]) for i in recall_ids),
                "base_recall": sum(bool(base[i]["correct"]) for i in recall_ids),
                "questions": len(recall_ids),
                "sign_test_p": exact_sign_test(
                    sum(
                        bool(base[i]["correct"]) and not adapters[SHIPPED][i]["correct"]
                        for i in recall_ids
                    ),
                    sum(
                        bool(adapters[SHIPPED][i]["correct"]) and not base[i]["correct"]
                        for i in recall_ids
                    ),
                ),
            },
            "behaviour": {m: behaviour(run) for m, run in {"base": base, **adapters}.items()},
            "cost": {m: cost(condition, m) for m in ("base",) + ADAPTERS},
            "eight_seeds_conversation_resampled_interval": bootstrap_gain_interval(
                [int(bool(base[i]["correct"])) for i in recall_ids],
                [[int(bool(run[i]["correct"])) for i in recall_ids] for run in adapters.values()],
            ),
        }
        checks = [
            report[k]["pass"] for k in report if k.startswith("rule_") and "pass" in report[k]
        ]
        report["all_rules_pass"] = (
            all(checks)
            if report["rule_4_coherence"].get("pass") is not None
            else "waiting for coherence"
        )
        (OUT / f"{condition}.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
        print(json.dumps({k: v for k, v in report.items() if k != "per_kind_correct"}, indent=1))


if __name__ == "__main__":
    main()
