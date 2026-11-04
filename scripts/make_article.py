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
from collections import Counter

from aya_retrieval.provenance import REPO_ROOT
from aya_retrieval.report_data import (
    COHERENCE_DIR,
    EVAL_DIR,
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
    recall_sources,
    share,
    train_report,
)
from aya_retrieval.stats import bootstrap_gain_interval, exact_sign_test

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
SCREENS = [  # label, its reference, what changed, outcome (the record that decided it)
    (
        "screen_full82",
        "screen_base",
        "v2: the full training set",
        "the reference for fixes 1 and 1b",
    ),
    (
        "screen_read_hint82",
        "screen_full82",
        "Fix 1: read in-view facts through a hint",
        "led to 1b (R-024)",
    ),
    ("screen_hard_in_view82", "screen_full82", "Fix 1b: 75 hard in-view rows", "**v3** (R-026)"),
    (
        "screen_few_never_told82",
        "screen_hard_in_view82",
        "Fix 3: fewer never-told rows",
        "dropped (R-028)",
    ),
    (
        "screen_hard_in_view_lean82",
        "screen_hard_in_view82",
        "v3 retrained with the lean loss",
        "same results (R-032)",
    ),
    (
        "screen_second_search_82",
        "screen_hard_in_view_lean82",
        "Fix 4: a second search after an empty one",
        "dropped (R-032)",
    ),
    (
        "screen_coherent_targets_82",
        "screen_hard_in_view_lean82",
        "Fix 5: a judge filters the training answers",
        "dropped on coherence (R-032)",
    ),
    (
        "screen_scripted_confirm_82",
        "screen_hard_in_view_lean82",
        "Fix 5b: plain answers on “did I tell you…?”",
        "failed its coherence rule (R-034)",
    ),
    (
        "screen_relation_answers_82",
        "screen_hard_in_view_lean82",
        "Fix 5c: 5b, and answers name the relation",
        "**v4** (R-036)",
    ),
    (
        "screen_epochs4_82",
        "screen_relation_answers_82",
        "4 epochs instead of 3",
        "candidate (R-037)",
    ),
    (
        "screen_lr1e4_82",
        "screen_relation_answers_82",
        "Learning rate 1e-4 instead of 2e-4",
        "dropped (R-040)",
    ),
    (
        "screen_more_indirect_82",
        "screen_relation_answers_82",
        "Fix 6: more ways of saying “I forgot”",
        "candidate (R-040)",
    ),
    (
        "screen_lora_mlp_82",
        "screen_relation_answers_82",
        "LoRA on the MLP layers too",
        "candidate (R-044)",
    ),
    ("screen_lora_r32_82", "screen_relation_answers_82", "LoRA rank 32", "candidate (R-044)"),
    ("screen_lr3e4_82", "screen_relation_answers_82", "Learning rate 3e-4", "candidate (R-046)"),
    (
        "screen_fix6_mlp_82",
        "screen_more_indirect_82",
        "Fix 6 with LoRA on the MLP layers",
        "no gain over fix 6 (R-047)",
    ),
    ("screen_fix6_r32_82", "screen_more_indirect_82", "Fix 6 at rank 32", "beaten (R-052)"),
    (
        "screen_fix6_mlp_r32_82",
        "screen_more_indirect_82",
        "Fix 6 at rank 32 with the MLP layers",
        "ties rank 32 alone (R-048)",
    ),
    (
        "screen_message_queries_82",
        "screen_more_indirect_82",
        "Fix 7: searches in the friend's own words",
        "dropped on false retrieval (R-050)",
    ),
    (
        "screen_more_statements_82",
        "screen_more_indirect_82",
        "Fix 8: more ways of stating each fact",
        "candidate on the lead's settings (R-054)",
    ),
    ("screen_fix6_lr3e4_82", "screen_more_indirect_82", "Fix 6 at 3e-4", "ties rank 32 (R-052)"),
    (
        "screen_fix6_all_82",
        "screen_more_indirect_82",
        "Fix 6 at rank 32, with MLP, at 3e-4",
        "failed its coherence rule (R-055)",
    ),
    (
        "screen_fix6_r64_82",
        "screen_fix6_r32_82",
        "Fix 6 at rank 64",
        "no gain over rank 32 (R-053)",
    ),
    (
        "screen_never_told_hits_82",
        "screen_more_indirect_82",
        "Fix 7b: 7, never-told rows only with results",
        "dropped on statements (R-054)",
    ),
    (
        "screen_fix6_r32_lr3e4_82",
        "screen_fix6_all_82",
        "Fix 6 at rank 32 and 3e-4, attention only",
        "loses statements (R-053)",
    ),
    (
        "screen_fix9_all_82",
        "screen_fix6_all_82",
        "Fix 9: more plain-chat lines, lead's settings",
        "passed its screen; confirmation (R-056)",
    ),
    (
        "screen_fix8_all_82",
        "screen_fix6_all_82",
        "Fix 8 data on the lead's settings",
        "loses statements (R-056)",
    ),
    (
        "screen_fix6_all_e4_82",
        "screen_fix6_all_82",
        "Lead's settings, 4 epochs",
        "loses statements (R-056)",
    ),
]
KIND_NAMES = {
    "older": "Fact told long ago",
    "confirm": "“Did I tell you…?”",
    "in_view": "Fact still on screen",
    "never_told": "Never told",
    "statement": "Just chatting",
}


def pct(pair: tuple[int, int]) -> str:
    return f"{100 * pair[0] / pair[1]:.0f}"


def lr_text(rate: float) -> str:
    mantissa, exponent = f"{rate:.0e}".split("e")
    return f"{mantissa}e{int(exponent)}"


def p_text(p: float) -> str:
    return "<0.01" if p < 0.01 else f"{p:.2f}"


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
    dropped = [
        change
        for label, _, change, outcome in SCREENS
        if outcome.startswith("dropped")
        and (EVAL_DIR / f"{label}_seed_{SCREEN_PROBE}.json").exists()
    ]
    parts = [
        "**Changes that did not help were dropped**, with their numbers in the table: "
        + "; ".join(d[0].lower() + d[1:] for d in dropped)
        + "."
    ]
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


def ablation_numbers(out) -> None:
    """One row per screen with a results file, against its own reference, on the screen probe."""
    lines = []
    for label, reference, change, outcome in SCREENS:
        path = EVAL_DIR / f"{label}_seed_{SCREEN_PROBE}.json"
        if not path.exists():
            continue
        new = {r["id"]: r for r in eval_rows(label, SCREEN_PROBE)}
        ref = {r["id"]: r for r in eval_rows(reference, SCREEN_PROBE)}
        rows = list(new.values())
        only_ref = sum(ref[i]["correct"] and not new[i]["correct"] for i in ref)
        only_new = sum(new[i]["correct"] and not ref[i]["correct"] for i in ref)
        in_view = by_kind(rows)["in_view"]
        lines.append(
            f"| {change} | {recall(rows)[0]} ({recall(list(ref.values()))[0]}) "
            f"| {in_view[0]} | {share(rows, 'right_decision')[0]} "
            f"| {only_ref} / {only_new} | {p_text(exact_sign_test(only_ref, only_new))} "
            f"| {outcome} |"
        )
    base = eval_rows("screen_base", SCREEN_PROBE)
    out["ablation_table"] = (
        "| Change | Recall of 96 (reference) | On screen of 48 | Right decisions of 240 "
        "| Right, all kinds: only reference / only change | Sign test p | Outcome |\n"
        "|---|---|---|---|---|---|---|\n"
        f"| Untrained model | {recall(base)[0]} | {by_kind(base)['in_view'][0]} "
        f"| {share(base, 'right_decision')[0]} | | | |\n" + "\n".join(lines)
    )


def sources_numbers(base, tuned, out) -> None:
    """Right answers on questions that need a search, split by whether the fact was retrieved."""
    b = recall_sources(base)
    seeds = [recall_sources(tuned[s]) for s in SEEDS]
    t = {key: sum(s[key] for s in seeds) for key in b}
    rows = [
        ("Right, fact in its own search results", "retrieved"),
        ("Right, searched but the fact was not returned", "searched_not_returned"),
        ("Right without searching", "no_search"),
        ("Wrong although the fact was returned", "wrong_though_retrieved"),
    ]
    table = "\n".join(f"| {name} | {b[key]} | {t[key]} |" for name, key in rows)
    guesses_b = b["searched_not_returned"] + b["no_search"]
    guesses_t = t["searched_not_returned"] + t["no_search"]
    right_t = t["retrieved"] + guesses_t
    out["sources_text"] = (
        f"| Questions that need a search | Untrained ({b['questions']}) "
        f"| Adapter, {len(SEEDS)} seeds ({t['questions']}) |\n|---|---|---|\n"
        + table
        + f"\n\nOf the adapter's {right_t} right answers, {t['retrieved']} were retrieved and "
        f"{guesses_t} {'was a guess' if guesses_t == 1 else 'were guesses'} "
        f"(the untrained model: {b['retrieved']} and {guesses_b}). "
        + (
            "The gain is recovered information, not better guessing. "
            if guesses_t <= 0.05 * right_t
            else "A share of the gain is guessing, counted here apart. "
        )
        + "The final test applies the recall rule to "
        "retrieved answers alone as well (R-041)."
    )


def interval_numbers(base, tuned, out) -> None:
    """95% intervals for the headline recall gains, resampling conversations."""
    parts = []
    for size in SIZES:
        ids = [r["id"] for r in base if r["kind"] in ("older", "confirm") and r["size"] == size]
        b = {r["id"]: int(r["correct"]) for r in base}
        a = [{r["id"]: int(r["correct"]) for r in tuned[s]} for s in SEEDS]
        gain = bootstrap_gain_interval([b[i] for i in ids], [[t[i] for i in ids] for t in a])
        rel, low, high = gain["relative_gain"]
        parts.append(
            f"at {size} messages {100 * rel:+.0f}% (95% interval {100 * low:+.0f}% to "
            f"{100 * high:+.0f}%, {len(ids)} conversations)"
        )
    out["recall_intervals"] = "Recall above the untrained model, " + "; ".join(parts) + "."


CURRENT_TRAIN_REPORT = "screen_relation_answers_82"  # v4, seed 82
FIRST_ADAPTER = ("tuned81", 45356)  # R-018, training-style conversations


def setup_numbers(out) -> None:
    report = train_report(CURRENT_TRAIN_REPORT)
    data = REPO_ROOT / report["data"]
    lines = data.read_text(encoding="utf-8").splitlines()
    kinds = Counter(json.loads(line)["kind"] for line in lines)
    per_kind = ", ".join(f"{KIND_NAMES[k]} {kinds[k]}" for k in KINDS)
    out["training_setup"] = (
        f"{report['rows']} rows ({per_kind}); LoRA rank {report.get('lora_r', 16)} on the "
        f"attention projections, learning rate {lr_text(report['learning_rate'])}, "
        f"{report['epochs']} epochs, batch {report['batch_size']}."
    )
    before, after = train_report(TRL_LOSS_RUN), train_report(LEAN_LOSS_RUN)
    out["mem_saved"] = f"{before['train_peak_vram_gib'] - after['train_peak_vram_gib']:.1f}"
    label, seed = FIRST_ADAPTER
    first = share(eval_rows(label, seed))
    out["first_adapter"] = f"{first[0]} of {first[1]}"
    old = {r["id"]: r for r in eval_rows("screen_hard_in_view82", SCREEN_PROBE)}
    new = {r["id"]: r for r in eval_rows("screen_hard_in_view_lean82", SCREEN_PROBE)}
    differ = sum(old[i]["correct"] != new[i]["correct"] for i in old)
    out["lean_retrain_diff"] = f"{differ} of {len(old)}"


# Published prices, read 2026-11-03. Per million tokens: input, cached input, output.
# Source: https://developers.openai.com/api/docs/pricing (standard tier, short context).
CLOSED_PRICES = {
    "gpt-6-astra": (10.00, 1.00, 50.00),
    "gpt-6.1-sol": (2.00, 0.10, 10.00),
    "gpt-6.1-terra": (1.00, 0.05, 5.00),
    "gpt-6-luna": (0.10, 0.01, 0.50),
}
# Dollars per GPU hour. Source: https://huggingface.co/docs/inference-endpoints/en/pricing
GPU_PRICE = ("NVIDIA A10G on Hugging Face Inference Endpoints (AWS)", 1.00)
THROUGHPUT = REPO_ROOT / "results" / "throughput" / "v4_seed_82.json"
ROI_SIZE = 419


def roi_numbers(tuned, out) -> None:
    """Cost per million turns: the adapter self-hosted against closed models sent the whole chat."""
    rows = [r for s in SEEDS for r in tuned[s] if r["size"] == ROI_SIZE]
    read = sum(r["tokens_read"] for r in rows) / len(rows)
    written = sum(r["tokens_written"] for r in rows) / len(rows)
    whole = sum(r["whole_chat_tokens"] for r in rows) / len(rows)
    calls = 1 + sum(len(r["queries"]) for r in rows) / len(rows)
    out["roi_tokens"] = (
        f"At {ROI_SIZE} messages the adapter reads {read:,.0f} tokens a turn on average over "
        f"{calls:.2f} model calls and writes {written:.0f}; the whole chat is {whole:,.0f} tokens, "
        f"so it reads {100 * (1 - read / whole):.0f}% less."
    )
    if not THROUGHPUT.exists():
        out["roi_text"] = (
            "*Pending: the throughput benchmark (`scripts/run_throughput.py`) is queued.*"
        )
        return
    bench = json.loads(THROUGHPUT.read_text(encoding="utf-8"))
    gpu_name, per_hour = GPU_PRICE
    lines, self_costs, closed = [], [], {}
    for b in bench["batches"]:
        cost = 1e6 * calls / b["calls_per_hour"] * per_hour
        self_costs.append((b["batch_size"], cost))
        lines.append(f"| This adapter, self-hosted, batch {b['batch_size']} | ${cost:,.0f} | |")
    for model, (inp, cached, outp) in CLOSED_PRICES.items():
        plain = whole * inp + written * outp  # dollars per million turns
        warm = whole * cached + written * outp
        closed[model] = (plain, warm)
        lines.append(f"| {model}, whole chat each turn | ${plain:,.0f} | ${warm:,.0f} |")
    batch, best = self_costs[-1]
    cheapest = min(closed, key=lambda m: closed[m][0])
    ratios = sorted(closed[m][0] / best for m in closed)
    summary = (
        f"At batch {batch} the adapter costs ${best:,.0f} per million turns, "
        f"{ratios[0]:.0f}× to {ratios[-1]:.0f}× less than these closed models sent the whole chat. "
        + (
            f"With every chat token billed at the cached rate, the cheapest closed model "
            f"({cheapest}, ${closed[cheapest][1]:,.0f}) costs about the same or less, so the "
            "saving there is privacy and control rather than money."
            if closed[cheapest][1] <= 1.25 * best
            else f"Even fully cached, the cheapest closed model costs ${closed[cheapest][1]:,.0f}."
        )
    )
    out["roi_text"] = (
        "| Per million turns | Cost | With the chat prefix cached |\n|---|---|---|\n"
        + "\n".join(lines)
        + f"\n\n{summary}\n\n"
        f"**Assumptions.** Self-hosted cost assumes the {gpu_name} at ${per_hour:.2f} an hour "
        f"serves calls as fast as the measured card ({bench['gpu']}, plain Transformers, calls of "
        f"about {bench['batches'][0]['mean_prompt_tokens']} prompt tokens). The A10G has less "
        "memory bandwidth than that card, so it would likely be somewhat slower, while a "
        "dedicated serving engine would be faster. Closed-model cost sends the whole chat each "
        "turn and writes as many tokens as the adapter; the cached column charges every chat token "
        "at the cached rate, the most favourable case for the closed model. A closed model could "
        "also retrieve instead of reading the whole chat; the point here is that a 3B model can "
        "do the retrieval itself."
    )


def numbers() -> dict[str, str]:
    base = eval_rows(BASE, PROBE)
    tuned = {s: eval_rows(f"{TUNED}{s}", PROBE) for s in SEEDS}
    out: dict[str, str] = {}
    recall_numbers(base, tuned, out)
    kind_numbers(base, tuned, out)
    coherence_numbers(out)
    false_retrieval_numbers(base, tuned, out)
    ablation_numbers(out)
    interval_numbers(base, tuned, out)
    sources_numbers(base, tuned, out)
    roi_numbers(tuned, out)
    setup_numbers(out)
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
