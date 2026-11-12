"""S3's loader, flags and tools (R-178) on the brief's own made-up example, never the sealed set."""

import copy
import importlib.util
import json
import re
from pathlib import Path

import pytest

from aya_retrieval.harness import TurnResult
from aya_retrieval.heldout3 import (
    RIGHT_VIEW,
    SPLIT_FILE,
    WRONG_VIEW,
    Split,
    chat_problem,
    copy_flag,
    draw_sample,
    false_answer,
    load_s3,
    load_split,
    n_hit_query,
    never_told_right,
    set_problems,
    view_exchanges,
)
from aya_retrieval.recall_tool import build_recall_tool

ROOT = Path(__file__).parents[1]
BRIEF = ROOT / "docs" / "heldout3" / "BRIEF.md"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


split_script = load(
    "split_categories_r178", ROOT / "scripts" / "records" / "split_categories_r178.py"
)
seal = load("seal_s3", ROOT / "scripts" / "records" / "seal_s3.py")
checker = load("check_s3", ROOT / "scripts" / "records" / "check_s3.py")
drawer = load("draw_s3_sample", ROOT / "scripts" / "records" / "draw_s3_sample.py")
evaluator = load("run_s3_eval", ROOT / "scripts" / "run_s3_eval.py")

SPLIT = load_split(SPLIT_FILE)


def example() -> dict:
    """The brief's worked example, under a writer id the loader accepts."""
    block = re.search(r"```json\n(.*?)\n```", BRIEF.read_text(encoding="utf-8"), re.S).group(1)
    chat = json.loads(block)
    chat["id"] = "w1_01"
    return chat


def write_chats(folder: Path, *chats: dict) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    for chat in chats:
        (folder / f"{chat['id']}.json").write_text(json.dumps(chat), encoding="utf-8")
    return folder


def question(chat: dict, kind: str, overlap: bool = False) -> dict:
    for q in chat["questions"]:
        if q["kind"] == kind and (
            kind != "never_told" or (q["overlap_exchange"] is not None) == overlap
        ):
            return q
    raise KeyError(kind)


def test_the_brief_example_passes_every_rule(tmp_path):
    items, dropped, batch, digest = load_s3(write_chats(tmp_path, example()), SPLIT)
    assert dropped == []
    assert batch == ["w1: 1 chats, not 10"]
    kinds = sorted((s3.view, s3.item.kind) for s3 in items)
    right = [k for v, k in kinds if v == RIGHT_VIEW]
    wrong = [k for v, k in kinds if v == WRONG_VIEW]
    assert sorted(right) == sorted(
        ["older"] * 3 + ["confirm", "in_view", "statement"] + ["never_told"] * 2
    )
    assert sorted(wrong) == sorted(["older"] * 3 + ["never_told"] * 2 + ["re_ask"])
    assert len(digest) == 64


def test_the_brief_lists_are_the_committed_split():
    lists = checker.brief_lists(BRIEF)
    assert lists["A"] == set(SPLIT.outside)
    assert lists["B"] == set(SPLIT.inside)


def test_the_two_views_differ_only_in_the_earlier_reply():
    chat = example()
    right, wrong = view_exchanges(chat, RIGHT_VIEW), view_exchanges(chat, WRONG_VIEW)
    at = chat["earlier_question"]["exchange"]
    assert right[at][1] == chat["earlier_question"]["right_reply"]
    assert wrong[at][1] == chat["earlier_question"]["wrong_reply"]
    assert [p for n, p in enumerate(right) if n != at] == [
        p for n, p in enumerate(wrong) if n != at
    ]


def broken(change) -> dict:
    chat = example()
    change(chat)
    return chat


def test_each_chat_rule_rejects_a_chat_that_breaks_it():
    def drop_people(c):
        c["people"] = c["people"][:4]
        c["lookalikes"] = c["people"][:2]

    def no_correction(c):
        c["facts"][6]["corrects"] = None

    def few_user_facts(c):
        for fact in c["facts"]:
            if fact["person"] == "me" and fact["category"] != "C02":
                fact["person"] = "Lucia (my manager)"

    def reply_filled(c):
        c["exchanges"][18][1] = "hm"

    def wrong_reply_names_answer(c):
        c["earlier_question"]["wrong_reply"] = "Pistachio or Waffles."

    def wrong_value_is_an_answer(c):
        question(c, "older")["answer"] = "Waffles"

    def lists(c):
        for fact in c["facts"]:
            if fact["category"] in ("C36", "C19", "C18"):
                fact["category"] = "C02"
        c["facts"][5]["category"] = c["facts"][6]["category"] = "C01"

    cases = {
        "exchanges, not 20 to 30": lambda c: c.update(exchanges=c["exchanges"][-15:]),
        "fewer than 5 people": drop_people,
        "no correction": no_correction,
        "under a third of facts": few_user_facts,
        "assistant half is not empty": reply_filled,
        "wrong reply does not name the wrong value alone": wrong_reply_names_answer,
        "wrong value is, or contains, an answer": wrong_value_is_an_answer,
        "value is not in its exchange": lambda c: c["facts"][0].update(value="spanish"),
        "facts from list A": lists,
        "not 3": lambda c: c["questions"].pop(0),
        "never_told questions are not one plain": lambda c: question(
            c, "never_told", overlap=True
        ).update(overlap_exchange=None),
        "earlier question is not in the last three": lambda c: c["earlier_question"].update(
            exchange=10
        ),
    }
    for reason, change in cases.items():
        problem = chat_problem(broken(change), SPLIT)
        assert problem and reason in problem, (reason, problem)


def test_each_question_rule_drops_only_that_question(tmp_path):
    def confirm_claim_mismatch(c):
        question(c, "confirm")["claim"] = "true"

    cases = {
        "answer appears in view": lambda c: question(c, "older").update(
            answer="Pistachio",
            category="C09",
            person="Farah (my sister)",
            fact_exchange=2,
            wrong=[],
        ),
        "claim does not match": confirm_claim_mismatch,
        "never_told fact was told": lambda c: question(c, "never_told").update(
            person="Bogdan (my neighbour)"
        ),
        "wrong does not list every chat value": lambda c: question(c, "never_told").update(
            wrong=["brewery"]
        ),
        "shares no content word": lambda c: question(c, "never_told", overlap=True).update(
            message="what show is he into lately"
        ),
        "re_ask is not the earlier question's fact": lambda c: question(c, "re_ask").update(
            answer="Porto",
            category="C15",
            person="Kenji (my cousin)",
            fact_exchange=8,
            wrong=["Lisbon", "Waffles"],
        ),
        "statement names a fact": lambda c: question(c, "statement").update(
            message="still thinking about dumplings"
        ),
        "in_view fact is out of view": lambda c: question(c, "in_view").update(
            answer="sesame", category="C19", person="me", fact_exchange=4
        ),
    }
    for number, (reason, change) in enumerate(cases.items()):
        folder = tmp_path / f"case_{number}"
        items, dropped, _, _ = load_s3(write_chats(folder, broken(change)), SPLIT)
        assert len(dropped) == 1 and reason in dropped[0][1], (reason, dropped)
        assert "_q" in dropped[0][0]
        assert items


def test_set_rules_count_chats_and_confirm_balance():
    chats = []
    for n in range(1, 11):
        chat = example()
        chat["id"] = f"w2_{n:02d}"
        chats.append(chat)
    assert set_problems(chats) == ["w2: confirm claims 0 true, 10 false, not half and half"]
    for chat in chats[:5]:
        confirm = question(chat, "confirm")
        confirm.update(claim="true", claimed_value="pharmacy", message="the pharmacy right?")
    assert set_problems(chats) == []


def items_by_id(tmp_path):
    items, _, _, _ = load_s3(write_chats(tmp_path, example()), SPLIT)
    return {s3.item.item_id: s3 for s3 in items}


def test_flags(tmp_path):
    items = items_by_id(tmp_path)
    older_wrong = items["w1_01_q0_wrong"]
    assert copy_flag(older_wrong, "He works at a place, I think Waffles?") is True
    assert copy_flag(older_wrong, "At the brewery.") is False
    assert copy_flag(items["w1_01_q0_right"], "Waffles") is None
    assert copy_flag(items["w1_01_q8_wrong"], "Waffles") is None
    assert false_answer(older_wrong, "The pharmacy.") is True
    assert false_answer(older_wrong, "The brewery.") is False
    confirm = items["w1_01_q3_right"]
    assert false_answer(confirm, "No, not the brewery: the pharmacy.") is False
    plain = items["w1_01_q6_right"]
    assert never_told_right(plain, "You didn't tell me.") is True
    assert never_told_right(plain, "He works at the brewery.") is False
    assert never_told_right(older_wrong, "anything") is None
    assert false_answer(items["w1_01_q5_right"], "anything") is None
    assert n_hit_query("What show is Bogdan into lately?") == "show bogdan"


def test_eval_rows_carry_every_flag(tmp_path):
    items = items_by_id(tmp_path / "chats")
    s3 = items["w1_01_q7_wrong"]
    tool = build_recall_tool(s3.item, tmp_path / "index.sqlite", match_all=False)
    result = TurnResult(reply="He's into Waffles, I think.", queries=["bogdan show"])
    row = evaluator.score_row(s3, "tool", result, tool)
    assert row["view"] == WRONG_VIEW and row["kind"] == "never_told"
    assert row["variant"] == "overlap"
    assert row["n_hit"] is True
    assert row["copy"] is True
    assert row["item_correct"] is True  # Waffles is not under this item's wrong
    assert row["false_answer"] is False
    assert len(row["search_outputs"]) == 1 and "brewery" in row["search_outputs"][0]
    reask = items["w1_01_q8_wrong"]
    tool = build_recall_tool(reask.item, tmp_path / "index.sqlite", match_all=False)
    row = evaluator.score_row(reask, "tool", TurnResult(reply="It's Pistachio."), tool)
    assert row["item_correct"] is True and row["right_decision"] is False and row["copy"] is None


def test_eval_refuses_without_final():
    with pytest.raises(SystemExit):
        evaluator.parse_args(["--arm", "tool", "--index", "x.sqlite", "--label", "x"])
    with pytest.raises(SystemExit):
        evaluator.parse_args(
            ["--final", "--arm", "whole_chat", "--adapter", "a", "--index", "x", "--label", "x"]
        )
    assert evaluator.parse_args(["--final", "--arm", "tool", "--index", "x", "--label", "x"]).final


def test_the_set_hash_follows_every_byte(tmp_path):
    folder = write_chats(tmp_path, example())
    first = load_s3(folder, SPLIT)[3]
    path = folder / "w1_01.json"
    path.write_text(path.read_text(encoding="utf-8") + " ", encoding="utf-8")
    assert load_s3(folder, SPLIT)[3] != first


def test_the_sample_is_fixed_by_its_seed(tmp_path):
    items = list(items_by_id(tmp_path).values())
    assert draw_sample(items, size=5) == draw_sample(items, size=5)
    assert draw_sample(items, size=5, seed=1) != draw_sample(items, size=5, seed=2)
    assert len(draw_sample(items)) == len(items)  # fewer items than the sample size: all of them
    record = drawer.sample(tmp_path, SPLIT_FILE)
    assert record["size"] == 120 and len(record["ids"]) == len(items)


def test_seal_check_passes_unchanged_and_names_every_change(tmp_path):
    chats = write_chats(tmp_path / "chats", example())
    judge = tmp_path / "judge.md"
    judge.write_text("judge brief", encoding="utf-8")
    manifest = tmp_path / "manifest.json"
    seal.write(manifest, chats, [judge.as_posix()])
    assert seal.check(manifest, chats) == []
    judge.write_text("judge brief, edited", encoding="utf-8")
    other = copy.deepcopy(example())
    other["id"] = "w1_02"
    write_chats(chats, other)
    found = seal.check(manifest, chats)
    assert any("judge_briefs" in line for line in found)
    assert any("w1_02.json" in line for line in found)
    assert any("load_sha256" in line for line in found)


def test_check_prints_counts_and_reasons_but_no_chat_text(tmp_path):
    chat = broken(lambda c: question(c, "confirm").update(claim="true"))
    lines, ok = checker.report(write_chats(tmp_path, chat), BRIEF, SPLIT_FILE)
    assert not ok
    shown = "\n".join(lines)
    assert "w1_01_q3: claim does not match" in shown
    texts = [t for pair in chat["exchanges"] for t in pair if t] + [
        q["message"] for q in chat["questions"]
    ]
    texts += [f["value"] for f in chat["facts"]]
    assert not [t for t in texts if t.casefold() in shown.casefold()]


def test_the_split_matches_whole_words_in_queries_only(tmp_path):
    def call(query):
        return json.dumps([{"tool_name": "search_corpus", "parameters": {"query": query}}])

    rows = [
        {
            "turns": [
                {"role": "user", "content": "my cats are wild and i love hockey"},
                {"role": "assistant", "content": call("sister cats")},
                {"role": "user", "content": "Tool result for search_corpus: dog park"},
                {"role": "assistant", "content": "Your sister has cats."},
            ]
        },
        {"turns": [{"role": "assistant", "content": call("brother new place")}]},
    ]
    training = tmp_path / "train.jsonl"
    training.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    table = tmp_path / "categories.md"
    table.write_text(
        "| id | kind | keywords |\n|---|---|---|\n"
        "| C01 | pet | cat, dog |\n| C02 | team | hockey, fan |\n"
        "| C03 | move | new place, moving |\n",
        encoding="utf-8",
    )
    queries, user_lines = split_script.extract(training)
    assert queries == ["sister cats", "brother new place"]
    assert user_lines == ["my cats are wild and i love hockey"]
    result = split_script.split(split_script.read_categories(table), queries, user_lines)
    assert result["inside"] == ["C03"]
    assert result["outside"] == ["C01", "C02"]  # "cats" is not "cat"; hockey is in a user line
    assert result["per_category"]["C02"]["user_line_keywords"] == ["hockey"]


def test_unknown_categories_are_rejected():
    chat = example()
    chat["facts"][0]["category"] = "C99"
    assert chat_problem(chat, SPLIT) == "fact 0: unknown category"
    assert chat_problem(example(), Split(outside=frozenset(), inside=frozenset())) is not None
