# Lane 10: Practitioner (critical), round 2
Verdict: submit after fixes. Most round-1 fixes landed, but the short paper is still 3,957 words (the author wants about 5 pages), the opening paragraph is one 449-word block, and the "Use this when" box does not say which of code, 6.37 or C1 to pick.

## Round-1 findings: status
F1 (generator-chat vs outside-writer gap not stated early) partly fixed: HF_ARTICLE.md:6-7 now says 6.37 "beats plain code only where the chats come from the generator that made its training chats". The 28 to 44% recall on outside-writer chats is still only in the table (line 119) and in section 6; the opening does not give it.
F2 (no "what to use when") partly fixed: a "Use this when" paragraph was added (lines 57-60). It sits inside section 1 after the threat model, not at the top. It does not say what to use for a chat that is too long (code is simpler and ties 6.37 on LongMemEval-S, line 10-11, but is not named in the box), and it does not say which of 6.37 or C1 to deploy.
F3 (whole_chat_or_search.png against the table) partly fixed: the axis now reads "Older-fact questions answered right (not confirm questions; the tables give recall)" and the subtitle is "no measured difference". The dots are still older-only (untrained set 1 shows 14%, the table's recall is 26 of 120 = 22%), and the figure still omits the code arm that the table compares.
F4 (never_told_slide.png cut off) fixed by removal: the figure is not referenced in HF_ARTICLE.md (grep: only s3_faults is linked for S3). I did not re-check the png itself.
F5 (s3_faults / s3_misses row labels and denominators) partly fixed: "Report arms" is now introduced at line 214, but after the figure at line 204, and the figure still has K1, K1.3 and K2.1 rows tagged "(report)" with no caption line. C1's 7.2% against base 5.9% is not annotated. s3_misses.png still plots shares of 1,242 recall questions (C1 searched-not-found is about 53%, which is 661 of 1,242) while the text says "661 of 878 wrong"; no bridge.
F6 (query named as the cause) fixed: lines 223-224 now say "whether the query or the keyword tool is the cause was not separated".
F7 (first sealed test vs S3 label) fixed: line 43 "(the first sealed test and S3)".
F8 (undefined terms) partly fixed: N-hit and copies are now defined in the metrics paragraph (lines 86-89) and OP's "corrections of its own errors" is explained (line 176). No glossary; `hard_dev`, `probe`, `heldout`, `independent`, "taught turns", R2c, Demo2 to Demo5 are still used without a definition in the short paper; clause (b) wording unchanged (lines 156).
F9 (section 1 dense) not fixed: the settings run-on (line 65-66) and the data paragraph (76-84) are unchanged, the provenance note (31-33) is still before section 1, and the new "Use this when" paragraph made section 1 longer.
F10 (garbled LLE sentence, "faster" without a number, "$0") partly fixed: the LLE sentence is repaired (line 266-267) and the cost line reads "at no cost beyond that hardware". "Code ... is faster" (line 123) still has no number; the long paper has them (1.7 to 2.1 s against 1.0 to 1.5 s, ARTICLE.md around line 693).
F11 (figure and table use different seed sets) partly fixed: the figure legend now says "6.37, eight seeds pooled" and the subtitle says sealed pools are generator-built, but the text under the figure does not say the table is seed 82 and the figure is pooled.

## New findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md, whole file: it is 3,957 words, the same as in round 1 (`wc -w`). The author asked for about 5 pages. The opening "Result first" paragraph alone is 449 words and carries about 25 numbers, six of which are repeated in the section 6 table. A ten-minute reader cannot hold it.
    Evidence: `wc -w docs/submission/HF_ARTICLE.md` = 3957; opening paragraph lines 5-20.
    Fix: the cut list below. It takes the paper to about 2,500 words without removing a claim or a disclosure.

F2. [MAJOR] HF_ARTICLE.md:57-60 and the opening: a practitioner still cannot answer "what do I deploy". The box says show the whole chat if it fits, and gives the 6.37 and C1 facts, but never says (a) for a chat that does not fit, code that searches every turn ties 6.37 on LongMemEval-S (40 against 53 of 248, p = 0.12) and is simpler, while naming a listed value on 51.3% of never-told S3 questions against 6.37's 40.4%; (b) whether to use C1 or 6.37 if the faults matter (C1: 0.6% and 7.2%; 6.37: 21.8% and 40.4%). The only reason given for shipping 6.37 is the registered rule.
    Evidence: lines 57-60, 197-199, 219-221.
    Fix: move the box to directly under the opening paragraph and add two lines: "Too long to fit: 6.37 or code, no measured difference on LongMemEval-S; code is simpler, 6.37 is slower at fixing faults. If the two faults matter, C1 measured far lower rates, but it missed one registered clause and 6.37 is the shipped model."

F3. [MINOR] HF_ARTICLE.md:7-8 against 114: the opening gives seed 82 as 52, 52, 46 and 44 of 60 (419-message chats), line 114 says "seed 82's 44 to 55". README.md:144 shows 44 to 55 spans both views (46 to 55 at 58 messages), so 55 is the 58-message view. The same paper gives two ranges for the same four conditions with no bridge.
    Evidence: README.md:144; results/analysis/R-168/refs.json has seed_82 = 55 at one condition.
    Fix: line 114 "44 to 52 on the 419-message chats (the opening's figures)", or say that the range spans both chat lengths.

F4. [MINOR] The "Use this when" box says 6.37 "recalls more than code on generated chats too long to show whole on this card". Those chats are 419 messages that fit the 8,192-token window; "too long" is a 10 GB memory-cap effect (R-166), not a context limit. A practitioner on a larger card shows the chat whole. The only chats that truly do not fit are LongMemEval-S, where there is no difference from code.
    Evidence: lines 6-8, 57-59.
    Fix: write "generated chats that this project's card could not show whole".

F5. [MINOR] Sections 5 and 7 state the same disclosures twice: the demo-rule change (R-276, R-278, R-283) is in the "How C1 became the pick" paragraph (lines 180-188) and again in the first bullet of section 7 (230-231).
    Fix: keep the full account in section 5, and a one-line pointer in section 7.

## Cut list for a ten-minute reader (move to the long paper, all already there per the paper's own routing table)
Words are my estimates from the current text.
- Opening paragraph, 449 to about 200: keep the claim in four sentences (strong on generated chats, weak on outside-writer chats, two faults on S3, C1 missed one clause by 1.3 points, 6.37 stays shipped, C1 published beside it). Cut: the three intervals, the 53 against 40 and p-value, 195 of 894 and 286 of 708 style counts (they are in the section 6 table).
- Lines 31-33 (provenance note, "filled by make_article.py") and the link list, about 100: one sentence in section 8.
- Settings run-on (line 65-66) and "How the Lexsi toolkits connect" (92 words): collapse to one sentence each plus the long paper's section 4. The AuditKIT bootstrap detail goes.
- "Data, splits and leak checks" (159): keep four facts in two sentences: train pools only, four-word overlap check, S3 overlap 140 of 42,561, no embedding or MinHash check and no pretraining-contamination probe. Cut the licence and flow detail.
- Metrics paragraph (86): keep only the two S3 definitions (copy, N-hit false answer); the rest to the long paper.
- Section 3 baselines text (282): keep the table and two sentences. Cut the by-seed "did I tell you" counts, the 480 of 1,242 against 260 of 414 query comparison, and the "..., right?" correction counts (exploratory, small n).
- LongMemEval paragraph (101): keep "53, 34 and 40 of 248; no measured difference from code; declines 233 of 470 answerable". The 11-of-19 split and the judge caveat go.
- Section 5 (about 390 with "How C1 became the pick"): cut to about 150. Keep: candidates were registered before build, 24 listed, the demos were contaminated (keep the demo_contamination figure, it reads at a glance), C1 chosen after the rule changed, one sentence on the 775 against 742 lead being inside seed spread. Drop the bullet detail on K1.3, R2c and OP.
- Section 6: keep the table, the 1.3-point miss with its interval, the ship decision. Cut the seed-by-seed counts, the "Report arms" paragraph (K1 and K2.1 become one sentence in "Not done"), and keep one line for S3's whole-chat 66.2% against 6.37's 27.9% (that is the practitioner's main number).
- Section 7 (339): merge the three "Disclosed" read-by-the-orchestrator bullets into one, shorten "What the S3 measures count" to two sentences. Keep every disclosure, only fewer words.
- Section 8 changelog (72): to the long paper. The "Where each required item is" table (228): keep only if the hackathon form requires the mapping; otherwise cut to five rows.
- Figures: keep recall_out_of_view.png (headline gap), s3_faults.png (the verdict), demo_contamination.png. Move whole_chat_or_search.png (duplicates the table, F3 of round 1) and s3_misses.png (the cause is untested; two text sentences carry it) to the long paper.

Must stay in the short paper: the headline gap between generator chats and outside-writer chats; what was built (one paragraph); the use-when box; the first-sealed-test result and the baselines table; the two faults; S3's design and the ship rule fixed before opening (clauses a to c); the S3 table; the 1.3-point miss and its interval; why 6.37 stays shipped; the rule-change and reading disclosures; limits (Claude judges, no real-person chats, one model and card, contamination not probed); links to both adapters; the author and LLM-usage statement.

## What holds up
The story order (task, build, first sealed test, faults, reopening, S3, limits) is clear, and C1's miss (7.2 against 5.9, 1.3 points) is stated in the opening and the table.
recall_out_of_view.png, s3_faults.png and demo_contamination.png read at a glance, and s3_faults.png's grey band now sits at base's rate with its caption.
I could not break the 661 of 878 (1,242 minus 364 right) arithmetic or the "5 of 894 / 51 of 708" C1 counts against the table.
