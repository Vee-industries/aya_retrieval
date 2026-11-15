# Lane 8: Voice editor (round 2)
Verdict: submit after fixes (10 of 21 round-1 findings fixed, 8 partly, 3 not; no em dash, no "we/our/us", no stance adverb in any of the five documents; the new findings are wording only and none changes a number)

Scope read in full: kv_voice_v2; HF_ARTICLE.md; ABSTRACT.md; MODEL_CARD.md; MODEL_CARD_C1.md; ARTICLE.md lines 1 to 162 (Abstract, Submission summary, section 1), 409 to 917 (sections 6.2 to 15). Line numbers are the built files (`docs/ARTICLE.md` = ARTICLE, `docs/submission/HF_ARTICLE.md` = HF, ABS = `docs/submission/ABSTRACT.md`, MC = `docs/MODEL_CARD.md`, C1 = `docs/MODEL_CARD_C1.md`). Commands run: grep for U+2014/U+2013, " -- ", whole-word we/our/us/ours, the section 3.1 stance list, the section 3.2 hedge list, the section 3.3/9.2 marketing list, plus `most|far|best|poor|many|few`. All stance, we/our and dash counts are 0 in the five files. STANDARD.md exists in the repo, so the "STANDARD rule N" citations are openable.

## Round-1 findings: status
F1 partly: HF:146 fixed ("I reopened the project to fix the weakness the demo showed; the extra day allowed further training"). ARTICLE:512 still reads "The demo showed results I had missed, and the extra day gave enough time to train further".
F2 fixed: ARTICLE:584-585 and HF:147-148 ("R2c's passes sat inside run-to-run variation ... I moved to a different method").
F3 fixed: HF:172 "Demo2's and Demo3's answers are fact values in the training chats".
F4 fixed: ARTICLE:34 "24 candidates were listed for screening (R-279) and six were read on all 20 lines".
F5 fixed: HF:266 "only the plan (R-001) and my chat engine LLE".
F6 partly: "C1 removed most of both faults" is gone (now -97% and -82%, ARTICLE:678-679). Still "most": ARTICLE:128 and HF:39 "a part most layers do not see"; ARTICLE:594 "most had the fact absent from its own search output".
F7 partly: fixed are "Code pays" (ARTICLE:692 "Code is worse on every other kind"), "flatter" (HF:245, ARTICLE:786 "overstate"), "The four stages" (ARTICLE:575), "reachable only through one tool" (HF:49). Not fixed: ARTICLE:767 "6.37 is a poor bar for recall".
F8 partly: ARTICLE section 14 (835-842) now states gaps as facts; HF:255-257 likewise. Not fixed: HF:255 "The whole chat on chats too long to fit is not measured" (419-message chats fit the 8,192-token window; HF:7 says so). ARTICLE:839 "not measured on a card that holds it" leaves open what the card is.
F9 partly: ARTICLE and HF now say "a mean of 1,400 tokens"; "about five pages" and "the few typed" are gone. Remaining: MC:113 "about 1,400 tokens a chat" (MC:23 and 187 say "a mean of 1,400"); MC:140 "about 6,236 tokens"; MC:119 and ARTICLE:440 "gaps under about 15 points".
F10 partly: HF has no "far". Remaining: ARTICLE:444 "far worse"; MC:135 "far above both references"; MC:188 "far below"; ARTICLE:405 (section 6.1, outside my sections) "far above both".
F11 fixed: no "best" in the five files.
F12 not fixed: ARTICLE:694 "when the chat fits, show it whole"; MC:111 heading "give it the whole chat"; MC:186 "show it the whole chat". These are use advice, not findings. HF:57 and ARTICLE:84 "Use this when" is a model-card style block and may stay; the sentence at ARTICLE:694 can become "On chats that fit, base with the whole chat recalls the most."
F13 partly: HF:12-14 and ABS:13-15 fixed ("no measured difference"). Remaining: ARTICLE:146 "both match or beat the adapter on recall" (code's 47 is below 6.37's 53 on set 2); MC:111 heading and MC:125 "recalls as well as this adapter".
F14 partly: ARTICLE:658 fixed. Remaining: ARTICLE:37 "but a miss by one line is a miss", HF:210 "A miss by one line is a miss", ABS:26 "but a miss is a miss".
F15 fixed: ARTICLE:809 "Not probed, or not ruled out."
F16 fixed: ARTICLE:788 "spans 73 to 90 of 96 by seed".
F17 fixed: ABS:20 and ARTICLE:30 "I reopened the project".
F18 not fixed: ARTICLE:158 "follows STaR" (the section 10 pattern "approach of"); the 12-citation run at ARTICLE:153-160 is unchanged.
F19 not fixed: ARTICLE:619, ARTICLE:770 and HF:184 "too poor to judge by".
F20 not fixed: "read many times" at HF:44, 77, 245; ARTICLE:121, 786.
F21 fixed: ARTICLE:129 "code outside a Llama model".

## New findings (most severe first)
F1. [MAJOR] ARTICLE:662 and HF:211: "I hold that the aggregate should have decided; that view is stated, not applied (R-294)." This is a stance-bearing first-person introducer (3.4), and a defence of the result placed beside the rule's verdict. The decision to state it is Kevin's; if kept, state it as a fact about the record.
    Evidence: voice 3.4 and 3.5; sentence added by the round-1 fixes (R-294).
    Fix: "R-294 records my position that the pooled result should have decided; the registered rule was applied." Or delete it and keep "R-178 requires every clause to pass, so 6.37 seed 82 stays shipped".

F2. [MAJOR] ARTICLE:37, HF:210, ABS:26: "a miss (by one line) is a miss" is a rhetorical tautology. Its force comes from the author's attitude, not from added content (2.1, 2.3). ARTICLE:658 already has the plain form.
    Fix: ARTICLE:37 "and the registered rule requires every clause to pass: by the registered rule, 6.37 stays shipped (R-287)." HF:210 "The registered rule requires every clause to pass, so 6.37 stays shipped". ABS:26 "cannot tell them apart; the registered rule requires every clause to pass, so 6.37 stays shipped".

F3. [MAJOR] ARTICLE:512; ARTICLE:594; ARTICLE:128 and HF:39: the three remaining round-1 breaches with known counts.
    - ARTICLE:512: "The deadline was reported extended (R-173). I reopened the project to fix the weakness the demo showed; the extra day allowed further training (R-177)."
    - ARTICLE:594: "Of OP's 117 errors about the user on its own items, 106 had the fact absent from its own search output (R-267, RECORDS.md line 9840)".
    - ARTICLE:128 and HF:39: "a part 27 of 36 layers do not see" (ARTICLE:126-127 gives 9 of 36 attending to all).

F4. [MAJOR] HF:255: "The whole chat on chats too long to fit is not measured." The paper's own account (HF:7, MC:140-143) is that the 419-message chats fit the window and ran out of card memory. A reader sees a contradiction.
    Fix: "The whole chat at 419 messages is not measured (it ran out of memory on the 10 GB card, R-166)." ARTICLE:839: same wording in place of "on a card that holds it".

F5. [MINOR] ARTICLE:146: "on short chats, both match or beat the adapter on recall". Code scores 47 against 6.37's 53 on set 2 (ARTICLE:426).
    Fix: "on short chats, the whole chat recalls more, and code shows no measured difference". MC:111 heading: "when the chat fits, give it the whole chat; code shows no measured difference from the adapter"; MC:125: "recalls as well as" becomes "shows no measured difference from".

F6. [MINOR] MC:207 and MC:152: "goes along with most false claims" / "goes along with the rest". "Goes along" is an idiom and "most" has a count (6.37 corrects 1 and 3 of 20).
    Fix: "It corrects 1 and 3 of 20 false claims in tag questions (R-164)."

F7. [MINOR] ARTICLE:767: "6.37 is a poor bar for recall" is evaluative. Fix: "6.37 is the model whose weakness was found; the published comparison was against base". ARTICLE:529 already says this.

F8. [MINOR] ARTICLE:619, 770 and HF:184: "too poor to judge by" restates the next clause. Fix: "one demo's six older questions are too few to rank these models" (ARTICLE:799 already says "too few to rank close models (R-283)").

F9. [MINOR] "orchestrator" at HF:232 and ARTICLE:771 is an undefined internal term. Fix: "partly seen by the Claude session that ran the work, through a judge's marks".

F10. [MINOR] Approximation words on exact numbers: MC:113 "about 1,400 tokens" to "a mean of 1,400 tokens"; MC:140 "about 6,236 tokens" to "6,236 tokens"; MC:102-103 "declines half the questions that have an answer (233 of 470)" to "declines 233 of the 470 questions that have an answer"; ARTICLE:450 "about as often as base" to "base 1 and 0"; ARTICLE:440 and MC:119 "gaps under about 15 points" to the computed threshold or "gaps under 15 points".

F11. [MINOR] Intensifiers (3.1): ARTICLE:444 "far worse" to "worse"; MC:135 "far above both references" to "above both references: 44 to 55 of 60 against code's 14 to 32"; MC:188 "far below" to "below"; ARTICLE:405 same.

F12. [MINOR] ARTICLE:442-443 repeats itself: the bold heading says "no measured difference" and the sentence ends "p = 0.45 on set 2): no measured difference." Delete the second.

F13. [MINOR] ARTICLE:447 and ARTICLE:137: "6.37 searches more often than base (37 against 38, 35 against 39)" gives left-unsearched counts as if they were search counts, so the reader sees a larger number for the model said to search more. Fix: "6.37 left 37 and 35 of 40 statements unsearched, against base's 38 and 39."

F14. [MINOR] HF:65 and ARTICLE section 4 equivalent: "seed 82 was named to ship before most of them existed". "Most" of eight seeds; R-092 and R-141 hold the count. Fix: give the count ("before N of the eight existed").

F15. [MINOR] ARTICLE:36, ABS:25, MC:55: "the second had to be no higher than base's": "the second" does not name its object. Fix: "the N-hit false-answer rate had to be no higher than base's".

F16. [MINOR] Nested parentheses in the headline paragraphs: HF:15-16 and ABS:16 "(53 against 40 of 248 (+5.2 points, 95% interval -0.8 to +11.3, p = 0.12); Claude judges ...)". Voice 8.5 limits parentheses to asides. Fix: move the interval into a following sentence.

F17. [MINOR] ARTICLE:158 and the run at 153-160 (F18 of round 1): "follows STaR" and a chain of 12 cites. Keep the items the text uses by name (Self-RAG, RAFT, LongMemEval, LoRA, STaR), and write "Training on a model's own outputs that pass a check is STaR (Zelikman et al., 2022)."

F18. [MINOR] ABS:30: "Both sealed tests and their rules were registered before they ran". Deviations 13 and 17 (ARTICLE:772, 776) say S3's scorer was written after S3 started and the first test's rule was amended three times before the held-out run. Not a breach of voice; a claim that reads stronger than the table. Fix: "Both sealed tests' rules were registered before they ran; the S3 scorer was fixed after S3 started and before any S3 file was read (R-281)."

F19. [MINOR] ARTICLE:184 (section 3, outside my sections) "Everything earlier sits behind one tool": the HF fix (reachable only through one tool) did not reach the long paper.

## What holds up
- Dashes, "we/our/us", stance adverbs, "I show/find/claim", "novel/robust/powerful": 0 in all five files (grep).
- Limits and disclosures (ARTICLE:780-820, HF section 7, C1 card "Limits") read as facts without apology; the "not blind to the hypotheses" line and the section 11 table are flat and unhedged.
- Person and tense follow 7.5: "I opened S3 once", "6.37 stays shipped", present tense for the apparatus. The round-1 fixes to ABS (first person for decisions) hold.
