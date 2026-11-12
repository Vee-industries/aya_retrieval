Judge review: aya_retrieval (Track 3). I read only the seven files in the review folder. I did not open the SOP, because the brief limited reading to those files. No file was edited.

## 1. Validity

What is shown and linked:
- **Public adapter:** linked.
- **Two Hugging Face datasets and both collections:** linked in README.md.
- **Public GitHub repo:** linked, with setup, pinned toolkit commits, and train and run commands.
- **Before-and-after metrics:** many.
- **Core model:** Tiny Aya Global, which is an Aya model.

Gaps a judge will notice:
- **Toolkit chain is stated more strongly than the long write-up supports.** ABSTRACT.md says "AuditKIT checks the scorer and CuratorKIT the training answers" in the present tense. ARTICLE.md §4 says "no AuditKIT run on 6.37 exists", and the CuratorKIT gate ran on "v6's found-fact training answers". The rule of two chained toolkits (AgentTune plus CuratorKIT) is likely met. But no file says in one place which toolkit touched the shipped model, and how.
- **Un-gated status is never stated** for the adapter or the datasets. A judge has to click through to check.
- **Links:**
  - HF_ARTICLE.md links the datasets collection as `collections/KevinVaillancourt/aya-retrieval-datasets`, without the id suffix that README.md uses (`...-6af35d3cf9a91556f52af373`). This link is probably broken.
  - HF_ARTICLE.md does not link the models collection.
  - MODEL_CARD.md links no dataset or collection.
- **Sealed test chats are missing from the dataset card.** hf_data_card.md lists the training sets and the two outside-writer sets only. It does not say whether the 300-chat sealed `heldout` and `independent` conditions are published, or how to rebuild them (item seed 90311 is in ARTICLE.md only).
- **Cost comparison with closed models (optional, preferred):** absent. Only latency against an always-search script is given, and no file says the closed-model comparison was left out.
- **Double-blind:** the byline and about 30 uses of "Kevin" (ARTICLE.md 14, README.md 12, HF_ARTICLE.md 5, MODEL_CARD.md 3, the eval-logs card 2) name the author. ABSTRACT.md has none. Inside the text, "Kevin" is also never introduced to a stranger.
- **Abstract length:** 496 words without the title and 511 with it, against "under 500". Check how the form counts.

Dataset cards:
- **hf_data_card.md:** says what is in each folder, but not the row format, has no sample row, and gives no loading line. A judge can see what is there but not how to use it.
- **hf_eval_logs_card.md:** the folder map and the note on LongMemEval being "not redistributed" are clear. It has no file format, no sample, and no pointer from a headline number to the file that holds it. It also does not explain "the 18 judges' marks" when the write-ups say three judges.

## 2. Scores

Code / notebook quality: skipped, since I cannot see the code.

**HF_ARTICLE.md (short write-up)**
- **Clarity: 6/10.**
  - Clear structure ("What was built", numbered sections, "6. Limits") with two figures and clean tables.
  - Nearly every sentence carries two to four numbers plus record ids.
  - Terms like "code", "base", "arm" and "Judge 1 decides." are never defined.
  - The first section after the setup is "1. When the chat fits, give it the whole chat". A judge meets a result where the method loses before seeing what the method wins.
- **Practical usefulness: 5/10.**
  - The use case is real: memory for a small chat model.
  - The measured value is narrow: "What training adds there is deciding when not to search". "Code that searches every turn is faster than 6.37 on every set."
  - The most practical evidence is in ARTICLE.md only: tool calls that are clean every time, the prompted baseline, and the toolkit defect and memory fix.

**ARTICLE.md (long write-up)**
- **Clarity: 4/10.**
  - The "Abstract" is 784 words, there are 452 record references, and some tables run to 9 columns (§6 code table, §10 cost).
  - The first figure comes after about 350 lines.
  - Codenames ("fix17cs37", "7.1", "Fix B", "17m") are never collected in one place.
  - Its strengths are real: the table mapping the Track 3 statement to the measures (§1), "Every deviation from the registered plan, in one place" (§5), and plain limits (§15).
- **Practical usefulness: 6/10.**
  - It has what a builder needs: clean first calls "180 of 180" against base's "52 of 136" (§7), and "441 of 441" against "146 of 328" on LongMemEval-S (§9).
  - It shows the prompted baseline, where both prompts lower base recall (§8), and a "How to use" rule: show the whole chat when it fits.
  - Two engineering findings are useful: "AuditKIT's paired bootstrap does not centre its resamples" (§12), and the TRL loss memory fix from 9.81 to 7.12 GiB.

**Overall (whole submission): 62/100.**
- **For:** valid and unusually rigorous (registered, frozen, sealed). It beats the untrained model by large margins and reports its own strongest baselines without softening them.
- **Against:** the headline has to be pieced together from many qualified numbers. The win over the strongest simple baseline is limited to generated chats and to the decision not to search, and the reliability evidence that matches the track sits deep in the long file.

**Does ARTICLE.md's length help or hurt?** It helps a judge who opens it to check a claim, since every number has a table, a deviation entry or a record. It hurts a judge who reads it in full: the abstract alone is longer than the form abstract, and the results start at §6.

What a judge needs from it that HF_ARTICLE.md lacks:
- the table mapping the track statement to the measures;
- clean-call and right-decision counts;
- the prompted baseline;
- the false-retrieval (rule 3) and coherence (rule 4) tables;
- the deviation list;
- the toolkit findings (§12);
- the LongMemEval mechanical table (gold answer in the reply, 51 / 51 / 63).

## 3. First belief from the abstract alone

The belief: "Training lifts Tiny Aya's out-of-view recall from about 8 to 28% to 85 to 90% on the project's own generated chats, but on outside-written chats a plain always-search script recalls as well, so what training adds there is knowing when not to search."

The rest of the write-up confirmed this. It changed two things:
- The abstract's "declines 233 of all 470 answerable questions" reads as a neutral count. The write-ups show it is a main failure: half the answerable LongMemEval-S questions are refused.
- The abstract implies AuditKIT checks the shipped model's scorer. ARTICLE.md says AuditKIT never ran on 6.37.

## 4. Changes, ranked

These change only wording, order, length, figures, or what is shown first.

**HF_ARTICLE.md (also apply 1, 2, 5 and 6 to the README top and ABSTRACT.md)**

1. **Top, after the byline: add one results table.**
   - Rows: sealed generated recall; outside-writer recall; outside-writer `in_view`, `never_told`, `statement`; LongMemEval-S judged right.
   - Columns: base with tool, code that searches every turn, base with whole chat, 6.37.
   - Why: the strongest baselines and the method sit side by side in the first thing read, which is the fastest honest summary.
2. **"What was built": add the track-to-measure table from ARTICLE.md §1.** Judges score against the problem statement, and this table does that mapping for them.
3. **Add a "Tool calls" paragraph using ARTICLE.md §7 and §9:** clean first calls 180 of 180 against base's 52 of 136, and 441 of 441 against 146 of 328. Right search decisions 296 to 298 of 300 against base's 180 to 193. This matches the track's "reliable tool calling" and is now missing from the short write-up.
4. **Add the prompted baseline (ARTICLE.md §8) next to the code baseline in §2.**
   - Wording: "Two fixed system prompts on the untrained model lower its recall on both sets (19 and 18, 15 and 20 of 120, against 26 and 27)."
   - Why: "did you try prompting?" is a judge's first question.
5. **Add a "How the toolkits chain" paragraph or small figure:**
   - AgentTune trains every adapter.
   - CuratorKIT's grounding gate rejected 22 of 350 v6 answers, and its accepted replacements went into 6.37's set.
   - AuditKIT was a second scorer in development (959 of 960 agreement on v3) and was not run on 6.37. It surfaced a bootstrap defect, with a one-line fix.
   - Why: this makes the validity item explicit and shows a finding the organizers will value.
6. **Remove record ids and codenames from body text** (13 ids, plus "fix17cs37" and "R-016 registered a reference..."). Keep one line saying ids are in RECORDS.md. Define "base", "code" and "judge 1 decides" on first use. Replace "Kevin" with "the author".
7. **§4 LongMemEval-S: state the denominators once, then move the refusal to the first bullet.**
   - Denominators: 500 questions, 30 with no answer, 248 judged, of which 15 have no answer.
   - Wording: "6.37 refuses 233 of the 470 questions that have an answer; base with the tool refuses 22."
   - Add the mechanical gold-answer row (51 / 51 / 63 of 411) from README.md.
8. **§5 Cost: turn the bullets into a three-row table** (seconds and tokens read per turn). Add: "No comparison with closed models was made." Fix the datasets collection link and add the models collection link.

**ARTICLE.md**

1. **Cut "## Abstract" from 784 words to the form abstract's length or less.** Move the per-set pairs into §6 to §9, where they already appear.
2. **Right after the abstract: add the same one-table summary as HF_ARTICLE.md change 1, and both figures.** Today the first figure is in §6.
3. **Add a glossary table before §3:** base, code (`always_search`), arm, 6.37 = `fix17cs37` seed 82, v5, v6, 7, 7.1, `probe`, `hard_dev`, `heldout`, `independent`, outside-writer sets, judge 1.
4. **Move inline record ids into a closing "Records:" line per paragraph or table caption.** 452 inline ids break most sentences into fragments.
5. **Split the 9-column tables** (§6 code table, §10 cost table) into two narrower tables each. They wrap badly on GitHub.
6. **§11: move "What the ledger shows" from the end to the start.** §14: open with one sentence on what the list covers.
7. **§4 "The Lexsi toolkits": add a 3-row table** (toolkit | what it did | ran on the shipped 6.37?). Point to §12 for the AuditKIT bootstrap defect.
8. **§5 deviation list: add a one-line summary drawn from the list's own text.** Example: "Deviation 7 added the two references reported in sections 6 and 7; R-163's pass rules did not depend on them." Then replace "Kevin" with "the author" throughout.

## 5. Sentences hard to follow on first reading

1. ABSTRACT.md: "Per 60 recall questions at one chat length" (which length, which arms?)
2. ABSTRACT.md: "facts never told, 37 and 36 against 31 and 24" (the reader does not know what counts as right)
3. HF_ARTICLE.md: "R-016 registered a reference that was left out of the sealed run"
4. HF_ARTICLE.md: "Judge 1 decides."
5. HF_ARTICLE.md: "Kevin marked 50 lines blind before any judged number was read."
6. HF_ARTICLE.md: "The answerable and unanswerable split was read after the registered result."
7. README.md: "read as a report on 6.37 once none was left"
8. README.md: "development since R-151 (7 was designed from its failures)"
9. MODEL_CARD.md: "so an invented value outside the list passes (R-020)"
10. ARTICLE.md §3: "the freeze panel's lane cited it in arguing for the freeze"

## 6. Inconsistencies between files

1. **Seed 82 range at one chat length.**
   - ABSTRACT.md: "at one chat length... against the shipped seed's 44 to 55".
   - HF_ARTICLE.md §1: "against 6.37's 46 to 55 with the tool".
   - ARTICLE.md §7: 46 to 55 is the 58-message range, and 44 to 55 covers both sizes. Code's "14 to 32" also covers both sizes (15 to 32 at 58 messages).
2. **LongMemEval-S questions with no answer.**
   - ABSTRACT.md: "6.37 declines 13 of the 15 unanswerable questions".
   - README.md: "declines on the 30 unanswerable: 21".
   - The 13 is judged-right on a 15-question subset, not a decline count.
3. **AuditKIT.**
   - ABSTRACT.md: "AuditKIT checks the scorer".
   - ARTICLE.md §12: "AuditKIT was not run on 6.37."
4. **Status of `blind_dev`.**
   - hf_data_card.md: "The two outside-writer test sets".
   - README.md: `data/blind_dev/` is used for "development since R-151".
5. **Human check.**
   - hf_eval_logs_card.md: "Kevin's blind check of the scorer on 50 replies (R-139)".
   - README.md: "by Kevin and a second marker (R-139, R-144, R-145)".
6. **Number of judges.**
   - hf_eval_logs_card.md: "the 18 judges' marks".
   - HF_ARTICLE.md and README.md: "three fresh Claude Sonnet judges".
7. **Base reading only the evidence sessions** (two measures, neither labelled in the short files).
   - HF_ARTICLE.md: "right on 47 of its 71 lines".
   - README.md: "gets 63 of 114 on the short questions".
8. **Coherence rule wording (minor).**
   - HF_ARTICLE.md rule: "judged coherent at least as often as base".
   - ABSTRACT.md result: "rated every adapter coherent more often". Both can be true, but stating the rule beside the result in one sentence would remove the doubt.
9. **Training peak memory (minor, ARTICLE.md internal).**
   - §4: "peaking at 7.81 to 7.84 GiB".
   - §12: "training peaks at 7.12 GiB". This is v3 under the lean loss, not 6.37, but the text does not say so.
   - HF_ARTICLE.md §5 gives 7.02 GiB, the sealed-run inference peak, right after the training time.
