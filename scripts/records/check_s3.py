"""R-178: mechanical checks over the written S3 set; prints counts and reasons, never chat text.

Runs every rule of ``docs/heldout3/BRIEF.md`` through ``aya_retrieval.heldout3.load_s3`` and prints:
chats found and kept per writer, every dropped chat and question with its reason, the batch reasons
(chats per writer, confirm balance), items per view and kind, older questions inside and outside
the training lexicon, never_told plain and overlap, and the set's sha256. It also checks that the
brief's lists A and B are the committed split's outside and inside categories. Reasons name ids,
counts and field names only. Exits 1 if anything was dropped or any batch rule or list check fails.

Usage:
    python scripts/records/check_s3.py [--items-dir PATH] [--brief PATH] [--split PATH]
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

from aya_retrieval.heldout3 import CHATS_DIR, OLDER, REPO_ROOT, SPLIT_FILE, load_s3, load_split

BRIEF = REPO_ROOT / "docs" / "heldout3" / "BRIEF.md"
LIST_HEADING = re.compile(r"^### List ([AB])\s*$")
LIST_LINE = re.compile(r"^- (C\d{2}): ")


def brief_lists(path: Path) -> dict[str, set[str]]:
    """Return the category ids under the brief's "### List A" and "### List B" headings."""
    lists: dict[str, set[str]] = {"A": set(), "B": set()}
    current = None
    for line in path.read_text(encoding="utf-8").splitlines():
        heading = LIST_HEADING.match(line)
        if heading:
            current = heading.group(1)
            continue
        if line.startswith("#"):
            current = None
            continue
        entry = LIST_LINE.match(line)
        if entry and current:
            lists[current].add(entry.group(1))
    return lists


def report(items_dir: Path, brief: Path, split_path: Path) -> tuple[list[str], bool]:
    """Return the lines to print and whether every check passed."""
    split = load_split(split_path)
    items, dropped, batch, digest = load_s3(items_dir, split)
    lines, ok = [], True
    found = sorted(p.stem for p in items_dir.glob("*.json"))
    lines.append(f"chat files {len(found)}")
    chats_dropped = [(cid, why) for cid, why in dropped if "_q" not in cid]
    questions_dropped = [(qid, why) for qid, why in dropped if "_q" in qid]
    kept = Counter(writer for _, writer in {(s3.chat_id, s3.writer) for s3 in items})
    lines.append("chats kept per writer " + ", ".join(f"{w} {n}" for w, n in sorted(kept.items())))
    lines.append(f"chats dropped {len(chats_dropped)}")
    lines += [f"  {cid}: {why}" for cid, why in chats_dropped]
    lines.append(f"questions dropped {len(questions_dropped)}")
    lines += [f"  {qid}: {why}" for qid, why in questions_dropped]
    lines.append(f"batch problems {len(batch)}")
    lines += [f"  {why}" for why in batch]
    by_kind = Counter((s3.view, s3.item.kind) for s3 in items)
    lines.append("items " + ", ".join(f"{v}/{k} {n}" for (v, k), n in sorted(by_kind.items())))
    older = Counter(
        "inside" if s3.inside else "outside"
        for s3 in items
        if s3.view == "right" and s3.item.kind == OLDER
    )
    lines.append(f"older (right view): inside {older['inside']}, outside {older['outside']}")
    variants = Counter(s3.variant for s3 in items if s3.view == "right" and s3.variant)
    lines.append(f"never_told (right view): {dict(sorted(variants.items()))}")
    lists = brief_lists(brief)
    lists_ok = lists["A"] == set(split.outside) and lists["B"] == set(split.inside)
    lines.append(
        f"brief lists: A {len(lists['A'])}, B {len(lists['B'])}; "
        f"match the split's outside and inside: {lists_ok}"
    )
    lines.append(f"set sha256 {digest}")
    ok = not dropped and not batch and lists_ok
    return lines, ok


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--items-dir", type=Path, default=CHATS_DIR)
    parser.add_argument("--brief", type=Path, default=BRIEF)
    parser.add_argument("--split", type=Path, default=SPLIT_FILE)
    args = parser.parse_args()
    lines, ok = report(args.items_dir, args.brief, args.split)
    print("\n".join(lines))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
