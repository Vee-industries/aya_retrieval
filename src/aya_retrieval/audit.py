"""Score recorded replies again with AuditKIT's agent evaluation, as a check on our own scorer.

Each results row becomes an AuditKIT episode: the friend's message, one search call per query the
model made, and its final reply. Search results were not kept, so AuditKIT marks them unavailable.
The outcome of each case comes from an AuditKIT oracle:

- ``older``, ``confirm``, ``in_view``: AuditKIT's ``AnswerAssertion`` in ``contains`` mode, which
  matches the planted answer on word boundaries. Our scorer matches any substring and also fails
  a reply that names a wrong value, so the two can disagree, and the disagreements are reported.
- ``never_told``: a ``CustomPredicate`` that the reply names no value of that kind.
- ``statement``: a ``CustomPredicate`` that the episode holds no tool call.

Base and adapter are then compared with AuditKIT's paired bootstrap on these outcomes.
"""

from __future__ import annotations

import json

from auditkit._bootstrap import paired_bootstrap
from auditkit.agent_eval import (
    AgentCase,
    AgentEvalRunner,
    AgentEvalSpec,
    AnswerAssertion,
    CustomPredicate,
    episode_from_openai_messages,
)

from aya_retrieval.conversations import ITEM_KINDS, NEVER_TOLD, STATEMENT, RecallItem, build_item
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME

ORACLE_VERSION = "1"
DIAGNOSTICS = ["tool_call_validity", "redundant_tool_calls"]


def rebuild_item(row: dict, probe_seed: int, pool: str) -> RecallItem:
    """Rebuild a row's test item from its id, as the evaluation built it, and check it matches."""
    size, number = int(row["id"].split("_")[0]), int(row["id"].rsplit("_", 1)[1])
    seed = probe_seed + size * 1000 + ITEM_KINDS.index(row["kind"]) * 100 + number
    item = build_item(row["id"], seed, size, row["kind"], pool)
    if item.message != row["message"] or item.answer != row["answer"]:
        raise ValueError(f"rebuilt item {row['id']} does not match the results row")
    return item


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
    """AuditKIT's paired bootstrap of adapter against base, paired by case id."""
    pairs = [(base[i], adapter[i]) for i in sorted(base.keys() & adapter.keys())]
    return paired_bootstrap(pairs, n_resamples=10_000, seed=0)
