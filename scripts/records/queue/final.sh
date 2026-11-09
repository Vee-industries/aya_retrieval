# R-162: the sealed final run (R-016, R-038, R-039, R-041); sourced by a backlog line inside runner2.sh.
FINAL_SEED=90311
final_check() {  # stop every sealed run unless the freeze holds (R-154, R-160)
  if "$VP" scripts/records/freeze_r154.py check results/freeze/sealed_manifest.json \
      --adapter "$W/adapters/screens/fix17cs37_82" 2>&1 | grep -q "every frozen file and value matches"; then
    echo "== freeze check passes $(date)"
  else
    echo "== FREEZE CHECK FAILS $(date)"; touch "$S/r162_stop"
  fi
}
final() {  # condition letter, pool, decoys, model label, adapter dir or "base"
  local label="final_$1_$4" out="results/recall_eval/final_$1_$4_seed_$FINAL_SEED.json"
  have "${label}_seed_$FINAL_SEED" && { echo "== have $label"; return 0; }
  local adapter=(); [ "$5" = base ] || adapter=(--adapter "$5")
  for try in 1 2 3; do
    clean
    echo "== final $label try $try $(date)"
    "$VP" scripts/run_recall_eval.py --final --pool "$2" --decoys "$3" --seed "$FINAL_SEED" --items-per-kind 30 \
      --index "C:/Users/Gaming/scratch/eval_final_$2_$3.sqlite" --label "$label" --arms tool_loop \
      --max-vram-fraction 0.85 "${adapter[@]}" 2>&1 | quiet | tail -n 3
    [ -s "$out" ] && break
    sleep 30
  done
  [ -s "$out" ] || { echo "NO RESULTS $label"; return 1; }
  git add "$out" && git commit -q -m "$label (R-162 sealed final run)" -m "$ATTR"; push
}
final_all() {  # condition letter, pool, decoys: base, then the eight 6.37 seeds
  final "$1" "$2" "$3" base base || return 1
  for s in 82 83 94 95 96 97 98 99; do
    final "$1" "$2" "$3" "fix17cs37_$s" "$W/adapters/screens/fix17cs37_$s" || return 1
  done
}
