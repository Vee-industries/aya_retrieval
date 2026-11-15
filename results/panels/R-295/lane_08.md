# Lane 8: Voice editor
Verdict: submit after fixes (no em dashes, no "we", no "I show that" forms in the three documents; 21 findings, wording only, none changes a number)

Scope read: kv_voice_v2 in full; HF_ARTICLE.md and ABSTRACT.md in full; ARTICLE.md Abstract, Submission summary, sections 1, 7, 8, 9, 12, 14. Line numbers are the built files. Checked by command: `grep` for U+2014/U+2013 gives 0 in all three; whole-word we/our/us gives 0 in all three. I did not read ARTICLE.md sections 2 to 6, 10, 11, 13, 15, so breaches there are not covered. Of the scanner's template hits, "as often as", "could not", "about 1,400" counted below; the rest (record ids, code, tables) are plain.

## Findings (most severe first; ARTICLE = docs/ARTICLE.md, HF = docs/submission/HF_ARTICLE.md, ABS = docs/submission/ABSTRACT.md)

F1. [MAJOR] ARTICLE:494; HF:122: concession about what the author missed (3.5). "The demo showed results I had missed, and the extra day gave enough time..."
    Fix: "I reopened the project to fix the weakness the demo showed (R-177); the extra day allowed further training."

F2. [MAJOR] ARTICLE:567-568; HF:146: luck framing, hedge and "approach" (3.2, 3.5, 9.2). "Since those passes could be lucky draws, I moved to a different approach (R-253)."
    Fix: "R2c's passes were within run-to-run variation, so I moved to a different method (R-253)."

F3. [MAJOR] HF:147: "turned out to be" is the forbidden "turns out" (2.3). Fix: "Demo2's and Demo3's answers are fact values in the training chats".

F4. [MAJOR] ARTICLE:28-29: sentence has no verb: "From 12 to 14 November, 24 candidates in the screening list of R-279, six of them read on all 20 lines; C1 became the pick."
    Fix: "From 12 to 14 November, 24 candidates were listed for screening (R-279) and six were read on all 20 lines; C1 became the pick."

F5. [MAJOR] HF:225-226: "the plan (R-001) and the my chat engine LLE" is ungrammatical. Fix: "only the plan (R-001) and my chat engine LLE".

F6. [MAJOR] "most" for a count, where the count is known (3.2 vague quantifier). The counts exist.
    - ARTICLE:646 "C1 removed most of both faults": "C1 reduced both faults: copies by 97%, N-hit false answers by 82%."
    - HF:11 and ARTICLE:70 and ABS has no such phrase; same fix.
    - ARTICLE:577-578, HF:155: "most of OP's remaining errors" / "most had the fact absent": "106 of OP's 117 errors about the user had the fact absent from its search output (R-267)" (RECORDS.md line 9841).
    - ARTICLE:109: "a part most layers do not see": "a part 27 of 36 layers do not see" (9 of 36 attend to all).

F7. [MAJOR] Metaphors (agent card and Kevin's no-metaphor rule). 
    - ARTICLE:660 and HF:189 "Code pays for it on every other kind" / "Code pays on everything else": "Code is lower on every other kind:".
    - ARTICLE:743 and HF:208 "development numbers flatter what was chosen": "development numbers overstate the chosen candidate's performance".
    - ARTICLE:511 "a poor bar for recall": delete; "because 6.37 is the model whose weakness was found, and the published comparison was against base."
    - ARTICLE:558 "The story in four turns": "The four stages."
    - HF:39 "Everything older sits behind one tool": "Everything older is reachable only through one tool".

F8. [MAJOR] ARTICLE:787-791 and HF:215-216: Future work is a plan ("In order: train...", "Next. Train...") (11: "Avoid 'future work will'"; "The S3 result names the next step" is also personification). Fix, state as facts: "Query writing is untrained; it is the largest recall loss on S3 (661 of 878 wrong recall answers). The whole chat is not measured at 419 messages. LoCoMo is not run (R-100). Instructions hidden in retrieved passages are not tested. Reward-based training on the search decision is not tried. The lean loss and the bootstrap fix are not offered to TRL and AuditKIT." Also HF:216 "chats too long to fit" contradicts ARTICLE:789 "a card that holds it" (419 messages is about 6,200 tokens, under the 8,192 limit; README:325 says it ran out of card memory). Use "at 419 messages".

F9. [MINOR] Approximation hedges where the number is exact (3.2).
    - "about 1,400 tokens": ARTICLE:64, 393; ABS:11; HF:97; README. `make_article.py:258` computes the mean to the unit. Fix: "mean 1,400 tokens".
    - ARTICLE:5: "about five pages". HF is 3,103 words. Fix: "The short version (3,103 words)". (Or drop the page claim.)
    - ARTICLE:9 and HF:25 "except the few typed from the record": section 15 names four items. Fix: "except the four items section 15 lists".

F10. [MINOR] Intensifiers (3.1): HF:95 "far above both"; HF:110 "far longer than the model's context"; ARTICLE "far"/"far above" in summary line 66 ("recall far above base and code").
    Fix: "seed 82 recalls 44 to 55 of 60, code 14 to 32"; "histories of about 115,000 tokens against an 8,192-token window" (README:148 gives the 115,000); line 66: "recall 44 to 55 of 60 against code's 14 to 32 (R-168)".

F11. [MINOR] ARTICLE:64: "the whole chat recalls best" (9.2, "best" needs its comparison; also README, MODEL_CARD). Fix: "recalls most".

F12. [MINOR] ARTICLE:662, HF:105: "when the chat fits, show it whole" is advice, not a finding. Fix: "On chats that fit the context, base with the whole chat recalls most."

F13. [MINOR] ARTICLE:128, HF:105, ABS:13, ARTICLE:22, 65: "match or beat" / "recalls as well as 6.37" while ARTICLE:424 reports only "no measured difference" (p = 0.76, 0.45). Fix: "code recalls 42 and 47 against 6.37's 39 and 53 (no measured difference, p = 0.76 and 0.45)". In ABS this replaces "recalls as well as 6.37 (42 and 47 against 39 and 53)".

F14. [MINOR] ARTICLE:638: "A miss by one line is a miss (STANDARD rule 2)" cites an internal file the reader cannot open (10) and repeats the preceding sentence (5). Fix: "The rule registered before S3 opened (R-178) requires every clause to pass; (c) failed, so 6.37 seed 82 stays shipped."

F15. [MINOR] ARTICLE:760: heading "Probed but not ruled out" over items that say "not probed" and "no check was run". Fix: "Not probed or not ruled out."

F16. [MINOR] ARTICLE:745: "Seed noise is large" (evaluative). Fix: "6.37's `hard_dev` recall spans 73 to 90 of 96 by seed".

F17. [MINOR] ABS:18-19: "the project was reopened" hides the decision-maker (7.4; decisions are Kevin's). Fix: "I reopened the project." Same in ARTICLE:27 ("the project was reopened (R-177)").

F18. [MINOR] ARTICLE:135-142 Related work: the pattern "A (cite), B (cite), C (cite)" §10 names as performance, and "follows STaR" (§10 avoids "following the approach of"). Fix at least: "Training on a model's own outputs that pass a check is STaR (Zelikman et al., 2022)." and keep only items the paper uses by name (Self-RAG, RAFT, LongMemEval, LoRA, STaR).

F19. [MINOR] ARTICLE:600-601, HF:163-164: "too poor to judge by" restates the next clause (5). Fix: delete it; keep "K1.3 scored 1 of 6 on Demo4 and 3 of 6 on Demo5, two demos from one brief."

F20. [MINOR] "read many times" (HF:35, 61, 208; ARTICLE:743): a count exists in RECORDS.md; give it or "read at every candidate".

F21. [MINOR] ARTICLE:110 "code around a Llama model": "code wrapped" is also spatial; "with code outside a Llama model" is plain.

## What holds up
- No em dash, no "we/our/us", no "I show/find that", no "interestingly/clearly/novel/robust" in any of the three documents (grep, counts 0).
- Limits (ARTICLE section 12, HF section 7) and disclosures are stated as facts without apology, apart from F1, F16, F20.
- Tense and person follow section 7.5: "I opened S3 once", "6.37 stays shipped".
