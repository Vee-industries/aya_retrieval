# Lane: Method
Recommendation: 6.37 seed 82 stays the model put forward; C1 is reported as the candidate that failed (c) by 1.3 points; running 6.37 on Demo4 and Demo5 is allowed only as a report row that decides nothing.

## Answers to questions 1 to 4

**1. What each ruling decided.**
- R-278 (commit 10 Nov 14, 10:54:10): Kevin on seeing the Demo4/Demo5 readings: "hmm it has a higher point spread"; asked to judge by totals, "yes". The entry says: "R-276's demo test is read as the totals over Demo4 and Demo5 on seed 82". It continues "C1 is the pick only if its pooled pick recall ... is above K1.3's 742". Its subject is the candidate screen (C1 against K1.3). It says nothing about S3 or about 6.37.
- Ship rule, R-178 (12 Nov, 06:01): "(a) recall ... (b) ... (c) false answers on never_told items whose search returns passages at least 10 points lower, bound above 0, and not above base's. All of (a), (b) and (c). ... If the candidate fails, 6.37 seed 82 stays shipped". The rule has no demo term. R-191 (12 Nov, 11:19, before S3 opened) replaced 6.37 with base in (a) only; (b) and (c) "unchanged". R-281 (14 Nov, 14:16:58) fixed the computation: "Pass = (a), (b) and (c) all hold ... otherwise 6.37 seed 82 stays shipped". R-280 (14:14), after R-278, restates the ship rule as "R-178's as changed by R-191" with no demo term.
- So R-278 governs which candidate went into S3. The ship rule governs whether that candidate replaces 6.37. They are separate. R-287 (18:51): (c) fails on "above base's: FAIL"; "6.37 seed 82 stays shipped".

**2. Timing and rule 2.**
- Kevin's aggregate call is R-278, 10:54 on 14 Nov. The record has no earlier aggregate call. It came after both models' Demo4 and Demo5 readings (R-278: "set after both models' Demo4 and Demo5 readings exist"). It came before S3's first result file (commit 14:29) and before the verdict (18:51). So it predates S3's result, but it was never a rule about S3 or shipping. Kevin's own reason for it (R-283): "the results were garbage" on one demo; it concerned the demo test.
- A ruling now that C1 is put forward over 6.37 changes (c) after R-287. STANDARD rule 2: "Rules are not loosened after results; any change of rule is the researcher's, made before the results it would decide." The change would loosen (c), and the result it decides is S3. Same rule: "A miss by one judged line is a miss." R-287 already recorded that sentence. Rule 13: the sealed run "is opened once" and the claim rests on it.
- Contrast with R-191: that change was disclosed and made before S3 opened, so rule 2 allowed it. This one cannot meet the "before" test.
- Reading without a change: none found. R-281 took "the stricter reading" and "not above base's" is a point comparison: 51 of 708 (7.2%) against 14 of 236 (5.9%). The panel's points (interval -3.1 to +5.7 against base, per-seed 11/29/11 of 236, scorers missing invented values) are arguments that the line is noisy. They were not registered as an escape clause, so they cannot reopen it. They go in the limits section.

**3. Running 6.37 on Demo4 and Demo5.**
- Valid as a measurement; neither demo is sealed (Demo5 read twice, R-277), so no rule 13 breach. It can only be an exploratory row (rule 38) with n = 6 older and 4 never-told per demo; R-283 says one demo's fixed line "cannot tell these models apart".
- It cannot decide the ship choice: the ship rule has no demo term, and adding one now is the rule change in Q2. If it favours C1, using it to switch is a post-sealed-result rule change. If it favours 6.37, it adds nothing the rule did not already settle. Register before running: "report only, decides nothing". Run it at seed 82, same judges method as R-277.

**4. Recommendation.**
Put forward 6.37 seed 82 (submitted 10 Nov), by the registered rule. Both papers must say:
- The ship rule (R-178, R-191, R-281) was registered before S3 opened; C1 passed (a), (b) and two parts of (c) and failed "not above base's" (51 of 708, 7.2%, against 14 of 236, 5.9%); a miss by one line is a miss; 6.37 stays shipped.
- 6.37's measured weakness on S3, three seeds pooled: copies 195 of 894 (21.8%, base 3.7%); N-hit false answers 286 of 708 (40.4%, base 5.9%); plain never-told 238 of 360. C1 against 6.37: copies 5 of 894, N-hit 51 of 708, never-told 344 of 360, recall 364 against 347 of 1,242 (+1.4 points, interval -3.1 to +5.9).
- C1 minus base on the failed clause is +1.3 points, interval -3.1 to +5.7: S3 cannot tell them apart. Base's 5.9% is a floor (scorers miss invented values). Reported as limits, not as a pass.
- The demo test was changed after both models' readings existed (R-276, R-278, R-283); the deviations table keeps that row. If 6.37 is run on Demo4/5, it is labelled exploratory and decides nothing.
- Not checked: the papers' current text, the S3 result files, the intervals (taken from the brief and R-287).

## The strongest point against, and why it does not change the recommendation
6.37 is worse than base on the fault measures, and C1 cannot be told from base on the one failed clause. Shipping 6.37 ships the model the project found to be the worse one, on a one-point miss inside noise. Kevin owns the rules and may rule. It does not change the recommendation because rule 2 limits his power to rules "made before the results it would decide", and S3's result is already recorded. A switch now would be a recorded change after the sealed verdict, made after seeing it. The weakness argument is fully available in the paper (the numbers above), so the reader sees it without a ship rule being bent. If Kevin overrides, the papers must state: C1 failed the registered rule; the choice was made by his ruling after R-287 (18:51, 14 Nov); the ruling is a post-result deviation (rule 2, rule 26); every S3 number is given.
