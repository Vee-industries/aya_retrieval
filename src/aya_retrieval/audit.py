"""Score recorded replies again with AuditKIT's agent evaluation, as a check on our own scorer.

Each results row becomes an AuditKIT episode: the friend's message, one search call per query the
model made, and its final reply. Search results were not kept, so AuditKIT marks them unavailable.
The outcome of each case comes from an AuditKIT oracle:

- ``older``, ``confirm``, ``in_view``: AuditKIT's ``AnswerAssertion`` in ``contains`` mode, which
  matches the planted answer on word boundaries. Our scorer matches any substring and also fails
  a reply that names a wrong value, so the two can disagree, and the disagreements are reported.
- ``never_told``: a ``CustomPredicate`` that the reply names no value of that kind.
- ``statement``: a ``CustomPredicate`` that the episode holds no tool call.

Base and adapter are then compared on these outcomes with an exact sign test and a centred paired
bootstrap (``aya_retrieval.stats``). AuditKIT's own paired bootstrap is not used: in 1.1.3 it does
not centre its resamples, so a gain on every case reads as p = 1 (R-031).
"""

from __future__ import annotations

import json

from auditkit.agent_eval import (
    AgentCase,
    AgentEvalRunner,
    AgentEvalSpec,
    AnswerAssertion,
    CustomPredicate,
    episode_from_openai_messages,
)

from aya_retrieval.conversations import NEVER_TOLD, STATEMENT, RecallItem, rebuild_eval_item
from aya_retrieval.stats import exact_sign_test, paired_bootstrap
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME

ORACLE_VERSION = "1"
DIAGNOSTICS = ["tool_call_validity", "redundant_tool_calls"]


def rebuild_item(row: dict, probe_seed: int, pool: str, decoys: int = 1) -> RecallItem:
    """Rebuild a row's test item from its id, as the evaluation built it, and check it matches."""
    return rebuild_eval_item(row, probe_seed, pool, decoys)


def episode_for(row: dict):
    """The row's recorded turn as an AuditKIT episode."""
    messages = [{"role": "user", "content": row["message"]}]
    for i, query in enumerate(row["queries"]):
        call = {
            "id": f"c{i}",
            "type": "function",
            "function": {"name": SEARCH_TOOL_NAME, "arguments": json.dumps({"query": query})},
        }
        messages.append({"role": "assistant", "content": None, "tool_calls": [call]})
    messages.append({"role": "assistant", "content": row["reply"]})
    return episode_from_openai_messages(messages, case_id=row["id"], final_answer=row["reply"])


def names_no_value(forbidden: tuple[str, ...]):
    """Predicate: the final reply names none of ``forbidden``."""

    def check(episode, case) -> bool:
        text = (episode.final_answer or "").casefold()
        return not any(value.casefold() in text for value in forbidden)

    return check


def made_no_call(episode, case) -> bool:
    """Predicate: the episode holds no tool call."""
    return not episode.tool_call_events()


def case_for(row: dict, item: RecallItem) -> AgentCase:
    """The AuditKIT case for one row, with the oracle for its kind."""
    if row["kind"] == NEVER_TOLD:
        outcome = CustomPredicate(
            names_no_value(item.forbidden), version=ORACLE_VERSION, name="names_no_value"
        )
    elif row["kind"] == STATEMENT:
        outcome = CustomPredicate(made_no_call, version=ORACLE_VERSION, name="made_no_call")
    else:
        outcome = AnswerAssertion(item.answer, mode="contains")
    return AgentCase(
        id=row["id"],
        task=row["message"],
        category=row["kind"],
        allowed_tools=[SEARCH_TOOL_NAME],
        outcome=outcome,
    )


def audit_rows(rows: list[dict], probe_seed: int, pool: str):
    """Run AuditKIT's recorded-mode agent evaluation over results rows."""
    cases = [case_for(row, rebuild_item(row, probe_seed, pool)) for row in rows]
    episodes = [episode_for(row) for row in rows]
    spec = AgentEvalSpec(cases=cases, mode="recorded", episodes=episodes, scorers=DIAGNOSTICS)
    return AgentEvalRunner().run(spec)


def verified(result) -> dict[str, float]:
    """Per case id, 1.0 for a verified success and 0.0 for anything else."""
    return {r.case_id: float(r.outcome["verdict"] == "success") for r in result.rows}


def compare(base: dict[str, float], adapter: dict[str, float]) -> dict:
    """Adapter against base on the same cases, paired by case id: sign test and bootstrap."""
    ids = sorted(base.keys() & adapter.keys())
    pairs = [(base[i], adapter[i]) for i in ids]
    only_base = sum(b > a for b, a in pairs)
    only_adapter = sum(a > b for b, a in pairs)
    return {
        "only_base": only_base,
        "only_adapter": only_adapter,
        "sign_test_p": exact_sign_test(only_base, only_adapter),
        "bootstrap": paired_bootstrap(pairs),
    }
