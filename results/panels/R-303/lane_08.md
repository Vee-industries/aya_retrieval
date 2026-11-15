# Lane 8: Voice editor (round 4)
Verdict: submit after fixes (wording only; no number changes; 0 em or en dashes, 0 "we/our/us" in the five documents; abstract 480 words)

Files at commit 125b902: ARTICLE = docs/ARTICLE.md, HF = docs/submission/HF_ARTICLE.md, ABS = docs/submission/ABSTRACT.md, MC = docs/MODEL_CARD.md, C1 = docs/MODEL_CARD_C1.md.

## Round-3 findings: status
F1 partly: the K1 sentence is fixed. "The expectation in hand" (ARTICLE:776, HF:212) and "The records hold no forecast of recall." (ARTICLE:773-774) remain.
F2 fixed (ARTICLE:77). F4 fixed (ARTICLE:527, 892). F5 fixed (ARTICLE:552, HF:149). F6 fixed (HF:5-7). F7 fixed (ARTICLE:86; MC:27 counts). F8 fixed (MC:178-179; C1:60). F9 fixed (ABS:34). F11, F12, F13, F15 fixed.
F3 not fixed, and R-302 records it as the author's wording ("results he had missed"): ARTICLE:29, ARTICLE:474, HF:125, ABS:20, MC:52.
F10/F14 partly: "far" and "about 15" are gone; "about 22" is new (F3 below).
F16 partly: "follows STaR" is fixed; the citation list remains (F1 below).

## New findings (most severe first)
F1. [MINOR] ARTICLE:174-181 "Related work": eight-citation background list (voice 10: "X has been approached through A (cite), B (cite)... reads as performance"; cite for fact, not credibility). Also "poorly" (line 179) is evaluative.
    Fix: "**Related work.** RAFT fine-tunes with distractor documents (Zhang et al., 2024), the role this project's decoys play inside a chat. STaR trains on a model's own outputs that pass a check (Zelikman et al., 2022); 6.37's targets are the untrained model's own replies that pass the scorer. LongMemEval (Wu et al., 2025) supplies the outside check, LoRA (Hu et al., 2022) the adapter, and a model judge follows Zheng et al., 2023." Remove the matching rows from References if no other line cites them.
F2. [MINOR] ARTICLE:776, HF:212 heading "The expectation in hand", and ARTICLE:773-774 "The records hold no forecast of recall." An expectation is a stance; the denial of a forecast is commentary (voice 11).
    Fix: heading "K1's S3 report arm (exploratory)." Delete "The records hold no forecast of recall." Delete the tautology "a sealed test of K1 passes or fails on S3's rule as registered" (ARTICLE:777-778, HF:213-214); end the sentence at "against base's 14 of 236 (5.9%)."
F3. [MINOR] MC:129 and ARTICLE:427 "differences under about 22 points": a hedge, and I found no source for 22 in R-142 (which says plus or minus 15) or R-165.
    Fix: drop "about" and cite the record that computes the figure, or write "differences under 15 points (R-142)" if 15 is the source.
F4. [MINOR] ABS:27-28 "chosen after the demo test changed twice once both models' readings existed": missing comma, reads as one clause.
    Fix: "chosen under a demo test that changed twice after both models' readings existed".
F5. [MINOR] MC:138 "Base with the tool searches too little" is evaluative; the counts are at MC:27-28.
    Fix: "Base with the tool searches on 54 and 42 of the 120 recall questions; code searches every turn."
F6. [MINOR] MC:163 "The shipped seed is not the strongest." Evaluative heading.
    Fix: "Seed 82 is the lowest of the eight training seeds on the first outside-writer set, on sealed conditions C and D, and on `hard_dev`" (drop the bold heading sentence; the next sentence states it).
F7. [MINOR] ARTICLE:746, HF:201 "a false memory the user may act on": hedge.
    Fix: "A value given as something the user said, when the user never said it, is a false memory, and the user can act on it."
F8. [MINOR] ARTICLE:616 "The whole chat is not free of the first fault": figure of speech.
    Fix: "The whole chat also shows the first fault:".
F9. [MINOR] Outside the assigned sections: ARTICLE:440 "mostly a search that missed the fact" has no count; Appendix A gives 38 of 81 and 36 of 67.
    Fix: "by R-139's stages, a search that missed the fact is the largest stage (38 of 81 and 36 of 67; Appendix A)".

## What holds up
- Sections 12 and 14's gap list, Appendices A to C, C1's "Limits" state limits as facts with counts.
- First person only for decisions; present tense for the apparatus; no "I claim/find/show" introducers; no stance adverbs.
- Appendix and section pointers I tried (Appendix C for 402 of 708, `re_ask`, Appendix B for candidates) hold what they say.
