#!/usr/bin/env bash
# S3 queue (R-178, R-191, R-193): opened once, after the pick is committed. Usage: qs3.sh PICK (K1 or K1.3).
# Baselines first, then 6.37 at 82/83/94, the shippable arm at 82/83/94, the report arms at 82/83.
# Each result is committed as it lands; no push. Under the card lock by qs3_lock.py; log qs3.log.
set -u
S="$(cd "$(dirname "$0")" && pwd)"
W="/c/Users/Gaming/Desktop/hackathons/Lexsi Sprint"
VP="$W/venv/Scripts/python.exe"
A="$W/adapters/screens"
cd "$W/aya_retrieval" || exit 1
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
ATTR="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
declare -A DIR=([6.37]=fix17cs37 [K1]=k1_r178 [K1.3]=k1_3_r200 [K2.1]=k2_1_r187 [C1]=k13opc1_r263)  # R-280: C1 added
PICK="${1:?PICK}"; [ -n "${DIR[$PICK]:-}" ] || { echo "unknown pick $PICK"; exit 1; }
quiet() { grep -v -E "Redirects are currently|triton not found|Loading weights" | cut -c1-400; }
clean() { until ! git status --short --untracked-files=no | grep -q .; do echo "waiting for a clean tree $(date)"; sleep 60; done; }
fail() { echo "FAIL $1 $(date)"; touch "$S/qs3_fail.flag"; exit 1; }
run() {  # label, then run_s3_eval arguments
  local label="$1"; shift
  [ -s "results/s3/$label.json" ] && { echo "== have $label"; return; }
  clean; echo "== s3 $label $(date)"
  timeout 14400 "$VP" scripts/run_s3_eval.py --final --index "C:/Users/Gaming/scratch/s3_eval.sqlite" \
    --label "$label" --max-vram-fraction 0.85 "$@" 2>&1 | quiet | tail -6
  [ -s "results/s3/$label.json" ] || fail "$label"
  git add results/s3 && git commit -q -m "S3 $label" -m "$ATTR" -- results/s3 || fail "commit $label"
}
adapter() { run "s3_${DIR[$1]}_$2" --arm tool --adapter "$A/${DIR[$1]}_$2"; }
run s3_always_search --arm always_search
run s3_whole_chat --arm whole_chat
run s3_base_tool --arm tool
for seed in 82 83 94; do adapter 6.37 $seed; done
for seed in 82 83 94; do adapter "$PICK" $seed; done
for name in K1 K1.3 K2.1; do [ "$name" = "$PICK" ] && continue; for seed in 82 83; do adapter $name $seed; done; done
echo "== qs3 done $(date)"; touch "$S/qs3_done.flag"
