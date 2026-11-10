"""R-170: the CPU pass over LongMemEval-S before any model runs on it.

Usage:
    HF_HUB_OFFLINE=1 python -I scripts/records/profile_r170.py \
        --data C:/Users/Gaming/Downloads/longmemeval/longmemeval_s_cleaned.json

Why: R-170 registered, before the scored run, a CPU pass that tokenises every question's view (the
tool arms' system prompt, the three exchanges in view and the dated question) and lists the 20
longest, so the dry run of arm 1 runs on ids this pass fixed. It also reports what the adaptation
does to the data: exchanges per question, chunks per exchange (one long exchange becomes several
passages), the turns that did not pair and were joined, the questions with an answer turn in view,
and how many questions the evidence-only arm can run (evidence sessions under 6,000 tokens). Only
the tokenizer is loaded, from the local cache. Writes aggregates and question ids only, to
results/analysis/R-170/profile.json and results/analysis/R-170/dry_run_ids.json.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

from huggingface_hub import snapshot_download
from transformers import AutoTokenizer

from aya_retrieval.harness import turns_from
from aya_retrieval.inference import prompt_tokens
from aya_retrieval.longmemeval import load_longmemeval, passages
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.provenance import REPO_ROOT, run_metadata
from aya_retrieval.tool_prompt import system_prompt_with_tools

sys.path.insert(0, str(Path(__file__).parents[1]))
from run_recall_eval import SYSTEM, SYSTEM_WITH_TOOL  # noqa: E402

OUT = REPO_ROOT / "results" / "analysis" / "R-170"
CONTEXT = 8192  # the model's context length
EVIDENCE_LIMIT = 6000  # R-170: the evidence-only arm runs on evidence sessions under this
DRY_RUN = 20


def spread(values: list[int]) -> dict:
    ordered = sorted(values)

    def at(share: float) -> int:
        return ordered[min(len(ordered) - 1, int(share * len(ordered)))]

    return {
        "n": len(ordered),
        "min": ordered[0],
        "median": statistics.median(ordered),
        "mean": round(statistics.fmean(ordered), 1),
        "p90": at(0.9),
        "p99": at(0.99),
        "max": ordered[-1],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, required=True, help="longmemeval_s_cleaned.json")
    args = parser.parse_args()

    items, digest = load_longmemeval(args.data)
    snapshot = snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(snapshot, local_files_only=True)
    with_tool = system_prompt_with_tools(SYSTEM_WITH_TOOL)

    views, evidence, chunks, exchanges, types = {}, {}, [], [], Counter()
    for item in items:
        ask = {"role": "user", "content": item.message}
        view = [{"role": "system", "content": with_tool}, *turns_from(item.view()), ask]
        views[item.item_id] = prompt_tokens(tokenizer, view)
        only = [{"role": "system", "content": SYSTEM}, *turns_from(item.evidence_exchanges), ask]
        evidence[item.item_id] = prompt_tokens(tokenizer, only)
        per_exchange = Counter(p["exchange"] for p in passages(item.older()))
        chunks += [per_exchange[i] for i in range(len(item.older()))]
        exchanges.append(len(item.exchanges))
        types[item.kind] += 1

    longest = sorted(views, key=lambda i: (-views[i], i))[:DRY_RUN]
    under = [i for i in evidence if evidence[i] < EVIDENCE_LIMIT]
    kinds = {item.item_id: item.kind for item in items}
    report = {
        "provenance": run_metadata(),
        "data_sha256": digest,
        "model": MODEL_ID,
        "model_revision": MODEL_REVISION,
        "questions": len(items),
        "types": dict(sorted(types.items())),
        "abstention": sum(item.abstention for item in items),
        "marked": sum(bool(item.evidence_indexes()) for item in items),
        "evidence_in_view": sorted(item.item_id for item in items if item.evidence_in_view()),
        "exchanges_per_question": spread(exchanges),
        "view_tokens": spread(list(views.values())),
        "views_over_context": sum(v > CONTEXT for v in views.values()),
        "views_over_6000": sum(v >= EVIDENCE_LIMIT for v in views.values()),
        "chunks_per_older_exchange": spread(chunks),
        "older_exchanges_over_one_chunk": sum(c > 1 for c in chunks),
        "older_exchanges": len(chunks),
        "turns_joined": sum(item.joined for item in items),
        "turns_joined_across_sessions": sum(item.joined_across_sessions for item in items),
        "histories_opened_by_assistant": sum(item.opened_by_assistant for item in items),
        "exchanges_from_two_sessions": sum(
            len(ids) > 1 for item in items for ids in item.session_ids
        ),
        "evidence_only_prompt_tokens": spread(list(evidence.values())),
        "evidence_only_under_6000": len(under),
        "evidence_only_under_6000_by_type": dict(sorted(Counter(kinds[i] for i in under).items())),
        "longest_views": [{"id": i, "type": kinds[i], "tokens": views[i]} for i in longest],
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "profile.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    dry = {"record": "R-170", "data_sha256": digest, "ids": longest}
    (OUT / "dry_run_ids.json").write_text(json.dumps(dry, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "provenance"}, indent=1))


if __name__ == "__main__":
    main()
