# Lane 1: Retrieval and tool-use researcher (hostile)
Verdict: submit after fixes

Reviewed 125b902. Recounts from `results/s3/*.json` with `panel5/l1_chk.py` and `panel5/l1_q.py` (outside the repository).

## Round-3 findings: status (one line each)
F1 fixed: HF_ARTICLE.md:65-72 lists the four clauses with S3 outcomes (480 of 1,242; 260 of 414; 288 of 480).
F2 fixed, but wrong in part (new F1): ARTICLE.md:1018-1021, HF:181-184.
F3 fixed: ARTICLE.md:62 gives 6.37, seed 82, C1 and code.
F4 fixed: ARTICLE.md:164-166.
F5 fixed: HF:9-10.

## New findings (most severe first)
F1. [MAJOR] ARTICLE.md:1018-1021 (Appendix C), :778-781, HF_ARTICLE.md:181-184: "code's raw message found the fact where seed 82's queries did not on 141 ... so on those questions the query made the difference." On 53 of the 141 seed 82 made no search at all (47 `confirm`, 6 `older`), so they are "when" misses, not query misses. Where both searched: 88 against 22 (sign test p = 1.6e-10). C1 seed 82: 100 against 29 (p = 2.5e-10), 6 not searched. My round-3 wording caused this.
    Evidence: rows with `found_fact` true for code and false for the adapter, split by empty `queries`; `s3_always_search.json` against `s3_fix17cs37_82.json` and `s3_k13opc1_r263_82.json`.
    Fix: "where both searched, code's raw message found the fact and seed 82's queries did not on 88 (22 the reverse); on 53 more seed 82 did not search (C1 seed 82: 100 and 29; 6)." Drop "on those questions the query made the difference" or limit it to the 88.

F2. [MAJOR] HF_ARTICLE.md:67-68 ("When ... met for answers in view and plain statements"): the short paper never says that on S3 code, which never decides, makes more right decisions than any 6.37 seed (714 of 834 against 682, 666 and 670). The long paper has it (ARTICLE.md:155). A judge scoring "decides when" from the short paper reads only the good half.
    Evidence: `right_decision` sums, round-3 recount; 714 = 834 minus 60 in view minus 60 statements.
    Fix: add the long paper's sentence at ARTICLE.md:154-155 to the "When" bullet.

F3. [MINOR] ARTICLE.md:1015-1016 (Appendix C): "661 of 878 are searches that did not find the fact, and 178 had the fact": the remaining 39 (6.37: 154 of 895) did not search. They go unnamed, and 154 is 6.37's second-largest loss.
    Evidence: wrong recall rows split by `found_fact` and `queries`, three seeds each.
    Fix: add "; 39 did not search (6.37: 154)".

F4. [MINOR] HF_ARTICLE.md:71-72: "as often as base on code's passages" (60.0% against 60.8%; unpaired, about plus or minus 7 points) states equality. The long paper's "59 of 347 right answers on rows marked not found" is missing from the short paper.
    Fix: "no measured difference (-0.8 points)"; add the 59 of 347.

F5. [MINOR] HF_ARTICLE.md: no related-work line, and no line saying the baselines ran in one setting each against 64 candidate sets (ARTICLE.md:735). Carried since round 2.
    Fix: one sentence each in HF section 7.

## What holds up
- S3 never-told counts: whole chat 57 of 236 N-hit and 89 of 120 plain; base 14 of 236 and 111 of 120; seed 82 76 of 120.
- S3 grounding counts: code 158 of 260, base 17 of 29, seed 82 81 of 141.
- Appendix C's lines, per-seed recall and re_ask pointers lead to the content they name.
