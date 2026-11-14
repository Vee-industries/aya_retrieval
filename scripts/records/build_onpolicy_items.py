"""R-253: training chats as eval items, to find a model's own mistakes on them.

Usage: python scripts/records/build_onpolicy_items.py

For each of K4.8's 128 K3 writer chats (``data/screens/k4_8/writers/k3``, possessives out), one
file in ``data/onpolicy/items/`` in the dev-set format (``aya_retrieval.dev_set``): the chat's 24
exchanges, then 3 questions chosen in the order of SHA-256("R-253|...") with no look at any
result: 2 ``older`` questions, and 1 trap from the chat's K4 near-miss or K4.4 wrong-person
questions, as ``never_told`` with the stored fact's value as its wrong value (the value a model
names when it copies the other fact). ``meta.json`` beside them maps each item id to its writer
question, for building rows. Only training chats are read; no screening set.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

CHATS = Path("data/screens/k4_8/writers/k3")
TRAPS = (Path("data/screens/k4_8/writers/k4"), Path("data/screens/k4_8/writers/k4_4"))
OUT = Path("data/onpolicy/items")
SALT = "R-253"
RUN = 6  # S3's run length (build_k3_1.S3_RUN)
BLIND = (Path("data/blind_dev/chats"), Path("data/blind_dev2/chats"))
DEMOS = (Path("demo2"), Path("demo3"))


def order(key: str) -> bytes:
    return hashlib.sha256(f"{SALT}|{key}".encode()).digest()


def runs(text: str) -> set[tuple[str, ...]]:
    w = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(w[i : i + RUN]) for i in range(len(w) - RUN + 1)}


def gate_answers() -> list[tuple[set, set[str]]]:
    """Each gate chat's six-word runs and answer words; read for counts only, never printed."""
    out = []
    for folder in BLIND:
        for path in sorted(folder.glob("*.json")):
            chat = json.loads(path.read_text(encoding="utf-8"))
            text = "\n".join(" ".join(pair) for pair in chat["exchanges"])
            keys = {q["answer"].casefold() for q in chat["questions"] if q.get("answer")}
            out.append((runs(text), keys))
    for folder in DEMOS:
        questions = json.loads((folder / "questions.json").read_text(encoding="utf-8"))["questions"]
        keys = {q["key"].casefold() for q in questions if q["key"] != "never told"}
        out.append((runs((folder / "chat.txt").read_text(encoding="utf-8")), keys))
    return out


def shares_gate_answer(exchanges: list[list[str]], gates: list[tuple[set, set[str]]]) -> bool:
    """A six-word run in both this chat and a gate chat holds one of that gate chat's answers."""
    mine = runs("\n".join(" ".join(pair) for pair in exchanges))
    for theirs, keys in gates:
        for run in mine & theirs:
            if any(re.search(rf"\b{re.escape(k)}\b", " ".join(run)) for k in keys):
                return True
    return False


def stored_value(chat: dict, q: dict) -> str | None:
    """The value of the fact a trap question is built against (the chat's annotations 1 to 21)."""
    if q["kind"] == "near_miss":
        person, category = q["person"], q.get("stored_category")
    else:  # other_person
        person, category = q.get("stored_person"), q.get("category")
    for m in chat["messages"][:21]:
        f = m.get("fact")
        if (
            f
            and f["category"] == category
            and (f.get("person") or "").casefold() == (person or "").casefold()
        ):
            return f["value"]
    return None


def main() -> None:
    traps = defaultdict(list)
    for folder in TRAPS:
        for path in sorted(folder.glob("*.json")):
            for q in json.loads(path.read_text(encoding="utf-8"))["questions"]:
                if q["kind"] in ("near_miss", "other_person"):
                    traps[q["file"], q["chat"]].append(q)
    OUT.mkdir(parents=True, exist_ok=True)
    meta, made, excluded = {}, 0, []
    gates = gate_answers()
    for path in sorted(CHATS.glob("*.json")):
        for c, chat in enumerate(json.loads(path.read_text(encoding="utf-8"))["chats"]):
            cid = f"{path.stem}_{c:02d}"
            exchanges = [[m["user"], m["assistant"]] for m in chat["messages"]]
            if shares_gate_answer(exchanges, gates):
                excluded.append(cid)  # R-253: no gate answer reaches the corrections
                continue
            older = sorted(
                (q for q in chat["questions"] if q["kind"] == "older"),
                key=lambda q: order(f"{cid}|{q['question']}"),
            )[:2]
            trap = [
                q
                for q in sorted(traps[path.name, c], key=lambda q: order(f"{cid}|{q['question']}"))
                if stored_value(chat, q)
            ][:1]
            questions = [
                {
                    "kind": "older",
                    "message": q["question"],
                    "answer": q["value"],
                    "wrong": [],
                    "fact_exchange": q["source_message"] - 1,
                }
                for q in older
            ] + [
                {"kind": "never_told", "message": q["question"], "wrong": [stored_value(chat, q)]}
                for q in trap
            ]
            for n, q in enumerate(older + trap):
                meta[f"{cid}_q{n}"] = {**q, "chat_file": path.name, "chat_index": c}
            item = {"id": cid, "exchanges": exchanges, "questions": questions}
            (OUT / f"{cid}.json").write_text(
                json.dumps(item, ensure_ascii=False, indent=1), encoding="utf-8"
            )
            made += len(questions)
    (OUT.parent / "excluded.json").write_text(json.dumps(excluded, indent=1), encoding="utf-8")
    (OUT.parent / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"{OUT}: {len(list(OUT.glob('*.json')))} chats, {made} questions; excluded {excluded}")


if __name__ == "__main__":
    main()
