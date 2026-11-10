# R-164: base with the whole chat in view, report only; sourced by a backlog line inside runner2.sh.
wcrun() {  # label, then run_recall_eval.py arguments (seed, pool or items, index)
  local label="$1" seed="$3"; shift
  local out="results/recall_eval/${label}_seed_$seed.json"
  have "${label}_seed_$seed" && { echo "== have $label"; return 0; }
  for try in 1 2 3; do
    clean
    echo "== whole chat $label try $try $(date)"
    "$VP" scripts/run_recall_eval.py "$@" --label "$label" --arms whole_chat --max-vram-fraction 0.85 2>&1 | quiet | tail -n 3
    [ -s "$out" ] && break
    sleep 30
  done
  [ -s "$out" ] || { echo "NO RESULTS $label"; return 1; }
  git add "$out" && git commit -q -m "$label (R-164 whole-chat control)" -m "$ATTR"; push
}
