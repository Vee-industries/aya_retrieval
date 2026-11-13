"""R-222 early stop: exit 1 if a seed's hard_dev fails a screening line (never_told >= 44, false retrieval <= 6.37's + 3).

Usage (from the repo, with the venv python): python hd_gate.py LABEL SEED
"""

import sys

sys.path.insert(0, "scripts/records")
import decide_r191 as d  # noqa: E402
from aya_retrieval.report_data import false_retrieval  # noqa: E402

label, seed = sys.argv[1], int(sys.argv[2])
hd = f"hd_{label}_{seed}"
nt = d.count(hd, 73157, ("never_told",))
fr = sum(h for h, _ in false_retrieval(hd, 73157).values())
ref = sum(h for h, _ in false_retrieval(f"hd_{d.REF}_{seed}", 73157).values())
ok = nt is not None and nt >= 44 and fr <= ref + 3
print(f"hd gate {hd}: never_told {nt} (at least 44), false retrieval {fr} (at most {ref + 3}): {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
