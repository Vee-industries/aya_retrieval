VOTE: YES

The design meets every yes condition I set in round 2:
- **The 6.37 reference runs.** 6.37 is retrained at 97 to 99 from the byte-identical set and command, queued first and alone on the card. The main session's correction that those runs end about 17:26 only adds slack.
- **The recall comparison.** It uses pooled three-seed sums on probe and `hard_dev` recall, with ties passing. 6.38 fails if 6.37's runs there do not finish. 6.37's files are not opened until 6.38's are done, and they do not re-decide whether 6.37 ships.
- **The reference at 82 and 83** is fixed before any row is built, at 6.37's 192 (probe) and 163 (`hard_dev`), the stricter choice.
- **The rows.** Only the 28 rewritten targets change. The build stops on any row that shares a four-word run with the test pools, and each new target needs a blind judge's pass or the old target stays. Row count, kinds and decision mix are unchanged.
- **The reporting.** In-view and lower-case results are reported whatever they show, with no gain claimed below +3 a seed. The write-up says the targets were written after reading misses on the same items, and that this is candidate 17. Any failed line stops the try, with no 6.39.

I checked the chair's claims that I could: the 28 ids and the copied phrases match my own counts.

My estimate stays at about 5% that 6.38 replaces 6.37. The binding lines are the recall comparison against 6.37 at 97 to 99, the per-seed phone floor and R-097's probe in-view line. The fix reaches only the last of these.