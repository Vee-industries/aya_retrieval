"""Scripted long conversations, each ending in one message of a known kind.

Everything is made up and generated from a seed, so a conversation can be rebuilt exactly. Most of
the conversation has left the view, so a model that sees only the last exchanges has to search.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from aya_retrieval.pools import POOLS, FactTemplate, Pool

EXCHANGES_IN_VIEW = 3
ASK_FORMS = ("same_words", "new_words", "indirect")

OLDER = "older"
CONFIRM = "confirm"
IN_VIEW = "in_view"
NEVER_TOLD = "never_told"
STATEMENT = "statement"
ITEM_KINDS = (OLDER, CONFIRM, IN_VIEW, NEVER_TOLD, STATEMENT)
NEEDS_SEARCH = (OLDER, CONFIRM, NEVER_TOLD)


@dataclass(frozen=True)
class RecallItem:
    """One conversation and the message that ends it."""

    item_id: str
    kind: str
    exchanges: tuple[tuple[str, str], ...]
    message: str
    answer: str
    decoy: str
    forbidden: tuple[str, ...]
    fact_index: int
    query: str
    reply: str

    def view(self) -> tuple[tuple[str, str], ...]:
        """Return the exchanges that stay in view."""
        return self.exchanges[-EXCHANGES_IN_VIEW:]

    def older(self) -> tuple[tuple[str, str], ...]:
        """Return the exchanges outside the view, reachable only by searching."""
        return self.exchanges[:-EXCHANGES_IN_VIEW]


def _small_talk(rng: random.Random, pool: Pool) -> tuple[str, str]:
    mood = rng.choice(pool.moods)
    subject = rng.choice(pool.subjects)
    user = rng.choice(mood.user_lines).format(subject=subject)
    reply = rng.choice(mood.replies).format(subject=subject)
    return user, reply[0].upper() + reply[1:]


def _query(template: FactTemplate, message: str, relation: str, person: str) -> str:
    """Return the search a good reply would make, using only names the message gives it."""
    return template.query.format(who=person if person in message else relation)


def build_item(item_id: str, seed: int, messages: int, kind: str, pool_name: str) -> RecallItem:
    """Return a conversation of about ``messages`` messages ending in a message of ``kind``."""
    pool = POOLS[pool_name]
    rng = random.Random(seed)
    template = pool.facts[rng.choice(sorted(pool.facts))]
    answer, decoy = rng.sample(template.values, 2)
    relation, decoy_relation, other_relation = rng.sample(pool.relations, 3)
    person, decoy_person, other_person = rng.sample(pool.people, 3)

    exchange_count = max(messages // 2, EXCHANGES_IN_VIEW + 3)
    exchanges = [_small_talk(rng, pool) for _ in range(exchange_count)]
    older_slots = range(exchange_count - EXCHANGES_IN_VIEW)
    fact_index, decoy_index = rng.sample(older_slots, 2)
    if kind == IN_VIEW:
        fact_index = exchange_count - rng.randint(1, EXCHANGES_IN_VIEW)

    fact = template.statement.format(relation=relation, person=person, value=answer)
    decoy_fact = template.statement.format(
        relation=decoy_relation, person=decoy_person, value=decoy
    )
    exchanges[decoy_index] = (decoy_fact, rng.choice(pool.acknowledgements))
    if kind != NEVER_TOLD:
        exchanges[fact_index] = (fact, rng.choice(pool.acknowledgements))

    ask_form = getattr(template, rng.choice(ASK_FORMS))
    reply = template.answer.format(relation=relation, person=person, value=answer)
    forbidden: tuple[str, ...] = (decoy,)
    if kind == STATEMENT:
        line, reply = rng.choice(pool.statements)
        message = line.format(relation=relation, person=person)
        answer, query = "", ""
    elif kind == NEVER_TOLD:
        message = ask_form.format(relation=other_relation, person=other_person)
        query = _query(template, message, other_relation, other_person)
        reply = rng.choice(pool.unknown_replies)
        forbidden, answer = tuple(template.values), ""
    else:
        form = template.confirm if kind == CONFIRM else ask_form
        message = form.format(relation=relation, person=person)
        query = _query(template, message, relation, person)

    return RecallItem(
        item_id=item_id,
        kind=kind,
        exchanges=tuple(exchanges),
        message=message,
        answer=answer,
        decoy=decoy,
        forbidden=forbidden,
        fact_index=fact_index,
        query=query,
        reply=reply,
    )
