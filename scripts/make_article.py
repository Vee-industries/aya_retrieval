"""Fill the article and model card templates from committed results files, and write both.

Usage:
    python scripts/make_article.py

Every ``{{name}}`` in ``docs/article_template.md`` and ``docs/model_card_template.md`` is computed
here from files under ``results/`` (and, for the model's context limits, the pinned model's own
config in the local cache), so no result number in either is typed by hand. A placeholder left
unfilled stops the script, and so does any check below that finds two results files disagreeing
or a result that no longer matches what the text says about it.

The numbers are final for the shipped model, 6.37 (``fix17cs37`` seed 82, frozen in R-160): the
sealed run (R-162, R-163), the outside-writer sets (R-146, R-157, R-164) and the whole-chat control
(R-164, R-165).
"""

from __future__ import annotations

import json
import re
import statistics
from collections import Counter

from aya_retrieval.harness import MAX_CALLS
from aya_retrieval.provenance import REPO_ROOT
from aya_retrieval.recall_tool import TOP_K
from aya_retrieval.report_data import (
    COHERENCE_DIR,
    EVAL_DIR,
    KINDS,
    RECALL_KINDS,
    SIZES,
    eval_rows,
    recall,
    train_report,
)
from aya_retrieval.stats import exact_sign_test

DOCS = REPO_ROOT / "docs"
RESULTS = REPO_ROOT / "results"
ANALYSIS = RESULTS / "analysis"
TEMPLATES = {
    DOCS / "article_template.md": DOCS / "ARTICLE.md",
    DOCS / "model_card_template.md": DOCS / "MODEL_CARD.md",
}
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


def paired(first: list[dict], second: list[dict], kind: str) -> tuple[int, int, float]:
    """Only-first-right and only-second-right counts on the same questions, and the sign test."""
    a = {r["id"]: bool(r["correct"]) for r in first if r["kind"] == kind}
    b = {r["id"]: bool(r["correct"]) for r in second if r["kind"] == kind}
    if set(a) != set(b):
        raise SystemExit(f"{kind}: the two runs do not hold the same questions")
    only_a = sum(a[i] and not b[i] for i in a)
    only_b = sum(b[i] and not a[i] for i in a)
    return only_a, only_b, exact_sign_test(only_a, only_b)


def table(header: list[str], rows: list[str]) -> str:
    return "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n" + "\n".join(rows)


# --- Status and the model -----------------------------------------------------------------------


def status_numbers(out) -> None:
    out["status_line"] = (
        "Final numbers for the shipped model, 6.37 (`fix17cs37` seed 82, frozen in R-160): the "
        "sealed final run (registered in R-162, results in R-163), the outside-writer sets "
        "(R-146, R-157) and the whole-chat control (R-164, R-165). Every number is computed from "
        "committed results files by `scripts/make_article.py`."
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
    out["top_k"] = str(TOP_K)
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
    # R-142: the noise of a kind with about 40 questions, as a 95% half-width at a 50% rate.
    n = load(SET_FILES[1])["per_kind_correct"]["confirm"]["items"]
    out["kind_noise"] = f"{100 * 1.96 * (0.25 / n) ** 0.5:.0f}"
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
    split_rows, kind_rows, behaviour_rows, sources = [], [], [], []
    adapter_rates, base_rates, gains, ship_recall, base_recall = [], [], [], [], []
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
        behaviour_rows.append(
            f"| {c} | {b['base']['right_decisions']} | {b[SHIP]['right_decisions']} "
            f"| {span(b[a]['right_decisions'] for a in ADAPTERS)} "
            f"| {b['base']['clean_calls']['clean']} of {b['base']['clean_calls']['of']} "
            f"| {b[SHIP]['clean_calls']['clean']} of {b[SHIP]['clean_calls']['of']} "
            f"| {b['base']['ran_out_of_calls']} "
            f"| {sum(b[a]['ran_out_of_calls'] for a in ADAPTERS)} "
            f"| {b[SHIP]['recall_found_fact']} / {b[SHIP]['recall_right_and_found']} |"
        )
        ship_recall.append(d["shipped_seed_82"]["recall"])
        base_recall.append(d["shipped_seed_82"]["base_recall"])
        if d["shipped_seed_82"]["sign_test_p"] >= 0.01:
            raise SystemExit(f"condition {c}: seed 82's sign test is not below 0.01")
    out["sealed_conversations"] = str(runs["A"]["conversations"])
    out["sealed_recall_n"] = str(runs["A"]["shipped_seed_82"]["questions"])
    out["sealed_per_kind_n"] = str(runs["A"]["conversations"] // len(KINDS))
    out["sealed_adapters_range"] = f"{min(adapter_rates)} to {max(adapter_rates)}"
    out["sealed_base_range"] = f"{min(base_rates)} to {max(base_rates)}"
    out["sealed_gain_range"] = f"{min(gains):.0f} to {max(gains):.0f}"
    out["sealed_ship_range"] = span(ship_recall)
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
        [
            "Condition",
            "Right search decisions: base",
            "seed 82",
            "eight seeds",
            "Clean first calls: base",
            "seed 82",
            "Ran out of calls: base",
            "all eight adapters",
            "Seed 82 recall: fact found / right",
        ],
        behaviour_rows,
    )
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
    out["sealed_ship_found_cd"] = " and ".join(
        f"found the fact in {runs[c]['behaviour'][SHIP]['recall_found_fact']} and answered "
        f"{runs[c]['behaviour'][SHIP]['recall_right_and_found']} right ({c})"
        for c in ("C", "D")
    )
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
    rows, peaks, shares = [], [], []
    for c in CONDITIONS:
        cost = runs[c]["cost"]
        b, s = cost["base"], cost[SHIP]
        per = [cost[a]["seconds_per_conversation"] for a in ADAPTERS]
        searches = [cost[a]["searches_per_conversation"] for a in ADAPTERS]
        share = 100 * s["tokens_read_per_turn"] / s["whole_chat_tokens"]
        shares.append(share)
        rows.append(
            f"| {c} | {b['seconds']}, {b['seconds_per_conversation']:.2f} "
            f"| {s['seconds']}, {s['seconds_per_conversation']:.2f} "
            f"| {min(per):.2f} to {max(per):.2f} "
            f"| {b['tokens_read_per_turn']:,.0f} / {s['tokens_read_per_turn']:,.0f} "
            f"| {s['whole_chat_tokens']:,.0f} | {share:.0f}% "
            f"| {b['tokens_written_per_turn']:.0f} / {s['tokens_written_per_turn']:.0f} "
            f"| {b['searches_per_conversation']:.2f} / {min(searches):.2f} to {max(searches):.2f} |"
        )
        peaks += [cost[a]["peak_vram_gib"] for a in ("base", *ADAPTERS)]
    out["cost_table"] = table(
        [
            "Condition",
            "Base: seconds, per conversation",
            "Seed 82: seconds, per conversation",
            "Eight adapters: seconds per conversation",
            "Tokens read per turn, base / seed 82",
            "Whole chat, tokens",
            "Seed 82 reads, share of the whole chat",
            "Tokens written per turn, base / seed 82",
            "Searches per conversation, base / eight adapters",
        ],
        rows,
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


# --- The outside-writer sets (R-146, R-157, R-164) ----------------------------------------------


def outside_writer_numbers(out) -> None:
    numbers = load(ANALYSIS / "R-164" / "writeup_numbers.json")
    recall_rows, kind_rows, claim_rows, prompt_rows, writer_rows, stage_rows = (
        [] for _ in range(6)
    )
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
        order = sorted(seeds.values())
        out[f"ow_82_place_{n}"] = (
            "the lowest of the eight"
            if seeds["82"] == order[0]
            else "inside the eight seeds' range"
        )
        recall_rows.append(
            f"| Set {n} | {prim['base']} | {prim['ship']} | {prim['only_base']}, "
            f"{prim['only_ship']}, p = {p_text(prim['p_exact_sign'])} "
            f"| {points(prim['chat_resampled_interval']['difference'])} "
            f"| {', '.join(str(seeds[str(s)]) for s in SEEDS)} | {points(pooled_interval)} |"
        )
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
        out[f"claims_82_true_{n}"] = str(c82["right_on_true"])
        out["claims_false_n"] = str(c82["false_claims"])
        out["claims_true_n"] = str(c82["true_claims"])
        pc = numbers["outside_writer_sets"][f"set_{n}"]["prompt_control"]
        cells = []
        for arm in ("base_prompta_vs_seed_82", "base_promptb_vs_seed_82"):
            t = pc[arm]
            cells.append(f"{t['only_first']}, {t['only_second']}, p = {p_text(t['p'])}")
        prompt_rows.append(
            f"| Set {n} | {models['base']['recall']} | {models['base_prompta']['recall']} "
            f"| {models['base_promptb']['recall']} | {models['seed_82']['recall']} | "
            + " | ".join(cells)
            + " |"
        )
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
        wv = blind["recall_on_questions_with_wrong_values"]
        out[f"ow_wrongvals_{n}"] = f"{wv['ship']} against {wv['base']} of {wv['items']}"
    out["ow_recall_table"] = table(
        [
            "Set",
            "Base",
            "6.37 seed 82",
            "Only base right, only seed 82 right, sign test",
            "Seed 82 gain, 95% interval resampling chats (points)",
            "Each seed (82, 83, 94 to 99)",
            "Eight seeds pooled, gain interval (points)",
        ],
        recall_rows,
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
        [
            "Set",
            "Base",
            "Base, prompt A (rules)",
            "Base, prompt B (rules and four worked examples)",
            "6.37 seed 82",
            "Prompt A against seed 82: only A right, only 6.37 right, sign test",
            "Prompt B against seed 82",
        ],
        prompt_rows,
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
        f"Kevin agreed with the scorer on {agree['agree']} of {agree['n']} lines (Cohen's kappa "
        f"{agree['kappa']}), and the scorer passed no reply he failed (R-144). A second marker "
        f"agreed with the scorer on {second['agree_with_scorer']} of {agree['n']} (kappa "
        f"{second['kappa_with_scorer']}) and with Kevin on {second['agree_with_kevin']} (kappa "
        f"{second['kappa_with_kevin']}) (R-145)"
    )
    if agree["kevin_wrong_scorer_right"]:
        raise SystemExit("the scorer passed a reply Kevin failed; the text says it never did")
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
        "6.31 plus 72 scripted in-view rows, one epoch on top (Kevin's call)",
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
        f"| {num or '—'} | {name} (`{label}`) | {change} | {end} | {screen(label)} "
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
        outside_writer_numbers,
        method_numbers,
        protocol_numbers,
        ledger_numbers,
        toolkit_numbers,
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
        out.write_text(
            re.sub(r"\{\{(\w+)\}\}", lambda m: values[m.group(1)], text), encoding="utf-8"
        )
        print(f"wrote {out.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
