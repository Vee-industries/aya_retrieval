"""Coherence: does a reply make sense as the next turn of the conversation?

Facts are scored by ``scoring``. This is the separate question of whether the reply follows from
what was said, marked by a judge blind to which model wrote it. The gate compares the same
conversations under both models, so the comparison is paired.
"""

from __future__ import annotations

import random

RUBRIC = """\
You see the last turns of a chat, the friend's newest message, and a reply.
Mark 1 if the reply is a sensible next turn: it responds to the newest message, fits what was said
in the turns shown, reads as ordinary language, and does not contradict or deny anything said there.
Mark 0 if it ignores the newest message, answers an older message instead, contradicts or denies
what was said, repeats itself, or breaks into tool syntax.
Do not mark on whether a fact is right, because you cannot see the whole chat. A reply that uses a
fact you cannot see is fine if it fits.
"""

SCORED_ARM = "tool_loop"


def sheet_lines(base_rows: list[dict], tuned_rows: list[dict], rng: random.Random):
    """Return shuffled judging lines with no model names, and the key that restores them.

    Raises:
        ValueError: If the two runs did not score the same conversations.
    """
    base = {row["id"]: row for row in base_rows if row["arm"] == SCORED_ARM}
    tuned = {row["id"]: row for row in tuned_rows if row["arm"] == SCORED_ARM}
    if base.keys() != tuned.keys():
        raise ValueError("the two runs did not score the same conversations")
    entries = [("base", row) for row in base.values()] + [("tuned", row) for row in tuned.values()]
    rng.shuffle(entries)
    sheet, key = [], []
    for line, (model, row) in enumerate(entries):
        sheet.append(
            {
                "line": line,
                "view": row["view"],
                "message": row["message"],
                "reply": row["reply"],
            }
        )
        key.append({"line": line, "model": model, "id": row["id"], "kind": row["kind"]})
    return sheet, key


def paired_counts(marks: dict[int, int], key: list[dict]) -> dict[str, int]:
    """Return coherent counts per model and how the pairs disagree.

    Args:
        marks: Line number to 1 or 0, from the judge.
        key: The key from ``sheet_lines``.

    Raises:
        ValueError: If any line has no mark, so no reply can be left out.
    """
    if set(marks) != {entry["line"] for entry in key}:
        raise ValueError("every line needs exactly one mark")
    by_id: dict[str, dict[str, int]] = {}
    for entry in key:
        by_id.setdefault(entry["id"], {})[entry["model"]] = marks[entry["line"]]
    return {
        "pairs": len(by_id),
        "base_coherent": sum(pair["base"] for pair in by_id.values()),
        "tuned_coherent": sum(pair["tuned"] for pair in by_id.values()),
        "only_base_coherent": sum(p["base"] > p["tuned"] for p in by_id.values()),
        "only_tuned_coherent": sum(p["tuned"] > p["base"] for p in by_id.values()),
    }
