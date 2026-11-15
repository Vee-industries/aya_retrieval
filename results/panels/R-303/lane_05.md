# Lane 5: AI safety and alignment reviewer (hostile), round 4
Verdict: submit after fixes (no blocker, no major; five minor wording fixes)

## Round-3 findings: status (one line each)
F1 fixed: HF_ARTICLE.md:19-21, ARTICLE.md:93-96 and 616-618, MODEL_CARD.md:102-105 give 57 of 236 and 89 of 120; `panel5/l05/offcat_wc.py` reproduces both.
F2 fixed: ARTICLE.md:599-600 now says "answered with no listed value".
F3 fixed: MODEL_CARD_C1.md:40 "-97% on copies and -82% on N-hit false answers".
F4 fixed, with a placement fault (new F2): HF:200-201, ARTICLE.md:745-746 and 787.
F5 fixed: ABSTRACT.md:27 (495 words).

## New findings (most severe first)
F1. [MINOR] ARTICLE.md:616-617: "The whole chat is not free of the first fault", backed by the 57 of 236 flag. ARTICLE.md:729 calls "another category's stored fact" "the demo's first fault" and says that flag does not count it. The sentence cites a measure that, by the paper's own definition, does not count the fault it names.
    Fix: "The whole chat is not free of N-hit false answers".
F2. [MINOR] HF_ARTICLE.md:200-201, ARTICLE.md:745-746: the false-memory sentence sits under the bold heading "Not tested: instructions hidden in retrieved passages", so it reads as a description of injection. It is the only sentence in either paper that says why the faults matter for safety (grep for "safety|harm|act on|trust": only these lines, the title line and one reference).
    Fix: keep the heading as its own bullet, and move "A value given as something the user said, when the user never said it, is a false memory the user may act on" to the threat-model line (HF:62-63, the matching line in ARTICLE.md).
F3. [MINOR] HF:20-21, ARTICLE.md:95-96 and 618, MODEL_CARD.md:105: "against 111 of 120 (92.5%)" does not name the arm.
    Fix: "against base with the tool's 111 of 120 (92.5%)".
F4. [MINOR] ARTICLE.md:75-77 (judges' minute): "402 of 708 (56.8%) ... (sections 6.2 and 12, Appendix C; R-298)". Section 6.2 covers the outside-writer sets and does not contain 402. Section 12 (line 731) only points on. The number appears only in Appendix C (line 1012), where it is labelled exploratory. It has no label here.
    Fix: "(exploratory; Appendix C, R-298)".
F5. [MINOR] HF_ARTICLE.md:15, ARTICLE.md:85, README.md:9-10: "names values on never-told questions more often than the untrained model". The flag counts listed values only, and the papers say base invents values that pass unseen. A crude decline-word count puts a reply with no decline word in 135 of base's 222 passed N-hit replies (`panel5/l05/nodecl.py`; regex, approximate). "Values" claims more than the flag measured.
    Fix: "names listed values".

## What holds up
Every fault count reproduces from `results/s3/`: the flags (base 14, 6.37 286, C1 51), other stored facts (17, 402, 99), whole-chat copies 2 of 298, and the -97% and -82% changes.
The reopening, both demo-rule changes, Demo5's double read and deviation 20 (no decline check) are disclosed in the deviations table, HF section 7 and the abstract.
The threat model states its scope (the chat's own content) and lists injection as untested.
