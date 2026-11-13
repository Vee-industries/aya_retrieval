"""K4.6's training set (R-214): K4.5's build, with plain never_told rows searching a second time.

Usage: python scripts/records/build_k4_6.py

K4.5 (``build_k4_5.py``) passed hard_dev on seed 82 and bombed Demo2. On the outside-writer sets,
K4.1's older misses were mostly never found, and in 61 of 66 of those the model searched once, got
passages without the fact and stopped (R-214 lane). In training, a first search that returns text
without the fact is followed by another search in about 25 rows and by a decline in about 300.
K4.6 reruns K4.5's whole chain from K4.5's stripped writer copies with one change: the K3 writers'
never_told rows (not near_miss or other_person) whose first search returns text also run
``second_query``, and keep both searches when it returns text too (else one), then decline;
the balance and every other rule are K4.5's.
``scripts/records/check_k3.py --set k4_6_r214`` then checks the set.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

spec = importlib.util.spec_from_file_location("build_k4_5", HERE / "build_k4_5.py")
K45 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = K45
spec.loader.exec_module(K45)

if __name__ == "__main__":
    K45.DIR, K45.WRITERS = Path("data/screens/k4_6"), Path("data/screens/k4_6/writers")
    K45.OUT = Path("data/screens/k4_6_r214.jsonl")
    K45.main(record="R-214", never_told_twice=True)
