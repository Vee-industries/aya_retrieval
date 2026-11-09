# Panel R-100: LoCoMo as an outside benchmark after the freeze

Kevin (the researcher), 2026-11-06, "Yes, panel it", to: score the frozen model and base on LoCoMo's memory questions
after the freeze, the rules registered before anything is scored. Purpose: every pool of ours, sealed ones included,
is built from our own templates; a public benchmark built by someone else answers that better than data we make.

## The project in brief

LoRA on CohereLabs/tiny-aya-global for recall of facts that have scrolled out of a long chat, using a search tool
(`search_corpus` over earlier exchanges, passages returned as chunks), with coherence kept. Repo (read-only for you):
`C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`. Harness: `scripts/run_recall_eval.py`,
`src/aya_retrieval/harness.py`, `recall_tool.py`, `scoring.py`, `inference.py`. Arms: `tool_loop` (search tool, last
three exchanges in view) and `three_exchanges` (no tool). Our five kinds: `older`, `confirm`, `in_view`, `statement`,
`never_told`. Our test chats are 58 to about 200 messages; a 240-item scoring run takes about 12 minutes (about 3 s
an item) on a 10 GB card shared with the researcher's own use, memory capped at 0.85.

Schedule: model freeze Tue Nov 10; the sealed final run on Kevin's go (about Nov 11); write-up Nov 12; demo and
hosting Nov 13; submit by end of Nov 14. Judging rubric: write-up clarity, practical usefulness, code quality.

## LoCoMo, as read from its repo and paper (Maharana et al., ACL 2024, arXiv 2402.17753)

- Released file `data/locomo10.json`: 10 conversations (a subset of the paper's 50, the longest with the best
  annotations). Paper averages for the 50: 304.9 turns, 19.3 sessions, 9,209 tokens a conversation; up to 35 sessions.
- Two speakers (`speaker_a`, `speaker_b`), sessions with dates, turns with `speaker`, `dia_id` (D<session>:<turn>),
  `text`, some with an image caption. Made by two gpt-3.5-turbo agents from personas and event graphs; people edited
  about 15% of turns.
- QA list: `question`, `answer`, `evidence` (dia_ids holding the answer), `category` 1 to 5. Questions are third
  person about the speakers ("What did Caroline research?"). Categories, by the scorer's code: 1 multi-hop, 2
  temporal, 3 inference/commonsense, 4 single-hop (2 to 4 inferred from sample questions), 5 adversarial (no answer;
  the scorer gives 1 if the output says "no information available" or "not mentioned"). Paper counts for the 50:
  7,512 questions; per-category counts for the released 10 not yet read.
- Metric: token F1 after normalisation (lower case, punctuation and articles removed, Porter stemming); category 1
  split on commas. Reported overall F1: Mistral-7B 13.9; GPT-3.5-turbo 22.4; GPT-4-turbo 32.1; GPT-3.5-16K with RAG
  over dialog turns, top-5, 31.7 (retrieval recall at 5: 58.8%). Human 87.9.
- Licence of the data: CC BY-NC 4.0 (LICENSE.txt), non-commercial; research use allowed with attribution.
- The file is not downloaded yet. Kevin downloads it (our rule: he fetches sources); nothing is committed to the repo
  until the panel says what may be.

## Hard constraints

- Never open `src/aya_retrieval/pool_independent.py`, anything under `docs/independent_pool/`, or lines 452 onward of
  `src/aya_retrieval/pools.py` (sealed). Run no code; write nothing outside your reply.
- The benchmark must not choose or tune anything: the model is frozen before it is scored.
- No invented mechanisms; any change to LoCoMo's questions, scoring or format is a disclosed deviation.

## Questions

1. How is a LoCoMo conversation put through our harness: who is the user, what is in view, what the search tool
   indexes (turns, sessions), how dates and images are handled, and are questions kept in the third person or put to
   the model as the friend's own question?
2. Which categories are scored, with which metric (LoCoMo's own F1 and refusal check, and anything beside it), and
   which arms (base with the tool, v6 with the tool, base without the tool; v5?)?
3. All questions or a registered sample; GPU hours; when it runs relative to the freeze and the sealed run.
4. What is registered before scoring, what the write-up may claim from it, and what it must not.
5. Licence and data handling: what may enter the public repo (scripts only? results?), attribution.
