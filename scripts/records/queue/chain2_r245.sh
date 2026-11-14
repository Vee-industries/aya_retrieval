#!/usr/bin/env bash
# R-245: after chain_r240.sh ends, run the second blend grid (qblend2.sh) under its lock helper. Log: chain2_r245.log.
S="$(cd "$(dirname "$0")" && pwd)"
until grep -q "chain done" "$S/chain_r240.log" 2>/dev/null; do sleep 60; done
echo "== chain2: blend2 $(date)"; "C:/Users/Gaming/Desktop/Python312/python.exe" "$S/qblend2_lock.py"; echo "== chain2: blend2 exit $? $(date)"
echo "== chain2 done $(date)"
