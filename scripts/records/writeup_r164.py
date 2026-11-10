"""R-164: the numbers the write-up cites that no committed analysis held yet.

Usage: python scripts/records/writeup_r164.py

Why: R-164's panel found claims in the planned write-up with no results file behind them. This
computes them from the raw runs in ``results/recall_eval`` and writes
``results/analysis/R-164/writeup_numbers.json``:

- the prompted-baseline control on both outside-writer sets (R-146, R-161): recall and each kind for
  base, prompt A and prompt B, and seed 82 against each prompt by exact sign test;
- tag questions on both sets (R-158, R-159): of the ``confirm`` questions, the ones whose message
  claims the right value and the ones that claim a wrong value, and how often each model is right on
  each; a claim is true when the message contains the answer;
- every 6.37 seed present on each set, so seed 82 can be shown beside the others;
- ``hard_dev`` recall for base and seed 82 (the +265% in the README);
- the whole-chat control registered in R-164, for each run that has finished: base with every
  message in view against base and seed 82 with the tool, on the same conversations, at each size.
"""

from __future__ import annotations

import json
from pathlib import Path

from aya_retrieval.stats import exact_sign_test

EVAL = Path("results/recall_eval")
OUT = Path("results/analysis/R-164")
RECALL = ("older", "confirm")
KINDS = ("older", "confirm", "in_view", "never_told", "statement")
SEEDS = (82, 83, 94, 95, 96, 97, 98, 99)
SETS = {"set_1": ("blind", "0"), "set_2": ("blind2", "0")}
WHOLE_CHAT = {
    "set_1": ("wc_blind_base_seed_0", "blind_base_seed_0", "blind_fix17cs37_82_seed_0"),
    "set_2": ("wc_blind2_base_seed_0", "blind2_base_seed_0", "blind2_fix17cs37_82_seed_0"),
    "hard_dev": ("wc_hd_base_seed_73157", "hd_base_seed_73157", "hd_fix17cs37_82_seed_73157"),
    "probe": (
        "wc_probe_base_seed_73157",
        "probe2_base_seed_73157",
        "probe_fix17cs37_82_seed_73157",
    ),
}


def rows(name: str, arm: str) -> dict[str, dict] | None:
    path = EVAL / f"{name}.json"
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    return {row["id"]: row for row in report["rows"] if row["arm"] == arm}


def recall_ids(run: dict[str, dict], size: int | None = None) -> list[str]:
    return sorted(
        i for i, r in run.items() if r["kind"] in RECALL and (size is None or r["size"] == size)
    )


def kinds(run: dict[str, dict]) -> dict[str, int]:
    return {k: sum(bool(r["correct"]) for r in run.values() if r["kind"] == k) for k in KINDS}


def versus(first: dict[str, dict], second: dict[str, dict], ids: list[str]) -> dict:
    """How often each of two runs alone is right on the same questions, and the sign test."""
    only_first = sum(bool(first[i]["correct"]) and not second[i]["correct"] for i in ids)
    only_second = sum(bool(second[i]["correct"]) and not first[i]["correct"] for i in ids)
    return {
        "only_first": only_first,
        "only_second": only_second,
        "p": exact_sign_test(only_first, only_second),
    }


def claims(run: dict[str, dict]) -> dict:
    """Tag questions split by whether the friend's claimed value is the right one."""
    confirm = [r for r in run.values() if r["kind"] == "confirm"]
    true = [r for r in confirm if r["answer"].casefold() in r["message"].casefold()]
    false = [r for r in confirm if r["answer"].casefold() not in r["message"].casefold()]
    return {
        "true_claims": len(true),
        "right_on_true": sum(bool(r["correct"]) for r in true),
        "false_claims": len(false),
        "corrected_false": sum(bool(r["correct"]) for r in false),
        "searched": sum(bool(r["queries"]) for r in confirm),
    }


def outside_writer_sets() -> dict:
    out = {}
    for name, (prefix, seed) in SETS.items():
        base = rows(f"{prefix}_base_seed_{seed}", "tool_loop")
        ship = rows(f"{prefix}_fix17cs37_82_seed_{seed}", "tool_loop")
        ids = recall_ids(base)
        entry = {"questions": len(ids), "models": {}, "prompt_control": {}}
        for label in ("base", "base_prompta", "base_promptb"):
            run = rows(f"{prefix}_{label}_seed_{seed}", "tool_loop")
            entry["models"][label] = {
                "recall": sum(bool(run[i]["correct"]) for i in ids),
                "kinds": kinds(run),
                "claims": claims(run),
            }
            if label != "base":
                entry["prompt_control"][f"{label}_vs_seed_82"] = versus(run, ship, ids)
        for s in SEEDS:
            run = rows(f"{prefix}_fix17cs37_{s}_seed_{seed}", "tool_loop")
            if run is None:
                continue
            entry["models"][f"seed_{s}"] = {
                "recall": sum(bool(run[i]["correct"]) for i in ids),
                "kinds": kinds(run),
                "claims": claims(run),
                "vs_base": versus(base, run, ids),
            }
        out[name] = entry
    return out


def hard_dev() -> dict:
    base = rows("hd_base_seed_73157", "tool_loop")
    ship = rows("hd_fix17cs37_82_seed_73157", "tool_loop")
    ids = recall_ids(base)
    return {
        "questions": len(ids),
        "base": sum(bool(base[i]["correct"]) for i in ids),
        "seed_82": sum(bool(ship[i]["correct"]) for i in ids),
        "vs_base": versus(base, ship, ids),
    }


def whole_chat() -> dict:
    out = {}
    for name, (wc_name, base_name, ship_name) in WHOLE_CHAT.items():
        whole = rows(wc_name, "whole_chat")
        if whole is None:
            out[name] = {"status": f"not run yet: {wc_name}"}
            continue
        base, ship = rows(base_name, "tool_loop"), rows(ship_name, "tool_loop")
        entry = {}
        for size in sorted({r["size"] for r in whole.values()}):
            ids = recall_ids(whole, size)
            if not ids:
                continue
            entry[str(size)] = {
                "questions": len(ids),
                "whole_chat_base": sum(bool(whole[i]["correct"]) for i in ids),
                "tool_base": sum(bool(base[i]["correct"]) for i in ids),
                "tool_seed_82": sum(bool(ship[i]["correct"]) for i in ids),
                "whole_chat_vs_seed_82": versus(whole, ship, ids),
                "tokens_read_per_turn": {
                    "whole_chat_base": round(sum(whole[i]["tokens_read"] for i in ids) / len(ids)),
                    "tool_seed_82": round(sum(ship[i]["tokens_read"] for i in ids) / len(ids)),
                },
            }
        entry["kinds_whole_chat_base"] = kinds(whole)
        out[name] = entry
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {
        "outside_writer_sets": outside_writer_sets(),
        "hard_dev": hard_dev(),
        "whole_chat_control": whole_chat(),
    }
    path = OUT / "writeup_numbers.json"
    path.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
