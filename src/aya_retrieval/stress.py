"""Harder versions of a test conversation, for development checks (R-067).

Each takes a built ``RecallItem`` and returns a changed copy, so any pool can be tested this way
without writing a new one. The kinds of difficulty come from the failure categories another chat
project tracked (its categories only; none of its text): how a real user types, and facts that are
corrected later. One comes from this project's own demo chat: a question asked right after another.

``phone_style`` is held out of training (R-099): it is the measure for training on messy chats, so
no training row may be built with it.
"""

from __future__ import annotations

import dataclasses
import random
import re

from aya_retrieval.conversations import ASK_FORMS, CONFIRM, EXCHANGES_IN_VIEW, OLDER, RecallItem
from aya_retrieval.pools import POOLS

# Contractions typed without the apostrophe, as many people text.
_CONTRACTIONS = re.compile(r"\b(\w+)'(t|s|m|re|ll|ve|d)\b")
# Phone texting habits ``typed`` never applies (R-099): "u" and "ur" for "you" and "your".
_SHORT_FORMS = (
    (re.compile(r"\byou\b", re.IGNORECASE), "u"),
    (re.compile(r"\byour\b", re.IGNORECASE), "ur"),
)
_LONG_WORD = re.compile(r"[A-Za-z]{5,}")
# Openings for a correction. A correction restates the fact with the new value after one of these.
CORRECTION_OPENINGS = (
    "oh wait i got that wrong before, ",
    "correction on something i said ages ago, ",
    "scratch what i told you earlier, ",
    "actually i mixed that up before, ",
)
# Training's own correction wordings (R-102), fixed before the held-out wordings were written.
# A correction is an opening before the restated fact line, or an ending after it.
TRAIN_CORRECTION_OPENINGS = (
    *CORRECTION_OPENINGS,
    "wait no, ",
    "my bad, i told you wrong before, ",
    "update on something i said a while back, ",
    "small fix to something i mentioned, ",
    "i misspoke earlier, ",
)
TRAIN_CORRECTION_ENDINGS = (
    ", i had that wrong before",
    " (i said it wrong last time)",
    ", not what i told you earlier",
)
# Words two wordings may share and still count as different wordings (R-102).
_FUNCTION_WORDS = frozenset(
    "a an and the i me my you your it its that this was is be what about on to of in for so "
    "just oh well".split()
)


def content_words(wording: str) -> frozenset[str]:
    """Return the words of ``wording`` that carry meaning, lower case, punctuation dropped."""
    return frozenset(
        w for w in re.findall(r"[a-z]+", wording.casefold()) if w not in _FUNCTION_WORDS
    )


def shares_wording(wording: str, others: tuple[str, ...]) -> bool:
    """Return True if ``wording`` shares a content word with any of ``others``.

    A held-out wording must not be a light rewording of a training one: one shared word is enough.
    """
    return any(content_words(wording) & content_words(other) for other in others)


def typed(line: str, rng: random.Random) -> str:
    """Return ``line`` as the user types: lower case, sparse punctuation, some trailing ellipses.

    Every letter goes lower case, names included. Commas and exclamation marks go. Apostrophes
    in contractions go one time in three. A full stop at the end goes, or becomes an ellipsis one
    time in six. A question mark stays six times in ten.
    """
    text = line.casefold().replace(",", "").replace("!", "")
    if rng.random() < 1 / 3:
        text = _CONTRACTIONS.sub(r"\1\2", text)
    text = text.rstrip()
    if text.endswith("?"):
        text = text if rng.random() < 0.6 else text[:-1]
    else:
        text = text.rstrip(".")
        if rng.random() < 1 / 6:
            text += "..."
    return text


def user_style(item: RecallItem, seed: int) -> RecallItem:
    """Return ``item`` with every friend line, and the final message, typed as a real user types."""
    rng = random.Random(seed)
    exchanges = tuple((typed(user, rng), reply) for user, reply in item.exchanges)
    return dataclasses.replace(item, exchanges=exchanges, message=typed(item.message, rng))


def phone_typed(line: str, rng: random.Random, keep: frozenset[str]) -> str:
    """Return ``line`` as typed fast on a phone: no apostrophes, "u" and "ur", one slipped letter.

    Every apostrophe goes, possessives included ("my sisters dog"). "you" and "your" become "u" and
    "ur". In one word of five letters or more two neighbouring letters change places, never the
    first or last letter, and never in a word in ``keep`` (names, relations and fact values).
    """
    text = line.replace("'", "").replace("\u2019", "")
    for pattern, short in _SHORT_FORMS:
        text = pattern.sub(short, text)
    words = [m for m in _LONG_WORD.finditer(text) if m.group(0).casefold() not in keep]
    rng.shuffle(words)
    for m in words:
        word = m.group(0)
        spots = [i for i in range(1, len(word) - 2) if word[i] != word[i + 1]]
        if spots:
            i = rng.choice(spots)
            word = word[:i] + word[i + 1] + word[i] + word[i + 2 :]
            return text[: m.start()] + word + text[m.end() :]
    return text


def phone_style(item: RecallItem, seed: int, pool_name: str) -> RecallItem:
    """Return ``item`` with every friend line, and the final message, typed fast on a phone."""
    rng = random.Random(seed)
    pool = POOLS[pool_name]
    values = (v for t in pool.facts.values() for v in t.values)
    keep = frozenset(
        w.casefold()
        for w in (*pool.people, *pool.relations, *" ".join(values).split(), *item.answer.split())
    )
    exchanges = tuple((phone_typed(user, rng, keep), reply) for user, reply in item.exchanges)
    return dataclasses.replace(
        item, exchanges=exchanges, message=phone_typed(item.message, rng, keep)
    )


def corrected(item: RecallItem, seed: int, pool_name: str) -> RecallItem:
    """Return an ``older`` or ``confirm`` item whose fact is corrected later, still out of view.

    The correction restates the fact line with a new value of the same type, after an opening
    that says the earlier one was wrong. The new value is the answer; the old one joins the
    forbidden values, so naming it is wrong. Other kinds are returned unchanged.
    """
    if item.kind not in (OLDER, CONFIRM):
        return item
    rng = random.Random(seed)
    template = next(
        t
        for t in POOLS[pool_name].facts.values()
        if item.answer in t.values and item.decoy in t.values
    )
    spare = [v for v in template.values if v != item.answer and v not in item.forbidden]
    new = rng.choice(spare)
    fact_line, fact_reply = item.exchanges[item.fact_index]
    correction = rng.choice(CORRECTION_OPENINGS) + fact_line.replace(item.answer, new)

    exchanges = list(item.exchanges)
    last_older = len(exchanges) - EXCHANGES_IN_VIEW - 1
    told = {v for v in (item.decoy, *item.forbidden) if v}
    free = [
        i
        for i in range(last_older + 1)
        if i != item.fact_index and not any(v in exchanges[i][0] for v in told)
    ]
    later = [i for i in free if i > item.fact_index]
    fact_index = item.fact_index
    if not later:
        # The fact sits in the last free slot: move it earlier, and correct it where it was.
        fact_index = rng.choice([i for i in free if i < item.fact_index])
        exchanges[fact_index] = (fact_line, fact_reply)
        later = [item.fact_index]
    exchanges[rng.choice(later)] = (correction, fact_reply)
    return dataclasses.replace(
        item,
        exchanges=tuple(exchanges),
        answer=new,
        forbidden=(*item.forbidden, item.answer),
        fact_index=fact_index,
        reply=item.reply.replace(item.answer, new),
    )


def asked_before(item: RecallItem, seed: int, pool_name: str) -> RecallItem:
    """Return ``item`` with an earlier question, answered, as the newest exchange in view.

    In real chats one question often follows another, so the last question is still in view when
    the next arrives. The earlier question asks about a fact of another type, about a relation and
    person the conversation never mentions, and its reply declines, which is right. If the item's
    fact sits in the newest exchange, the question goes in the one before it. Nothing the item is
    scored on changes.
    """
    rng = random.Random(seed)
    pool = POOLS[pool_name]
    own = next(t for t in pool.facts.values() if item.decoy in t.values)
    template = rng.choice([t for _, t in sorted(pool.facts.items()) if t is not own])
    said = " ".join([item.message, *(u + " " + r for u, r in item.exchanges)]).casefold()
    relation = rng.choice([r for r in pool.relations if r.casefold() not in said])
    person = rng.choice([p for p in pool.people if p.casefold() not in said])
    form = getattr(template, rng.choice(ASK_FORMS))
    question = form.format(relation=relation, person=person)

    exchanges = list(item.exchanges)
    slot = len(exchanges) - 1
    if slot == item.fact_index:
        slot -= 1
    exchanges[slot] = (question, rng.choice(pool.unknown_replies))
    return dataclasses.replace(item, exchanges=tuple(exchanges))
