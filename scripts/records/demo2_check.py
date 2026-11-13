"""R-201: check the Demo2 writer's files against the brief's rules, printing no chat text.

Nobody reads the chat or the questions before the run, so this prints only PASS or FAIL per rule,
with question numbers, and the number of content words each question shares with its source
message (R-201 lane, finding 7; R-176's word rule). The shared words themselves are written to
``results/demo2/overlap.json`` for the report after the run.

Usage:
    python scripts/records/demo2_check.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_overlap_r176 import words  # noqa: E402  R-176's content words

CHAT = REPO_ROOT / "demo2" / "chat.txt"
QUESTIONS = REPO_ROOT / "demo2" / "questions.json"
OUT = REPO_ROOT / "results" / "demo2" / "overlap.json"
KINDS = ["older"] * 6 + ["in_view"] * 2 + ["never_told"] * 4


def has(text: str, key: str) -> bool:
    return bool(re.search(rf"(?<!\w){re.escape(key.casefold())}(?!\w)", text.casefold()))


def main() -> None:
    messages = [m for m in CHAT.read_text(encoding="utf-8").splitlines() if m]
    qs = json.loads(QUESTIONS.read_text(encoding="utf-8"))["questions"]
    fails: dict[str, list[int]] = {}

    def check(rule: str, ok: bool, number: int = 0) -> None:
        fails.setdefault(rule, [])
        if not ok:
            fails[rule].append(number)

    check("24 messages", len(messages) == 24)
    check("12 questions, kinds in the brief's order", [q.get("kind") for q in qs] == KINDS)
    rows = []
    for n, q in enumerate(qs, 1):
        person = words(str(q.get("person", "")))
        shared_any = sorted(
            set().union(*(words(q["question"]) & words(m) for m in messages)) - person
        )
        row = {"number": n, "shared_with_any_message_besides_person": shared_any}
        if q["kind"] == "never_told":
            check(
                "never_told: source null, key 'never told'",
                q["source_message"] is None and q["key"] == "never told",
                n,
            )
            if n <= 10:
                check("never_told 9-10: no shared word besides the person", not shared_any, n)
            else:
                m = q.get("overlap_message")
                ok = isinstance(m, int) and 1 <= m <= 21
                shared = (
                    sorted(words(q["question"]) & words(messages[m - 1]) - person) if ok else []
                )
                check("never_told 11-12: shares a word with overlap_message 1-21", bool(shared), n)
                row["shared_with_overlap_message"] = shared
        else:
            s, key = q["source_message"], q["key"]
            low, high = (1, 21) if q["kind"] == "older" else (22, 24)
            check(
                "source message in range for its kind", isinstance(s, int) and low <= s <= high, n
            )
            if not isinstance(s, int) or not 1 <= s <= 24:
                continue
            check("key exactly as written in its source", key in messages[s - 1], n)
            check(
                "key in no other message",
                not any(has(m, key) for i, m in enumerate(messages, 1) if i != s),
                n,
            )
            check("key in no question", not any(has(x["question"], key) for x in qs), n)
            check(
                "key at least 4 letters, no digits", len(key) >= 4 and not re.search(r"\d", key), n
            )
            shared = sorted(words(q["question"]) & words(messages[s - 1]))
            row["shared_with_source"] = shared
            print(f"question {n}: {len(shared)} content words shared with its source")
        rows.append(row)
    check(
        "question 1 or 4 has other_value (look-alike)",
        any(qs[i].get("other_value") for i in (0, 3)),
    )
    check("older list I: one about the user", any(q.get("person") == "me" for q in qs[:3]))
    check("older list O: one about the user", any(q.get("person") == "me" for q in qs[3:6]))

    for rule, numbers in fails.items():
        print(
            f"{'FAIL' if numbers else 'PASS':5} {rule}"
            + (f" (questions {numbers})" if numbers else "")
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"record": "R-201", "rows": rows}, indent=1) + "\n", encoding="utf-8")
    print(f"== demo2 check: {sum(bool(v) for v in fails.values())} FAIL")


if __name__ == "__main__":
    main()
