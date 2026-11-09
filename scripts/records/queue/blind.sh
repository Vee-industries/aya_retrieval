# R-142: the independent development set's runs; sourced by a backlog line inside runner2.sh.
blind() {  # label, extra args
  local out="results/recall_eval/$1_seed_0.json"
  have "$1_seed_0" && { echo "== have $1"; return 0; }
  for try in 1 2 3; do
    clean
    echo "== blind $1 try $try $(date)"
    "$VP" scripts/run_recall_eval.py --seed 0 --items-dir data/blind_dev/chats --index "C:/Users/Gaming/scratch/eval_blind.sqlite" --label "$1" --arms tool_loop --max-vram-fraction 0.85 "${@:2}" 2>&1 | quiet | tail -n 3
    [ -s "$out" ] && break
    sleep 30
  done
  [ -s "$out" ] || { echo "NO RESULTS $1"; return 1; }
  git add "$out" && git commit -q -m "$1 (R-142 independent set)" -m "$ATTR"; push
}
