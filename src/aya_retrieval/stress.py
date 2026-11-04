"""Harder versions of a test conversation, for development checks (R-067).

Each takes a built ``RecallItem`` and returns a changed copy, so any pool can be tested this way
without writing a new one. The kinds of difficulty come from the failure categories another chat
project tracked (its categories only; none of its text): how a real user types, and facts that are
corrected later.
"""

from __future__ import annotations

import dataclasses
import random
import re

from aya_retrieval.conversations import CONFIRM, EXCHANGES_IN_VIEW, OLDER, RecallItem
from aya_retrieval.pools import POOLS

# Contractions typed without the apostrophe, as many people text.
_CONTRACTIONS = re.compile(r"\b(\w+)'(t|s|m|re|ll|ve|d)\b")
# Openings for a correction. A correction restates the fact with the new value after one of these.
CORRECTION_OPENINGS = (
    "oh wait i got that wrong before, ",
    "correction on something i said ages ago, ",
    "scratch what i told you earlier, ",
    "actually i mixed that up before, ",
)


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
