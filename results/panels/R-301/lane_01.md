# Lane 1: Retrieval and tool-use researcher (hostile)
Verdict: submit after fixes

Reviewed commit 48c6586. Recounts from `results/s3/*.json` with read-only scripts outside the repository
(`scratchpad/panel3/l1_s3.py` and one-line checks).

## Round-2 findings: status (one line each)
F1 fixed: ARTICLE.md:73 now says code recalls more than 6.37 on S3 (+11.0 points, +3.5 to +18.6).
F2 fixed: MODEL_CARD.md:97-106 has the papers' three-case box; :204-206 gives S3's code and whole-chat recall.
F3 not fixed: ARTICLE.md:62, the S3 recall row still gives only C1 (364 of 1,242) in the "Trained" column, while both fault rows give 6.37. R-298 neither applies nor carries it.
F4 fixed: ARTICLE.md:139 gives 288 of 480 against 158 of 260, and the 59 of 347.
F5 partly: the short paper still has no related-work line (carried, R-298 synthesis) and no line on the two fixed prompts on base (ARTICLE.md:419). I drop the tool-format repair point: on S3, none of base's 352 unsearched recall replies holds any call text, so base declines to call. It does not fail at the format.
F6 fixed: ARTICLE.md:590, HF:144.
F7 fixed: HF:169, ARTICLE.md:735.

## New findings (most severe first)
F1. [MAJOR] docs/submission/HF_ARTICLE.md, whole file: the short paper quotes problem statement 4 (:31) but never says which clauses 6.37 meets. The "what" result (its queries found the fact on 480 of 1,242 S3 recall questions; code's raw message on 260 of 414) and S3 grounding (288 of 480, the same as base reading code's passages) are missing. A judge who reads only this paper cannot score the track fit.
    Evidence: grep "480", "288", "260 of 414", "714", "right decision" in HF_ARTICLE.md and ABSTRACT.md: 0 hits.
    Fix: add the long paper's four-row table (ARTICLE.md:136-141), or four one-line outcomes, to HF section 3 or 6.

F2. [MAJOR] ARTICLE.md:957-960 (Appendix C, "Where recall is lost"): "whether the query or the keyword tool is the cause was not separated." The run files do separate most of it. Seed 82 against code on the same S3 recall questions: the tool, given the raw newest message, found the fact on 141 questions where 6.37's own queries did not, and the reverse held on 22 (exact sign test p = 1.9e-22). For C1 seed 82 the counts are 106 and 29 (p = 1.7e-11). Query writing is a measured cause, so the sentence softens the "what" failure.
    Evidence: `found_fact` per id in `s3_always_search.json` against `s3_fix17cs37_82.json` and `s3_k13opc1_r263_82.json`; recall kinds only.
    Fix: "On 141 recall questions code's raw message found the fact and seed 82's queries did not (22 the reverse; C1 seed 82: 106 and 29), so query writing is a measured cause; on questions where both missed, the tool is not ruled out." Mark it exploratory.

F3. [MAJOR] ARTICLE.md:62: the round-2 F3 fix above still stands, and it is the paper's headline table.
    Fix: trained cell "6.37 347 of 1,242 (27.9%; seed 82 99 of 414); C1 364 of 1,242"; baseline cell add "code: 161 of 414".

F4. [MINOR] ARTICLE.md:147-149 (contribution 2): "training's measured gain is leaving answers in view and plain statements unsearched." That gain is only over code. Base with the tool leaves them unsearched just as often (S3 right decisions 58 of 60 on each). Over base, the gain is searching on `older` (340 of 356 against 58 of 356, seed 82). MODEL_CARD.md:26 states it correctly.
    Fix: "over code, leaving answers in view and statements unsearched; over base, searching for facts out of view."

F5. [MINOR] HF_ARTICLE.md:9: "code ... recalls as much or more" on outside writers. On set 2, code has 42/47 and 6.37 39/53, and the measured result is no difference (HF:82).
    Fix: "code shows no measured difference on recall, and on S3 recalls more."

## What holds up
- S3 right decisions: base with the tool 201 of 834, 6.37 682/666/670, code 714, C1 797/789/807. The "when" row's numbers match.
- Every Appendix pointer after R-300 (ARTICLE.md:422, 431, 482, 564, 591, 594, 695) leads to the content it names.
- Grounding row: 347 - 288 = 59 of 347 right answers with the fact not found; 6.37's 895 and C1's 878 wrong answers are consistent with 1,242 minus recall.
