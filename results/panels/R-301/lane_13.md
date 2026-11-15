# Lane 13: Cold reader

Verdict: clear after fixes

Read first: HF_ARTICLE.md, ABSTRACT.md. My answers were written before I opened docs/ARTICLE.md.

## My answers from the two short texts

1. **Built.** A LoRA adapter (6.37) on Tiny Aya Global (3.35B) that lets the model call a keyword search over chat turns older than the last three exchanges. A second adapter, C1, is published beside it.
2. **Good at:** recalling facts from chats made by the same generator as its training chats (91 to 107 of 120, against 13 to 32 for the untrained model with the tool). **Bad at:** chats from outside writers (whole chat in view recalls more; code that searches every turn recalls as much or more). On S3 it repeats its own wrong answer (21.8%) and names an unrelated stored value on never-told questions (40.4%), far more than the untrained model (3.7%, 5.9%).
3. **Shipped:** 6.37 (seed 82). Reason given: "no replacement passed the rule". That is a reason to keep it, but not a reason it is good; I could not tell why the author did not ship the model that scored better on both faults, other than a rule missed by 1.3 points.
4. **For my own chat assistant:** if the chat fits 8,192 tokens, show it whole to the untrained model, no adapter. If longer, code that searches every turn (simpler, no training, no measured difference from 6.37). Neither adapter.
5. **Lost the thread (quotes):**
   - "missed one clause of a rule fixed before S3 opened by 1.3 points, a gap S3 cannot resolve" (first paragraph; I needed section 6 to understand "clause").
   - "**6.37 stays shipped** because no replacement passed the rule, not because it passed S3." Read twice.
   - "(a) pass / (b) pass / (c) **fail**" in the S3 table: the clauses are in section 4 in one long sentence ("(a) beat base on recall, lose no more than 5 points on in-view, statement and plain never-told ... keep coherence at least base's times 0.95"). Hard to map back.
   - Undefined or late-defined terms: "N-hit", "copy", "never-told" (defined in a long paragraph), "Demo2", "Demo3", "Demo5", "K1", "K1.3", "K2.1", "OP", "report arms", "seed 82" vs "all eight seeds" vs "three seeds pooled", "AgentTune", "CuratorKIT", "AuditKIT", "R-166".
   - "code": "code that searches every turn" is used as a noun for a baseline; first read I thought it meant the repository code.
   - "of 120": what 120 counts (facts? questions?) is never stated in the short paper.
   - "a lead inside the seed-to-seed spread", "Small stages on K1.3 sat inside run-to-run variation": no numbers.
   - "it left only 50 of 60 (83.3%) plain statements unsearched, -13.3 points": "unsearched" is the good outcome; confusing next to "fails".
   - "no measured difference" beside 53 against 34 and 40 (LongMemEval-S); I did not know it means an interval that includes zero.
   - "9 of its 36 layers attend to all of them": why this matters is not said.
   - Section 8's last sentence ("The expectation in hand, exploratory: K1's S3 report arm ... fails if its rate is above base's") is about 90 words and unreadable.
   - "Use this when" says use C1 "if both faults matter" while C1 is "not the shipped model" and fails a registered clause. The advice and the shipping decision point in opposite directions.
   - Abstract: "S3's flags see only listed values of the asked category" needs the flag definitions I did not have.

## Check against docs/ARTICLE.md

**Answered:** Terms section defines Base, Tool, Code, Whole chat, Recall, In view, Never told, Statement, Seed 82, Copy, N-hit false answer, confirmatory/exploratory. Table at line 920 defines OP ("a stage on K1.3's own mistakes"). AuditKIT and CuratorKIT roles are described (lines 283-289). The "Use this when" paragraph is repeated, not expanded.

**Not answered:** (a) why 6.37 rather than C1 or K1 is shipped beyond the rule, and why the rule was kept after the author's own stated position that the aggregate should have decided; (b) what "120" counts is only implied by the Recall definition; (c) K1, K1.3, K2.1 are explained only in a late ledger table, not in the Terms; (d) "no measured difference" is given with an interval in the abstract (+5.2, -0.8 to +11.3) but the short paper omits it; (e) no plain statement for a reader choosing a model: "I would not deploy 6.37 on outside chats."

## Fixes that would make it clear
1. Add a "Terms" block to the short paper (recall, copy, N-hit, never-told, code, whole chat, K1/K1.3/OP/Demo) in two lines each.
2. Put the three ship-rule clauses in a list; label table rows with them.
3. Say what 120 counts; explain "no measured difference" once (interval spans zero).
4. Split the section 8 final sentence into three.
5. Reconcile "Use this when" with the shipped model in one sentence.
