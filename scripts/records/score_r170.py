"""R-170: score the LongMemEval-S outside check, mechanically, on every arm that completed.

Usage:
    python -I scripts/records/score_r170.py \
        --data C:/Users/Gaming/Downloads/longmemeval/longmemeval_s_cleaned.json \
        --index C:/scratch/score_r170.sqlite

Why: R-170 registered its measures before any run, and this computes them (all but the judged
accuracy, measure 4, which comes from judge sheets). Measure 1, evidence found: a search counts if
a passage it returned comes from an exchange holding a ``has_answer`` turn, read on the marked
questions outside the 3 with evidence in view, at the first search's top 5, over all searches,
with the share of questions searched beside it; the same at session level, and "evidence shown"
(the gold in the passage text the model was given); two CPU references, a search on the question
text and 5 random passages. Measure 2, the gold in the reply, normalised and matched on word
boundaries, with number words as digits and alternatives split by the rule below; preference
questions and temporal questions whose gold is not a single value are not read, a list fixed from
the golds alone and written before any run. The scorer must pass every gold as a reply and fail
known-wrong replies, or it stops. Beside them: each arm's false-match rate (its replies against
another question's gold), reply length, the 60-token cap. Measure 3, abstention on the 30 ``_abs``
questions by R-170's wording list, with the refusal rate on the 470 answerable ones. Measure 5,
clean calls, tokens read per turn, seconds per question, failures. Then H1 to H3: paired exact sign
tests and 95% intervals resampling questions, on the questions every full arm completed, and again
counting a failure as wrong for that arm only. An arm that did not complete is not reported. The
data is read only through ``aya_retrieval.longmemeval``. Writes aggregates only (no chat, question
or answer text) to results/analysis/R-170/scores.json, and the question ids measure 2 reads to
results/analysis/R-170/answer_read_ids.json.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import statistics
from collections import Counter
from pathlib import Path

from aya_retrieval.longmemeval import exchange_index, load_longmemeval, passages
from aya_retrieval.provenance import REPO_ROOT, run_metadata
from aya_retrieval.recall_tool import TOP_K, build_search_tool
from aya_retrieval.scoring import clean_call
from aya_retrieval.stats import bootstrap_gain_interval, exact_sign_test

RESULTS = REPO_ROOT / "results" / "longmemeval"
OUT = REPO_ROOT / "results" / "analysis" / "R-170"
# R-170's arms, in its run order: name -> (results label, runner arm).
ARMS = {
    "637_tool": ("lme_637_82_tool", "tool_loop"),
    "base_tool": ("lme_base_tool", "tool_loop"),
    "always_search": ("lme_base_as", "always_search"),
    "three_exchanges": ("lme_base_three", "three_exchanges"),
    "evidence_only": ("lme_base_evidence", "evidence_only"),
}
ADAPTER_ARM = "637_tool"  # the only arm that runs an adapter; the rest are base
FULL_ARMS = ("637_tool", "base_tool", "always_search", "three_exchanges")  # run on every question
SEARCH_ARMS = ("637_tool", "base_tool", "always_search")
REFERENCES = ("question_search", "random_passages")  # R-170's two CPU references
TRAINED_FOR = ("single-session-user", "knowledge-update")
PREFERENCE = "single-session-preference"
TEMPORAL = "temporal-reasoning"
SEED = 170
RANDOM_PASSAGES = 5
SHOWN = 350  # the tool shows each passage's first 350 characters
MAX_TOKENS = 60  # run_recall_eval.MAX_TOKENS, the cap on each reply

# The alternatives rule, written before any run (R-170, measure 2):
# - "X. Y (...) is also acceptable." gives X and Y, the bracket dropped; "X. Answers ranging from
#   N [unit] to M <unit> are also acceptable." gives X and each whole number N to M with the unit;
# - "X (or Y, ...)" gives X without the bracket, and Y up to its first comma;
# - "X or Y" gives X and Y only for a gold of at most 6 words with no punctuation, since in a
#   longer sentence "or" joins parts of one answer ("I replaced or fixed five items: ...").
ALSO_ACCEPTABLE = re.compile(
    r"^(?P<first>.+?)\.\s+(?P<second>.+?)\s+(?:is|are) also acceptable\.?$", re.I
)
RANGE = re.compile(
    r"^answers ranging from (?P<low>\d+) (?:\w+ )?to (?P<high>\d+) (?P<unit>\w+)$", re.I
)
OR_BRACKET = re.compile(r"\(or\s+(?P<other>[^),]+)[^)]*\)", re.I)
OR_SPLIT_WORDS = 6
# A temporal gold is a single value when each alternative has at most this many words, normalised.
SINGLE_VALUE_WORDS = 4
ARTICLES = {"a", "an", "the"}
UNITS = (
    "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen "
    "fifteen sixteen seventeen eighteen nineteen"
).split()
TENS = {
    name: 10 * n
    for n, name in enumerate("_ _ twenty thirty forty fifty sixty seventy eighty ninety".split())
    if n >= 2
}
# R-170, measure 3: written before any run and taken from no model output.
DECLINES = (
    "don't know",
    "do not know",
    "no information",
    "not mentioned",
    "didn't mention",
    "did not mention",
    "can't recall",
    "cannot recall",
    "don't have",
    "do not have",
    "not sure",
    "no record",
    "haven't told",
    "never told",
    "never mentioned",
)
KNOWN_WRONG = ("I don't know.", "Sure, I can help with that.", "")


def words(text: str) -> list[str]:
    """Return ``text`` normalised: case folded, apostrophes and punctuation out, no articles,
    number words as digits ("twenty-five" is "25")."""
    text = text.casefold().replace("\u2019", "").replace("\u2018", "").replace("'", "")
    tokens = [t for t in re.findall(r"[^\W_]+", text) if t not in ARTICLES]
    out, i = [], 0
    while i < len(tokens):
        token = tokens[i]
        if token in TENS:
            value = TENS[token]
            if i + 1 < len(tokens) and tokens[i + 1] in UNITS[1:10]:
                value += UNITS.index(tokens[i + 1])
                i += 1
            out.append(str(value))
        elif token in UNITS:
            out.append(str(UNITS.index(token)))
        else:
            out.append(token)
        i += 1
    return out


def alternatives(gold: str) -> list[str]:
    """Return the forms of ``gold`` that count, by the rule written above."""
    gold = gold.strip()
    also = ALSO_ACCEPTABLE.match(gold)
    bracket = OR_BRACKET.search(gold)
    if also:
        second = re.sub(r"\([^)]*\)", "", also["second"]).strip()
        span = RANGE.match(second)
        if span:
            low, high = int(span["low"]), int(span["high"])
            forms = [also["first"], *(f"{n} {span['unit']}" for n in range(low, high + 1))]
        else:
            forms = [also["first"], second]
    elif bracket:
        forms = [OR_BRACKET.sub("", gold), bracket["other"]]
    elif len(words(gold)) <= OR_SPLIT_WORDS and not re.search(r"[.,;:!?]", gold):
        forms = re.split(r"\s+or\s+", gold, flags=re.I)
    else:
        forms = [gold]
    return [form.strip() for form in forms if words(form)]


def contains(haystack: list[str], needle: list[str]) -> bool:
    """Return True if ``needle`` appears in ``haystack`` as consecutive whole words."""
    n = len(needle)
    return n > 0 and any(haystack[i : i + n] == needle for i in range(len(haystack) - n + 1))


def matches(reply: str | None, gold: str) -> bool:
    """Return True if the reply holds one of the gold's forms, on word boundaries."""
    said = words(reply or "")
    return any(contains(said, words(form)) for form in alternatives(gold))


def single_value(gold: str) -> bool:
    """Return True if every form of ``gold`` is at most ``SINGLE_VALUE_WORDS`` words."""
    forms = alternatives(gold)
    return bool(forms) and all(len(words(form)) <= SINGLE_VALUE_WORDS for form in forms)


def answer_read(kind: str, gold: str, abstention: bool) -> str | None:
    """Return why measure 2 does not read a question, or None if it does; golds alone decide."""
    if abstention:
        return "abstention (measure 3)"
    if kind == PREFERENCE:
        return "preference: the gold is a rubric"
    if kind == TEMPORAL and not single_value(gold):
        return "temporal: the gold is not a single value"
    return None


def declines(reply: str | None) -> bool:
    """Return True if the reply uses a wording from R-170's list."""
    text = (reply or "").casefold().replace("\u2019", "'")
    return any(re.search(rf"\b{re.escape(phrase)}\b", text) for phrase in DECLINES)


def shifted(gold: str) -> str:
    """Return the gold, normalised, with every number moved up by ten: a known-wrong reply."""
    return " ".join(str(int(w) + 10) if w.isdigit() else w for w in words(gold))


def check_answer_scorer(golds: dict[str, str]) -> dict:
    """Return the self-test's counts; every gold and form must pass, every known-wrong fail."""
    failed = []
    for item_id, gold in sorted(golds.items()):
        replies = [gold, *alternatives(gold)]
        if not all(matches(reply, gold) for reply in replies):
            failed.append((item_id, "gold as reply"))
        if any(matches(reply, gold) for reply in KNOWN_WRONG):
            failed.append((item_id, "known-wrong reply"))
        if all(any(w.isdigit() for w in words(f)) for f in alternatives(gold)):
            if matches(shifted(gold), gold):
                failed.append((item_id, "numbers moved by ten"))
    return {"golds": len(golds), "failed": failed}


def false_match_partners(ids: list[str], seed: int = SEED) -> dict[str, str]:
    """Return, for each id, another id whose gold its reply is scored against (a fixed shuffle)."""
    order = sorted(ids)
    random.Random(seed).shuffle(order)
    return {order[i]: order[(i + 1) % len(order)] for i in range(len(order))}


def false_match_rate(replies: dict[str, str], golds: dict[str, str], seed: int = SEED) -> dict:
    """Return how many replies hold another question's gold, of how many were scored."""
    if len(replies) < 2:
        return {"matches": 0, "of": len(replies)}
    partners = false_match_partners(list(replies), seed)
    hits = sum(matches(replies[i], golds[partners[i]]) for i in replies)
    return {"matches": hits, "of": len(replies), "rate": round(hits / len(replies), 4)}


def share(hits: int, total: int) -> dict:
    return {"hits": hits, "of": total, "rate": round(hits / total, 4) if total else None}


def load_arm(name: str, digest: str, questions: int) -> dict | None:
    """Return a completed arm's rows by id, or None if it did not run or did not complete."""
    label, arm = ARMS[name]
    path = RESULTS / f"{label}.json"
    if not path.exists():
        return None
    report = json.loads(path.read_text(encoding="utf-8"))
    if report["data_sha256"] != digest or report["arm"] != arm:
        raise ValueError(f"{path} is not {arm} on R-170's data")
    if (report["adapter"] is None) != (name != ADAPTER_ARM):
        raise ValueError(f"{path}: only {ADAPTER_ARM} runs an adapter")
    if not report["completed"] or report["ids_file"] or len(report["rows"]) != questions:
        return {"status": "not completed"}
    return {"status": "completed", "report": report, "rows": {r["id"]: r for r in report["rows"]}}


def shown_text(contents: list[str]) -> str:
    """Return the text the tool shows for these passages: the first 350 characters of each."""
    return "\n\n".join(content[:SHOWN] for content in contents)


def done(row: dict | None) -> bool:
    """Return True if the arm ran this question to a reply."""
    return bool(row) and not row.get("error") and not row.get("skipped")


def evidence_outcome(
    doc_lists: list[list[str]], texts: list[str], turn: set, session: set, gold: str
) -> dict:
    """Return what one question's searches found: each search's top 5 and the text shown."""
    hit = [any(exchange_index(d) in turn for d in docs) for docs in doc_lists]
    hit_session = [any(exchange_index(d) in session for d in docs) for docs in doc_lists]
    seen = [matches(text, gold) for text in texts]
    return {
        "searched": bool(doc_lists),
        "first": bool(hit) and hit[0],
        "any": any(hit),
        "first_session": bool(hit_session) and hit_session[0],
        "any_session": any(hit_session),
        "first_shown": bool(seen) and seen[0],
        "any_shown": any(seen),
        "passages": sum(len(docs) for docs in doc_lists),
    }


def evidence_measures(table: dict[str, dict], ids: list[str], shown_ids: list[str], kinds) -> dict:
    """Measure 1 on ``ids``: searched, then found at the first search and at any, by type."""
    rows = [table[i] for i in ids if i in table]
    searched = [r for r in rows if r["searched"]]
    shown = [table[i] for i in shown_ids if i in table and table[i]["searched"]]

    def count(chosen: list[dict], field: str) -> dict:
        return share(sum(r[field] for r in chosen), len(chosen))

    out = {
        "questions": len(ids),
        "completed": len(rows),
        "searched": share(len(searched), len(rows)),
        "first_search_turn": count(searched, "first"),
        "any_search_turn": count(searched, "any"),
        "first_search_session": count(searched, "first_session"),
        "any_search_session": count(searched, "any_session"),
        "passages_per_searched_question": (
            round(statistics.fmean(r["passages"] for r in searched), 2) if searched else None
        ),
        "evidence_shown_first": count(shown, "first_shown"),
        "evidence_shown_any": count(shown, "any_shown"),
        "by_type": {},
    }
    for kind in sorted({kinds[i] for i in ids}):
        typed = [table[i] for i in ids if kinds[i] == kind and i in table]
        typed = [r for r in typed if r["searched"]]
        out["by_type"][kind] = {
            "trained_for": kind in TRAINED_FOR,
            "first_search_turn": count(typed, "first"),
            "any_search_turn": count(typed, "any"),
        }
    return out


def paired(first: dict[str, int], second: dict[str, int], ids: list[str]) -> dict:
    """Exact sign test and question-resampled 95% interval of first minus second, on ``ids``.

    A question missing from ``first`` or ``second`` counts as wrong for that arm.
    """
    a, b = [first.get(i, 0) for i in ids], [second.get(i, 0) for i in ids]
    only_first = sum(x and not y for x, y in zip(a, b, strict=True))
    only_second = sum(y and not x for x, y in zip(a, b, strict=True))
    out = {
        "n": len(ids),
        "first": sum(a),
        "second": sum(b),
        "only_first": only_first,
        "only_second": only_second,
        "p": exact_sign_test(only_first, only_second),
    }
    if len(ids) >= 2:
        difference = bootstrap_gain_interval(b, [a], seed=SEED)["difference"]
        out["difference_and_95_interval"] = [round(x, 4) for x in difference]
    return out


def two_readings(
    first: dict[str, int], second: dict[str, int], ids: list[str], completed: set[str]
) -> dict:
    """The paired test on the questions every full arm completed, then on all of ``ids``.

    ``first`` and ``second`` hold the questions each arm completed, so in the second reading a
    failure counts as wrong for that arm only.
    """
    return {
        "completed_by_every_arm": paired(first, second, [i for i in ids if i in completed]),
        "failures_wrong": paired(first, second, ids),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--data", type=Path, required=True, help="longmemeval_s_cleaned.json")
    parser.add_argument("--index", type=Path, required=True, help="scratch database path")
    args = parser.parse_args()

    items, digest = load_longmemeval(args.data)
    by_id = {item.item_id: item for item in items}
    kinds = {item.item_id: item.kind for item in items}
    golds = {item.item_id: item.answer for item in items}
    not_read = {i.item_id: answer_read(i.kind, i.answer, i.abstention) for i in items}
    read = sorted(i for i, why in not_read.items() if why is None)
    rule_counts = dict(sorted(Counter(why or "read" for why in not_read.values()).items()))
    OUT.mkdir(parents=True, exist_ok=True)
    fixed = {"record": "R-170", "data_sha256": digest, "rule_counts": rule_counts, "ids": read}
    (OUT / "answer_read_ids.json").write_text(json.dumps(fixed, indent=1), encoding="utf-8")
    self_test = check_answer_scorer({i: golds[i] for i in read})
    if self_test["failed"]:
        raise SystemExit(f"the answer scorer fails its self-test: {self_test['failed']}")

    evidence_ids = sorted(
        i.item_id for i in items if i.evidence_indexes() and not i.evidence_in_view()
    )
    shown_ids = sorted(set(evidence_ids) & set(read))
    abstention_ids = sorted(i.item_id for i in items if i.abstention)
    answerable_ids = sorted(i.item_id for i in items if not i.abstention)
    arms = {name: load_arm(name, digest, len(items)) for name in ARMS}
    ran = {name: arm["rows"] for name, arm in arms.items() if arm and arm["status"] == "completed"}
    finished = {name: {i: r for i, r in rows.items() if done(r)} for name, rows in ran.items()}
    completed = set(by_id)
    for name in FULL_ARMS:
        completed &= set(finished.get(name, by_id))

    # Rebuild each question's index on the CPU: the references search it, and each logged search
    # is run again to recover the passage text the model was shown (without the tool's headers,
    # whose chunk numbers and scores would match a numeric gold).
    found: dict[str, dict[str, dict]] = {name: {} for name in [*ran, *REFERENCES]}
    not_reproduced = dict.fromkeys(ran, 0)
    for item_id in evidence_ids:
        item = by_id[item_id]
        marks = (set(item.evidence_indexes()), set(item.answer_session_indexes()), golds[item_id])
        tool = build_search_tool(item.older(), args.index, match_all=False)

        def search(query: str, tool=tool) -> tuple[list[str], str]:
            hits = tool.backend.search(query, top_k=TOP_K)
            doc_ids = [hit["metadata"]["doc_id"] for hit in hits]
            return doc_ids, shown_text([hit["content"] for hit in hits])

        docs, text = search(item.question)
        found["question_search"][item_id] = evidence_outcome([docs], [text], *marks)
        pool = passages(item.older())
        drawn = random.Random(f"{SEED}:{item_id}").sample(pool, min(RANDOM_PASSAGES, len(pool)))
        found["random_passages"][item_id] = evidence_outcome(
            [[p["doc_id"] for p in drawn]], [shown_text([p["text"] for p in drawn])], *marks
        )
        for name in ran:
            row = finished[name].get(item_id)
            if name not in SEARCH_ARMS or not row:
                continue
            again = [search(q) for q in row["queries"][: len(row["doc_ids"])]]
            not_reproduced[name] += [docs for docs, _ in again] != row["doc_ids"]
            texts = [text for _, text in again]
            found[name][item_id] = evidence_outcome(row["doc_ids"], texts, *marks)
    args.index.unlink(missing_ok=True)

    report = {
        "provenance": run_metadata(),
        "record": "R-170",
        "data_sha256": digest,
        "arms": {name: (arm or {"status": "not run"})["status"] for name, arm in arms.items()},
        "answer_scorer_self_test": {"golds": self_test["golds"], "failed": 0},
        "answer_read": {"rule_counts": rule_counts, "read": len(read)},
        "evidence_questions": len(evidence_ids),
        "evidence_shown_questions": len(shown_ids),
        "abstention_questions": len(abstention_ids),
        "completed_by_every_full_arm": (
            len(completed) if all(n in ran for n in FULL_ARMS) else None
        ),
        "references": {
            name: evidence_measures(found[name], evidence_ids, shown_ids, kinds)
            for name in REFERENCES
        },
        "measures": {},
        "hypotheses": {},
    }
    scores = {}
    for name, rows in ran.items():
        meta, done_rows = arms[name]["report"], finished[name]
        replies = {i: r["reply"] for i, r in done_rows.items()}
        scores[name] = {
            "first": {i: int(o["first"]) for i, o in found[name].items()},
            "any": {i: int(o["any"]) for i, o in found[name].items()},
            "answer": {i: int(matches(replies[i], golds[i])) for i in read if i in replies},
            "declines": {i: int(declines(r)) for i, r in replies.items()},
        }
        right, refused = scores[name]["answer"], scores[name]["declines"]
        searching = [r for r in done_rows.values() if r.get("queries")]

        def mean(field: str, places: int = 1, rows=done_rows) -> float | None:
            values = [r[field] for r in rows.values()]
            return round(statistics.fmean(values), places) if values else None

        lengths = [len(r or "") for r in replies.values()]
        word_counts = [len((r or "").split()) for r in replies.values()]
        entry = {
            "failures": sum(bool(r.get("error")) for r in rows.values()),
            "skipped": sum(bool(r.get("skipped")) for r in rows.values()),
            "completed": len(done_rows),
            "answer_in_reply": share(sum(right.values()), len(right)),
            "answer_in_reply_by_type": {},
            "false_match": false_match_rate({i: replies[i] for i in right}, golds),
            "reply_characters_mean": round(statistics.fmean(lengths), 1) if lengths else None,
            "reply_words_mean": round(statistics.fmean(word_counts), 1) if word_counts else None,
            "replies_at_60_token_cap": share(
                sum(r.get("reply_tokens", 0) >= MAX_TOKENS for r in done_rows.values()),
                len(done_rows),
            ),
            "abstention": share(
                sum(refused.get(i, 0) for i in abstention_ids),
                sum(i in replies for i in abstention_ids),
            ),
            "refusal_on_answerable": share(
                sum(refused.get(i, 0) for i in answerable_ids),
                sum(i in replies for i in answerable_ids),
            ),
            "clean_first_calls": share(
                sum(clean_call(r["first_reply"]) for r in searching), len(searching)
            ),
            "ran_out_of_calls": sum(bool(r.get("ran_out_of_calls")) for r in done_rows.values()),
            "tokens_read_per_question": mean("tokens_read"),
            "tokens_written_per_question": mean("tokens_written"),
            "seconds_per_question": mean("seconds", 2),
            "run_seconds": meta.get("seconds"),
            "peak_vram_gib": meta.get("peak_vram_gib"),
        }
        for kind in sorted({kinds[i] for i in right}):
            typed = [i for i in right if kinds[i] == kind]
            entry["answer_in_reply_by_type"][kind] = {
                "trained_for": kind in TRAINED_FOR,
                **share(sum(right[i] for i in typed), len(typed)),
            }
        if name in SEARCH_ARMS:
            entry["evidence"] = evidence_measures(found[name], evidence_ids, shown_ids, kinds)
            entry["logged_searches_not_reproduced"] = not_reproduced[name]
        if name == "evidence_only":
            entry["same_questions_other_arms"] = {
                other: share(sum(scores[other]["answer"].get(i, 0) for i in right), len(right))
                for other in FULL_ARMS
                if other in scores
            }
        report["measures"][name] = entry

    hypotheses = report["hypotheses"]
    if "637_tool" in scores and "base_tool" in scores:
        new, base = scores["637_tool"], scores["base_tool"]
        both = [
            i
            for i in evidence_ids
            if found["637_tool"].get(i, {}).get("searched")
            and found["base_tool"].get(i, {}).get("searched")
        ]
        hypotheses["H1_first_search_637_vs_base_tool"] = {
            "no_search_counts_as_not_found": two_readings(
                new["first"], base["first"], evidence_ids, completed
            ),
            "questions_both_searched": paired(new["first"], base["first"], both),
        }
        hypotheses["H3_637_vs_base_tool"] = {
            "abstention": two_readings(
                new["declines"], base["declines"], abstention_ids, completed
            ),
            "refusal_on_answerable": two_readings(
                new["declines"], base["declines"], answerable_ids, completed
            ),
        }
    if "637_tool" in scores and "always_search" in scores:
        new, code = scores["637_tool"], scores["always_search"]
        hypotheses["H2_637_vs_always_search"] = {
            "first_search_turn": two_readings(new["first"], code["first"], evidence_ids, completed),
            "any_search_turn": two_readings(new["any"], code["any"], evidence_ids, completed),
            "answer_in_reply": two_readings(new["answer"], code["answer"], read, completed),
        }
    (OUT / "scores.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "provenance"}, indent=1))


if __name__ == "__main__":
    main()
