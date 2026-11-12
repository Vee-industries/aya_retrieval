AGAINST LANE, panel R-173. Sources: the review folder only. No file edited.

## 1. The three beliefs

**Belief 1 (adopt all 16 changes plus every section 6 fix) is wrong as stated.** At least seven of the changes overstate something or drop a limitation if they are done the way the reader worded them (see part 2). Three of the section 6 "inconsistencies" are not inconsistencies, and "fixing" them would put an error in:
- **Item 8.** The rule is "coherent count at or above base's" (ARTICLE section 5). The result is "Every adapter is above base under every judge" (section 7). Both statements are true. Rewording either one misstates the rule or undersells the result. Leave both as they are.
- **Item 6.** "18 judges' marks" is probably a count of judge runs, not of judges. The sealed run had "The 33 judges took 53 to 129 s". So 18 is likely 3 judges times 6 sheets. Do not change it to "three"; label it.
- **Item 9.** The three memory figures (7.81 to 7.84, 7.12 and 7.02 GiB) measure three different things. Each needs a label, not a reconciliation.

The reader also missed real overstatements of the same kind it caught:
- HF_ARTICLE line 30 says "AuditKIT re-scores recorded replies as a check on the scorer" in the present tense, the same defect as the abstract.
- The data card, HF_ARTICLE and ABSTRACT all say CuratorKIT "checked the training answers". ARTICLE section 12 says it ran "over v6's found-fact training answers" (350 of them). 6.37's 1,094 rows include later rows (corrections, statements, contrast lines) that it never saw.

**Belief 2 (90+ by wording alone) does not hold.** Section 4 below gives the full case. In short, the practical-usefulness score is capped by the results, not by the prose: "Code that searches every turn is faster than 6.37 on every set" (HF_ARTICLE line 131).

**Belief 3 (one more fresh blind read will show it) does not hold.** One reader is a sample of one, with unknown variance. It is the same model family that wrote the prose, the outside-writer chats and every judge's marks. And the edits were made to its own rubric, so a rise in its score measures fit to that rubric. Section 3 gives a better setup.

## 2. Changes that would overstate, hide or break a rule, and the safe version

1. **HF change 1 and ARTICLE change 2 (one summary table).**
   - The "base, whole chat" column does not exist for LongMemEval-S, and for the generated sealed chats it exists at 58 messages only. "Base, evidence only" is a reading ceiling, not a baseline, so it must not fill that cell.
   - The code and whole-chat arms ran against seed 82, not the eight pooled seeds. The 6.37 cell must therefore be seed 82: 91 to 107 of 120, which is 76 to 89%, not 85 to 90%.
   - In the statement row, code's 0 and whole chat's 40 are "by construction".
   - The LongMemEval row of 53/34/40 hides p = 0.12 against code, the post-hoc split, and "6.37 declines 233 of all 470 answerable".
   - **Safe version:** every not-measured cell says "not measured (does not fit 10 GB)". By-construction cells are marked. LongMemEval gets an answerable-only row and a declines row. The outside-writer recall row comes first, and base with the whole chat (71 and 65 of 120) is shown as the strongest arm on it.
2. **HF change 3 (tool calls).**
   - "180 of 180 vs 52 of 136" has different denominators. "Clean" means "nothing written after them". The write-up must say whether unclean calls still ran; if they did, this is mostly a format measure.
   - The 296 to 298 right decisions are on generated chats. On the outside-writer chats 6.37 is below base on statement: "37 against 38, 35 against 39", and "eight of the eight seeds below base" on set 2.
   - **Safe version:** carry the definition, both denominators, and the outside-writer statement result in the same paragraph.
3. **The phrase "what training adds is deciding when not to search" (already in ABSTRACT, HF section 2 and README).** It is true against code only. Base with the tool already avoids searching more often than 6.37 does. **Safe version:** "Base searches too little and code searches every turn. Training adds searching when the answer is out of view (against base) and not searching when it is in view (against code)."
4. **HF change 5 (how the toolkits chain).**
   - "One-line fix" must say it is the project's proposed fix. ARTICLE section 16 lists "Offer ... the bootstrap fix to AuditKIT" as future work.
   - The CuratorKIT sentence must say it gated v6's 350 found-fact answers, not 6.37's set.
   - **ARTICLE change 7:** the "ran on 6.37?" column must read "AuditKIT: no; CuratorKIT: on an ancestor set only". Do not mark CuratorKIT "yes".
5. **HF change 6 and ARTICLE change 4 (strip record ids).**
   - Per-sentence ids are what separate registered results from post-hoc ones: "Added after reading the registered result". They also carry the late disclosures (R-167).
   - A per-paragraph "Records:" line loses that mapping, and any consistency checker or `make_article.py` step that keys on ids must be checked before ids are removed.
   - **Safe version:** keep inline ids on every registration, deviation, post-hoc and limitation sentence, and move the rest to captions.
   - "Kevin" becomes "the author (not an independent marker)" on the human checks. This makes a limitation clearer; plain "the author" would bury it.
6. **ARTICLE change 1 (cut the 784-word abstract to form length).** ABSTRACT.md drops limitations the long abstract carries:
   - seed 82's set 1 p = 0.047, "above the registered 0.01";
   - seed 82 is the lowest of the eight seeds;
   - the tag-question failure, which corrects only "1 and 3 of 20";
   - the coherence judges were "never checked against a person".

   The rules allow a limitation to move, never to drop. **Safe version:** a short limits paragraph that keeps all four, directly after the cut abstract.
7. **ARTICLE change 5 (split the wide tables).** Split them by set, not by arm. Splitting by arm separates base with the whole chat (71 and 65) from the code-against-6.37 comparison.
8. **ARTICLE change 6 (move "What the ledger shows" to the start).** It would then open on "6.37 is the only copy after v6 that passed every registered line". **Safe version:** open with the noise sentence, "`hard_dev` recall moves between training seeds alone ... by more than most changes moved it", and with the fact that 40 candidates were screened on reused development pools.
9. **ARTICLE change 8 (a one-line deviation summary).** It must not read as "every deviation only made the test harder". That was true of the amendments, not of the deviations. **Safe version:** "Ten deviations; three found by the write-up's reviewer and first disclosed in R-167; none changes a pass rule."
10. **ABSTRACT's LongMemEval sentence (current, not on the reader's list).** It leads with "53 ... 34 (p = 0.014)" and leaves out that the answerable split is 40 against 32, p = 0.29. Put the condition first.
11. **ABSTRACT's last line.** "For longer chats the adapter matches code" overstates. The outside-writer chats are about 1,400 tokens with an artificial three-exchange view; only LongMemEval is actually long.

## 3. Tuning to one LLM reader

**What would raise an LLM reader's score but not a human's:**
- glossaries, denominators in every sentence, deviation lists, record-id hygiene;
- explicit framing sentences such as "This is a result, not only a limit";
- matching the rubric it wrote.

**What would raise a human founder's score but not an LLM's:**
- one sentence on what it is for;
- a runnable snippet or demo;
- a clear answer to "why not always-search code, or a model with a longer context?"

An industry judge will see that a free script matches recall and is faster. No rewording changes that. Founders also skim: the HF article and README top are what get read.

**How to set up the next round so its score means something:**
- **Readers:** at least 4, from at least two model families, and one human if possible.
- **Noise floor:** each reader also scores the unchanged round 1 text, blind to which version is which.
- **Criteria:** give them the hackathon's published judging criteria, not this panel's rubric.
- **Code:** give them the repository, since code quality was unscored in round 1.
- **Time limit:** a skim budget for the short write-up.
- **Two extra measures, fixed before reading:**
  - a list of every claim the reader thinks the data does not support (the overstatement count must not rise);
  - a factual quiz, for example "Does 6.37 beat plain code on outside-writer recall?" (the right answers must not fall).
- **Decision rule:** register the target and the rule before reading.

## 4. Is 90 reachable?

Not honestly, without new results.

**Clarity:** 8 to 9 is reachable by editing.

**Practical usefulness is capped by what was measured:**
- Shown the whole chat, the untrained model is better.
- When the chat does not fit, plain code matches recall and is faster.
- On LongMemEval-S, code finds more evidence (372 against 333), 6.37 is judged right on 53 of 248 (21%), and it declines half the answerable questions.
- The recall win over code is on the project's own generator only.
- No gated-search heuristic baseline was tried ("no other retrieval system was tried"). A cheap rule could plausibly capture "when not to search".

**Honest ceiling:** usefulness about 6 to 7 out of 10, and overall about 72 to 80. A reader who gives usefulness a 9 after these edits is a sign the prose now overstates, not that the work improved.

## 5. The closed-model cost comparison

It could mislead in seven ways:
1. **It may break a fixed rule.** A public price is neither a committed results file nor an existing record. It must first be recorded as one, with its URL, model version and date read.
2. **Tokenizer mismatch.** The token counts come from Tiny Aya's 262,144-word vocabulary; a closed model counts the same text differently. State the size of that difference, or recount with the closed model's tokenizer offline, which is not a model run.
3. **Cost without accuracy.** No closed-model run is allowed, so there is no cost per right answer. A closed model could read the whole 115,000-token LongMemEval history. The comparison must say "accuracy of the closed model not measured" and must not imply 6.37 is a substitute.
4. **A per-token fee compared with local hardware.** It must state the local side: card, power, and the training time of 33 to 35 minutes a seed.
5. **What "tokens read per turn" counts.** Each search adds a model call that re-reads the context. State whether the figure sums every call.
6. **The cheapest arm.** The table must include code that always searches, which is already cheaper and faster than 6.37.
7. **Price terms.** Give input and output prices separately, and say whether caching or batch discounts were excluded.

## 6. Errors or overstatements in round1_report.md beyond the marked WRONG item

- **The reader's belief, "85 to 90%".** That is the eight-seed pool. The shipped seed is 76 to 89%. The abstract invites the same misreading.
- **The un-gated addition.** The README says "Tiny Aya is gated: accept the licence". A plain "the artifacts are un-gated" misleads about reproducing the work unless it says the base model is gated. Check the adapter and datasets' gate status on the Hub from outside before stating it.
- **"Sample row and loading line".** The sample must not come from the sealed pools or from LongMemEval text, which "are not redistributed". The loading line must be tested: subfolders with mixed formats may need `data_files`.
- **HF change 8's "No comparison with closed models was made."** This contradicts belief 2's plan to add one.
- **The reader's "TRL loss memory fix 9.81 to 7.12 GiB".** That is v3. 6.37 trained at 7.81 to 7.84 GiB, so it must not be presented as 6.37's figure.
- **Inconsistency item 4 is a real overstatement, not a wording clash.** The data card calls `blind_dev` a "test set" when it has been "development since R-151".
- **Inconsistency item 2.** "Declines 13 of the 15" mixes judged-right with declines. The safe wording is "judged right on 13 of 15; declines 21 of 30".
- **Double-blind.** The byline names Kevin Vaillancourt, and every HF and GitHub link names the author. Changing "Kevin" to "the author" in the body does not make the submission anonymous. If the hackathon requires anonymity, that is the author's call, and the rules should be checked. If it does not, the change is cosmetic.
