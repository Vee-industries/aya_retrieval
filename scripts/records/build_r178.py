"""R-178: candidate K1's training set, 6.37's rows (fix17cs37) with F2 and F3, as k1_r178.

Usage: python scripts/records/build_r178.py --index C:/scratch/build_r178.sqlite

K1 = F2 + F3 on 6.37's own set, so every other part of 6.37's set stays as it was:

- Each row's conversation is rebuilt from its seed: the training builder's runs that made 6.37's
  rows (``brief_chat`` at seed 71119, the statement spares at 71120, 71127 and 71128) and R-102's
  appended rows (``build_r102.py``). A row counts as rebuilt only if the rebuilt conversation
  renders to the row's own turns byte for byte. The 124 spliced rows (``indirect/``, ``facts/``,
  ``contrast/``) have no seed and are kept as they are.
- F2: every rebuilt chat gains 2 to 4 facts of other types out of view
  (``conversations.add_other_facts``), the rows of each kind in three equal shares
  (``OTHER_FACT_SHARES``), decoys as 6.37 drew them, so the number of passages a search returns
  still does not tell found from not found (R-020). ``never_told`` rows are kept only when the
  search returns passages; one that returns none is replaced by a fresh scripted ``never_told``
  row of the same share. Values in the returned passages other than the answer join the
  forbidden values.
- F3: 30% of the rows of each kind, drawn from the rebuilt base-build rows, gain 1 or 2 earlier
  questions with replies in view (``stress.earlier_answers``), and 50 more ``older`` and
  ``confirm`` rows are re-asks: their own question answered wrong in view. Values the earlier
  replies give join the forbidden values.

No model runs. A row keeps its own 6.37 target when that target still passes the scorer against
the new forbidden values (a statement target must also name no earlier value); otherwise a found
fact gets the scripted answer, a search that no longer finds the fact gets the scripted "not
found" reply, and a row that fits neither keeps 6.37's turns as they were. Row order and ids are
6.37's; replacements take the place of the row they replace.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import importlib.util
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

from agenttune.agentic.rollout_engines.rollout_factory import DEFAULT_TOOL_RESULT_FORMAT
from transformers import AutoTokenizer

from aya_retrieval.conversations import (
    CONFIRM,
    IN_VIEW,
    ITEM_KINDS,
    NEEDS_SEARCH,
    NEVER_TOLD,
    OLDER,
    OTHER_FACT_SHARES,
    STATEMENT,
    build_item,
)
from aya_retrieval.demonstrations import demonstration_turns, values_named
from aya_retrieval.models import MODEL_ID, MODEL_REVISION
from aya_retrieval.pools import TRAIN
from aya_retrieval.provenance import run_metadata
from aya_retrieval.recall_tool import build_recall_tool, search_finds_fact
from aya_retrieval.scoring import item_correct
from aya_retrieval.stress import earlier_answers
from aya_retrieval.tool_prompt import SEARCH_TOOL_NAME

SCRIPTS = Path(__file__).resolve().parents[1]
DATA = Path("data/screens")
BASE_SET, OUT = DATA / "fix17cs37.jsonl", DATA / "k1_r178.jsonl"
# The training builder's runs whose rows 6.37's set keeps (their provenance files), and the kinds
# each built; every one ran with --more-indirect --more-chat.
BUILDS = ((71119, ITEM_KINDS), (71120, (STATEMENT,)), (71127, (STATEMENT,)), (71128, (STATEMENT,)))
MAX_ATTEMPTS = 4000
F3_SHARE = 0.30
REASK_ROWS = {OLDER: 25, CONFIRM: 25}
SELECT_SEED = 178_000
FRESH_SEED = 178_100_000


def load_script(path: Path):
    """Import a script by path, for its constants and functions."""
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


BUILDER = load_script(SCRIPTS / "run_build_training_set.py")
R102 = load_script(SCRIPTS / "records" / "build_r102.py")


@dataclasses.dataclass
class Source:
    """How a row's conversation is rebuilt: its build arguments, and R-102's change if any."""

    seed: int
    decoys: int
    query: str
    builder: bool
    r102: str | None = None


def row_query(row: dict) -> str | None:
    """Return the query of a row's search call, or None for a row with no search."""
    if row["kind"] not in NEEDS_SEARCH:
        return None
    return json.loads(row["turns"][7]["content"])[0]["parameters"]["query"]


def tool_turn(output: str) -> str:
    return DEFAULT_TOOL_RESULT_FORMAT.format(name=SEARCH_TOOL_NAME, content=output)


def builder_item(row_id: str, kind: str, source: Source, share: str | None = None):
    """Return the builder's conversation for a row, with F2 in ``share`` if given."""
    item = build_item(
        row_id,
        source.seed,
        BUILDER.SIZE,
        kind,
        "train",
        source.decoys,
        True,
        False,
        True,
        other_facts=share,
    )
    return dataclasses.replace(item, query=source.query) if source.query else item


def search(item, query: str, index: Path) -> tuple[str, bool]:
    tool = build_recall_tool(item, index, match_all=False)
    return tool.execute(query).output, search_finds_fact(tool, item, query)


def find_builder_sources(rows: list[dict], index: Path) -> dict[str, Source]:
    """Return the seed and decoys of every row the training builder made, checked byte for byte."""
    wanted = defaultdict(list)
    for row in rows:
        if "/" not in row["id"]:
            wanted[tuple(t["content"] for t in row["turns"][:7])].append(row)
    sources = {}
    for build_seed, kinds in BUILDS:
        for kind in kinds:
            offset = BUILDER.kind_seed_offset(kind)
            for attempt in range(MAX_ATTEMPTS):
                seed = build_seed + offset + attempt
                for decoys in BUILDER.DECOY_CHOICES[kind]:
                    item = build_item(
                        "x", seed, BUILDER.SIZE, kind, "train", decoys, True, False, True
                    )
                    key = tuple(c for pair in item.view() for c in pair) + (item.message,)
                    for row in wanted.get(key, ()):
                        if row["id"] in sources or row["kind"] != kind:
                            continue
                        source = Source(seed, decoys, row_query(row) or "", True)
                        if rebuilt_turns(row, source, index) == row["turns"]:
                            sources[row["id"]] = source
    return sources


def rebuilt_turns(row: dict, source: Source, index: Path) -> list[dict]:
    """Return the turns a source rebuilds for a row, with the row's own target."""
    item = builder_item(row["id"], row["kind"], source)
    target = row["turns"][-1]["content"]
    if row["kind"] not in NEEDS_SEARCH:
        return demonstration_turns(item, "", target, False, target)
    output, found = search(item, source.query, index)
    return demonstration_turns(item, output, target, found, target)


def r102_rows(index: Path, tokenizer):
    """Yield R-102's appended rows as its build made them: kind name, seed, item, change, turns."""
    rng = random.Random(R102.FIRST_SEED)
    seed = R102.FIRST_SEED
    for kind_name, wanted in R102.COUNTS.items():
        made = 0
        while made < wanted:
            seed += 1
            built = R102.make(kind_name, made, seed, rng)
            if not built:
                continue
            item, fixed, needed = built
            output = build_recall_tool(fixed, index, match_all=False).execute(fixed.query).output
            if not all(value in output for value in needed):
                continue
            turns = demonstration_turns(fixed, output, fixed.reply, True, TRAIN.unknown_replies[0])
            if R102.row_tokens(turns, tokenizer) > R102.MAX_ROW_TOKENS:
                continue
            yield kind_name, seed, item, fixed, turns
            made += 1


def with_r102_change(plain, changed, other):
    """Return R-102's changed conversation with F2's added lines from ``other`` copied in.

    ``plain`` is R-102's conversation before its change and ``other`` the same with F2; an added
    line goes in only where R-102's change left the exchange as it was.
    """
    exchanges = list(changed.exchanges)
    for slot, (before, after) in enumerate(zip(plain.exchanges, other.exchanges, strict=True)):
        if before != after and changed.exchanges[slot] == before:
            exchanges[slot] = after
    return dataclasses.replace(changed, exchanges=tuple(exchanges))


def names_any(reply: str, values) -> bool:
    return any(value.casefold() in reply.casefold() for value in values)


def k1_turns(row: dict, item, earlier: tuple[str, ...], found_before: bool, index: Path, tally):
    """Return a row's K1 turns for its changed conversation, or None if no target fits.

    ``earlier`` are the values the earlier replies in view give; ``found_before`` is whether the
    row's 6.37 search found its fact.
    """
    kind, target = row["kind"], row["turns"][-1]["content"]
    if kind not in NEEDS_SEARCH:
        if kind == IN_VIEW and not item_correct(kind, target, item.answer, item.forbidden, 0):
            target = item.reply
            if not item_correct(kind, target, item.answer, item.forbidden, 0):
                return None
            tally["in_view_scripted_target"] += 1
        if names_any(target, earlier):
            return None
        return demonstration_turns(item, "", target, False, target)
    output, found = search(item, item.query, index)
    passed = values_named(output, "train", item.answer)
    item = dataclasses.replace(item, forbidden=tuple(dict.fromkeys((*item.forbidden, *passed))))
    if kind == NEVER_TOLD:
        if "chunk_id=" not in output or not item_correct(kind, target, "", item.forbidden, 1):
            return None
        return demonstration_turns(item, output, target, False, target)
    if found:
        if not (found_before and item_correct(kind, target, item.answer, item.forbidden, 1)):
            target = item.reply
            if not item_correct(kind, target, item.answer, item.forbidden, 1):
                return None
            tally[f"{kind}_scripted_target"] += 1
    elif found_before:
        target = random.Random(hash_seed(row["id"])).choice(TRAIN.unknown_replies)
        tally[f"{kind}_now_missed"] += 1
    return demonstration_turns(item, output, target, found, target)


def hash_seed(text: str) -> int:
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:12], 16)


def f2_shares(rows: list[dict], rebuilt) -> dict[str, str]:
    """Give the rebuilt rows of each kind the three shares in turn, in row order."""
    shares, made = {}, Counter()
    for row in rows:
        if row["id"] in rebuilt:
            shares[row["id"]] = OTHER_FACT_SHARES[made[row["kind"]] % 3]
            made[row["kind"]] += 1
    return shares


def fresh_never_told(n: int, share: str, index: Path, tokenizer):
    """Return a fresh scripted never_told row in ``share`` whose search returns passages."""
    seed = FRESH_SEED + 1000 * n
    while True:
        seed += 1
        decoys = random.Random(seed).choice(BUILDER.DECOY_CHOICES[NEVER_TOLD])
        item = build_item(
            f"k1/never_told_{n:04d}",
            seed,
            BUILDER.SIZE,
            NEVER_TOLD,
            "train",
            decoys,
            True,
            False,
            True,
            other_facts=share,
        )
        output, _ = search(item, item.query, index)
        turns = demonstration_turns(item, output, item.reply, False, item.reply)
        if "chunk_id=" in output and BUILDER.row_tokens(turns, tokenizer) <= BUILDER.MAX_ROW_TOKENS:
            return {"id": item.item_id, "kind": NEVER_TOLD, "turns": turns}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--index", type=Path, required=True, help="scratch search database")
    parser.add_argument("--out", type=Path, default=OUT, help="where to write the set")
    args = parser.parse_args()
    provenance = run_metadata()
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, revision=MODEL_REVISION)
    base_text = BASE_SET.read_text(encoding="utf-8")
    rows = [json.loads(line) for line in base_text.splitlines()]
    by_id = {row["id"]: row for row in rows}
    tally = Counter()

    sources = find_builder_sources(rows, args.index)
    r102 = {}
    for kind_name, seed, plain, fixed, turns in r102_rows(args.index, tokenizer):
        row = by_id.get(fixed.item_id)
        if row and row["turns"] == turns:
            decoys = next(
                d
                for d in (0, 1, 2, 3)
                if build_item(plain.item_id, seed, R102.SIZE, plain.kind, "train", d).exchanges
                == plain.exchanges
            )
            r102[fixed.item_id] = (kind_name, seed, decoys, plain, fixed)
    tally["rebuilt_builder_rows"] = len(sources)
    tally["rebuilt_r102_rows"] = len(r102)
    tally["kept_as_they_were"] = len(rows) - len(sources) - len(r102)

    # Whether each search row's 6.37 search found its fact; R-102 kept only rows that did.
    found_before = dict.fromkeys(r102, True)
    for row in rows:
        if row["id"] in sources and row["kind"] in NEEDS_SEARCH:
            item = builder_item(row["id"], row["kind"], sources[row["id"]])
            found_before[row["id"]] = search(item, item.query, args.index)[1]

    shares = f2_shares(rows, {*sources, *r102})

    def f2_item(row):
        """Return the row's conversation with F2, or None for a row kept as it was."""
        if row["id"] in sources:
            share = shares[row["id"]]
            return builder_item(row["id"], row["kind"], sources[row["id"]], share), share
        if row["id"] in r102:
            _, seed, decoys, plain, fixed = r102[row["id"]]
            share = shares[row["id"]]
            other = build_item(
                plain.item_id, seed, R102.SIZE, plain.kind, "train", decoys, other_facts=share
            )
            return with_r102_change(plain, fixed, other), share
        return None, None

    # F3 picks: 30% of each kind's rows, from the rebuilt base-build rows, plus the re-asks.
    pick_rng = random.Random(SELECT_SEED)
    kinds = Counter(row["kind"] for row in rows)
    quota = {kind: round(F3_SHARE * kinds[kind]) for kind in ITEM_KINDS}
    order = {
        kind: pick_rng.sample(
            [r["id"] for r in rows if r["kind"] == kind and r["id"] in sources],
            sum(1 for r in rows if r["kind"] == kind and r["id"] in sources),
        )
        for kind in ITEM_KINDS
    }

    out, f2_items = {}, {}
    for row in rows:
        item, share = f2_item(row)
        if item is None:
            out[row["id"]] = row
            continue
        turns = k1_turns(row, item, (), found_before.get(row["id"], False), args.index, tally)
        if turns is None and row["kind"] == NEVER_TOLD:
            replaced = tally["never_told_no_passages_replaced"]
            tally["never_told_no_passages_replaced"] += 1
            out[row["id"]] = fresh_never_told(replaced, share, args.index, tokenizer)
            tally[f"{row['kind']}_share_{share}"] += 1
            continue
        if turns is None or BUILDER.row_tokens(turns, tokenizer) > BUILDER.MAX_ROW_TOKENS:
            tally[f"{row['kind']}_f2_not_applied"] += 1
            out[row["id"]] = row
            continue
        out[row["id"]] = {"id": row["id"], "kind": row["kind"], "turns": turns}
        tally[f"{row['kind']}_f2"] += 1
        tally[f"{row['kind']}_share_{share}"] += 1
        if row["id"] in sources:
            f2_items[row["id"]] = item

    reply_kinds, with_f3 = Counter(), set()
    for kind in ITEM_KINDS:
        for reask, wanted in ((True, REASK_ROWS.get(kind, 0)), (False, quota[kind])):
            made = 0
            for row_id in order[kind]:
                if made == wanted:
                    break
                if row_id not in f2_items or row_id in with_f3:
                    continue
                changed = earlier_answers(f2_items[row_id], sources[row_id].seed, "train", reask)
                if changed is None:
                    continue
                item, used, earlier = changed
                if reask and not search(item, item.query, args.index)[1]:
                    tally[f"{kind}_reask_missed"] += 1
                    continue
                found = found_before.get(row_id, False)
                turns = k1_turns(by_id[row_id], item, earlier, found, args.index, tally)
                if turns is None or BUILDER.row_tokens(turns, tokenizer) > BUILDER.MAX_ROW_TOKENS:
                    tally[f"{kind}_f3_unfit"] += 1
                    continue
                out[row_id] = {"id": row_id, "kind": kind, "turns": turns}
                with_f3.add(row_id)
                reply_kinds.update(f"{kind}_{used_kind}" for used_kind in used)
                made += 1
            tally[f"{kind}_{'reask' if reask else 'f3'}"] = made

    final = [out[row["id"]] for row in rows]
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in final)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text, encoding="utf-8")
    args.index.unlink(missing_ok=True)
    report = {
        "provenance": provenance,
        "base_set": BASE_SET.as_posix(),
        "base_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "out_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "rows": len(final),
        "kinds": dict(Counter(row["kind"] for row in final)),
        "f3_quota": quota,
        "reask_rows": REASK_ROWS,
        "earlier_reply_kinds": dict(reply_kinds),
        "tally": dict(tally),
    }
    args.out.with_suffix(".provenance.json").write_text(
        json.dumps(report, indent=1), encoding="utf-8"
    )
    print(f"{args.out}: {len(final)} rows; {report['kinds']}; {dict(tally)}")


if __name__ == "__main__":
    main()
