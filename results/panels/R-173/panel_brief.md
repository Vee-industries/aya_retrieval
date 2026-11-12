# Panel R-173: raise the write-up scores to 90+ honestly

## The request
The author (Kevin), 2026-11-12, after a blind reader scored the submission: "Yes, make them" (the reader's
wording fixes), then "also make sure you're running everything through a panel. get these up to 90+".

Orchestrator's reading of "90+": a fresh blind reader (Opus, same brief as round 1, never the same agent twice)
gives the whole submission 90 or more out of 100, and each write-up 9 or more out of 10 on clarity and on
practical usefulness. Round 1 gave 62/100; short write-up 6 and 5; long write-up 4 and 6.

## The project in five lines
A LoRA adapter (6.37) on Tiny Aya Global (3.35B) for a Lexsi Labs hackathon (Track 3, Agentic Fine-tuning;
problem statements: RAG fine-tuning and reliable tool calling). It searches an earlier chat it can no longer see.
The model is frozen and a sealed final test ran once (all registered rules passed). It beats the untrained model
by large margins. On outside-writer chats plain code that always searches recalls as well; training adds
deciding when not to search, clean tool calls, and declining questions with no answer. Submission due
2026-11-15 11:59 PM AoE; resubmission allowed, the latest counts.

## Files (all in this folder; read only what your lane needs; read nothing else on the machine)
Folder: C:\Users\Gaming\scratch\claude\C--Users-Gaming--claude-spares-spare-wcSF8M\3f7d989b-d009-44ac-9f86-64e88058f022\scratchpad\review
- round1_report.md: the round 1 reader's full report, with the orchestrator's checks of it. Read this first.
- ABSTRACT.md (form abstract, limit under 500 words), HF_ARTICLE.md (short write-up, about 5 pages),
  ARTICLE.md (long write-up, about 50 pages), README.md (GitHub README), MODEL_CARD.md,
  hf_data_card.md, hf_eval_logs_card.md (the two Hugging Face dataset cards).
- article_template.md and model_card_template.md: ARTICLE.md and MODEL_CARD.md are generated from these by a
  script that fills every {{name}} from committed results files. Edits to the long write-up go into the template.
- kv_voice_v2.md: the author's voice spec. All public prose follows it.

## Fixed rules (not open to the panel)
- No new training, no new model runs, no change to the frozen model or the sealed result.
- Never soften a negative result or hide a limitation; never overstate. A limitation may be moved or restated
  more clearly, never dropped.
- Every number in the write-up comes from a committed results file or an existing record.
- Voice spec applies: no em dashes, no "we" or "our", no marketing words, no hedges.
- Nothing is published without the author's yes.

## What the orchestrator wants to be true (the against lane argues with this)
1. All 16 of the reader's ranked changes should be adopted, plus fixes for every inconsistency in its section 6.
2. 90+ is reachable by wording, order, length and what is shown first, plus three small additions: a statement
   that the artifacts are public and un-gated, a sample row and loading line in each dataset card, and a cost
   comparison against a closed model computed from token counts already in the eval logs and a cited public
   price list.
3. One more round of fresh blind reading after the edits will show whether the target is met.
