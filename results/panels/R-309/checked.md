# R-309: the editorial review (`review.md`) checked against the papers

Checked by the orchestrator, 15 November, before any change; line numbers are those of the built files at ca1af5d.
Every number the review cites matches the papers, `results/s3/ship_rule.json`, RECORDS or Appendix C.

## Held, applied as proposed

1. Long 79-81 named the whole chat as beaten at 419 messages; it ran at 58 only (R-166 out of memory, R-168). Also long
   613 and 767-768.
2. The N-hit Terms (long 138, HF 24) said "a value listed for the chat". The scorer (`heldout3.py`, `false_answer`)
   flags the item's `wrong` values and the chat values of the asked category, as long 774 and HF 171 and 200 say.
3. Long 177-180 counted statements left unsearched as a gain over code; code searches every statement by construction
   (R-168).
4. Long 590-592, "what ships did not depend on the change": K1.3's two S3 seeds gave 9 and 28 of 236; a third would have
   needed 5 or fewer (42 of 708, base's rate) and was not run. Now stated as not shown.
5. HF 122, LongMemEval-S 53 against 40: on the 233 answerable questions 6.37 ties code, 40 against 40. The review's text
   left out the long paper's label "split after reading the registered result"; the label is kept.
6. HF: why C1 failed (c), the development false-answer gate compared with 6.37, not base (long 662-663).
7. HF: the wider N-hit count (R-298) moved beside the 1.3-point miss.
8. Long 825-833 repeated Appendix C; now a pointer to it.

## Held after a fix

- HF Claim: the S3 faults added, as proposed.
- `older` alone in HF: a sentence, not a table row; the proposed row needed a seed 82 count that neither paper holds.
- The 6.37 against C1 paragraph (review P9), added to long section 9, not the Abstract. As written it said 6.37 is
  "below C1" on copies and N-hit false answers, where 6.37 is higher (worse): 195 against 5 of 894, 286 against 51 of
  708. It also put recall among C1's gains, where the papers report no measured change. Its "on no outside set did 6.37
  measure above" now reads "show a measured difference above", since 6.37's 53 is above code's 40 on LongMemEval-S
  with p = 0.12.

## Not applied

- Cutting the HF stage table (157 words): it is the only date-to-record map in the short paper; kept.
- A new conclusion section: the P9 paragraph is in section 9 instead.
- Future work reordered with the query-writing isolation design first: the research order is Kevin's; not changed.
- The derived 62 right `confirm` answers (347 minus 285): correct arithmetic, not used; it would need a generated key.
- Minor items (stage tables differ, section 8 heading, the "no measured difference" either-or rule): no change.
