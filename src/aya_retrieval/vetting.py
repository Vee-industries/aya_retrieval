"""Vet training targets of one kind with a blind judge before training (fix 10, R-058; fix 12).

Statement and in_view rows train on base's own reply. Some of those replies are weak ("Lucia is a
great name."), and the adapter copies them (R-057). A judge marks every target of the kind on the
coherence rubric, without knowing which rows are spares; each target marked incoherent is swapped
for a spare row the judge marked coherent.
"""

from __future__ import annotations

import random

from aya_retrieval.conversations import STATEMENT

SOURCES = ("data", "spare")

# For vetting training targets only; evaluation keeps the coherence rubric. Its first sentences are
# that rubric's; the rest names faults that rubric leaves to the judge, which the first vetting let
# through and the adapter then learned (R-077).
TARGET_RUBRIC = """\
You see the last turns of a chat, the friend's newest message, and a reply.
Mark 1 if the reply is a sensible next turn: it responds to the newest message, fits what was said
in the turns shown, reads as ordinary language, and does not contradict or deny anything said there.
Mark 0 if it ignores the newest message, answers an older message instead, contradicts or denies
what was said, repeats itself, or breaks into tool syntax.
Also mark 0 if it gets the feeling wrong (treats a complaint, a worry or bad news as good news, or
good news as bad); mixes up who is who or who did what (calls the friend by another person's name,
or treats the friend as the one going away, visiting or forgetting when it is someone else, or the
reverse); asks for something the friend has just said; or adds a detail that does not fit.
Do not mark on whether a fact is right, because you cannot see the whole chat. A reply that uses a
fact you cannot see is fine if it fits.
"""


def all_judges(marks: list[dict[int, int]]) -> dict[int, int]:
    """Return 1 for a line only where every judge marked it 1.

    Raises:
        ValueError: If the judges did not mark the same lines.
    """
    lines = set(marks[0])
    if any(set(judge) != lines for judge in marks):
        raise ValueError("judges marked different lines")
    return {line: min(judge[line] for judge in marks) for line in lines}


def target_sheet(
    data: list[dict], spare: list[dict], rng: random.Random, kind: str = STATEMENT
) -> tuple[list[dict], list[dict]]:
    """Return a shuffled sheet of every ``kind`` target in ``data`` and ``spare``, and its key.

    Sheet lines have the turns in view, the friend's message and the reply, as
    ``render_judge_sheet.render`` prints them; the key says which file and row each line came from.
    """
    entries = [
        (source, row)
        for source, rows in zip(SOURCES, (data, spare), strict=True)
        for row in rows
        if row["kind"] == kind
    ]
    rng.shuffle(entries)
    sheet, key = [], []
    for line, (source, row) in enumerate(entries):
        turns = row["turns"]
        view = [(turns[i]["content"], turns[i + 1]["content"]) for i in range(0, len(turns) - 2, 2)]
        sheet.append(
            {
                "line": line,
                "view": view,
                "message": turns[-2]["content"],
                "reply": turns[-1]["content"],
            }
        )
        key.append({"line": line, "source": source, "id": row["id"]})
    return sheet, key


def replace_rejected(
    data: list[dict],
    spare: list[dict],
    key: list[dict],
    marks: dict[int, int],
    kind: str = STATEMENT,
) -> tuple[list[dict], dict[str, int]]:
    """Return ``data`` with each ``kind`` row marked 0 swapped for a spare row marked 1.

    Spares are used in file order, each once, and a spare repeating a kept row's message is
    skipped, so the set keeps as many distinct messages as it can. Raises ValueError if the
    spares run out or a line has no mark.
    """
    mark = {(entry["source"], entry["id"]): marks[entry["line"]] for entry in key}
    kept_messages = {
        row["turns"][-2]["content"]
        for row in data
        if row["kind"] == kind and mark[("data", row["id"])] == 1
    }
    good_spares = [row for row in spare if row["kind"] == kind and mark[("spare", row["id"])] == 1]
    fresh = [row for row in good_spares if row["turns"][-2]["content"] not in kept_messages]
    queue = fresh + [row for row in good_spares if row not in fresh]

    out, rejected = [], 0
    for row in data:
        if row["kind"] == kind and mark[("data", row["id"])] == 0:
            if not queue:
                raise ValueError("not enough coherent spare rows to replace every rejected target")
            out.append({**queue.pop(0), "id": f"{row['id']}_vetted"})
            rejected += 1
        else:
            out.append(row)
    tally = {
        "kind": kind,
        "targets": sum(row["kind"] == kind for row in data),
        "rejected": rejected,
        "spares_coherent": len(good_spares),
        "spares_used": rejected,
    }
    return out, tally


def splice_kind(into: list[dict], rows: list[dict], kind: str) -> list[dict]:
    """Return ``into`` with its ``kind`` rows replaced, in order, by the ``kind`` rows of ``rows``.

    Every other row keeps its place, so the rest of a training set stays exactly as it was. Raises
    ValueError unless both have the same number of ``kind`` rows.
    """
    new = [row for row in rows if row["kind"] == kind]
    if len(new) != sum(row["kind"] == kind for row in into):
        raise ValueError(f"{kind} row counts differ")
    supply = iter(new)
    return [next(supply) if row["kind"] == kind else row for row in into]
