"""Scripted long conversations, each ending in one message of a known kind.

Everything is made up and generated from a seed, so a conversation can be rebuilt exactly. Most of
the conversation has left the view, so a model that sees only the last exchanges has to search.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from aya_retrieval.pools import POOLS, FactTemplate, Pool
from aya_retrieval.train_phrasings import MORE_INDIRECT, MORE_STATEMENTS

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


def build_item(
    item_id: str,
    seed: int,
    messages: int,
    kind: str,
    pool_name: str,
    decoys: int = 1,
    more_indirect: bool = False,
    more_statements: bool = False,
) -> RecallItem:
    """Return a conversation of about ``messages`` messages ending in a message of ``kind``.

    Args:
        item_id: Names the item in results.
        seed: Rebuilds the conversation exactly.
        messages: Rough length of the conversation.
        kind: One of ``ITEM_KINDS``.
        pool_name: A key of ``POOLS``.
        decoys: Facts of the same type about other people. Training varies this, because if
            the number of passages a search returns told found from not found, the model would
            never have to read them. Tests keep the default.
        more_indirect: Draw an indirect question from the template's own phrasing and those in
            ``train_phrasings.MORE_INDIRECT``, from a separate generator, so the rest of the
            conversation is the same with or without it.
        more_statements: State each fact in the template's own wording or one from
            ``train_phrasings.MORE_STATEMENTS``, drawn per line from a separate generator.
    """
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

    wordings = (template.statement,)
    if more_statements:
        wordings += MORE_STATEMENTS.get(template.statement, ())
    phraser = random.Random(seed + 3)
    fact = phraser.choice(wordings).format(relation=relation, person=person, value=answer)
    decoy_fact = phraser.choice(wordings).format(
        relation=decoy_relation, person=decoy_person, value=decoy
    )
    decoy_line = (decoy_fact, rng.choice(pool.acknowledgements))
    if decoys:
        exchanges[decoy_index] = decoy_line
    if kind != NEVER_TOLD:
        exchanges[fact_index] = (fact, rng.choice(pool.acknowledgements))

    # A separate generator, so the default conversation is the same with or without this feature.
    extras = random.Random(seed + 1)
    spare_values = [value for value in template.values if value not in (answer, decoy)]
    spare_relations = [
        r for r in pool.relations if r not in (relation, decoy_relation, other_relation)
    ]
    spare_people = [p for p in pool.people if p not in (person, decoy_person, other_person)]
    spare_slots = [slot for slot in older_slots if slot not in (fact_index, decoy_index)]
    extra_values = extras.sample(spare_values, max(decoys - 1, 0))
    for value in extra_values:
        line = phraser.choice(wordings).format(
            relation=spare_relations.pop(extras.randrange(len(spare_relations))),
            person=spare_people.pop(extras.randrange(len(spare_people))),
            value=value,
        )
        slot = spare_slots.pop(extras.randrange(len(spare_slots)))
        exchanges[slot] = (line, extras.choice(pool.acknowledgements))

    form_name = rng.choice(ASK_FORMS)
    ask_form = getattr(template, form_name)
    if more_indirect and form_name == "indirect":
        extra = MORE_INDIRECT.get(template.indirect, ())
        ask_form = random.Random(seed + 2).choice((template.indirect, *extra))
    reply = template.answer.format(relation=relation, person=person, value=answer)
    forbidden: tuple[str, ...] = (decoy, *extra_values)
    if kind == STATEMENT:
        line, reply = rng.choice(pool.statements)
        message = line.format(relation=relation, person=person)
        answer, query = "", ""
    elif kind == NEVER_TOLD:
        # Half use the confirm wording: if that wording always meant found, it would teach nothing
        # about reading the result.
        form = rng.choice((ask_form, template.confirm))
        message = form.format(relation=other_relation, person=other_person)
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


def rebuild_eval_item(row: dict, probe_seed: int, pool: str, decoys: int = 1) -> RecallItem:
    """Rebuild a results row's test item from its id, as the evaluation built it, and check it.

    Raises:
        ValueError: If the rebuilt item's message or answer differs from the row's.
    """
    size, number = int(row["id"].split("_")[0]), int(row["id"].rsplit("_", 1)[1])
    seed = probe_seed + size * 1000 + ITEM_KINDS.index(row["kind"]) * 100 + number
    item = build_item(row["id"], seed, size, row["kind"], pool, decoys)
    if item.message != row["message"] or item.answer != row["answer"]:
        raise ValueError(f"rebuilt item {row['id']} does not match the results row")
    return item
