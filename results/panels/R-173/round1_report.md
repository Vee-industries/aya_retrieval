# Round 1 blind reader report (Opus, 2026-11-12), with the orchestrator's checks

Scores: short write-up (HF_ARTICLE.md) clarity 6/10, practical usefulness 5/10. Long write-up (ARTICLE.md)
clarity 4/10, practical usefulness 6/10. Overall submission 62/100. Code quality not scored (no code seen).

## Orchestrator's checks of the report (done against the repo, 2026-11-12)
- CONFIRMED: ABSTRACT.md line 7 says "AuditKIT checks the scorer and CuratorKIT the training answers" (present
  tense). ARTICLE.md section 12 says "AuditKIT was not run on 6.37." The abstract overstates.
- WRONG: the reader said HF_ARTICLE.md's datasets collection link (no id suffix) is broken. Tested: the short
  link returns 200 with title "aya_retrieval datasets"; the README's long link 302-redirects to the short one.
  Both work.
- CONFIRMED (minor): ABSTRACT.md says "Per 60 recall questions at one chat length ... against the shipped seed's
  44 to 55". 46 to 55 is the one-length (58-message) range against whole chat; 44 to 55 is the both-lengths range
  against code. HF_ARTICLE.md line 54 has 46 to 55, line 98 has 44 to 55.
- CONFIRMED: "Kevin" appears ARTICLE 14, README 12, HF_ARTICLE 5, MODEL_CARD 3, eval-logs card 2, ABSTRACT 0.
  Every HF and GitHub link names the author anyway (KevinVaillancourt, Vee-industries).
- CONFIRMED: ABSTRACT.md is 496 words without the title line, 511 with it. Limit "under 500".
- NOT YET CHECKED: the other inconsistency items in section 6 below.

## Reader's validity notes
- Toolkit chain stated more strongly in the abstract than the long write-up supports; no file says in one place
  which toolkit touched the shipped model and how.
- Un-gated status never stated for the adapter or datasets.
- HF_ARTICLE.md does not link the models collection; MODEL_CARD.md links no dataset or collection.
- hf_data_card.md does not say whether the 300-chat sealed heldout and independent conditions are published, or
  how to rebuild them (seed 90311 is in ARTICLE.md only).
- Closed-model cost comparison (optional, preferred) absent, and no file says it was left out.
- Dataset cards: what is in each folder, but no row format, no sample row, no loading line, no pointer from a
  headline number to the file that holds it. Eval-logs card says "the 18 judges' marks" while write-ups say three
  judges.

## Reader's reasons
Short write-up clarity 6: clear structure, two figures, clean tables; but nearly every sentence carries two to
four numbers plus record ids; "code", "base", "arm", "Judge 1 decides." never defined; the first section after
setup is "1. When the chat fits, give it the whole chat", so a judge meets where the method loses before what it
wins.
Short write-up usefulness 5: real use case (memory for a small chat model); measured value narrow ("What training
adds there is deciding when not to search"; "Code that searches every turn is faster than 6.37 on every set");
the most practical evidence (clean tool calls, prompted baseline, toolkit defect and memory fix) is in ARTICLE.md
only.
Long write-up clarity 4: "Abstract" is 784 words; 452 record references; 9-column tables (section 6 code table,
section 10 cost); first figure after about 350 lines; codenames (fix17cs37, 7.1, Fix B, 17m) never collected.
Strengths: track-to-measure table (section 1), deviation list (section 5), plain limits (section 15).
Long write-up usefulness 6: clean first calls 180 of 180 vs base 52 of 136 (section 7), 441 of 441 vs 146 of 328
on LongMemEval-S (section 9); prompted baseline lowers base recall (section 8); "How to use" rule; AuditKIT
bootstrap defect (section 12); TRL loss memory fix 9.81 to 7.12 GiB.
Overall 62: valid, unusually rigorous, beats untrained model by large margins, reports strongest baselines
without softening; but the headline has to be pieced together from many qualified numbers, the win over the
strongest simple baseline is limited to generated chats and to the decision not to search, and the reliability
evidence that matches the track sits deep in the long file.
Length of ARTICLE.md: helps a judge checking a claim; hurts one reading in full (its abstract is longer than the
form abstract; results start at section 6).

## Reader's belief from the abstract alone
"Training lifts recall from about 8 to 28% to 85 to 90% on the project's own generated chats, but on
outside-written chats a plain always-search script recalls as well, so what training adds there is knowing when
not to search." Confirmed by the rest, with two changes: "declines 233 of all 470 answerable questions" reads as
neutral but is a main failure; the abstract implies AuditKIT checks the shipped model's scorer.

## Reader's ranked changes
HF_ARTICLE.md (1, 2, 5, 6 also for README top and ABSTRACT):
1. Top: one results table. Rows: sealed generated recall; outside-writer recall; outside-writer in_view,
   never_told, statement; LongMemEval-S judged right. Columns: base with tool, code that searches every turn,
   base with whole chat, 6.37.
2. "What was built": add the track-to-measure table from ARTICLE.md section 1.
3. Add a "Tool calls" paragraph from ARTICLE sections 7 and 9: clean first calls 180/180 vs 52/136; 441/441 vs
   146/328; right search decisions 296 to 298 of 300 vs base 180 to 193.
4. Add the prompted baseline (ARTICLE section 8) next to the code baseline: two fixed system prompts lower base
   recall (19 and 18, 15 and 20 of 120, against 26 and 27).
5. "How the toolkits chain" paragraph: AgentTune trains every adapter; CuratorKIT gate rejected 22 of 350 v6
   answers and accepted replacements went into 6.37's set; AuditKIT second scorer in development (959 of 960 on
   v3), not run on 6.37, found a bootstrap defect with a one-line fix.
6. Remove record ids and codenames from body text; one line saying ids are in RECORDS.md; define base, code,
   judge 1 on first use; "Kevin" -> "the author".
7. LongMemEval-S: state denominators once (500 questions, 30 with no answer, 248 judged, 15 of those with no
   answer); put the refusal first: "6.37 refuses 233 of the 470 questions that have an answer; base with the tool
   refuses 22"; add the mechanical gold-answer row (51/51/63 of 411).
8. Cost: three-row table (seconds and tokens per turn); "No comparison with closed models was made."; add models
   collection link.
ARTICLE.md:
1. Cut the 784-word abstract to the form abstract's length or less.
2. Right after it: the same one-table summary and both figures.
3. Glossary before section 3: base, code (always_search), arm, 6.37 = fix17cs37 seed 82, v5, v6, 7, 7.1, probe,
   hard_dev, heldout, independent, outside-writer sets, judge 1.
4. Move inline record ids into a closing "Records:" line per paragraph or table caption.
5. Split the 9-column tables (section 6 code table, section 10 cost) into two narrower tables each.
6. Section 11: move "What the ledger shows" to the start. Section 14: open with one sentence on what it covers.
7. Section 4: 3-row toolkit table (toolkit | what it did | ran on 6.37?), pointing to section 12.
8. Section 5: one-line summary of the deviation list; "Kevin" -> "the author".

## Reader's hard-to-follow sentences
ABSTRACT "Per 60 recall questions at one chat length"; ABSTRACT "facts never told, 37 and 36 against 31 and 24";
HF_ARTICLE "R-016 registered a reference that was left out of the sealed run"; HF_ARTICLE "Judge 1 decides.";
HF_ARTICLE "Kevin marked 50 lines blind before any judged number was read."; HF_ARTICLE "The answerable and
unanswerable split was read after the registered result."; README "read as a report on 6.37 once none was left";
README "development since R-151 (7 was designed from its failures)"; MODEL_CARD "so an invented value outside the
list passes (R-020)"; ARTICLE section 3 "the freeze panel's lane cited it in arguing for the freeze".

## Reader's inconsistencies (only the first is checked)
1. Seed 82 range 44-55 vs 46-55 (checked, see above).
2. ABSTRACT "6.37 declines 13 of the 15 unanswerable" vs README "declines on the 30 unanswerable: 21" (reader:
   13 is judged-right on a 15-question subset, not a decline count).
3. AuditKIT (checked, see above).
4. hf_data_card "The two outside-writer test sets" vs README data/blind_dev used "for development since R-151".
5. eval-logs card "Kevin's blind check of the scorer on 50 replies (R-139)" vs README "by Kevin and a second
   marker (R-139, R-144, R-145)".
6. eval-logs card "the 18 judges' marks" vs "three fresh Claude Sonnet judges".
7. HF_ARTICLE "right on 47 of its 71 lines" vs README "gets 63 of 114 on the short questions" (two measures, not
   labelled).
8. Coherence rule wording: rule "at least as often as base" vs result "more often".
9. Training peak memory: ARTICLE section 4 "7.81 to 7.84 GiB" vs section 12 "7.12 GiB" (v3 under lean loss, not
   6.37, unstated); HF_ARTICLE section 5 7.02 GiB is the sealed-run inference peak.
