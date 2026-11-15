# Lane 1: Retrieval and tool-use researcher (hostile)
Verdict: submit after fixes

## Findings (most severe first)

F1. [BLOCKER] docs/ARTICLE.md:120 (problem-statement table, "what to retrieve"); HF_ARTICLE.md sections 3 and 6: the paper maps "what to retrieve" to "found by the model's own query" but never reports that measure against code. On every set not built by the generator, the trained queries find the fact less often than the user's raw message used as the query. 6.37's queries recite training fact-type keywords: S3 "what am i doing my masters in again" becomes `brother car auction`, and "where's kofi flying off to" becomes `kofi moving city`.
    Evidence: `found_fact` on recall rows. Outside set 1: 6.37 51 of 120, code 85 (`blind_fix17cs37_82_seed_0`, `as_blind_base_seed_0`). Set 2: 54 against 88. S3: 6.37 pooled 480 of 1,242 (38.6%), C1 532 of 1,242 (42.8%), code 260 of 414 (62.8%). On S3 `older` right-view questions, code alone found the fact on 46 and seed 82 alone on 11 (exact sign test p = 3.3e-6). LongMemEval first search: 333 against 372 (ARTICLE section 6.3). Generated sealed chats are the one place 6.37's queries win (106 to 111 against 83 to 103 of 120, `final_*` and `ref_*_base_as`, seed 90311).
    Fix: state in the section 1 table, the abstract and the short paper that the query-writing part of "what" was not achieved: the queries beat the raw message only on generator-built chats.

F2. [MAJOR] ARTICLE.md:65 ("everywhere, searching when the answer is out of view"); HF_ARTICLE.md:105-106: the "when" claim is overstated. 6.37 rarely searches on `confirm` questions ("did I tell you...?"), whose facts are out of view. Its defined measure, right search decisions, is never reported; grep finds it only at lines 119, 177 and 304.
    Evidence: `right_decision`. Confirm searched: outside sets 9 of 40 and 12 of 40; S3 7, 0 and 5 of 58 (seeds 82, 83, 94); S3 `re_ask` 3 of 60. Total right decisions on S3: code 714 of 834, 6.37 682, 666 and 670, C1 797, 789 and 807. Outside sets: 6.37 199 and 204 of 240, code 160.
    Fix: add a per-kind right-decision table. Limit the claim to `older`, `in_view` and statements, and say that on S3 6.37 decides worse in total than always searching.

F3. [MAJOR] ARTICLE.md:122 ("ignores distracting documents"), abstract: on the confirmatory S3, the shipped model fails the distractor clause. Asked a never-told question and given retrieved passages that do not hold the answer, it names a value 286 of 708 times (40.4%) against base's 14 of 236 (5.9%). It also copies its own wrong answer in view 21.8% of the time against base's 3.7%, a grounding failure. The mapped measure, decoy false retrieval, covers only same-type facts about other people in generator chats. The numbers are printed, but no line says which clauses of problem statement 4 6.37 meets.
    Evidence: ARTICLE section 9 table; `results/s3/ship_rule.json`.
    Fix: add an outcome column to the section 1 table. Met: decoys in generated chats. Failed: S3's no-answer passages and the in-view copies.

F4. [MAJOR] ARTICLE section 9, HF section 6: the shipped artifact is seed 82, but S3 reports 6.37 only pooled over three seeds. Seed 82 is the weakest of the three on recall. A search for "99 of 414" in the docs found nothing.
    Evidence: `s3_fix17cs37_82.json`: recall 99 of 414 (23.9%; seeds 83 and 94: 120 and 128), copies 62 of 298, false answers on never-told questions with returned passages 100 of 236 (42.4%).
    Fix: add a seed 82 row.

F5. [MAJOR] ARTICLE.md:418, sections 6 and 9; HF section 3: the baselines are not the strongest simple ones, and they got far less tuning. 6.37 came from 40 trained candidate sets, and the reopening screened 24 more. Code ran in one setting (raw message, top 5, base reads). The prompted baseline was two fixed prompts, run only on the outside sets and never on either sealed test (R-137, R-161). The short paper never mentions it. Untested simple baselines:
    - a router that searches only on question-shaped messages;
    - code retrieval with a score threshold, or with 6.37 as the reader;
    - the whole chat cut to the last 8,192 tokens at 419 messages;
    - base with its tool-call format repaired. Base made clean first calls on only 146 of 328 LongMemEval questions, and was right on 30 of the 37 probe recall questions it did search (R-137).
    Evidence: a keyword rule I wrote after seeing the data (search if the message ends in "?", starts with a question word or holds ", right"). S3: 671 of 834 right decisions, against 6.37's 666 to 682. Outside sets: 163 and 168 of 240, against 6.37's 199 and 204. This is post hoc and not a result, but it shows the "when" gain over trivial routing is not established on S3.
    Fix: state the gap in tuning budget in section 12. Name these baselines as not run. Add the prompted control to the short paper.

F6. [MAJOR] ARTICLE.md:51 (headline table), HF_ARTICLE.md:95-96: the row is labelled "recall of 120", but its baseline cell reads "code: 14 to 32 of 60". On the same 120, code scores 29 to 64. At 58 messages the whole chat (21 to 33 of 60) is the strongest reference in conditions A, C and D, not code.
    Evidence: `ref_{A..D}_base_as_seed_90311.json` recall 64, 61, 37, 29 of 120; ARTICLE section 6.1 reference table.
    Fix: give code as 29 to 64 of 120 and name the whole chat at 58 messages.

F7. [MAJOR] HF_ARTICLE.md (no related-work section); ARTICLE.md:135-143: the short paper cites no prior work. The long paper leaves out the work closest to the distractor, abstention and query clauses. Searched both files for these names and found none:
    - Shi et al. 2023 (models distracted by irrelevant context);
    - Yoran et al. 2024 (fine-tuning to be robust to irrelevant retrieval, close to the reopening's fix);
    - RGB, Chen et al. 2024 (noise robustness and negative rejection, the same idea as `never_told` and the N-hit measure);
    - CRAG, Yan et al. 2024;
    - FLARE, Jiang et al. 2023, and Adaptive-RAG, Jeong et al. 2024 (when to retrieve);
    - Rewrite-Retrieve-Read, Ma et al. 2023, and Search-R1, Jin et al. 2025 (query writing, the stated next step);
    - LoCoMo, cited only as a deviation (line 725).
    The descriptions of the existing citations are fair.
    Fix: add two or three sentences to the long paper and one line to the short one.

F8. [MINOR] HF_ARTICLE.md:34, ARTICLE.md "Terms": "a sealed test opened once (the first sealed test, S3)" reads as if the two tests were one.
    Fix: "(the first sealed test and S3)".

## What holds up
- Rule 2 (grounding on found facts): seed 82's right recall answers all came from searches that found the fact: 106, 107, 92 and 91 right against 106, 107, 111 and 111 found, in `final_{A..D}_fix17cs37_82`.
- Decoy false retrievals on the first sealed test are lower than base's (seed 82: 0 to 7; base: 12 to 24).
- Leaving answers in view unsearched is real: right decisions on `in_view` were 33 and 39 of 40 on the outside sets and 55 to 57 of 60 on S3.
