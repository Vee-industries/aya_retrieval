# Panel brief: is there a 7.1, and if so what is it

You are one lane of a three-lane panel. You read and may run light CPU-only Python to count things; you write nothing
to disk and change nothing. Your answer is your final message, under 700 words.

## Hard limits (break one and your answer is void)

- Never open `src/aya_retrieval/pool_independent.py`, anything under `docs/independent_pool/`, or line 452 onward of
  `src/aya_retrieval/pools.py` (sealed held-out material). When you search `pools.py`, limit the search to lines 1 to
  451 (for example `head -n 451 src/aya_retrieval/pools.py | grep ...`); never grep the whole file. Never open a file
  whose name contains "token".
- Never open anything under `C:/Users/Gaming/scratch/claude/C--Users-Gaming-Desktop-Claude-s-House/389594c2-8513-47d9-80f1-1a28b96837f7/scratchpad/indep2/`
  or `data/blind_dev2/`, any result whose name contains `blind2` or `75002`.
- Training rows come only from the TRAIN pool (`pools.py` lines 1 to 451) or new material that shares no four-word run
  with the probe or `hard_dev` pools (`scripts/records/build_r110.py` `TEST_GRAMS`). Never from probe, `hard_dev`,
  either independent set, break-test items or held-out material. `phone_style` never enters training. Never copy a
  probe or `hard_dev` wording into training, and do not design a row aimed at one probe template's wording.

## Repo and context

`C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`. Read `RECORDS.md` R-150 to R-155 first (R-153 is 7's
design, R-155 its result), then earlier records as needed (R-127 on probe pass rates; R-110 to R-128 on how 6.37's set
was built and what failed). Sets: 6.37 `data/screens/fix17cs37.jsonl`, 7 `data/screens/fix17cs7.jsonl` (its builder
`scripts/records/build_r153.py`). Results: `results/recall_eval/{probe,hd,screen,st_cc}_{fix17cs37,fix17cs7}_{82,83}_*`
(screen = probe seed 51203, seed 82 only). The first independent set, a development set: `data/blind_dev/chats/`,
6.37's results `results/recall_eval/blind_*_seed_0.json`, analysis `results/analysis/R-146/blind.json`.

## The facts

- 6.37 (fix17cs37 seed 82) is the shipped model. 7 (6.37's rows with 100 `confirm`, 20 `never_told` and 20 `in_view`
  questions reworded as tag questions) failed R-153 at seeds 82 and 83 on two lines: probe 51203 recall 92 (needs
  94) and probe 73157 recall pooled 189 (needs 192). Six of its seven probe misses are `older` questions in one probe
  wording with no search; 6.37 misses that wording once. `hard_dev` recall 81 and 85 against 6.37's 73 and 90.
- 7 was meant to fix tag questions on chats written by people who never saw the generator (R-146: 23 of 29 `confirm`
  misses there never searched). Whether it did is unknown: its independent-set runs are skipped.
- R-127: a copy with no defect misses one probe question in 192 about 28% of the time.
- Time: it is Mon Nov 9 11:10. Model freeze Wed Nov 11 night. A candidate costs about 7 GPU hours to judge in full
  (82 and 83 with scores, stress runs, judged sheets, 94 to 96, the second independent set at five seeds). A new set
  must be buildable on the CPU by script within a few hours. A candidate trains from scratch with 6.37's recipe unless
  the design argues otherwise, and passes everything 7 had to pass (R-153), unchanged.

## The question

Should there be a 7.1 before the freeze? Give one design or say "no 7.1", with reasons. A design names which rows
change or are added and how they are built, how many, what the answers look like, and why it should keep 7's
intended gain on tag questions without the `older` cost. Say what result shows it failed, the chance it passes R-153
if it has no effect at all, and the single biggest risk. Options already raised: 7 without the 20 `in_view` tag rows;
fewer tag rows; the next-exchange hop R-153 left out; no 7.1.

## Your lane

{LANE}
