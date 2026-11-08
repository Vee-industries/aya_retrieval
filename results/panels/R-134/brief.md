You are one expert on a panel for a research project. You WRITE NOTHING: no files (not even scratch files), no git commands that change anything. Read-only commands only (cat, sed -n, grep with explicit paths, head, ls, `python -c` that only prints). Plain words, no metaphors.

## The project
Lexsi AI Safety hackathon, Track 3. A LoRA adapter on CohereLabs/tiny-aya-global (3.35B) for recall of facts that have gone out of view in a long chat. The model sees only the last few exchanges and has a `search_corpus` tool over the earlier chat. It must search when a fact is out of view, answer directly when the fact is in view or the message is plain chat, say so when a fact was never told, and stay coherent (blind Sonnet judges mark replies against the base model).

Repo (read-only): `C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval`. Python: `../venv/Scripts/python.exe` from the repo, with `PYTHONPATH=src`.

## FORBIDDEN reads (sealed final-test data or private)
- `src/aya_retrieval/pool_independent.py`
- anything under `docs/independent_pool/`
- lines 452 onward of `src/aya_retrieval/pools.py` (the HELDOUT pool); lines 1-451 are allowed
- any file whose name contains "token"
Never grep recursively over `src` or `docs`; name files explicitly.

## Where things stand (Sunday 2026-11-08 afternoon, EST)
- The shipping copy is 6.37: `fix17cs37` seed 82, training set `data/screens/fix17cs37.jsonl` (1,094 rows), built by `scripts/records/build_r122.py` (removal only) from 6.31's set. It passed every gate at seeds 82, 83 and fresh seeds 94 to 96 (RECORDS.md R-128 to R-131).
- A one-agent panel (R-132) found no fix the data supported and said "no 7". Kevin has now asked for an extensive and varied panel of experts to discuss fixes. You are one of them. Think freshly; R-132 is one opinion, not a ruling.
- RECORDS.md is long. Read the index table at the top first, then entries by range: `awk '/^## R-132 /{f=1} /^## R-133 /{f=0} f' RECORDS.md`. Key entries: R-063, R-064, R-086 (gate at 82/83), R-076 (fresh-seed rule), R-094 (who-is-who slip gate), R-099/R-102 (messy-chat battery), R-110, R-114 (the replacement rule), R-115, R-120, R-121, R-122 to R-127 (removal tries), R-131, R-132, R-133 (6.37's battery at 82 and 83).
- The write-up's list of known failures: `docs/article_template.md`, the bullet list around "Forgetting read as wordplay" and "It sounds like" on facts in view, and "A search built from the wrong message".
- Training: `scripts/run_recall_train.py` (read it for the recipe, the loss masking and what rows look like). Eval rows with replies: `results/recall_eval/<set>_<name>_<seed>_seed_73157.json`, rows have id, kind, arm, message, reply, queries, correct; use arm == "tool_loop". Sets: probe, hd (hard_dev, written by another author), st_style, st_phone, st_fix, st_fixh (held-out corrections), st_asked, st_cc. Seed-level summaries for 6.37 at 94 to 96: `C:/Users/Gaming/scratch/claude/C--Users-Gaming-Desktop-Claude-s-House/389594c2-8513-47d9-80f1-1a28b96837f7/scratchpad/fresh_r131.txt` (you may read that one scratch file). Battery report: `PYTHONPATH=src ../venv/Scripts/python.exe scripts/records/battery_report.py fix17cs37`.
- 6.37's measured weaknesses (recounted): on `hard_dev` facts in view it misses 40 of 240 over seeds 82, 83, 94 to 96, and 32 of those replies open "It sounds like" and talk about a feeling. The set has 150 in-view rows; 22 open "It sounds like". Removing those 22 was already tried (6.34, from 6.33): the opener vanished but `hard_dev` in-view fell 78 to 69 over two seeds, the misses becoming searches and denials. Separately, about 25 of 41 `hard_dev` recall misses at 94 to 96 found the right line and left out the asked detail ("Your coach Rhys collected the keys" for "parakeets").
- New today (R-133, 6.37's messy-chat battery at 82 and 83, messy minus plain): lower-case typing costs facts in view 8 of 96 on the probe and 5 on `hard_dev` (v6: 1 and 3), a new gap by R-099's trigger; phone typing costs in-view 5 on the probe. The 19 lower-case in-view answers lost are all unsearched; they deflect ("You can ask your godfather about it.") or open "It sounds like" (11 of 19). So the in-view deflection is the one failure seen in three places: plain `hard_dev`, lower-case typing, phone typing. Corrections are fixed (0 and -1 of 192; v6 -187, -146).
- Do NOT read any result file for seeds 97, 98 or 99; those are the unread confirmation seeds.
- History: almost every additive change since v6 bought one line and cost another (R-115, R-120, R-121). 6.37 came from removal.

## Rules a fix must live with (do not propose changing these)
- Gates never move. A copy replaces 6.37 only by passing the full gate: R-086 whole, R-094, R-097, R-102 at seeds 82 and 83; then R-076's rule with Sheets A, B and h (three fresh judges), R-094's slips, recall not below the shipping copy's at the same seeds, and R-102's fresh-seed items, at unread seeds 97 to 99. Nothing may be tuned on a seed it is then confirmed on. Eval items are the same at every training seed; only the training seed is unread.
- Training rows come from the TRAIN pool only; `phone_style` never enters training; held-out pools stay sealed.
- New tries train from scratch on a changed set (Kevin 2026-11-07); a recipe change (loss masking, epochs, learning rate) is a changed run and is allowed if it is registered before training.
- Clock: 82-and-83 training must start by Sunday 22:00; fresh-seed training by Monday 04:00; nothing starts after Monday 12:00; model freeze Tuesday. One training run takes about 52 minutes; each eval about 5 to 11 minutes. The GPU is free from about 15:05.
- No invented rules: every number in a proposal comes from the data or the records, not a guess.

## What to return (under 600 words)
1. Your expert reading of the most fixable weakness, with numbers and the files they came from.
2. One concrete proposed fix (or "none"), precise enough to code: which rows of `fix17cs37.jsonl` change or are added (with counts you checked by reading the file), or which recipe setting changes and to what. Say why it should not repeat the trade-off pattern of R-115, R-120, R-121 and 6.34.
3. The measured line it should move, and which gate line it most risks.
4. Your confidence it replaces 6.37 under the full gate, as a rough probability, and why.
