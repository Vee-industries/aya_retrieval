Method lane, panel R-173. I read only the review folder. Edits that change only wording, order and what comes first can lift the write-ups' clarity scores to 8 or 9. They cannot get practical usefulness, or the overall score, to 9/10 and 90/100. Point 2 of the orchestrator's hopes, as worded, is likely wrong.

**1. Edit plan by file (priority order; the rubric line each one raises)**

**ABSTRACT (clarity, validity).**
1. Open with the lead claim in section 2 below (clarity, usefulness).
2. Fix the AuditKIT overstatement. Use the past tense and say it was not run on 6.37 (validity; fixed rule).
3. "declines 13 of the 15 unanswerable" is wrong. The 30-question count is a decline count; the 15-question count is a judged count. Write: "declines 21 of the 30 unanswerable questions (judged right on 13 of the 15 judged), and 233 of the 470 answerable" (validity).
4. Replace "Per 60 recall questions at one chat length" with labelled ranges: "46 to 55 at 58 messages; 44 to 55 at both lengths" (clarity).
5. Add the clean-call result (section 3 numbers) in one sentence, because it is the track's "reliable tool calling" measure (usefulness).
6. Keep the length at 480 words or fewer with the title line included.

**HF_ARTICLE (both rubric lines).** Adopt the reader's 8 changes, with these changes to them:
- **R1, summary table: adopt and widen.**
  - Keep the reader's four columns.
  - Add three rows: right search decisions; clean first calls; LongMemEval-S declines on answerable questions, next to the judged-right row so the refusal sits in the same view.
  - Write "not run" in empty cells (whole chat at 419 messages; whole chat on LongMemEval-S).
  - Use seed 82 counts throughout, with denominators in the row labels.
  - This table is where the strongest baselines are told first. That meets the "strongest baseline first" rule while the opening sentence names a win.
- **New section 2, "Which to use when".** The model card's "How to use it" rule, in three lines: whole chat if it fits; otherwise 6.37 or code, and the measured trade-off between them. Raises usefulness.
- **R2, track table: adopt and add a third column, "result".** Each track phrase then sits next to its number: when, 296 to 298 of 300 against 180 to 193; ignores distractors, the false-retrieval rule; grounds, rule 2.
- **R3, tool calls, and R4, prompted baseline: adopt.** They are the strongest evidence that training was needed. Word R4 as "for these two prompts".
- **R5, toolkit chain: adopt.** Add the TRL loss memory fix and the AuditKIT bootstrap defect with its one-line fix (ARTICLE section 12). The short file has neither, and both are directly useful to Lexsi.
- **R6, ids, codenames and "Kevin": change it.** Use "I", not "the author" (voice spec 7.1, first person singular for authorial acts): "I marked 50 lines blind." Move record ids to one "Records:" line per section. Define base, code, recall, judge 1, "clean call" and seed 82 at first use.
- **R7, LongMemEval-S: adopt as written.** The mechanical gold-answer row (63 against 51 of 411, p = 0.20) is a strongest-baseline result and must be shown.
- **R8, cost.** See section 5 below. Add the models collection link.
- Rewrite the reader's hard sentences:
  - "R-016 registered a reference..." becomes "A reference fixed before any training: code that searches on every turn."
  - "Judge 1 decides." becomes "Three judges mark each reply; the first judge's mark is the score, and the other two are reported."
  - Label "47 of 71" as judged and "63 of 114" as gold-in-reply.

**article_template (clarity 4 is the weakest line).**
- **R1: drop the 784-word abstract.** Fill the slot from the same template text as ABSTRACT.md, so the two cannot drift apart.
- **R2: adopt.** The summary table and both figures go right after the abstract.
- **R3, glossary: adopt, but move it.** Put it straight after the summary table, not before section 3, because the table already uses the terms. Cap it at 12 terms.
- **R4, ids: change to a partial move.** Take ids out of the abstract, section 1, and every section's first paragraph. Keep them in tables and in sections 11 to 14, where checking a claim is the purpose. Moving all 452 risks traceability for little gain on a file judges skim.
- **R5 to R8: adopt.** Split the four tables with 8 or 9 columns (the section 7 behaviour table and R-016 references table, the section 8 recall and prompted tables, the section 10 cost table). Section 11 opens with its findings. Section 14 gets an opening sentence. Section 4 gets a 3-row toolkit table. Section 5 gets a one-line summary.
- Fix the memory labels: 7.81 to 7.84 GiB is 6.37's training peak; 7.12 GiB is v3 under the loss fix; 7.02 GiB is the sealed-run inference peak.

**README top.**
- Replace the status block with the lead claim and the summary table.
- Add one line on access: adapter and datasets public and un-gated. Verify that on Hugging Face before writing it. The base model is gated (README line 246), so say that users accept Tiny Aya's licence.
- Move the quick-start command above the results.
- Rewrite "once none was left" and "since R-151 (7 was designed from its failures)" as plain sentences.

**MODEL_CARD template.**
- Move the scorer caveat and the statement-search count out of paragraph one into Limitations. Restate the caveat: "The scorer counts a decline as right when it names no listed value; a reply that invents a value not on the list also passes."
- Add the summary table, the dataset and collection links, and the gated-base line.
- Change "Kevin" to "I".
- A loading snippet only if it is copied from an already-tested README command. No new untested code.

**Data cards.**
- Field list and one sample row.
- A loading line, tested against the published repo (loading data is not a model run).
- A table linking each headline number to its file: sealed recall to `analysis/R-162/`, LongMemEval-S to `analysis/R-170/scores.json`.
- Say whether `heldout` and `independent` are published, and how to rebuild them (item seed 90311). The orchestrator must check this; I cannot from the folder.
- Fix the set 1 status: "set 1 became a development set when 7 was designed from its failures; set 2 was read by no decision that changed 6.37."
- Eval-logs card:
  - Replace "18 judges" with the true structure (three judges a sheet; confirm the 18 count from the records).
  - Name both blind checkers of the scorer (R-139, R-144, R-145).
  - Change "Kevin" to "I".
- Coherence rule wording everywhere: "rule: at least as often as base; result: more often, for every adapter under every judge."

**2. Lead claim (every file)**

"Trained with Lexsi's AgentTune, a LoRA adapter lets Tiny Aya Global (3.35B), shown only the last three exchanges of a chat, decide when to search the rest: on the sealed test (300 unseen generated chats in each of four conditions) recall rises from 8 to 28% for the untrained model with the same tool to 85 to 90% over eight seeds, and on LongMemEval-S all 441 of its first tool calls are clean against the untrained model's 146 of 328. On chats by outside writers, plain code that searches every turn recalls as well (42 and 47 of 120 against 39 and 53), so the measured gain there is deciding when not to search (answers in view, 35 and 37 of 40 against code's 13 and 16); a chat short enough to show whole is better shown whole."

**3. Practical usefulness: the case to make**

The use case is a memory layer for a small local chat model with reliable tool calls. Do not pitch it as a recall gain over a search script.

| Evidence | Numbers | Where |
|---|---|---|
| Clean first calls (LongMemEval-S) | 6.37 441 of 441; base 146 of 328 | ARTICLE s9 table |
| Ran out of calls (LongMemEval-S) | 6.37 0; base 12; code 31 | ARTICLE s9 table |
| Clean first calls (sealed) | 6.37 180 of 180 and 184 of 184; base 52 of 136 and 49 of 107 | ARTICLE s7 behaviour table |
| Right search decisions (sealed) | 6.37 296 to 298 of 300; base 180 to 193 | ARTICLE s7 behaviour table |
| Plain statements left unsearched | 6.37 37 and 35 of 40; code 0 | HF s2 |
| Declines on unanswerable questions | 6.37 21 of 30; base 2; code 0 | README LongMemEval table |
| Fits a 10 GB consumer card | inference peak 7.02 GiB; training 33 to 35 min a seed on an RTX 3080 | ARTICLE s10 |
| Tokens read a turn | 6.37 1,196 to 1,266; whole chat 3,227 to 3,610 | ARTICLE s10 table |
| Tokens written a turn | 6.37 26 to 27; base 36 to 38 | ARTICLE s10 table |
| A written prompt does not buy the gain | prompts A and B lower base recall to 19 and 18, and 15 and 20, against 26 and 27 | ARTICLE s8 |
| TRL loss fix (any 10 GB trainer can reuse it) | training peak 9.81 to 7.12 GiB, bit for bit | ARTICLE s12 |
| AuditKIT bootstrap defect | one-line fix | ARTICLE s12 |

The costs stated beside these:
- 6.37 declines 233 of 470 answerable questions on LongMemEval-S.
- Code is faster on every set (3.09 against 3.81 s a question).

**4. Scores these edits alone can reach**

| File | Reachable score | What caps it |
|---|---|---|
| HF_ARTICLE | clarity 8, 9 possible; usefulness 7 | On outside-written chats code matches recall. On LongMemEval-S 6.37 declines half the answerable questions, ties code on the answerable ones, and is slower. |
| ARTICLE | clarity 7; usefulness 7 | Length, ids in the deep sections, results starting at section 6. |
| ABSTRACT | clarity 8 | Needs fresh judging. |
| MODEL_CARD | 8 | Same measured results as HF_ARTICLE. |
| Data cards | 8 to 9 | A sample row and a loading line are concrete fixes. |
| Overall | 74 to 80, not 90 | The round 1 reader's overall reasons. |

The round 1 reader's overall reasons were "the win over the strongest simple baseline is limited to generated chats and to the decision not to search". Wording cannot change that. The one lever not yet used: round 1 saw no code. If the hackathon judges get the repo, the next blind reader should get it too, so code quality is scored.

Method points for the next round:
- Use two fresh readers, not one. One reader's score is too noisy to say the target is met.
- Do not show them the round 1 report.
- Adopt only changes a real judge's rubric rewards, not this reader's preferences.

**5. Closed-model cost comparison**

Partly buildable. These figures are already in the files:

| Set | Figures | Where |
|---|---|---|
| Sealed | tokens read a turn (base 1,148 to 1,154, 6.37 1,196 to 1,266, whole chat 3,227 to 3,610); tokens written a turn (36 to 38 against 26 to 27); seconds a conversation | ARTICLE s10 table |
| LongMemEval-S | tokens read a question (4,055, 3,794, 3,161, 1,730); seconds; words a reply; the 60-token cap | ARTICLE s9 table |
| LongMemEval-S | history of about 115,000 tokens a question | README |

From outside it would need:
- A named closed model's dated public price per million input and output tokens, with the URL.
- A tokenizer conversion, or a stated note that these are Tiny Aya token counts.
- Card power draw and an electricity price, or a cloud GPU hourly price, for the local side. The files hold seconds, not watts.
- LongMemEval-S output tokens, which are not counted. Only words a reply and the 60-token cap exist.
- The computation committed as a results file with a record, so the number meets the "from a committed file" rule.

Even built, it compares the price of reading the same tokens, not the price per right answer. No closed model was run, and the rules forbid running one. It must say so in one sentence. If that cannot be done and approved before 15 November, write "No comparison with closed models was made." It lifts usefulness by one point at most.
