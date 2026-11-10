"""R-168: score R-016's two references on the sealed pools against base and the 6.37 adapters.

Usage: python scripts/records/refs_r168.py

Why: R-016 registered ``whole_chat`` and ``always_search`` as references reported beside the rules;
the sealed run (R-162) ran neither (R-167). R-168 ran them late, base only, on the same sealed
conversations: the whole chat (``whole_chat_all``, every kind) at 58 messages only, since it does
not fit under the memory cap at 419 (R-166), and code that searches first on every turn
(``always_search``) at both sizes. This reports, per condition, size and kind, correct answers for
each reference beside base with the tool, seed 82 and the eight adapters pooled (from the R-162
runs), with exact sign tests of seed 82 against each reference on recall (``older`` and
``confirm``), false retrievals, and searches per kind. ``statement`` is scored on the call count,
so it is right by construction for the whole chat and wrong by construction for ``always_search``;
it is reported, not read. Writes results/analysis/R-168/refs.json.
"""

from __future__ import annotations

import json
from pathlib import Path

from aya_retrieval.report_data import false_retrieval
from aya_retrieval.stats import exact_sign_test

EVAL = Path("results/recall_eval")
OUT = Path("results/analysis/R-168")
SEED = 90311
ADAPTERS = tuple(f"fix17cs37_{s}" for s in (82, 83, 94, 95, 96, 97, 98, 99))
SHIPPED = "fix17cs37_82"
KINDS = ("older", "confirm", "in_view", "never_told", "statement")
RECALL = ("older", "confirm")
REFERENCES = {"whole_chat": ("wca", "whole_chat_all"), "always_search": ("as", "always_search")}


def rows(label: str, arm: str) -> dict[str, dict]:
    report = json.loads((EVAL / f"{label}_seed_{SEED}.json").read_text(encoding="utf-8"))
    return {row["id"]: row for row in report["rows"] if row["arm"] == arm}


def right(run: dict[str, dict], ids: list[str]) -> int:
    return sum(bool(run[i]["correct"]) for i in ids)


def versus(first: dict[str, dict], second: dict[str, dict], ids: list[str]) -> dict:
    only_first = sum(bool(first[i]["correct"]) and not second[i]["correct"] for i in ids)
    only_second = sum(bool(second[i]["correct"]) and not first[i]["correct"] for i in ids)
    p = exact_sign_test(only_first, only_second)
    return {"only_first": only_first, "only_second": only_second, "p": p}


def condition(name: str) -> dict:
    tool_base = rows(f"final_{name}_base", "tool_loop")
    adapters = {a: rows(f"final_{name}_{a}", "tool_loop") for a in ADAPTERS}
    out = {}
    for reference, (short, arm) in REFERENCES.items():
        label = f"ref_{name}_base_{short}"
        ref = rows(label, arm)
        false = false_retrieval(label, SEED, arm)
        entry = {"false_retrievals": sum(n for n, _ in false.values()), "sizes": {}}
        for size in sorted({r["size"] for r in ref.values()}):
            ids_size = [i for i in ref if ref[i]["size"] == size]
            recall = sorted(i for i in ids_size if ref[i]["kind"] in RECALL)
            kinds = {}
            for kind in KINDS:
                ids = sorted(i for i in ids_size if ref[i]["kind"] == kind)
                kinds[kind] = {
                    "of": len(ids),
                    "reference": right(ref, ids),
                    "base_tool": right(tool_base, ids),
                    "seed_82": right(adapters[SHIPPED], ids),
                    "adapters_mean": round(sum(right(a, ids) for a in adapters.values()) / 8, 1),
                    "reference_searched": sum(bool(ref[i]["queries"]) for i in ids),
                }
            entry["sizes"][str(size)] = {
                "recall": {
                    "of": len(recall),
                    "reference": right(ref, recall),
                    "base_tool": right(tool_base, recall),
                    "seed_82": right(adapters[SHIPPED], recall),
                    "adapters": {a: right(run, recall) for a, run in adapters.items()},
                    "reference_vs_seed_82": versus(ref, adapters[SHIPPED], recall),
                },
                "kinds": kinds,
            }
        out[reference] = entry
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    report = {c: condition(c) for c in "ABCD"}
    (OUT / "refs.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
