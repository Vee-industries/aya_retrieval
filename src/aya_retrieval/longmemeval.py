"""Load LongMemEval-S as long chats ending in one question, for the outside check (R-170).

Usage:
    from aya_retrieval.longmemeval import load_longmemeval
    items, digest = load_longmemeval(Path("C:/.../longmemeval_s_cleaned.json"))

Why: R-170 runs base and 6.37 on LongMemEval-S (Wu et al., ICLR 2025), a set written outside the
project. Each question has its own history of chat sessions. R-170 fixes the adaptation, and this
module is it:

- Turns are paired into (user, assistant) exchanges in order, across the whole history. A turn that
  does not pair (two turns of one role in a row, across a session boundary included) is joined to
  its neighbour of the same role, so no text changes role or order. A history that opens with an
  assistant turn has no user turn to pair it with; that exchange's user side holds only the date.
- Each user text is prefixed with its session date, once per session it holds, and the question,
  the newest message, with its question date.
- The last three exchanges are in view; everything earlier is indexed, as in every other test.

Each exchange keeps the sessions its turns came from and whether one of its turns is marked
``has_answer``. The file is checked against R-170's sha256 before it is read, and never enters the
repository: it is an outside download, read only by a Python started with ``-I``.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

from agenttune.rag.retrieval.corpus_loader import CorpusDocument, chunk_corpus

from aya_retrieval.conversations import EXCHANGES_IN_VIEW
from aya_retrieval.recall_tool import CHUNK_SIZE, exchange_doc_id

DATA_SHA256 = "d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442"
ABSTENTION_SUFFIX = "_abs"
USER, ASSISTANT = "user", "assistant"


@dataclass(frozen=True)
class Pairing:
    """Exchanges built from turns, with what each holds and how many turns did not pair."""

    exchanges: tuple[tuple[str, str], ...]
    session_ids: tuple[tuple[str, ...], ...]
    has_answer: tuple[bool, ...]
    joined: int
    joined_across_sessions: int
    opened_by_assistant: int


@dataclass(frozen=True)
class LongMemItem:
    """One LongMemEval question and its history, shaped like ``conversations.RecallItem``."""

    item_id: str
    kind: str
    exchanges: tuple[tuple[str, str], ...]
    message: str
    question: str
    answer: str
    session_ids: tuple[tuple[str, ...], ...]
    has_answer: tuple[bool, ...]
    answer_session_ids: tuple[str, ...]
    evidence_exchanges: tuple[tuple[str, str], ...]
    joined: int
    joined_across_sessions: int
    opened_by_assistant: int

    def view(self) -> tuple[tuple[str, str], ...]:
        """Return the exchanges that stay in view."""
        return self.exchanges[-EXCHANGES_IN_VIEW:]

    def older(self) -> tuple[tuple[str, str], ...]:
        """Return the exchanges outside the view, reachable only by searching."""
        return self.exchanges[:-EXCHANGES_IN_VIEW]

    def evidence_indexes(self) -> tuple[int, ...]:
        """Return the indexes of the exchanges holding a ``has_answer`` turn."""
        return tuple(i for i, marked in enumerate(self.has_answer) if marked)

    def evidence_in_view(self) -> bool:
        """Return True if an exchange holding a ``has_answer`` turn is in view."""
        first_in_view = len(self.exchanges) - EXCHANGES_IN_VIEW
        return any(i >= first_in_view for i in self.evidence_indexes())

    def answer_session_indexes(self) -> tuple[int, ...]:
        """Return the indexes of the exchanges holding a turn from an evidence session."""
        evidence = set(self.answer_session_ids)
        return tuple(i for i, ids in enumerate(self.session_ids) if evidence & set(ids))

    @property
    def abstention(self) -> bool:
        """True for the questions whose answer is not in the history (id ends ``_abs``)."""
        return self.item_id.endswith(ABSTENTION_SUFFIX)


def dated(date: str, text: str) -> str:
    """Return ``text`` with ``date`` in front, as each user text and the question carry it."""
    return f"[{date}] {text}" if text else f"[{date}]"


def pair_turns(sessions: list[list[dict]], dates: list[str], ids: list[str]) -> Pairing:
    """Pair the sessions' turns, in order, into exchanges, as the module docstring describes.

    Raises:
        ValueError: On a turn whose role is neither user nor assistant.
    """
    exchanges, session_ids, has_answer = [], [], []
    joined = across = opened = 0
    users: list[tuple[str, str, str]] = []  # (session id, date, text)
    replies: list[str] = []
    sources: list[str] = []
    marked = False
    previous_session = None

    def close() -> None:
        parts, last = [], None
        for session, date, text in users:
            parts.append(text if session == last else dated(date, text))
            last = session
        exchanges.append(("\n\n".join(parts), "\n\n".join(replies)))
        session_ids.append(tuple(dict.fromkeys(sources)))
        has_answer.append(marked)

    for session, date, session_id in zip(sessions, dates, ids, strict=True):
        for turn in session:
            role, text = turn["role"], turn["content"]
            if role not in (USER, ASSISTANT):
                raise ValueError(f"unknown role {role!r} in session {session_id}")
            same_role = (role == USER and users and not replies) or (role == ASSISTANT and replies)
            if same_role:
                joined += 1
                across += session_id != previous_session
            if role == USER:
                if replies:
                    close()
                    users, replies, sources, marked = [], [], [], False
                users.append((session_id, date, text))
            else:
                if not users and not replies:
                    opened += 1
                    users.append((session_id, date, ""))
                replies.append(text)
            sources.append(session_id)
            marked = marked or bool(turn.get("has_answer"))
            previous_session = session_id
    if users or replies:
        close()
    return Pairing(
        exchanges=tuple(exchanges),
        session_ids=tuple(session_ids),
        has_answer=tuple(has_answer),
        joined=joined,
        joined_across_sessions=across,
        opened_by_assistant=opened,
    )


def convert(record: dict) -> LongMemItem:
    """Return one LongMemEval record as an item."""
    sessions, dates = record["haystack_sessions"], record["haystack_dates"]
    ids = record["haystack_session_ids"]
    history = pair_turns(sessions, dates, ids)
    evidence = set(record["answer_session_ids"])
    chosen = [i for i, session_id in enumerate(ids) if session_id in evidence]
    evidence_only = pair_turns(
        [sessions[i] for i in chosen], [dates[i] for i in chosen], [ids[i] for i in chosen]
    )
    return LongMemItem(
        item_id=record["question_id"],
        kind=record["question_type"],
        exchanges=history.exchanges,
        message=dated(record["question_date"], record["question"]),
        question=record["question"],
        answer=str(record["answer"]),
        session_ids=history.session_ids,
        has_answer=history.has_answer,
        answer_session_ids=tuple(record["answer_session_ids"]),
        evidence_exchanges=evidence_only.exchanges,
        joined=history.joined,
        joined_across_sessions=history.joined_across_sessions,
        opened_by_assistant=history.opened_by_assistant,
    )


def load_longmemeval(path: Path) -> tuple[list[LongMemItem], str]:
    """Return every question as an item, in file order, and the file's sha256.

    Raises:
        ValueError: If the file is not the one R-170 registered.
    """
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != DATA_SHA256:
        raise ValueError(f"{path} has sha256 {digest}, not R-170's {DATA_SHA256}")
    return [convert(record) for record in json.loads(raw)], digest


def passages(exchanges) -> list[dict]:
    """Return the passages ``recall_tool.build_search_tool`` indexes for ``exchanges``.

    Each has the chunk id and document id the tool reports, the exchange index and the full text
    (the tool shows its first 350 characters). Built the same way, so chunks can be counted and
    drawn on the CPU without a database.
    """
    docs = [
        CorpusDocument(
            doc_id=exchange_doc_id(index),
            title=f"Exchange {index}",
            text=f"User: {user}\nAssistant: {assistant}",
            metadata={},
        )
        for index, (user, assistant) in enumerate(exchanges)
    ]
    chunks = chunk_corpus(docs, chunk_size=CHUNK_SIZE, overlap=0)
    return [
        {
            "chunk_id": chunk["chunk_id"],
            "doc_id": chunk["doc_id"],
            "exchange": exchange_index(chunk["doc_id"]),
            "text": chunk["text"],
        }
        for chunk in chunks
    ]


def exchange_index(doc_id: str) -> int:
    """Return the exchange index named by a document id from ``recall_tool.exchange_doc_id``."""
    return int(doc_id.rsplit("_", 1)[1])
