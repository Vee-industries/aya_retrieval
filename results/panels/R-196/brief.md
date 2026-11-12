# Panel R-196: the next candidate after K2.1 failed screening (K1.1, a refinement of K1)

## The request
Kevin (the author), 2026-11-12: a head-to-head between candidates, then "training that one once or twice more", with
any number of candidates as long as training is done by the cutoff (R-194). K2.1 failed a screening line (R-195), so
K1 is the only candidate still open. This panel decides the next candidate, K1.1, a refinement of K1. Read RECORDS.md
entries R-178, R-183, R-185, R-187, R-191, R-194 and R-195 first (grep for "## R-178" and so on; read only those),
then `results/panels/R-185/lane_method.md` and `lane_against.md`.

## Project in brief
A LoRA adapter on Tiny Aya Global (3.35B) for a Lexsi Labs hackathon (Track 3). The model sees the last three
exchanges of a chat and can call a full-text search over older exchanges (OR matching, top 5; each passage is one
whole exchange). 6.37 (data `data/screens/fix17cs37.jsonl`) is the published version. K1 (`k1_r178.jsonl`, built by
`scripts/records/build_r178.py`) = 6.37's rows + F2 (2 to 4 other facts out of view in every rebuilt chat, three
shares: same_type, same_person, shared_word) + F3 (earlier answers in view). Since R-191 the recall lines compare with
base (no adapter), whose rerun is under way now; the failure-mode targets still compare with 6.37.

## Where K1 stands (R-195 table, committed results)
K1 meets both failure-mode targets by wide margins (copies of an earlier wrong value 68 against 6.37's 368; false
answers on never-told questions among other facts 3 against 53) and passes every line that does not need base. Its
weak point is hard_dev recall: 57 and 65 at seeds 82 and 83, against 6.37's 73 and 90. K2.1 (half the same_person
never_told rows moved to other shares) scored 68 and 51: no steady gain, and a failed in_view line at seed 83.

## New evidence for this panel (my count, from `results/recall_eval/hd_*_seed_73157.json`)
hard_dev older and confirm items that 6.37 gets right and the candidate misses, by what the candidate did:

| | K1 82 | K1 83 | K2.1 82 | K2.1 83 |
|---|---|---|---|---|
| searched, fact's passage found, reply declines | 17 | 19 | 14 | 18 |
| searched, found, other wrong reply | 3 | 5 | 6 | 8 |
| searched, not found | 1 | 4 | 0 | 14 |
| items the candidate gets right and 6.37 misses | 5 | 3 | 15 | 1 |

In many of the found-and-declined items, K1 sent the same query as 6.37 and got the same passages, and 6.37 answered
while K1 declined. Examples, seed 82: "my head has lost the name of the place my housemate came of age in" (key Lyon;
query and 5 passages identical for both; 6.37 "Your housemate Mirela grew up in Lyon.", K1 "I don't know that one
yet."); "did where my lodger came of age ever come up from me" (key Cork; identical query and passages). hard_dev
questions often use other words than the message that stated the fact ("came of age" for "grew up").

## My reading, to be tested, not assumed
F2's same_person share puts a passage naming the asked person, about a different fact, next to a never_told question,
with a decline target. When the question's words match the passage's fact, the model can tell the cases apart; when
the question uses other words (hard_dev), it cannot, and K1 declines. Two directions I see; check each against the
data before taking it:

A. **Found rows in other words.** K1.1 = K1, plus or in place of some found rows: older and confirm rows in the
   same_person share whose question asks the fact in other words than its message, so the training shows a
   same-person passage answering a question that shares few words with it. The wording must come from training
   pools (`TRAIN` in `pools.py`, up to line 451, and the builder's question forms), never from hard_dev's forms. Check
   whether the builder already makes such questions (`run_build_training_set.py`, `--more-indirect`).
B. **The spliced rows.** The 124 spliced rows (`indirect/`, `facts/`, `contrast/`) have no seed and K1 keeps them
   unchanged, so they never get F2. If indirect questions live mostly in those rows, K1's training never shows an
   indirect question next to a same-person passage of another fact. Check how many rows of each set ask in other
   words, and in which shares.

Pick one, change it, propose another, or argue for none (for example: ship K1 as it is to the pick).

## Constraints
- Time: Thursday 12 November, about 15:00 Eastern. R-194: every candidate's training, seeds 82, 83 and 94, is done by
  Saturday 14 November 16:00 Eastern. Training about 33 minutes a seed; screening about 75 minutes a seed with the
  stress sets. The card is busy until about 17:30 today (base reruns, then K1's seed 94).
- K1.1 is designed after K1's and K2.1's dev results were read; that is disclosed. S3 stays sealed until the pick.
- Screening lines are R-191's, unchanged (`scripts/records/decide_r191.py`). Seed-to-seed noise on dev pools is about
  20 points (K2.1's hard_dev 68 against 51).
- Rules: every number from a committed file; never soften or overstate; plain words, no metaphors; no invented rates
  or margins; a build that changes only what the record names.

## Read limits
Repo: C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval. You may read RECORDS.md, scripts/,
src/aya_retrieval/ (pools.py only up to line 451), results/recall_eval/ files whose names start with hd_, probe_,
st_, blind_ or blind2_, results/panels/, and data/screens/ files named fix17cs37, k1_r178 or k2_1_r187. Do not open
src/aya_retrieval/pools.py beyond line 451, any file under data/ named heldout or independent (this includes
data/heldout3/), or results/longmemeval/. Edit nothing except your own lane file, run no model, no git. You may run
read-only Python with `..\venv\Scripts\python.exe` from the repo (set PYTHONPATH=src) to count things in the allowed
files.
