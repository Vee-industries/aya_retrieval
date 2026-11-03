"""Fill the article template's numbers from committed results files and write ``docs/ARTICLE.md``.

Usage:
    python scripts/make_article.py

Every ``{{name}}`` in ``docs/article_template.md`` is computed here from files under ``results/``,
so no number in the article is typed by hand. A placeholder left unfilled stops the script.
The current set is v4 on probe seed 73157 (development); the final run swaps in the held-out files.
"""

from __future__ import annotations

import json
import re

from aya_retrieval.provenance import REPO_ROOT
from aya_retrieval.report_data import (
    COHERENCE_DIR,
    KINDS,
    SIZES,
    by_kind,
    coherence_by_model_and_kind,
    coherence_pooled,
    eval_rows,
    false_retrieval,
    percent_above,
    pooled,
    recall,
    share,
    train_report,
)
from aya_retrieval.stats import exact_sign_test

TEMPLATE = REPO_ROOT / "docs" / "article_template.md"
OUT = REPO_ROOT / "docs" / "ARTICLE.md"
PROBE = 73157
SEEDS = (82, 83, 84)
BASE = "probe2_base"
TUNED = "probe6_tuned"  # v4
SCREEN_PROBE = 51203
SCREEN_REFERENCE = "screen_hard_in_view_lean82"
DROPPED = {
    "fewer “never told” rows (fix 3)": "screen_few_never_told82",
    "a second search after an empty one (fix 4)": "screen_second_search_82",
}
JUDGED_TARGETS = (
    "R-032",
    "judge_fix5/marks.json",
    "sheet_fix5/key.json",
)  # fix 5, filtered answers
SHEET_A = ("R-036", [f"a{s}" for s in SEEDS])  # v4, older and confirm, with the tool
SHEET_B = ("R-036B", [f"b{s}" for s in SEEDS])  # v4, statement and in_view, base with no tool
AUDIT = REPO_ROOT / "results" / "audit" / "fix5c_probe73157.json"
AUDIT_BUG_EXAMPLE = REPO_ROOT / "results" / "audit" / "v3_probe73157.json"
TRL_LOSS_RUN, LEAN_LOSS_RUN = "hard_in_view_84", "screen_hard_in_view_lean_82"
KIND_NAMES = {
    "older": "Fact told long ago",
    "confirm": "“Did I tell you…?”",
    "in_view": "Fact still on screen",
    "never_told": "Never told",
    "statement": "Just chatting",
}


def pct(pair: tuple[int, int]) -> str:
    return f"{100 * pair[0] / pair[1]:.0f}"


def signed(value: float) -> str:
    return f"{value:+.0f}"


def totals(counts: dict[str, tuple[int, int]]) -> tuple[int, int]:
    return pooled(list(counts.values()))


def recall_numbers(base, tuned, out) -> None:
    for size in SIZES:
        b = recall(base, size)
        t = pooled([recall(tuned[s], size) for s in SEEDS])
        out[f"base_recall_{size}"], out[f"tuned_recall_{size}"] = pct(b), pct(t)
        out[f"gain_{size}"] = signed(percent_above(t, b))


def kind_numbers(base, tuned, out) -> None:
    kb = by_kind(base)
    kt = {k: pooled([by_kind(tuned[s])[k] for s in SEEDS]) for k in KINDS}
    out["kind_table"] = "\n".join(
        f"| {KIND_NAMES[k]} | {pct(kb[k])}% | {pct(kt[k])}% "
        f"| {signed(percent_above(kt[k], kb[k]))}% |"
        for k in KINDS
    )
    behind = [KIND_NAMES[k] for k in KINDS if kt[k][0] / kt[k][1] <= kb[k][0] / kb[k][1]]
    out["kinds_summary"] = (
        "Every kind of message improves."
        if not behind
        else f"Every kind improves except {', '.join(behind)}."
    )
    decisions = [share(tuned[s], "right_decision") for s in SEEDS]
    seed_list = ", ".join(map(str, SEEDS))
    out["decisions_base"] = str(share(base, "right_decision")[0])
    out["decisions_n"] = str(len(base))
    out["decisions_tuned"] = ", ".join(str(d[0]) for d in decisions) + f" (seeds {seed_list})"


def coherence_numbers(out) -> None:
    with_tool, no_tool = coherence_pooled(*SHEET_A), coherence_pooled(*SHEET_B)
    lines, below = [], []
    for counts, label in ((with_tool, "both with the tool"), (no_tool, "untrained with no tool")):
        for kind in KINDS:
            if kind not in counts["tuned"]:
                continue
            b, t = counts["base"][kind], counts["tuned"][kind]
            lines.append(
                f"| {KIND_NAMES[kind]} | {label} | {b[0]} of {b[1]} | {t[0]} of {t[1]} "
                f"| {signed(percent_above(t, b))}% |"
            )
            if t[0] < b[0]:
                below.append(KIND_NAMES[kind])
    sheets = len(SHEET_A[1]) + len(SHEET_B[1])
    out["coherence_text"] = (
        f"Pooled over {len(SEEDS)} adapter seeds and {sheets} sheets, each with its own judge:\n\n"
        "| Kind | Setting | Untrained | Adapter | Above untrained |\n|---|---|---|---|---|\n"
        + "\n".join(lines)
        + "\n\nFact questions are judged with the search tool for both models. On-screen facts and "
        "ordinary chat are judged against the untrained model with no tool at all, so the adapter "
        "is held to the model's own ordinary talk."
    )
    a_base, a_tuned = totals(with_tool["base"]), totals(with_tool["tuned"])
    b_base, b_tuned = totals(no_tool["base"]), totals(no_tool["tuned"])
    both = pooled([a_tuned, b_tuned]), pooled([a_base, b_base])
    out["coherence_summary"] = (
        f"A blind judge finds the adapter's replies {percent_above(*both):.0f}% more often "
        "coherent than the untrained model's, "
        + (
            "and at or above it on every kind judged."
            if not below
            else f"though below it on {', '.join(below)}."
        )
    )


def false_retrieval_numbers(base, tuned, out) -> None:
    fb = false_retrieval(BASE, PROBE)
    ft = {k: pooled([false_retrieval(f"{TUNED}{s}", PROBE)[k] for s in SEEDS]) for k in KINDS}
    all_b, all_t = totals(fb), totals(ft)
    rows = "\n".join(
        f"| {KIND_NAMES[k]} | {fb[k][0]} of {fb[k][1]} | {ft[k][0]} of {ft[k][1]} |" for k in KINDS
    )
    searched_b = sum(bool(r["queries"]) for r in base if r["kind"] in ("older", "confirm"))
    searched_t = sum(
        bool(r["queries"]) for s in SEEDS for r in tuned[s] if r["kind"] in ("older", "confirm")
    )
    facts_b = pooled([fb["older"], fb["confirm"]])
    facts_t = pooled([ft["older"], ft["confirm"]])
    out["false_retrieval_text"] = (
        "| Kind | Untrained | Adapter |\n|---|---|---|\n"
        + rows
        + f"\n| **All** | **{all_b[0]} of {all_b[1]}** | **{all_t[0]} of {all_t[1]}** |\n\n"
        f"Over every kind the adapter names a wrong value in {100 * all_t[0] / all_t[1]:.1f}% of "
        f"replies against {100 * all_b[0] / all_b[1]:.1f}%, "
        f"{signed(percent_above(all_t, all_b))}%. Most of the gain is on facts still on screen and "
        "questions never told, where the untrained model fills in a value. On the two kinds that "
        f"need a search the counts are small, {facts_b[0]} and {facts_t[0]}, and the untrained "
        f"model searches far less often ({searched_b} of {facts_b[1]} questions against "
        f"{searched_t} of {facts_t[1]}), so it has fewer chances to pick up a decoy. The "
        "registered final test adds a crowded condition with four decoys a chat for exactly this "
        "reason."
    )
    out["false_retrieval_summary"] = (
        f"It names the wrong person's fact in {100 * all_t[0] / all_t[1]:.1f}% of replies, against "
        f"{100 * all_b[0] / all_b[1]:.1f}% for the untrained model."
    )


def audit_numbers(out) -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    labels = audit["labels"]
    agree = sum(v["cases"] - len(v["disagreements_with_our_scorer"]) for v in labels.values())
    cases = sum(v["cases"] for v in labels.values())
    ps = [audit["bootstrap"][f"{TUNED}{s}"]["all_kinds"]["sign_test_p"] for s in SEEDS]
    out["auditkit_text"] = (
        f"AuditKIT agrees with our scorer on {agree} of {cases} cases. The exact sign test on "
        f"AuditKIT's verdicts puts every adapter seed above the untrained model with p between "
        f"{min(ps):.0e} and {max(ps):.0e}."
    )
    found = json.loads(AUDIT_BUG_EXAMPLE.read_text(encoding="utf-8"))
    first = found["bootstrap"][next(iter(found["bootstrap"]))]["all_kinds"]["bootstrap"]
    out["auditkit_bug_example"] = (
        f"{100 * first['mean_base']:.0f}% → {100 * first['mean_adapter']:.0f}% "
        f"over {first['n']} paired cases"
    )


def memory_numbers(out) -> None:
    before, after = train_report(TRL_LOSS_RUN), train_report(LEAN_LOSS_RUN)
    out["mem_before"] = f"{before['train_peak_vram_gib']:.2f}"
    out["mem_after"] = f"{after['train_peak_vram_gib']:.2f}"
    steps = after["rows"] / after["batch_size"] * after["epochs"]
    out["step_seconds"] = f"{after['train_seconds'] / steps:.1f}"


def dropped_numbers(out) -> None:
    reference = eval_rows(SCREEN_REFERENCE, SCREEN_PROBE)
    ref = {r["id"]: r for r in reference}
    parts = []
    for name, label in DROPPED.items():
        new = {r["id"]: r for r in eval_rows(label, SCREEN_PROBE)}
        only_ref = sum(ref[i]["correct"] and not new[i]["correct"] for i in ref)
        only_new = sum(new[i]["correct"] and not ref[i]["correct"] for i in ref)
        parts.append(
            f"{name[0].upper() + name[1:]}: recall {recall(list(new.values()))[0]} against "
            f"{recall(reference)[0]} of {recall(reference)[1]} on the screen "
            f"(sign test p = {exact_sign_test(only_ref, only_new):.2f})."
        )
    record, marks, key = JUDGED_TARGETS
    judged = coherence_by_model_and_kind(
        COHERENCE_DIR / record / marks, COHERENCE_DIR / record / key
    )
    b, t = judged["base"]["confirm"], judged["tuned"]["confirm"]
    parts.append(
        "Having a judge filter the training answers (fix 5) left “Did I tell you…?” "
        f"coherence at {t[0]} of {t[1]} against the untrained model's {b[0]}, because the judge "
        "passed the same openers."
    )
    out["dropped_fixes"] = " ".join(parts)


def numbers() -> dict[str, str]:
    base = eval_rows(BASE, PROBE)
    tuned = {s: eval_rows(f"{TUNED}{s}", PROBE) for s in SEEDS}
    out: dict[str, str] = {}
    recall_numbers(base, tuned, out)
    kind_numbers(base, tuned, out)
    coherence_numbers(out)
    false_retrieval_numbers(base, tuned, out)
    audit_numbers(out)
    memory_numbers(out)
    dropped_numbers(out)
    out["results_scope"] = (
        f"Development numbers: the probe pool, {len(base)} conversations "
        f"({len(base) // 10} of each kind at each length), the untrained model against "
        f"{len(SEEDS)} adapters (v4) trained on seeds {', '.join(map(str, SEEDS))}. "
        "The held-out run replaces these."
    )
    out["status_line"] = (
        "Draft. Numbers are development results on the probe pool; the registered held-out run "
        "replaces them before submission."
    )
    return out


def main() -> None:
    text = TEMPLATE.read_text(encoding="utf-8")
    values = numbers()
    filled = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], text)
    left = re.findall(r"\{\{\w+\}\}", filled)
    if left:
        raise SystemExit(f"unfilled: {left}")
    OUT.write_text(filled, encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
