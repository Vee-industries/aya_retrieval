"""K4.3's training set (R-211): K4.2's build with only never_told rows added (no fact-row declines).

Usage: python scripts/records/build_k4_3.py

K4.2 (``build_k4_2.py``) bombed Demo2. Of its 57 new rows, 22 were fact rows (older, check_true,
check_false) that decline after two empty searches; 18 of the 20 that end empty ask about the user,
and train the model to give up on a fact that is in the chat (R-211 against lane). K4.3 runs K4.2's
build unchanged and keeps only the new never_told rows (near_miss rows are built as never_told).
``scripts/records/check_k3.py --set k4_3_r211`` then checks the set.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path("data/screens/k4_3_r211.jsonl")

spec = importlib.util.spec_from_file_location("build_k4_2", HERE / "build_k4_2.py")
K42 = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = K42
spec.loader.exec_module(K42)

if __name__ == "__main__":
    K42.main(out_path=OUT, record="R-211", kinds={"never_told"})
