"""R-178: draw S3's coherence sample by the sealed seed, at unsealing.

Picks ``heldout3.SAMPLE_SIZE`` (120) item ids from every S3 item, both views, with
``random.Random(heldout3.SAMPLE_SEED)`` over the ids in sorted order, so the sample is fixed by the
seal and not chosen by anyone. The judges score the replies of these items under R-154's coherence
rule. Needs ``--final``, since loading the set opens it. Writes ids only, and prints the count.

Usage:
    python scripts/records/draw_s3_sample.py --final [--items-dir PATH] [--out PATH]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from aya_retrieval.heldout3 import (
    CHATS_DIR,
    REPO_ROOT,
    SAMPLE_SEED,
    SAMPLE_SIZE,
    SPLIT_FILE,
    draw_sample,
    load_s3,
    load_split,
)

OUT = REPO_ROOT / "results" / "s3" / "coherence_sample.json"


def sample(items_dir: Path, split_path: Path) -> dict:
    """Return the sample record: the seed, the size, the set's hash and the drawn ids."""
    items, _, _, digest = load_s3(items_dir, load_split(split_path))
    ids = draw_sample(items)
    return {
        "record": "R-178",
        "seed": SAMPLE_SEED,
        "size": SAMPLE_SIZE,
        "items_sha256": digest,
        "drawn_from": len(items),
        "ids": ids,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--items-dir", type=Path, default=CHATS_DIR)
    parser.add_argument("--split", type=Path, default=SPLIT_FILE)
    parser.add_argument("--out", type=Path, default=OUT)
    parser.add_argument("--final", action="store_true", help="needed: S3 is sealed")
    args = parser.parse_args()
    if not args.final:
        parser.error("S3 is sealed: drawing the sample needs --final")
    record = sample(args.items_dir, args.split)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
    print(f"drew {len(record['ids'])} of {record['drawn_from']} items; wrote {args.out}")


if __name__ == "__main__":
    main()
