# Lane 1: Retrieval and tool-use researcher (hostile)
Verdict: submit after fixes

Reviewed commit 8735c87. Recounts are from `results/s3/*.json` with a read-only script
(`scratchpad/panel3/l1_s3.py`, outside the repository).

## Round-1 findings: status
F1 partly: ARTICLE.md:138 and HF_ARTICLE.md:125-126 now say the queries find the fact less often than code's raw message (480 of 1,242 against 260 of 414). The abstract still says nothing about the "what" clause, and ABSTRACT.md:3-4 still says the model searches "when the answer is out of view". The short paper has no clause-by-clause outcome statement.
F2 partly: ARTICLE.md:137 limits "when" and gives `confirm` 7, 0 and 5 of 58. Not stated anywhere: on S3, 6.37's total right decisions (682, 666, 670 of 834) are below code's 714 (grep "714": 0 hits); `re_ask` searched 3 of 60 on each seed. ARTICLE.md:147 (contribution 2) still says "training's gain is when to search (sections 6 and 9)", and section 9 does not show that gain.
F3 fixed: ARTICLE.md:140 outcome column; the abstract and HF:14-16 state the S3 rates against base.
F4 fixed: ARTICLE.md:664-670 and HF:196-200 give seed 82's own S3 lines.
F5 partly: ARTICLE.md:805-807 and HF:249-251 state the tuning gap and name the router and score-threshold baselines. Not named: base with its tool-call format repaired, and code with 6.37 as the reader. The prompted control is still absent from the short paper (grep "prompt" in HF: 0 hits on it).
F6 fixed: ARTICLE.md:62 gives code as 29 to 64 of 120 and the whole chat at 58 messages; HF:117-118 uses "of 60" on both sides.
F7 not fixed: ARTICLE.md:150-157 and the reference list are unchanged. HF_ARTICLE.md has no related-work line (grep Toolformer, Self-RAG, Asai, RAFT: 0 hits). Shi 2023, Yoran 2024, RGB, CRAG, FLARE, Adaptive-RAG, Rewrite-Retrieve-Read and Search-R1 are still not cited.
F8 fixed: ARTICLE.md:120, HF:41.

## New findings (most severe first)
F1. [MAJOR] ARTICLE.md:73 ("For judges"): "code that searches every turn shows no measured difference from 6.37 and is faster. The same holds on S3." This is false for S3, and it contradicts ARTICLE.md:691.
    Evidence: on S3 recall, code is right on 161 of 414 and seed 82 on 99 of 414. Code alone was right on 100 questions and seed 82 alone on 38 (exact sign test p = 1.3e-7). Pooled, 6.37 is right on 347 of 1,242 (27.9%) against code's 38.9%. Against C1 seed 82, code alone was right on 92 and C1 alone on 58 (p = 0.0069).
    Fix: "On S3 the whole chat (274 of 414) and code (161 of 414) both recall more than 6.37 (seed 82: 99)."

F2. [MAJOR] docs/MODEL_CARD.md:100-101, heading at :109, :201-203: under "Which to use when", item 2 says that when the chat does not fit, code shows no measured difference and is faster. Its evidence is the outside-writer chats, which do fit. The papers' "Use this when" boxes (ARTICLE.md:84-85, HF:57-58) give the opposite advice: on long generated chats 6.37 recalls more than code. The heading "plain code recalls as well" and the Limitations section leave out S3, where code recalls more (grep "161" in the card: 0 hits).
    Fix: copy the papers' "Use this when" text into the card, and add S3's code and whole-chat recall to its Limitations.

F3. [MAJOR] ARTICLE.md:62 (headline table): the S3 recall row gives only C1's 364 of 1,242. It leaves out the shipped model's S3 recall (6.37 347 of 1,242; seed 82 99 of 414) and code's 161 of 414. The fault rows give 6.37's numbers. Only the recall row, where 6.37 is weakest, shows only C1.
    Fix: put 6.37's pooled and seed 82 recall in the trained cell, and add code's 161 of 414 to the baseline cell.

F4. [MAJOR] ARTICLE.md:139 ("grounds" row): it reports the first sealed test only, while the other three rows give S3 outcomes. On S3, 6.37 got 288 of the 480 recall questions right where its own search found the fact (60.0%; seed 82: 81 of 141). That is the same rate as base reading code's passages, 158 of 260 (60.8%). In addition, 59 of 6.37's 347 right answers (seed 82: 18 of 99) are on rows the scorer marks as fact not found, so rule 2's "every right answer came from a search that found the fact" does not hold on S3. C1 seed 82 has 1 such row. Not checked: whether those 59 rows reflect paraphrases that the `found_fact` matcher misses.
    Fix: add "on S3, it used a found fact no more often than base reading code's passages" to the row.

F5. [MAJOR] RECORDS.md R-297 (line 10528) says R-295's fixes were applied, but three of them are not in the documents, and R-297 does not list them as not done: D's related-work line in the short paper, C's prompted baseline in the short paper, and the tool-format repair named as an untested baseline (the "Carried" list in R-295).
    Fix: apply all three, or list them in R-297's "Not done" with a reason.

F6. [MINOR] HF_ARTICLE.md:220-221 and ARTICLE.md:692: "Code is worse on the faults" (HF) and "Code is worse on every other kind" (long paper) both cite code's copy rate of 65 of 298 (21.8%). That equals 6.37's pooled 195 of 894 (21.8%) and is above seed 82's 62 of 298 (20.8%) by only one point. On copies, code is not worse than the shipped model.
    Fix: "worse than base and C1; on copies, the same as 6.37."

F7. [MINOR] HF_ARTICLE.md:259: "Query writing is untrained." 6.37's training rows include its own search calls, so its queries were trained by supervised fine-tuning (ARTICLE.md:65). ARTICLE.md:836 limits the claim to the reopening.
    Fix: "Query writing was not trained on its own, and the reopening did not change it."

## What holds up
- S3's counts in the long paper match the run files on my recount: recall 99, 120 and 128 of 414 (6.37 by seed); found the fact 141, 180 and 159 (total 480) against code's 260; `confirm` searched 7, 0 and 5 of 58.
- Section 9's baseline paragraph (whole chat 274, code 161 of 414) and the seed 82 table (ARTICLE.md:664-670) match the files.
- The "when" row's in-view claim holds on S3: 55, 57 and 55 of 60 in-view answers left unsearched, and 60 of 60 statements on every seed.
