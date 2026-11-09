# Panel R-099: messy proxies in the training data?

Kevin (the researcher), 2026-11-06: "can we get some messy proxies in for training?" He asked after hearing that every
pool, sealed ones included, is built from templates, so a pass shows the model handles new words in our kind of
conversation, not real messy chats.

## The project in brief

LoRA on CohereLabs/tiny-aya-global for recall of facts that have scrolled out of a long chat, using a search tool,
with coherence kept. Repo (read-only for you): `C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`.
Five question kinds: `older` (fact out of view), `confirm` ("did i tell you about..."), `in_view` (fact on screen),
`statement` (friend shares news: just chat, no search), `never_told` (say you were never told).

- v6 = recipe "17m" seed 82: `data/screens/strict_chat.jsonl`, `--loss-on chat_decision`, rank 32, 3 epochs.
- Fix C2 (fix17z) is being screened now; if it passes it replaces v6.
- Model freeze Tue Nov 10. No training or scoring starts after Mon Nov 9 12:00. One candidate-seed is about 55
  minutes of GPU (training plus scoring). The queue is busy with C2 until about 15:00 today, then has spare time.
- Gates: R-086's gate (seeds 82, 83, counts and judged coherence sheets), R-076's rule (fresh seeds 88 to 90), R-094's
  slip gate. Pre-registered; a miss by one is a miss.

## Evidence already in hand (development, probe seed 73157, tool arm, 96 recall questions, 48 of each other kind)

Typing style (`stress.user_style`: lower case, sparse punctuation, some ellipses; R-067):

| | plain recall | styled recall | styled in_view / never_told / statement |
|---|---|---|---|
| base, probe | 30 | 38 | 28 / 41 / 30 |
| v5 seed 82, probe | (about 93-96) | 92 | 40 / 47 / 48 |
| base, hard_dev | 20 | 22 | 29 / 40 / 33 |
| v5 seed 82, hard_dev | 58 | 58 | 35 / 47 / 48 |

So lower-case texting style costs little. Bigger known gaps: `hard_dev` (unseen fact types and wording) recall 74 of
96 for v6 at seed 82 against 96 on the probe (R-068: the model writes the training pool's fixed query phrase for the
nearest training fact type); an earlier question still in view sends the search to the wrong message (R-076, R-081);
corrections ("scratch what i told you earlier") and 1,000-message chats have stress tests (R-067).

## Hard constraints

- Never open `src/aya_retrieval/pool_independent.py`, anything under `docs/independent_pool/`, or lines 452 onward of
  `src/aya_retrieval/pools.py` (the sealed held-out pool). Never open `data/` sealed files. Read only RECORDS.md,
  `src/aya_retrieval/pools.py` lines 1 to 451, `stress.py`, `conversations.py`, `pool_hard_dev.py`, `scripts/`,
  `docs/article_template.md`.
- Nothing from any other project's code or test sets may enter the repo.
- No invented mechanisms; anchor proposals in what real chats look like.
- Run no code; write nothing outside your reply.

## Questions

1. Which kinds of messiness are worth adding to training, given the evidence (what costs answers now)?
2. How are the messy rows made: rule-based noise on TRAIN templates, blind writer agents, or something else? Who can
   write them without having read the sealed pools or their brief, so training does not target the test's own spec?
3. Which base set does it go on (v6's or C2's), how many rows, and what must stay byte-identical?
4. What measure shows it worked, registered before the run, beside the existing gates? What is the stop rule?
5. Does it fit before Monday 12:00 alongside C2's remaining gate, and which goes first if they compete?
