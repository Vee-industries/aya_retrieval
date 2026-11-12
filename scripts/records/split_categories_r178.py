"""R-178: split the S3 fact categories into those inside and outside the training lexicon.

A category in ``docs/heldout3/categories.md`` is inside when any of its keywords appears as a whole
word (or, for a keyword of several words, as a whole phrase) in any search query of the training set
``data/screens/fix17cs37.jsonl`` (6.37's set). Otherwise it is outside. Queries sit inside the
assistant turns as JSON strings; each one is parsed, as ``results/panels/R-178/count_queries.py``
reads them. Every user line (tool results excluded) is extracted too, and the keywords each
category shares with them are recorded beside the split, but they do not decide it.

Writes ``docs/heldout3/category_split.json`` and prints counts only.

Usage:
    python scripts/records/split_categories_r178.py
    python scripts/records/split_categories_r178.py --training PATH --categories PATH --out PATH
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TRAINING = REPO_ROOT / "data" / "screens" / "fix17cs37.jsonl"
CATEGORIES = REPO_ROOT / "docs" / "heldout3" / "categories.md"
OUT = REPO_ROOT / "docs" / "heldout3" / "category_split.json"
SEARCH_TOOL = "search_corpus"
TOOL_RESULT = "Tool result for "
ROW = re.compile(r"^\|\s*(C\d{2})\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")
# Letters, digits and apostrophes are word characters, so "cat" is not found in "can't" or "cats".
WORD_CHARS = "a-z0-9'"


def read_categories(path: Path) -> dict[str, dict]:
    """Return {id: {"description", "keywords"}} from the categories table."""
    categories = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match:
            cid, description, keywords = match.groups()
            words = [k.strip().casefold() for k in keywords.split(",") if k.strip()]
            categories[cid] = {"description": description, "keywords": words}
    if not categories:
        raise SystemExit(f"{path}: no category rows found")
    return categories


def _calls(content: str) -> list[dict]:
    try:
        calls = json.loads(content)
    except json.JSONDecodeError:
        return []
    if not isinstance(calls, list):
        return []
    return [c for c in calls if isinstance(c, dict) and c.get("tool_name") == SEARCH_TOOL]


def extract(path: Path) -> tuple[list[str], list[str]]:
    """Return every search query and every user line (tool results excluded) in the set."""
    queries, user_lines = [], []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        for turn in json.loads(line)["turns"]:
            content = str(turn.get("content", ""))
            if turn.get("role") == "assistant":
                for call in _calls(content):
                    query = call.get("parameters", {}).get("query")
                    if isinstance(query, str):
                        queries.append(query)
            elif turn.get("role") == "user" and not content.startswith(TOOL_RESULT):
                user_lines.append(content)
    return queries, user_lines


def has_word(text: str, keyword: str) -> bool:
    """Return True if ``keyword`` appears in ``text`` as a whole word or whole phrase."""
    pattern = rf"(?<![{WORD_CHARS}]){re.escape(keyword.casefold())}(?![{WORD_CHARS}])"
    return re.search(pattern, text.casefold()) is not None


def hits(keywords: list[str], texts: set[str]) -> list[str]:
    """Return the keywords found as whole words in any of ``texts``."""
    return [k for k in keywords if any(has_word(text, k) for text in texts)]


def split(categories: dict[str, dict], queries: list[str], user_lines: list[str]) -> dict:
    """Return the split: inside and outside ids, and per category the keywords that matched."""
    distinct_queries, distinct_lines = set(queries), set(user_lines)
    per_category = {}
    for cid, category in sorted(categories.items()):
        in_queries = hits(category["keywords"], distinct_queries)
        per_category[cid] = {
            "inside": bool(in_queries),
            "query_keywords": in_queries,
            "user_line_keywords": hits(category["keywords"], distinct_lines),
        }
    return {
        "inside": [cid for cid, c in per_category.items() if c["inside"]],
        "outside": [cid for cid, c in per_category.items() if not c["inside"]],
        "per_category": per_category,
    }


def sha256(path: Path) -> str:
    """SHA-256 of a text file with LF line endings, as git stores it."""
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--training", type=Path, default=TRAINING)
    parser.add_argument("--categories", type=Path, default=CATEGORIES)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()

    categories = read_categories(args.categories)
    queries, user_lines = extract(args.training)
    result = split(categories, queries, user_lines)

    def shown(path: Path) -> str:
        try:
            return path.resolve().relative_to(REPO_ROOT).as_posix()
        except ValueError:
            return path.as_posix()

    report = {
        "record": "R-178",
        "rule": "inside: any keyword appears as a whole word or phrase in any training search "
        "query; otherwise outside. User-line keywords are recorded and do not decide the split.",
        "training": shown(args.training),
        "training_sha256": sha256(args.training),
        "categories": shown(args.categories),
        "categories_sha256": sha256(args.categories),
        "queries": len(queries),
        "distinct_queries": len(set(queries)),
        "user_lines": len(user_lines),
        **result,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(
        f"queries {report['queries']} (distinct {report['distinct_queries']}), "
        f"user lines {report['user_lines']}"
    )
    print(
        f"categories {len(categories)}: inside {len(result['inside'])}, "
        f"outside {len(result['outside'])}"
    )


if __name__ == "__main__":
    main()
