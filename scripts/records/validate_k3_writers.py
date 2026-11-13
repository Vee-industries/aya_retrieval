"""Validate K3-brief writer files (R-215): structure and the brief's checkable rules.

Usage: python scripts/records/validate_k3_writers.py FILE [FILE ...]

Per chat: 24 messages with ``user`` and ``assistant``; 11 questions of the brief's kinds (4 older,
2 check_true, 2 check_false, 2 never_told, 1 in_view); for older and check_true, ``source_message``
in 1 to 21 (in_view: 22 to 24) and the value written in that message; a query on every searching
question. Prints one line per file and exits 1 on any fault.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

KINDS = Counter(older=4, check_true=2, check_false=2, never_told=2, in_view=1)


def faults(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        return [f"does not parse: {e}"]
    out = []
    for c, chat in enumerate(data.get("chats", [])):
        msgs, qs = chat.get("messages", []), chat.get("questions", [])
        if len(msgs) != 24 or any(not m.get("user") or not m.get("assistant") for m in msgs):
            out.append(f"chat {c}: {len(msgs)} messages, or one without user or assistant")
        if Counter(q.get("kind") for q in qs) != KINDS:
            out.append(f"chat {c}: question kinds {dict(Counter(q.get('kind') for q in qs))}")
        for j, q in enumerate(qs):
            kind = q.get("kind")
            if kind != "in_view" and not q.get("query"):
                out.append(f"chat {c} q{j}: no query")
            if kind in ("older", "check_true", "in_view"):
                s = q.get("source_message")
                low, high = (22, 24) if kind == "in_view" else (1, 21)
                if not isinstance(s, int) or not low <= s <= high:
                    out.append(f"chat {c} q{j}: source_message {s}")
                elif str(q.get("value", "")) not in msgs[s - 1]["user"]:
                    out.append(f"chat {c} q{j}: value not in message {s}")
    if len(data.get("chats", [])) != 8:
        out.append(f"{len(data.get('chats', []))} chats")
    return out


def main() -> None:
    bad = 0
    for name in sys.argv[1:]:
        found = faults(Path(name))
        bad += bool(found)
        print(f"{'FAIL' if found else 'PASS'}  {Path(name).name}: {len(found)} faults {found[:4]}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
