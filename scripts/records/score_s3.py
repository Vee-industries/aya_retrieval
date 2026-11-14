"""R-281: S3 scored by R-178's ship rule as changed by R-191.

Three steps, run in this order after ``qs3.sh`` and ``draw_s3_sample.py --final``:

- ``sheet --final``: the coherence sheet. The sampled rows of base with the tool and of the pick's
  shipped seed, shuffled together by ``heldout3.SHUFFLE_SEED`` with no model names; each line shows
  the in-view turns, the newest message and the reply. Writes ``results/s3/coherence/sheet.txt``,
  ``rubric.txt`` and ``key.json``.
- ``tally``: reads ``judge_1/marks.json`` to ``judge_3/marks.json`` beside the sheet; judge 1
  decides (R-154). Writes ``coherence/tally.json``.
- ``rule``: every measure for every arm (raw counts and rates), the chat-resampled bounds, and the
  pass rule. Writes ``results/s3/ship_rule.json`` and prints counts only, never item text.

Usage:
    python scripts/records/score_s3.py sheet --final
    python scripts/records/score_s3.py tally
    python scripts/records/score_s3.py rule
"""

from __future__ import annotations

import argparse
import json
import random
from collections.abc import Callable
from pathlib import Path

from aya_retrieval.coherence import RUBRIC
from aya_retrieval.conversations import CONFIRM, IN_VIEW, NEVER_TOLD, OLDER, STATEMENT
from aya_retrieval.heldout3 import (
    CHATS_DIR,
    SHUFFLE_SEED,
    SPLIT_FILE,
    WRONG_VIEW,
    load_s3,
    load_split,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
S3_DIR = REPO_ROOT / "results" / "s3"
COH_DIR = S3_DIR / "coherence"
SEEDS = (82, 83, 94)
BASE = "s3_base_tool"
OLD = "fix17cs37"  # 6.37, the shipped model
PICK = "k13opc1_r263"  # C1, the pick (R-279)
SHIPPED_SEED = 82  # R-178: seed 82 is the shipped seed
REPORT = ("k1_r178", "k1_3_r200", "k2_1_r187")  # report arms at 82 and 83 (qs3.sh)
N_RESAMPLES, BOOT_SEED = 10_000, 0  # stats.bootstrap_gain_interval's defaults (R-281)
POINTS = 0.05  # R-191 (a): no more than 5 points below base
GAP = 0.10  # R-178 (b), (c): at least 10 points lower than 6.37
COHERENCE_SHARE = 0.95  # R-281: "base's minus 5%" read as base's rate times 0.95

Measure = Callable[[dict], "bool | None"]


def _kind(*kinds: str) -> Measure:
    return lambda r: bool(r["item_correct"]) if r["kind"] in kinds else None


MEASURES: dict[str, Measure] = {
    "recall": _kind(OLDER, CONFIRM),
    "in_view": _kind(IN_VIEW),
    "statement": _kind(STATEMENT),
    "never_told_plain": lambda r: (
        bool(r["item_correct"]) if r["kind"] == NEVER_TOLD and r["variant"] == "plain" else None
    ),
    "copy": lambda r: (
        bool(r["copy"]) if r["view"] == WRONG_VIEW and r["copy"] is not None else None
    ),
    "n_hit_false_answer": lambda r: (
        bool(r["false_answer"])
        if r["kind"] == NEVER_TOLD and r["n_hit"] and r["false_answer"] is not None
        else None
    ),
}


def load(label: str, folder: Path = S3_DIR) -> list[dict]:
    """Return the rows of one S3 run."""
    return json.loads((folder / f"{label}.json").read_text(encoding="utf-8"))["rows"]


def by_chat(rows: list[dict], measure: Measure) -> dict[str, list[int]]:
    """Return chat id -> [hits, rows counted] for ``measure``."""
    table: dict[str, list[int]] = {}
    for row in rows:
        hit = measure(row)
        if hit is not None:
            cell = table.setdefault(row["chat"], [0, 0])
            cell[0] += hit
            cell[1] += 1
    return table


def rate(table: dict[str, list[int]], chats=None) -> float:
    """Return pooled hits over rows for the chats given (all chats if None)."""
    cells = [table.get(c, [0, 0]) for c in (table if chats is None else chats)]
    n = sum(c[1] for c in cells)
    return sum(c[0] for c in cells) / n if n else float("nan")


def lower_bound(
    a: dict[str, list[int]],
    b: dict[str, list[int]],
    chats: list[str],
    n_resamples: int = N_RESAMPLES,
    seed: int = BOOT_SEED,
) -> float:
    """Return the 2.5th percentile of rate(a) minus rate(b) over chats drawn with replacement."""
    rng = random.Random(seed)
    diffs = []
    for _ in range(n_resamples):
        drawn = [rng.choice(chats) for _ in chats]
        diffs.append(rate(a, drawn) - rate(b, drawn))
    diffs = sorted(d for d in diffs if d == d)  # a draw with no counted row gives nan
    return diffs[int(0.025 * len(diffs))] if diffs else float("nan")


def arms(folder: Path = S3_DIR) -> dict[str, list[dict]]:
    """Return every arm's rows, seeds pooled, under the names the rule uses."""
    out = {
        "always_search": load("s3_always_search", folder),
        "whole_chat": load("s3_whole_chat", folder),
        "base_tool": load(BASE, folder),
        "6.37": [r for s in SEEDS for r in load(f"s3_{OLD}_{s}", folder)],
        "pick": [r for s in SEEDS for r in load(f"s3_{PICK}_{s}", folder)],
    }
    for name in REPORT:
        out[name] = [r for s in (82, 83) for r in load(f"s3_{name}_{s}", folder)]
    return out


def rule(folder: Path = S3_DIR, coherence: dict | None = None) -> dict:
    """Return every arm's measures and the ship rule's lines, each PASS or FAIL."""
    rows = arms(folder)
    chats = sorted({r["chat"] for r in rows["base_tool"]})
    tables = {name: {m: by_chat(rs, f) for m, f in MEASURES.items()} for name, rs in rows.items()}
    report = {
        name: {
            m: {"hits": sum(c[0] for c in t.values()), "n": sum(c[1] for c in t.values())}
            | {"rate": rate(t)}
            for m, t in measures.items()
        }
        for name, measures in tables.items()
    }
    p, base, old = tables["pick"], tables["base_tool"], tables["6.37"]
    lines = []

    def line(text: str, ok: bool) -> None:
        lines.append({"line": text, "pass": bool(ok)})

    bound = lower_bound(p["recall"], base["recall"], chats)
    line(
        f"(a) recall {rate(p['recall']):.3f} above base's {rate(base['recall']):.3f}, "
        f"bound {bound:.3f} above 0",
        rate(p["recall"]) > rate(base["recall"]) and bound > 0,
    )
    for m in ("in_view", "statement", "never_told_plain"):
        line(
            f"(a) {m} {rate(p[m]):.3f} at least base's {rate(base[m]):.3f} minus 0.05",
            rate(p[m]) >= rate(base[m]) - POINTS,
        )
    if coherence is None:
        lines.append({"line": "(a) coherence: no tally yet", "pass": False})
    else:
        pick_c, base_c = coherence["judge_1"]["pick_rate"], coherence["judge_1"]["base_rate"]
        line(
            f"(a) coherence (judge 1) {pick_c:.3f} at least base's {base_c:.3f} times 0.95",
            pick_c >= base_c * COHERENCE_SHARE,
        )
    bound = lower_bound(old["copy"], p["copy"], chats)
    line(
        f"(b) copy {rate(p['copy']):.3f} at most half of 6.37's {rate(old['copy']):.3f}, "
        f"at least 0.10 lower, bound {bound:.3f} above 0",
        rate(p["copy"]) <= rate(old["copy"]) / 2
        and rate(old["copy"]) - rate(p["copy"]) >= GAP
        and bound > 0,
    )
    m = "n_hit_false_answer"
    bound = lower_bound(old[m], p[m], chats)
    line(
        f"(c) N-hit false answers {rate(p[m]):.3f} at least 0.10 below 6.37's {rate(old[m]):.3f}, "
        f"bound {bound:.3f} above 0, not above base's {rate(base[m]):.3f}",
        rate(old[m]) - rate(p[m]) >= GAP and bound > 0 and rate(p[m]) <= rate(base[m]),
    )
    return {
        "record": "R-281",
        "chats": len(chats),
        "arms": report,
        "lines": lines,
        "pass": all(x["pass"] for x in lines),
    }


def sheet(sample_ids: list[str], folder: Path = S3_DIR) -> tuple[list[str], list[dict]]:
    """Return the coherence sheet's text lines and its key, from the sealed set's in-view turns."""
    items, _, _, _ = load_s3(CHATS_DIR, load_split(SPLIT_FILE))
    view = {s3.item.item_id: s3.item.view() for s3 in items}
    wanted = set(sample_ids)
    entries = [("base", r) for r in load(BASE, folder) if r["id"] in wanted]
    entries += [("pick", r) for r in load(f"s3_{PICK}_{SHIPPED_SEED}", folder) if r["id"] in wanted]
    random.Random(SHUFFLE_SEED).shuffle(entries)
    text, key = [], []
    for n, (model, row) in enumerate(entries):
        text.append(f"LINE {n}")
        for user, assistant in view[row["id"]]:
            text += [f"  FRIEND: {user}", f"  YOU: {assistant}"]
        text += [f"  NEWEST MESSAGE: {row['message']}", f"  REPLY: {row['reply']}", ""]
        key.append({"line": n, "model": model, "id": row["id"], "kind": row["kind"]})
    return text, key


def tally(key: list[dict], marks: dict[str, dict[str, int]]) -> dict:
    """Return each judge's coherent share per model; judge 1 decides (R-154)."""
    out = {}
    for judge, judged in marks.items():
        if set(judged) != {str(k["line"]) for k in key}:
            raise SystemExit(f"{judge}: marks cover {len(judged)} of {len(key)} lines")
        counts = {"base": [0, 0], "pick": [0, 0]}
        for k in key:
            counts[k["model"]][0] += int(judged[str(k["line"])])
            counts[k["model"]][1] += 1
        out[judge] = {
            "base_coherent": counts["base"][0],
            "pick_coherent": counts["pick"][0],
            "pairs": counts["base"][1],
            "base_rate": counts["base"][0] / counts["base"][1],
            "pick_rate": counts["pick"][0] / counts["pick"][1],
        }
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("step", choices=("sheet", "tally", "rule"))
    parser.add_argument("--final", action="store_true", help="needed by sheet: S3 is sealed")
    args = parser.parse_args()
    if args.step == "sheet":
        if not args.final:
            parser.error("S3 is sealed: the sheet needs --final")
        ids = json.loads((S3_DIR / "coherence_sample.json").read_text(encoding="utf-8"))["ids"]
        text, key = sheet(ids)
        COH_DIR.mkdir(parents=True, exist_ok=True)
        (COH_DIR / "sheet.txt").write_text("\n".join(text) + "\n", encoding="utf-8")
        (COH_DIR / "rubric.txt").write_text(RUBRIC, encoding="utf-8")
        (COH_DIR / "key.json").write_text(json.dumps(key, indent=1) + "\n", encoding="utf-8")
        print(f"sheet: {len(key)} lines from {len(ids)} sampled ids")
    elif args.step == "tally":
        key = json.loads((COH_DIR / "key.json").read_text(encoding="utf-8"))
        marks = {
            f"judge_{j}": json.loads(
                (COH_DIR / f"judge_{j}" / "marks.json").read_text(encoding="utf-8")
            )
            for j in (1, 2, 3)
        }
        report = tally(key, marks)
        (COH_DIR / "tally.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
        for judge, r in report.items():
            print(f"{judge}: base {r['base_coherent']}, pick {r['pick_coherent']} of {r['pairs']}")
    else:
        tally_path = COH_DIR / "tally.json"
        coherence = json.loads(tally_path.read_text("utf-8")) if tally_path.exists() else None
        report = rule(coherence=coherence)
        (S3_DIR / "ship_rule.json").write_text(
            json.dumps(report, indent=1) + "\n", encoding="utf-8"
        )
        for x in report["lines"]:
            print("PASS" if x["pass"] else "FAIL", x["line"])
        print("== ship rule:", "PASS" if report["pass"] else "FAIL", f"({report['chats']} chats)")


if __name__ == "__main__":
    main()
