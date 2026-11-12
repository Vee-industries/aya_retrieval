"""Scripted long conversations, each ending in one message of a known kind.

Everything is made up and generated from a seed, so a conversation can be rebuilt exactly. Most of
the conversation has left the view, so a model that sees only the last exchanges has to search.
"""

from __future__ import annotations

import dataclasses
import random
import re
from dataclasses import dataclass

from aya_retrieval.pools import POOLS, FactTemplate, Pool
from aya_retrieval.train_phrasings import MORE_CHAT, MORE_INDIRECT, MORE_STATEMENTS

EXCHANGES_IN_VIEW = 3
ASK_FORMS = ("same_words", "new_words", "indirect")

OLDER = "older"
CONFIRM = "confirm"
IN_VIEW = "in_view"
NEVER_TOLD = "never_told"
STATEMENT = "statement"
ITEM_KINDS = (OLDER, CONFIRM, IN_VIEW, NEVER_TOLD, STATEMENT)
NEEDS_SEARCH = (OLDER, CONFIRM, NEVER_TOLD)
# Where the passages a search returns come from in a chat with facts of other types (F2, R-178):
# same-type facts about other people, other-type facts about the asked person, or a small-talk
# line that shares an ordinary word with the search.
OTHER_FACT_SHARES = ("same_type", "same_person", "shared_word")


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
    more_chat: bool = False,
    force_indirect: bool = False,
    chat_line: tuple[str, str] | None = None,
    fact_type: str | None = None,
    other_facts: str | None = None,
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
        more_chat: Draw a ``statement`` item's line from the pool's own and
            ``train_phrasings.MORE_CHAT``, from a separate generator.
        force_indirect: Ask in the indirect form whatever the draw; the draw is still made, so
            the rest of the conversation is unchanged.
        chat_line: A ``statement`` item's line and reply, in place of the drawn one; the draw is
            still made, so the rest of the conversation is unchanged.
        fact_type: A key of the pool's facts, in place of the drawn one; the draw is still made.
        other_facts: One of ``OTHER_FACT_SHARES``: add facts of other types out of view, as
            ``add_other_facts`` does, from a separate generator, so the rest of the conversation
            is the same with or without it. None, the default, adds none.
    """
    pool = POOLS[pool_name]
    rng = random.Random(seed)
    template = pool.facts[rng.choice(sorted(pool.facts))]
    if fact_type:
        template = pool.facts[fact_type]
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
    if force_indirect:
        form_name = "indirect"
    ask_form = getattr(template, form_name)
    if more_indirect and form_name == "indirect":
        extra = MORE_INDIRECT.get(template.indirect, ())
        ask_form = random.Random(seed + 2).choice((template.indirect, *extra))
    reply = template.answer.format(relation=relation, person=person, value=answer)
    forbidden: tuple[str, ...] = (decoy, *extra_values)
    if kind == STATEMENT:
        line, reply = rng.choice(pool.statements)
        if more_chat:
            line, reply = random.Random(seed + 4).choice((*pool.statements, *MORE_CHAT))
        if chat_line:
            line, reply = chat_line
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

    item = RecallItem(
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
    if other_facts:
        asked = (other_relation, other_person) if kind == NEVER_TOLD else (relation, person)
        item = add_other_facts(item, seed, pool_name, other_facts, asked)
    return item


def _words(text: str) -> set[str]:
    """Return the words of ``text``, lower case; a possessive's name counts as the name."""
    return set(re.findall(r"[a-z]+", text.casefold()))


def add_other_facts(
    item: RecallItem, seed: int, pool_name: str, share: str, asked: tuple[str, str]
) -> RecallItem:
    """Return ``item`` with 2 to 4 facts of other types in free out-of-view slots (F2, R-178).

    The first added type is stated twice, about two people, so the chat holds another value of
    that type. A free slot is an out-of-view exchange whose friend line names no value of the
    pool, so no fact, decoy or correction is overwritten. New people are ones the chat never
    names. Nothing scored changes: answer, forbidden values, query and reply stay as they were.

    Args:
        item: The conversation.
        seed: Draws the facts, from its own generator.
        pool_name: A key of ``POOLS``.
        share: One of ``OTHER_FACT_SHARES``. ``same_person``: the first fact, and about half of
            the rest, are about ``asked``. ``same_type`` and ``shared_word``: none is about
            ``asked``; ``shared_word`` also adds a small-talk line about the last word of the
            item's query that is not a name, ends in no "ed" and has three letters or more.
        asked: The relation and person the final message is about.
    """
    if share not in OTHER_FACT_SHARES:
        raise ValueError(f"unknown share {share!r}")
    rng = random.Random(seed + 7)
    pool = POOLS[pool_name]
    own = next(name for name, t in sorted(pool.facts.items()) if item.decoy in t.values)
    values = [v for t in pool.facts.values() for v in t.values]
    exchanges = list(item.exchanges)
    older = len(exchanges) - EXCHANGES_IN_VIEW
    free = [
        i
        for i in range(older)
        if i != item.fact_index and not any(v in exchanges[i][0] for v in values)
    ]
    said = _words(" ".join([item.message, *(u + " " + r for u, r in exchanges)]))
    people = [p for p in pool.people if p.casefold() not in said and p != asked[1]]
    unsaid = [r for r in pool.relations if r.casefold() not in said and r != asked[0]]
    reused = [r for r in pool.relations if r != asked[0]]

    count = rng.randint(2, 4)
    types = rng.sample([name for name in sorted(pool.facts) if name != own], count - 1)
    pair = rng.sample(pool.facts[types[0]].values, 2)
    plan = [(types[0], pair[0]), (types[0], pair[1])]
    plan += [(name, rng.choice(pool.facts[name].values)) for name in types[1:]]
    lines = []
    for index, (name, value) in enumerate(plan):
        # The second fact of the stated-twice type is always about someone else.
        about_asked = share == "same_person" and index != 1 and (index == 0 or rng.random() < 0.5)
        if about_asked:
            relation, person = asked
        elif people:
            # A relation the chat never names while one is left, then any but the asked one.
            relation = unsaid.pop(rng.randrange(len(unsaid))) if unsaid else rng.choice(reused)
            person = people.pop(rng.randrange(len(people)))
        else:
            continue
        line = pool.facts[name].statement.format(relation=relation, person=person, value=value)
        lines.append((line, rng.choice(pool.acknowledgements)))
    if share == "shared_word":
        names = {w.casefold() for w in (*pool.people, *pool.relations)}
        ordinary = [
            w
            for w in item.query.casefold().split()
            if w not in names and not w.endswith("ed") and len(w) >= 3
        ]
        if ordinary:
            mood = rng.choice(pool.moods)
            subject = f"the {ordinary[-1]}"
            reply = rng.choice(mood.replies).format(subject=subject)
            lines.append(
                (rng.choice(mood.user_lines).format(subject=subject), reply[0].upper() + reply[1:])
            )
    for slot, line in zip(rng.sample(free, min(len(free), len(lines))), lines, strict=False):
        exchanges[slot] = line
    return dataclasses.replace(item, exchanges=tuple(exchanges))


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
