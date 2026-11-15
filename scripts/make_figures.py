"""Draw the write-up's figures from committed results files into ``figures/``.

Usage:
    python scripts/make_figures.py

Every value plotted comes from files under ``results/``: the whole-chat control (R-164, R-165),
the outside-writer sets (R-146, R-157), the sealed final run (R-162, R-163) and the training-memory
comparison (R-029, R-032), the sealed S3 test of the reopened work (R-287, through ``score_s3.py``'s
own functions), the hard_dev runs of the on-policy stages (R-261, R-269, R-272) and the demo
contamination check (R-254). The shipped model is 6.37 (``fix17cs37``).
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

from aya_retrieval.provenance import REPO_ROOT  # noqa: E402
from aya_retrieval.report_data import (  # noqa: E402
    RECALL_KINDS,
    eval_rows,
    recall,
    records_script,
    train_report,
    weights_gib,
)

OUT = REPO_ROOT / "figures"
ANALYSIS = REPO_ROOT / "results" / "analysis"
SHIP = "fix17cs37_82"
SEEDS = (82, 83, 94, 95, 96, 97, 98, 99)
ADAPTERS = tuple(f"fix17cs37_{s}" for s in SEEDS)
SETS = {1: "blind", 2: "blind2"}
SET_FILES = {1: ANALYSIS / "R-146" / "blind.json", 2: ANALYSIS / "R-157" / "blind2.json"}
CONDITIONS = {"A": "heldout, 1 decoy", "B": "heldout, 4 decoys", "C": "independent, 1 decoy"}
CONDITIONS["D"] = "independent, 4 decoys"
TRL_LOSS_RUN = "hard_in_view_84"  # v3 data, TRL's loss (R-026)
LEAN_LOSS_RUN = "screen_hard_in_view_lean_82"  # same data, lean loss (R-032)

# One colour per model in every figure (R-301): the untrained base grey, 6.37 blue, C1 orange,
# the other candidates and the report arms purple; Figure 8 has its own outcome palette.
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
BASE_C = "#6f6e69"  # base, every figure
TUNED_C = "#1c5cab"  # 6.37
SEED_C = "#5b97dc"  # 6.37's single seeds
C1_C = "#c4621a"  # C1
REPORT_C = "#7a4fa3"  # K1, K1.3, K2.1, OP, C2
CARD_C = "#d03b3b"
OUTCOME_C = {  # Figure 8's outcomes, apart from the model colours
    "right": "#2f7d4a",
    "misread": "#e2a63b",
    "missed": "#c23b3b",
    "none": "#c3c2b7",
}

plt.rcParams.update(
    {
        "font.family": "Segoe UI",
        "font.size": 10.5,
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": INK_2,
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.8,
        "axes.axisbelow": True,
        "svg.hashsalt": "aya_retrieval",
    }
)


def load(path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def titled(fig, title: str, subtitle: str) -> None:
    height = fig.get_figheight()
    fig.text(
        0.02, 1 - 0.12 / height, title, fontsize=14, fontweight="semibold", color=INK, va="top"
    )
    fig.text(0.02, 1 - 0.44 / height, subtitle, fontsize=10.5, color=INK_2, va="top")


def save(fig, name: str) -> None:
    OUT.mkdir(exist_ok=True)
    for ext in ("png", "svg"):
        meta = {"Date": None} if ext == "svg" else {"Software": None}
        fig.savefig(OUT / f"{name}.{ext}", dpi=200, metadata=meta)
    plt.close(fig)
    print(f"wrote figures/{name}.png and .svg")


def legend(ax, base_label: str, tuned_label: str) -> None:
    handles = [
        Line2D([], [], marker="o", ls="", ms=9, mfc=c, mec=SURFACE, mew=2, label=label)
        for c, label in ((BASE_C, base_label), (TUNED_C, tuned_label))
    ]
    ax.legend(
        handles=handles,
        loc="lower right",
        bbox_to_anchor=(1.0, 1.0),
        ncol=2,
        frameon=False,
        fontsize=10,
        labelcolor=INK_2,
        handletextpad=0.3,
        columnspacing=1.2,
    )


def dumbbell(ax, labels, base_vals, tuned_vals, seed_vals=None, xmax=100, split=None) -> None:
    """Rows top to bottom; a hairline from base to adapter, value labels at both ends.

    ``split``: the number of top rows set apart from the rest by a rule.
    """
    ys = list(range(len(labels)))[::-1]
    if split:
        ax.axhline(len(labels) - split - 0.5, color=AXIS, lw=1, zorder=0)
    pad = 0.022 * xmax
    for y, b, t in zip(ys, base_vals, tuned_vals, strict=True):
        ax.plot([b, t], [y, y], color=AXIS, lw=2, solid_capstyle="round", zorder=1)
        ax.scatter([b], [y], s=110, color=BASE_C, edgecolor=SURFACE, linewidth=2, zorder=3)
        ax.scatter([t], [y], s=130, color=TUNED_C, edgecolor=SURFACE, linewidth=2, zorder=4)
        for value, tuned in ((b, False), (t, True)):
            on_right = value > (t if not tuned else b) or (value == b == t and tuned)
            ax.text(
                value + pad if on_right else value - pad,
                y,
                f"{value:.0f}%",
                ha="left" if on_right else "right",
                va="center",
                color=INK if tuned else INK_2,
                fontsize=10,
                fontweight="semibold" if tuned else "normal",
            )
    if seed_vals:
        for y, seeds in zip(ys, seed_vals, strict=True):
            ax.scatter(
                seeds, [y - 0.24] * len(seeds), s=14, color=SEED_C, alpha=0.7, zorder=2, lw=0
            )
    ax.set_yticks(ys, labels)
    ax.set_ylim(-0.6, len(labels) - 0.45)
    ax.tick_params(axis="y", length=0, labelsize=10.5)
    ax.set_xlim(-0.08 * xmax, 1.08 * xmax)
    ticks = [xmax * i / 4 for i in range(5)]
    ax.set_xticks(ticks, [f"{t:g}%" for t in ticks])
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)


def right(rows: list[dict], kind: str) -> float:
    asked = [r for r in rows if r["kind"] == kind]
    return 100 * sum(bool(r["correct"]) for r in asked) / len(asked)


def fig_whole_chat_or_search() -> None:
    """`older` on the outside-writer sets: three exchanges and search, or the whole chat."""
    labels, base, tuned, tokens = [], [], [], []
    for n, prefix in SETS.items():
        rows = eval_rows(f"{prefix}_base", 0)
        tokens += [r["whole_chat_tokens"] for r in rows]
        older_n = sum(r["kind"] == "older" for r in rows)
        labels += [f"Set {n}: last 3 exchanges, search", f"Set {n}: whole chat"]
        base += [
            right(eval_rows(f"{prefix}_base", 0), "older"),
            right(eval_rows(f"wc_{prefix}_base", 0, "whole_chat"), "older"),
        ]
        tuned += [
            right(eval_rows(f"{prefix}_{SHIP}", 0), "older"),
            right(eval_rows(f"wc_{prefix}_{SHIP}", 0, "whole_chat"), "older"),
        ]
    fig, ax = plt.subplots(figsize=(8, 4.1))
    fig.subplots_adjust(left=0.33, right=0.97, top=0.7, bottom=0.14)
    dumbbell(ax, labels, base, tuned)
    ax.set_xlabel(
        "Older-fact questions answered right (not confirm questions; the tables give recall)"
    )
    legend(ax, "Tiny Aya, untrained", "6.37, seed 82")
    titled(
        fig,
        "When the chat fits, the whole chat wins",
        f"Outside-writer sets, a mean of {round(sum(tokens) / len(tokens), -2):,.0f} tokens "
        f"a chat; {older_n} older-fact questions a set.\n"
        "One run of each arm, one seed of 6.37 (R-164, R-165).",
    )
    save(fig, "whole_chat_or_search")


def fig_recall_out_of_view() -> None:
    """Recall with the last three exchanges in view: outside-writer sets and the sealed run."""
    labels, base, pooled, seeds, whole = [], [], [], [], []
    for n, prefix in SETS.items():
        blind = load(SET_FILES[n])
        per = blind["recall_per_seed"]
        items = blind["primary"]["items"]
        labels.append(f"Outside-writer set {n} ({items})")
        base.append(100 * blind["primary"]["base"] / items)
        pooled.append(100 * sum(per[str(s)] for s in SEEDS) / (items * len(SEEDS)))
        seeds.append([100 * per[str(s)] / items for s in SEEDS])
        whole.append(recall(eval_rows(f"wca_{prefix}_base", 0, "whole_chat_all")))
    for c, name in CONDITIONS.items():
        d = load(ANALYSIS / "R-162" / f"{c}.json")
        kinds = d["per_kind_correct"]
        items = d["shipped_seed_82"]["questions"]
        per = {a: sum(kinds[k][a] for k in RECALL_KINDS) for a in ("base", *ADAPTERS)}
        labels.append(f"Sealed {c}: {name} ({items})")
        base.append(100 * per["base"] / items)
        pooled.append(100 * sum(per[a] for a in ADAPTERS) / (items * len(ADAPTERS)))
        seeds.append([100 * per[a] / items for a in ADAPTERS])
    fig, ax = plt.subplots(figsize=(8, 4.8))
    fig.subplots_adjust(left=0.36, right=0.97, top=0.75, bottom=0.12)
    dumbbell(ax, labels, base, pooled, seeds, split=len(SETS))
    ax.set_xlabel("Recall (older and confirm questions), last 3 exchanges in view")
    legend(ax, "Tiny Aya, untrained", "6.37, eight seeds pooled")
    whole_text = " and ".join(f"{h} of {n}" for h, n in whole)
    titled(
        fig,
        "Recall out of view, untrained and trained",
        "Small dots: each training seed; row labels give the questions a run. Outside-writer sets\n"
        f"R-146, R-157 (base shown the whole chat: {whole_text}); "
        "sealed run R-163 (both pools generator-built).",
    )
    save(fig, "recall_out_of_view")


def fig_memory() -> None:
    weights, card = weights_gib(), 10.0
    before = train_report(TRL_LOSS_RUN)["train_peak_vram_gib"]
    after = train_report(LEAN_LOSS_RUN)["train_peak_vram_gib"]
    fig, ax = plt.subplots(figsize=(8, 3.3))
    fig.subplots_adjust(left=0.15, right=0.97, top=0.66, bottom=0.18)
    rows = [("TRL's loss", before), ("Lean loss", after)]
    for y, (_, peak) in zip((1, 0), rows, strict=True):
        ax.barh(y, weights, height=0.42, color=INK_2, edgecolor=SURFACE, linewidth=2)
        ax.barh(
            y,
            peak - weights,
            left=weights,
            height=0.42,
            color=AXIS,
            edgecolor=SURFACE,
            linewidth=2,
        )
        ax.text(
            max(peak, card) + 0.1,
            y,
            f"{peak:.2f} GiB",
            va="center",
            color=INK,
            fontweight="semibold",
        )
    ax.axvline(card, color=CARD_C, lw=1.5)
    ax.text(card - 0.05, 1.42, "card: 10 GiB", ha="right", va="center", color=INK_2, fontsize=9.5)
    ax.set_yticks([1, 0], [r[0] for r in rows])
    ax.tick_params(axis="y", length=0, labelsize=10.5)
    ax.set_xlim(0, 11.4)
    ax.set_ylim(-0.5, 1.65)
    ax.set_xlabel("Peak card memory during training (GiB)")
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    handles = [
        Line2D(
            [], [], marker="s", ls="", ms=10, mfc=INK_2, mec=INK_2, label="Model weights (bf16)"
        ),
        Line2D([], [], marker="s", ls="", ms=10, mfc=AXIS, mec=AXIS, label="Training on top"),
    ]
    ax.legend(
        handles=handles,
        loc="lower right",
        bbox_to_anchor=(1.0, 1.02),
        ncol=2,
        frameon=False,
        fontsize=10,
        labelcolor=INK_2,
    )
    titled(
        fig,
        f"Same loss, {before - after:.1f} GiB less memory",
        "Longest rows of an early development run (R-029), not 6.37. Same values bit for bit.",
    )
    save(fig, "training_memory")


# --- The reopened work: S3, the on-policy stages, the demos (R-254, R-272, R-287) ----------------

S3 = records_script("score_s3")
ARM_COLOURS = {"always_search": MUTED, "whole_chat": MUTED, "base_tool": BASE_C, "6.37": TUNED_C}
ARM_COLOURS |= {"pick": C1_C}  # every other arm is a report arm: REPORT_C
STAGES = (  # hard_dev seed 82: K1.3, then OP's stage once, twice (C1) and three times (C2)
    ("K1.3, the start", "k1_3_r200"),
    ("OP: one stage", "k13op_r253"),
    ("C1: two stages", "k13opc1_r263"),
    ("C2: three stages", "k13opc2_r271"),
)
NEVER_TOLD_GATE = 44  # R-191: hard_dev never_told at least 44 of 48
DEMOS = {2: "demo2/contamination_demo2.txt", 3: "demo2/contamination_demo3.txt"}
DEMOS |= {4: "demo4/contamination.txt", 5: "demo5/contamination.txt"}


def wilson(hits: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """The Wilson 95% interval of a share."""
    p = hits / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * (p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5 / (1 + z * z / n)
    return centre - half, centre + half


def arm_label(name: str) -> str:
    """The scorer's name for an arm; the pooled 6.37 arm is named by its seeds, not 'shipped'."""
    return S3.ARM_NAMES[name].replace("shipped", "three seeds")


def arm_points(
    ax, measure: str, names: list[str], tables: dict, chats: list[str], fontsize: float = 9
) -> float:
    """One row an arm: the pooled rate and its chat-resampled 95% interval; base's as a band.

    Returns the largest upper bound drawn, in percent, so a caller can fit the x-axis.
    """
    ys = list(range(len(names)))[::-1]
    lo, hi = S3.interval(tables["base_tool"][measure], chats)
    ax.axvspan(100 * lo, 100 * hi, color=GRID, alpha=0.7, lw=0, zorder=0)
    top = 100 * hi
    for y, name in zip(ys, names, strict=True):
        table = tables[name][measure]
        rate, (lo, hi) = S3.rate(table), S3.interval(table, chats)
        top = max(top, 100 * hi)
        hits, n = sum(c[0] for c in table.values()), sum(c[1] for c in table.values())
        colour = ARM_COLOURS.get(name, REPORT_C)
        ax.plot([100 * lo, 100 * hi], [y, y], color=colour, lw=2.2, solid_capstyle="round")
        ax.scatter(
            [100 * rate], [y], s=70, color=colour, edgecolor=SURFACE, linewidth=0.8, zorder=3
        )
        # End ticks above the dot, so an interval narrower than the dot still shows.
        ax.scatter([100 * lo, 100 * hi], [y, y], marker="|", s=60, color=INK, lw=1.1, zorder=4)
        ax.text(100 * hi + 1.5, y, f"{hits}/{n}", va="center", color=INK_2, fontsize=fontsize)
    ax.set_yticks(ys, [arm_label(n) for n in names])
    ax.tick_params(axis="y", length=0, labelsize=10)
    ax.set_ylim(-0.6, len(names) - 0.4)
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    return top


def fig_s3_recall() -> None:
    """S3 recall by arm, with chat-resampled intervals."""
    chats, tables = S3.measure_tables()
    names = list(tables)
    fig, ax = plt.subplots(figsize=(8, 0.42 * len(names) + 1.9))
    fig.subplots_adjust(left=0.29, right=0.93, top=1 - 1.05 / fig.get_figheight(), bottom=0.16)
    arm_points(ax, "recall", names, tables, chats)
    ax.set_xlim(0, 80)
    ax.set_xticks(range(0, 81, 20), [f"{t}%" for t in range(0, 81, 20)])
    ax.set_xlabel("Recall (older and confirm questions), both views")
    titled(
        fig,
        "The sealed S3 test: recall by arm",
        f"{len(chats)} chats; 95% intervals resample chats; grey band: base with the tool. "
        "6.37 and C1 pool seeds 82, 83, 94;\n"
        "the report arms pool seeds 82 and 83 and enter no line of the rule (R-287).",
    )
    save(fig, "s3_recall")


def fig_s3_faults() -> None:
    """The two faults the reopening targeted, by arm on S3."""
    chats, tables = S3.measure_tables()
    names = list(tables)
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 0.42 * len(names) + 2.2), sharey=True)
    fig.subplots_adjust(
        left=0.25,
        right=0.97,
        top=1 - 1.05 / fig.get_figheight(),
        bottom=0.75 / fig.get_figheight(),
        wspace=0.18,
    )
    panels = (
        ("copy", "Names its in-view wrong value\nwhen answering another question"),
        (
            "n_hit_false_answer",
            "Never told, search returned text:\nnames a value listed for the chat",
        ),
    )
    for ax, (measure, label) in zip(axes, panels, strict=True):
        top = arm_points(ax, measure, names, tables, chats, fontsize=10)
        step = 10 if top < 40 else 20
        ticks = range(0, int(top) + 1, step)
        # A little below 0, so a 0% dot and its interval show whole; room right for the counts.
        ax.set_xlim(-0.05 * top, 1.3 * top)
        ax.set_xticks(ticks, [f"{t}%" for t in ticks])
        ax.tick_params(axis="x", labelsize=10)
        ax.set_xlabel(label, fontsize=10)
    axes[1].tick_params(axis="y", labelleft=False)
    titled(
        fig,
        "C1 cuts 6.37's two faults; its false answers stay above base's",
        "Lower is better. Grey band: base with the tool, the line C1 had to be under on the right "
        "(R-178 (c)).\n"
        "95% intervals resample chats; 6.37 and C1 pool three seeds, report arms two.",
    )
    save(fig, "s3_faults")


def fig_s3_misses() -> None:
    """Where recall is lost on S3: right, fact found and misread, searched and missed, no search."""
    rows = S3.arms()
    names = [n for n in rows if n != "whole_chat"]
    parts = (
        ("Right", OUTCOME_C["right"]),
        ("Fact in its own search output, answered wrong", OUTCOME_C["misread"]),
        ("Searched, fact not found", OUTCOME_C["missed"]),
        ("No search", OUTCOME_C["none"]),
    )
    fig, ax = plt.subplots(figsize=(8.6, 0.42 * len(names) + 2.2))
    fig.subplots_adjust(left=0.27, right=0.97, top=1 - 1.45 / fig.get_figheight(), bottom=0.13)
    ys = list(range(len(names)))[::-1]
    for y, name in zip(ys, names, strict=True):
        asked = [r for r in rows[name] if r["kind"] in RECALL_KINDS]
        wrong = [r for r in asked if not r["item_correct"]]
        counts = [
            len(asked) - len(wrong),
            sum(bool(r["found_fact"]) for r in wrong),
            sum(not r["found_fact"] and bool(r["queries"]) for r in wrong),
            sum(not r["found_fact"] and not r["queries"] for r in wrong),
        ]
        left = 0.0
        for count, (_, colour) in zip(counts, parts, strict=True):
            width = 100 * count / len(asked)
            ax.barh(y, width, left=left, height=0.6, color=colour, edgecolor=SURFACE, lw=1.5)
            left += width
        lo, hi = wilson(counts[0], len(asked))
        ax.plot([100 * lo, 100 * hi], [y + 0.36, y + 0.36], color=INK, lw=1.2)
        estimate = 100 * counts[0] / len(asked)
        ax.scatter([estimate], [y + 0.36], s=16, color=INK, lw=0, zorder=4)
        ax.text(101, y, f"n = {len(asked)}", va="center", color=INK_2, fontsize=9)
    ax.set_yticks(ys, [arm_label(n) for n in names])
    ax.tick_params(axis="y", length=0, labelsize=10)
    ax.set_xlim(0, 110)
    ax.set_xticks(range(0, 101, 25), [f"{t}%" for t in range(0, 101, 25)])
    ax.set_xlabel("Share of S3's recall questions (older and confirm, both views)")
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    handles = [Line2D([], [], marker="s", ls="", ms=9, mfc=c, mec=c, label=t) for t, c in parts]
    ax.legend(
        handles=handles,
        loc="lower left",
        bbox_to_anchor=(-0.3, 1.0),
        ncol=2,
        frameon=False,
        fontsize=9,
        labelcolor=INK_2,
    )
    titled(
        fig,
        "Where recall is lost on S3",
        "Black dot and line: the right share and its 95% Wilson interval (rows, not chats). R-287.",
    )
    save(fig, "s3_misses")


def fig_never_told_slide() -> None:
    """hard_dev never_told at seed 82 as OP's stage is repeated (R-261, R-269, R-272)."""
    fig, ax = plt.subplots(figsize=(9, 3.6))
    fig.subplots_adjust(left=0.1, right=0.97, top=0.7, bottom=0.2)
    ax.axhspan(NEVER_TOLD_GATE - 0.5, 48.5, color=GRID, alpha=0.7, lw=0, zorder=0)
    counts = []
    for x, (label, run) in enumerate(STAGES):
        asked = [r for r in eval_rows(f"hd_{run}_82", 73157) if r["kind"] == "never_told"]
        hits = sum(bool(r["correct"]) for r in asked)
        counts.append(f"{label.split(':')[0].split(',')[0]} {hits}")
        colour = C1_C if run == "k13opc1_r263" else REPORT_C
        lo, hi = wilson(hits, len(asked))
        ax.plot([x, x], [lo * len(asked), hi * len(asked)], color=colour, lw=2.2)
        ax.scatter([x], [hits], s=100, color=colour, edgecolor=SURFACE, linewidth=0.8, zorder=3)
        ax.text(x + 0.08, hits, f"{hits} of {len(asked)}", va="center", color=INK, fontsize=10)
    ax.set_xticks(range(len(STAGES)), [s[0] for s in STAGES])
    ax.set_xlim(-0.4, len(STAGES) - 0.4)
    ax.set_ylim(35, 49.5)
    ax.set_yticks(range(36, 49, 2))
    ax.set_ylabel("Never-told questions declined", fontsize=9.5)
    ax.grid(axis="x", visible=False)
    ax.text(
        0.5, NEVER_TOLD_GATE - 0.3, "the gate: at least 44", ha="center", color=INK_2, fontsize=9
    )
    titled(
        fig,
        f"hard_dev never-told declines at seed 82: {', '.join(counts)} of {len(asked)}",
        "Exploratory: one run each, hard_dev, seed 82; Wilson 95% intervals overlap;\n"
        "grey band: passes the gate.",
    )
    save(fig, "never_told_slide")


def fig_demo_contamination() -> None:
    """Demo answer keys that are training fact values (R-254)."""
    results = REPO_ROOT / "results"
    fig, ax = plt.subplots(figsize=(8, 3.0))
    fig.subplots_adjust(left=0.14, right=0.97, top=0.7, bottom=0.2)
    for y, (n, path) in zip(range(len(DEMOS))[::-1], DEMOS.items(), strict=True):
        questions = load(REPO_ROOT / f"demo{n}" / "questions.json")["questions"]
        keys = sum(q["kind"] != "never_told" for q in questions)
        text = (results / path).read_text(encoding="utf-8").splitlines()
        line = next(t for t in text if "fact value" in t)
        hits = len(json.loads(line.split(":", 1)[1]))
        ax.barh(y, keys, height=0.55, color=GRID, edgecolor=SURFACE)
        ax.barh(y, hits, height=0.55, color=CARD_C, edgecolor=SURFACE)
        ax.text(keys + 0.15, y, f"{hits} of {keys}", va="center", color=INK, fontsize=10)
    ax.set_yticks(range(len(DEMOS))[::-1], [f"Demo{n}" for n in DEMOS])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 9.5)
    ax.set_xlabel("Answer keys that are fact values in the training data (red)")
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)
    titled(
        fig,
        "Two demos held answers the candidates had trained on",
        "Every training set and writer chat checked; "
        "Demo4 and Demo5 rewritten until clean (R-254).",
    )
    save(fig, "demo_contamination")


if __name__ == "__main__":
    fig_whole_chat_or_search()
    fig_recall_out_of_view()
    fig_memory()
    fig_s3_recall()
    fig_s3_faults()
    fig_s3_misses()
    fig_never_told_slide()
    fig_demo_contamination()
