#!/usr/bin/env bash
# R-088: 19a, fix 20 at three doses and 19b at seeds 82-83, seed 84 for each that passes, then the stress tests. Offline.
S="/c/Users/Gaming/scratch/claude/C--Users-Gaming-Desktop-Claude-s-House/389594c2-8513-47d9-80f1-1a28b96837f7/scratchpad"
W="/c/Users/Gaming/Desktop/hackathons/Lexsi Sprint"
VP="$W/venv/Scripts/python.exe"
export TMP="$S" TEMP="$S" PYTHONIOENCODING=utf-8 HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
cd "$W/aya_retrieval" || exit 1
quiet() { grep -v -E "Redirects are currently|triton not found|Loading weights" | cut -c1-900; }
ATTR="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
MLP="q_proj k_proj v_proj o_proj gate_proj up_proj down_proj"
clean() { until ! git status --short --untracked-files=no | grep -q .; do echo "waiting for a clean tree $(date)"; sleep 60; done; }
push() { timeout 120 git push -q || echo "push failed, continuing $(date)"; }
# R-088 backlog runner: runs backlog.txt line by line; append lines to add work. A failed line is logged and skipped.
B="$S/backlog.txt"; DONE="$S/backlog.done"; touch "$B" "$DONE"
DIALS="$W/adapters/dials"
have() { [ -s "results/recall_eval/$1.json" ]; }
evalrun() {  # pool, probe seed, label, adapter dir
  local out="results/recall_eval/$3_seed_$2.json"
  have "$3_seed_$2" && { echo "== have $3"; return 0; }
  for try in 1 2 3; do
    clean
    echo "== score $3 on $1 $2 try $try $(date)"
    "$VP" scripts/run_recall_eval.py --pool "$1" --seed "$2" --items-per-kind 24 --index "C:/Users/Gaming/scratch/eval_q56_$1.sqlite" --label "$3" --arms tool_loop --max-vram-fraction 0.85 --adapter "$4" 2>&1 | quiet | tail -11
    [ -s "$out" ] && break
    sleep 30
  done
  [ -s "$out" ] || { echo "NO RESULTS $3"; return 1; }
  git add results/recall_eval && git commit -q -m "$3 (R-088), scored on $1 seed $2" -m "$ATTR"; push
}
stress() {  # label, pool, extra args
  local out="results/recall_eval/$1_seed_73157.json"
  have "$1_seed_73157" && { echo "== have $1"; return 0; }
  for try in 1 2 3; do
    clean
    echo "== score $1 try $try $(date)"
    "$VP" scripts/run_recall_eval.py --seed 73157 --pool "$2" --items-per-kind 24 --index "C:/Users/Gaming/scratch/eval_stress.sqlite" --label "$1" --arms tool_loop --max-vram-fraction 0.85 "${@:3}" 2>&1 | quiet | tail -11
    [ -s "$out" ] && break
    sleep 30
  done
  [ -s "$out" ] || { echo "NO RESULTS $1"; return 1; }
  git add results/recall_eval && git commit -q -m "$1 (R-088)" -m "$ATTR"; push
}
train() {  # name, seed, data, extra training args
  local AD="$W/adapters/screens/$1_$2" save="--save-epochs 2"
  [[ " ${*:4} " == *" --epochs 2 "* ]] && save=""
  [ -s "$AD/adapter_model.safetensors" ] && { echo "== have adapter $1_$2"; return 0; }
  for try in 1 2 3; do
    clean
    rm -rf "$AD"
    echo "== train $1 seed_$2 try $try $(date)"
    "$VP" scripts/run_recall_train.py --seed "$2" --out-dir "$AD" --data "$3" --report-name "$1_$2" --lora-r 32 --lora-targets $MLP --learning-rate 3e-4 --loss-on demonstrated --max-vram-fraction 0.85 $save "${@:4}" 2>&1 | tee "$S/train_$1_$2.log" | quiet | tail -2
    [ -s "$AD/adapter_model.safetensors" ] && break
    sleep 30
  done
  [ -s "$AD/adapter_model.safetensors" ] || { echo "NO ADAPTER $1 $2"; return 1; }
  git add results/recall_train && git commit -q -m "$1 (R-088), seed $2: ${*:4}" -m "$ATTR"; push
}
CC="--kinds statement --chat-check data/check/chat_check.json"
scores() {  # name, seed, adapter dir
  if [ "$2" = 82 ]; then evalrun probe 51203 "screen_$1_82" "$3" || return 1; fi
  evalrun hard_dev 73157 "hd_$1_$2" "$3" || return 1
  evalrun probe 73157 "probe_$1_$2" "$3" || return 1
  stress "st_cc_$1_$2" probe $CC --adapter "$3" || return 1
  echo "== candidate $1 seed $2 scored $(date)"
}
cand() {  # name, seed, data, extra training args
  train "$@" || return 1
  scores "$1" "$2" "$W/adapters/screens/$1_$2"
}
dial() {  # name, seed, adapter dir: scoring only
  scores "$1" "$2" "$3"
}
gate_then() {  # name, data, extra training args: seed 84 if the unjudged gate passes
  if "$VP" scripts/records/gate_r086.py "$1"; then
    echo "== $1 passes the unjudged gate $(date)"; cand "$1" 84 "${@:2}"
  else
    echo "== $1 fails the unjudged gate $(date)"
  fi
}
if [ -n "$1" ]; then  # a result file a stopped queue's running step will write
  echo "== waiting for $1 $(date)"
  until [ -s "$1" ]; do sleep 30; done; sleep 20
  git add results && git commit -q -m "$(basename "$1" .json) (R-086)" -m "$ATTR"; push
fi
while true; do
  n=$(( $(wc -l < "$DONE") + 1 ))
  line=$(sed -n "${n}p" "$B")
  if [ -z "$line" ]; then
    [ -f "$S/idle.flag" ] || { echo "== backlog empty $(date)"; touch "$S/idle.flag"; }
    sleep 60; continue
  fi
  rm -f "$S/idle.flag"
  echo "== line $n: $line $(date)"
  if eval "$line"; then echo "== line $n done $(date)"; else echo "== line $n FAILED $(date)"; fi
  echo "$n" >> "$DONE"
done
