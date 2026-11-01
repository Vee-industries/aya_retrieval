"""Scripted long conversations with one planted fact, one decoy fact and small talk around them.

Everything is made up and generated from a seed, so a conversation can be rebuilt exactly. The fact
sits outside the last exchanges, so a model that sees only those cannot answer without recall.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

EXCHANGES_IN_VIEW = 3

PEOPLE = ["Dana", "Marc", "Priya", "Tomas", "Lena", "Omar", "Greta", "Yusuf", "Nell", "Ivan"]
RELATIONS = ["sister", "brother", "neighbour", "cousin", "coworker", "aunt", "uncle", "roommate"]
VALUES = {
    "dog": ["Pepper", "Rusty", "Biscuit", "Juno", "Waffles", "Clover"],
    "city": ["Lisbon", "Oslo", "Tbilisi", "Valparaiso", "Hobart", "Quebec City"],
    "job": ["welder", "paramedic", "surveyor", "pastry chef", "court reporter", "beekeeper"],
    "car": ["green Corolla", "red Civic", "blue Tacoma", "white Forester", "grey Golf"],
    "hobby": ["pottery", "curling", "birdwatching", "fencing", "glassblowing", "bouldering"],
}
# Each fact has a question that repeats its words and one that shares only the relation word.
FACTS = {
    "dog": (
        "my {relation} {person} adopted a dog named {value} last month",
        "what is the name of the dog {person} adopted",
        "what do they call that pup over at my {relation}'s place",
    ),
    "city": (
        "my {relation} {person} is moving to {value} in the spring",
        "which city is {person} moving to",
        "where is my {relation} headed once winter is over",
    ),
    "job": (
        "my {relation} {person} just started work as a {value}",
        "what job did {person} start",
        "what does my {relation} do for a living these days",
    ),
    "car": (
        "my {relation} {person} bought a {value} from an auction",
        "what car did {person} buy at the auction",
        "what's my {relation} driving around in now",
    ),
    "hobby": (
        "my {relation} {person} has taken up {value} on weekends",
        "what has {person} taken up on weekends",
        "how does my {relation} keep busy on saturdays",
    ),
}
ACK = "Thanks for telling me."

SMALL_TALK_SUBJECTS = [
    "the bus", "my knee", "the garden", "that show", "the fridge", "the rain", "my phone",
    "the bakery", "the laundry", "my desk", "the snow", "the printer", "the kettle", "my bike",
    "the roof", "the wifi", "the parking lot", "my coffee", "the dishwasher", "the mail",
]  # fmt: skip
SMALL_TALK = [
    ("{subject} was acting up again today", "That sounds annoying. Hope it settles down."),
    ("i keep thinking about {subject}", "Sounds like it's been on your mind."),
    ("did i mention {subject} yesterday", "Not that I recall, but tell me about it."),
    ("{subject} is the least of my worries this week", "Sounds like a full week."),
    ("anyway, {subject} is fine now", "Good to hear it worked out."),
    ("not much going on, just dealing with {subject}", "Fair enough, one thing at a time."),
]


@dataclass(frozen=True)
class RecallItem:
    """One conversation ending in a question whose answer is outside the last exchanges."""

    item_id: str
    exchanges: tuple[tuple[str, str], ...]
    question: str
    answer: str
    decoy: str
    fact_index: int
    shares_words: bool

    def view(self) -> tuple[tuple[str, str], ...]:
        """Return the exchanges that stay in view."""
        return self.exchanges[-EXCHANGES_IN_VIEW:]

    def older(self) -> tuple[tuple[str, str], ...]:
        """Return the exchanges outside the view, reachable only by searching."""
        return self.exchanges[:-EXCHANGES_IN_VIEW]


def _small_talk(rng: random.Random) -> tuple[str, str]:
    user, assistant = rng.choice(SMALL_TALK)
    return user.format(subject=rng.choice(SMALL_TALK_SUBJECTS)), assistant


def build_item(item_id: str, seed: int, messages: int, shares_words: bool) -> RecallItem:
    """Return one conversation of about ``messages`` messages, fixed by ``seed``."""
    rng = random.Random(seed)
    kind = rng.choice(sorted(FACTS))
    statement, same_words_question, new_words_question = FACTS[kind]
    answer, decoy = rng.sample(VALUES[kind], 2)
    relation, decoy_relation = rng.sample(RELATIONS, 2)
    person, decoy_person = rng.sample(PEOPLE, 2)

    exchange_count = max(messages // 2, EXCHANGES_IN_VIEW + 2)
    exchanges = [_small_talk(rng) for _ in range(exchange_count)]
    older_slots = range(exchange_count - EXCHANGES_IN_VIEW)
    fact_index, decoy_index = rng.sample(older_slots, 2)
    exchanges[fact_index] = (
        statement.format(relation=relation, person=person, value=answer),
        ACK,
    )
    exchanges[decoy_index] = (
        statement.format(relation=decoy_relation, person=decoy_person, value=decoy),
        ACK,
    )
    template = same_words_question if shares_words else new_words_question
    return RecallItem(
        item_id=item_id,
        exchanges=tuple(exchanges),
        question=template.format(relation=relation, person=person),
        answer=answer,
        decoy=decoy,
        fact_index=fact_index,
        shares_words=shares_words,
    )
