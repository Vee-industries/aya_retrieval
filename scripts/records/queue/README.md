# The GPU queue and its gate scripts, as run

Copied byte for byte from the working folder on 2026-11-09 (R-157), so every file a record cites as
`$S/<file>` is here. They are records, not maintained code: kept unformatted (excluded from ruff), with
the absolute paths of the machine they ran on.

- `runner2.sh` reads `backlog.txt` one line at a time and runs it; `blind.sh` and `blind2.sh` define the
  runs on the two independent sets. A line after a candidate's gate is guarded by that record's stop file.
- `decide_r*.py` print each registered gate line of that record as PASS, WAIT or FAIL and touch the
  stop file on a FAIL; `target_r*.py` compute the target on an independent set.
- `backlog.txt` is the backlog after 7.1's run (491 lines), every line as it ran or skipped.
