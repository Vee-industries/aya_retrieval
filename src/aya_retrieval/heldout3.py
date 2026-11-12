"""Load and check S3, the third sealed test set (R-178), and score what the model-free flags need.

Each chat file follows ``docs/heldout3/BRIEF.md``. One exchange in the last three holds an earlier
user question about a fact that is out of view; its assistant half is empty in the file, and the
loader fills it with the writer's ``right_reply`` or ``wrong_reply``. That gives two views of every
chat, the same for every arm:

- the right-reply view scores older, confirm, in_view, statement and never_told;
- the wrong-reply view scores older, never_told and re_ask (the fact the wrong reply got wrong).

Every rule of the brief is a check that returns a reason, never chat text. A chat that breaks a
chat rule is dropped whole; a question that breaks a question rule is dropped alone. Nothing is
repaired, since repairing would mean editing the writer's material. Rules over a writer's whole
batch (how many chats, the confirm balance) come back as reasons from ``set_problems``.

The model-free flags the eval records (copy, N-hit, false answer, the never-told rubric) live here
so the seal covers them with the loader.
"""

from __future__ import annotations

import hashlib
import json
import random
import re
from dataclasses import dataclass
from pathlib import Path

from aya_retrieval.conversations import (
    CONFIRM,
    EXCHANGES_IN_VIEW,
    IN_VIEW,
    NEVER_TOLD,
    OLDER,
    STATEMENT,
    RecallItem,
)
from aya_retrieval.dev_set import MIN_LETTERS, NO_FACT, question_problem

REPO_ROOT = Path(__file__).resolve().parents[2]
CHATS_DIR = REPO_ROOT / "data" / "heldout3" / "chats"
SPLIT_FILE = REPO_ROOT / "docs" / "heldout3" / "category_split.json"

VIEW = 3  # exchanges in view; the brief is written for this number
RE_ASK = "re_ask"
KINDS = (OLDER, CONFIRM, IN_VIEW, STATEMENT, NEVER_TOLD, RE_ASK)
RIGHT_VIEW, WRONG_VIEW = "right", "wrong"
# R-178 method lane, section 1: every question in the right view; older, never_told and the
# re-ask also in the wrong view. The re-ask's answer is in view in the right view, so it is not
# scored there.
VIEW_KINDS = {
    RIGHT_VIEW: (OLDER, CONFIRM, IN_VIEW, STATEMENT, NEVER_TOLD),
    WRONG_VIEW: (OLDER, NEVER_TOLD, RE_ASK),
}
# Per chat: three older (one from list B, two from list A), one of each other kind, and two
# never_told (one plain, one sharing a content word with another exchange).
KIND_COUNTS = {OLDER: 3, CONFIRM: 1, IN_VIEW: 1, STATEMENT: 1, NEVER_TOLD: 2, RE_ASK: 1}
OLDER_FROM_A, OLDER_FROM_B = 2, 1
MIN_EXCHANGES, MAX_EXCHANGES = 20, 30
MIN_PEOPLE = 5
MIN_FACTS_PER_LIST = 2
USER = "me"
CHATS_PER_WRITER = 10
CLAIMS = ("true", "false")
CHAT_ID = re.compile(r"^(w[1-9])_(\d{2})$")
CATEGORY_ID = re.compile(r"^C\d{2}$")

# R-178 item 3: fixed before sealing, the same for every arm.
NEVER_TOLD_RUBRIC = (
    "A never_told reply is right when it says it does not see the fact, does not know it, or was "
    "not told it ('I don't see it', 'I don't know', 'you didn't tell me', or the same in other "
    "words) and names no value. A reply that names any value for the asked fact is wrong."
)
SAMPLE_SEED = 178  # the coherence sample's draw (R-178 item 7 of the build brief)
SAMPLE_SIZE = 120  # R-178 method lane, section 1: a 120-question sample drawn by code
SHUFFLE_SEED = 1780  # the order of judge sheets built from S3 replies

# Content words, as R-176 counted them (scripts/records/demo_overlap_r176.py).
STOP = frozenset(
    "a about again all an and any anyway are at be been but did do does for go had has have he her "
    "his how i i'm i've if in into is it it's its just lately me my of on or out over really s she "
    "should so that the their them they this to up was we were what what's when where which who "
    "with you your".split()
)


def content_words(text: str) -> set[str]:
    """Return the lower-case words of ``text`` that are not stop words."""
    return {w for w in re.findall(r"[a-z']+", text.casefold()) if w not in STOP}


@dataclass(frozen=True)
class Split:
    """Category ids from ``category_split.json``: list A is outside the training lexicon."""

    outside: frozenset[str]
    inside: frozenset[str]

    def known(self, category: object) -> bool:
        return category in self.outside or category in self.inside


def load_split(path: Path = SPLIT_FILE) -> Split:
    """Return the committed category split."""
    data = json.loads(path.read_text(encoding="utf-8"))
    return Split(outside=frozenset(data["outside"]), inside=frozenset(data["inside"]))


@dataclass(frozen=True)
class S3Item:
    """One question in one view, with what the S3 flags need beside the scorer's item."""

    item: RecallItem
    chat_id: str
    writer: str
    view: str
    question: int
    category: str | None
    inside: bool | None
    variant: str | None  # never_told only: "plain" or "overlap"
    claim: str | None  # confirm only: "true" or "false"
    claimed_value: str | None  # confirm only: the value the user names
    category_values: tuple[str, ...]  # every chat value of the asked category
    earlier_wrong_value: str  # the value the wrong reply names


def _text(exchanges) -> str:
    return "\n".join(f"{user}\n{assistant}" for user, assistant in exchanges).casefold()


def _same(a: str, b: str) -> bool:
    return a.casefold() == b.casefold()


def _overlaps(a: str, b: str) -> bool:
    a, b = a.casefold(), b.casefold()
    return a in b or b in a


def view_exchanges(chat: dict, view: str) -> tuple[tuple[str, str], ...]:
    """Return the chat's exchanges with the earlier question's reply for ``view`` filled in."""
    earlier = chat["earlier_question"]
    reply = earlier["right_reply"] if view == RIGHT_VIEW else earlier["wrong_reply"]
    exchanges = [(str(u), str(a)) for u, a in chat["exchanges"]]
    user, _ = exchanges[earlier["exchange"]]
    exchanges[earlier["exchange"]] = (user, str(reply))
    return tuple(exchanges)


def _current_facts(facts: list[dict]) -> list[dict]:
    """Facts not replaced by a later correction."""
    replaced = {f["corrects"] for f in facts if isinstance(f.get("corrects"), int)}
    return [f for n, f in enumerate(facts) if n not in replaced]


def _shape_problem(chat: dict) -> str | None:
    """Return a reason if the file does not have the brief's fields and types."""
    if not isinstance(chat, dict):
        return "file is not one JSON object"
    for key, kind in (
        ("id", str),
        ("people", list),
        ("exchanges", list),
        ("facts", list),
        ("lookalikes", list),
        ("earlier_question", dict),
        ("questions", list),
    ):
        if not isinstance(chat.get(key), kind):
            return f"field {key} is missing or of the wrong type"
    if not CHAT_ID.match(chat["id"]):
        return "id is not {writer}_{nn}"
    for pair in chat["exchanges"]:
        if not (
            isinstance(pair, list) and len(pair) == 2 and all(isinstance(t, str) for t in pair)
        ):
            return "an exchange is not a [user, assistant] pair of strings"
    if not all(isinstance(p, str) and p.strip() for p in chat["people"]):
        return "people is not a list of names"
    for fact in chat["facts"]:
        if not isinstance(fact, dict):
            return "a fact is not an object"
        if not isinstance(fact.get("exchange"), int) or not isinstance(fact.get("value"), str):
            return "a fact has no exchange number or value"
        if not isinstance(fact.get("person"), str) or not isinstance(fact.get("category"), str):
            return "a fact has no person or category"
        if fact.get("corrects") is not None and not isinstance(fact.get("corrects"), int):
            return "a fact's corrects is neither null nor a fact number"
    earlier = chat["earlier_question"]
    for key in ("exchange", "fact_exchange"):
        if not isinstance(earlier.get(key), int):
            return f"earlier_question.{key} is not a number"
    for key in ("category", "person", "answer", "wrong_value", "wrong_reply", "right_reply"):
        if not isinstance(earlier.get(key), str) or not earlier[key].strip():
            return f"earlier_question.{key} is missing"
    for number, question in enumerate(chat["questions"]):
        if not isinstance(question, dict):
            return f"question {number} is not an object"
        if not isinstance(question.get("message"), str):
            return f"question {number} has no message"
        if not isinstance(question.get("answer", ""), str):
            return f"question {number}: answer is not a string"
        if not isinstance(question.get("wrong", []), list):
            return f"question {number}: wrong is not a list"
        for key in ("category", "person"):
            if not isinstance(question.get(key), str | None):
                return f"question {number}: {key} is not a string"
        for key in ("fact_exchange", "overlap_exchange"):
            value = question.get(key)
            if value is not None and (not isinstance(value, int) or isinstance(value, bool)):
                return f"question {number}: {key} is neither null nor a number"
    return None


def chat_problem(chat: dict, split: Split) -> str | None:
    """Return the first chat rule of the brief that ``chat`` breaks, or None."""
    problem = _shape_problem(chat)
    if problem:
        return problem
    exchanges, facts, people = chat["exchanges"], chat["facts"], chat["people"]
    if not MIN_EXCHANGES <= len(exchanges) <= MAX_EXCHANGES:
        return f"{len(exchanges)} exchanges, not {MIN_EXCHANGES} to {MAX_EXCHANGES}"
    last = len(exchanges) - VIEW
    if len({p.casefold() for p in people}) < MIN_PEOPLE or USER in {p.casefold() for p in people}:
        return f"fewer than {MIN_PEOPLE} people besides the user"
    persons = set(people) | {USER}
    text = [f"{u}\n{a}".casefold() for u, a in exchanges]
    for number, fact in enumerate(facts):
        if not 0 <= fact["exchange"] < len(exchanges):
            return f"fact {number}: exchange out of range"
        if fact["person"] not in persons:
            return f"fact {number}: person is not in people"
        if not split.known(fact["category"]):
            return f"fact {number}: unknown category"
        if len(fact["value"].strip()) < MIN_LETTERS:
            return f"fact {number}: value under {MIN_LETTERS} letters"
        if fact["value"].casefold() not in text[fact["exchange"]]:
            return f"fact {number}: value is not in its exchange"
        old = fact.get("corrects")
        if old is not None:
            if not 0 <= old < number:
                return f"fact {number}: corrects a fact that is not earlier in the list"
            before = facts[old]
            same = before["person"] == fact["person"] and before["category"] == fact["category"]
            if not same or _same(before["value"], fact["value"]):
                return f"fact {number}: correction changes the person, category or not the value"
            if before["exchange"] >= fact["exchange"]:
                return f"fact {number}: correction is not later in the chat"
    if not any(f.get("corrects") is not None for f in facts):
        return "no correction"
    in_a = sum(f["category"] in split.outside for f in facts)
    in_b = sum(f["category"] in split.inside for f in facts)
    if in_a < MIN_FACTS_PER_LIST or in_b < MIN_FACTS_PER_LIST:
        return f"facts from list A {in_a}, list B {in_b}; at least {MIN_FACTS_PER_LIST} each"
    if 3 * sum(f["person"] == USER for f in facts) < len(facts):
        return "under a third of facts are about the user"
    pair = chat["lookalikes"]
    if len(pair) != 2 or pair[0] == pair[1] or not all(p in people for p in pair):
        return "lookalikes is not two different people from people"
    first = [f for f in facts if f["person"] == pair[0]]
    second = [f for f in facts if f["person"] == pair[1]]
    if not any(
        a["category"] == b["category"] and not _same(a["value"], b["value"])
        for a in first
        for b in second
    ):
        return "the look-alikes have no fact of one category with different values"

    earlier = chat["earlier_question"]
    at, fact_at = earlier["exchange"], earlier["fact_exchange"]
    answer, wrong_value = earlier["answer"], earlier["wrong_value"]
    if not last <= at < len(exchanges):
        return "earlier question is not in the last three exchanges"
    if exchanges[at][1] != "":
        return "earlier question's assistant half is not empty"
    if not 0 <= fact_at < last:
        return "earlier question's fact is not out of view"
    if not any(
        f["exchange"] == fact_at
        and f["category"] == earlier["category"]
        and f["person"] == earlier["person"]
        and _same(f["value"], answer)
        for f in _current_facts(facts)
    ):
        return "earlier question's answer is not a current fact at its exchange"
    if _overlaps(answer, wrong_value):
        return "earlier answer and wrong value contain one another"
    if not any(
        f["category"] == earlier["category"] and _same(f["value"], wrong_value) for f in facts
    ):
        return "wrong value is not a chat value of the same category"
    wrong_reply, right_reply = earlier["wrong_reply"].casefold(), earlier["right_reply"].casefold()
    if wrong_value.casefold() not in wrong_reply or answer.casefold() in wrong_reply:
        return "wrong reply does not name the wrong value alone"
    if answer.casefold() not in right_reply or wrong_value.casefold() in right_reply:
        return "right reply does not name the answer alone"
    asked = exchanges[at][0].casefold()
    if answer.casefold() in asked or wrong_value.casefold() in asked:
        return "earlier question names its answer or the wrong value"
    for question in chat["questions"]:
        given = question.get("answer")
        if isinstance(given, str) and given.strip() and _overlaps(given, wrong_value):
            return "wrong value is, or contains, an answer to a question"

    kinds = [q.get("kind") for q in chat["questions"]]
    for kind, count in KIND_COUNTS.items():
        if kinds.count(kind) != count:
            return f"{kinds.count(kind)} {kind} questions, not {count}"
    if len(kinds) != sum(KIND_COUNTS.values()):
        return "a question of an unknown kind"
    older = [q.get("category") for q in chat["questions"] if q.get("kind") == OLDER]
    if (
        sum(c in split.outside for c in older) != OLDER_FROM_A
        or sum(c in split.inside for c in older) != OLDER_FROM_B
    ):
        return f"older questions are not {OLDER_FROM_A} from list A and {OLDER_FROM_B} from list B"
    variants = sorted(
        "overlap" if isinstance(q.get("overlap_exchange"), int) else "plain"
        for q in chat["questions"]
        if q.get("kind") == NEVER_TOLD
    )
    if variants != ["overlap", "plain"]:
        return "never_told questions are not one plain and one overlap"
    return None


def _question_problem_s3(chat: dict, number: int, split: Split) -> str | None:
    """Return the first question rule that question ``number`` breaks, or None."""
    question = chat["questions"][number]
    kind = question.get("kind")
    facts, earlier = chat["facts"], chat["earlier_question"]
    persons = set(chat["people"]) | {USER}
    last = len(chat["exchanges"]) - VIEW
    right, wrong = view_exchanges(chat, RIGHT_VIEW), view_exchanges(chat, WRONG_VIEW)
    base = {key: question.get(key) for key in ("kind", "message", "answer", "wrong")}
    base["fact_exchange"] = question.get("fact_exchange")
    base["wrong"] = base["wrong"] if base["wrong"] is not None else []
    base["answer"] = base["answer"] or ""
    if kind == RE_ASK:
        problem = question_problem(wrong, base | {"kind": OLDER})
    else:
        problem = question_problem(right, base) or question_problem(wrong, base)
    if problem:
        return problem
    message = question["message"].casefold()
    if kind == STATEMENT:
        older_values = [f["value"] for f in facts if f["exchange"] < last]
        if any(v.casefold() in message for v in older_values):
            return "statement names a fact from before the last three exchanges"
        return None
    category, person = question.get("category"), question.get("person")
    if not split.known(category):
        return "unknown category"
    if person not in persons:
        return "person is not in people"
    values = [f for f in facts if f["category"] == category]
    if kind == NEVER_TOLD:
        if any(f["person"] == person for f in values):
            return "never_told fact was told"
        if not values:
            return "no chat value of the asked category"
        named = {w.casefold() for w in question["wrong"]}
        if any(f["value"].casefold() not in named for f in values):
            return "wrong does not list every chat value of the asked category"
        at = question.get("overlap_exchange")
        if at is None:
            return None
        if not isinstance(at, int) or not 0 <= at < last:
            return "overlap exchange is not out of view"
        there = [f for f in facts if f["exchange"] == at and f["category"] != category]
        if not any(f["value"].casefold() in named for f in there):
            return "wrong does not list the overlap exchange's value"
        if not content_words(question["message"]) & content_words(" ".join(chat["exchanges"][at])):
            return "never_told shares no content word with its overlap exchange"
        return None
    fact_at, answer = question["fact_exchange"], question["answer"]
    if kind == IN_VIEW and fact_at == earlier["exchange"]:
        return "in_view fact is the earlier question's exchange"
    if not any(
        f["exchange"] == fact_at and f["person"] == person and _same(f["value"], answer)
        for f in _current_facts(values)
    ):
        return "answer is not a current fact of this person and category at its exchange"
    if kind == RE_ASK:
        same = (category, person, fact_at) == (
            earlier["category"],
            earlier["person"],
            earlier["fact_exchange"],
        )
        if not same or not _same(answer, earlier["answer"]):
            return "re_ask is not the earlier question's fact"
        if earlier["wrong_value"].casefold() not in {w.casefold() for w in question["wrong"]}:
            return "re_ask wrong does not list the wrong reply's value"
    if kind == CONFIRM:
        claim, claimed = question.get("claim"), question.get("claimed_value")
        if claim not in CLAIMS or not isinstance(claimed, str) or not claimed.strip():
            return "confirm has no claim or claimed value"
        if claimed.casefold() not in message:
            return "claimed value is not in the message"
        if (claim == "true") != _same(claimed, answer):
            return "claim does not match whether the claimed value is the answer"
        if claim == "false":
            if claimed.casefold() in {w.casefold() for w in question["wrong"]}:
                return "a false claim's value is listed in wrong"
            if not any(_same(f["value"], claimed) for f in values):
                return "a false claim's value is not a chat value of the category"
    return None


def set_problems(chats: list[dict]) -> list[str]:
    """Return the batch rules the loaded chats break: chats per writer and the confirm balance."""
    writers: dict[str, list[dict]] = {}
    for chat in chats:
        writers.setdefault(CHAT_ID.match(chat["id"]).group(1), []).append(chat)
    reasons = []
    for writer, own in sorted(writers.items()):
        if len(own) != CHATS_PER_WRITER:
            reasons.append(f"{writer}: {len(own)} chats, not {CHATS_PER_WRITER}")
        claims = [
            q.get("claim") for chat in own for q in chat["questions"] if q.get("kind") == CONFIRM
        ]
        if abs(claims.count("true") - claims.count("false")) > len(claims) % 2:
            reasons.append(
                f"{writer}: confirm claims {claims.count('true')} true, "
                f"{claims.count('false')} false, not half and half"
            )
    return reasons


def _items(chat: dict, kept: list[int], split: Split) -> list[S3Item]:
    writer = CHAT_ID.match(chat["id"]).group(1)
    wrong_value = chat["earlier_question"]["wrong_value"]
    built = []
    for view, kinds in VIEW_KINDS.items():
        exchanges = view_exchanges(chat, view)
        for number in kept:
            question = chat["questions"][number]
            kind = question["kind"]
            if kind not in kinds:
                continue
            category = question.get("category")
            wrong = tuple(question.get("wrong") or ())
            fact = question.get("fact_exchange")
            item = RecallItem(
                item_id=f"{chat['id']}_q{number}_{view}",
                kind=kind,
                exchanges=exchanges,
                message=question["message"],
                answer=(question.get("answer") or "") if kind != NEVER_TOLD else "",
                decoy=wrong[0] if wrong else "",
                forbidden=wrong,
                fact_index=fact if isinstance(fact, int) else NO_FACT,
                query="",
                reply="",
            )
            values = tuple(
                dict.fromkeys(f["value"] for f in chat["facts"] if f["category"] == category)
            )
            built.append(
                S3Item(
                    item=item,
                    chat_id=chat["id"],
                    writer=writer,
                    view=view,
                    question=number,
                    category=category,
                    inside=None if category is None else category in split.inside,
                    variant=(
                        (
                            "overlap"
                            if isinstance(question.get("overlap_exchange"), int)
                            else "plain"
                        )
                        if kind == NEVER_TOLD
                        else None
                    ),
                    claim=question.get("claim") if kind == CONFIRM else None,
                    claimed_value=question.get("claimed_value") if kind == CONFIRM else None,
                    category_values=values,
                    earlier_wrong_value=wrong_value,
                )
            )
    return built


def load_s3(
    folder: Path = CHATS_DIR, split: Split | None = None
) -> tuple[list[S3Item], list[tuple[str, str]], list[str], str]:
    """Return the items of both views, the dropped chats and questions with reasons, the batch
    reasons, and the set's sha256.

    The hash covers every file's name and bytes in name order, as ``load_dev_set``'s does.
    """
    if EXCHANGES_IN_VIEW != VIEW:
        raise RuntimeError(f"the harness shows {EXCHANGES_IN_VIEW} exchanges; S3 is for {VIEW}")
    split = split or load_split()
    items, dropped, loaded, digest = [], [], [], hashlib.sha256()
    for path in sorted(folder.glob("*.json")):
        digest.update(path.name.encode("utf-8") + b"\0" + path.read_bytes())
        try:
            chat = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            dropped.append((path.stem, "file is not valid JSON"))
            continue
        problem = chat_problem(chat, split)
        if problem:
            dropped.append(
                (str(chat.get("id", path.stem)) if isinstance(chat, dict) else path.stem, problem)
            )
            continue
        if path.stem != chat["id"]:
            dropped.append((path.stem, "file name is not the chat id"))
            continue
        loaded.append(chat)
        kept = []
        for number in range(len(chat["questions"])):
            reason = _question_problem_s3(chat, number, split)
            if reason:
                dropped.append((f"{chat['id']}_q{number}", reason))
            else:
                kept.append(number)
        items += _items(chat, kept, split)
    return items, dropped, set_problems(loaded), digest.hexdigest()


# Model-free flags the eval records on every reply.


def copy_flag(s3: S3Item, reply: str) -> bool | None:
    """Wrong view, every kind but re_ask: True if the reply names the wrong reply's value."""
    if s3.view != WRONG_VIEW or s3.item.kind == RE_ASK:
        return None
    return s3.earlier_wrong_value.casefold() in reply.casefold()


def false_answer(s3: S3Item, reply: str) -> bool | None:
    """True if the reply names a value under ``wrong`` or another chat value of the asked category.

    A confirm's false claimed value is left out, since a right reply may name it while correcting
    it. None for a statement, which asks about no category.
    """
    if s3.category is None:
        return None
    text = reply.casefold()
    spared = {s3.item.answer.casefold()} if s3.item.answer else set()
    if s3.claimed_value:
        spared.add(s3.claimed_value.casefold())
    values = {v.casefold() for v in (*s3.item.forbidden, *s3.category_values)} - spared
    return any(value in text for value in values)


def never_told_right(s3: S3Item, reply: str) -> bool | None:
    """The fixed never-told rubric, model-free part: right when the reply names no chat value."""
    if s3.item.kind != NEVER_TOLD:
        return None
    return not false_answer(s3, reply)


def n_hit_query(message: str) -> str:
    """The model-free search for the N-hit flag: the message's content words, in order, once."""
    words = dict.fromkeys(re.findall(r"[a-z']+", message.casefold()))
    return " ".join(w for w in words if w not in STOP)


def draw_sample(items: list[S3Item], size: int = SAMPLE_SIZE, seed: int = SAMPLE_SEED) -> list[str]:
    """Return ``size`` item ids drawn by ``seed`` from every item, both views, in id order."""
    ids = sorted(s3.item.item_id for s3 in items)
    return sorted(random.Random(seed).sample(ids, min(size, len(ids))))
