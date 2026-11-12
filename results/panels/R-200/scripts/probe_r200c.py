import importlib.util, json, sys
from pathlib import Path
here = Path("scripts/records")
spec = importlib.util.spec_from_file_location("check_r199", here / "check_r199.py")
c = importlib.util.module_from_spec(spec); sys.modules["check_r199"] = c; spec.loader.exec_module(c)
rows = [json.loads(l) for l in Path("data/screens/k1_r178.jsonl").read_text(encoding="utf-8").splitlines()]
_, at = c.roles(rows)
for side, ctr in at.items(): print(side, sorted((n, v) for (n, _t), v in ctr.items()))
