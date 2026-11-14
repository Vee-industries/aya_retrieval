#!/usr/bin/env bash
# R-253: after the T6 and T4 grid (chain2_r245.sh), the on-policy evals, the rehearsal-only control C0, then the
# on-policy stage OP once its three per-seed sets exist. Log: chain5_r253.log beside this file.
S="$(cd "$(dirname "$0")" && pwd)"
PY="C:/Users/Gaming/Desktop/Python312/python.exe"
REPO="/c/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval"
run() { echo "== chain: $* $(date)"; "$PY" "$S/qtry2_lock.py" "$@"; echo "== chain: $1 exit $? $(date)"; }
until grep -q "chain2 done" "$S/chain2_r245.log" 2>/dev/null; do sleep 30; done
echo "== chain: op evals $(date)"; "$PY" "$S/qop_eval_lock.py"; echo "== chain: op evals exit $? $(date)"
run k13c0_r253 1e-4 1 data/screens/k1_3_r200.jsonl
until [ -s "$REPO/data/screens/k13op_82_r253.jsonl" ] && [ -s "$REPO/data/screens/k13op_83_r253.jsonl" ] && [ -s "$REPO/data/screens/k13op_94_r253.jsonl" ]; do sleep 30; done
run k13op_r253 1e-4 1 data/screens/k13op_SEED_r253.jsonl
echo "== chain5 done $(date)"
