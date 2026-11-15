# Lane 10: Practitioner (critical), round 3
Verdict: submit after fixes. At 2,441 words (`wc -w`) the short paper is the right size and now answers "what to use when" near the top; what is left is undefined labels in sections 5 and 6, a muddled last paragraph in section 8, and a figure and table that show different seeds without saying so.

## Round-2 findings: status (one line each)
F1 (3,957 words) fixed: 2,441 words; the opening paragraph is about 150 words.
F2 (no "what to deploy") fixed: "Use this when" sits directly under the opening and names whole chat, code and C1 (lines 15-18).
F3 (seed 82 range 44 to 55 against 52/52/46/44) fixed: the 58- and 419-message views are now separate (lines 71-74).
F4 ("too long to show whole" a memory-cap effect) fixed: line 73 says so, with R-166.
F5 (demo-rule change told twice) partly fixed: section 5 (117-122) and section 7 (155-158) are shorter but still both list the demo-rule change.
Round-2 cut list: followed, including moving whole_chat_or_search.png and s3_misses.png out.

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md:77-80 against figures/recall_out_of_view.png: the table's 6.37 column is seed 82 (39 / 53 of 120 = 32.5% / 44.2%); the figure's dots for the same two sets are eight seeds pooled (40% and 43%) and the figure omits the whole-chat arm (71 / 65), the arm that makes the opening's "weak on outside chats" claim. The text never says which seed the table is. A reader who compares 33% in the table with 40% in the figure sees a mismatch, and a reader of the figure alone sees 6.37 beating the untrained model on outside chats, not losing to the whole chat.
    Evidence: figure legend "6.37, eight seeds pooled"; table has no seed label; opening line 7 says "91 to 107 of 120" (seed 82) while line 65-66 gives pooled 85.2 to 90.4% with no label.
    Fix: head the table "6.37 seed 82" and line 7 "the shipped seed recalls"; add to the figure's subtitle "outside-writer sets: whole chat recalls 71 and 65 of 120 (table below)".

F2. [MAJOR] HF_ARTICLE.md:168-171: the last "With more credits" paragraph contradicts itself ("the result expected being that rule's pass or fail, not a forecast" then "The records hold no forecast of recall. The expectation in hand ... is expected to read like that"). K1 is also never introduced in the short paper (it first appears at line 145 as a "report arm"). A ten-minute reader cannot parse it.
    Fix: cut after "judge applying the full never-told rubric". One sentence: "K1 (two seeds, exploratory) met every S3 line; a sealed test of it is the next step."

F3. [MINOR] HF_ARTICLE.md:109-113 and 144-146: K1, K1.3, K2.1, OP, "stage" and Demo2 to Demo5 are used with no definition ("Training K1.3 on corrections of its own errors gave OP, and the same stage twice gave C1"). The reader cannot follow the chain and does not need to.
    Fix: replace section 5's first paragraph with "Candidates were registered before they were built; the pick had the highest development recall among those passing a line against base (R-191, R-192)" and drop the K1.3/OP chain; in section 6 write "three earlier candidates (report arms)" and name them only in the figure.

F4. [MINOR] figures/s3_faults.png: the row "6.37, shipped" is the three-seed pool (195/894), while the table's "(shipped)" column is seed 82 (62/298). Same word, different numbers.
    Fix: relabel the row "6.37, three seeds".

F5. [MINOR] HF_ARTICLE.md:102-104: clause (b) "copy at most half as often as 6.37 and 10 points less" does not say both conditions must hold. Fix: "both at most half as often and 10 points less".

F6. [MINOR] demo_contamination.png reads at a glance, but section 5 places it before the paragraph that explains why the demos mattered; move it after "How C1 became the pick" or drop it (two sentences carry it).

## What holds up
Story order (task, build, first sealed test, faults, rule before test, S3, limits) is clear; C1's 1.3-point miss is stated in the opening, the table and the figure.
S3 table counts match the figure (195/894, 5/894, 286/708, 51/708, 14/236); "91 to 107 of 120" and "13 to 32" match README.md:6 and R-162.
The paper stands without the long one for what was built, what works and what to use.
