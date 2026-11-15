# Lane 9: Against (the strongest case against submitting as is)
Verdict: submit after fixes (F1 is text only; do not submit with F1 standing)

## Round-2 findings: status (one line each)
N1 fixed: ARTICLE:75-76, ABSTRACT:28-29, HF:143-144 (code above both, with intervals).
N2 fixed: ARTICLE:156 and deviation 13 agree; README:37 and ABSTRACT:21 now claim only the ship rule.
N3 partly: ARTICLE:694 says base invents values and its rates are floors; the size (my 14 of 20 hand read) is still not given. Carried, not blocking.
N4 fixed: "Use this when" (HF:15-18, ARTICLE:88-91) no longer claims a win past the card.
N5 fixed: deviation 19 (ARTICLE:667).
N6 fixed: no "as well as", "declines a plain" or "best" left in README (grep).
N7 withdrawn: the first sealed test's rules hold no never-told line, so no upper-bound note is needed there.

## New findings (most severe first)

F1. [MAJOR] ABSTRACT:15-17, HF:16-17 and section 3 (LongMemEval-S paragraph), ARTICLE:79 and :89-90: "6.37 and code show no measured difference" is stated without a qualifier, and the only numbers given (53 against 40 judged, base 34) favour 6.37. The registered test against code, H2 (R-170), found a measured difference in code's favour: code's first search finds the evidence on 372 of 476 against 6.37's 333 (-8 points, -13 to -4, p = 0.0004), and the gold answer is in 63 of 411 code replies against 51 (6.37 ties base, 51 and 51). The judged measure, which had no registered hypothesis, puts 6.37 ahead only through the 15 unanswerable questions (13 of 15 against 0); on the 233 answerable it is 40 against 40. The README (326-335) and the long paper's hypothesis table report this; the abstract and short paper, the two documents a judge reads, do not.
    Evidence: RECORDS.md R-170, lines 6976-6986; ARTICLE:879 (Appendix A); README:329-335.
    Fix: ABSTRACT and HF section 3: "against code, no measured difference on answers (judged 40 against 40 on the answerable questions); code finds the evidence more often (372 against 333 of 476, registered H2, p = 0.0004)." In "Use this when", "no measured difference in answers".

F2. [MINOR] HF:122 and ARTICLE:534: "775 against 742" (and Appendix B's "Pick recall" column) still carries no denominator, the round-1 F8 item. A judge cannot tell whether 33 is large.
    Fix: give n once, in Appendix B's header and in HF:122.

F3. [MINOR] HF:169-172 ("With more credits") says the expected result is "not a forecast" and that "the records hold no forecast", then says "a sealed test of K1 is expected to read like that". The two sentences contradict each other.
    Fix: "K1's S3 report arm (two seeds, exploratory) reads: ...; a sealed test of K1 passes or fails on S3's rule as registered."

F4. [MINOR] HF:60 (section 2 table) lists 15 November as "R-294 to R-298"; R-299 (audit) and R-300 (shortening) are missing, and ARTICLE:181 ends 14 November at R-287 where HF ends it at R-292.
    Fix: make both tables give the same ranges, through R-300 (or the last record before upload).

## What holds up
- Every S3 count I checked in the "Every arm" table, Appendix C's rule lines (0.293, 0.889, 0.922, 0.956, 0.808, 0.006, 0.072) and the recall-loss sums (878 + 364 and 895 + 347 = 1,242) agree with each other and the short paper.
- R-300's appendix pointers (ARTICLE:378, 422, 431, 482, 564, 591, 594, 695) each land on a table that holds what the pointer says.
- The headline no longer misleads: the claim, "Result first" and the abstract each state, in the opening paragraph, that 6.37 is weak on outside chats, that code beats both trained models on S3, and that 6.37 stays shipped only because no replacement passed.
