# Lane 9: Against (the strongest case against submitting as is)
Verdict: submit after fixes (all text only; F1 and F2 should not go out standing)

## Round-3 findings: status (one line each)
F1 fixed: ABSTRACT:14-16, HF:22-24 and :119-120 give H2 (372 against 333 of 476); 53 against 40 is inside "no measured difference" (ARTICLE:450, interval -0.8 to +11.3).
F2 partly: Appendix B now gives "of 1,296" (ARTICLE:954); HF:151 still prints 775 against 742 with no n.
F3 fixed: HF:212-214 no longer calls it expected.
F4 fixed: HF:89 and ARTICLE:194 both end at R-301 (see F5).

## New findings (most severe first)
F1. [MAJOR] ARTICLE:554, HF:150, ABSTRACT:27, MODEL_CARD_C1:71: "both changes came after both models' readings existed" is false for the first change. When R-276 was made, K1.3 had no Demo5 reading. R-276 itself ordered that reading, "chosen knowing C1's". Only R-278 came after all four readings. The error points toward more contamination, not less, so it is MAJOR, not BLOCKER, but it is a false statement inside a disclosure. ABSTRACT:27's "changed twice once both models' readings existed" is also a broken clause.
    Evidence: RECORDS.md R-276 (line 10091: "K1.3 has no Demo5 reading"), R-277 (10:45), R-278 (10:50).
    Fix: "The first change (R-276) came after both of C1's demo readings and K1.3's Demo4 reading, and it ordered K1.3's Demo5 reading knowing C1's; the second (R-278) came after all four."
F2. [MAJOR] HF:24-25 ("Use this when", the safety branch): "If both faults matter: 6.37 is shipped by the registered rule" puts the shipped model forward in the one case where it measured worse than base on both faults. Its "-97%" and "-82%" are measured against 6.37, but that is not stated, and base with the tool is still lower than C1 on N-hit (5.9% against 7.2%).
    Evidence: ARTICLE:572-576 (Every arm table).
    Fix: "If both faults matter, do not use 6.37: on S3 it is worse than base on both. C1 measured lower rates than 6.37 (-97% on copies, -82% on N-hit) but is not below base on N-hit (7.2% against 5.9%)."
F3. [MINOR] ABSTRACT:24-25: "286 of 708 (40.4%) never-told questions". The 708 are only the N-hit never-told questions (plain never-told adds 360). The long abstract (ARTICLE:33-34) keeps the qualifier.
    Fix: add "whose search returned text".
F4. [MINOR] HF:142-143: no reason is given why K1 was dropped, though HF:184-186 shows K1 meets every measured S3 line. Both pick changes were won by leads inside the seed spread (742 against 720, then 775 against 742).
    Evidence: ARTICLE:511-512, :960-979; RECORDS R-203, R-279.
    Fix: one line in section 5: "K1.3 led K1 742 to 720 of 1,296, inside the seed spread."
F5. [MINOR] HF:89 and ARTICLE:194: the ranges stop at R-301 and call it "a third review round". This round and R-302 are left out.
    Fix: set both to the last record before upload.
F6. [MINOR] MODEL_CARD_C1:47-49: it states (c) in two parts, then says C1 "passed the first two parts of (c)". The rule has three parts: it adds "bound above 0" (ARTICLE:368, :489).
    Fix: state all three parts.

## What holds up
- The Every arm table, Appendix B's pick recalls and HF section 6's counts agree with each other and with R-279.
- "Six minutes later" matches the commit times (10:48, 10:54) at ARTICLE:544.
- The claim and "Result first" lines state the generator-only win, the outside-writer reversal and why 6.37 stays shipped before any other result.
