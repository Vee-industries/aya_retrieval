# Panel R-185: one more candidate (K2) after K1 failed screening

## The request
Kevin (the author), 2026-11-12, after K1's screening result: "One more candidate". Read RECORDS.md entries R-177,
R-178, R-180, R-182, R-183 and R-184 first (grep for "## R-177" and so on; read only those entries).

## Project in brief
A LoRA adapter (6.37, rank 32, all seven projections, lr 3e-4, `--loss-on chat_decision`, data
`data/screens/fix17cs37.jsonl`, 1,094 rows) on Tiny Aya Global (3.35B), for a Lexsi Labs hackathon (Track 3). The
model sees the last three exchanges of a chat and can call a full-text search tool over older exchanges (OR matching;
each passage is one whole exchange). A public demo showed two failures: an unrelated passage given as the answer to
a never-told question, and an earlier wrong answer in view repeated. The project was reopened (R-177); a new test, S3,
was sealed and put on GitHub before any candidate result (R-179, R-181). R-178 registered one candidate, K1 = F2 + F3
on 6.37's own rows (`scripts/records/build_r178.py`), screening gates, and a ship rule on S3. S3 is still unopened.

## K1's result (R-183, R-184)
- Failure-mode targets met by wide margins: copies of an earlier wrong value 368 to 68 (gate at most 184); false
  answers on never-told questions among other facts 53 to 3 (gate at most 26). Demo: 4 of 4 and 3 of 8, against
  6.37's 2 of 4 and 0 of 8.
- Failed three recall gates: hard_dev recall 122 against 6.37's 163 (gate at least 151); outside-writer recall 171
  against 188 (gate at least 178); other-facts recall 296 against 323 (gate at least 318).
- On hard_dev, 61 of K1's 70 misses found the fact's passage; most replies decline ("I don't have that from you").

## New evidence for this panel (`scripts/records/passages_r185.py`, committed files only)
Passages the search returns, per training row (bins 0 to 5, 5 means 5 or more):

| Set | found rows (older, confirm) | never_told rows |
|---|---|---|
| 6.37 | 1: 165, 2: 165, 3: 164, 4: 50, 5: 18 | 0: 22, 1: 40, 2: 40, 3: 51, 4: 4, 5: 3 |
| K1 | 1: 69, 2: 146, 3: 143, 4: 137, 5: 67 | 0: 0, 1: 29, 2: 41, 3: 46, 4: 30, 5: 14 |

hard_dev older and confirm questions whose search found the fact, seeds 82 and 83 pooled, right / wrong:

| Passages | 6.37 | K1 |
|---|---|---|
| 1 | 68 / 10 | 31 / 25 |
| 2 | 52 / 1 | 62 / 8 |
| 3 | 2 / 2 | 2 / 2 |
| 4 | 5 / 1 | 6 / 3 |
| 5 or more | 36 / 8 | 21 / 23 |

F2 adds other facts to every chat, which the search also returns; single-passage found rows fell from 165 to 69, and
K1's worst bin on hard_dev is the single passage. The 5-or-more bin is also worse for K1, although K1's training has
more found rows there, so passage count alone does not explain that bin.

## Two options I see (pick one, change it, or argue for neither)
A. **Passage count kept.** K2 = K1, except each found row (older, confirm) gets the F2 share whose search returns the
   same number of passages as the row's 6.37 search, trying the three shares in a fixed order, and no F2 if none
   matches. never_told rows and F3 as in K1. Check before training (no model): found rows' passage-count
   distribution within a stated distance of 6.37's.
B. **Half dose.** K2 = K1 with F2 and F3 on half the rows of each kind (the rest keep 6.37's rows), on the view that
   K1 overshot both targets and a lower dose keeps them while costing less recall.

## Constraints
- One candidate. Same screening gates and targets as R-178, against 6.37 at seeds 82 and 83; same ship rule on S3.
- Time: it is Thursday 12 November, 10:50 Eastern. Training starts no later than Saturday 23:59 Eastern (R-182).
  Training is about 33 minutes a seed; one seed's screening about 45 minutes. K2's build should take under 2 hours.
- K2 is designed after K1's dev results were read; that is disclosed. S3 stays unopened until the candidate set is
  final, so S3 remains a clean test for K2.
- History: every candidate after 6.37 (6.38, 6.39, 7, 7.1, K1) failed a registered gate; seed-to-seed noise on dev
  pools is about 20 points; many candidate sets were screened on reused dev pools (R-141, R-157).
- Rules: a panel before a change of method; every number from a committed file; never soften or overstate; plain
  words, no metaphors.

## Read limits
Repo: C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval. You may read RECORDS.md (the named entries, and
others by grep if needed), scripts/, src/aya_retrieval/ files other than pools.py, results/recall_eval/ files whose
names start with hd_, probe_, st_, blind_ or blind2_, data/screens/fix17cs37.jsonl and data/screens/k1_r178.jsonl.
Do not open src/aya_retrieval/pools.py beyond line 451, any file under data/ named heldout or independent (this
includes data/heldout3/), or results/longmemeval/. Edit nothing, run no model, no git write. You may run read-only
Python with `..\venv\Scripts\python.exe` from the repo (set PYTHONPATH=src) to count things in the allowed files.
