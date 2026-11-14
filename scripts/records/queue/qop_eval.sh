#!/usr/bin/env bash
# R-253: run K1.3's seed 82, 83 and 94 adapters over the on-policy training-chat items (data/onpolicy/items),
# under the card lock (qop_eval_lock.py). Log: qop_eval.log beside this file.
set -u
S="$(cd "$(dirname "$0")" && pwd)"
W="/c/Users/Gaming/Desktop/hackathons/Lexsi Sprint"
VP="$W/venv/Scripts/python.exe"
cd "$W/aya_retrieval" || exit 1
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
ATTR="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
clean() { until ! git status --short --untracked-files=no | grep -q .; do echo "waiting for a clean tree $(date)"; sleep 60; done; }
for SEED in 82 83 94; do
  L="op_k13_$SEED"
  [ -s "results/recall_eval/${L}_seed_0.json" ] && { echo "== have $L"; continue; }
  clean; echo "== score $L $(date)"
  timeout 5400 "$VP" scripts/run_recall_eval.py --seed 0 --items-dir data/onpolicy/items --index "C:/Users/Gaming/scratch/eval_op.sqlite" --label "$L" --arms tool_loop --max-vram-fraction 0.85 --adapter "$W/adapters/screens/k1_3_r200_$SEED" 2>&1 | grep -v -E "Redirects|triton" | tail -2
  [ -s "results/recall_eval/${L}_seed_0.json" ] || { echo "FAIL $L $(date)"; exit 1; }
  git add results && git commit -q -m "$L: K1.3 seed $SEED on the on-policy items (R-253)" -m "$ATTR"
  echo "OP EVAL DONE $SEED $(date)"
done
rm -f C:/Users/Gaming/scratch/eval_op.sqlite
echo "== qop_eval done $(date)"
