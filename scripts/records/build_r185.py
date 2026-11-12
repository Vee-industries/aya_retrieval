"""R-185: candidate K2's training set, K1's build with half its same_person never_told rows moved.

Usage: python scripts/records/build_r185.py --index C:/scratch/build_r185.sqlite

K2 = K1 (``build_r178.py``) with one change, in the F2 shares: the never_told rows K1 gives the
``same_person`` share are taken in row order, and the 2nd, 4th, 6th and so on get ``same_type``
instead. They keep a decline target; the build's own fallback replaces any never_told row whose
search returns no passages. Every other row, share, F3 pick and seed is K1's code unchanged.
``scripts/records/check_r185.py`` then checks the set before any training.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path("data/screens/k2_r185.jsonl")


def load_k1_build():
    spec = importlib.util.spec_from_file_location("build_r178", HERE / "build_r178.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module  # dataclasses look the module up by name
    spec.loader.exec_module(module)
    return module


K1 = load_k1_build()
k1_shares = K1.f2_shares


def k2_shares(rows, rebuilt) -> dict[str, str]:
    """K1's shares, with every second same_person never_told row given same_type."""
    shares = k1_shares(rows, rebuilt)
    moved = 0
    for row in rows:
        if row["kind"] == K1.NEVER_TOLD and shares.get(row["id"]) == "same_person":
            if moved % 2:
                shares[row["id"]] = "same_type"
            moved += 1
    return shares


if __name__ == "__main__":
    K1.f2_shares = k2_shares
    if "--out" not in sys.argv:
        sys.argv += ["--out", str(OUT)]
    K1.main()
