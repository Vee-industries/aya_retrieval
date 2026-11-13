#!/usr/bin/env bash
# R-229 one try of the stage ladder: a stage on each seed's K1.3 adapter, then Demo2, then Demo3 (held out), then
# screening, modeled on q227.sh. Run under the card lock by qtry_lock.py; no push.
# Usage: qtry.sh LABEL LR EPOCHS DATA
#   LABEL  results label, e.g. k13t2_r229 (adapters/screens/LABEL_SEED)
# After each Demo run the queue prints DEMO2 READY or DEMO3 READY and waits for a read file beside the log:
# LABEL_read2.txt, then LABEL_read3.txt, holding "pass" or "bomb" (written by hand after two blind judges).
# A bomb, or a failed hard_dev line on seed 82 or 83 (hd_gate.py), ends the try; the lock then passes on.
set -u
LABEL=$1 LR=$2 EPOCHS=$3 DATA=$4
S="$(cd "$(dirname "$0")" && pwd)"
W="/c/Users/Gaming/Desktop/hackathons/Lexsi Sprint"
VP="$W/venv/Scripts/python.exe"
cd "$W/aya_retrieval" || exit 1
export HF_HUB_OFFLINE=1 HF_HUB_DISABLE_TELEMETRY=1
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True  # R-231: fits the 0.78 cap; changes no numbers
ATTR="Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
MLP="q_proj k_proj v_proj o_proj gate_proj up_proj down_proj"
CAP=5400
VRAM=0.78  # R-228: the whole card stays under the card rule's 85% with the desktop's 0.7 GB
quiet() { grep -v -E "Redirects are currently|triton not found|Loading weights" | cut -c1-600; }
clean() { until ! git status --short --untracked-files=no | grep -q .; do echo "waiting for a clean tree $(date)"; sleep 60; done; }
have() { [ -s "results/recall_eval/$1.json" ]; }
commit() { git add results && git commit -q -m "$1 (R-229 $LABEL)" -m "$ATTR"; }
fail() { echo "FAIL $1 $(date)"; touch "$S/${LABEL}_fail.flag"; exit 1; }
stop() { echo "== $LABEL $1; try done $(date)"; touch "$S/${LABEL}_done.flag"; exit 0; }

evalrun() {  # pool, probe seed, label, adapter dir
  have "$3_seed_$2" && { echo "== have $3"; return 0; }
  clean; echo "== score $3 on $1 $2 $(date)"
  timeout $CAP "$VP" scripts/run_recall_eval.py --pool "$1" --seed "$2" --items-per-kind 24 --index "C:/Users/Gaming/scratch/eval_${LABEL}_$1.sqlite" --label "$3" --arms tool_loop --max-vram-fraction $VRAM --adapter "$4" 2>&1 | quiet | tail -4
  have "$3_seed_$2" || fail "$3"; commit "$3"
}
stress() {  # label, pool, extra args
  have "$1_seed_73157" && { echo "== have $1"; return 0; }
  clean; echo "== stress $1 $(date)"
  timeout $CAP "$VP" scripts/run_recall_eval.py --seed 73157 --pool "$2" --items-per-kind 24 --index "C:/Users/Gaming/scratch/eval_${LABEL}_stress.sqlite" --label "$1" --arms tool_loop --max-vram-fraction $VRAM "${@:3}" 2>&1 | quiet | tail -4
  have "$1_seed_73157" || fail "$1"; commit "$1"
}
blindrun() {  # folder, label, adapter dir
  have "$2_seed_0" && { echo "== have $2"; return 0; }
  clean; echo "== blind $2 $(date)"
  timeout $CAP "$VP" scripts/run_recall_eval.py --seed 0 --items-dir "data/$1/chats" --index "C:/Users/Gaming/scratch/eval_${LABEL}_blind.sqlite" --label "$2" --arms tool_loop --max-vram-fraction $VRAM --adapter "$3" 2>&1 | quiet | tail -3
  have "$2_seed_0" || fail "$2"; commit "$2"
}
train() {  # seed: the stage on the same seed's K1.3 adapter
  local AD="$W/adapters/screens/${LABEL}_$1"
  [ -s "$AD/adapter_model.safetensors" ] && { echo "== have adapter ${LABEL}_$1"; return 0; }
  clean; rm -rf "$AD"; echo "== train ${LABEL} seed $1 (lr $LR, $EPOCHS epochs, $DATA) $(date)"
  timeout $CAP "$VP" scripts/run_recall_train.py --seed "$1" --out-dir "$AD" --data "$DATA" --report-name "${LABEL}_$1" --lora-r 32 --lora-targets $MLP --learning-rate "$LR" --epochs "$EPOCHS" --loss-on chat_decision --max-vram-fraction $VRAM --init-adapter "$W/adapters/screens/k1_3_r200_$1" 2>&1 | tee "$S/train_${LABEL}_$1.log" | quiet | tail -2
  [ -s "$AD/adapter_model.safetensors" ] || fail "train ${LABEL}_$1"
  git add results/recall_train && git commit -q -m "${LABEL} seed $1 trained (R-229)" -m "$ATTR"
}
demo() {  # 2 or 3: run Demo N on seed 82, then wait for its read
  local OUT="results/demo2/branches_${LABEL}_82_demo$1.json"
  if [ ! -s "$OUT" ]; then
    clean; echo "== demo$1 ${LABEL}_82 $(date)"
    timeout $CAP "$VP" scripts/run_demo2.py --demo-dir "demo$1" --adapter "${LABEL}=$W/adapters/screens/${LABEL}_82" --out "$OUT" 2>&1 | quiet | tail -3
    [ -s "$OUT" ] || fail "demo$1"
    git add "$OUT" && git commit -q -m "Demo$1 on ${LABEL} seed 82 (R-229)" -m "$ATTR" -- "$OUT"
  fi
  echo "DEMO$1 READY $(date)"
  until [ -s "$S/${LABEL}_read$1.txt" ]; do sleep 30; done
  local R; R=$(tr -d ' \r\n' < "$S/${LABEL}_read$1.txt"); echo "== demo$1 read: $R $(date)"
  [ "$R" = bomb ] && stop "bombs Demo$1"
  [ "$R" = pass ] || fail "read file holds $R"
}
hdgate() {  # R-222: stop on the first failed hard_dev line
  "$VP" "$S/hd_gate.py" "$LABEL" "$1" 2>&1 | grep "hd gate"
  "$VP" "$S/hd_gate.py" "$LABEL" "$1" >/dev/null 2>&1 || stop "fails hard_dev at seed $1"
}
stresses() {  # name, seed, adapter dir
  stress "st_wb_probe_$1_$2" probe --wrong-before --kinds older confirm in_view --adapter "$3"
  stress "st_wb_hd_$1_$2" hard_dev --wrong-before --kinds older confirm in_view --adapter "$3"
  stress "st_of_probe_$1_$2" probe --other-facts --adapter "$3"
  stress "st_of_hd_$1_$2" hard_dev --other-facts --adapter "$3"
}
CC="--kinds statement --chat-check data/check/chat_check.json"
candidate() {  # seed
  local AD="$W/adapters/screens/${LABEL}_$1"
  train "$1"
  [ "$1" = 82 ] && { demo 2; demo 3; }
  evalrun hard_dev 73157 "hd_${LABEL}_$1" "$AD"
  hdgate "$1"
  [ "$1" = 82 ] && evalrun probe 51203 "screen_${LABEL}_82" "$AD"
  evalrun probe 73157 "probe_${LABEL}_$1" "$AD"
  stress "st_cc_${LABEL}_$1" probe $CC --adapter "$AD"
  blindrun blind_dev "blind_${LABEL}_$1" "$AD"
  blindrun blind_dev2 "blind2_${LABEL}_$1" "$AD"
  stresses "$LABEL" "$1" "$AD"
  stresses fix17cs37 "$1" "$W/adapters/screens/fix17cs37_$1"
}
pick94() {  # seed 94: the pick sets only (R-192)
  local AD="$W/adapters/screens/${LABEL}_94"
  train 94
  evalrun hard_dev 73157 "hd_${LABEL}_94" "$AD"
  evalrun probe 73157 "probe_${LABEL}_94" "$AD"
  blindrun blind_dev "blind_${LABEL}_94" "$AD"
  blindrun blind_dev2 "blind2_${LABEL}_94" "$AD"
}
rm -f "$S/${LABEL}_done.flag" "$S/${LABEL}_fail.flag"
echo "== try $LABEL start (lr $LR, $EPOCHS epochs, $DATA) $(date)"
candidate 82
candidate 83
pick94
rm -f C:/Users/Gaming/scratch/eval_${LABEL}_*.sqlite
echo "== try $LABEL done $(date)"; touch "$S/${LABEL}_done.flag"
