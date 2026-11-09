# Panel R-100, round 2: the merged plan (ACCEPT, or ACCEPT IF with the one smallest change)

1. **Status: an outside check, never a decision.** It runs on the frozen model (Nov 10) and decides nothing: no
   tuning, prompt edit, candidate, seed or go for the sealed run rests on it. Losses and nulls are reported in full.
   [all lanes]
2. **Data.** Kevin downloads `locomo10.json`; its sha256 is registered. The data, its questions, answers and turns,
   and per-item outputs that quote them stay local, out of git. Committed: scripts, the hash, the registration,
   item ids (conversation, question index), aggregate numbers; a LoCoMo line in NOTICE with attribution (Maharana et
   al., ACL 2024, CC BY-NC 4.0). [lanes 2, 3, 4]
3. **Adaptation** [lane 1]: consecutive turns paired as (user, assistant) within each session, speaker names kept in
   the text ("Caroline: ..."); the last three exchanges of the conversation in view; one passage per older exchange
   indexed, one index per conversation, TOP_K 5; every exchange prefixed with its session date; images as "[shares a
   photo: <caption>]"; questions verbatim, third person, as the last user message; system prompts unchanged. Check
   that no exchange exceeds the chunk size; disclose if it does. Every item here is a listed deviation.
4. **Arms**: base with the tool, v6 (the frozen model) with the tool, base without the tool. v6 without the tool and
   v5 cut. [lanes 1, 2; lane 3 wanted the 2x2, lane 4 two arms]
5. **Sample**: a seeded draw registered before scoring, 500 questions from categories 1 to 4 in proportion plus 100
   from category 5, chosen by hash of the question text. [lane 3; lane 1 wanted all, lane 4 100 of category 4] About
   2 to 2.5 GPU hours for three arms.
6. **Scoring.** Primary: LoCoMo's own token F1 (its normaliser, stemming, category 1 comma split, category 3 first
   part), per category, and pooled over 1 to 4 for H1; category 5 by its refusal check, reported apart. Secondary,
   mechanical: gold-token recall (the share of gold tokens in the reply, because F1 penalises sentence replies),
   evidence recall at 5 (the share of evidence exchanges a search returned), search rate. No LLM judge. [lanes 1, 3;
   lane 2 asked for a judged sample]
7. **Registered hypotheses.** H1: v6 with the tool above base with the tool on pooled F1 (1 to 4); a gain counts only
   if the lower bound of a paired bootstrap 95% interval clustered by conversation (10,000 resamples; only 10
   clusters, stated) is above 0, with a sign test beside it. H2: v6's category 5 refusal rate not more than 5 points
   below base's. Results reported as relative increase over base. A floor result (both arms near the paper's weakest
   baselines) is declared uninformative in advance. [lanes 1, 2, 3]
8. **Timing.** Converter, scorer, registration: CPU only, Nov 7 to 9. The scorer is tested on gold-as-answer and on
   known-wrong answers; a format dry run uses 10 base items excluded from the sample, read for format only. The
   registration is committed before the first scored item, and if it is not committed by the end of Nov 9 the
   benchmark is dropped. The GPU run comes after the sealed final run (overnight Nov 11 to 12), never delaying it.
   [lanes 1, 2, 4; lane 3 wanted Nov 10 evening]
9. **Write-up**: its own section, "outside check, not the registered test", never in the sealed table. Allowed: "on
   an outside chat set built differently from our templates, the frozen model scored X against base's Y on the same
   questions", per category, with intervals. Forbidden: robustness to real chats, ranking against published systems
   (their scores printed only as context, "not comparable"), anything about the sealed result, any claim that the
   freeze was validated. [lanes 2, 4]

Reply in under 120 words: ACCEPT, or ACCEPT IF with the one smallest change and its reason.
