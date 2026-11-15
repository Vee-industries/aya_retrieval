# Lane 8: Voice editor (round 3)
Verdict: submit after fixes (wording only; no number changes; 0 em/en dashes, 0 "we/our/us", 0 stance adverbs in the five documents and the in-scope long-paper sections)

Files: ARTICLE = docs/ARTICLE.md, HF = docs/submission/HF_ARTICLE.md, ABS = docs/submission/ABSTRACT.md, MC = docs/MODEL_CARD.md, C1 = docs/MODEL_CARD_C1.md. Line numbers are of commit 48c6586.

## Round-2 findings: status
F1 ("I hold that...") fixed: ARTICLE:564, HF:139 now "R-294 records my position...".
F2 ("a miss is a miss") fixed: ARTICLE:37, HF:105, ABS:26.
F3 partly: "a part most layers do not see" fixed (ARTICLE:134). Not fixed: ARTICLE:453-454, ARTICLE:506.
F4, F5, F6, F7, F9, F14, F15, F19 fixed (HF:255 and ARTICLE:735 now say the 419-message run ran out of memory; MC:113 and MC:210 plain).
F8 partly: HF:120 fixed. Not fixed: ARTICLE:530 and 659.
F10 partly: MC:121 "about 15", MC:123 "about the same length" remain.
F11 partly: "far" remains at ARTICLE:91, HF:18, MC:104, HF:86.
F16 partly: nested parentheses remain at HF:145-146.
F17 not fixed: ARTICLE:166-167 "follows STaR", and the 10-citation run at 161-168.
F18 partly: ABS:30 (see F9 below).
F12, F13 are in section 6.2, outside this round's sections; not rechecked.

## New findings (most severe first)
F1. [MAJOR] ARTICLE:730-733 and 738-739, HF:168-171: the future-work paragraph says "not a forecast" and then "a sealed test of K1 is expected to read like that". An expectation is a prediction with the author's stance (voice 11: no "will"/"plan"). "The records hold no forecast of recall" appears twice in ARTICLE.
    Fix: "A sealed test of K1 on a new set of outside chats under S3's rule; the rule decides pass or fail." End the K1 sentence at "against base's 14 of 236 (5.9%). A sealed test of K1 passes (c) if its rate is no higher than base's." Delete the second "The records hold no forecast..." (ARTICLE:738-739).
F2. [MAJOR] ARTICLE:72: "On outside chats it mostly answers a never-told question with another stored fact". "Mostly" has no count, and the counted claim is on S3.
    Fix: "On S3 it names a stored value on 402 of 708 never-told questions whose search returned text (56.8%, Appendix C; R-298)."
F3. [MINOR] ARTICLE:453-454: "The demo showed results I had missed, and the extra day gave enough time to train further" (voice 3.5, what the author missed).
    Fix: "The deadline was reported extended (R-173). I reopened the project to fix the weakness the demo showed; the extra day allowed further training (R-177)."
F4. [MINOR] Counts replace "most" and "mostly": ARTICLE:506 "most had the fact absent" becomes "106 of OP's 117 errors about the user on its own items had the fact absent from its own search output (R-267)" (checked, RECORDS.md line 9840-9841). ARTICLE:839-840 "mostly on `confirm`" and "most misses there are facts it found and did not use" become "18 of its 28 misses in C and 20 of 29 in D are on `confirm`; 19 and 20 are facts it found and did not use" (92 and 91 right of 111 found).
F5. [MINOR] ARTICLE:530 and 659: "too poor to judge by". Fix: "one demo's six older questions are too few to rank these models" (as HF:120).
F6. [MINOR] HF:6: "strong on ... and weak on" is evaluative. Fix: "It recalls 91 to 107 of 120 facts on chats from the generator that made its training chats, and 39 and 53 of 120 on chats from outside writers."
F7. [MINOR] "rarely": ARTICLE:81 becomes "it searched on 7, 0 and 5 of 58 'did I tell you...?' questions by seed on S3". MC:27 "which base rarely does" needs the count from R-146 and R-157 (RECORDS.md shows base searching 58 of 96 on `hard_dev`, so "rarely" is not general).
F8. [MINOR] "few" and "many": MC:170 and 208 "Every arm answers few questions" becomes "No arm judged right more than 53 of 248". C1:60 "invents many values" becomes "invents values".
F9. [MINOR] ABS:30 "S3's scorer was written before any S3 file was read" omits deviation 13 (ARTICLE:660, "Written after S3 started"). Fix: "S3's scorer was written after the S3 runs began and before any S3 file was read (R-281)."
F10. [MINOR] "far": ARTICLE:91, HF:18, MC:104 "far lower rates" becomes "rates lower by 97% and 82%"; HF:86 "far past the window" becomes "past the window".
F11. [MINOR] "only": ARTICLE:566, HF:140 "left only 50 of 60" becomes "left 50 of 60".
F12. [MINOR] "simpler": ARTICLE:90, HF:17, MC:101 "code is simpler and trains nothing" becomes "code needs no training".
F13. [MINOR] ARTICLE:693 "Both directions matter." has no propositional content. Delete it.
F14. [MINOR] MC:121 "gaps under about 15 points" becomes the computed threshold (R-142, R-165) or "gaps under 15 points"; MC:123 "of about the same length (58 messages, 1,105 to 1,332 tokens)" becomes "of 58 messages, 1,105 to 1,332 tokens".
F15. [MINOR] HF:145-146: "(12 of 472 (2.5%) and 14 of 472 (3.0%) on (c))" and "(37 of 472 (7.8%))" nest parentheses. Fix: "K1 and K2.1 name a listed value on 12 and 14 of 472, 2.5% and 3.0%; K1.3 on 37 of 472, 7.8%."
F16. [MINOR] ARTICLE:166-167 "follows STaR": "Training on a model's own outputs that pass a check is STaR (Zelikman et al., 2022)." Keep only the citations the text uses by name.

## What holds up
- Section 12, section 14's list of gaps, Appendices A to C and C1's "Limits" state limits as facts with counts.
- First person for decisions ("I reopened", "I changed the test") and present tense for the apparatus follow voice 7.
- ABS is 465 words (under 500).
