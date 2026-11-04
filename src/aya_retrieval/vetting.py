"""Vet `statement` training targets with a blind judge before training (fix 10, R-058).

Statement rows train on base's own reply with no tool in sight. Some of those replies are weak
("Lucia is a great name."), and the adapter copies them (R-057). A judge marks every statement
target on the coherence rubric, without knowing which rows are spares; each target marked
incoherent is swapped for a spare row the judge marked coherent.
"""

from __future__ import annotations

import random

from aya_retrieval.conversations import STATEMENT

SOURCES = ("data", "spare")


def statement_sheet(
    data: list[dict], spare: list[dict], rng: random.Random
) -> tuple[list[dict], list[dict]]:
    """Return a shuffled sheet of every statement target in ``data`` and ``spare``, and its key.

    Sheet lines have the turns in view, the friend's message and the reply, as
    ``render_judge_sheet.render`` prints them; the key says which file and row each line came from.
    """
    entries = [
        (source, row)
        for source, rows in zip(SOURCES, (data, spare), strict=True)
        for row in rows
        if row["kind"] == STATEMENT
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
    data: list[dict], spare: list[dict], key: list[dict], marks: dict[int, int]
) -> tuple[list[dict], dict[str, int]]:
    """Return ``data`` with each statement row marked 0 swapped for a spare row marked 1.

    Spares are used in file order, each once, and a spare repeating a kept row's message is
    skipped, so the set keeps as many distinct messages as it can. Raises ValueError if the
    spares run out or a statement line has no mark.
    """
    mark = {(entry["source"], entry["id"]): marks[entry["line"]] for entry in key}
    kept_messages = {
        row["turns"][-2]["content"]
        for row in data
        if row["kind"] == STATEMENT and mark[("data", row["id"])] == 1
    }
    good_spares = [
        row for row in spare if row["kind"] == STATEMENT and mark[("spare", row["id"])] == 1
    ]
    fresh = [row for row in good_spares if row["turns"][-2]["content"] not in kept_messages]
    queue = fresh + [row for row in good_spares if row not in fresh]

    out, rejected = [], 0
    for row in data:
        if row["kind"] == STATEMENT and mark[("data", row["id"])] == 0:
            if not queue:
                raise ValueError("not enough coherent spare rows to replace every rejected target")
            out.append({**queue.pop(0), "id": f"{row['id']}_vetted"})
            rejected += 1
        else:
            out.append(row)
    tally = {
        "statement_targets": sum(row["kind"] == STATEMENT for row in data),
        "rejected": rejected,
        "spares_coherent": len(good_spares),
        "spares_used": rejected,
    }
    return out, tally
