"""Unblind one coherence sheet: paired counts overall and by kind.

Usage: python scripts/records/unblind.py <marks.json> <key.json>
"""

import json
import sys
from collections import defaultdict

from aya_retrieval.coherence import paired_counts

marks = {int(k): int(v) for k, v in json.load(open(sys.argv[1])).items()}
key = json.load(open(sys.argv[2]))
print(paired_counts(marks, key))
by_kind = defaultdict(lambda: [0, 0, 0])
for entry in key:
    by_kind[entry["kind"]][0 if entry["model"] == "base" else 1] += marks[entry["line"]]
    by_kind[entry["kind"]][2] += 1
print("  kind: base tuned pairs", {k: (v[0], v[1], v[2] // 2) for k, v in by_kind.items()})
