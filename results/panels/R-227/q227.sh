#!/usr/bin/env bash
# R-227 screening queue for K1.3s (K1.3 + one epoch of K4.8's set at 1e-4, from each seed's K1.3 adapter; one read)
# no push (commits stay local until Kevin says), each step capped at 90 minutes, run under the card lock
# by q227_lock.py. Log: q227.log beside this file. Writes q227_done.flag when finished, q227_fail.flag on a failure.
set -u
S="$(cd "$(dirname "$0")" && pwd)"
W="/c/Users/Gaming/Desktop/hackathons/Lexsi Sprint"
VP="$W/venv/Scripts/python.exe"
cd "$W/aya_retrieval" || exit 1
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
ATTR="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
MLP="q_proj k_proj v_proj o_proj gate_proj up_proj down_proj"
CAP=5400
quiet() { grep -v -E "Redirects are currently|triton not found|Loading weights" | cut -c1-600; }
clean() { until ! git status --short --untracked-files=no | grep -q .; do echo "waiting for a clean tree $(date)"; sleep 60; done; }
have() { [ -s "results/recall_eval/$1.json" ]; }
commit() { git add results && git commit -q -m "$1 (R-227 screening)" -m "$ATTR"; }
fail() { echo "FAIL $1 $(date)"; touch "$S/q227_fail.flag"; exit 1; }

evalrun() {  # pool, probe seed, label, adapter dir
  have "$3_seed_$2" && { echo "== have $3"; return 0; }
  clean; echo "== score $3 on $1 $2 $(date)"
  timeout $CAP "$VP" scripts/run_recall_eval.py --pool "$1" --seed "$2" --items-per-kind 24 --index "C:/Users/Gaming/scratch/eval_q227_$1.sqlite" --label "$3" --arms tool_loop --max-vram-fraction 0.85 --adapter "$4" 2>&1 | quiet | tail -4
  have "$3_seed_$2" || fail "$3"; commit "$3"
}
stress() {  # label, pool, extra args
  have "$1_seed_73157" && { echo "== have $1"; return 0; }
  clean; echo "== stress $1 $(date)"
  timeout $CAP "$VP" scripts/run_recall_eval.py --seed 73157 --pool "$2" --items-per-kind 24 --index "C:/Users/Gaming/scratch/eval_q227_stress.sqlite" --label "$1" --arms tool_loop --max-vram-fraction 0.85 "${@:3}" 2>&1 | quiet | tail -4
  have "$1_seed_73157" || fail "$1"; commit "$1"
}
blindrun() {  # folder, label, adapter dir
  have "$2_seed_0" && { echo "== have $2"; return 0; }
  clean; echo "== blind $2 $(date)"
  timeout $CAP "$VP" scripts/run_recall_eval.py --seed 0 --items-dir "data/$1/chats" --index "C:/Users/Gaming/scratch/eval_q227_blind.sqlite" --label "$2" --arms tool_loop --max-vram-fraction 0.85 --adapter "$3" 2>&1 | quiet | tail -3
  have "$2_seed_0" || fail "$2"; commit "$2"
}
train() {  # seed
  local AD="$W/adapters/screens/k1_3s_r227_$1"
  [ -s "$AD/adapter_model.safetensors" ] && { echo "== have adapter k1_3s_r227_$1"; return 0; }
  clean; rm -rf "$AD"; echo "== train k1_3s_r227 seed $1 $(date)"
  timeout $CAP "$VP" scripts/run_recall_train.py --seed "$1" --out-dir "$AD" --data data/screens/k4_8_r220.jsonl --report-name "k1_3s_r227_$1" --lora-r 32 --lora-targets $MLP --learning-rate 1e-4 --epochs 1 --loss-on chat_decision --max-vram-fraction 0.85 --init-adapter "$W/adapters/screens/k1_3_r200_$1" 2>&1 | tee "$S/train_k13s_$1.log" | quiet | tail -2
  [ -s "$AD/adapter_model.safetensors" ] || fail "train k1_3s_r227_$1"
  git add results/recall_train && git commit -q -m "k1_3s_r227 seed $1 trained (R-227 screening)" -m "$ATTR"
}
stresses() {  # name, seed, adapter dir
  stress "st_wb_probe_$1_$2" probe --wrong-before --kinds older confirm in_view --adapter "$3"
  stress "st_wb_hd_$1_$2" hard_dev --wrong-before --kinds older confirm in_view --adapter "$3"
  stress "st_of_probe_$1_$2" probe --other-facts --adapter "$3"
  stress "st_of_hd_$1_$2" hard_dev --other-facts --adapter "$3"
}
READ="$S/k13s_read.txt"  # written by hand after judging: 1 (pass) or bomb (R-227)
demo82() {  # R-227: Demo2 on seed 82 right after training (Kevin's gate)
  if [ ! -s results/demo2/branches_k1_3s_r227_82.json ]; then
    clean; echo "== demo2 k1_3s_r227_82 $(date)"
    timeout $CAP "$VP" scripts/run_demo2.py --adapter "K1.3s=$W/adapters/screens/k1_3s_r227_82" --out results/demo2/branches_k1_3s_r227_82.json 2>&1 | quiet | tail -3
    [ -s results/demo2/branches_k1_3s_r227_82.json ] || fail demo2_k1_3s
    git add results/demo2 && git commit -q -m "Demo2 on k1_3s_r227 seed 82 (R-227)" -m "$ATTR" -- results/demo2
  fi
  echo "DEMO2 READY $(date)"
  until [ -s "$READ" ]; do sleep 60; done
  R=$(tr -d ' \r\n' < "$READ"); echo "== read: $R $(date)"
  [ "$R" = bomb ] && { echo "== K1.3s bombs Demo2; q227 done $(date)"; touch "$S/q227_done.flag"; exit 0; }
  [ "$R" = 1 ] || fail "read file holds $R"
}
ckpt() {  # seed -> the read checkpoint's adapter dir
  echo "$W/adapters/screens/k1_3s_r227_$1"
}
hdgate() {  # R-222: stop on the first failed hard_dev line
  "$VP" "$S/hd_gate.py" k1_3s_r227 "$1" 2>&1 | grep "hd gate"
  "$VP" "$S/hd_gate.py" k1_3s_r227 "$1" >/dev/null 2>&1 || { echo "== K1.3s fails screening at seed $1; q227 done $(date)"; touch "$S/q227_done.flag"; exit 0; }
}
CC="--kinds statement --chat-check data/check/chat_check.json"
candidate() {  # seed; every score from the read checkpoint (R-222)
  train "$1"
  [ "$1" = 82 ] && demo82
  local AD; AD=$(ckpt "$1")
  evalrun hard_dev 73157 "hd_k1_3s_r227_$1" "$AD"
  hdgate "$1"
  [ "$1" = 82 ] && evalrun probe 51203 "screen_k1_3s_r227_82" "$AD"
  evalrun probe 73157 "probe_k1_3s_r227_$1" "$AD"
  stress "st_cc_k1_3s_r227_$1" probe $CC --adapter "$AD"
  blindrun blind_dev "blind_k1_3s_r227_$1" "$AD"
  blindrun blind_dev2 "blind2_k1_3s_r227_$1" "$AD"
  stresses k1_3s_r227 "$1" "$AD"
  stresses fix17cs37 "$1" "$W/adapters/screens/fix17cs37_$1"
}
rm -f "$S/q227_done.flag" "$S/q227_fail.flag"
echo "== q227 start $(date)"
candidate 82
candidate 83
pick94() {  # seed 94: the pick sets only (R-192), read checkpoint as 82 and 83
  train 94
  local AD; AD=$(ckpt 94)
  [ -s "$AD/adapter_model.safetensors" ] || fail "no read checkpoint for seed 94"
  evalrun hard_dev 73157 "hd_k1_3s_r227_94" "$AD"
  evalrun probe 73157 "probe_k1_3s_r227_94" "$AD"
  blindrun blind_dev "blind_k1_3s_r227_94" "$AD"
  blindrun blind_dev2 "blind2_k1_3s_r227_94" "$AD"
}
pick94
rm -f C:/Users/Gaming/scratch/eval_q227_*.sqlite
echo "== q227 done $(date)"; touch "$S/q227_done.flag"
