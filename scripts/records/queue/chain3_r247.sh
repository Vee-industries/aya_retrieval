#!/usr/bin/env bash
# R-247: replaces chain_r240.sh after R2d: R2cf (R2c's recipe on the checked set), the blend grid, R3a; then marks
# chain_r240.log done so chain2_r245.sh (the T6 and T4 blend) runs. Log: chain3_r247.log beside this file.
S="$(cd "$(dirname "$0")" && pwd)"
PY="C:/Users/Gaming/Desktop/Python312/python.exe"
run() { echo "== chain: $* $(date)"; "$PY" "$S/qtry2_lock.py" "$@"; echo "== chain: $1 exit $? $(date)"; }
run k13r2cf_r247 1e-4 1 data/screens/k5f_r247.jsonl
echo "== chain: blend $(date)"; "$PY" "$S/qblend_lock.py"; echo "== chain: blend exit $? $(date)"
run k46r3a_r241 1e-4 1 data/screens/k4_6tw_r241.jsonl k4_6_r214
echo "== chain3 done $(date)"; echo "== chain done (by chain3_r247.sh) $(date)" >> "$S/chain_r240.log"
