"""Read-only: K3's own older questions, found (names_value) by person me vs others, using build_k3.chat_rows."""
import importlib.util, json, sys
from collections import Counter
from pathlib import Path
LANE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("bk3", "scripts/records/build_k3.py")
B = importlib.util.module_from_spec(spec); sys.modules["bk3"] = B; spec.loader.exec_module(B)
c = Counter()
for p in sorted(Path("data/screens/k3_writers").glob("*.json")):
    for i, chat in enumerate(json.loads(p.read_text(encoding="utf-8"))["chats"]):
        for r in B.chat_rows(p.stem, i, chat, LANE):
            m = r.get("meta", {})
            if m.get("kind") in ("older", "never_told") and "names_value" in m:
                who = "me" if (m.get("person") or "").lower() == "me" else "other"
                c[(m["kind"], who, "value" if m["names_value"] else "decline", m["searches"])] += 1
for f in LANE.glob("*.sqlite"):
    f.unlink()
for k, v in sorted(c.items()):
    print(k, v)
