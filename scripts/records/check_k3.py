"""R-205's check before training: K3's natural rows against the registered lines.

Lines (a FAIL on any one means K3 does not train; no writer file is rewritten to pass):
1. Every first query's words are in its question and none is a filler word; 1 to 4 words. No second
   query holds its value.
2. Value-naming rows' replies hold the stored value; declining rows' replies are from
   ``TRAIN.unknown_replies``.
3. Passage gap between value-naming and declining rows at most 0.37, natural rows alone and the
   whole set.
4. Natural questions sharing a four-word run with a question of hard_dev, probe, either
   outside-writer set or Demo2: 0. Natural answer values that are also answers there: at most 25%.
5. S3 (``overlap_s3_training.py``, counts only): four-word runs S3 shares with K3 at most twice
   those it shares with K1.3.
6. Facts about the user at least a third of natural fact rows; check_false at least 15% of natural
   rows.
7. Every row at most 1,024 tokens.
Reported: rows by kind and person, second searches and misses by side, top scores by side.

Usage:
    python scripts/records/check_k3.py
"""

from __future__ import annotations

import importlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

from huggingface_hub import snapshot_download
from transformers import AutoTokenizer

from aya_retrieval.chat import SYSTEM_WITH_TOOL
from aya_retrieval.conversations import NEVER_TOLD
from aya_retrieval.demonstrations import FILLER
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.pools import POOLS, TRAIN
from aya_retrieval.tool_prompt import system_prompt_with_tools

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
REPO = HERE.parents[1]
NAME = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "k3_r205"
SET = REPO / f"data/screens/{NAME}.jsonl"  # R-206: k3_1_r206
BASE = REPO / "data/screens/k1_3_r200.jsonl"
WRITERS = REPO / "data/screens/k3_writers"
if NAME.startswith(("k4_5", "k4_6", "k4_7", "k4_8")):  # R-213: writer copies, possessives out
    WRITERS = REPO / f"data/screens/{NAME[:4]}/writers/k3"
FIELDS = ("statement", "same_words", "new_words", "indirect", "confirm")  # check_r196.FIELDS
BRIEF_FILLER = set(
    "say tell told mention remember again know think what where which who does did is".split()
)
MAX_GAP = 0.37


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", text.casefold())


def bare(text: str) -> list[str]:
    """Words with a possessive 's removed (R-206: "calderbrook's" holds "calderbrook")."""
    return [w.removesuffix("'s") for w in words(text)]


def runs(text: str) -> set[tuple[str, ...]]:
    w = words(text)
    return {tuple(w[i : i + 4]) for i in range(len(w) - 3)}


def last_output(row: dict) -> str | None:
    outputs = [t["content"] for t in row["turns"] if t["content"].startswith("Tool result for")]
    return outputs[-1] if outputs else None


def top_score(output: str) -> float:
    scores = [float(s) for s in re.findall(r"score=([0-9.]+)\]", output)]
    return max(scores, default=0.0)


def s3_shared(train: Path) -> int:
    script = HERE / "overlap_s3_training.py"
    out = subprocess.run(
        [sys.executable, str(script), "--final", "--train", str(train)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return int(re.search(r"^all: (\d+) of", out, re.M).group(1))


def dev_sets() -> tuple[list[str], set[str]]:
    """Questions and answers of hard_dev, probe, both outside-writer sets and Demo2."""
    dev_questions, dev_values = [], set()
    for pool in ("hard_dev", "probe"):
        dev_questions += [getattr(t, f) for t in POOLS[pool].facts.values() for f in FIELDS]
        dev_values |= {v.casefold() for t in POOLS[pool].facts.values() for v in t.values}
    for folder in ("blind_dev", "blind_dev2"):
        for path in sorted((REPO / "data" / folder / "chats").glob("*.json")):
            for q in json.loads(path.read_text(encoding="utf-8"))["questions"]:
                dev_questions.append(q["message"])
                dev_values.add(str(q["answer"]).casefold())
    demo2 = json.loads((REPO / "demo2/questions.json").read_text(encoding="utf-8"))["questions"]
    dev_questions += [q["question"] for q in demo2]
    dev_values |= {q["key"].casefold() for q in demo2 if q["key"] != "never told"}
    return dev_questions, dev_values


def dev_questions() -> list[str]:
    return dev_sets()[0]


def main() -> None:
    rows = [json.loads(line) for line in SET.read_text(encoding="utf-8").splitlines()]
    base = [json.loads(line) for line in BASE.read_text(encoding="utf-8").splitlines()]
    provenance = json.loads(SET.with_suffix(".provenance.json").read_text(encoding="utf-8"))
    meta = provenance["meta"]
    natural = [r for r in rows if r["id"].startswith("k3_")]
    by_id = {r["id"]: r for r in natural}
    questions = {}
    for path in sorted(WRITERS.glob("*.json")):
        for c, chat in enumerate(json.loads(path.read_text(encoding="utf-8"))["chats"]):
            for q, question in enumerate(chat["questions"]):
                questions[f"k3_{path.stem}_{c:02d}_{q:02d}"] = question
    questions.update(
        provenance.get("k4_questions", {})
    )  # R-208: K4's near-miss and contrast questions
    if NAME != "k3_r205":  # R-207: only the questions whose rows are in the set (a fault fix)
        questions = {k: v for k, v in questions.items() if k in by_id}
    checks = []

    # 1. queries
    bad_first, bad_second = [], []
    for qid, q in questions.items():
        if q["kind"] == "in_view":
            continue
        query = bare(q["query"])
        if not 1 <= len(query) <= 4 or any(
            w not in bare(q["question"]) or w in FILLER or w in BRIEF_FILLER for w in query
        ):
            bad_first.append(qid)
        if q.get("value") and q["value"].casefold() in words(q.get("second_query", "")):
            bad_second.append(qid)
    checks.append(
        (f"first queries breaking the rule {len(bad_first)} {bad_first[:5]}", not bad_first)
    )
    checks.append(
        (f"second queries holding the value {len(bad_second)} {bad_second[:5]}", not bad_second)
    )

    # 2. replies
    unknown = set(TRAIN.unknown_replies)
    bad_reply = []
    for rid, m in meta.items():
        if not m or "names_value" not in m:
            continue
        reply = by_id[rid]["turns"][-1]["content"]
        if m["names_value"]:
            if questions[rid]["value"].casefold() not in reply.casefold():
                bad_reply.append(rid)
        elif reply not in unknown:
            bad_reply.append(rid)
    checks.append(
        (f"replies not matching their side {len(bad_reply)} {bad_reply[:5]}", not bad_reply)
    )

    # 3. passage gap
    def gap(pairs: list[tuple[bool, int]]) -> tuple[float, float, float]:
        v = [n for named, n in pairs if named]
        d = [n for named, n in pairs if not named]
        mv, md = sum(v) / max(1, len(v)), sum(d) / max(1, len(d))
        return abs(mv - md), mv, md

    nat_pairs = [
        (m["names_value"], m["passages"]) for m in meta.values() if m and "names_value" in m
    ]
    base_pairs = [
        (r["kind"] != NEVER_TOLD, last_output(r).count("[chunk_id="))
        for r in base
        if last_output(r) is not None
    ]
    if NAME.startswith(("k4_2", "k4_3", "k4_4", "k4_5", "k4_6", "k4_7", "k4_8")):  # R-210: count 0
        nat_pairs = [(named, n) for named, n in nat_pairs if n]
        after_empty = [
            any(
                t["content"].startswith("Tool result for") and "[chunk_id=" not in t["content"]
                for t in r["turns"][-2:-1]
            )
            for r in natural
        ]
        checks.append(
            (f"replies after an empty search {sum(after_empty)}, at least 1", any(after_empty))
        )
    if NAME.startswith(
        ("k4_5", "k4_6", "k4_7", "k4_8")
    ):  # R-213: a possessive query word finds nothing
        calls = [
            c["parameters"]["query"]
            for r in natural
            for t in r["turns"]
            if t["role"] == "assistant" and t["content"].startswith("[{")
            for c in json.loads(t["content"])
        ]
        marked = [q for q in calls if "'" in q or "’" in q]
        checks.append(
            (f"natural queries holding an apostrophe {len(marked)} of {len(calls)}", not marked)
        )
    for name, pairs in (("natural rows", nat_pairs), ("whole set", nat_pairs + base_pairs)):
        g, mv, md = gap(pairs)
        checks.append(
            (f"passage gap, {name}: {g:.2f} (value {mv:.2f}, decline {md:.2f})", g <= MAX_GAP)
        )

    # 4. dev overlap
    dev_questions, dev_values = dev_sets()
    dev_runs = set().union(*(runs(q) for q in dev_questions))
    shared_q = [qid for qid, q in questions.items() if runs(q["question"]) & dev_runs]
    values = {q["value"].casefold() for q in questions.values() if q.get("value")}
    share_v = len(values & dev_values) / max(1, len(values))
    checks.append(
        (
            f"natural questions sharing a four-word run with dev or Demo2 {len(shared_q)}",
            not shared_q,
        )
    )
    checks.append(
        (
            f"natural answer values also dev or Demo2 answers {share_v:.1%} ({len(values)} values)",
            share_v <= 0.25,
        )
    )

    # 5. S3, counts only
    k3_s3, k13_s3 = s3_shared(SET), s3_shared(BASE)
    if NAME == "k3_r205":
        checks.append(
            (
                f"S3 four-word runs shared: K3 {k3_s3}, K1.3 {k13_s3}, at most twice",
                k3_s3 <= 2 * k13_s3,
            )
        )
    else:  # R-206 (Kevin): no natural row shares a six-word run with S3; four-word runs reported
        overlap = importlib.import_module("overlap_s3_training")
        six = set()
        for path in sorted(overlap.CHATS.glob("*.json")):
            text = overlap.chat_text(json.loads(path.read_text(encoding="utf-8")))
            w = re.findall(r"[a-z0-9']+", text.lower())
            six |= {tuple(w[i : i + 6]) for i in range(len(w) - 5)}
        hit = 0
        for r in natural:
            for turn in r["turns"]:
                if turn["content"].startswith("Tool result"):
                    continue
                w = re.findall(r"[a-z0-9']+", turn["content"].lower())
                if {tuple(w[i : i + 6]) for i in range(len(w) - 5)} & six:
                    hit += 1
                    break
        checks.append((f"natural rows sharing a six-word run with S3 {hit}", not hit))
        print(f"report: S3 four-word runs shared, this set {k3_s3}, K1.3 {k13_s3}")

    # 6. shares
    facts = [
        m for m in meta.values() if m and m.get("kind") in ("older", "check_true", "check_false")
    ]
    me = sum(m["person"] == "me" for m in facts) / max(1, len(facts))
    false_share = sum(m["kind"] == "check_false" for m in meta.values() if m) / max(1, len(natural))
    checks.append(
        (
            f"facts about the user {me:.1%} of {len(facts)} natural fact rows, at least a third",
            me >= 1 / 3,
        )
    )
    checks.append(
        (
            f"check_false {false_share:.1%} of {len(natural)} natural rows, at least 15%",
            false_share >= 0.15,
        )
    )

    if NAME.startswith("k4"):  # R-208: line 6's second half, registered before K4's build
        kinds6 = Counter(m.get("kind") for m in meta.values() if m)
        checks[-1] = (
            f"check_false rows {kinds6['check_false']} at least check_true rows "
            f"{kinds6['check_true']}",
            kinds6["check_false"] >= kinds6["check_true"],
        )
    # 7. tokens
    tokenizer = AutoTokenizer.from_pretrained(
        snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True)
    )
    system = {"role": "system", "content": system_prompt_with_tools(SYSTEM_WITH_TOOL)}
    longest = max(
        len(
            tokenizer.apply_chat_template([system, *r["turns"]], tokenize=True, return_dict=True)[
                "input_ids"
            ]
        )
        for r in rows
    )
    checks.append((f"longest row {longest} tokens, at most 1024", longest <= 1024))

    for text, ok in checks:
        print(f"{'PASS' if ok else 'FAIL':5} {text}")
    kinds = Counter((r["kind"], (meta.get(r["id"]) or {}).get("kind")) for r in natural)
    print(f"report: natural rows by kind {dict(kinds)}")
    side = Counter(
        (m["names_value"], m["searches"]) for m in meta.values() if m and "names_value" in m
    )
    print(f"report: (names value, searches) {dict(side)}")
    scores = {True: [], False: []}
    for rid, m in meta.items():
        if m and "names_value" in m:
            scores[m["names_value"]].append(top_score(last_output(by_id[rid])))
    print(
        "report: top score, value rows "
        f"{sum(scores[True]) / max(1, len(scores[True])):.2f}, declining rows "
        f"{sum(scores[False]) / max(1, len(scores[False])):.2f}"
    )
    print(f"== k3 check: {sum(not ok for _, ok in checks)} FAIL (R-205 lines)")


if __name__ == "__main__":
    main()
