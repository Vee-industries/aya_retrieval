# Fix C panel, round 2: one agreed plan

Every lane reads all four round-1 positions and gives the one plan it would accept. The panel ends with one
plan all four accept.

## Round 1, in short

**Lane 1 (data).** C = fix A's set plus a listed delta of at most 23 rows: the 22 v6 rejections (8 already
rewritten by A) plus A's one rejected rewrite. Build 1: those rows get the scripted "Your {relation} {person}
..." answer (scripted `older` share 60 to about 83 of 200). Pre-train: `slip_shape` 0; person and value
present; a fresh three-judge CuratorKIT re-check on one blind sheet of the 23 new answers, 20 old rejections as
positive controls and 20 passing answers; go only if all 23 pass at 2 of 3 and at least 18 of 20 controls are
still rejected. Build 2 (only if build 1 fails the `in_view` line): the same rows written by a blind Claude
teacher from passage and question only. Build 3: resample base's reply up to 4 times, then scripted.

**Lane 2 (gate risk).** C will probably hit probe Sheet B `in_view` again: changing `older` targets pulls
against `in_view` (R-063/R-064), and more scripted voice adds to it. C must include A's 27 rewrites or the 19
gate-passing slip rows keep the tail. Protect `in_view`: change as few rows as possible; for the 14 non-slip
rejections resample base's own reply and re-gate it, else drop the row; leave every `in_view`, `statement` and
`never_told` row byte-identical. Also a drop-only variant (drop the 22, keep A's 27 rewrites) to trace a
failure. Order: seed 82 counts first; if probe `in_view` is below 41, stop without judging; judge only after
counts pass.

**Lane 3 (measurement).** R-094, R-086 and R-076 word for word; a one-line miss is a miss. The new targets
pass a fresh three-judge CuratorKIT re-check of the full 350 with the 22 original rejects sealed in as hidden
controls (at least about 18 of 22 rejected, or the re-check means nothing); template rewrites only, never
edited in response to judge reasons. Only 88-90 are clean seeds; disclose the candidate count. Write-up: a
data-quality gate on training targets with Claude verdicts, not an independent check of the model and not
Cohere; the re-check is an acceptance test.

**Lane 4 (against).** Keep v6. C aims at faults the slip gate does not count (19 slip rows pass the gate); the
tail may be seed-level; A already did the slip job and missed by one judge-1 line; a third recipe on the same
seeds adds selection risk; scripted rows cost coherence before (R-033); 5.5 h of GPU plus three-judge sheets
before Tuesday leaves no time to react. Present CuratorKIT as an audit finding (22 of 350, 26 of 27 rewrites
pass), not a pipeline stage. Spend the weekend on clarity, usefulness and code quality. Optional: fix A at seed
88 alone, exploratory.

Runner's note on lane 4's "not reproducible": the three judges' verdicts are saved
(`results/curator/R-096/judges/`), and `run_curator_check.py apply` reruns CuratorKIT's gate from them to the
same result; only fresh judging needs agents or an API.

## Where they differ

- Build C at all (lanes 1, 2, 3) or not (lane 4).
- Replacement for the rejected rows: scripted (1), resampled base reply else drop (2), template only (3).
- Re-check scope: 23 new answers plus controls (1) or the full 350 plus 22 hidden controls (3).
- A counts-first stop at seed 82 on probe `in_view` below 41 (2).
- A drop-only variant (2).

Reply in under 300 words: (1) the plan you would accept, ordered, with candidate-seeds; (2) your position on
each difference and what you concede; (3) anything you cannot accept.
