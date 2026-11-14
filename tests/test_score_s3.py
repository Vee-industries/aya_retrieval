"""R-281's S3 scorer: shown to fail planted bad results before its verdict is believed."""

import importlib.util
import json
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "records" / "score_s3.py"
spec = importlib.util.spec_from_file_location("score_s3", SCRIPT)
score_s3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score_s3)

CHATS = [f"w1_{n:02d}" for n in range(20)]


def rows(recall, copy, false_answer, chats=CHATS):
    """One chat's rows for every measure: recall and copy as 0/1 per chat, false answers too."""
    out = []
    for i, chat in enumerate(chats):
        base = {"chat": chat, "variant": None, "copy": None, "n_hit": False, "false_answer": None}
        out += [
            {**base, "kind": "older", "view": "right", "item_correct": recall(i)},
            {**base, "kind": "in_view", "view": "right", "item_correct": True},
            {**base, "kind": "statement", "view": "right", "item_correct": True},
            {
                **base,
                "kind": "never_told",
                "variant": "plain",
                "view": "right",
                "item_correct": True,
            },
            {**base, "kind": "re_ask", "view": "wrong", "item_correct": True, "copy": copy(i)},
            {
                **base,
                "kind": "never_told",
                "variant": "overlap",
                "view": "wrong",
                "item_correct": True,
                "n_hit": True,
                "false_answer": false_answer(i),
            },
        ]
    return out


def write(folder: Path, pick_copy) -> None:
    runs = {
        "s3_always_search": rows(lambda i: i % 2 == 0, lambda i: False, lambda i: False),
        "s3_whole_chat": rows(lambda i: True, lambda i: False, lambda i: False),
        "s3_base_tool": rows(lambda i: i % 2 == 0, lambda i: False, lambda i: i % 2 == 0),
    }
    for seed in score_s3.SEEDS:
        runs[f"s3_{score_s3.OLD}_{seed}"] = rows(lambda i: True, lambda i: True, lambda i: True)
        runs[f"s3_{score_s3.PICK}_{seed}"] = rows(lambda i: True, pick_copy, lambda i: False)
    for name in score_s3.REPORT:
        for seed in (82, 83):
            runs[f"s3_{name}_{seed}"] = rows(lambda i: True, lambda i: False, lambda i: False)
    for label, data in runs.items():
        (folder / f"{label}.json").write_text(json.dumps({"rows": data}), encoding="utf-8")


COHERENT = {"judge_1": {"pick_rate": 0.9, "base_rate": 0.9}}


def test_rule_passes_a_planted_pass(tmp_path):
    write(tmp_path, lambda i: False)
    report = score_s3.rule(tmp_path, COHERENT)
    assert report["pass"], report["lines"]
    assert report["arms"]["pick"]["copy"] == {"hits": 0, "n": 60, "rate": 0.0}


def test_rule_fails_a_pick_that_copies_as_often_as_637(tmp_path):
    write(tmp_path, lambda i: True)
    report = score_s3.rule(tmp_path, COHERENT)
    failed = [x["line"] for x in report["lines"] if not x["pass"]]
    assert not report["pass"] and len(failed) == 1 and failed[0].startswith("(b)")


def test_rule_fails_on_coherence_and_without_a_tally(tmp_path):
    write(tmp_path, lambda i: False)
    low = {"judge_1": {"pick_rate": 0.85, "base_rate": 0.9}}  # 0.85 is under 0.9 x 0.95
    assert not score_s3.rule(tmp_path, low)["pass"]
    assert not score_s3.rule(tmp_path, None)["pass"]


def test_bound_is_not_above_zero_when_one_chat_carries_the_gain(tmp_path):
    a = {c: [1 if c == CHATS[0] else 0, 1] for c in CHATS}
    b = {c: [0, 1] for c in CHATS}
    assert score_s3.lower_bound(a, b, CHATS, n_resamples=2000) <= 0


def test_tally_needs_every_line_and_judge_1_decides():
    key = [{"line": 0, "model": "base"}, {"line": 1, "model": "pick"}]
    report = score_s3.tally(key, {"judge_1": {"0": 1, "1": 0}, "judge_2": {"0": 1, "1": 1}})
    assert report["judge_1"]["pick_rate"] == 0.0 and report["judge_2"]["pick_rate"] == 1.0
    try:
        score_s3.tally(key, {"judge_1": {"0": 1}})
    except SystemExit:
        return
    raise AssertionError("a judge with a missing line was accepted")
