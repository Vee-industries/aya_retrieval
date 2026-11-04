"""Draw the write-up's figures from committed results files into ``figures/``.

Usage:
    python scripts/make_figures.py

Every value plotted comes from ``aya_retrieval.report_data`` on files under ``results/``. The
current set is v3 on probe seed 73157 (R-026, R-027); the final run swaps in the held-out files.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

from aya_retrieval.provenance import REPO_ROOT  # noqa: E402
from aya_retrieval.report_data import (  # noqa: E402
    KINDS,
    SIZES,
    by_kind,
    coherence_pooled,
    eval_rows,
    false_retrieval,
    pooled,
    recall,
    train_report,
    weights_gib,
)

OUT = REPO_ROOT / "figures"
PROBE = 73157
SEEDS = (82, 83, 84)
BASE_LABEL = "probe2_base"
VERSIONS = {
    "v1": "probe2_tuned",
    "v2": "probe3_tuned",
    "v3": "probe4_tuned",
    "v4": "probe6_tuned",
    "v5": "probe12_tuned",
}
CURRENT = "v5"
SHEET_A_RECORD = "R-061"  # v5, older and confirm, with the tool
SHEET_B_RECORD = "R-061B"  # v5, statement and in_view, base with no tool
TRL_LOSS_RUN = "hard_in_view_84"  # v3 data, TRL's loss (R-026)
LEAN_LOSS_RUN = "screen_hard_in_view_lean_82"  # same data, lean loss (R-032)

# Reference palette (dataviz skill): one hue, two shades for before -> after, validated --ordinal.
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"
BASE_C = "#86b6ef"
TUNED_C = "#1c5cab"
SEED_C = "#2a78d6"
CARD_C = "#d03b3b"

KIND_NAMES = {
    "older": "Fact told long ago",
    "confirm": "“Did I tell you…?”",
    "in_view": "Fact still on screen",
    "never_told": "Never told",
    "statement": "Just chatting",
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
        "xtick.color": MUTED,
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


def pct(hits_total: tuple[int, int]) -> float:
    return 100 * hits_total[0] / hits_total[1]


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


def legend(ax) -> None:
    handles = [
        Line2D(
            [],
            [],
            marker="o",
            ls="",
            ms=9,
            mfc=BASE_C,
            mec=SURFACE,
            mew=2,
            label="Tiny Aya, untrained",
        ),
        Line2D(
            [],
            [],
            marker="o",
            ls="",
            ms=9,
            mfc=TUNED_C,
            mec=SURFACE,
            mew=2,
            label="With the adapter",
        ),
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


def dumbbell(ax, labels, base_vals, tuned_vals, seed_vals=None, xmax=100) -> None:
    """Rows top to bottom; a hairline from base to adapter, value labels at both ends.

    The adapter's value is always the bold one, on whichever side it falls.
    """
    ys = list(range(len(labels)))[::-1]
    pad = 0.022 * xmax
    fmt = "{:.0f}%" if xmax > 40 else "{:.1f}%"
    for y, b, t in zip(ys, base_vals, tuned_vals, strict=True):
        ax.plot([b, t], [y, y], color=AXIS, lw=2, solid_capstyle="round", zorder=1)
        ax.scatter([b], [y], s=110, color=BASE_C, edgecolor=SURFACE, linewidth=2, zorder=3)
        ax.scatter([t], [y], s=130, color=TUNED_C, edgecolor=SURFACE, linewidth=2, zorder=4)
        for value, tuned in ((b, False), (t, True)):
            on_right = value > (t if not tuned else b) or (value == b == t and tuned)
            ax.text(
                value + pad if on_right else value - pad,
                y,
                fmt.format(value),
                ha="left" if on_right else "right",
                va="center",
                color=INK if tuned else INK_2,
                fontsize=10,
                fontweight="semibold" if tuned else "normal",
            )
    if seed_vals:
        for y, seeds in zip(ys, seed_vals, strict=True):
            ax.scatter(
                seeds, [y - 0.22] * len(seeds), s=14, color=SEED_C, alpha=0.7, zorder=2, lw=0
            )
    ax.set_yticks(ys, labels)
    ax.set_ylim(-0.6, len(labels) - 0.45)
    ax.tick_params(axis="y", length=0, labelsize=10.5)
    ax.set_xlim(-0.08 * xmax, 1.08 * xmax)
    ticks = [xmax * i / 4 for i in range(5)]
    ax.set_xticks(ticks, [f"{t:g}%" for t in ticks])
    ax.grid(axis="y", visible=False)
    ax.spines["left"].set_visible(False)


def current_rows():
    base = eval_rows(BASE_LABEL, PROBE)
    tuned = {s: eval_rows(f"{VERSIONS[CURRENT]}{s}", PROBE) for s in SEEDS}
    return base, tuned


def fig_recall_by_length() -> None:
    base, tuned = current_rows()
    labels = [f"{size} messages" for size in SIZES]
    b = [pct(recall(base, s)) for s in SIZES]
    t = [pct(pooled([recall(tuned[k], s) for k in SEEDS])) for s in SIZES]
    seeds = [[pct(recall(tuned[k], s)) for k in SEEDS] for s in SIZES]
    fig, ax = plt.subplots(figsize=(8, 3.1))
    fig.subplots_adjust(left=0.17, right=0.97, top=0.68, bottom=0.2)
    dumbbell(ax, labels, b, t, seeds)
    ax.set_xlabel("Questions about earlier facts answered correctly")
    legend(ax)
    titled(
        fig,
        "Recall out of view, before and after training",
        f"Probe pool, {len(SEEDS)} adapter seeds pooled (small dots: each seed). "
        "Only the last 3 exchanges are in view.",
    )
    save(fig, "recall_by_length")


def fig_by_kind() -> None:
    base, tuned = current_rows()
    kb = by_kind(base)
    kt = {k: pooled([by_kind(tuned[s])[k] for s in SEEDS]) for k in KINDS}
    seeds = [[pct(by_kind(tuned[s])[k]) for s in SEEDS] for k in KINDS]
    fig, ax = plt.subplots(figsize=(8, 4.3))
    fig.subplots_adjust(left=0.24, right=0.97, top=0.75, bottom=0.13)
    dumbbell(
        ax,
        [KIND_NAMES[k] for k in KINDS],
        [pct(kb[k]) for k in KINDS],
        [pct(kt[k]) for k in KINDS],
        seeds,
    )
    ax.set_xlabel("Right answer or right action")
    legend(ax)
    titled(
        fig,
        "Every kind of message, before and after",
        "Probe pool, both chat lengths. “Never told”: says so instead of inventing. "
        "“Just chatting”: no needless search.",
    )
    save(fig, "by_kind")


def fig_coherence() -> None:
    with_tool = coherence_pooled(SHEET_A_RECORD, [f"a{s}" for s in SEEDS])
    no_tool = coherence_pooled(SHEET_B_RECORD, [f"b{s}" for s in SEEDS])
    kinds = [k for k in KINDS if k in with_tool["tuned"] or k in no_tool["tuned"]]
    counts = {k: with_tool if k in with_tool["tuned"] else no_tool for k in kinds}
    fig, ax = plt.subplots(figsize=(8, 3.9))
    fig.subplots_adjust(left=0.24, right=0.97, top=0.72, bottom=0.14)
    dumbbell(
        ax,
        [KIND_NAMES[k] for k in kinds],
        [pct(counts[k]["base"][k]) for k in kinds],
        [pct(counts[k]["tuned"][k]) for k in kinds],
    )
    ax.set_xlabel("Replies a blind judge marked coherent")
    legend(ax)
    titled(
        fig,
        "Coherence, judged blind",
        f"Probe pool, {len(SEEDS)} seeds pooled. Fact questions with the tool; "
        "the rest against the untrained model with no tool.",
    )
    save(fig, "coherence_by_kind")


def fig_false_retrieval() -> None:
    base, _ = current_rows()
    b = false_retrieval(BASE_LABEL, PROBE)
    t = {
        k: pooled([false_retrieval(f"{VERSIONS[CURRENT]}{s}", PROBE)[k] for s in SEEDS])
        for k in KINDS
    }
    seeds = [
        [pct(false_retrieval(f"{VERSIONS[CURRENT]}{s}", PROBE)[k]) for s in SEEDS] for k in KINDS
    ]
    top = max(
        10.0, max(max(pct(b[k]), pct(t[k]), *row) for k, row in zip(KINDS, seeds, strict=True))
    )
    fig, ax = plt.subplots(figsize=(8, 4.3))
    fig.subplots_adjust(left=0.24, right=0.97, top=0.75, bottom=0.13)
    dumbbell(
        ax,
        [KIND_NAMES[k] for k in KINDS],
        [pct(b[k]) for k in KINDS],
        [pct(t[k]) for k in KINDS],
        seeds,
        xmax=20 * -(-top // 20),
    )
    ax.set_xlabel("Replies naming a wrong value of the fact asked about (lower is better)")
    legend(ax)
    titled(
        fig,
        "False retrieval: the wrong person's fact",
        f"Probe pool, one decoy a chat, {len(SEEDS)} seeds pooled (small dots: each seed). "
        "Never told: any value at all.",
    )
    save(fig, "false_retrieval")


def fig_development_path() -> None:
    base = eval_rows(BASE_LABEL, PROBE)
    names = list(VERSIONS)
    fig, ax = plt.subplots(figsize=(8, 3.8))
    fig.subplots_adjust(left=0.1, right=0.86, top=0.76, bottom=0.14)
    xs = list(range(len(names) + 1))
    means = [pct(recall(base))]
    for i, v in enumerate(names, start=1):
        per_seed = [pct(recall(eval_rows(f"{VERSIONS[v]}{s}", PROBE))) for s in SEEDS]
        ax.scatter([i] * len(per_seed), per_seed, s=22, color=SEED_C, alpha=0.7, lw=0, zorder=2)
        means.append(pct(pooled([recall(eval_rows(f"{VERSIONS[v]}{s}", PROBE)) for s in SEEDS])))
    ax.plot(xs, means, color=TUNED_C, lw=2, zorder=3, solid_capstyle="round")
    ax.scatter(xs[1:], means[1:], s=70, color=TUNED_C, edgecolor=SURFACE, linewidth=2, zorder=4)
    ax.scatter(xs[:1], means[:1], s=70, color=BASE_C, edgecolor=SURFACE, linewidth=2, zorder=4)
    ax.text(
        xs[-1] + 0.12, means[-1], f"{means[-1]:.0f}%", va="center", color=INK, fontweight="semibold"
    )
    ax.text(xs[0] + 0.12, means[0], f"{means[0]:.0f}%", va="center", color=INK_2)
    ax.set_xticks(xs, ["Untrained", *(f"Adapter {v}" for v in names)])
    ax.tick_params(axis="x", length=0, colors=INK_2)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.grid(axis="x", visible=False)
    ax.set_ylabel("Recall out of view")
    titled(
        fig,
        "Each training set, one fix at a time",
        "Probe pool, line: 3 seeds pooled, dots: each seed. "
        "Each kept only if it passed a rule written before its 3-seed runs.",
    )
    save(fig, "development_path")


def fig_memory() -> None:
    weights, card = weights_gib(), 10.0
    before = train_report(TRL_LOSS_RUN)["train_peak_vram_gib"]
    after = train_report(LEAN_LOSS_RUN)["train_peak_vram_gib"]
    fig, ax = plt.subplots(figsize=(8, 3.3))
    fig.subplots_adjust(left=0.15, right=0.97, top=0.66, bottom=0.18)
    rows = [("TRL's loss", before), ("Lean loss", after)]
    for y, (_, peak) in zip((1, 0), rows, strict=True):
        ax.barh(y, weights, height=0.42, color=TUNED_C, edgecolor=SURFACE, linewidth=2)
        ax.barh(
            y,
            peak - weights,
            left=weights,
            height=0.42,
            color=BASE_C,
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
            [], [], marker="s", ls="", ms=10, mfc=TUNED_C, mec=TUNED_C, label="Model weights (bf16)"
        ),
        Line2D([], [], marker="s", ls="", ms=10, mfc=BASE_C, mec=BASE_C, label="Training on top"),
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
        "Longest training rows. The lean loss gives TRL's values bit for bit, "
        "and training runs beside a browser.",
    )
    save(fig, "training_memory")


if __name__ == "__main__":
    fig_recall_by_length()
    fig_by_kind()
    fig_coherence()
    fig_development_path()
    fig_memory()
    fig_false_retrieval()
