"""Check the found-fact training answers with CuratorKIT's grounding gate and a Claude judge.

CuratorKIT's ``HallucinationGate`` asks a judge model whether each answer is supported by the source
text it came from (R-096). The organisers allow any model as a judge for validation. A Claude agent
cannot be called from Python, so the judge is plugged into CuratorKIT's own backend class
(``BaseLLM``) in two passes:

``sheet``: runs the gate with a backend that records every prompt the gate sends and answers
nothing of substance, then writes the same prompts as a judge sheet: the gate's instructions once
and each item's source text, question and answer. Every recorded prompt is checked against the
sheet, so the judge sees exactly what the gate asked.

``apply``: runs the gate again with a backend that replays the judge's answer to each prompt, so
CuratorKIT's own score parsing, threshold, rejection reasons and provenance decide the verdicts.

Usage:
    python scripts/run_curator_check.py sheet --out-dir C:/scratch/curator
    (a fresh judge writes responses.json from judge_sheet.txt)
    python scripts/run_curator_check.py apply --responses C:/scratch/curator/responses.json \
        --key C:/scratch/curator/key.json --out-dir results/curator/R-096
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from curatorkit.gates.hallucination import _DEFAULT_GROUNDING_PROMPT, HallucinationGate
from curatorkit.llm.base import BaseLLM, LLMResponse
from curatorkit.schema import DataSample

from aya_retrieval.provenance import run_metadata
from aya_retrieval.scoring import slip_shape

DATA = Path("data/screens")
SETS = {"v6": DATA / "strict_chat.jsonl", "fix17w": DATA / "fix17w.jsonl"}
THRESHOLD = 0.7  # CuratorKIT's default


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def friend_message(turns):
    return next(
        t["content"]
        for t in reversed(turns[:-1])
        if t["role"] == "user" and not t["content"].startswith("Tool result")
    )


def tool_result(turns):
    return next(
        t["content"] for t in reversed(turns[:-1]) if t["content"].startswith("Tool result")
    )


def samples() -> list[DataSample]:
    """v6's found-fact answers, and fix17w's only where it rewrote one."""
    v6 = {}
    for line in SETS["v6"].read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["kind"] in ("older", "confirm"):
            v6[row["id"]] = row
    out = [sample("v6", row) for row in v6.values()]
    for line in SETS["fix17w"].read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["id"] in v6 and row["turns"][-1]["content"] != v6[row["id"]]["turns"][-1]["content"]:
            out.append(sample("fix17w", row))
    return out


def sample(name: str, row: dict) -> DataSample:
    turns = row["turns"]
    return DataSample(
        id=f"{name}:{row['id']}",
        source_uri=f"{SETS[name].as_posix()}#{row['id']}",
        instruction=friend_message(turns),
        input=tool_result(turns),
        output=turns[-1]["content"],
        task_type="qa",
    )


class RecordLLM(BaseLLM):
    """Records each prompt the gate sends; its answers carry no verdict and are thrown away."""

    def __init__(self) -> None:
        super().__init__(model="record", temperature=0.0)
        self.prompts: set[str] = set()

    def _call(self, messages, **kwargs) -> LLMResponse:
        self.prompts.add(digest(messages[-1]["content"]))
        return LLMResponse(text='{"grounding_score": 1.0, "verdict": "grounded"}', model="record")


class ReplayLLM(BaseLLM):
    """Returns the judge's answer to each prompt the gate sends, found by the prompt's digest."""

    def __init__(self, answers: dict[str, str]) -> None:
        super().__init__(model="claude-judge-replay", temperature=0.0)
        self.answers = answers

    def _call(self, messages, **kwargs) -> LLMResponse:
        return LLMResponse(text=self.answers[digest(messages[-1]["content"])], model=self.model)


def sheet(out_dir: Path) -> None:
    items = samples()
    key = []
    for n, s in enumerate(items):
        prompt = _DEFAULT_GROUNDING_PROMPT.format(
            source_text=s.input, question=s.instruction, answer=s.output
        )
        key.append({"item": n, "id": s.id, "digest": digest(prompt)})
    recorder = RecordLLM()
    HallucinationGate(recorder, threshold=THRESHOLD, concurrency=1).run(items)
    if recorder.prompts != {k["digest"] for k in key}:
        raise SystemExit("the gate's prompts differ from the judge sheet")
    head, _, rest = _DEFAULT_GROUNDING_PROMPT.partition("Source text:")
    instructions = rest.split("Answer: {answer}", 1)[1].replace("{{", "{").replace("}}", "}")
    lines = [
        head.strip(),
        "Each ITEM below gives the source text, the question and the answer. Evaluate each item "
        "as these instructions say:",
        instructions.strip(),
        "Write one JSON object for the whole sheet, item number to that item's JSON verdict.",
        "",
    ]
    for n, s in enumerate(items):
        lines += [f"ITEM {n}", "Source text:", s.input, f"Question: {s.instruction}"]
        lines += [f"Answer: {s.output}", ""]
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "judge_sheet.txt").write_text("\n".join(lines), encoding="utf-8")
    (out_dir / "key.json").write_text(json.dumps(key, indent=1), encoding="utf-8")
    print(f"{len(items)} items; the gate's {len(recorder.prompts)} prompts match the sheet")


def apply(responses: Path, key_path: Path, out_dir: Path) -> None:
    key = json.loads(key_path.read_text(encoding="utf-8"))
    judged = json.loads(responses.read_text(encoding="utf-8"))
    answers = {k["digest"]: json.dumps(judged[str(k["item"])]) for k in key}
    items = samples()
    passed, rejected = HallucinationGate(
        ReplayLLM(answers), threshold=THRESHOLD, concurrency=1
    ).run(items)
    by_id = {s.id: s for s in items}
    rows = []
    for r in rejected:
        s = by_id[r.id]
        rows.append(
            {
                "id": r.id,
                "reason": r.rejection_reason,
                "slip_shape": slip_shape(s.output, s.instruction),
                "question": s.instruction,
                "answer": s.output,
            }
        )
    slips = {s.id for s in items if slip_shape(s.output, s.instruction)}
    caught = slips & {r["id"] for r in rows}
    summary = {
        "provenance": run_metadata(),
        "toolkit": "CuratorKIT HallucinationGate, default prompt, threshold 0.7",
        "judge": "Claude (Sonnet) agent, answers replayed through a CuratorKIT BaseLLM backend",
        "items": len(items),
        "passed": len(passed),
        "rejected": len(rejected),
        "rejected_by_set": {n: sum(r["id"].startswith(n + ":") for r in rows) for n in SETS},
        "slip_shaped": len(slips),
        "slip_shaped_rejected": len(caught),
        "rejected_not_slip_shaped": sum(not r["slip_shape"] for r in rows),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "rejected.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print({k: v for k, v in summary.items() if k != "provenance"})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="step", required=True)
    s = sub.add_parser("sheet")
    s.add_argument("--out-dir", type=Path, required=True)
    a = sub.add_parser("apply")
    a.add_argument("--responses", type=Path, required=True)
    a.add_argument("--key", type=Path, required=True)
    a.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    if args.step == "sheet":
        sheet(args.out_dir)
    else:
        apply(args.responses, args.key, args.out_dir)


if __name__ == "__main__":
    main()
