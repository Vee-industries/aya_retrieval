#!/usr/bin/env bash
# R-245 the second blend grid on seed 82: T6 and T4 blended at w = 0.33, 0.5, 0.67 (blend_adapters.py), hard_dev on each,
# then Demo2 once and Demo3 for the highest w that passes both hard_dev lines. Run under the card lock by
# qblend_lock.py; no push. Read files beside the log: t6t4blend_read2.txt, t6t4blend_read3.txt ("pass" or "bomb").
# A Demo3 pass stops the queue with BLEND PASSES DEMO3: seeds 83 and 94 then need T4's stage first (R-237).
set -u
S="$(cd "$(dirname "$0")" && pwd)"
W="/c/Users/Gaming/Desktop/hackathons/Lexsi Sprint"
VP="$W/venv/Scripts/python.exe"
cd "$W/aya_retrieval" || exit 1
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
ATTR="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
CAP=5400
VRAM=0.85  # R-232
A="$W/adapters/screens"
quiet() { grep -v -E "Redirects are currently|triton not found|Loading weights" | cut -c1-600; }
clean() { until ! git status --short --untracked-files=no | grep -q .; do echo "waiting for a clean tree $(date)"; sleep 60; done; }
have() { [ -s "results/recall_eval/$1.json" ]; }
fail() { echo "FAIL $1 $(date)"; touch "$S/t6t4blend_fail.flag"; exit 1; }
stop() { echo "== blend $1; blend done $(date)"; touch "$S/t6t4blend_done.flag"; exit 0; }

read_demo() {  # 2 or 3, label
  local OUT="results/demo2/branches_$2_82_demo$1.json"
  if [ ! -s "$OUT" ]; then
    clean; echo "== demo$1 $2_82 $(date)"
    timeout $CAP "$VP" scripts/run_demo2.py --demo-dir "demo$1" --adapter "$2=$A/$2_82" --out "$OUT" 2>&1 | quiet | tail -3
    [ -s "$OUT" ] || fail "demo$1"
    git add "$OUT" && git commit -q -m "Demo$1 on $2 seed 82 (R-245 blend)" -m "$ATTR" -- "$OUT"
  fi
  echo "DEMO$1 READY $(date)"
  until [ -s "$S/t6t4blend_read$1.txt" ]; do sleep 30; done
  local R; R=$(tr -d ' \r\n' < "$S/t6t4blend_read$1.txt"); echo "== demo$1 read: $R $(date)"
  [ "$R" = bomb ] && stop "bombs Demo$1"
  [ "$R" = pass ] || fail "read file holds $R"
}

rm -f "$S/t6t4blend_done.flag" "$S/t6t4blend_fail.flag"
echo "== blend start $(date)"
BEST=""
for TAG in 033 050 067; do
  LABEL="t6t4b${TAG}_r245"
  [ -s "$A/${LABEL}_82/adapter_model.safetensors" ] || CUDA_VISIBLE_DEVICES= "$VP" scripts/records/blend_adapters.py "$A/k13t6_r229_82" "$A/k13t4_r229_82" "0.${TAG#0}" "$A/${LABEL}_82" 2>&1 | quiet | tail -1
  [ -s "$A/${LABEL}_82/adapter_model.safetensors" ] || fail "blend $TAG"
  if ! have "hd_${LABEL}_82_seed_73157"; then
    clean; echo "== score hd_${LABEL}_82 $(date)"
    timeout $CAP "$VP" scripts/run_recall_eval.py --pool hard_dev --seed 73157 --items-per-kind 24 --index "C:/Users/Gaming/scratch/eval_blend2_hard_dev.sqlite" --label "hd_${LABEL}_82" --arms tool_loop --max-vram-fraction $VRAM --adapter "$A/${LABEL}_82" 2>&1 | quiet | tail -2
    have "hd_${LABEL}_82_seed_73157" || fail "hd $TAG"
    git add results && git commit -q -m "hd_${LABEL}_82 (R-245 blend)" -m "$ATTR"
  fi
  "$VP" "$S/hd_gate.py" "$LABEL" 82 2>&1 | grep "hd gate"
  "$VP" "$S/hd_gate.py" "$LABEL" 82 >/dev/null 2>&1 && BEST="$LABEL"
done
rm -f C:/Users/Gaming/scratch/eval_blend2_*.sqlite
[ -n "$BEST" ] || stop "fails hard_dev at every w"
echo "== highest w passing hard_dev: $BEST $(date)"
read_demo 2 "$BEST"
read_demo 3 "$BEST"
echo "BLEND PASSES DEMO3 $BEST $(date)"; touch "$S/t6t4blend_done.flag"
