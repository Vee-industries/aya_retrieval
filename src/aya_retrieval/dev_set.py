"""Load the independent development set: chats written blind to the generator (R-139, item 4).

Each file holds one conversation and six alternative final questions. Every question becomes its own
``RecallItem`` on the same conversation, so the harness, the search tool and the scorer are the ones
every other result uses. A question that breaks a rule of the writing brief is dropped, with its
reason, rather than repaired: repairing it would mean editing the writer's material.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from aya_retrieval.conversations import (
    CONFIRM,
    EXCHANGES_IN_VIEW,
    IN_VIEW,
    ITEM_KINDS,
    NEVER_TOLD,
    OLDER,
    STATEMENT,
    RecallItem,
)

NO_FACT = -1  # never_told and statement items hold no fact, so no search can find one
# The scorer matches substrings; a short value would match inside longer words (R-139 panel).
MIN_LETTERS = 4


def _text(exchanges) -> str:
    return "\n".join(f"{user}\n{assistant}" for user, assistant in exchanges).casefold()


def question_problem(exchanges: tuple[tuple[str, str], ...], question: dict) -> str | None:
    """Return the first brief rule ``question`` breaks on this conversation, or None."""
    kind, message = question.get("kind"), question.get("message", "")
    answer, wrong = question.get("answer", ""), question.get("wrong", [])
    fact = question.get("fact_exchange")
    if kind not in ITEM_KINDS:
        return f"unknown kind {kind!r}"
    if not message.strip():
        return "empty message"
    if not isinstance(wrong, list) or not all(isinstance(w, str) and w.strip() for w in wrong):
        return "wrong values are not a list of strings"
    if any(len(w.strip()) < MIN_LETTERS for w in wrong):
        return "a wrong value is under 4 letters"
    chat, last = _text(exchanges), len(exchanges) - EXCHANGES_IN_VIEW
    if kind == STATEMENT:
        return None
    if kind == NEVER_TOLD:
        if not wrong:
            return "never_told item with no wrong values"
        if any(w.casefold() not in chat for w in wrong):
            return "a wrong value is not in the conversation"
        return None
    if not answer.strip():
        return "empty answer"
    if len(answer.strip()) < MIN_LETTERS:
        return "answer is under 4 letters"
    if not isinstance(fact, int) or not 0 <= fact < len(exchanges):
        return "fact exchange out of range"
    if answer.casefold() not in _text(exchanges[fact : fact + 1]):
        return "answer is not in its fact exchange"
    if any(w.casefold() not in chat for w in wrong):
        return "a wrong value is not in the conversation"
    if any(w.casefold() in answer.casefold() or answer.casefold() in w.casefold() for w in wrong):
        return "a wrong value and the answer contain one another"
    if kind != CONFIRM and answer.casefold() in message.casefold():
        return "answer is in the question"
    if kind in (OLDER, CONFIRM):
        if fact >= last:
            return "fact exchange is in view"
        if answer.casefold() in _text(exchanges[last:]):
            return "answer appears in view"
    if kind == IN_VIEW and fact < last:
        return "in_view fact is out of view"
    return None


def load_dev_set(folder: Path) -> tuple[list[RecallItem], list[tuple[str, str]], str]:
    """Return the set's items, the dropped questions with their reasons, and the set's sha256.

    The hash covers every file's name and bytes in name order, so a result names exactly the
    material it was scored on.
    """
    items, dropped, digest = [], [], hashlib.sha256()
    for path in sorted(folder.glob("*.json")):
        digest.update(path.name.encode("utf-8") + b"\0" + path.read_bytes())
        chat = json.loads(path.read_text(encoding="utf-8"))
        exchanges = tuple((str(user), str(assistant)) for user, assistant in chat["exchanges"])
        if len(exchanges) <= EXCHANGES_IN_VIEW:
            dropped.append((chat["id"], "conversation too short"))
            continue
        for number, question in enumerate(chat["questions"]):
            item_id = f"{chat['id']}_q{number}"
            problem = question_problem(exchanges, question)
            if problem:
                dropped.append((item_id, problem))
                continue
            wrong = tuple(question["wrong"])
            fact = question.get("fact_exchange")
            items.append(
                RecallItem(
                    item_id=item_id,
                    kind=question["kind"],
                    exchanges=exchanges,
                    message=question["message"],
                    answer=question.get("answer", "") if question["kind"] != NEVER_TOLD else "",
                    decoy=wrong[0] if wrong else "",
                    forbidden=wrong,
                    fact_index=fact if isinstance(fact, int) else NO_FACT,
                    query="",
                    reply="",
                )
            )
    return items, dropped, digest.hexdigest()
