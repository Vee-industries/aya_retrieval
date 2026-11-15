# Lane 3: Evaluation and leakage specialist (hostile)
Verdict: submit after fixes

## Findings (most severe first)
F1. [BLOCKER] ARTICLE.md:54, 619-628, 637-638; HF_ARTICLE.md:176; ABSTRACT.md:22-24: "Names a value when never told" gives base 14 of 236 (5.9%). The flag (`heldout3.false_answer`) counts only values that appear in the chat for that category, or in the writer's `wrong` list. Base makes up values outside the chat all the time, and the flag cannot see them. So the label is false for base, and clause (c)'s base comparator is a floor.
    Evidence: `results/s3/s3_base_tool.json`. Of base's 222 N-hit never_told rows not flagged, a seeded sample of 30 (`l03/s3_sample.py`, seed 3) holds 19 that name a value for the asked fact ("Pilar is married to David.", "Bao has a Shih Tzu.", "Nkechi has a dog named Bella."). The same sample read 1 of 30 for C1 (of 657 unflagged) and 2 to 3 of 30 for 6.37. Rough estimate under R-178's own rubric ("A reply that names any value for the asked fact is wrong", `NEVER_TOLD_RUBRIC`): base about 155 of 236, C1 about 73 of 708. One reader (me, a Claude agent, not blind to arm). R-281 used only the "model-free part", and no reader ever applied the rest of the rubric on S3.
    Fix: keep the registered verdict, since rescoring now would be post hoc. Relabel the measure everywhere as "names a value from the chat". Add one sentence with the counts above: the flag misses made-up values, base makes many of them, so the failed clause shows C1 leaks chat values slightly more than base, not that C1 answers never-told questions with values more often than base.

F2. [BLOCKER] HF_ARTICLE.md:177, ARTICLE.md:648, ship line (a) never_told_plain: "Declines a plain never-told question: base 111 of 120 (92.5%)" is false as worded. The scorer marks a reply right whenever it names no listed value. It does not test whether the reply declines.
    Evidence: I read all 111 of base's plain never_told rows scored right (`s3_base_tool.json`). 28 decline. 56 name a specific made-up value ("Lena supports the Chicago Cubs.", "Haruto drives a 2018 Honda Civic EX."). 15 state an answer the chat never gave ("No, Priya is not dealing with any health issues."). 12 are off topic. Across both views, base names no listed value but gives no decline phrase on 155 of 226 never_told rows scored right (`l03/s3_scorer_probe.py`). For 6.37, 19 of 30 sampled unflagged rows are unrelated stored facts, which is fault (1) of R-177, and the scorer counts them right. The limit appears only in MODEL_CARD.md:205. ARTICLE §12 "Construct validity" names only the scorer's strict side.
    Fix: rename the measure to "names no listed value". Fix ARTICLE.md:170-171 ("names no value of that type"). Add the lenient side, with these counts, to §12 and to HF_ARTICLE's limits.

F3. [MAJOR] ARTICLE.md:99-100 (Terms), HF_ARTICLE.md:127-128: "Copy" is defined as repeating the earlier wrong answer "to the same question". The copy flag is never computed on that question. `copy_flag` leaves out `re_ask` and counts the wrong value in replies to the other older and never_told questions (298 = 178 + 120). The re-ask results, which measure the R-176 fault directly, appear nowhere.
    Evidence: heldout3.py:529-533. Copies by kind: 6.37 older 101, never_told 94; C1 2 and 3. Re-ask right: base 1 of 60, whole chat 17 of 60, code 23 of 60, 6.37 6 of 180, C1 110 of 180.
    Fix: define copy as "names the in-view wrong value when answering another question". Add a re_ask row to the S3 table.

F4. [MAJOR] ARTICLE.md:224 (leakage table, Non-independence): the row describes clustering inside the test. Kapoor and Narayanan's L3.2 is non-independence between train and test. That applies here: `train` and the first sealed pools come from one generator (`conversations.py`: same skeleton, ask forms and five kinds), and `heldout` was written by the same Claude session as `train` (R-039). The headline 91 to 107 of 120 is a within-generator result. On writer chats, seed 82 gets 39 and 53 of 120, and 6.37 gets 27.9% on S3.
    Evidence: R-039 "Why"; conversations.py:14-15 and 70-187; ARTICLE.md:399, 408, 621.
    Fix: add this to the row, and add "made by the same generator as the training chats" to the headline sentence in the Abstract and Submission summary.

F5. [MAJOR] ARTICLE.md:226: "every chat here was written after its release" is false for LongMemEval-S (Wu et al., public 2024 to 2025), which this article uses. For the chats the project wrote, the date already rules out verbatim contamination. The open risk is LongMemEval-S, and the row does not name it. I did not verify Tiny Aya's release date.
    Fix: "the project's own chats postdate the model; LongMemEval-S predates it and may be in pretraining; not probed."

F6. [MINOR] ARTICLE.md:754-755: the human scorer check (R-144, R-145) used 50 lines from `probe` and `hard_dev` only (7 never_told; `results/human_check/R-139/key.json`). No person ever checked S3's flags (copy, false_answer, n_hit), and the confirmatory S3 result rests on them.
    Fix: say this in §12.

F7. [MINOR] ARTICLE.md:221: "Illegitimate features: found and fixed". 6.37's own set still returns 2.27 passages on found rows against 1.90 on never_told rows (R-180).
    Fix: "reduced; mean gap 2.27 against 1.90 remains".

F8. [MINOR] ARTICLE.md:222: "Demo4 and Demo5, checked clean". R-254 reports 5 keys that appear as ordinary words in training text (Demo4 3, 8; Demo5 3, 4, 7). It also records that the writers rewrote their drafts after seeing the list of training values.
    Fix: add both facts.

F9. [MINOR] ABSTRACT.md:8-9: "three judges rated every adapter coherent more often" has no caveat. The judges are Claude Sonnet, were never checked against a person, and see only the turns in view, so they cannot tell a made-up value from a right one.
    Fix: add half a sentence.

F10. [MINOR] ARTICLE.md:100, 308: "whose search returned passages" reads as the model's own search. N-hit is a fixed OR search with no model (`n_hit_query`), and 236 of 240 never_told items qualify.
    Fix: say so.

## What holds up
- The S3 counts match the row files: copies 11/298, 195/894, 5/894; N-hit flags 14/236, 286/708, 51/708.
- The recall scorer is not lenient in a way that matters. On S3, right recall replies that hold a negation or match only inside a longer word number 2 to 15 an arm, nearly all real right answers ("Thursdays"), plus 2 base and 1 C1 true-claim confirms where the reply denies the claim.
- The coherence line (a) passes under all three judges (C1 97/100/98 against base 95/97/99 of 120).
