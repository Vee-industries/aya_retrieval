"""Draw the write-up's figures from committed results files into ``figures/``.

Usage:
    python scripts/make_figures.py

Every value plotted comes from files under ``results/``: the whole-chat control (R-164, R-165),
the outside-writer sets (R-146, R-157), the sealed final run (R-162, R-163) and the training-memory
comparison (R-029, R-032). The model shown is the shipped one, 6.37 (``fix17cs37``).
"""

from __future__ import annotations

import json

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

from aya_retrieval.provenance import REPO_ROOT  # noqa: E402
from aya_retrieval.report_data import RECALL_KINDS, eval_rows, train_report, weights_gib  # noqa: E402

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


def dumbbell(ax, labels, base_vals, tuned_vals, seed_vals=None, xmax=100) -> None:
    """Rows top to bottom; a hairline from base to adapter, value labels at both ends."""
    ys = list(range(len(labels)))[::-1]
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
        tokens += [r["whole_chat_tokens"] for r in eval_rows(f"{prefix}_base", 0)]
        labels += [f"Set {n}: last 3 exchanges, search", f"Set {n}: whole chat"]
        base += [
            right(eval_rows(f"{prefix}_base", 0), "older"),
            right(eval_rows(f"wc_{prefix}_base", 0, "whole_chat"), "older"),
        ]
        tuned += [
            right(eval_rows(f"{prefix}_{SHIP}", 0), "older"),
            right(eval_rows(f"wc_{prefix}_{SHIP}", 0, "whole_chat"), "older"),
        ]
    fig, ax = plt.subplots(figsize=(8, 3.9))
    fig.subplots_adjust(left=0.33, right=0.97, top=0.75, bottom=0.14)
    dumbbell(ax, labels, base, tuned)
    ax.set_xlabel("Questions about facts told earlier answered right")
    legend(ax, "Tiny Aya, untrained", "6.37, seed 82")
    titled(
        fig,
        "When the chat fits, the whole chat wins",
        f"Outside-writer sets, about {round(sum(tokens) / len(tokens), -2):,.0f} tokens a chat "
        "(R-164). Whole chat: no measured difference.",
    )
    save(fig, "whole_chat_or_search")


def fig_recall_out_of_view() -> None:
    """Recall with the last three exchanges in view: outside-writer sets and the sealed run."""
    labels, base, pooled, seeds = [], [], [], []
    for n in SETS:
        blind = load(SET_FILES[n])
        per = blind["recall_per_seed"]
        items = blind["primary"]["items"]
        labels.append(f"Outside-writer set {n}")
        base.append(100 * blind["primary"]["base"] / items)
        pooled.append(100 * sum(per[str(s)] for s in SEEDS) / (items * len(SEEDS)))
        seeds.append([100 * per[str(s)] / items for s in SEEDS])
    for c, name in CONDITIONS.items():
        d = load(ANALYSIS / "R-162" / f"{c}.json")
        kinds = d["per_kind_correct"]
        items = d["shipped_seed_82"]["questions"]
        per = {a: sum(kinds[k][a] for k in RECALL_KINDS) for a in ("base", *ADAPTERS)}
        labels.append(f"Sealed {c}: {name}")
        base.append(100 * per["base"] / items)
        pooled.append(100 * sum(per[a] for a in ADAPTERS) / (items * len(ADAPTERS)))
        seeds.append([100 * per[a] / items for a in ADAPTERS])
    fig, ax = plt.subplots(figsize=(8, 4.6))
    fig.subplots_adjust(left=0.33, right=0.97, top=0.78, bottom=0.12)
    dumbbell(ax, labels, base, pooled, seeds)
    ax.set_xlabel("Recall (older and confirm questions), last 3 exchanges in view")
    legend(ax, "Tiny Aya, untrained", "6.37, eight seeds pooled")
    titled(
        fig,
        "Recall out of view, untrained and trained",
        "Small dots: each training seed. Outside-writer sets R-146, R-157; "
        "sealed run R-163, both pools generator-built.",
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
        "Longest rows of an early development run (R-029), not 6.37. Same values bit for bit.",
    )
    save(fig, "training_memory")


if __name__ == "__main__":
    fig_whole_chat_or_search()
    fig_recall_out_of_view()
    fig_memory()
