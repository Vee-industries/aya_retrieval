"""R-199's check before training: K1.2's set against the registered lines, with K1 for scale.

Lines (a FAIL on any one means nothing trains):
1. Same evidence as K1: in every row, every turn with its facts mapped back to their template
   wording (found anywhere in a line, replies included) equals K1's byte for byte, so the same
   facts return, in the same order, with the same scores, and every reply's content is K1's.
2. Found against never_told mean passage gap at most 0.37; never_told rows with passages: all.
3. Four-word runs shared by the wordings the build can draw and hard_dev's forms: 0.
4. Returned lines of the asked type, by role: the drawn-wording share of answer lines and of decoys
   (other people) in found rows differ by at most 5 points; so do decoys in found and in never_told
   rows.
5. Rows whose returned lines of the asked type are all in the template wording: their share of
   found rows and of never_told rows differ by at most 5 points, compared separately for each number
   of such lines a search returns (each count with at least 30 rows on both sides).
Reported only: z statistics, the asked person's other lines (R-102's old values, other people with
the asked relation), facts wrapped in other words (R-102's corrections) and their drawn share,
replies that share four words with a template but state no whole fact, and the drawn share of all
facts.

Usage:
    python scripts/records/check_r199.py
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.conversations import NEEDS_SEARCH, NEVER_TOLD
from aya_retrieval.pool_hard_dev import HARD_DEV
from aya_retrieval.pools import TRAIN

HERE = Path(__file__).resolve().parent
NAME = "k1_2_r199"
MAX_GAP = 0.37
MAX_POINTS = 0.05
QUERIES = {t.statement: t.query.replace("{who}", "").strip() for t in TRAIN.facts.values()}


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


R196 = load_module("check_r196")


PATTERNS = [
    (re.compile(pattern.pattern, re.I), template, kind)
    for kind, patterns in (("template", R196.TEMPLATES), ("more", R196.MORE))
    for pattern, _used, template in patterns
]


def match(text: str):
    """Return (wording kind, template statement, match) for the fact in ``text``, else None."""
    for pattern, template, kind in PATTERNS:
        found = pattern.search(text)
        if found:
            return kind, template, found
    return None


def mapped(text: str, reply: bool = False) -> str:
    """``text`` with its fact in the template wording, as build_r199 would have had it."""
    got = match(text)
    if not got:
        return text
    _kind, template, found = got
    span, new = found.group(0), template.format(**found.groupdict())
    if reply and found.start() == 0 and span[0].isupper():
        new = new[0].upper() + new[1:]
    return text[: found.start()] + new + text[found.end() :]


def search_turns(row: dict) -> tuple[str, str, str]:
    """Return the query, the search output and the last reply of a row with a search."""
    turns = row["turns"]
    call = max(
        i for i, t in enumerate(turns) if t["role"] == "assistant" and "tool_name" in t["content"]
    )
    query = json.loads(turns[call]["content"])[0]["parameters"]["query"]
    return query, turns[call + 1]["content"], turns[-1]["content"]


def has_word(text: str, word: str) -> bool:
    return bool(re.search(rf"\b{re.escape(word.casefold())}\b", text.casefold()))


def mapped_turn(turn: dict) -> str:
    content = turn["content"]
    if R196.tool_output(turn):
        return re.sub(r"^User: (.*)$", lambda m: f"User: {mapped(m.group(1))}", content, flags=re.M)
    if turn["role"] == "user":
        return mapped(content)
    return content if "tool_name" in content else mapped(content, reply=True)


def roles(rows: list[dict]):
    """Wording counts of returned lines of the asked type by role, and all-template rows."""
    counts = {r: Counter() for r in ("answer", "asked_other", "found_decoy", "never_told_decoy")}
    all_template = {"found": Counter(), NEVER_TOLD: Counter()}  # (n lines, all template?) -> rows
    for row in rows:
        if row["kind"] not in NEEDS_SEARCH:
            continue
        query, output, reply = search_turns(row)
        side = NEVER_TOLD if row["kind"] == NEVER_TOLD else "found"
        kinds = []
        for line in re.findall(r"^User: (.*)$", output, re.M):
            got = match(line)
            if not got or not query.endswith(QUERIES[got[1]]):
                continue
            kind, _template, found = got
            fields = found.groupdict()
            kinds.append(kind)
            asked = has_word(query, fields["person"]) or has_word(query, fields["relation"])
            if side == NEVER_TOLD:
                role = "asked_other" if asked else "never_told_decoy"
            elif not asked:
                role = "found_decoy"
            else:
                role = "answer" if fields["value"].casefold() in reply.casefold() else "asked_other"
            counts[role][kind] += 1
        if kinds:
            all_template[side][(len(kinds), set(kinds) == {"template"})] += 1
    return counts, all_template


def share(c: Counter, key: str) -> float:
    return c[key] / max(1, sum(c.values()))


def z(a: Counter, b: Counter, key: str) -> float:
    n1, n2 = sum(a.values()), sum(b.values())
    p = (a[key] + b[key]) / max(1, n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / max(1, n1) + 1 / max(1, n2)))
    return 0.0 if se == 0 else (share(a, key) - share(b, key)) / se


def main() -> None:
    k1, k12 = R196.rows("k1_r178"), R196.rows(NAME)

    unlike = [
        b["id"]
        for a, b in zip(k1, k12, strict=True)
        if a["id"] != b["id"]
        or [mapped_turn(t) for t in b["turns"]] != [t["content"] for t in a["turns"]]
    ]

    s = R196.CHECK.stats(k12)
    gap = abs(s["found_mean"] - s["never_told_mean"])

    facts, wrapped, echoes = Counter(), Counter(), 0
    templates = [R196.grams(t.statement) for t in TRAIN.facts.values()]
    for row in k12:
        for turn in row["turns"]:
            content = turn["content"]
            if R196.tool_output(turn):
                texts = re.findall(r"^User: (.*)$", content, re.M)
            elif turn["role"] == "user":
                texts = [content]
            else:
                if "tool_name" not in content and not match(content):
                    echoes += any(R196.grams(content) & g for g in templates)
                continue
            for text in texts:
                got = match(text)
                if got:
                    kind, _template, found = got
                    facts[kind] += 1
                    if found.group(0) != text:
                        wrapped[kind] += 1
    # every wording the build can draw, a superset of those in use
    in_use = [t.statement for t in TRAIN.facts.values()] + [w for _p, w, _t in R196.MORE]
    hd_forms = [getattr(t, f) for t in HARD_DEV.facts.values() for f in R196.FIELDS]
    hd_grams = set().union(*(R196.grams(f) for f in hd_forms))
    shared = sorted({" ".join(g) for w in in_use for g in R196.grams(w) if g in hd_grams})

    c, at = roles(k12)
    d_answer = share(c["answer"], "more") - share(c["found_decoy"], "more")
    d_decoys = share(c["found_decoy"], "more") - share(c["never_told_decoy"], "more")
    by_n = []
    for n in sorted({n for side in at.values() for n, _ in side}):
        f = Counter({k: v for (m, k), v in at["found"].items() if m == n})
        t_ = Counter({k: v for (m, k), v in at[NEVER_TOLD].items() if m == n})
        if sum(f.values()) >= 30 and sum(t_.values()) >= 30:
            by_n.append((n, share(f, True), share(t_, True), sum(f.values()), sum(t_.values())))

    checks = [
        (f"rows unlike K1 beyond wording {len(unlike)} {unlike[:5]}", not unlike),
        (f"mean passage gap {gap:.2f} at most {MAX_GAP}", gap <= MAX_GAP),
        (
            f"never_told with passages {s['with_passages']} of {s['never_told']}",
            s["with_passages"] == s["never_told"],
        ),
        (f"four-word runs shared with hard_dev forms {len(shared)} {shared}", not shared),
        (
            f"drawn share, answers {share(c['answer'], 'more'):.1%} against found decoys "
            f"{share(c['found_decoy'], 'more'):.1%}, at most 5 points apart "
            f"(z {z(c['answer'], c['found_decoy'], 'more'):.2f})",
            abs(d_answer) <= MAX_POINTS,
        ),
        (
            f"drawn share, found decoys against never_told decoys "
            f"{share(c['never_told_decoy'], 'more'):.1%}, at most 5 points apart "
            f"(z {z(c['found_decoy'], c['never_told_decoy'], 'more'):.2f})",
            abs(d_decoys) <= MAX_POINTS,
        ),
    ]
    checks += [
        (
            f"all-template outputs with {n} same-type lines, found {f:.1%} ({nf} rows) against "
            f"never_told {nt:.1%} ({nn} rows), at most 5 points apart",
            abs(f - nt) <= MAX_POINTS,
        )
        for n, f, nt, nf, nn in by_n
    ]
    for text, ok in checks:
        print(f"{'PASS' if ok else 'FAIL':5} {text}")
    for role, counts in c.items():
        print(f"report: {role} {dict(counts)} drawn {share(counts, 'more'):.1%}")
    print(
        f"report: facts drawn {facts['more']} of {sum(facts.values())} "
        f"({share(facts, 'more'):.1%}); "
        f"wrapped facts drawn {wrapped['more']} of {sum(wrapped.values())}; replies sharing four "
        f"words with a template but stating no whole fact {echoes}; all-template counts {at}"
    )
    print(
        f"report: passages found {s['found_mean']:.2f}, "
        f"never_told {s['never_told_mean']:.2f}; never_told naming the asked person "
        f"{s['asked_person']}"
    )
    print(f"== {NAME} check: {sum(not ok for _, ok in checks)} FAIL (R-199 lines)")


if __name__ == "__main__":
    main()
