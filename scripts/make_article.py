"""Fill the article template's numbers from committed results files and write ``docs/ARTICLE.md``.

Usage:
    python scripts/make_article.py

Every ``{{name}}`` in ``docs/article_template.md`` is computed here from files under ``results/``,
so no number in the article is typed by hand. A placeholder left unfilled stops the script.
The current set is v3 on probe seed 73157 (development); the final run swaps in the held-out files.
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
    eval_rows,
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
TUNED = "probe4_tuned"  # v3
SCREEN_PROBE = 51203
SCREEN_REFERENCE = "screen_hard_in_view_lean82"
DROPPED = {
    "fewer “never told” rows (fix 3)": "screen_few_never_told82",
    "a second search after an empty one (fix 4)": "screen_second_search_82",
}
SHEET_A = ("R-027", "judge/marks_a82.json", "sheet_a82/key.json")
SHEET_B = [("R-026", f"judge/marks_{s}.json", f"sheet_b{s}/key.json") for s in SEEDS]
AUDIT = REPO_ROOT / "results" / "audit" / "v3_probe73157.json"
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


def sheet(record: str, marks: str, key: str):
    folder = COHERENCE_DIR / record
    return coherence_by_model_and_kind(folder / marks, folder / key)


def totals(counts: dict[str, tuple[int, int]]) -> tuple[int, int]:
    return pooled(list(counts.values()))


def numbers() -> dict[str, str]:
    base = eval_rows(BASE, PROBE)
    tuned = {s: eval_rows(f"{TUNED}{s}", PROBE) for s in SEEDS}
    out: dict[str, str] = {}

    for size in SIZES:
        b = recall(base, size)
        t = pooled([recall(tuned[s], size) for s in SEEDS])
        out[f"base_recall_{size}"], out[f"tuned_recall_{size}"] = pct(b), pct(t)
        out[f"gain_{size}"] = signed(percent_above(t, b))

    kb = by_kind(base)
    lines = []
    for kind in KINDS:
        t = pooled([by_kind(tuned[s])[kind] for s in SEEDS])
        lines.append(
            f"| {KIND_NAMES[kind]} | {pct(kb[kind])}% | {pct(t)}% "
            f"| {signed(percent_above(t, kb[kind]))}% |"
        )
    out["kind_table"] = "\n".join(lines)

    decisions = [share(tuned[s], "right_decision") for s in SEEDS]
    out["decisions_base"] = str(share(base, "right_decision")[0])
    out["decisions_n"] = str(len(base))
    seed_list = ", ".join(map(str, SEEDS))
    out["decisions_tuned"] = ", ".join(str(d[0]) for d in decisions) + f" (seeds {seed_list})"

    a = sheet(*SHEET_A)
    a_base, a_tuned = totals(a["base"]), totals(a["tuned"])
    out["coherence_overall_change"] = f"{percent_above(a_tuned, a_base):.0f}% more"
    b_rows = []
    for (record, marks, key), seed in zip(SHEET_B, SEEDS, strict=True):
        s = sheet(record, marks, key)
        b_rows.append(f"{totals(s['tuned'])[0]} against {totals(s['base'])[0]} (seed {seed})")
    conf_b, conf_t = a["base"]["confirm"], a["tuned"]["confirm"]
    gaining = sum(a["tuned"][k][0] > a["base"][k][0] for k in KINDS)
    words = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}
    out["coherence_text"] = (
        f"**With the search tool** (adapter seed 82, every kind): the adapter's replies are "
        f"coherent {a_tuned[0]} of {a_tuned[1]} times against the untrained model's {a_base[0]}, "
        f"{signed(percent_above(a_tuned, a_base))}%. {words[gaining]} kinds gain. "
        f"**One kind loses:** on "
        f"“Did I tell you…?” the adapter is coherent {conf_t[0]} of {conf_t[1]} times "
        f"against {conf_b[0]}. Its incoherent replies open with a reaction to news "
        f"(“That's great news!”) when the friend asked a question, a habit carried over "
        f"from some of the untrained model's own answers in the training data. This is the open "
        f"problem the next fix targets.\n\n"
        f"**Ordinary talk, with no tool at all** (just chatting and facts on screen, "
        f"{totals(s['base'])[1]} replies a sheet, {len(SEEDS)} adapter seeds, each against the "
        f"untrained model): " + "; ".join(b_rows) + ". "
        "Training the tool habit did not cost ordinary conversation."
    )

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
    v82 = audit["bootstrap"][f"{TUNED}82"]["all_kinds"]["bootstrap"]
    out["auditkit_bug_example"] = (
        f"{100 * v82['mean_base']:.0f}% → {100 * v82['mean_adapter']:.0f}% "
        f"over {v82['n']} paired cases"
    )

    before, after = train_report(TRL_LOSS_RUN), train_report(LEAN_LOSS_RUN)
    out["mem_before"] = f"{before['train_peak_vram_gib']:.2f}"
    out["mem_after"] = f"{after['train_peak_vram_gib']:.2f}"
    steps = after["rows"] / after["batch_size"] * after["epochs"]
    out["step_seconds"] = f"{after['train_seconds'] / steps:.1f}"

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
    out["dropped_fixes"] = " ".join(parts)

    out["results_scope"] = (
        f"Development numbers: the probe pool, {len(base)} conversations "
        f"({len(base) // 10} of each kind at each length), the untrained model against "
        f"{len(SEEDS)} adapters trained on seeds {seed_list}. The held-out run replaces these."
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
