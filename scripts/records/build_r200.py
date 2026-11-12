"""R-200: candidate K1.3's training set: K1.2, the template wording given by quota per role.

Usage: python scripts/records/build_r200.py

K1.3 = K1.2 (``build_r199.py``) with the template wording given by quota instead of by chance.
K1.2's one draw came out uneven between roles (found decoys 67% drawn, never_told decoys 83%;
R-200), which failed R-199's lines 4. Here:

1. Each fact in a row gets a role. In a search row's output, a line of the asked type is an answer,
   the asked person's other value, a found decoy or a never_told decoy (as ``check_r199.roles``
   classes them); a line of another type is found_other_type or never_told_other_type. Every other
   fact is "other".
2. Search rows are grouped by side (found, never_told) and by n, the number of asked-type lines
   their output returns. In each group exactly ``0.25 ** n`` of the rows, picked by a hashed
   order, have every such line in the template wording (check line 5); every other row keeps one
   of them drawn.
3. Within each role, the template wording then goes to a quarter of the occurrences (row, fact),
   counting those from step 2, filled in a hashed order (check line 4).
4. A fact not kept in the template takes one of ``build_r196.WORDINGS`` (the template excluded),
   drawn from a hash of row and fact with a salt of its own.

A fact has one wording within a row; across rows the same fact is drawn again (K1.2 gave it one
wording everywhere). A fact kept in the template wording is left byte for byte as K1 had it. Finding
facts anywhere in a line, rewording replies that repeat them, and keeping every search result,
score and reply's content as K1's are as in K1.2.

This changes only the training rows. Every evaluation keeps the plain keyword search.
``scripts/records/check_r199.py --set k1_3_r200`` then checks the set before any training.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

from aya_retrieval.conversations import NEEDS_SEARCH, NEVER_TOLD
from aya_retrieval.provenance import run_metadata

HERE = Path(__file__).resolve().parent
BASE = Path("data/screens/k1_r178.jsonl")
OUT = Path("data/screens/k1_3_r200.jsonl")
SALT = "R-200"
TEMPLATE_SHARE = 0.25


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


K12 = load("build_r199")
CHECK = load("check_r199")


def fact(text: str):
    """Return the template fact in ``text`` (casefolded key, match), else None."""
    for pattern, _statement in K12.PATTERNS:
        found = pattern.search(text)
        if found:
            return found.group(0).casefold(), found
    return None


def texts(turn: dict) -> list[tuple[str, bool]]:
    """The texts of a turn that can state a fact, each with whether it is a reply."""
    content = turn["content"]
    if content.startswith("Tool result for"):
        return [(line, False) for line in re.findall(r"^User: (.*)$", content, re.M)]
    if turn["role"] == "user":
        return [(content, False)]
    return [] if "tool_name" in content else [(content, True)]


def roles(row: dict) -> tuple[dict[str, str], str | None, int]:
    """Roles of the facts a search row's output returns, by fact key; the side; the number of
    returned lines of the asked type. Lines of other types get a role of their own per side."""
    if row["kind"] not in NEEDS_SEARCH:
        return {}, None, 0
    query, output, reply = CHECK.search_turns(row)
    side = NEVER_TOLD if row["kind"] == NEVER_TOLD else "found"
    out, n = {}, 0
    for line in re.findall(r"^User: (.*)$", output, re.M):
        got = CHECK.match(line)
        if not got:
            continue
        key = got[2].group(0).casefold()
        if not query.endswith(CHECK.QUERIES[got[1]]):
            out[key] = f"{side}_other_type"
            continue
        n += 1
        fields = got[2].groupdict()
        asked = CHECK.has_word(query, fields["person"]) or CHECK.has_word(query, fields["relation"])
        if side == NEVER_TOLD:
            role = "asked_other" if asked else "never_told_decoy"
        elif not asked:
            role = "found_decoy"
        else:
            role = "answer" if fields["value"].casefold() in reply.casefold() else "asked_other"
        out[key] = role
    return out, side, n


def digest(*parts: str) -> int:
    return int.from_bytes(hashlib.sha256("|".join((SALT, *parts)).encode()).digest()[:8], "big")


ASKED_TYPE = {"answer", "asked_other", "found_decoy", "never_told_decoy"}


def main() -> None:
    provenance = run_metadata()
    base_text = BASE.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]

    # Every (row, fact) by role, and each search row's returned asked-type facts by (side, count).
    by_role, asked_lines, groups = defaultdict(set), {}, defaultdict(list)
    for row in rows:
        role_of, side, n = roles(row)
        for turn in row["turns"]:
            for text, _reply in texts(turn):
                got = fact(text)
                if got:
                    by_role[role_of.get(got[0], "other")].add((row["id"], got[0]))
        if n:
            asked_lines[row["id"]] = [(row["id"], k) for k, r in role_of.items() if r in ASKED_TYPE]
            groups[(side, n)].append(row["id"])

    # 1. Rows whose returned asked-type lines are all template: exactly 0.25 ** n of each group,
    #    so check line 5 holds on both sides; every other search row keeps one of them drawn.
    template, drawn = set(), set()
    for (_side, n), ids in groups.items():
        ordered = sorted(ids, key=lambda i: digest("all", i))
        chosen = set(ordered[: round(TEMPLATE_SHARE**n * len(ordered))])
        for row_id in ids:
            if row_id in chosen:
                template.update(asked_lines[row_id])
            else:
                drawn.add(min(asked_lines[row_id], key=lambda o: digest("keep", *o)))
    # 2. Each role's quota (a quarter template), filled from the occurrences still open.
    for occurrences in by_role.values():
        target = round(TEMPLATE_SHARE * len(occurrences)) - len(occurrences & template)
        open_ = sorted(occurrences - template - drawn, key=lambda o: digest("quota", *o))
        template.update(open_[: max(0, target)])

    def reworded(row_id: str, text: str, reply: bool) -> str:
        got = fact(text)
        if not got:
            return text
        key, found = got
        statement = next(s for p, s in K12.PATTERNS if p.pattern == found.re.pattern)
        if (row_id, key) in template:
            return text
        wording = random.Random(digest("wording", row_id, key)).choice(K12.WORDINGS[statement])
        new = wording.format(**found.groupdict())
        if reply and found.start() == 0 and found.group(0)[0].isupper():
            new = new[0].upper() + new[1:]
        return text[: found.start()] + new + text[found.end() :]

    def reworded_turn(row_id: str, turn: dict) -> dict:
        content = turn["content"]
        if content.startswith("Tool result for"):
            content = re.sub(
                r"^User: (.*)$",
                lambda m: f"User: {reworded(row_id, m.group(1), False)}",
                content,
                flags=re.M,
            )
        elif turn["role"] == "user":
            content = reworded(row_id, content, False)
        elif "tool_name" not in content:
            content = reworded(row_id, content, True)
        return {**turn, "content": content}

    out = [{**row, "turns": [reworded_turn(row["id"], t) for t in row["turns"]]} for row in rows]
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in out)
    OUT.write_text(text, encoding="utf-8")
    report = {
        "provenance": provenance,
        "record": "R-200",
        "base_set": BASE.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(out),
        "rows_changed": sum(a != b for a, b in zip(rows, out, strict=True)),
        "occurrences_by_role": {r: len(o) for r, o in sorted(by_role.items())},
        "template_by_role": {
            r: sum(o in template for o in occ) for r, occ in sorted(by_role.items())
        },
        "all_template_rows": {
            f"{side} {n}": [sum(set(asked_lines[i]) <= template for i in ids), len(ids)]
            for (side, n), ids in sorted(groups.items())
        },
    }
    OUT.with_suffix(".provenance.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(f"{OUT}: {report['rows']} rows, {report['rows_changed']} changed")


if __name__ == "__main__":
    main()
