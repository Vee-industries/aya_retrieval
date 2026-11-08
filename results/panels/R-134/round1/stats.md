**Evaluation and statistics expert, round 1**

**1. Reading: the binding lines are not the in-view lines**

Per-seed spread of 6.37 over seeds 82, 83, 94, 95, 96 (RECORDS R-128 to R-131, `fresh_r131.txt`, and my count from `results/recall_eval/{hd,probe}_fix17cs37_*_seed_73157.json` on the tool arm):
- `hard_dev` recall: 73, 90, 77, 87, 83. That is a standard deviation (sd) of 7.0 per seed. The 82-minus-83 difference across 12 copies gives the same figure (6.9).
- `hard_dev` in_view: 42, 40, 43, 36, 39 (sd 2.7). The misses total 40, and 32 of them open "It sounds like". I confirmed this count.
- Probe in_view: 44, 44, 45, 39, 42 (sd 2.4).
- Probe phone typing: 87, 89, 91, 85, 85 (sd 2.6).

There is no shared seed effect. The 82-minus-83 `hard_dev` recall differences across 12 copies are 7 positive and 5 negative, mean −2.2 (standard error about 2.8). So a same-seed pairing removes almost none of the variance. A 7 and 6.37 at 97 to 99 are two independent three-seed draws.

Chance that a copy exactly as good as 6.37 passes each line:

| Line | P(pass) |
|---|---|
| **At 82 and 83** | |
| Probe recall 192 of 192 (11% to 20% of files miss one, R-127) | 0.72 |
| R-097: probe in_view at least 41 at both seeds (6.37 itself had 39 at seed 95) | 0.69 |
| `hard_dev` Sheet B `statement` at or above base (6.37 tied 44/44) | about 0.7 |
| `hard_dev` recall pooled at least v6's 157 | 0.78 |
| `hard_dev` recall pooled at least 6.37's 163 instead | 0.56 |
| Probe 51203 `statement` / recall | about 0.85 / 0.9 |
| R-102 phone typing | 0.92 |
| Everything else | about 0.95 |
| **Product for 82 and 83** | **about 0.16** (0.12 against 163) |
| **At 97 to 99** | |
| `hard_dev` recall pooled not below 6.37 (sd of the difference 17) | 0.51 |
| Probe recall pooled not below 6.37 | 0.74 |
| Probe phone typing at least 85 at each of three seeds (two of 6.37's five seeds were exactly 85) | 0.65 |
| Judged sheets A, B and h | about 0.8 |
| Slips and R-076's counts | about 0.92 |
| **Product for 97 to 99** | **about 0.18** |

**Full gate for a clone of 6.37: about 3% (2% to 6%).** The record agrees: 2 of about 16 candidates since R-093 passed at 82 and 83.

**2. Proposed fix: none**

No in-view fix moves a binding line by more than seed noise, except a little on R-097.
- **What a fix would have to show.** To beat noise over five seeds against 6.37's eight, a fix must lift `hard_dev` in_view by about 3 per seed, which is 16 of 240 answers.
- **Removal already failed this test.** 6.34 removed the 22 "It sounds like" rows. The opener vanished, but in_view fell about 4.5 per seed and the misses turned into searches and denials. So the failure is not the opener itself.
- **Added in-view rows cost recall.** In R-120 and R-121, the 72 added in-view rows cost `hard_dev` recall 30 to 41 pooled over two seeds. That is 3 to 4 sd, and it lands on the coin-flip line.
- **Even a perfect in-view fix barely helps.** Suppose one lifts probe in_view by 2 per seed and costs nothing. R-097 rises from 0.69 to about 0.9, and the full gate from about 3% to about 4%.
- **A small recall cost sinks it.** A cost of 3 per seed in `hard_dev` recall drops the 97-to-99 recall line from 0.51 to 0.30.
- **Expected value.** The added in-view rows' record says a fix is more likely to lose `hard_dev` recall than to gain the one point. A 17th draw buys at most about 1 point of pass chance against a likely cost.

**3. The fair version of the same-seed comparison at 97 to 99**

Register these before any 7 row is built:
- 6.37 is retrained at 97, 98 and 99 from the byte-identical `fix17cs37.jsonl` (SHA-256 `04df294a`), with the same code commit, recipe, eval seed 73157 and items.
- 6.37 is queued first, never shares the card with another job (see R-114's second runner), and is scored by the same scripts.
- The comparison is the pooled three-seed sum on probe and `hard_dev` recall, with ties passing.
- 6.37's results at 82, 83 and 94 to 96 never stand in for 97 to 99. If 6.37's runs at 97 to 99 do not finish, the 7 fails.
- At 82 and 83, fix the reference now. 6.37's 192 and 163 is the version consistent with "replaces 6.37"; v6's 192 and 157 is the literal R-094 wording. Pick one before training and do not pick after reading.
- 6.37's results at 97 to 99 are reported. They do not re-decide 6.37's ship status.
- **Power, stated honestly:** a copy no better than 6.37 passes the `hard_dev` line 51% of the time. Passing it 80% of the time needs a true lift of about 14 pooled, or 4.8 per seed. That is larger than any lift in the record (6.37 over v6 at 94 to 96 was +10).

**4. Confidence**

If a 7 is trained anyway, the line it would move is R-097's probe in_view. The line it most risks is `hard_dev` recall pooled against 6.37 at 97 to 99. Probability that any in-view 7 replaces 6.37: about 3%, and no more than about 5% if the fix works perfectly. Six gate lines each carry a 22% to 49% risk of failing by seed luck alone, and the fix touches at most one of them.

**Files I used** (I wrote nothing):
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/RECORDS.md
- C:/Users/Gaming/scratch/claude/C--Users-Gaming-Desktop-Claude-s-House/389594c2-8513-47d9-80f1-1a28b96837f7/scratchpad/fresh_r131.txt
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/results/recall_eval/hd_fix17cs37_{82,83,94,95,96}_seed_73157.json and the matching probe_ files
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/data/screens/fix17cs37.jsonl