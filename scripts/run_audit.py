"""Score results files again with AuditKIT and compare each adapter with base (R-030).

Usage:
    python scripts/run_audit.py --probe-seed 73157 --pool probe --base probe2_base
        --adapters probe4_tuned82 probe4_tuned83 probe4_tuned84 --name v3_probe

Writes ``results/audit/<name>.json``: per label, AuditKIT's verified successes by kind, the cases
where AuditKIT and our scorer disagree, AuditKIT's diagnostics, and for each adapter a sign test
and a centred paired bootstrap against base on every case and on the recall kinds (R-031).
"""

from __future__ import annotations

import argparse
import json
from collections import Counter

from aya_retrieval.audit import audit_rows, compare, verified
from aya_retrieval.provenance import REPO_ROOT, require_clean_tree, run_metadata
from aya_retrieval.report_data import KINDS, RECALL_KINDS, eval_rows

OUT_DIR = REPO_ROOT / "results" / "audit"


def summarize(rows: list[dict], result) -> dict:
    success = verified(result)
    by_kind = {k: [0, 0] for k in KINDS}
    for row in rows:
        by_kind[row["kind"]][0] += int(success[row["id"]])
        by_kind[row["kind"]][1] += 1
    disagree = [
        {
            "id": r["id"],
            "ours": bool(r["correct"]),
            "auditkit": bool(success[r["id"]]),
            "reply": r["reply"],
        }
        for r in rows
        if bool(r["correct"]) != bool(success[r["id"]])
    ]
    statuses = Counter(r.status for r in result.rows)
    diagnostics = Counter()
    for r in result.rows:
        for name, value in r.diagnostics.items():
            if isinstance(value, dict) and "value" in value and value["value"] is not None:
                diagnostics[f"{name}_sum"] += float(value["value"])
                diagnostics[f"{name}_n"] += 1
    return {
        "verified_by_kind": {k: tuple(v) for k, v in by_kind.items()},
        "verified": sum(success.values()),
        "cases": len(rows),
        "disagreements_with_our_scorer": disagree,
        "statuses": dict(statuses),
        "diagnostics": dict(diagnostics),
        "summary": result.summary(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--probe-seed", type=int, required=True)
    parser.add_argument("--pool", required=True)
    parser.add_argument("--base", required=True, help="results label of the untrained model")
    parser.add_argument("--adapters", nargs="+", required=True, help="results labels of adapters")
    parser.add_argument("--name", required=True, help="names the output file")
    parser.add_argument("--allow-dirty", action="store_true", help="development runs only")
    args = parser.parse_args()
    require_clean_tree(args.allow_dirty)

    report = {
        "provenance": run_metadata(),
        "probe_seed": args.probe_seed,
        "pool": args.pool,
        "labels": {},
    }
    successes = {}
    for label in [args.base, *args.adapters]:
        rows = eval_rows(label, args.probe_seed)
        result = audit_rows(rows, args.probe_seed, args.pool)
        successes[label] = verified(result)
        report["labels"][label] = summarize(rows, result)
        print(label, report["labels"][label]["verified"], "of", len(rows))
    recall_ids = {
        r["id"] for r in eval_rows(args.base, args.probe_seed) if r["kind"] in RECALL_KINDS
    }
    base = successes[args.base]
    report["bootstrap"] = {
        label: {
            "all_kinds": compare(base, successes[label]),
            "recall_kinds": compare(
                {i: v for i, v in base.items() if i in recall_ids},
                {i: v for i, v in successes[label].items() if i in recall_ids},
            ),
        }
        for label in args.adapters
    }
    for label, test in report["bootstrap"].items():
        print(label, test)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"{args.name}.json"
    out.write_text(json.dumps(report, indent=1), encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
