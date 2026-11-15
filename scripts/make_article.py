"""Fill the article and model card templates from committed results files, and write both.

Usage:
    python scripts/make_article.py

Every ``{{name}}`` in ``docs/article_template.md``, ``docs/model_card_template.md`` and
``docs/submission/hf_article_template.md`` (the short write-up) is computed
here from files under ``results/`` (and, for the model's context limits, the pinned model's own
config in the local cache), so no result number in either is typed by hand. A placeholder left
unfilled stops the script, and so does any check below that finds two results files disagreeing
or a result that no longer matches what the text says about it.

The numbers are final for the shipped model, 6.37 (``fix17cs37`` seed 82, frozen in R-160): the
sealed run (R-162, R-163), the outside-writer sets (R-146, R-157, R-164), the whole-chat control
(R-164, R-165), R-016's two references run late (R-168, R-169) and the LongMemEval-S outside
check (R-170, from its committed aggregates only). The reopened work is read from R-279's screening
output, the demo judges' tallies and the sealed S3 test (R-287, through ``score_s3.py``'s own
functions).
"""

from __future__ import annotations

import json
import random
import re
import statistics
from collections import Counter

from aya_retrieval.harness import MAX_CALLS
from aya_retrieval.provenance import REPO_ROOT
from aya_retrieval.recall_tool import CHUNK_SIZE, TOP_K
from aya_retrieval.report_data import (
    COHERENCE_DIR,
    EVAL_DIR,
    KINDS,
    RECALL_KINDS,
    SIZES,
    eval_rows,
    pooled,
    recall,
    records_script,
    train_report,
)
from aya_retrieval.stats import exact_sign_test, wilson_interval

DOCS = REPO_ROOT / "docs"
RESULTS = REPO_ROOT / "results"
ANALYSIS = RESULTS / "analysis"
TEMPLATES = {
    DOCS / "article_template.md": DOCS / "ARTICLE.md",
    DOCS / "model_card_template.md": DOCS / "MODEL_CARD.md",
    DOCS / "submission" / "hf_article_template.md": DOCS / "submission" / "HF_ARTICLE.md",
    DOCS / "submission" / "abstract_template.md": DOCS / "submission" / "ABSTRACT.md",
    DOCS / "model_card_c1_template.md": DOCS / "MODEL_CARD_C1.md",
}
ABSTRACT_WORDS = 500  # the form's limit (R-171)
SHIP = "fix17cs37_82"
SEEDS = (82, 83, 94, 95, 96, 97, 98, 99)
ADAPTERS = tuple(f"fix17cs37_{s}" for s in SEEDS)
CONDITIONS = {  # condition: (pool, decoys a chat)
    "A": ("heldout", 1),
    "B": ("heldout", 4),
    "C": ("independent", 1),
    "D": ("independent", 4),
}
SETS = {1: "blind", 2: "blind2"}  # outside-writer set: label prefix of its runs (R-142, R-152)
SET_FILES = {1: ANALYSIS / "R-146" / "blind.json", 2: ANALYSIS / "R-157" / "blind2.json"}
KIND_NAMES = {
    "older": "`older`",
    "confirm": "`confirm`",
    "in_view": "`in_view`",
    "never_told": "`never_told`",
    "statement": "`statement`",
}


WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight"}


def load(path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def p_text(p: float) -> str:
    """An exact p-value in plain notation: two significant figures, or a power of ten."""
    if p >= 0.995:
        return "1.0"
    if p >= 0.001:
        return f"{p:.2g}"
    mantissa, exponent = f"{p:.1e}".split("e")
    return f"{mantissa} × 10<sup>{int(exponent)}</sup>"


def span(values) -> str:
    """'a to b' for the smallest and largest of values, or 'a' when they are equal."""
    values = list(values)
    low, high = min(values), max(values)
    return f"{low}" if low == high else f"{low} to {high}"


def points(interval) -> str:
    """A rate difference's 95% interval in percentage points."""
    _, low, high = interval
    return f"{100 * low:+.1f} to {100 * high:+.1f}"


def counts_by_kind(rows: list[dict]) -> dict[str, tuple[int, int]]:
    out = {}
    for kind in KINDS:
        asked = [r for r in rows if r["kind"] == kind]
        if asked:
            out[kind] = (sum(bool(r["correct"]) for r in asked), len(asked))
    return out


def paired(first: list[dict], second: list[dict], *kinds: str) -> tuple[int, int, float]:
    """Only-first-right and only-second-right counts on the same questions, and the sign test."""
    a = {r["id"]: bool(r["correct"]) for r in first if r["kind"] in kinds}
    b = {r["id"]: bool(r["correct"]) for r in second if r["kind"] in kinds}
    if set(a) != set(b):
        raise SystemExit(f"{', '.join(kinds)}: the two runs do not hold the same questions")
    only_a = sum(a[i] and not b[i] for i in a)
    only_b = sum(b[i] and not a[i] for i in a)
    return only_a, only_b, exact_sign_test(only_a, only_b)


def table(header: list[str], rows: list[str]) -> str:
    return "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n" + "\n".join(rows)


# --- Status and the model -----------------------------------------------------------------------


def status_numbers(out) -> None:
    out["status_line"] = (
        "6.37 (`fix17cs37` seed 82) is the shipped model. The reopened work's pick, C1, ran on "
        "the sealed S3 test and failed one clause of the ship rule registered before S3 opened "
        "(R-287), so 6.37 stays shipped. Every table and result number is computed from committed "
        "results files by `scripts/make_article.py`, except the items typed from the record that "
        "the long paper's section 15 lists; `RECORDS.md` holds the dated record behind each."
    )


def model_numbers(out) -> None:
    """The pinned model's context limits, read from its own config in the local cache."""
    from huggingface_hub import hf_hub_download

    from aya_retrieval.models import MODEL_ID, MODEL_REVISION

    path = hf_hub_download(MODEL_ID, "config.json", revision=MODEL_REVISION, local_files_only=True)
    config = load(path)
    layers = config["layer_types"]
    out["model_max_tokens"] = f"{config['max_position_embeddings']:,}"
    out["model_window"] = f"{config['sliding_window']:,}"
    out["model_layers"] = str(len(layers))
    out["model_vocab"] = f"{config['vocab_size']:,}"
    out["model_full_layers"] = str(layers.count("full_attention"))
    out["model_revision"] = MODEL_REVISION
    out["top_k"] = str(TOP_K)
    out["chunk_size"] = str(CHUNK_SIZE)
    out["max_calls"] = str(MAX_CALLS)


# --- Whole chat or search (R-164, R-165) --------------------------------------------------------


def whole_chat_numbers(out) -> None:
    numbers = load(ANALYSIS / "R-164" / "writeup_numbers.json")
    control = numbers["whole_chat_control"]
    writers = numbers["outside_writer_sets"]
    older_rows, kind_rows, search_lines, tokens = [], [], [], []
    smallest = []
    for n, prefix in SETS.items():
        wc_base = eval_rows(f"wc_{prefix}_base", 0, "whole_chat")
        wc_ship = eval_rows(f"wc_{prefix}_{SHIP}", 0, "whole_chat")
        wct = eval_rows(f"wct_{prefix}_{SHIP}", 0, "whole_chat_tool")
        wca = eval_rows(f"wca_{prefix}_base", 0, "whole_chat_all")
        tool_base = eval_rows(f"{prefix}_base", 0)
        tool_ship = eval_rows(f"{prefix}_{SHIP}", 0)
        summary = control[f"set_{n}"]["all"]
        # R-164's summary and the raw runs must agree before either is quoted.
        older = counts_by_kind(wc_base)["older"]
        if older != (summary["whole_chat_base"], summary["questions"]):
            raise SystemExit(f"set {n}: R-164's whole-chat count differs from its raw run")
        replies = {r["id"]: r["reply"] for r in wc_base}
        if any(replies[r["id"]] != r["reply"] for r in wca if r["kind"] == "older"):
            raise SystemExit(f"set {n}: whole_chat_all's older replies differ from whole_chat's")
        out["older_n"] = str(summary["questions"])
        out[f"wc_base_older_{n}"] = str(summary["whole_chat_base"])
        out[f"tool_base_older_{n}"] = str(summary["tool_base"])
        out[f"tool82_older_{n}"] = str(summary["tool_seed_82"])
        wc82 = counts_by_kind(wc_ship)["older"][0]
        wct82 = counts_by_kind(wct)["older"][0]
        out[f"wc82_older_{n}"] = str(wc82)
        out[f"wct82_older_{n}"] = str(wct82)
        vs = summary["whole_chat_vs_seed_82"]
        out[f"wc_vs_tool_{n}"] = (
            f"{vs['only_first']} right only for base with the whole chat and {vs['only_second']} "
            f"only for 6.37 with the tool, p = {p_text(vs['p'])}"
        )
        a = paired(wc_base, wc_ship, "older")
        b = paired(wca, wct, "older")
        older_rows.append(
            f"| Set {n} | {summary['tool_base']} | {summary['tool_seed_82']} "
            f"| {summary['whole_chat_base']} | {wc82} ({a[0]}, {a[1]}, p = {p_text(a[2])}) "
            f"| {wct82} ({b[0]}, {b[1]}, p = {p_text(b[2])}) |"
        )
        base_k, ship_k = counts_by_kind(wca), counts_by_kind(wct)
        models = writers[f"set_{n}"]["models"]
        for kind in KINDS:
            o_b, o_s, p = paired(wca, wct, kind)
            smallest.append(p)
            note = " (no tool, so right by construction)" if kind == "statement" else ""
            kind_rows.append(
                f"| {n} | {KIND_NAMES[kind]} ({base_k[kind][1]}) | {base_k[kind][0]}{note} "
                f"| {ship_k[kind][0]} | {o_b}, {o_s}, p = {p_text(p)} "
                f"| {models['seed_82']['kinds'][kind]} | {models['base']['kinds'][kind]} |"
            )
            if p < 0.05:
                raise SystemExit(f"set {n} {kind}: a gap near significance; the text says none")
        out[f"wct_statement_{n}"] = f"{ship_k['statement'][0]} of {ship_k['statement'][1]}"
        out[f"wct_statement_searched_{n}"] = str(
            sum(bool(r["queries"]) for r in wct if r["kind"] == "statement")
        )
        out[f"wct_never_told_{n}"] = str(ship_k["never_told"][0])
        out[f"wca_never_told_{n}"] = str(base_k["never_told"][0])
        out[f"wct_confirm_{n}"] = str(ship_k["confirm"][0])
        out[f"wca_confirm_{n}"] = str(base_k["confirm"][0])
        out[f"tool82_never_told_{n}"] = str(models["seed_82"]["kinds"]["never_told"])
        out[f"tool82_confirm_{n}"] = str(models["seed_82"]["kinds"]["confirm"])
        searched = {
            k: (sum(bool(r["queries"]) for r in wct if r["kind"] == k), ship_k[k][1])
            for k in ("older", "confirm", "never_told")
        }
        searched_tool = {
            k: sum(bool(r["queries"]) for r in tool_ship if r["kind"] == k)
            for k in ("older", "confirm", "never_told")
        }
        search_lines.append(
            f"set {n}, `older` {searched['older'][0]} of {searched['older'][1]} (with the last "
            f"three exchanges: {searched_tool['older']}), `confirm` {searched['confirm'][0]} of "
            f"{searched['confirm'][1]} ({searched_tool['confirm']}), `never_told` "
            f"{searched['never_told'][0]} of {searched['never_told'][1]} "
            f"({searched_tool['never_told']})"
        )
        read = summary["tokens_read_per_turn"]
        wct_read = statistics.mean(r["tokens_read"] for r in wct)
        tokens.append(
            f"set {n}, base with the whole chat {read['whole_chat_base']:,}, 6.37 with the last "
            f"three exchanges and the tool {read['tool_seed_82']:,}, 6.37 with the whole chat and "
            f"the tool {wct_read:,.0f}"
        )
        chat_tokens = [r["whole_chat_tokens"] for r in tool_base]
        out[f"ow_tokens_mean_{n}"] = f"{statistics.mean(chat_tokens):,.0f}"
        out[f"ow_tokens_max_{n}"] = f"{max(chat_tokens):,}"
    out["wc_min_p"] = p_text(min(smallest))
    both = [
        r["whole_chat_tokens"] for prefix in SETS.values() for r in eval_rows(f"{prefix}_base", 0)
    ]
    out["ow_tokens_mean"] = f"{statistics.mean(both):,.0f}"
    out["wc_older_table"] = table(
        [
            "Set",
            "Base, last three exchanges and the tool",
            "6.37, last three exchanges and the tool",
            "Base, whole chat",
            "6.37, whole chat (only base right, only 6.37 right, sign test)",
            "6.37, whole chat and the tool (the same, against base with the whole chat)",
        ],
        older_rows,
    )
    out["wc_kind_table"] = table(
        [
            "Set",
            "Kind (questions)",
            "Base, whole chat",
            "6.37, whole chat and the tool",
            "Only base right, only 6.37 right, sign test",
            "6.37, last three exchanges and the tool",
            "Base, last three exchanges and the tool",
        ],
        kind_rows,
    )
    out["wc_searches"] = "; ".join(search_lines)
    out["wc_tokens"] = "; ".join(tokens)
    peaks = [
        load(EVAL_DIR / f"{pre}_{prefix}_{SHIP}_seed_0.json")["peak_vram_gib"]
        for prefix in SETS.values()
        for pre in ("wc", "wct")
    ]
    out["wc_ship_peak"] = f"{min(peaks):.2f} to {max(peaks):.2f}"
    if not all(control[k]["status"].startswith("not run") for k in ("hard_dev", "probe")):
        raise SystemExit("R-164's generated-pool whole-chat runs now exist; update the text")
    # The generated 419-message chats, in tokens, from the runs that hold them.
    hd = [r for r in eval_rows(f"hd_{SHIP}", 73157) if r["size"] == 419]
    probe = [r for r in eval_rows(f"probe_{SHIP}", 73157) if r["size"] == 419]
    out["hd_419_tokens"] = f"{statistics.mean(r['whole_chat_tokens'] for r in hd):,.0f}"
    out["probe_419_tokens"] = f"{statistics.mean(r['whole_chat_tokens'] for r in probe):,.0f}"
    # R-014 and R-017: whole-chat base runs before any memory cap.
    r017 = eval_rows("base", 45356, "whole_chat")
    for size in SIZES:
        asked = [r for r in r017 if r["size"] == size and r["kind"] == "older"]
        out[f"r017_wc_{size}"] = f"{sum(bool(r['correct']) for r in asked)} of {len(asked)}"
    out["r017_peak"] = f"{load(EVAL_DIR / 'base_seed_45356.json')['peak_vram_gib']:.2f}"
    out["r014_peak"] = (
        f"{load(RESULTS / 'recall_first_test' / 'seed_18680.json')['peak_vram_gib']:.2f}"
    )


OOM_LOG = RESULTS / "control" / "R-164" / "wc_hd_base_oom.log"
OOM = re.compile(
    r"Tried to allocate (?P<more>[\d.]+) GiB\..*?(?P<allowed>[\d.]+) GiB allowed; "
    r"Of the allocated memory (?P<allocated>[\d.]+) GiB is allocated"
)


def oom_numbers(out) -> None:
    """The whole-chat runs on the generated pools that ran out of card memory (R-166)."""
    failures: dict[str, list[dict]] = {}
    started: Counter = Counter()
    label = None
    for line in OOM_LOG.read_text(encoding="utf-8").splitlines():
        start = re.match(r"== whole chat (\S+) try", line)
        if start:
            label = start.group(1)
            started[label] += 1
        found = OOM.search(line)
        if found and label:
            failures.setdefault(label, []).append(
                {k: float(v) for k, v in found.groupdict().items()}
            )
    for name, short in (("wc_hd_base", "hd"), ("wc_probe_base", "probe")):
        tries = failures[name]
        if len({(t["more"], t["allocated"]) for t in tries}) != 1:
            raise SystemExit(f"{name}: its out-of-memory tries differ; update the text")
        out[f"oom_{short}_tries"] = {1: "one", 2: "two", 3: "three"}[len(tries)]
        out[f"oom_{short}_more"] = f"{tries[0]['more']:.2f}"
        out[f"oom_{short}_allocated"] = f"{tries[0]['allocated']:.2f}"
    out["oom_probe_started"] = WORDS[started["wc_probe_base"]]
    allowed = {t["allowed"] for tries in failures.values() for t in tries}
    if len(allowed) != 1:
        raise SystemExit("the out-of-memory log shows more than one cap")
    out["oom_allowed"] = f"{allowed.pop():.2f}"
    peaks = [cost["peak_vram_gib"] for d in sealed().values() for cost in d["cost"].values()]
    out["sealed_peak_range"] = f"{min(peaks):.2f} to {max(peaks):.2f}"


# --- References and checks the reviewer asked for (R-014, R-017, R-142, R-144, R-167) ----------

TAG_NEG = r"(isn'?t|wasn'?t|didn'?t|doesn'?t|don'?t|aren'?t|weren'?t|hasn'?t|haven'?t|won'?t)"
TAG_ANYWHERE = re.compile(
    r"\b(right|yeah|correct)\s*\?|[,\s](right|yeah|correct)\s*[.!]*\s*$|\b"
    + TAG_NEG
    + r"\s+(it|he|she|they|i|that|we)\b\s*[?.!]*(\s|$)"
)
TAG_AT_END = re.compile(
    r"([,\s](right|yeah|correct)|\b" + TAG_NEG + r"\s+(it|he|she|they|i|that|we))\s*[?.!]*\s*$"
)


def reference_numbers(out) -> None:
    # R-014: base, whole chat and code that always searches, on the training pool (first test).
    first = load(RESULTS / "recall_first_test" / "seed_18680.json")["rows"]
    for arm in ("whole_chat", "always_search"):
        for size in SIZES:
            rows = [r for r in first if r["arm"] == arm and r["size"] == size]
            out[f"r014_{arm}_{size}"] = f"{sum(bool(r['correct']) for r in rows)} of {len(rows)}"
    # R-017: what always searching does to facts in view and plain chat.
    for arm in ("always_search", "three_exchanges"):
        rows = eval_rows("base", 45356, arm)
        for kind in ("in_view", "statement"):
            asked = [r for r in rows if r["kind"] == kind]
            out[f"r017_{arm}_{kind}"] = f"{sum(bool(r['correct']) for r in asked)} of {len(asked)}"
    # R-142: the noise of a kind with about 40 questions: the 95% half-width of the difference
    # between two arms' rates near 50% (variance 0.25 / n each).
    n = load(SET_FILES[1])["per_kind_correct"]["confirm"]["items"]
    out["kind_noise_diff"] = f"{100 * 1.96 * (2 * 0.25 / n) ** 0.5:.0f}"
    out["kind_noise_n"] = str(n)
    # Tag questions among each outside-writer set's `confirm` messages.
    for n_set, prefix in SETS.items():
        rows = [r for r in eval_rows(f"{prefix}_base", 0) if r["kind"] == "confirm"]
        anywhere = sum(bool(TAG_ANYWHERE.search(r["message"].lower())) for r in rows)
        at_end = sum(bool(TAG_AT_END.search(r["message"].lower())) for r in rows)
        out[f"tags_{n_set}"] = f"{anywhere} of {len(rows)}"
        out[f"tags_end_{n_set}"] = str(at_end)
    # Seed 82's place among the eight: lowest on set 1, sealed C and D, and hard_dev.
    runs = {c: load(ANALYSIS / "R-162" / f"{c}.json") for c in CONDITIONS}
    for c in ("C", "D"):
        per = recall_per_seed(runs[c])
        if per[SHIP] != min(per[a] for a in ADAPTERS):
            raise SystemExit(f"seed 82 is not the lowest in {c}; update the text")
    blind = load(SET_FILES[1])["recall_per_seed"]
    rigor = {a["condition"]: a for a in load(ANALYSIS / "R-139" / "dev_rigor.json")["across_seeds"]}
    if blind["82"] != min(blind.values()) or rigor["hd"]["per_seed"]["82"] != rigor["hd"]["min"]:
        raise SystemExit("seed 82 is not the lowest on set 1 or hard_dev; update the text")
    # Every kind where seed 82, or any seed, is below base.
    lines = []
    for n_set, prefix in SETS.items():
        kinds = load(SET_FILES[n_set])["per_kind_correct"]
        for k in KINDS:
            base = kinds[k][f"{prefix}_base"]
            below = [kinds[k][str(s)] for s in SEEDS if kinds[k][str(s)] < base]
            if below:
                lines.append(
                    f"set {n_set} `{k}`: seed 82 {kinds[k]['82']} against base's {base}; "
                    f"{WORDS[len(below)]} of the eight seeds below base ({span(below)})"
                )
    for c in CONDITIONS:
        kinds = runs[c]["per_kind_correct"]
        for k in KINDS:
            below = [kinds[k][a] for a in ADAPTERS if kinds[k][a] < kinds[k]["base"]]
            if below:
                lines.append(
                    f"sealed {c} `{k}`: seed 82 {kinds[k][SHIP]} against base's "
                    f"{kinds[k]['base']}; {WORDS[len(below)]} of the eight seeds below base "
                    f"({span(below)})"
                )
    out["below_base"] = "; ".join(lines)
    # R-144: recall replies scored wrong although they name the answer (a wrong value beside it).
    strict = {}
    for label in ("hd_base", "probe2_base", f"hd_{SHIP}", f"probe_{SHIP}"):
        rows = [r for r in eval_rows(label, 73157) if r["kind"] in RECALL_KINDS]
        strict[label] = (
            sum(
                (not r["correct"]) and r["answer"].casefold() in r["reply"].casefold() for r in rows
            ),
            len(rows),
        )
    if any(strict[k][0] for k in strict if k != "hd_base"):
        raise SystemExit("the strict-scorer case now touches a run other than hd_base")
    out["strict_hd_base"] = "{} of {}".format(*strict["hd_base"])


# --- R-016's two references, run late (R-167, R-168, R-169) ------------------------------------


def seconds_per_question(label: str, seed: int) -> float:
    """A run's wall-clock seconds over its questions (as R-162's cost reports per conversation)."""
    run = load(EVAL_DIR / f"{label}_seed_{seed}.json")
    return run["seconds"] / len(run["rows"])


def sealed_reference_numbers(out) -> None:
    """Base with the whole chat and code that always searches, on the sealed pools (R-168)."""
    refs = load(ANALYSIS / "R-168" / "refs.json")
    runs = sealed()
    tests, tokens = [], []
    # One row a measure, one column a condition, so the table stays narrow and keeps every arm.
    rows: dict[str, list[str]] = {}
    seen = {k: [] for k in ("wc", "as", "ship58", "ship", "as_in_view", "ship_in_view")}
    seen |= {"wc_in_view": [], "tool_in_view": [], "tool": []}
    longest, code_120 = (
        {"ship": [], "code": [], "tool": []},
        [],
    )  # 419-message chats; code over both sizes
    for c in CONDITIONS:
        whole, code = refs[c]["whole_chat"], refs[c]["always_search"]
        # Base with the tool and seed 82 here are R-162's runs, re-read; they must agree.
        kinds = runs[c]["per_kind_correct"]
        for k in KINDS:
            ship = sum(code["sizes"][str(s)]["kinds"][k]["seed_82"] for s in SIZES)
            base = sum(code["sizes"][str(s)]["kinds"][k]["base_tool"] for s in SIZES)
            if (ship, base) != (kinds[k][SHIP], kinds[k]["base"]):
                raise SystemExit(f"R-168 {c} {k}: counts differ from R-162's")
        if set(whole["sizes"]) != {"58"}:
            raise SystemExit("R-168's whole chat now has a 419-message run; update the text")
        wc = whole["sizes"]["58"]["recall"]
        by_size = {s: code["sizes"][str(s)]["recall"] for s in SIZES}
        if wc["base_tool"] != by_size[58]["base_tool"]:
            raise SystemExit(f"R-168 {c}: the two references do not hold the same questions")
        for r in (wc, *by_size.values()):
            t = r["reference_vs_seed_82"]
            if t["p"] >= 0.001 or r["reference"] >= r["seed_82"]:
                raise SystemExit(f"R-168 {c}: seed 82 is not far above a reference")
            tests.append(t)
        if any(
            code["sizes"][str(s)]["kinds"][k]["reference_searched"] < 30
            for s in SIZES
            for k in KINDS
        ):
            raise SystemExit(f"R-168 {c}: code that always searches skipped a search")
        seen["wc"].append(wc["reference"])
        seen["ship58"].append(wc["seed_82"])
        seen["as"] += [r["reference"] for r in by_size.values()]
        seen["ship"] += [r["seed_82"] for r in by_size.values()]
        seen["tool"] += [r["base_tool"] for r in by_size.values()]
        big = by_size[max(SIZES)]
        longest["ship"].append(big["seed_82"])
        longest["code"].append(big["reference"])
        longest["tool"].append(big["base_tool"])
        code_120.append(sum(r["reference"] for r in by_size.values()))
        for s in SIZES:
            view = code["sizes"][str(s)]["kinds"]["in_view"]
            seen["as_in_view"].append(view["reference"])
            seen["ship_in_view"].append(view["seed_82"])
        view = whole["sizes"]["58"]["kinds"]["in_view"]
        seen["wc_in_view"].append(view["reference"])
        seen["tool_in_view"].append(view["base_tool"])
        cells = {"Base, whole chat, no tool, 58 messages": wc["reference"]}
        for s in SIZES:
            cells[f"Code always searches, {s} messages"] = by_size[s]["reference"]
        for s in SIZES:
            cells[f"Base, tool, {s} messages"] = by_size[s]["base_tool"]
        for s in SIZES:
            cells[f"Seed 82, tool, {s} messages"] = by_size[s]["seed_82"]
        for s in SIZES:
            cells[f"Eight adapters, tool, {s} messages"] = span(by_size[s]["adapters"].values())
        cells["False retrievals: base, whole chat (58 messages only)"] = whole["false_retrievals"]
        cells["False retrievals: code always searches (both sizes)"] = code["false_retrievals"]
        for name, value in cells.items():
            rows.setdefault(name, []).append(str(value))
        chat = [
            r["whole_chat_tokens"] for r in eval_rows(f"ref_{c}_base_wca", 90311, "whole_chat_all")
        ]
        tokens.append(statistics.mean(chat))
    out["r168_recall_n"] = str(refs["A"]["whole_chat"]["sizes"]["58"]["recall"]["of"])
    out["r168_table"] = table(
        [f"Recall (of {out['r168_recall_n']} a size), or false retrievals", *CONDITIONS],
        [f"| {name} | " + " | ".join(cells) + " |" for name, cells in rows.items()],
    )
    out["r168_p_max"] = p_text(max(t["p"] for t in tests))
    out["r168_only_ref"] = span(t["only_first"] for t in tests)
    out["r168_only_ship"] = span(t["only_second"] for t in tests)
    for name, values in seen.items():
        out[f"r168_{name}"] = span(values)
    out["r168_wc_tokens"] = f"{min(tokens):,.0f} to {max(tokens):,.0f}"
    for name, values in longest.items():  # by condition, A to D, of r168_recall_n a size
        out[f"long_{name}"] = ", ".join(str(v) for v in values[:-1]) + f" and {values[-1]}"
    out["long_size"] = str(max(SIZES))
    if min(longest["ship"]) <= max(longest["code"]):
        raise SystemExit("seed 82 is no longer above code on every 419-message condition")
    out["r168_code_120"] = span(code_120)
    out["r168_kind_n"] = str(refs["A"]["always_search"]["sizes"]["58"]["kinds"]["in_view"]["of"])
    false = [runs[c]["rule_3_false_retrieval"]["counts"][a] for c in CONDITIONS for a in ADAPTERS]
    out["r168_false_adapters"] = span(false)


def outside_reference_numbers(out) -> None:
    """Code that always searches, on the two outside-writer sets (R-169)."""
    rows_by_set: dict[int, dict[str, str]] = {}
    for n, prefix in SETS.items():
        rows: dict[str, str] = {}
        rows_by_set[n] = rows
        code = eval_rows(f"as_{prefix}_base", 0, "always_search")
        ship = eval_rows(f"{prefix}_{SHIP}", 0)
        base = eval_rows(f"{prefix}_base", 0)
        whole = eval_rows(f"wca_{prefix}_base", 0, "whole_chat_all")
        if not all(r["queries"] for r in code):
            raise SystemExit(f"set {n}: code that always searches skipped a search")
        kinds = load(SET_FILES[n])["per_kind_correct"]
        counted = {name: counts_by_kind(r) for name, r in (("code", code), ("ship", ship))}
        counted |= {"base": counts_by_kind(base), "whole": counts_by_kind(whole)}
        for k in KINDS:
            if (counted["ship"][k][0], counted["base"][k][0]) != (
                kinds[k]["82"],
                kinds[k][f"{prefix}_base"],
            ):
                raise SystemExit(f"set {n} {k}: the runs differ from the set's analysis file")
        right = {name: recall(r)[0] for name, r in (("code", code), ("ship", ship), ("base", base))}
        right["whole"] = recall(whole)[0]
        only_code, only_ship, p = paired(code, ship, *RECALL_KINDS)
        if p < 0.05:
            raise SystemExit(
                f"set {n}: code and seed 82 differ on recall; the text says they do not"
            )
        out[f"as_recall_{n}"] = str(right["code"])
        out[f"as_vs_82_{n}"] = (
            f"{only_code} right only for code and {only_ship} only for seed 82, p = {p_text(p)}"
        )
        out[f"as_p_{n}"] = p_text(p)
        # Base with the tool and base with the whole chat, for the results-at-a-glance table.
        out[f"wc_recall_{n}"] = str(right["whole"])
        for k in ("in_view", "never_told", "statement"):
            out[f"ow_base_{k}_{n}"] = str(counted["base"][k][0])
            out[f"ow_wc_{k}_{n}"] = str(counted["whole"][k][0])
        rows["recall"] = (
            f"{right['code']} | {right['ship']} ({only_code}, {only_ship}, p = {p_text(p)}) "
            f"| {right['base']} | {right['whole']}"
        )
        for k in KINDS:
            o_c, o_s, p_k = paired(code, ship, k)
            out[f"as_{k}_p_{n}"] = p_text(p_k)
            note = {"statement": (" (wrong by construction)", " (right by construction)")}
            code_note, whole_note = note.get(k, ("", ""))
            test = "" if k == "statement" else f" ({o_c}, {o_s}, p = {p_text(p_k)})"
            rows[k] = (
                f"{counted['code'][k][0]}{code_note} | {counted['ship'][k][0]}{test} "
                f"| {counted['base'][k][0]} | {counted['whole'][k][0]}{whole_note}"
            )
        for k in ("in_view", "never_told", "statement"):
            if counted["ship"][k][0] <= counted["code"][k][0]:
                raise SystemExit(f"set {n} {k}: seed 82 is not above code; update the text")
            out[f"as_{k}_{n}"] = str(counted["code"][k][0])
            out[f"ship_{k}_{n}"] = str(counted["ship"][k][0])
        out["as_recall_n"] = str(recall(code)[1])
        out["as_kind_n"] = str(counted["code"]["in_view"][1])
    names = {"recall": f"recall (`older` and `confirm`, {out['as_recall_n']})"}
    names |= {k: f"{KIND_NAMES[k]} ({counts_by_kind(code)[k][1]})" for k in KINDS}
    # One table a set, so each keeps code, seed 82 and base with the whole chat side by side.
    for n, rows in rows_by_set.items():
        out[f"as_ow_table_{n}"] = table(
            [
                f"Set {n}: kind (questions)",
                "Code always searches",
                "Seed 82, tool (only code right, only seed 82 right, sign test)",
                "Base, tool",
                "Base, whole chat",
            ],
            [f"| {names[k]} | {cells} |" for k, cells in rows.items()],
        )


def speed_numbers(out) -> None:
    """Seconds a question for code that always searches against the tool arms (R-168 to R-170)."""
    runs = sealed()
    code = [seconds_per_question(f"ref_{c}_base_as", 90311) for c in CONDITIONS]
    ship = [runs[c]["cost"][SHIP]["seconds_per_conversation"] for c in CONDITIONS]
    base = [runs[c]["cost"]["base"]["seconds_per_conversation"] for c in CONDITIONS]
    ow_code = [seconds_per_question(f"as_{p}_base", 0) for p in SETS.values()]
    ow_ship = [seconds_per_question(f"{p}_{SHIP}", 0) for p in SETS.values()]
    ow_base = [seconds_per_question(f"{p}_base", 0) for p in SETS.values()]
    ow_whole = [seconds_per_question(f"wca_{p}_base", 0) for p in SETS.values()]
    lme = load(ANALYSIS / "R-170" / "scores.json")["measures"]
    if max(code) >= min(ship) or max(ow_code) >= min(ow_ship):
        raise SystemExit("code that always searches is not faster than seed 82; update the text")
    if lme["always_search"]["seconds_per_question"] >= lme["637_tool"]["seconds_per_question"]:
        raise SystemExit("on LongMemEval-S code is not faster than 6.37; update the text")

    def secs(values) -> str:
        return f"{min(values):.2f} to {max(values):.2f}"

    out["speed_sealed"] = (
        f"code that always searches {secs(code)} s a conversation, seed 82 {secs(ship)}, base with "
        f"the tool {secs(base)}"
    )
    out["speed_ow"] = (
        f"code {secs(ow_code)} s a question, seed 82 {secs(ow_ship)}, base with the tool "
        f"{secs(ow_base)}, base with the whole chat and no tool {secs(ow_whole)}"
    )
    out["speed_sealed_short"] = f"{secs(code)} s a conversation against {secs(ship)}"
    out["speed_ow_short"] = f"{secs(ow_code)} s a question against {secs(ow_ship)}"
    out["speed_lme_short"] = (
        f"{lme['always_search']['seconds_per_question']:.2f} s a question against "
        f"{lme['637_tool']['seconds_per_question']:.2f}"
    )


# --- LongMemEval-S, an outside check (R-170) ----------------------------------------------------

LME = ANALYSIS / "R-170"
LME_ARMS = {  # scores.json name: column name
    "637_tool": "6.37 seed 82, tool",
    "base_tool": "base, tool",
    "always_search": "code always searches",
    "three_exchanges": "base, three exchanges, no tool",
}
LME_SEARCH_ARMS = ("637_tool", "base_tool", "always_search")
LME_ARM_WORDS = {
    "637_tool": "6.37 with the tool",
    "base_tool": "base with the tool",
    "always_search": "code that always searches",
    "three_exchanges": "base with three exchanges",
    "evidence_only": "base reading only the evidence",
}


def diff_text(test: dict) -> str:
    """'a against b of n (difference, 95% interval, p)' from score_r170's paired entry."""
    diff, low, high = test["difference_and_95_interval"]
    return (
        f"{test['first']} against {test['second']} of {test['n']} ({100 * diff:+.1f} points, "
        f"95% interval {100 * low:+.1f} to {100 * high:+.1f}, p = {p_text(test['p'])})"
    )


def judged_split(key: dict, judge: str = "j1") -> tuple[dict, dict, dict]:
    """One judge's marks per arm and question, the questions by kind, and every line's verdict."""
    verdicts: dict[int, bool] = {}
    for sheet in sorted({line["sheet"] for line in key["lines"]}):
        marks = load(LME / "judge" / "marks" / f"marks_{sheet}_{judge}.json")
        verdicts |= {int(n): v == "yes" for n, v in marks.items()}
    by_arm: dict[str, dict[str, bool]] = {}
    for line in key["lines"]:
        by_arm.setdefault(line["arm"], {})[line["id"]] = verdicts[line["line"]]
    unanswerable = {line["id"] for line in key["lines"] if line["abstention"]}
    kinds = {
        "answerable": [q for q in key["questions"] if q not in unanswerable],
        "unanswerable": [q for q in key["questions"] if q in unanswerable],
    }
    return by_arm, kinds, verdicts


def longmemeval_numbers(out) -> None:
    scores = load(LME / "scores.json")
    judged = load(LME / "judged.json")
    profile = load(LME / "profile.json")
    m, hyp = scores["measures"], scores["hypotheses"]
    if any(state != "completed" for state in scores["arms"].values()):
        raise SystemExit("an R-170 arm is not completed; the text reports every arm")
    if scores["answer_scorer_self_test"]["failed"]:
        raise SystemExit("R-170's answer scorer failed its self-test")
    evidence_n, read_n = scores["evidence_questions"], scores["answer_read"]["read"]
    abstain_n = scores["abstention_questions"]
    answerable_n = profile["questions"] - abstain_n
    h1, h2, h3 = (
        hyp["H1_first_search_637_vs_base_tool"],
        hyp["H2_637_vs_always_search"],
        hyp["H3_637_vs_base_tool"],
    )
    found = {a: m[a]["evidence"]["first_search_turn"]["hits"] for a in LME_SEARCH_ARMS}
    first = h1["no_search_counts_as_not_found"]["failures_wrong"]
    if (first["first"], first["second"], first["n"]) != (
        found["637_tool"],
        found["base_tool"],
        evidence_n,
    ):
        raise SystemExit("R-170's H1 differs from its evidence counts")
    if h2["first_search_turn"]["failures_wrong"]["second"] != found["always_search"]:
        raise SystemExit("R-170's H2 differs from its evidence counts")
    answer = h2["answer_in_reply"]["failures_wrong"]
    if (answer["first"], answer["second"], answer["n"]) != (
        m["637_tool"]["answer_in_reply"]["hits"],
        m["always_search"]["answer_in_reply"]["hits"],
        read_n,
    ):
        raise SystemExit("R-170's H2 answers differ from its answer counts")
    abstain = h3["abstention"]["failures_wrong"]
    refuse = h3["refusal_on_answerable"]["failures_wrong"]
    if (abstain["n"], refuse["n"]) != (abstain_n, answerable_n):
        raise SystemExit("R-170's H3 counts differ from the profile")
    # The readings the text gives, checked against the numbers.
    if first["difference_and_95_interval"][1] <= 0:
        raise SystemExit("H1 no longer holds; the text says it does")
    both = h1["questions_both_searched"]
    if both["p"] < 0.05:
        raise SystemExit("6.37 and base differ when both searched; the text says they do not")
    if h2["first_search_turn"]["failures_wrong"]["difference_and_95_interval"][2] >= 0:
        raise SystemExit("code is no longer ahead of 6.37 on evidence; the text says it is")
    if not answer["difference_and_95_interval"][1] < 0 < answer["difference_and_95_interval"][2]:
        raise SystemExit("6.37 and code now differ on answers; the text says they do not")
    if abstain["difference_and_95_interval"][1] <= -0.05:
        raise SystemExit("H3 no longer holds; the text says it does")

    out["lme_questions"] = str(profile["questions"])
    types = profile["types"]
    out["lme_core_n"] = str(types["single-session-user"] + types["knowledge-update"])
    out["lme_abstain_n"] = str(abstain_n)
    out["lme_answerable_n"] = str(answerable_n)
    out["lme_evidence_n"] = str(evidence_n)
    out["lme_marked"] = str(profile["marked"])
    out["lme_in_view"] = str(len(profile["evidence_in_view"]))
    out["lme_read_n"] = str(read_n)
    ex, view = profile["exchanges_per_question"], profile["view_tokens"]
    out["lme_exchanges"] = f"{ex['median']:.0f} ({ex['min']} to {ex['max']})"
    out["lme_view"] = f"{view['median']:,.0f}"
    out["lme_view_p99"] = f"{view['p99']:,}"
    out["lme_view_max"] = f"{view['max']:,}"
    chunks = profile["chunks_per_older_exchange"]
    out["lme_chunks"] = f"{chunks['median']:.0f}"
    out["lme_multi_chunk"] = (
        f"{profile['older_exchanges_over_one_chunk']:,} of {profile['older_exchanges']:,}"
    )
    out["lme_joined"] = (
        f"{profile['turns_joined']:,} turns, {profile['turns_joined_across_sessions']:,} of them "
        "across a session boundary"
    )

    cap = next(
        int(found_cap.group(1))
        for k in m["637_tool"]
        if (found_cap := re.fullmatch(r"replies_at_(\d+)_token_cap", k))
    )
    out["lme_cap"] = str(cap)

    def of(share: dict) -> str:
        return f"{share['hits']} of {share['of']}"

    rows = [  # (measure, cell for an arm, whether the three-exchange arm has no tool for it)
        (
            "Searched (of the questions with marked evidence it completed)",
            lambda a: of(m[a]["evidence"]["searched"]),
            True,
        ),
        (
            f"Evidence found by the first search (of {evidence_n}; a failure or no search "
            "counts as not found)",
            lambda a: str(found[a]),
            True,
        ),
        (
            f"Gold answer in the reply (of {read_n} read; a failure counts as wrong)",
            lambda a: str(m[a]["answer_in_reply"]["hits"]),
            False,
        ),
        (
            "False matches (reply scored against another question's gold)",
            lambda a: f"{m[a]['false_match']['matches']} of {m[a]['false_match']['of']}",
            False,
        ),
        (
            f"Declines, {abstain_n} unanswerable (a failed run counts as no decline)",
            lambda a: str(m[a]["abstention"]["hits"]),
            False,
        ),
        (
            f"Declines, {answerable_n} answerable (a failed run counts as no decline)",
            lambda a: str(m[a]["refusal_on_answerable"]["hits"]),
            False,
        ),
        (
            "Clean first calls",
            lambda a: (
                of(m[a]["clean_first_calls"]) + (" (scripted)" if a == "always_search" else "")
            ),
            True,
        ),
        ("Ran out of calls", lambda a: str(m[a]["ran_out_of_calls"]), True),
        (
            f"Words a reply / replies at the {cap}-token cap",
            lambda a: f"{m[a]['reply_words_mean']:.1f} / {of(m[a][f'replies_at_{cap}_token_cap'])}",
            False,
        ),
        (
            "Tokens read / seconds a question",
            lambda a: (
                f"{m[a]['tokens_read_per_question']:,.0f} / {m[a]['seconds_per_question']:.2f}"
            ),
            False,
        ),
        (
            "Failures, before / after the rerun",
            lambda a: f"{m[a]['failures_before_rerun']} / {m[a]['failures']}",
            False,
        ),
    ]
    lines = []
    for name, cell, tool_only in rows:
        cells = ["no tool" if tool_only and a == "three_exchanges" else cell(a) for a in LME_ARMS]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    out["lme_table"] = table(["Measure", *LME_ARMS.values()], lines)

    searched = {a: m[a]["evidence"]["searched"]["rate"] for a in ("637_tool", "base_tool")}
    out["lme_h1"] = diff_text(first)
    out["lme_h1_completed"] = diff_text(
        h1["no_search_counts_as_not_found"]["completed_by_every_arm"]
    )
    out["lme_h1_both"] = (
        f"{both['first']} and {both['second']} of {both['n']}, p = {p_text(both['p'])}"
    )
    out["lme_searched_share"] = (
        f"{100 * searched['637_tool']:.0f}% against {100 * searched['base_tool']:.0f}%"
    )
    out["lme_h2_evidence"] = diff_text(h2["first_search_turn"]["failures_wrong"])
    any_search = h2["any_search_turn"]["failures_wrong"]
    out["lme_h2_any"] = f"{any_search['first']} against {any_search['second']}"
    out["lme_h2_answer"] = diff_text(answer)
    # Registered H2 told from code's side: code first, then 6.37 (R-170).
    h2_evidence = h2["first_search_turn"]["failures_wrong"]
    out["lme_h2_code"] = (
        f"{h2_evidence['second']} against {h2_evidence['first']} of {h2_evidence['n']}"
    )
    out["lme_h2_code_p"] = p_text(h2_evidence["p"])
    out["lme_h2_answer_code"] = (
        f"{answer['second']} against {answer['first']} of {answer['n']}, p = {p_text(answer['p'])}"
    )
    out["lme_h3"] = diff_text(abstain)
    out["lme_h3_refuse"] = diff_text(refuse)
    for a, short in (("637_tool", "ship"), ("base_tool", "base"), ("always_search", "code")):
        out[f"lme_found_{short}"] = str(found[a])
        out[f"lme_answer_{short}"] = str(m[a]["answer_in_reply"]["hits"])
        out[f"lme_refuse_{short}"] = str(m[a]["refusal_on_answerable"]["hits"])
        out[f"lme_abstain_{short}"] = str(m[a]["abstention"]["hits"])
        out[f"lme_secs_{short}"] = f"{m[a]['seconds_per_question']:.2f}"
    out["lme_clean"] = of(m["637_tool"]["clean_first_calls"])
    out["lme_clean_base"] = of(m["base_tool"]["clean_first_calls"])
    answers = [m[a]["answer_in_reply"]["hits"] for a in LME_ARMS]
    out["lme_answer_range"] = f"{min(answers)} to {max(answers)} of {read_n}"
    ev = m["evidence_only"]
    same = ev["same_questions_other_arms"]
    out["lme_evidence_arm"] = (
        f"{ev['completed']} completed, {ev['skipped']} skipped; the gold in "
        f"{ev['answer_in_reply']['hits']} of {ev['answer_in_reply']['of']} replies"
    )
    out["lme_evidence_same"] = ", ".join(f"{LME_ARM_WORDS[a]} {same[a]['hits']}" for a in LME_ARMS)
    runner = (REPO_ROOT / "scripts" / "run_longmemeval.py").read_text(encoding="utf-8")
    limit = re.search(r"^EVIDENCE_LIMIT = (\d+)", runner, re.M)
    out["lme_evidence_limit"] = f"{int(limit.group(1)):,}"
    references = scores["references"]
    out["lme_question_search"] = of(references["question_search"]["first_search_turn"])
    out["lme_random"] = of(references["random_passages"]["first_search_turn"])
    peaks = [m[a]["peak_vram_gib"] for a in m]
    rerun = [m[a]["rerun_peak_vram_gib"] for a in m]
    out["lme_peaks"] = f"{min(peaks):.2f} to {max(peaks):.2f}"
    out["lme_rerun_peaks"] = f"{min(rerun):.2f} to {max(rerun):.2f}"
    out["lme_dry_n"] = str(len(load(LME / "dry_run_ids.json")["ids"]))
    out["lme_failures"] = "; ".join(
        f"{LME_ARM_WORDS[a]} {m[a]['failures_before_rerun']} to {m[a]['failures']}" for a in m
    )

    # Judged accuracy (measure 4), not the official score: judge 1 decides.
    j = judged["judges"]
    groups = {
        "core_148": "single-session-user and knowledge-update",
        "rest_100": "a fixed random sample of the rest",
        "all_248": "all judged questions",
    }
    arms = (*LME_ARMS, "evidence_only")
    out["lme_judge_spread"] = str(
        max(
            abs(j[other][a][g]["hits"] - j["j1"][a][g]["hits"])
            for other in ("j2", "j3")
            for a in arms
            for g in groups
        )
    )
    judged_rows = []
    evidence_lines = j["j1"]["evidence_only"]["lines"]
    for g, name in groups.items():
        cells = [str(j["j1"][a][g]["hits"]) for a in LME_ARMS]
        cells.append(f"{j['j1']['evidence_only'][g]['hits']} (of its {evidence_lines} lines)")
        judged_rows.append(
            f"| {name} ({j['j1']['637_tool'][g]['of']}) | " + " | ".join(cells) + " |"
        )
    out["lme_judged_table"] = table(
        ["Judged right (questions)", *LME_ARMS.values(), "base, evidence only"], judged_rows
    )
    pairs = judged["paired"]
    vs_base, vs_code = (
        pairs["637_tool_vs_base_tool_all_248"],
        pairs["637_tool_vs_always_search_all_248"],
    )
    if vs_base["failures_wrong"]["difference_and_95_interval"][1] <= 0:
        raise SystemExit("6.37's judged lead over base is gone; update the text")
    if vs_code["failures_wrong"]["difference_and_95_interval"][1] > 0:
        raise SystemExit("6.37 is now judged above code; update the text")
    out["lme_judged_n"] = str(vs_base["failures_wrong"]["n"])
    for a, short in (("637_tool", "ship"), ("base_tool", "base"), ("always_search", "code")):
        out[f"lme_j_{short}"] = str(j["j1"][a]["all_248"]["hits"])
    out["lme_j_max"] = str(max(j["j1"][a]["all_248"]["hits"] for a in LME_ARMS))
    out["lme_judged_vs_base"] = diff_text(vs_base["failures_wrong"])
    out["lme_judged_vs_code"] = diff_text(vs_code["failures_wrong"])
    out["lme_judged_p_base"] = p_text(vs_base["failures_wrong"]["p"])
    out["lme_judged_p_code"] = p_text(vs_code["failures_wrong"]["p"])
    for other, short in (("base_tool", "base"), ("always_search", "code")):
        core = pairs[f"637_tool_vs_{other}_core_148"]["failures_wrong"]
        out[f"lme_judged_core_{short}"] = (
            f"{core['first']} against {core['second']}, p = {p_text(core['p'])}"
        )
        done = pairs[f"637_tool_vs_{other}_all_248"]["completed_by_every_arm"]
        out[f"lme_judged_done_{short}"] = (
            f"{done['first']} against {done['second']} of {done['n']}, p = {p_text(done['p'])}"
        )
    agree = list(judged["judge_agreement"].values())
    same = [a["same"] for a in agree]
    kappas = [a["kappa"] for a in agree]
    out["lme_judges_agree"] = (
        f"{min(same):,} to {max(same):,} of {agree[0]['of']:,} lines (kappa {min(kappas):.2f} to "
        f"{max(kappas):.2f})"
    )
    kevin = judged["kevin_agreement"]  # the author's blind marks (R-170)
    if len({(k["same"], k["kappa"]) for k in kevin.values()}) != 1:
        raise SystemExit("the author's agreement now differs between judges; update the text")
    first_judge = kevin["j1"]
    out["lme_kevin"] = (
        f"{first_judge['same']} of {first_judge['of']} (kappa {first_judge['kappa']:.2f})"
    )
    out["lme_kevin_yes"] = (
        f"I marked {judged['kevin_yes']['hits']} of them right, and judge 1 marked "
        f"{judged['deciding_judge_yes_on_kevins_lines']['hits']}"
    )

    # Added after reading the registered result: the same marks split by question kind.
    key = load(LME / "judge" / "key.json")
    by_arm, kinds, verdicts = judged_split(key)
    split_rows = []
    for kind, ids in kinds.items():
        cells = [str(sum(by_arm[a].get(q, False) for q in ids)) for a in LME_ARMS]
        split_rows.append(f"| {len(ids)} {kind} | " + " | ".join(cells) + " |")
    for a in LME_ARMS:
        total = sum(by_arm[a].get(q, False) for ids in kinds.values() for q in ids)
        if total != j["j1"][a]["all_248"]["hits"]:
            raise SystemExit(f"{a}: the split does not add up to judged.json's count")
    out["lme_split_table"] = table(["Judged right", *LME_ARMS.values()], split_rows)
    answerable = kinds["answerable"]
    ship = by_arm["637_tool"]
    for other, short in (("always_search", "code"), ("base_tool", "base")):
        them = by_arm[other]
        only_ship = sum(ship.get(q, False) and not them.get(q, False) for q in answerable)
        only_them = sum(them.get(q, False) and not ship.get(q, False) for q in answerable)
        p = exact_sign_test(only_ship, only_them)
        if p < 0.05:
            raise SystemExit(
                f"on answerable questions 6.37 now differs from {other}; update the text"
            )
        right_ship = sum(ship.get(q, False) for q in answerable)
        right_them = sum(them.get(q, False) for q in answerable)
        out[f"lme_split_vs_{short}"] = (
            f"{right_ship} against {right_them}; {only_ship} right only for 6.37 and {only_them} "
            f"only for {LME_ARM_WORDS[other]}, p = {p_text(p)}"
        )
        out[f"lme_split_vs_{short}_short"] = f"{right_ship} against {right_them}, p = {p_text(p)}"
        out[f"lme_ans_{short}"] = str(right_them)
        out[f"lme_ans_p_{short}"] = p_text(p)
        out["lme_ans_ship"] = str(right_ship)
        out[f"lme_lead_ans_{short}"] = str(right_ship - right_them)
    unanswered = {a: sum(by_arm[a].get(q, False) for q in kinds["unanswerable"]) for a in LME_ARMS}
    if unanswered["637_tool"] <= max(v for a, v in unanswered.items() if a != "637_tool"):
        raise SystemExit("6.37 no longer leads on the unanswerable questions; update the text")
    lead = int(out["lme_j_ship"]) - int(out["lme_j_base"])
    out["lme_lead"] = str(lead)
    out["lme_lead_unans"] = str(unanswered["637_tool"] - unanswered["base_tool"])
    out["lme_unans_ship"] = str(unanswered["637_tool"])
    if int(out["lme_lead_unans"]) + int(out["lme_lead_ans_base"]) != lead:
        raise SystemExit("the judged lead over base does not split into its two parts")
    out["lme_unanswerable_n"] = str(len(kinds["unanswerable"]))
    out["lme_judged_answerable_n"] = str(len(answerable))

    # Where the author's blind marks and judge 1 differ, from the key (no reply text).
    human = load(LME / "judge" / "human_key.json")["lines"]
    marks = load(LME / "judge" / "kevin_marks.json")
    line_of = {line["line"]: line for line in key["lines"]}
    others = [judged_split(key, judge)[2] for judge in ("j2", "j3")]
    differ: Counter = Counter()
    for n, mark in marks.items():
        line = line_of[human[n]]
        if any(other[line["line"]] != verdicts[line["line"]] for other in others):
            raise SystemExit(
                "the three judges differ on one of the author's lines; update the text"
            )
        if (mark == "yes") != verdicts[line["line"]]:
            what = "unanswerable" if line["abstention"] else f"`{line['type']}`"
            differ[(what, LME_ARM_WORDS[line["arm"]], mark == "yes")] += 1
    out["lme_kevin_n_differ"] = WORDS[sum(differ.values())]
    out["lme_kevin_differ"] = "; ".join(
        f"{WORDS[count]} {what} line{'s' if count > 1 else ''} from {arm}, which I marked "
        f"{'right' if yes else 'wrong'} and the judges {'wrong' if yes else 'right'}"
        for (what, arm, yes), count in sorted(differ.items())
    )


# --- The sealed run (R-162, R-163) --------------------------------------------------------------


def sealed() -> dict[str, dict]:
    return {c: load(ANALYSIS / "R-162" / f"{c}.json") for c in CONDITIONS}


def size_counts(data: dict) -> dict:
    """Right recall answers at each size, from the percentages, checked against the kind counts."""
    per_size = data["conversations"] // len(SIZES) // len(KINDS) * len(RECALL_KINDS)
    counts = {}
    for who, many in (("base", 1), ("adapters_pooled", len(ADAPTERS))):
        n = per_size * many
        sizes = data["rule_1_recall"]["sizes"]
        counts[who] = {s: round(sizes[str(s)][who] * n / 100) for s in SIZES}
        counts[who]["n"] = n
    kinds = data["per_kind_correct"]
    base_total = sum(kinds[k]["base"] for k in RECALL_KINDS)
    pooled_total = sum(kinds[k][a] for k in RECALL_KINDS for a in ADAPTERS)
    if sum(counts["base"][s] for s in SIZES) != base_total or (
        sum(counts["adapters_pooled"][s] for s in SIZES) != pooled_total
    ):
        raise SystemExit(f"condition {data['condition']}: size counts do not add up")
    return counts


def recall_per_seed(data: dict) -> dict[str, int]:
    kinds = data["per_kind_correct"]
    return {a: sum(kinds[k][a] for k in RECALL_KINDS) for a in ("base", *ADAPTERS)}


def coherence_sample(condition: str) -> int:
    """Conversations judged in one condition: base's lines on its sheets (one per conversation)."""
    total = 0
    for sheet in sorted((COHERENCE_DIR / "R-162").glob(f"sheet_{condition}*")):
        total += sum(e["model"] == "base" for e in load(sheet / "key.json"))
    return total


def sealed_numbers(out) -> None:
    runs = sealed()
    rule1, false_rows, coherence_rows, r016_rows = [], [], [], []
    split_rows, kind_rows, sources = [], [], []
    behaviour_rows: dict[str, list[str]] = {}  # one row a measure, one column a condition
    adapter_rates, base_rates, gains, ship_recall, base_recall = [], [], [], [], []
    ship_p = []  # seed 82 alone against base, each condition (rule 1 pools eight seeds)
    for c, (pool, decoys) in CONDITIONS.items():
        d = runs[c]
        if not d["all_rules_pass"]:
            raise SystemExit(f"condition {c} did not pass; the text says every rule passes")
        name = f"{c}, `{pool}`, {decoys} decoy{'s' if decoys > 1 else ''}"
        counts = size_counts(d)
        cells = []
        for s in SIZES:
            size = d["rule_1_recall"]["sizes"][str(s)]
            cells.append(
                f"{counts['base'][s]} of {counts['base']['n']} ({size['base']}%) "
                f"| {counts['adapters_pooled'][s]} of {counts['adapters_pooled']['n']} "
                f"({size['adapters_pooled']}%) | {size['points']:+.1f}"
            )
            base_rates.append(size["base"])
            adapter_rates.append(size["adapters_pooled"])
            gains.append(size["points"])
        if d["rule_1_recall"]["sign_test"]["p"] >= 0.01:
            raise SystemExit(f"condition {c}: the sign test is not below 0.01")
        interval = points(d["eight_seeds_conversation_resampled_interval"]["difference"])
        rule1.append(f"| {name} | " + " | ".join(cells) + f" | {interval} |")
        if d["rule_2_recall_retrieved_only"] != d["rule_1_recall"]:
            raise SystemExit(
                f"condition {c}: rule 2 differs from rule 1; the text says it does not"
            )
        b = d["behaviour"]
        per_seed = recall_per_seed(d)
        if any(b[a]["recall_right_and_found"] != per_seed[a] for a in ADAPTERS):
            raise SystemExit(f"condition {c}: some right adapter answer was not retrieved")
        if b["base"]["recall_right_and_found"] != d["shipped_seed_82"]["base_recall"]:
            raise SystemExit(f"condition {c}: some right base answer was not retrieved")
        sources.append(c)
        fr = d["rule_3_false_retrieval"]["counts"]
        false_rows.append(f"| {c} | {fr['base']} | {span(fr[a] for a in ADAPTERS)} | {fr[SHIP]} |")
        cells = []
        for coh in (
            d["rule_4_coherence"]["coherent"],
            d["coherence_judges_2_and_3"]["j2"]["coherent"],
            d["coherence_judges_2_and_3"]["j3"]["coherent"],
        ):
            if min(coh[a] for a in ADAPTERS) <= coh["base"]:
                raise SystemExit(f"condition {c}: an adapter is not above base under some judge")
            cells.append(f"{coh['base']} / {span(coh[a] for a in ADAPTERS)} / {coh[SHIP]}")
        coherence_rows.append(f"| {c} | {coherence_sample(c)} | " + " | ".join(cells) + " |")
        r = d["r016_three_seeds_recall"]
        r016_rows.append(
            f"| {c} | "
            + " | ".join(
                f"{r['sizes'][str(s)]['base']}% → {r['sizes'][str(s)]['adapters_pooled']}% "
                f"({r['sizes'][str(s)]['points']:+.1f})"
                for s in SIZES
            )
            + f" | {'met' if r['pass'] and r['sign_test']['p'] < 0.01 else 'NOT met'} |"
        )
        kinds = d["per_kind_correct"]
        per_kind_n = d["conversations"] // len(KINDS)
        split = []
        for k in RECALL_KINDS:
            pooled_k = sum(kinds[k][a] for a in ADAPTERS)
            split.append(
                f"{kinds[k]['base']} | {kinds[k][SHIP]} | {span(kinds[k][a] for a in ADAPTERS)} "
                f"| {pooled_k} of {per_kind_n * len(ADAPTERS)}"
            )
        split_rows.append(f"| {c} | " + " | ".join(split) + " |")
        kind_rows.append(
            f"| {c} | "
            + " | ".join(
                f"{kinds[k]['base']} / {kinds[k][SHIP]} / {span(kinds[k][a] for a in ADAPTERS)}"
                for k in ("in_view", "never_told", "statement")
            )
            + " |"
        )
        if not all(b[a]["clean_calls"]["clean"] == b[a]["clean_calls"]["of"] for a in ADAPTERS):
            raise SystemExit(f"condition {c}: some adapter call was not clean")
        cells = {
            "Right search decisions: base": b["base"]["right_decisions"],
            "Right search decisions: seed 82": b[SHIP]["right_decisions"],
            "Right search decisions: eight seeds": span(b[a]["right_decisions"] for a in ADAPTERS),
            "Clean first calls: base": (
                f"{b['base']['clean_calls']['clean']} of {b['base']['clean_calls']['of']}"
            ),
            "Clean first calls: seed 82": (
                f"{b[SHIP]['clean_calls']['clean']} of {b[SHIP]['clean_calls']['of']}"
            ),
            "Ran out of calls: base": b["base"]["ran_out_of_calls"],
            "Ran out of calls: all eight adapters": sum(b[a]["ran_out_of_calls"] for a in ADAPTERS),
            "Seed 82 recall: fact found / right": (
                f"{b[SHIP]['recall_found_fact']} / {b[SHIP]['recall_right_and_found']}"
            ),
        }
        for measure, value in cells.items():
            behaviour_rows.setdefault(measure, []).append(str(value))
        ship_recall.append(d["shipped_seed_82"]["recall"])
        base_recall.append(d["shipped_seed_82"]["base_recall"])
        if d["shipped_seed_82"]["sign_test_p"] >= 0.01:
            raise SystemExit(f"condition {c}: seed 82's sign test is not below 0.01")
        ship_p.append(d["shipped_seed_82"]["sign_test_p"])
    out["sealed_conversations"] = str(runs["A"]["conversations"])
    out["sealed_recall_n"] = str(runs["A"]["shipped_seed_82"]["questions"])
    out["sealed_per_kind_n"] = str(runs["A"]["conversations"] // len(KINDS))
    out["sealed_kind_size_n"] = str(runs["A"]["conversations"] // len(KINDS) // len(SIZES))
    out["sealed_adapters_range"] = f"{min(adapter_rates)} to {max(adapter_rates)}"
    out["sealed_base_range"] = f"{min(base_rates)} to {max(base_rates)}"
    out["sealed_gain_range"] = f"{min(gains):.0f} to {max(gains):.0f}"
    out["sealed_ship_range"] = span(ship_recall)
    out["sealed_ship_p_max"] = p_text(max(ship_p))
    out["sealed_shipbase_range"] = span(base_recall)
    out["sealed_ship_by_condition"] = ", ".join(
        f"{runs[c]['shipped_seed_82']['recall']} against "
        f"{runs[c]['shipped_seed_82']['base_recall']} ({c})"
        for c in CONDITIONS
    )
    out["sealed_rule1_table"] = table(
        [
            "Condition",
            "Base, 58 messages",
            "Eight adapters pooled, 58",
            "Points",
            "Base, 419 messages",
            "Eight adapters pooled, 419",
            "Points",
            "Gain, 95% interval resampling conversations (points)",
        ],
        rule1,
    )
    out["sealed_false_table"] = table(
        ["Condition", "Base", "Eight adapters", "Seed 82"], false_rows
    )
    out["sealed_coherence_table"] = table(
        [
            "Condition",
            "Conversations judged",
            "Judge 1 (decides): base / eight adapters / seed 82",
            "Judge 2",
            "Judge 3",
        ],
        coherence_rows,
    )
    out["sealed_r016_table"] = table(
        [
            "Condition",
            "58 messages: base → seeds 82, 83, 94 pooled (points)",
            "419 messages",
            "Rule 1",
        ],
        r016_rows,
    )
    out["sealed_split_table"] = table(
        [
            "Condition",
            "`older`: base",
            "seed 82",
            "eight seeds",
            "eight pooled",
            "`confirm`: base",
            "seed 82",
            "eight seeds",
            "eight pooled",
        ],
        split_rows,
    )
    out["sealed_kind_table"] = table(
        [
            "Condition",
            "`in_view`: base / seed 82 / eight seeds",
            "`never_told`: the same",
            "`statement`: the same",
        ],
        kind_rows,
    )
    out["sealed_behaviour_table"] = table(
        ["Measure", *CONDITIONS],
        [f"| {name} | " + " | ".join(cells) + " |" for name, cells in behaviour_rows.items()],
    )

    # For the results-at-a-glance table: one value a pool where its two conditions agree.
    def by_pool(cells: list[str]) -> str:
        per_condition = dict(zip(CONDITIONS, cells, strict=True))
        pools = []
        for pool in ("heldout", "independent"):
            values = [per_condition[c] for c, (p, _) in CONDITIONS.items() if p == pool]
            pools.append(" / ".join(dict.fromkeys(values)))
        return ", ".join(pools)

    for who, name in (("base", "base"), ("seed 82", "ship")):
        out[f"sealed_decisions_{name}"] = by_pool(behaviour_rows[f"Right search decisions: {who}"])
        out[f"sealed_clean_{name}"] = by_pool(behaviour_rows[f"Clean first calls: {who}"])
    ranks = []
    for c in ("C", "D"):
        confirm = runs[c]["per_kind_correct"]["confirm"]
        values = sorted(confirm[a] for a in ADAPTERS)
        if confirm[SHIP] != values[0]:
            raise SystemExit("seed 82 is no longer lowest on confirm in C or D; update the text")
        ranks.append(f"{confirm[SHIP]} of {runs[c]['conversations'] // len(KINDS)} in {c}")
    out["sealed_ship_confirm"] = " and ".join(ranks)
    out["sealed_ship_confirm_top"] = str(
        max(runs[c]["per_kind_correct"]["confirm"][a] for c in ("C", "D") for a in ADAPTERS)
    )
    found = [runs[c]["behaviour"][SHIP] for c in ("C", "D")]
    out["sealed_ship_found_cd"] = (
        f"found the fact in {found[0]['recall_found_fact']} (C) and {found[1]['recall_found_fact']}"
        f" (D) and answered {found[0]['recall_right_and_found']} and "
        f"{found[1]['recall_right_and_found']} of those right"
    )
    misses, found_wrong = [], []
    for c, f in zip(("C", "D"), found, strict=True):
        n = runs[c]["shipped_seed_82"]["questions"]
        missed = n - recall_per_seed(runs[c])[SHIP]
        confirm_n = runs[c]["conversations"] // len(KINDS)
        missed_confirm = confirm_n - runs[c]["per_kind_correct"]["confirm"][SHIP]
        misses.append(f"{missed_confirm} of its {missed} misses in {c}")
        found_wrong.append(f["recall_found_fact"] - f["recall_right_and_found"])
    out["sealed_ship_misses_cd"] = " and ".join(misses)
    out["sealed_ship_found_wrong"] = f"{found_wrong[0]} and {found_wrong[1]}"
    out["sealed_per_seed"] = "; ".join(
        f"{c}, " + ", ".join(str(recall_per_seed(runs[c])[a]) for a in ADAPTERS) for c in CONDITIONS
    )
    below = sum(
        runs[c]["per_kind_correct"]["in_view"][a] < runs[c]["per_kind_correct"]["in_view"]["base"]
        for c in ("A", "B")
        for a in ADAPTERS
    )
    out["sealed_in_view_below"] = f"{below} of the {2 * len(ADAPTERS)}"


# --- Cost (R-163) -------------------------------------------------------------------------------


def cost_numbers(out) -> None:
    runs = sealed()
    rows: dict[str, list[str]] = {}  # one row a measure, one column a condition
    peaks, shares = [], []
    for c in CONDITIONS:
        cost = runs[c]["cost"]
        b, s = cost["base"], cost[SHIP]
        per = [cost[a]["seconds_per_conversation"] for a in ADAPTERS]
        searches = [cost[a]["searches_per_conversation"] for a in ADAPTERS]
        share = 100 * s["tokens_read_per_turn"] / s["whole_chat_tokens"]
        shares.append(share)
        cells = {
            "Base: seconds, per conversation": (
                f"{b['seconds']}, {b['seconds_per_conversation']:.2f}"
            ),
            "Seed 82: seconds, per conversation": (
                f"{s['seconds']}, {s['seconds_per_conversation']:.2f}"
            ),
            "Eight adapters: seconds per conversation": f"{min(per):.2f} to {max(per):.2f}",
            "Tokens read per turn, base / seed 82": (
                f"{b['tokens_read_per_turn']:,.0f} / {s['tokens_read_per_turn']:,.0f}"
            ),
            "Whole chat, tokens": f"{s['whole_chat_tokens']:,.0f}",
            "Seed 82 reads, share of the whole chat": f"{share:.0f}%",
            "Tokens written per turn, base / seed 82": (
                f"{b['tokens_written_per_turn']:.0f} / {s['tokens_written_per_turn']:.0f}"
            ),
            "Searches per conversation, base / eight adapters": (
                f"{b['searches_per_conversation']:.2f} / {min(searches):.2f} to {max(searches):.2f}"
            ),
        }
        for measure, value in cells.items():
            rows.setdefault(measure, []).append(value)
        peaks += [cost[a]["peak_vram_gib"] for a in ("base", *ADAPTERS)]
    out["cost_table"] = table(
        ["Measure", *CONDITIONS],
        [f"| {name} | " + " | ".join(cells) + " |" for name, cells in rows.items()],
    )
    out["cost_share"] = f"{min(shares):.0f} to {max(shares):.0f}"
    out["cost_peak"] = f"{max(peaks):.2f}"
    times = list(load(COHERENCE_DIR / "R-162" / "judge_times.json").values())
    out["judges_n"] = str(len(times))
    out["judge_times"] = (
        f"{min(times)} to {max(times)} s each, median {statistics.median(times):.0f} s"
    )
    reports = [train_report(a) for a in ADAPTERS]
    minutes = [r["train_seconds"] / 60 for r in reports]
    out["train_minutes"] = f"{min(minutes):.0f} to {max(minutes):.0f}"
    out["train_peak"] = span(f"{r['train_peak_vram_gib']:.2f}" for r in reports)
    hours = {}  # GPU time the run files record (R-217's sum, carried to the newest run)
    for key, pattern, field in (
        ("train", "recall_train/*.json", "train_seconds"),
        ("eval", "recall_eval/*.json", "seconds"),
        ("s3", "s3/s3_*.json", "seconds"),
    ):
        files = sorted(RESULTS.glob(pattern))
        hours[key] = (len(files), sum(load(f)[field] for f in files) / 3600)
        out[f"gpu_{key}"] = f"{hours[key][1]:.1f} hours over {hours[key][0]:,} runs"
    out["gpu_total"] = f"{sum(h for _, h in hours.values()):.0f}"


# --- The outside-writer sets (R-146, R-157, R-164) ----------------------------------------------


def outside_writer_numbers(out) -> None:
    numbers = load(ANALYSIS / "R-164" / "writeup_numbers.json")
    kind_rows, claim_rows, writer_rows, stage_rows = ([] for _ in range(4))
    # The recall and prompted tables: one row a measure, one column a set.
    recall_rows: dict[str, list[str]] = {}
    prompt_rows: dict[str, list[str]] = {}
    for n, prefix in SETS.items():
        blind = load(SET_FILES[n])
        models = numbers["outside_writer_sets"][f"set_{n}"]["models"]
        prim = blind["primary"]
        if (prim["base"], prim["ship"]) != (models["base"]["recall"], models["seed_82"]["recall"]):
            raise SystemExit(f"set {n}: R-164's numbers differ from the set's analysis file")
        seeds = blind["recall_per_seed"]
        if any(seeds[str(s)] != models[f"seed_{s}"]["recall"] for s in SEEDS):
            raise SystemExit(f"set {n}: per-seed recall differs between R-164 and the set's file")
        base_key = f"{prefix}_base"
        out["ow_chats"] = str(blind["chats"])
        out["ow_items"] = str(blind["items"])
        out["ow_recall_n"] = str(prim["items"])
        out[f"ow_base_recall_{n}"] = str(prim["base"])
        out[f"ow_82_recall_{n}"] = str(prim["ship"])
        out[f"ow_82_p_{n}"] = p_text(prim["p_exact_sign"])
        out[f"ow_82_int_{n}"] = points(prim["chat_resampled_interval"]["difference"])
        pooled_interval = blind["recall_eight_seeds_chat_resampled_interval"]["difference"]
        out[f"ow_seeds_{n}"] = span(seeds.values())
        out[f"ow_seeds_int_{n}"] = points(pooled_interval)
        out[f"ow_seeds_diff_{n}"] = f"{100 * pooled_interval[0]:+.1f}"
        out[f"ow_82_diff_{n}"] = f"{100 * prim['chat_resampled_interval']['difference'][0]:+.1f}"
        out[f"ow_82_rel_{n}"] = f"{100 * prim['chat_resampled_interval']['relative_gain'][0]:+.0f}%"
        statement = blind["per_kind_right_decision"]["statement"]
        out[f"ow_82_stmt_searched_{n}"] = str(statement["items"] - statement["82"])
        out[f"ow_base_stmt_searched_{n}"] = str(statement["items"] - statement[base_key])
        for who, label in (("82", SHIP), ("base", "base")):  # recall questions that searched
            asked = [r for r in eval_rows(f"{prefix}_{label}", 0) if r["kind"] in RECALL_KINDS]
            out[f"ow_{who}_recall_searched_{n}"] = str(sum(bool(r["queries"]) for r in asked))
        order = sorted(seeds.values())
        out[f"ow_82_place_{n}"] = (
            "the lowest of the eight"
            if seeds["82"] == order[0]
            else "inside the eight seeds' range"
        )
        cells = {
            "Base, tool": prim["base"],
            "6.37 seed 82, tool": prim["ship"],
            "Only base right, only seed 82 right, sign test": (
                f"{prim['only_base']}, {prim['only_ship']}, p = {p_text(prim['p_exact_sign'])}"
            ),
            "Seed 82 gain, 95% interval resampling chats (points)": points(
                prim["chat_resampled_interval"]["difference"]
            ),
            "Each seed (82, 83, 94 to 99)": ", ".join(str(seeds[str(s)]) for s in SEEDS),
            "Eight seeds pooled, gain interval (points)": points(pooled_interval),
        }
        for measure, value in cells.items():
            recall_rows.setdefault(measure, []).append(str(value))
        kinds = blind["per_kind_correct"]
        kind_rows.append(
            f"| Set {n} | "
            + " | ".join(
                f"{kinds[k][base_key]} / {kinds[k]['82']} / "
                f"{span(kinds[k][str(s)] for s in SEEDS)} of {kinds[k]['items']}"
                for k in KINDS
            )
            + " |"
        )
        for k in RECALL_KINDS:
            out[f"ow_{k}_{n}"] = f"{kinds[k]['82']} against {kinds[k][base_key]}"
        out[f"ow_statement_{n}"] = (
            f"{kinds['statement']['82']} against {kinds['statement'][base_key]}"
        )
        decisions = blind["per_kind_right_decision"]
        out[f"ow_confirm_searched_{n}"] = (
            f"{decisions['confirm']['82']} of {decisions['confirm']['items']}, "
            f"base {decisions['confirm'][base_key]}"
        )
        cb, c82 = models["base"]["claims"], models["seed_82"]["claims"]
        corrected = [models[f"seed_{s}"]["claims"]["corrected_false"] for s in SEEDS]
        claim_rows.append(
            f"| Set {n} | {cb['right_on_true']} / {c82['right_on_true']} of {cb['true_claims']} "
            f"| {cb['corrected_false']} / {c82['corrected_false']} of {cb['false_claims']} "
            f"| {span(corrected)} | {cb['searched']} / {c82['searched']} |"
        )
        out[f"claims_82_corrected_{n}"] = str(c82["corrected_false"])
        out[f"claims_base_corrected_{n}"] = str(cb["corrected_false"])
        out[f"claims_82_true_{n}"] = str(c82["right_on_true"])
        out["claims_false_n"] = str(c82["false_claims"])
        out["claims_true_n"] = str(c82["true_claims"])
        pc = numbers["outside_writer_sets"][f"set_{n}"]["prompt_control"]
        tests = [
            f"{t['only_first']}, {t['only_second']}, p = {p_text(t['p'])}"
            for t in (pc["base_prompta_vs_seed_82"], pc["base_promptb_vs_seed_82"])
        ]
        cells = {
            "Base": models["base"]["recall"],
            "Base, prompt A (rules)": models["base_prompta"]["recall"],
            "Base, prompt B (rules and four worked examples)": models["base_promptb"]["recall"],
            "6.37 seed 82": models["seed_82"]["recall"],
            "Prompt A against seed 82: only A right, only 6.37 right, sign test": tests[0],
            "Prompt B against seed 82 (the same)": tests[1],
        }
        for measure, value in cells.items():
            prompt_rows.setdefault(measure, []).append(str(value))
        writers = blind["recall_per_writer"]
        writer_rows.append(
            f"| Set {n} | "
            + "; ".join(
                f"{w}: {v['base']} / {v['ship']} / {span([v['seeds_min'], v['seeds_max']])}"
                for w, v in writers.items()
            )
            + f" (of {next(iter(writers.values()))['items']} each) |"
        )
        out["ow_writers"] = str(len(writers))
        if not all(v["ship"] > v["base"] for v in writers.values()):
            raise SystemExit(f"set {n}: seed 82 is not above base for every writer")
        st = blind["ship_recall_miss_stages"]
        stage_rows.append(
            f"| Set {n} | {sum(st.values())} | {st['a_no_search']} "
            f"| {st['b_search_missed_the_fact']} | {st['c_named_a_wrong_value']} "
            f"| {st['d_found_but_wrong_otherwise']} |"
        )
        if max(st, key=st.get) != "b_search_missed_the_fact":
            raise SystemExit(f"set {n}: a missed search is no longer seed 82's largest stage")
        out[f"ow_missed_{n}"] = f"{st['b_search_missed_the_fact']} of {sum(st.values())}"
        wv = blind["recall_on_questions_with_wrong_values"]
        out[f"ow_wrongvals_{n}"] = f"{wv['ship']} against {wv['base']} of {wv['items']}"
    set_columns = [f"Set {n}" for n in SETS]
    out["ow_recall_table"] = table(
        [f"Recall (of {out['ow_recall_n']})", *set_columns],
        [f"| {name} | " + " | ".join(cells) + " |" for name, cells in recall_rows.items()],
    )
    out["ow_kind_table"] = table(
        ["Set", *(f"{KIND_NAMES[k]}: base / seed 82 / eight seeds" for k in KINDS)], kind_rows
    )
    out["ow_claims_table"] = table(
        [
            "Set",
            "True claims confirmed: base / seed 82",
            "False claims corrected: base / seed 82",
            "False claims corrected, eight seeds",
            "Tag questions searched: base / seed 82",
        ],
        claim_rows,
    )
    out["ow_prompt_table"] = table(
        [f"Recall (of {out['ow_recall_n']})", *set_columns],
        [f"| {name} | " + " | ".join(cells) + " |" for name, cells in prompt_rows.items()],
    )
    out["ow_writer_table"] = table(
        ["Set", "Recall per writer: base / seed 82 / eight seeds"], writer_rows
    )
    out["ow_stage_table"] = table(
        [
            "Set",
            "Wrong recall answers, seed 82",
            "Did not search",
            "Searched, the fact not found",
            "Named a listed wrong value",
            "Found the fact, wrong otherwise",
        ],
        stage_rows,
    )
    hd = numbers["hard_dev"]
    out["hd_base"], out["hd_82"], out["hd_n"] = (
        str(hd["base"]),
        str(hd["seed_82"]),
        str(hd["questions"]),
    )
    rigor = load(ANALYSIS / "R-139" / "dev_rigor.json")
    across = {a["condition"]: a for a in rigor["across_seeds"]}
    if across["hd"]["per_seed"]["82"] != hd["seed_82"] or across["hd"]["base"] != hd["base"]:
        raise SystemExit("R-141's hard_dev counts differ from R-164's")
    out["probe_templates"] = str(across["probe"]["templates"])
    out["hd_templates"] = str(across["hd"]["templates"])
    out["hd_seed_range"] = f"{across['hd']['min']} to {across['hd']['max']}"
    out["probe_base"] = str(across["probe"]["base"])
    out["probe_seed_range"] = f"{across['probe']['min']} to {across['probe']['max']}"
    out["hd_82_place"] = (
        "the lowest of the eight"
        if across["hd"]["per_seed"]["82"] == across["hd"]["min"]
        else "inside the eight seeds' range"
    )


# --- Method and protocol ------------------------------------------------------------------------


def method_numbers(out) -> None:
    report = train_report(SHIP)
    lines = (REPO_ROOT / report["data"]).read_text(encoding="utf-8").splitlines()
    kinds = Counter(json.loads(line)["kind"] for line in lines if line.strip())
    if sum(kinds.values()) != report["rows"]:
        raise SystemExit("the training set's rows differ from the train report's")
    recipe = ("data", "learning_rate", "lora_r", "lora_targets", "epochs", "loss_on", "rows")
    for other in ADAPTERS:
        r = train_report(other)
        if any(r[k] != report[k] for k in recipe):
            raise SystemExit(f"{other} was not trained with seed 82's recipe")
    mantissa, exponent = f"{report['learning_rate']:.0e}".split("e")
    targets = ", ".join(f"`{t}`" for t in report["lora_targets"])
    out["training_rows"] = f"{report['rows']:,}"
    out["training_kinds"] = ", ".join(f"`{k}` {kinds[k]}" for k in KINDS)
    out["training_file"] = f"`{report['data']}`"
    out["training_setup"] = (
        f"LoRA rank {report['lora_r']} on {targets}; peak learning rate "
        f"{mantissa}e{int(exponent)}, {report['epochs']} epochs, batch {report['batch_size']}, "
        f"loss mode `{report['loss_on']}`, "
        f"with TRL's chunked loss replaced by `{report['loss']}`; trained from no adapter; "
        f"{report['decision_rows']} plain-chat rows carry loss only on the reply's first token and "
        "its end-of-turn marker"
    )
    first = train_report("seed_81")  # R-018's adapter, trained as R-016 registered
    out["r016_rows"] = str(first["rows"])
    m, e = f"{first['learning_rate']:.0e}".split("e")
    out["r016_lr"] = f"{m}e{int(e)}"
    out["ship_lr"] = f"{mantissa}e{int(exponent)}"
    out["ship_rank"] = str(report["lora_r"])
    out["ship_targets_n"] = WORDS[len(report["lora_targets"])]
    audits = sorted(p.stem for p in (RESULTS / "audit").glob("*.json"))
    if any("fix17cs37" in a for a in audits):
        raise SystemExit("an AuditKIT run on 6.37 now exists; update the text")
    out["auditkit_runs"] = ", ".join(f"`{a}`" for a in audits)


def protocol_numbers(out) -> None:
    agree = load(RESULTS / "human_check" / "R-139" / "agreement.json")
    second = agree["second_marker"]
    out["human_check"] = (
        f"I (not an independent marker) agreed with the scorer on {agree['agree']} "
        f"of {agree['n']} lines (Cohen's kappa {agree['kappa']}), and the scorer passed no reply "
        f"I failed (R-144). A second, independent marker agreed with the scorer on "
        f"{second['agree_with_scorer']} of {agree['n']} (kappa {second['kappa_with_scorer']}) "
        f"and with me on {second['agree_with_kevin']} (kappa {second['kappa_with_kevin']}) "
        "(R-145)"
    )
    out["human_check_n"] = str(agree["n"])
    out["human_check_author"] = str(agree["agree"])
    out["human_check_second"] = str(second["agree_with_scorer"])
    if agree["kevin_wrong_scorer_right"]:
        raise SystemExit("the scorer passed a reply the author failed; the text says it never did")
    spread = load(RESULTS / "freeze" / "R-154" / "judge_spread_r128.json")
    split = sum(s["split_lines"] for s in spread.values())
    lines = sum(s["lines"] for s in spread.values())
    out["judge_spread"] = f"{split} of {lines} lines"


# --- The candidate ledger -----------------------------------------------------------------------

# Name, set label, what it changed, how it ended, record. In BEFORE_V6 the reference is v5.
BEFORE_V6 = [
    (
        "Fix 12",
        "fix12_all",
        "brief, vetted in-view answers",
        "dropped at the screen gate, recall",
        "R-063",
    ),
    (
        "Fix 13",
        "fix13_all",
        "more indirect in-view questions",
        "dropped at the screen gate, recall",
        "R-064",
    ),
    (
        "Fix 14",
        "fix14_all",
        "half the fact rows from 47 new fact types (the wide pool)",
        "failed its gate on `statement` and `never_told`",
        "R-069, R-071",
    ),
    (
        "Fix 14b",
        "fix14b_all",
        "fix 14, with chat lines naming the wide pool's people",
        "failed on `hard_dev` `never_told`",
        "R-073",
    ),
    (
        "Fix 14c",
        "fix14c_all",
        "a quarter of the fact rows from the new types",
        "failed on `hard_dev` `never_told`",
        "R-073",
    ),
    (
        "Fix 15",
        "fix15_all",
        "fix 14c, with never-told rows whose search returns someone else's fact",
        "passed its gate; failed confirmation on judged coherence items",
        "R-074, R-075",
    ),
    (
        "Fix 16a",
        "fix16a",
        "the loss on the taught turns only",
        "failed the screen gate on plain-chat coherence",
        "R-076, R-077",
    ),
    (
        "Fix 16b",
        "fix16b",
        "the loss on all but the scripted small talk",
        "failed its gate on counts",
        "R-079",
    ),
    ("Fix 16c", "fix16c", "fix 16a at learning rate 1e-4", "failed its gate on counts", "R-079"),
    (
        "Fix 17",
        "fix17",
        "fix 16c, with plain-chat targets re-vetted on a stricter rubric",
        "failed on counts",
        "R-078, R-080",
    ),
    (
        "Fix 17b",
        "fix17b",
        "fix 16a with the strictly vetted targets",
        "failed R-076's rule on a judged sheet at seed 83, and again at fresh seeds 85 to 87",
        "R-082, R-091",
    ),
    (
        "Fix 18a",
        "fix18a",
        "fix 17b, with chat lines that name a fact type",
        "dropped at the screen gate, recall",
        "R-083, R-085",
    ),
    (
        "Fix 18c",
        "fix18c",
        "control for 18a: chat lines that name none",
        "dropped at the screen gate, recall",
        "R-085",
    ),
    (
        "Fix 19a",
        "fix19a",
        "fix 18a, with questions asked as statements and answered from a search",
        "passed every count; failed the judged check set",
        "R-086, R-089",
    ),
    (
        "Fix 20",
        "fix20",
        "fix 17b, with one fact-word chat line and one indirect question a type",
        "failed several counted lines",
        "R-087, R-092",
    ),
    (
        "17m (**v6**)",
        "fix17m",
        "fix 17b, with plain-chat rows' loss only on the decision and the end marker",
        "passed at 82 and 83 and at fresh seeds 85 to 87: v6",
        "R-088, R-092, R-093",
    ),
]
# The records number the candidates read since v6 (R-093); None: not in that count.
SINCE_V6 = [
    (
        1,
        "Fix A",
        "fix17w",
        "v6, with its 27 slip-shaped answers rewritten",
        "failed a judged sheet under judge 1",
        "R-094, R-095",
    ),
    (
        None,
        "Fix B",
        "fix17mb",
        "v6, with base-written answers' loss only on the first token and end marker",
        "trained and scored at 82 and 83 and counted (R-101); no record states its result",
        "R-095, R-101",
    ),
    (
        2,
        "Fix C1",
        "fix17y",
        "fix A without the 15 answers CuratorKIT's gate rejected",
        "probe recall pooled below v6's",
        "R-097, R-098",
    ),
    (
        3,
        "Fix C2",
        "fix17z",
        "fix A with those 15 answers scripted",
        "`hard_dev` recall pooled below v6's; the track ends",
        "R-098, R-101",
    ),
    (
        4,
        "6.1",
        "fix17cr",
        "v6 plus 170 train-pool rows: corrections in training's wordings, cue controls, "
        "earlier questions in view",
        "a stepping stone, not gated; it broke the screen recall and `hard_dev` recall lines",
        "R-102 to R-104",
    ),
    (
        5,
        "6.11",
        "fix17cr11",
        "6.1 with fix C2's 41 rewritten answers, one epoch on top",
        "probe recall pooled below v6's",
        "R-105, R-106",
    ),
    (
        6,
        "6.111",
        "fix17cr111",
        "one more epoch on 6.11, nothing added",
        "recall below v6's on both sets",
        "R-107, R-108",
    ),
    (
        7,
        "6.2",
        "fix17cs2",
        "6.11's rows, from scratch",
        "passed at 82 and 83; failed a judged `statement` sheet at fresh seed 92",
        "R-109, R-112",
    ),
    (
        8,
        "6.21",
        "fix17cs21",
        "6.2 plus 100 rows whose found line says more than the asked detail, one epoch on top",
        "`hard_dev` recall pooled below v6's",
        "R-110, R-113",
    ),
    (
        9,
        "6.3",
        "fix17cs3",
        "6.2 plus 57 chat lines naming a fact type and 52 questions asked as statements",
        "probe slips at seed 83; screen `statement`",
        "R-114, R-116",
    ),
    (
        10,
        "6.31",
        "fix17cs31",
        "6.3 with those 52 answers scripted, plus 24 contrast statements (someone else "
        "forgets or loses something; no search)",
        "probe recall pooled below v6's",
        "R-117, R-119",
    ),
    (
        11,
        "6.311",
        "fix17cs311",
        "6.31 plus 72 scripted in-view rows, one epoch on top (my call)",
        "`hard_dev` recall pooled",
        "R-118, R-120",
    ),
    (
        12,
        "6.32",
        "fix17cs32",
        "the same 72 rows, from scratch",
        "`hard_dev` recall, probe recall, probe slips",
        "R-118, R-121",
    ),
    (
        13,
        "6.33",
        "fix17cs33",
        "6.31 less the 15 memory-word contrast rows",
        "probe recall pooled below v6's, on a new question",
        "R-122, R-123",
    ),
    (
        14,
        "6.34",
        "fix17cs34",
        "6.33 less the 22 in-view targets that open “It sounds like”",
        "screen `statement` and probe recall",
        "R-122, R-125",
    ),
    (
        15,
        "6.36",
        "fix17cs36",
        "6.31 less the 6 contrast rows whose reply has “Maybe”",
        "screen `statement` and probe recall",
        "R-124, R-126",
    ),
    (
        16,
        "**6.37**",
        "fix17cs37",
        "6.31 less the 9 wallet, umbrella and lost-track contrast rows",
        "passed every line at 82 and 83 and at fresh seeds 94 to 96; shipped and frozen",
        "R-127 to R-131, R-160",
    ),
    (
        17,
        "6.38",
        "fix17cs38",
        "6.37 with 28 deflecting in-view targets rewritten",
        "`hard_dev` recall pooled below 6.37's",
        "R-134, R-140",
    ),
    (
        18,
        "6.39",
        "fix17cs39",
        "6.37 plus R-110's 100 rows, from scratch",
        "`hard_dev` recall pooled below 6.37's",
        "R-147, R-149",
    ),
    (
        19,
        "7",
        "fix17cs7",
        "6.37 with 140 user messages reworded as tag questions (“..., right?”)",
        "screen recall at seed 82",
        "R-153, R-155, R-156",
    ),
    (
        20,
        "7.1",
        "fix17cs71",
        "7 without its 20 `in_view` tag rows",
        "probe `in_view` at seed 83",
        "R-156, R-157",
    ),
]
UNREAD = [  # trained and scored; no record reads the result
    ("17b at 2 epochs and 3e-4", "fix17e2"),
    ("17b at 2 epochs and 2e-4", "fix17e2lr2"),
    ("17r", "fix17r"),
]


def screen(label: str) -> str:
    """Recall of 96 on the development screen (probe seed 51203) at training seed 82."""
    name = "screen_base" if label == "base" else f"screen_{label}_82"
    if not (EVAL_DIR / f"{name}_seed_51203.json").exists():
        return "not run"
    return str(recall(eval_rows(name, 51203))[0])


def hard_dev(label: str) -> str:
    """`hard_dev` recall of 96 (seed 73157) at training seed 82."""
    names = {"base": ["hd_base"], "fix11_all": ["hd_v5_82"]}.get(
        label, [f"hd_{label}_82", f"hd_{label.removesuffix('_all')}_82"]
    )
    for name in names:
        if (EVAL_DIR / f"{name}_seed_73157.json").exists():
            return str(recall(eval_rows(name, 73157))[0])
    return "not run"


def ledger_numbers(out) -> None:
    header = [
        "#",
        "Candidate (set)",
        "What it changed",
        "How it ended",
        "Screen recall, seed 82 (of 96)",
        "`hard_dev` recall, seed 82 (of 96)",
        "Record",
    ]
    rows = [
        f"| | Base, untrained | | | {screen('base')} | {hard_dev('base')} | R-017 |",
        f"| | v5 (`fix11_all`) | | the reference for this table | {screen('fix11_all')} "
        f"| {hard_dev('fix11_all')} | R-061 |",
    ]
    rows += [
        f"| | {name} (`{label}`) | {change} | {end} | {screen(label)} | {hard_dev(label)} | {rec} |"
        for name, label, change, end, rec in BEFORE_V6
    ]
    out["ledger_before"] = table(header, rows)
    rows = [
        f"| {num or 'not counted'} | {name} (`{label}`) | {change} | {end} | {screen(label)} "
        f"| {hard_dev(label)} | {rec} |"
        for num, name, label, change, end, rec in SINCE_V6
    ]
    out["ledger_since"] = table(header, rows)
    out["ledger_unread"] = "; ".join(
        f"{name} (`{label}`: screen recall {screen(label)}, `hard_dev` {hard_dev(label)})"
        for name, label in UNREAD
    )
    numbered = [n for n, *_ in SINCE_V6 if n]
    if numbered != list(range(1, len(numbered) + 1)):
        raise SystemExit("the ledger's numbering since v6 has a gap")
    out["ledger_before_n"] = str(len(BEFORE_V6))
    out["ledger_since_n"] = str(len(numbered))
    out["ledger_ship_n"] = str(next(n for n, _, label, *_ in SINCE_V6 if label == "fix17cs37"))
    out["ledger_total"] = str(len(BEFORE_V6) + len(SINCE_V6) + len(UNREAD))
    out["ledger_since_rows"] = str(len(SINCE_V6))
    out["ledger_unread_n"] = str(len(UNREAD))
    labels = [r[1] for r in BEFORE_V6] + [r[2] for r in SINCE_V6] + [r[1] for r in UNREAD]
    if any(screen(label) == "not run" for label in labels):
        raise SystemExit("a counted candidate has no screen run; the text says every one has")
    out["ledger_no_hd"] = WORDS[sum(hard_dev(label) == "not run" for label in labels)]


# --- Toolkit findings ---------------------------------------------------------------------------

AUDIT = RESULTS / "audit" / "v3_probe73157.json"  # the run R-031 reads
AUDIT_BUG_EXAMPLE = RESULTS / "audit" / "v3_probe73157.json"
TRL_LOSS_RUN, LEAN_LOSS_RUN = "hard_in_view_84", "screen_hard_in_view_lean_82"


def toolkit_numbers(out) -> None:
    audit = load(AUDIT)
    labels = audit["labels"]
    agree = sum(v["cases"] - len(v["disagreements_with_our_scorer"]) for v in labels.values())
    cases = sum(v["cases"] for v in labels.values())
    out["auditkit_agree"] = f"{agree} of {cases}"
    found = load(AUDIT_BUG_EXAMPLE)
    first = found["bootstrap"][next(iter(found["bootstrap"]))]["all_kinds"]["bootstrap"]
    out["auditkit_bug_example"] = (
        f"{100 * first['mean_base']:.0f}% → {100 * first['mean_adapter']:.0f}% "
        f"over {first['n']} paired cases"
    )
    before, after = train_report(TRL_LOSS_RUN), train_report(LEAN_LOSS_RUN)
    out["mem_before"] = f"{before['train_peak_vram_gib']:.2f}"
    out["mem_after"] = f"{after['train_peak_vram_gib']:.2f}"
    out["mem_saved"] = f"{before['train_peak_vram_gib'] - after['train_peak_vram_gib']:.1f}"
    steps = after["rows"] / after["batch_size"] * after["epochs"]
    out["step_seconds"] = f"{after['train_seconds'] / steps:.1f}"
    old = {r["id"]: r for r in eval_rows("screen_hard_in_view82", 51203)}
    new = {r["id"]: r for r in eval_rows("screen_hard_in_view_lean82", 51203)}
    differ = sum(old[i]["correct"] != new[i]["correct"] for i in old)
    out["lean_retrain_diff"] = f"{differ} of {len(old)}"
    gate = load(RESULTS / "curator" / "R-096" / "summary.json")
    rejected = gate["rejected_by_set"]["v6"]
    out["curator_v6"] = f"{rejected} of {gate['items'] - gate['slip_shaped']}"
    out["curator_slip"] = str(gate["slip_shaped_rejected"])
    out["curator_other"] = str(rejected - gate["slip_shaped_rejected"])
    test = load(RESULTS / "curator" / "R-098" / "summary.json")["acceptance"]
    if test["scripted_rejected"] or test["passing_rejected"] or not test["go"]:
        raise SystemExit("R-098's acceptance test no longer reads as a pass")
    out["curator_controls"] = test["controls_rejected"]
    stored = {r["id"]: r for r in eval_rows(f"probe_{SHIP}", 73157)}
    repeat = eval_rows(f"rep_probe_{SHIP}", 73157)
    same = sum(r["reply"] == stored[r["id"]]["reply"] for r in repeat)
    out["repeat_match"] = f"{same} of {len(repeat)}"
    first_rows = eval_rows("tuned81", 45356)
    out["first_adapter"] = f"{sum(bool(r['correct']) for r in first_rows)} of {len(first_rows)}"


# --- The reopened work: the candidates, the demos and S3 (R-177 to R-287) -----------------------

S3_DIR = RESULTS / "s3"
DATA_SCREENS = REPO_ROOT / "data" / "screens"
DECIDE = RESULTS / "panels" / "R-279" / "decide_r191.txt"  # the screening that named C1 (R-279)
DEMO_JUDGES = RESULTS / "demo2"
REOPENED = [  # name in decide_r191.py, run label, what it changed, how it ended, records
    (
        "K1",
        "k1_r178",
        "earlier questions in view, facts of other types in every chat",
        "passed every line",
        "R-178, R-198",
    ),
    (
        "K2.1",
        "k2_1_r187",
        "K1's never-told rows moved to other trap types",
        "failed one line (probe in_view at seed 83)",
        "R-187, R-195",
    ),
    (
        "K1.3",
        "k1_3_r200",
        "K1 with each fact restated in other wordings",
        "passed every line; the pick from R-203 to R-279 (R2c held it from R-247 to R-249)",
        "R-200, R-203",
    ),
    (
        "K4.1",
        "k4_1_r209",
        "natural chats by writer agents, near-miss and contrast rows",
        "passed Demo2, failed 4 lines",
        "R-209, R-210",
    ),
    ("K4.2", "k4_2_r210", "K4.1 plus declines after empty searches", "failed Demo2", "R-210"),
    ("K4.3", "k4_3_r211", "K4.2, behind a diagnostic", "not trained", "R-211"),
    ("K4.4", "k4_4_r212", "plus wrong-person and contrast rows", "failed Demo2", "R-212"),
    ("K4.5", "k4_5_r213", "possessives out of every query", "failed Demo2", "R-213"),
    ("K4.6", "k4_6_r214", "never-told rows search twice", "failed Demo2", "R-214"),
    (
        "K4.7",
        "k4_7_r215",
        "plus 64 natural chats from 8 new writers",
        "failed Demo2",
        "R-215, R-218",
    ),
    (
        "K4.6e2",
        "k4_6e2_r214",
        "K4.6 read at its epoch-2 checkpoint",
        "passed Demo2, failed screening",
        "R-219, R-221",
    ),
    (
        "K4.8",
        "k4_8_r220",
        "near-miss and wrong-person questions for the 64 chats",
        "failed Demo2 at both checkpoints",
        "R-220, R-225",
    ),
    (
        "K4.9",
        "k4_9_r224",
        "plus miss-then-hit rows, first call out of the loss",
        "stopped before Demo2",
        "R-224, R-228",
    ),
    (
        "K1.3s",
        "k1_3s_r227",
        "a stage on K1.3: one epoch of K4.8's set at 1e-4",
        "failed Demo2",
        "R-227, R-230",
    ),
    (
        "R2c",
        "k13r2c_r235",
        "a stage on K1.3 on K5's third-search set",
        "passed every line; not eligible (its set failed a check line), and fragile (R2cf)",
        "R-235, R-247, R-249",
    ),
    (
        "R2cf",
        "k13r2cf_r247",
        "R2c's recipe, K5's set less 10 rows",
        "failed hard_dev",
        "R-247, R-249",
    ),
    (
        "OP",
        "k13op_r253",
        "a stage on K1.3's own mistakes on its training chats",
        "failed Demo4's older line",
        "R-253, R-261",
    ),
    (
        "OP2",
        "k136op2_r256",
        "the same, from T6",
        "stopped: no corrections to train on",
        "R-256, R-264",
    ),
    (
        "OP3",
        "k13op3_r263",
        "a second on-policy round from OP",
        "stopped: 0 new answer rows",
        "R-263, R-265",
    ),
    (
        "C1",
        "k13opc1_r263",
        "OP's stage a second time on OP's own set (OP3's control)",
        "passed every line under my change to the demo test; the pick for S3",
        "R-263, R-269, R-279",
    ),
    ("OP4", "k13op4_r267", "second-search rows from OP", "failed hard_dev", "R-267, R-268"),
    (
        "C2",
        "k13opc2_r271",
        "C1 plus the same stage a third time",
        "failed hard_dev never_told by one",
        "R-271, R-272",
    ),
    (
        "OPT",
        "k13opt_r271",
        "rows from C1's own turns on the training templates",
        "not run (C2 failed)",
        "R-271, R-272",
    ),
    ("OPO", "k13opo_r273", "OPT's rows from OP", "stopped: 0 answer rows", "R-274, R-275"),
]


def frac(hits: int, n: int) -> str:
    """Raw counts with the rate: '51 of 708 (7.2%)'."""
    return f"{hits:,} of {n:,} ({100 * hits / n:.1f}%)"


def relative(new: float, old: float) -> str:
    """The relative change from ``old`` to ``new``, signed: '-82%'."""
    return f"{100 * (new - old) / old:+.0f}%"


def decide_lines() -> dict[str, dict[str, str]]:
    """Each candidate's summary lines in R-279's screening output: fails, waits, pick recall."""
    out: dict[str, dict[str, str]] = {}
    for line in DECIDE.read_text(encoding="utf-8").splitlines():
        found = re.match(r"== (\S+): (\d+) FAIL, (\d+) WAIT", line)
        if found:
            out[found[1]] = {"fail": found[2], "wait": found[3], "pick": ""}
        found = re.match(r"== (\S+): pick recall over seeds .*: (\d+)", line)
        if found:
            out[found[1]]["pick"] = found[2]
    return out


def demo_tally(label: str, seed_label: str, demo: str) -> dict[str, tuple[int, int]]:
    """With-search counts of one model on one demo: older, never told (plain and shared word)."""
    per_arm = load(DEMO_JUDGES / f"judge_{label}_82_{demo}" / "tally.json")["per_arm"]
    name = next(a for a in per_arm if a in (seed_label, label.upper().replace("_", ".")))
    cells = {k: tuple(int(x) for x in v.split(" of ")) for k, v in per_arm[name].items()}
    never = [cells["never_told_plain"], cells["never_told_shared_word"]]
    return {"older": cells["older"], "never_told": pooled(never)}


def hd_never_told(run: str) -> str:
    """hard_dev never_told right of 48 at training seed 82, or 'not run'."""
    path = EVAL_DIR / f"hd_{run}_82_seed_73157.json"
    if not path.exists():
        return "not run"
    asked = [r for r in eval_rows(f"hd_{run}_82", 73157) if r["kind"] == "never_told"]
    return f"{sum(bool(r['correct']) for r in asked)}"


def reopened_numbers(out) -> None:
    lines = decide_lines()
    if [name for name, *_ in REOPENED] != list(lines):
        raise SystemExit("the reopened ledger and R-279's screening list different candidates")
    rows = []
    for name, run, change, end, rec in REOPENED:
        line = lines[name]
        screened = "every line read" if line["wait"] == "0" else f"{line['wait']} of 20 not read"
        if line["pick"]:
            end = f"{end}; pick recall {line['pick']}"
        rows.append(
            f"| {name} | {change} | {end} | {hd_never_told(run)} | {hard_dev(run)} "
            f"| {line['fail']} ({screened}) | {rec} |"
        )
    header = [
        "Candidate",
        "What it changed",
        "How it ended",
        "`hard_dev` never-told, seed 82 (of 48)",
        "`hard_dev` recall, seed 82 (of 96)",
        "Lines failed of 20",
        "Record",
    ]
    out["reopened_ledger"] = table(header, rows)
    # Pick recall's denominator: recall questions of probe, hard_dev and both outside-writer sets
    # at each of the three pick seeds (decide_r191.pick_recall, R-192).
    pick_n = 0
    for s in (82, 83, 94):
        for stem, seed in (("probe", 73157), ("hd", 73157), ("blind", 0), ("blind2", 0)):
            pick_n += sum(
                r["kind"] in RECALL_KINDS for r in eval_rows(f"{stem}_k13opc1_r263_{s}", seed)
            )
    out["pick_recall_n"] = f"{pick_n:,}"
    out["reopened_n"] = str(len(REOPENED))
    out["reopened_full"] = WORDS[sum(line["wait"] == "0" for line in lines.values())]
    out["pick_recall_c1"], out["pick_recall_k13"] = lines["C1"]["pick"], lines["K1.3"]["pick"]
    out["pick_recall_k1"] = lines["K1"]["pick"]
    r2c = RESULTS / "panels" / "R-247" / "decide_r191.txt"  # the screening that named R2c (R-247)
    found = re.search(r"== R2c: pick recall over seeds .*: (\d+)", r2c.read_text(encoding="utf-8"))
    out["pick_recall_r2c"] = found[1]
    totals = {}
    for key, label, seed_label in (("c1", "k13opc1", "k13opc1_r263"), ("k13", "k1_3", "k1_3_r200")):
        for demo in ("demo4", "demo5"):
            for kind, (h, n) in demo_tally(label, seed_label, demo).items():
                out[f"{demo}_{key}_{kind}"] = f"{h} of {n}"
                total = totals.setdefault((key, kind), [0, 0])
                total[0], total[1] = total[0] + h, total[1] + n
    for (key, kind), (h, n) in totals.items():
        out[f"demos_{key}_{kind}"] = f"{h} of {n}"
    for label, run in (("k13", "k1_3_r200"), ("op", "k13op_r253")):
        out[f"hd_nt_{label}"] = hd_never_told(run)
    out["hd_nt_c1"], out["hd_nt_c2"] = hd_never_told("k13opc1_r263"), hd_never_told("k13opc2_r271")
    slide = [wilson_interval(int(out[f"hd_nt_{k}"]), 48) for k in ("op", "c1", "c2")]
    if max(lo for lo, _ in slide) > min(hi for _, hi in slide):
        raise SystemExit("the never-told slide's intervals no longer all overlap; update the text")


def s3_numbers(out) -> None:
    rule = load(S3_DIR / "ship_rule.json")
    passes = [x["pass"] for x in rule["lines"]]
    if rule["pass"] or passes[-1] or not all(passes[:-1]):
        raise SystemExit("S3's ship rule no longer fails on (c) alone, which the text says")
    scorer = records_script("score_s3")
    chats, tables = scorer.measure_tables()
    if len(chats) != rule["chats"]:
        raise SystemExit("S3's results files and ship_rule.json disagree on the chats")
    arms = rule["arms"]
    names = {"6.37": "637", "pick": "c1", "base_tool": "base", "whole_chat": "wc"}
    names |= {"always_search": "as"}
    for arm, key in names.items():
        for measure, short in (
            ("recall", "recall"),
            ("copy", "copy"),
            ("never_told_plain", "ntp"),
            ("n_hit_false_answer", "nhit"),
            ("in_view", "iv"),
            ("statement", "st"),
        ):
            m = arms[arm][measure]
            out[f"s3_{short}_{key}"] = frac(m["hits"], m["n"])
    out["s3_chats"] = str(rule["chats"])
    c1, old, base = arms["pick"], arms["6.37"], arms["base_tool"]
    out["s3_gap_points"] = (
        f"{100 * (c1['n_hit_false_answer']['rate'] - base['n_hit_false_answer']['rate']):.1f}"
    )
    for measure, short in (
        ("copy", "copy"),
        ("n_hit_false_answer", "nhit"),
        ("never_told_plain", "ntp"),
        ("recall", "recall"),
    ):
        out[f"s3_rel_{short}"] = relative(c1[measure]["rate"], old[measure]["rate"])
    header = [
        "Arm",
        "Recall (95% interval)",
        "In view",
        "Statement",
        "Never told, plain: names no listed value",
        "Names its in-view wrong value when answering another question",
        "Never told, search returned text: names a value listed for the chat",
    ]
    rows = []
    for arm, measures in arms.items():
        lo, hi = scorer.interval(tables[arm]["recall"], chats)
        cells = [
            f"{measures['recall']['hits']}/{measures['recall']['n']} "
            f"({100 * lo:.0f} to {100 * hi:.0f}%)"
        ]
        cells += [
            f"{measures[m]['hits']}/{measures[m]['n']}"
            for m in ("in_view", "statement", "never_told_plain", "copy", "n_hit_false_answer")
        ]
        rows.append(f"| {scorer.ARM_NAMES[arm]} | " + " | ".join(cells) + " |")
    out["s3_table"] = table(header, rows)
    out["s3_lines"] = "\n".join(
        f"- {'PASS' if x['pass'] else 'FAIL'}: {x['line']}" for x in rule["lines"]
    )
    runs, waiting = [], []  # every report run written so far, one seed at a time (R-288)
    for name in scorer.REPORT:
        for seed in (82, 83):
            label = f"s3_{name}_{seed}"
            if not (S3_DIR / f"{label}.json").exists():
                waiting.append(f"{scorer.ARM_NAMES[name].removesuffix(' (report)')} seed {seed}")
                continue
            rows, m = scorer.load(label), {}
            for measure, counted in scorer.MEASURES.items():
                hits = [h for h in map(counted, rows) if h is not None]
                m[measure] = (sum(hits), len(hits))
            runs.append(
                f"{scorer.ARM_NAMES[name].removesuffix(' (report)')} seed {seed} recall "
                f"{m['recall'][0]} of {m['recall'][1]}, copies {m['copy'][0]} of {m['copy'][1]}, "
                f"false answers {m['n_hit_false_answer'][0]} of {m['n_hit_false_answer'][1]}"
            )
    text = "; ".join(runs) if runs else "none written"
    if waiting:
        text += (
            f". Not yet run when this was built: {', '.join(waiting)} (the queue stopped after K1 "
            "seed 82, R-288, and was restarted, R-289)"
        )
    out["s3_report_arms"] = text
    tally = load(S3_DIR / "coherence" / "tally.json")
    out["s3_coh_n"] = str(tally["judge_1"]["pairs"])
    for j in (1, 2, 3):
        out[f"s3_coh_j{j}"] = (
            f"C1 {tally[f'judge_{j}']['pick_coherent']}, "
            f"base {tally[f'judge_{j}']['base_coherent']}"
        )
    run = load(S3_DIR / "s3_base_tool.json")
    counts = Counter((r["view"], r["kind"]) for r in run["rows"])
    flow = [f"| Chats written, checked by `check_s3.py` | {len(chats)} | none dropped |"]
    flow.append(
        f"| Questions dropped by the brief's rules | {len(run['dropped'])} | the answer is not a "
        "current fact of that person and category |"
    )
    flow += [
        f"| Items, {view} view, `{kind}` | {n} | |" for (view, kind), n in sorted(counts.items())
    ]
    flow.append(
        f"| Items in every arm's run | {len(run['rows'])} | {len(run['batch_problems'])} "
        "batch problems |"
    )
    out["s3_flow"] = table(["Step", "Count", "Reason"], flow)
    out["s3_items"] = f"{len(run['rows']):,}"
    out["s3_writers"] = WORDS[len({r["writer"] for r in run["rows"]})]
    margin = c1["statement"]["rate"] - (base["statement"]["rate"] - scorer.POINTS)
    out["s3_st_margin"] = f"{100 * margin:.1f}"
    overlap = records_script("overlap_s3_training")  # R-179's count, recomputed
    train = overlap.training_runs(DATA_SCREENS / "fix17cs37.jsonl")
    chat_runs = [
        overlap.runs(overlap.chat_text(load(path))) for path in sorted(overlap.CHATS.glob("*.json"))
    ]
    shared, total = sum(len(c & train) for c in chat_runs), sum(len(c) for c in chat_runs)
    out["s3_runs_shared"] = f"{shared} of {total:,}"
    # The same count for C1's training set (seed 82's set: K1.3's rows plus OP's corrections).
    c1_train = overlap.training_runs(REPO_ROOT / train_report("k13opc1_r263_82")["data"])
    out["s3_runs_shared_c1"] = f"{sum(len(c & c1_train) for c in chat_runs)}"
    rows = scorer.arms()
    for arm, key in (("6.37", "637"), ("pick", "c1")):
        wrong = [r for r in rows[arm] if r["kind"] in RECALL_KINDS and not r["item_correct"]]
        missed = sum(not r["found_fact"] and bool(r["queries"]) for r in wrong)
        out[f"s3_missed_{key}"] = f"{missed} of {len(wrong)}"
        out[f"s3_misread_{key}"] = f"{sum(bool(r['found_fact']) for r in wrong)}"
        unsearched = sum(not r["found_fact"] and not r["queries"] for r in wrong)
        out[f"s3_nosearch_{key}"] = str(unsearched)


def c1_card_numbers(out) -> None:
    """C1 seed 82's own numbers for its model card (R-296): lineage, S3 lines, the gap to base."""
    op, c1 = train_report("k13op_r253_82"), train_report("k13opc1_r263_82")
    lineage = (op["init_adapter"], c1["init_adapter"])
    if not (lineage[0].endswith("k1_3_r200_82") and lineage[1].endswith("k13op_r253_82")):
        raise SystemExit("C1's lineage is no longer K1.3, OP's stage, then the same stage again")
    if op["data"] != c1["data"]:
        raise SystemExit("C1's second stage no longer uses OP's set; update the card")

    def projections(cmd: list) -> set:
        """The --lora-targets values of a training command."""
        start = cmd.index("--lora-targets") + 1
        end = next((i for i in range(start, len(cmd)) if cmd[i].startswith("--")), len(cmd))
        return set(cmd[start:end])

    ship = train_report("fix17cs37_82")
    same = projections(c1["provenance"]["command"]) == projections(ship["provenance"]["command"])
    if not same or c1["lora_r"] != ship["lora_r"]:
        raise SystemExit("C1's rank or projections no longer match 6.37's; update the card")
    out["c1_rank"] = str(c1["lora_r"])
    out["c1_set"] = f"`{c1['data']}`"
    out["c1_rows"] = f"{c1['rows']:,}"
    out["c1_stage"] = (
        f"learning rate {c1['learning_rate']:g}, {c1['epochs']:g} epoch, batch {c1['batch_size']}"
    )
    out["c1_minutes"] = f"{(op['train_seconds'] + c1['train_seconds']) / 60:.0f}"
    out["c1_peak"] = f"{max(op['train_peak_vram_gib'], c1['train_peak_vram_gib']):.2f}"
    scorer = records_script("score_s3")
    rows = scorer.load("s3_k13opc1_r263_82")
    counts = {}
    for measure, counted in scorer.MEASURES.items():
        hits = [h for h in map(counted, rows) if h is not None]
        counts[measure] = (sum(hits), len(hits))
    for measure, short in (
        ("recall", "recall"),
        ("in_view", "iv"),
        ("statement", "st"),
        ("never_told_plain", "ntp"),
        ("copy", "copy"),
        ("n_hit_false_answer", "nhit"),
    ):
        out[f"c1s82_{short}"] = frac(*counts[measure])
    base = scorer.measure_tables()[1]["base_tool"]["statement"]
    line = scorer.rate(base) - scorer.POINTS
    st = counts["statement"][0] / counts["statement"][1]
    out["c1s82_st_line"] = (
        f"{'below' if st < line else 'at or above'} (a)'s statement line, base's rate minus 5 "
        f"points ({100 * line:.1f}%)"
    )
    seeds = []
    for seed in (82, 83, 94):
        flag = scorer.MEASURES["n_hit_false_answer"]
        got = [h for h in map(flag, scorer.load(f"s3_k13opc1_r263_{seed}")) if h is not None]
        seeds.append(f"{sum(got)} of {len(got)} (seed {seed})")
    out["c1_nhit_seeds"] = ", ".join(seeds)
    chats, tables = scorer.measure_tables()
    pick, base_t = tables["pick"]["n_hit_false_answer"], tables["base_tool"]["n_hit_false_answer"]
    rng = random.Random(scorer.BOOT_SEED)  # R-281's resampling: chats with replacement
    diffs = []
    for _ in range(scorer.N_RESAMPLES):
        drawn = [rng.choice(chats) for _ in chats]
        diffs.append(scorer.rate(pick, drawn) - scorer.rate(base_t, drawn))
    diffs = sorted(d for d in diffs if d == d)
    lo, hi = diffs[int(0.025 * len(diffs))], diffs[min(int(0.975 * len(diffs)), len(diffs) - 1)]
    if lo > 0:
        raise SystemExit("C1 minus base on N-hit now has its lower bound above 0; update the card")
    out["c1_gap_interval"] = f"{100 * lo:+.1f} to {100 * hi:+.1f} points"


def s3_panel_numbers(out) -> None:
    """S3 numbers R-295 asked for: per seed, the shipped seed, report arms, search measures."""
    scorer = records_script("score_s3")

    def counts(label: str) -> dict[str, tuple[int, int]]:
        rows, got = scorer.load(label), {}
        for measure, counted in scorer.MEASURES.items():
            hits = [h for h in map(counted, rows) if h is not None]
            got[measure] = (sum(hits), len(hits))
        return got

    ship = counts("s3_fix17cs37_82")
    for measure, short in (
        ("recall", "recall"),
        ("copy", "copy"),
        ("n_hit_false_answer", "nhit"),
        ("never_told_plain", "ntp"),
    ):
        out[f"s3_ship82_{short}"] = frac(*ship[measure])
    for run, key in (("fix17cs37", "637"), ("k13opc1_r263", "c1")):
        per = [counts(f"s3_{run}_{seed}")["n_hit_false_answer"] for seed in (82, 83, 94)]
        out[f"s3_seed_nhit_{key}"] = f"{per[0][0]}, {per[1][0]} and {per[2][0]} of {per[0][1]}"
        per = [counts(f"s3_{run}_{seed}")["recall"] for seed in (82, 83, 94)]
        out[f"s3_seed_recall_{key}"] = f"{per[0][0]}, {per[1][0]} and {per[2][0]} of {per[0][1]}"
        found = [r for seed in (82, 83, 94) for r in scorer.load(f"s3_{run}_{seed}")]
        recall_rows = [r for r in found if r["kind"] in RECALL_KINDS]
        out[f"s3_found_{key}"] = frac(
            sum(bool(r["found_fact"]) for r in recall_rows), len(recall_rows)
        )
        conf = [
            [r for r in scorer.load(f"s3_{run}_{seed}") if r["kind"] == "confirm"]
            for seed in (82, 83, 94)
        ]
        searched = [sum(bool(r["queries"]) for r in c) for c in conf]
        out[f"s3_conf_{key}"] = f"{searched[0]}, {searched[1]} and {searched[2]} of {len(conf[0])}"
    code = [r for r in scorer.load("s3_always_search") if r["kind"] in RECALL_KINDS]
    out["s3_found_as"] = frac(sum(bool(r["found_fact"]) for r in code), len(code))
    arms = load(S3_DIR / "ship_rule.json")["arms"]
    chats, tables = scorer.measure_tables()
    base, old = tables["base_tool"], tables["6.37"]
    passing = []
    for arm, key in (("k1_r178", "k1"), ("k2_1_r187", "k21"), ("k1_3_r200", "k13")):
        m = arms[arm]
        out[f"s3_nhit_{key}"] = frac(m["n_hit_false_answer"]["hits"], m["n_hit_false_answer"]["n"])
        t = tables[arm]
        ok = (
            scorer.rate(t["recall"]) > scorer.rate(base["recall"])
            and scorer.lower_bound(t["recall"], base["recall"], chats) > 0
            and all(
                scorer.rate(t[x]) >= scorer.rate(base[x]) - scorer.POINTS
                for x in ("in_view", "statement", "never_told_plain")
            )
            and scorer.rate(t["copy"]) <= scorer.rate(old["copy"]) / 2
            and scorer.rate(old["copy"]) - scorer.rate(t["copy"]) >= scorer.GAP
            and scorer.lower_bound(old["copy"], t["copy"], chats) > 0
            and scorer.rate(old["n_hit_false_answer"]) - scorer.rate(t["n_hit_false_answer"])
            >= scorer.GAP
            and scorer.lower_bound(old["n_hit_false_answer"], t["n_hit_false_answer"], chats) > 0
            and scorer.rate(t["n_hit_false_answer"]) <= scorer.rate(base["n_hit_false_answer"])
        )
        if ok:
            passing.append(arm)
    if passing != ["k1_r178", "k2_1_r187"]:
        raise SystemExit(f"the report arms meeting every measured S3 line are now {passing}")


def s3_round2_numbers(out) -> None:
    """S3 numbers the second review round asked for (R-298); exploratory, beside the rule."""
    scorer = records_script("score_s3")
    chats, tables = scorer.measure_tables()

    def diff(a: dict, b: dict) -> str:  # rate(a) - rate(b), chats resampled as R-281
        rng, got = random.Random(scorer.BOOT_SEED), []
        for _ in range(scorer.N_RESAMPLES):
            drawn = [rng.choice(chats) for _ in chats]
            got.append(scorer.rate(a, drawn) - scorer.rate(b, drawn))
        got = sorted(d for d in got if d == d)
        lo, hi = got[int(0.025 * len(got))], got[min(int(0.975 * len(got)), len(got) - 1)]
        return (
            f"{100 * (scorer.rate(a) - scorer.rate(b)):+.1f} points, 95% interval "
            f"{100 * lo:+.1f} to {100 * hi:+.1f}"
        )

    code = tables["always_search"]["recall"]
    out["s3_code_vs_637"] = diff(code, tables["6.37"]["recall"])
    out["s3_code_vs_c1"] = diff(code, tables["pick"]["recall"])
    for measure, short in (("in_view", "iv"), ("statement", "st"), ("never_told_plain", "ntp")):
        out[f"s3_a_int_{short}"] = diff(tables["pick"][measure], tables["base_tool"][measure])
    c1_82 = scorer.by_chat(scorer.load("s3_k13opc1_r263_82"), scorer.MEASURES["statement"])
    out["c1s82_st_gap"] = diff(c1_82, tables["base_tool"]["statement"])

    runs = {
        "base": scorer.load("s3_base_tool"),
        "as": scorer.load("s3_always_search"),
        "wc": scorer.load("s3_whole_chat"),
        "637": [r for seed in (82, 83, 94) for r in scorer.load(f"s3_fix17cs37_{seed}")],
        "c1": [r for seed in (82, 83, 94) for r in scorer.load(f"s3_k13opc1_r263_{seed}")],
        "c182": scorer.load("s3_k13opc1_r263_82"),
        "k1": [r for seed in (82, 83) for r in scorer.load(f"s3_k1_r178_{seed}")],
        "k21": [r for seed in (82, 83) for r in scorer.load(f"s3_k2_1_r187_{seed}")],
    }
    for key in (
        "637",
        "as",
    ):  # grounding: right answers among recall rows whose search found the fact
        found = [r for r in runs[key] if r["kind"] in RECALL_KINDS and r["found_fact"]]
        out[f"s3_ground_{key}"] = frac(sum(bool(r["item_correct"]) for r in found), len(found))
    right = [r for r in runs["637"] if r["kind"] in RECALL_KINDS and r["item_correct"]]
    notfound = [r for r in right if not r["found_fact"]]
    out["s3_right_notfound_637"] = f"{len(notfound)} of {len(right)}"
    if any(r["kind"] != "confirm" or r["claim"] != "true" or r["queries"] for r in notfound):
        raise SystemExit("6.37's right answers on rows marked not found are not all agreements")
    # `confirm` on S3 is a tag question; a true claim holds the answer in the message, so
    # agreeing with it is right with no memory. `older` alone carries no such cue.
    confirm = [r for r in runs["base"] if r["kind"] == "confirm"]
    true_claims = [r for r in confirm if r["claim"] == "true"]
    older = [r for r in runs["base"] if r["kind"] == "older"]
    if not all(r["answer"].casefold() in r["message"].casefold() for r in true_claims) or any(
        r["answer"].casefold() in r["message"].casefold() for r in older
    ):
        raise SystemExit("S3's true claims no longer all hold the answer, or an older item does")
    out["s3_conf_true"] = f"{len(true_claims)} of {len(confirm)}"
    base_right = [r for r in runs["base"] if r["kind"] in RECALL_KINDS and r["item_correct"]]
    agree = [r for r in base_right if r["kind"] == "confirm" and r["claim"] == "true"]
    out["s3_agree_base"] = f"{len(agree)} of {len(base_right)}"
    out["s3_agree_base_ns"] = str(sum(not r["queries"] for r in agree))
    for key in ("base", "as", "wc", "637", "c1"):
        asked = [r for r in runs[key] if r["kind"] == "older"]
        out[f"s3_older_{key}"] = frac(sum(bool(r["item_correct"]) for r in asked), len(asked))
    runs["ship82"] = scorer.load("s3_fix17cs37_82")
    for key in ("base", "as", "wc", "637", "ship82", "c1", "c182", "k1", "k21"):
        asked = [r for r in runs[key] if r["kind"] == "confirm" and r["claim"] == "false"]
        out[f"s3_fc_{key}"] = f"{sum(bool(r['item_correct']) for r in asked)} of {len(asked)}"
    if not out["s3_fc_637"].startswith("0 of"):
        raise SystemExit("a 6.37 seed now corrects a false claim on S3; the text says none does")
    for key in ("base", "wc", "as", "637", "c1"):
        asked = [r for r in runs[key] if r["kind"] == "re_ask"]
        out[f"s3_reask_{key}"] = f"{sum(bool(r['item_correct']) for r in asked)} of {len(asked)}"
    for key, labels in (
        ("as", ["s3_always_search"]),
        ("637", [f"s3_fix17cs37_{seed}" for seed in (82, 83, 94)]),
        ("c1", [f"s3_k13opc1_r263_{seed}" for seed in (82, 83, 94)]),
    ):  # right search decisions, each run of 834 items
        got = [sum(bool(r["right_decision"]) for r in scorer.load(label)) for label in labels]
        n = len(scorer.load(labels[0]))
        out[f"s3_rd_{key}"] = (
            ", ".join(str(g) for g in got[:-1])
            + (" and " if len(got) > 1 else "")
            + f"{got[-1]} of {n}"
        )
    st82 = [scorer.MEASURES["statement"](r) for r in scorer.load("s3_fix17cs37_82")]
    st82 = [h for h in st82 if h is not None]
    out["s3_ship82_st"] = frac(sum(st82), len(st82))
    k1 = load(S3_DIR / "ship_rule.json")["arms"]["k1_r178"]
    for measure, short in (("recall", "recall"), ("copy", "copy")):
        out[f"s3_{short}_k1"] = frac(k1[measure]["hits"], k1[measure]["n"])
    # Query writing as a cause of lost recall (exploratory): on the same recall questions, did
    # code's raw message find the fact where the seed's own queries did not, or the reverse? A
    # question the seed did not search is a "when" miss, not a query miss, so it is counted apart.
    code = {r["id"]: r for r in runs["as"] if r["kind"] in RECALL_KINDS}
    for key, label in (("637", "s3_fix17cs37_82"), ("c1", "s3_k13opc1_r263_82")):
        own = {r["id"]: r for r in scorer.load(label) if r["kind"] in RECALL_KINDS}
        if set(own) != set(code):
            raise SystemExit(f"{label} and code do not hold the same S3 recall questions")
        code_only = [i for i in own if code[i]["found_fact"] and not own[i]["found_fact"]]
        own_only = [i for i in own if own[i]["found_fact"] and not code[i]["found_fact"]]
        searched = [i for i in code_only if own[i]["queries"]]
        unsearched = [i for i in own if not own[i]["queries"]]
        out[f"s3_qw_code_only_{key}"] = str(len(searched))
        out[f"s3_qw_own_only_{key}"] = str(len(own_only))
        out[f"s3_qw_nosearch_{key}"] = str(len(code_only) - len(searched))
        out[f"s3_qw_unsearched_{key}"] = str(len(unsearched))
        out[f"s3_qw_p_{key}"] = p_text(exact_sign_test(len(searched), len(own_only)))
        # Grounding on the questions both searches found: the seed's reply against base reading
        # code's passages, the same questions (the pooled rates are over different questions).
        both = [i for i in own if own[i]["found_fact"] and code[i]["found_fact"]]
        only_code = sum(bool(code[i]["item_correct"]) and not own[i]["item_correct"] for i in both)
        only_own = sum(bool(own[i]["item_correct"]) and not code[i]["item_correct"] for i in both)
        out[f"s3_gb_n_{key}"] = str(len(both))
        out[f"s3_gb_own_{key}"] = str(sum(bool(own[i]["item_correct"]) for i in both))
        out[f"s3_gb_code_{key}"] = str(sum(bool(code[i]["item_correct"]) for i in both))
        out[f"s3_gb_p_{key}"] = p_text(exact_sign_test(only_code, only_own))
    out["s3_qw_n"] = str(len(code))
    nhit = scorer.MEASURES["n_hit_false_answer"]
    c1_82_nhit = scorer.by_chat(scorer.load("s3_k13opc1_r263_82"), nhit)
    out["c1s82_nhit_gap"] = diff(c1_82_nhit, tables["base_tool"]["n_hit_false_answer"])
    base_rows = runs["base"]
    out["s3_nt_items"] = str(
        sum(r["kind"] == "never_told" and r["view"] == "right" for r in base_rows)
    )
    out["s3_nt_all"] = str(sum(r["kind"] == "never_told" for r in base_rows))
    out["s3_nhit_items"] = str(
        sum(
            r["kind"] == "never_told" and r["n_hit"] and r["false_answer"] is not None
            for r in base_rows
        )
    )
    # Another category's stored value named on an N-hit never-told question, unseen by the flag
    # (R-298): a chat's stored values are the answers of its other S3 items, four letters or more.
    stored: dict[str, dict[str, str]] = {}
    for path in sorted(S3_DIR.glob("s3_*.json")):
        for r in load(path)["rows"]:
            if r.get("answer") and r["kind"] != "never_told":
                stored.setdefault(r["chat"], {})[r["answer"].casefold()] = r["category"]

    def other(r: dict) -> bool:
        text = r["reply"].casefold()
        return any(
            cat != r["category"] and len(v) >= 4 and re.search(r"\b" + re.escape(v) + r"\b", text)
            for v, cat in stored.get(r["chat"], {}).items()
        )

    for key in ("base", "637", "c1", "c182", "k1", "k21"):
        rows = [
            r
            for r in runs[key]
            if r["kind"] == "never_told" and r["n_hit"] and r["false_answer"] is not None
        ]
        named = sum(bool(r["false_answer"]) or other(r) for r in rows)
        out[f"s3_off_{key}"] = frac(named, len(rows))


def numbers() -> dict[str, str]:
    out: dict[str, str] = {}
    for part in (
        status_numbers,
        model_numbers,
        whole_chat_numbers,
        sealed_numbers,
        cost_numbers,
        oom_numbers,
        reference_numbers,
        sealed_reference_numbers,
        outside_reference_numbers,
        speed_numbers,
        longmemeval_numbers,
        outside_writer_numbers,
        method_numbers,
        protocol_numbers,
        ledger_numbers,
        toolkit_numbers,
        reopened_numbers,
        s3_numbers,
        c1_card_numbers,
        s3_panel_numbers,
        s3_round2_numbers,
    ):
        part(out)
    return out


def main() -> None:
    values = numbers()
    for template, out in TEMPLATES.items():
        text = template.read_text(encoding="utf-8")
        missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", text)) - set(values))
        if missing:
            raise SystemExit(f"unfilled in {template.name}: {missing}")
        filled = re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], text)
        if out.name == "ABSTRACT.md":
            # Two counts: by spaces, and by word characters, which splits "6.37" and "of-view".
            for words in (len(filled.split()), len(re.findall(r"\w+", filled))):
                if words > ABSTRACT_WORDS:
                    raise SystemExit(f"the abstract is {words} words, over {ABSTRACT_WORDS}")
        out.write_text(filled, encoding="utf-8")
        print(f"wrote {out.relative_to(REPO_ROOT)}")
    # README is written by hand; its S3 ship-rule line must give the gap the papers give.
    ship_line = f"(c) fail by {values['s3_gap_points']} points"
    if ship_line not in (REPO_ROOT / "README.md").read_text(encoding="utf-8"):
        raise SystemExit(f"README's S3 ship-rule line does not read {ship_line!r}")


if __name__ == "__main__":
    main()
