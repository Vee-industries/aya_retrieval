# Panel R-178: a new sealed test and a fix for 6.37's weakness

## The request
Kevin (the author), 2026-11-12: "i want to address the weakness. explain how we caught it that we opened the project
back up sealed a new test and started working again". Read RECORDS.md entries R-175, R-176 and R-177 in the repo
first (grep for "## R-175", "## R-176", "### R-176 result", "## R-177"; read only those entries).

## Project in brief
A LoRA adapter (6.37, rank 32, all seven projections, 3 epochs, lr 3e-4, `--loss-on chat_decision`, data
`data/screens/fix17cs37.jsonl`, 1,094 rows) on Tiny Aya Global (3.35B), for a Lexsi Labs hackathon (Track 3). The
model sees the last three exchanges of a chat and can call a full-text search tool over older exchanges (OR matching,
`match_all=False`; each passage is a whole exchange, the user's message and the model's reply). Training rows are
generated from fact templates in the repo's pool code. Sealed result (R-162/R-163): recall 91 to 107 of 120 against
base 13 to 32. Outside-writer chats (Claude Opus agents): code that searches every turn matches 6.37's recall;
the whole chat beats both when it fits.

## Weaknesses found after the freeze (R-175 to R-177)
1. Query writing learned from few fact templates; an untrained fact type ("fixed the leak under the sink") gets a
   memorized query ("sister broke skiing injury").
2. An unrelated passage is given as the answer instead of "never told".
3. Its own wrong answer in view is repeated on later questions (6 of 8 in R-176).

## Constraints
- Deadline: submission 15 November 11:59 PM AoE (= 16 November 11:59 UTC); resubmission allowed, the latest
  counts. Shortlisted teams (16 November) have until 22 November to "prove their thesis" with slides or video.
- Card: one RTX 3080, 10 GB, shared with the author's games; one GPU job at a time under a lock. Training about
  35 minutes a seed; a full probe scoring run about 15 to 25 minutes.
- History: every candidate after 6.37 (6.38, 6.39, 7, 7.1) failed a registered gate; seed-to-seed noise on dev pools
  is about 20 points; 40 candidate sets were screened on reused dev pools (R-141, R-157).
- Sets already read and usable for development: probe, hard_dev, both outside-writer sets (blind_dev, blind_dev2),
  the sealed heldout and independent pools (read once, R-163), LongMemEval-S (read), the demo (read).
- Rules: a panel before a change of method; every number from a committed file; never soften or overstate; voice
  spec for prose; nothing pushed or published without the author's yes.

## Read limits
Repo: C:\Users\Gaming\Desktop\hackathons\Lexsi Sprint\aya_retrieval. You may read RECORDS.md (the named entries,
and others by grep if needed), README.md, docs/ARTICLE.md, docs/demo.md, scripts/, src/aya_retrieval/ files other
than pools.py, results/analysis/. Do not open src/aya_retrieval/pools.py beyond line 451, or any file under data/
named heldout or independent, or results/longmemeval/. Edit nothing, run no model, no git write.
