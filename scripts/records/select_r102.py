"""R-102: choose the held-out correction wordings from the blind agent's list.

Usage: python scripts/records/select_r102.py

The agent saw no project file and wrote 25 openings and 25 endings, most common first, then 25
more openings when the first 25 gave fewer than six
(``results/stress/R-102/blind_wordings.json``). The held-out set is the first six of each that
shares no content word with training's correction wordings (``stress.shares_wording``). It is
written to ``src/aya_retrieval/corrections_heldout.json``, which ``stress.corrected_heldout`` reads.
"""

import json
from pathlib import Path

from aya_retrieval.stress import (
    HELDOUT_CORRECTIONS,
    TRAIN_CORRECTION_ENDINGS,
    TRAIN_CORRECTION_OPENINGS,
    shares_wording,
)

BLIND = Path("results/stress/R-102/blind_wordings.json")
KEEP = 6

blind = json.loads(BLIND.read_text(encoding="utf-8"))
training = (*TRAIN_CORRECTION_OPENINGS, *TRAIN_CORRECTION_ENDINGS)
chosen = {}
for part in ("openings", "endings"):
    kept = [w for w in blind[part] if not shares_wording(w, training)][:KEEP]
    if len(kept) < KEEP:
        raise SystemExit(f"only {len(kept)} {part} share no word with training's")
    chosen[part] = kept
HELDOUT_CORRECTIONS.write_text(json.dumps(chosen, indent=1) + "\n", encoding="utf-8")
for part, kept in chosen.items():
    print(part, kept)
