"""R-162: audit one sealed-run judge's transcript, then file its marks if the audit passes.

Usage: python scripts/records/audit_judge_r162.py SHEET JUDGE AGENT_ID

Why: R-154's frozen rule allows a judge's marks only from a fresh ``claude-sonnet-5-5`` agent that
read its own folder alone and decided every mark by reading. Before a judge's marks were filed, its
transcript was checked for: the model; every path any tool call touched, which must sit inside the
judge's own folder; every shell command, which may only be the heredoc that writes the marks or a
command that counts (no interpreter, no redirect); and marks that cover every line of the sheet's
key with 0 or 1. A judge that passes has its marks copied to ``results/coherence/R-162/judge``; one
that does not is printed as NOT FILED for a person to read (R-163, disclosure 2). This is the script
as run from the session's scratch folder, with its paths written in parts; the checks are unchanged.
"""

import json
import re
import shutil
import sys
from pathlib import Path

SESSION = "389594c2-8513-47d9-80f1-1a28b96837f7"
PROJECT = "C--Users-Gaming-Desktop-Claude-s-House"
SCRATCH = Path("C:/Users/Gaming/scratch/claude") / PROJECT / SESSION / "scratchpad"
SUBAGENTS = Path("C:/Users/Gaming/.claude/projects") / PROJECT / SESSION / "subagents"
REPO = Path(__file__).resolve().parents[2]
COHERENCE = REPO / "results/coherence/R-162"

sheet, judge, agent = sys.argv[1:4]
folder_name = f"judge_r162_{sheet}_{judge}"
transcript = SUBAGENTS / f"agent-{agent}.jsonl"
models, outside, code_like, calls = set(), [], [], 0
for line in transcript.open(encoding="utf-8"):
    event = json.loads(line)
    if event.get("type") != "assistant":
        continue
    message = event["message"]
    if message.get("model"):
        models.add(message["model"])
    for block in message.get("content") or []:
        if not (isinstance(block, dict) and block.get("type") == "tool_use"):
            continue
        if block["name"] == "SubagentHandback":
            continue
        calls += 1
        text = json.dumps(block["input"])
        paths = re.findall(r"[A-Za-z]:[\\/]+[^\"' ]+|/c/[^\"' ]+", text)
        for p in paths:
            if folder_name not in p.replace("\\\\", "\\"):
                outside.append((block["name"], p[:160]))
        if block["name"] in ("Bash", "PowerShell"):
            command = block["input"].get("command", "")
            first = command.strip().splitlines()[0] if command.strip() else ""
            heredoc = re.match(r"cat >\s*\"?[^\"]+\"? <<'EOF'", first)
            counting = not re.search(r"python|node|sed |awk|perl|for |while |>(?!&)", command)
            if heredoc or counting:
                print("    ok command:", ("heredoc " if heredoc else "count ") + first[:90])
            else:
                code_like.append(command[:300])
print(f"{sheet} {judge} {agent}: models {sorted(models)}, tool calls {calls}")
print("  paths outside its folder:", outside or "none")
print("  code-like commands:", code_like or "none")
marks_path = SCRATCH / folder_name / f"marks_{sheet}.json"
marks = json.loads(marks_path.read_text(encoding="utf-8"))
key = json.loads((COHERENCE / f"sheet_{sheet}" / "key.json").read_text(encoding="utf-8"))
expected = [str(k["line"]) for k in key]
ok = sorted(marks, key=int) == expected and set(marks.values()) <= {0, 1}
print(f"  marks: {len(marks)} lines, ones {sum(marks.values())}, covers every line: {ok}")
if ok and models == {"claude-sonnet-5-5"} and not outside and not code_like:
    out = COHERENCE / "judge"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(marks_path, out / f"marks_{sheet}_{judge}.json")
    print("  FILED", out / f"marks_{sheet}_{judge}.json")
else:
    print("  NOT FILED: needs a look")
