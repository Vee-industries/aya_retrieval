#!/usr/bin/env bash
# R-240: run the registered tries one after another, each under its own lock helper, so one waits for the card at a
# time. Order: round 2 (R-235), the blend grid (R-237), round 3's R3a (R-241). R3b and R3c are conditional (R-241) and
# are added by hand when their condition is met. Log: chain_r240.log beside this file.
S="$(cd "$(dirname "$0")" && pwd)"
PY="C:/Users/Gaming/Desktop/Python312/python.exe"
run() { echo "== chain: $* $(date)"; "$PY" "$S/qtry2_lock.py" "$@"; echo "== chain: $1 exit $? $(date)"; }
run k13r2a_r235 1e-4 1 data/screens/k4_8m_r235.jsonl
run k46r2b_r235 1e-4 1 data/screens/k1_3_r200.jsonl k4_6_r214
run k13r2c_r235 1e-4 1 data/screens/k5_r226.jsonl
run k13r2d_r235 1e-4 1 data/screens/k4_9_r224.jsonl
echo "== chain: blend $(date)"; "$PY" "$S/qblend_lock.py"; echo "== chain: blend exit $? $(date)"
run k46r3a_r241 1e-4 1 data/screens/k4_6tw_r241.jsonl k4_6_r214
echo "== chain done $(date)"
