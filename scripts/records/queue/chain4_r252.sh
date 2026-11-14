#!/usr/bin/env bash
# R-252: after chain2_r245.sh ends, run round 5 one try at a time, each under its lock helper. Log: chain4_r252.log.
S="$(cd "$(dirname "$0")" && pwd)"
PY="C:/Users/Gaming/Desktop/Python312/python.exe"
run() { echo "== chain: $* $(date)"; "$PY" "$S/qtry2_lock.py" "$@"; echo "== chain: $1 exit $? $(date)"; }
until grep -q "chain2 done" "$S/chain2_r245.log" 2>/dev/null; do sleep 60; done
run k136r5a_r252 1e-4 1 data/screens/k5f_r247.jsonl k13t6_r229
run k13r5b_r252 3e-4 1 data/screens/k5f_r247.jsonl
run k46r5c_r252 1e-4 1 data/screens/k5f_r247.jsonl k4_6_r214
run k136r5d_r252 3e-4 1 data/screens/k5f_r247.jsonl k13t6_r229
run k13r5e_r252 1e-4 3 data/screens/k5f_r247.jsonl
echo "== chain4 done $(date)"
