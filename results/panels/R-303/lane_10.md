# Lane 10: Practitioner (critical), round 4
Verdict: submit after fixes. The short paper (2,761 words, `wc -w`) tells the story in order and stands without the long one; the "use this when" advice still hides code's measured faults and is not a clear pick between 6.37 and C1.

## Round-3 findings: status
F1 (table seed vs figure pooled) fixed: table headed "6.37 seed 82"; line 11 says "the shipped seed"; figure subtitle now gives whole chat 71 and 65 of 120; Figure 1 caption says the table is the shipped seed.
F2 (last paragraph) fixed: section 8 now reads clearly and K1 is defined in Terms.
F3 (undefined labels) partly: Terms defines K1, K1.3, OP, Demo2-5, but the chain still runs through sections 5 and 6, and Terms adds about 200 words. Defined, not cut.
F4 (figure row "shipped") fixed: row reads "6.37, three seeds".
F5 (clause b wording) not fixed: line 135 still reads "copy both at most half as often as 6.37 and at least 10 points less".
F6 (demo figure placement) fixed: Figure 2 now follows "How C1 became the pick".

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md:22-25 against 180-182 and Figure 3: the advice "if the chat is longer than the window, code needs no training" omits that code has the worst fault rates measured: copies 65/298, N-hit false answers 121/236 (51%), against base 11/298 and 14/236. Faults were not measured past the window, which the paper does not say. A practitioner will deploy code on that advice.
    Evidence: figures/s3_faults.png top row; line 180-182 "worse than base and C1 on both faults".
    Fix: add "but code has the highest fault rates on S3 (65/298 copies, 121/236 N-hit); faults were not measured on chats past the window."

F2. [MAJOR] HF_ARTICLE.md:19-22: "show it whole" is followed by the whole chat's never-told numbers (57 of 236 against 14; 89 of 120 against 111) with no word saying these are the whole chat's costs. The sentence reads as a list of figures; the reader cannot tell if they favour the advice. Same sentence recommends the arm that is worse than base-with-tool on both never-told measures.
    Fix: insert "but it names a listed value more often than base with the tool:" before the numbers.

F3. [MAJOR] HF_ARTICLE.md:24-25: "If both faults matter" ends in two answers (6.37 by rule, C1 lower rates) with no pick. C1's cost is stated only at line 176-178 (published C1 leaves 50 of 60 plain statements unsearched, fails (a)).
    Fix: "If both faults matter, use C1 (rates -97% and -82%), which leaves 50 of 60 plain statements unsearched; 6.37 is the registered ship."

F4. [MINOR] HF_ARTICLE.md:146-151 and 194-196: the demo-rule change is told in section 5 and again in section 7 (open since round 2). Cut the section 7 demo item to "(R-276 to R-278, section 5)". Section 8 "expectation in hand" repeats lines 184-186 (K1 12 of 472); cut to a pointer. Together about 100 words toward "short".

F5. [MINOR] Line 135: write "(b) copy at most half as often as 6.37 and at least 10 points less than it".

F6. [MINOR] Figure 3 labels C1 "the pick" and its title is "C1 cuts 6.37's faults" while the text says 6.37 stays shipped; relabel "C1, published".

F7. [MINOR] Figure 1 rows "Sealed A to D: heldout / independent" are not named in the text (section 3 says "four conditions"). Add "(Figure 1 rows A to D)" to line 93.

## What holds up
S3 counts in section 6 and the figure match; 372/333 of 476, 233 of 470, 274 and 161 of 414, 50 of 60 and "section 15" match ARTICLE.md lines 26, 87, 612, 588, 790.
Figures 2 and 3 read at a glance; Figure 1 reads once the subtitle's whole-chat numbers are seen.
