# Editorial and research review: ARTICLE.md and HF_ARTICLE.md

Reviewer: subagent, 2026-11-15 (11:35 Eastern at start). Line numbers are the built files'. Every number below was checked against the papers, `results/s3/ship_rule.json` or Appendix A/C; none disagreed. Not checked: `scoring.py` (not on the read list), the figures, the templates line by line.

## 1. Prioritized corrections and improvements

1. **HF Claim (HF 5-7) omits the false-memory faults**, which brief section 1 names as the main contribution. A reader who stops there does not learn 6.37 is worse than base on both S3 faults. P1.
2. **Whole chat at 419 messages (long 79-81, 767-768).** "at 58 messages and at 419 ..., recall above base, code and the whole chat" claims a win over a baseline that never ran at 419 (Appendix A: "58 messages only"; R-166). HF 111-114 is correct. P2.
3. **N-hit Terms differ from the scorer description.** Long 138-139 and HF 24: "a value listed for the chat"; long 774, HF 171, 200: "of the asked category listed for the chat". R-298's "other stored facts too" needs the second. Author to confirm against `scoring.py`.
4. **Statements as a gain over code (long 177-180).** Code fails statements by construction (long 434, 443), so this is not a measured gain. P3.
5. **"what ships did not depend on the change" (long 590-592)** rests on an unrun third K1.3 seed needing 5 or fewer of 236, against the run seeds' 9 and 28 (Appendix C 1091). Likely, not shown. P4.
6. **LongMemEval-S "53 against 40" reads as a lead (HF 122, long 24-25).** On the 233 answerable questions they tie 40 against 40 (long 481-483); the gap is the 15 unanswerable ones, from a model that declines 233 of 470 answerable. P5.
7. **HF has no `older`-only S3 result.** 28 of base's 59 right S3 recall answers are agreements with a true claim (long 781-782). P6.
8. **HF omits why C1 failed (c):** the development false-answer gate compared with 6.37, not base (long 662-663). The reopening's main method lesson, one sentence. P8.
9. **The R-298 broad count sits apart from the 1.3-point miss** (HF 180 against HF 202-204). Side by side, the reader sees the narrow flag is the reading that favours C1. P7.
10. **No conclusion section in either paper** (brief 2A). Add one paragraph to the long paper (P9) or drop the item.

## 2. Proposed replacement passages (kv_voice_v2)

**P1, HF 5-7** (+22 words; cut in item 6 of part 6):
> **Claim.** On a sealed test of chats from its training generator, 6.37 makes Tiny Aya Global recall 91 to 107 of 120 out-of-view facts, against the untrained model's 13 to 32. On chats from outside writers (Claude agents) it does not beat the strongest simple baselines, and on S3 it repeats its own wrong answers and names listed values on never-told questions more often than the untrained model.

Numbers: HF 5-7.

**P2, long 79-81:**
> - Where training helps: on the generator's sealed chats, recall above base, code and the whole chat at 58 messages, and above base and code at 419 messages, where the whole chat could not run on this card (R-166, R-168); over code, answers in view left alone.

Numbers: none new.

**P3, long 177-180, the clause after "on S3 code recalls more;":**
> training's measured gain is, over code, answers in view left alone (35 and 37 of 40 against code's 13 and 16 on the outside-writer sets); over base, searching for facts out of view. Code searches on every statement by construction, so statements measure no gain over it (sections 6 and 9).

Numbers: long 432, 441.

**P4, long 590-592, from "K1.3, the pick":**
> K1.3, the pick without the second change, also fails clause (c) on S3 as a report arm (37 of 472 (7.8%), two seeds, 9 and 28 of 236). Had it been the pick, a third seed would have needed 5 or fewer of 236 to pass, so what ships turns on the change only through a seed I did not run.

Numbers: long 591, Appendix C 1091.

**P5, HF 122, after "of a stratified 248.":** (+27 words)
> On the 233 answerable questions of the 248, 6.37 and code tie, 40 against 40; 6.37's lead over code comes from the 15 unanswerable ones.

Numbers: long 481-483.

**P6, HF section 6 table, new row after Recall:** (+25 words)
> | `older` only (no answer cue in the question) | 30 of 356 (8.4%) | 285 of 1,068 (26.7%) | (author to fill or leave blank) | 292 of 1,068 (27.3%) | none |

Numbers: long 783-784. Seed 82's `older` count is not in either paper.

**P7, HF 180, after "-3.1 to +5.7 points.":** (+33 words; move, not add, by cutting HF 202-204's sentence)
> Counting every stored value the chat holds, not only listed values of the asked category, C1 answers 99 of 708 (14.0%) N-hit questions with a value, base 17 of 236 (7.2%) (exploratory, R-298).

**P8, HF 196, after "none swapped in.":** (+33 words)
> I picked on development recall, under a development false-answer gate that compared with 6.37, not with base (R-191); the development screen and the demos did not predict S3 on that line.

Numbers: none. Text from long 662-663, put in first person.

## 3. Numerical, terminology and cross-document inconsistencies

- N-hit definition (item 3): long 33, 65, 138-139, 162, 603, 1061 and HF 24 against long 774, HF 171, 200.
- Stages: long 198-207 has a Plan row and one "14 to 15 Nov" row (R-280 to R-305); HF 87-94 has no Plan row and splits 14 Nov (R-280 to R-293) from 15 Nov (R-294 to R-305). Not wrong; pick one.
- Long section 8 heading and row 206, "The push to replace 6.37, then K1.3", reads as replacing K1.3. Suggest "The push to replace 6.37: K1.3, then C1".
- "No measured difference" (HF 28, long 142-143) is an interval OR a sign test; say which governs when they disagree (I found no case where they do).
- "What" to retrieve, "met on generated chats" (HF 73, long 160): no count in either paper.
- The query-writing counts (88 against 22; 53 of 67) sit in long 825-833 under Future work and again in Appendix C 1076-1085. Results in Future work; cite Appendix C there.

## 4. Claims stronger than the evidence

- Long 79-81, 767-768 (P2); long 177-180 (P3); long 590-592 (P4); HF 122 and long 24-25 (P5).
- HF 9-10 "lets Tiny Aya Global ... search the part of a chat it can no longer see" has no qualifier until line 10, while on S3 code makes more right search decisions than every 6.37 seed (714 against 682, 666, 670 of 834; HF 71-72). P1 covers it.

## 5. Underemphasized findings

- **6.37 against the rule's own lines.** 6.37's plain never-told rate, 238 of 360 (66.1%), is under base's 111 of 120 (92.5%) by more than (a)'s 5-point line; C1 is above 6.37 on four of six S3 count lines (long 608-609). R-294's panel carried the objection "on substance C1 is the better model for users"; neither paper says so. This shows most plainly that 6.37 ships by the rule, not on merit (P9).
- **Cue share of 6.37's recall.** 59 of its 347 right S3 answers are no-search agreements with a true claim (long 170-171). By my subtraction (347 minus 285 `older`) it has 62 right `confirm` answers, so nearly all its `confirm` score is the cue. The 62 is not in the papers.
- **K1, the first candidate, meets every measured S3 line** (HF 194-195) and the 24-candidate search moved away from it; now an aside.
- **No outside set where 6.37 measures above the strongest simple baseline on recall or judged answers.** The "Use this when" paragraphs (HF 30-37, long 91-101) never name a setting where 6.37 is the choice.
- **Future work order.** Long 821-823 and HF 219-221 lead with "a sealed test of K1"; the S3 diagnosis points at query writing (Appendix C 1073-1085). Add brief section 5's isolation design as a plan, labelled not run.

**P9, for the long abstract's last paragraph or a conclusion (author approval):**
> Read against the same lines, 6.37 is below C1 on recall, copies, N-hit false answers and plain never-told questions, and above it on statements (180 against 166 of 180) and in view by one item (161 against 160 of 180). Its plain never-told rate, 238 of 360 (66.1%), is below base's 111 of 120 (92.5%). 6.37 stays shipped because the registered rule names no replacement, not because it measures well on S3. On no outside set did 6.37 measure above the strongest simple baseline on recall or judged answers.

Numbers: long 608-609, 655-656; `ship_rule.json`.

## 6. Changes that need author approval

1. P1, the new HF Claim line (changes the headline claim).
2. P9 and the "on no outside set" sentence (a new reading of existing numbers; it states C1 measures better than the shipped model).
3. P4 (rewords a stated conclusion about the demo-test change).
4. N-hit Terms correction (item 3), after the author checks `scoring.py`.
5. Using the derived 62 `confirm` count (part 5), not in the papers.
6. HF word budget: P1, P5, P6, P8 add about 107 words; P7 is a move. Proposed cut: HF section 2's chronology table and R-304 note (HF 85-97, 157 words), replaced by one line ("Dates and records for each stage are in the long paper's section 2; R-304 renumbered every commit from 10 November."), net about 30 words shorter than now. Brief section 7 says the short paper should not reproduce the chronology.
7. A conclusion paragraph in the long paper, or the brief's 2A "conclusion" item dropped.
8. Future work reordered to put query-writing isolation first, with the four-arm design labelled as a plan.
