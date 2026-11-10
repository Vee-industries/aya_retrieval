"""R-170's judge prompts and sheets on small made-up data, never the real LongMemEval file."""

import importlib.util
from pathlib import Path
from types import SimpleNamespace

from aya_retrieval.longmemeval_judge import ABSTENTION, TEMPLATES, judge_prompt, judged_correct

SCRIPTS = Path(__file__).parents[1] / "scripts"
spec = importlib.util.spec_from_file_location(
    "judge_sheets_r170", SCRIPTS / "records" / "judge_sheets_r170.py"
)
sheets = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sheets)


def test_each_type_gets_its_template_and_abstention_overrides_the_type():
    prompt = judge_prompt("knowledge-update", "Q?", "A", "R", abstention=False)
    assert prompt.startswith(TEMPLATES["knowledge-update"].split("{}")[0])
    assert "Question: Q?\n\nCorrect Answer: A\n\nModel Response: R\n\n" in prompt
    assert judge_prompt("multi-session", "Q?", "A", "R", abstention=True) == ABSTENTION.format(
        "Q?", "A", "R"
    )
    assert "Rubric: A" in judge_prompt(
        "single-session-preference", "Q?", "A", "R", abstention=False
    )


def test_a_verdict_is_correct_when_yes_appears_in_it():
    assert judged_correct(" Yes.") and judged_correct("yes")
    assert not judged_correct("No") and not judged_correct("")


def item(item_id, kind, abstention=False):
    return SimpleNamespace(
        item_id=item_id, kind=kind, question=f"q {item_id}", answer="a", abstention=abstention
    )


def test_sheets_judge_every_core_question_and_skip_failures_and_skips():
    items = [item("c1", "single-session-user"), item("c2", "knowledge-update", abstention=True)]
    items += [item(f"r{n:03d}", "multi-session") for n in range(150)]
    assert sheets.select(items)[:2] == ["c1", "c2"] and len(sheets.select(items)) == 102
    assert sheets.select(items) == sheets.select(list(reversed(items)))
    arms = {
        "a": {
            "c1": {"reply": "x", "error": None},
            "c2": {"reply": None, "error": "OutOfMemoryError"},
        },
        "b": {"c1": {"reply": None, "skipped": "too long"}, "c2": {"reply": "y", "error": None}},
    }
    lines = sheets.build_lines(items, arms)
    assert sorted((line["id"], line["arm"]) for line in lines) == [("c1", "a"), ("c2", "b")]
    assert [line["line"] for line in lines] == [0, 1] and {line["sheet"] for line in lines} == {
        "L1"
    }
    abstained = next(line for line in lines if line["id"] == "c2")
    assert abstained["abstention"] and abstained["prompt"].startswith(
        "I will give you an unanswerable"
    )
