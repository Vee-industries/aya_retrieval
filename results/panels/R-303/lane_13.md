# Lane 13: Cold reader

Verdict: clear after fixes

Read: HF_ARTICLE.md, ABSTRACT.md, then (after writing answers) the first 150 lines of docs/ARTICLE.md.

## My answers (written before opening ARTICLE.md)
1. **Built:** a LoRA adapter (6.37) on a 3.35B model (Tiny Aya Global). It sees only the last three exchanges and calls a text-search tool over older turns to recall facts. A second adapter, C1, is published beside it.
2. **Good:** chats from the generator that made its training chats: 91 to 107 of 120 facts against 13 to 32 untrained. **Bad:** chats by outside writers (whole chat in view recalls more; code that searches every turn is no different or better); on S3 it repeats its own wrong answer (21.8% vs 3.7%) and names a stored value on never-told questions (40.4% vs 5.9%).
3. **Shipped:** 6.37. A rule fixed before S3 needs every clause; C1 missed one by 1.3 points. The paper says it ships because no replacement passed, not because it passed.
4. **My assistant:** chat fits 8,192 tokens: show the whole chat, no adapter. Longer: code that searches every turn, no training. Not 6.37 or C1.
5. **Lost the thread:**
- "the whole chat recalls more and code that searches every turn shows no measured difference" (Result first): the comparison target is missing; I had to guess it means 6.37.
- "C1 cut both faults and missed one clause of a rule fixed before S3 opened, by 1.3 points, a gap S3 cannot resolve." Two clauses, a number and a clause about resolution in one sentence; I read it three times.
- "S3" is never spelled out (only "a second sealed test"); "R-xxx", "H2", "N-hit", "K1, K1.3, OP", "Demo2 to Demo5" are used before or without meaning.
- "On S3, a second sealed test from outside writers, code recalls more, and 6.37 repeats its own wrong answers and names values on never-told questions more often" ("Result first"): "names values" has no object until the Terms.
- "Use this when": "names a listed value on 57 of 236 (24.2%) ... against base with the tool's 14 of 236" is hard to parse; "listed" and "N-hit" are defined only in Terms below.
- "I first ruled ... six minutes later I changed the test" (section 5): reads as a confession with no stated consequence.
- Table in section 6: "C1's line" column with "(a) pass" refers to clauses (a)-(c) defined two sections earlier.
- "Grounds ... answered 288 of 480 ... as often as base on code's passages": "grounds" is jargon.
- Section 7: "plain never-told rates ... are ceilings": unclear direction.
- Never stated plainly: that 6.37, the shipped model, is the worse one on the two faults, and why a reader should not use it (only implied by "Use this when").

## After opening docs/ARTICLE.md
Answered: its Terms list defines Tool, Seed 82, Never told, Statement, Copy, N-hit with fuller wording; its "For judges: one minute" states plainly where it fails. Did not answer: S3 is still not spelled out; the abstract is the same sentence-dense style; the "worse than untrained on both faults yet shipped" tension is not resolved in plain words; the R-numbers still need RECORDS.md.

## Fixes suggested
Define S3 and N-hit in the first paragraph; split the C1 sentence; state the recommendation in one line at the top ("do not use 6.37 for a chat assistant; here is what to use").
