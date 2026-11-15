# Lane 10: Practitioner (critical)
Verdict: submit after fixes. The short paper tells the story in order and is honest, but it never says what to use when, one figure contradicts the table beside it, and one figure is cut off.

## Findings (most severe first)
F1. [MAJOR] HF_ARTICLE.md, "Result first" paragraph and section 3: the opening leads with 91 to 107 of 120 recalled on generated chats, and the reader reaches 6.37's recall on chats written by other people (39 and 53 of 120 in the section 3 table; 347 of 1,242, 27.9%, on S3 in section 6) only after that. The result is the gap between 85 to 90% on the generator's chats and 28 to 44% on outside-writer chats. A practitioner needs that gap in the first paragraph, because it says how far the headline number carries to a different chat distribution. The paper never states that the 85 to 90% figure comes from chats built by the same generator that built the training rows.
    Evidence: HF_ARTICLE.md lines 5-14, 99-101, 174.
    Fix: add one sentence to the opening paragraph: recall is about 90% on generator chats and about 28 to 44% on chats by outside writers.

F2. [MAJOR] No "what to use when" statement. The only guidance is "When the chat fits, show it whole" (line 105). For chats too long to fit, the paper says 6.37 gets 53 of 248 on LongMemEval-S and declines 233 of 470 answerable questions, and "the whole chat on chats too long to fit" is listed as future work. The paper also does not say whether to deploy 6.37 or C1 (C1 is not published; only 6.37 is linked), or why a 40.4% false-answer rate on never-told questions is acceptable to ship.
    Evidence: lines 105-106, 110-113, 215-216, 186.
    Fix: add a short "Use this when" box with three lines: chat fits, show it whole; chat does not fit, 6.37 with the tool, and what it still gets wrong; code that searches every turn, when speed matters and false answers do not.

F3. [MAJOR] whole_chat_or_search.png does not agree with the table next to it. The figure plots `older` questions only (scripts/make_figures.py lines 158-183: `right(..., "older")`), but its axis says "Questions about facts told earlier answered right" and it appears under the table, which uses recall (older plus confirm, of 120). Untrained model on set 1: 14% in the figure, 26 of 120 (22%) in the table and 22% in recall_out_of_view.png. Whole chat, set 1: 72% in the figure, 71 of 120 (59%) in the table. The headline "the whole chat wins" is true in both, but a reader checking numbers sees three conflicting values for the same condition. The subtitle "no measured difference" sits under dots that show 6.37 ahead by 2 to 5 points in whole-chat mode. The figure also omits the code baseline, which is the table's main comparison.
    Evidence: figures/whole_chat_or_search.png; HF_ARTICLE.md lines 99-101; make_figures.py:158-183.
    Fix: plot recall (older plus confirm) so it matches the table, or relabel the axis "older questions only" and add the code arm. Reword the subtitle to "6.37 and base are within error with the whole chat".

F4. [MAJOR] never_told_slide.png: the subtitle is cut off at the right edge ("grey: passes t..."), so the figure's own explanation of the grey band is lost. The y-axis ticks (35, 38, 41, 44, 47) are uneven for a count of 48. OP's 48 of 48 marker is clipped by the top of the plot. The title ("Each repeat ... declined fewer") reads as if K1.3 to OP also fell, but 46 to 48 rose. The text under the figure carries the meaning (OP 48, C1 46, C2 43), so this figure does not read at a glance.
    Evidence: figures/never_told_slide.png; HF_ARTICLE.md lines 153-158.
    Fix: shorten the subtitle, widen the figure, put the y-axis at 40 to 48 in steps of 2, title "Declines fall with each repeat: OP 48, C1 46, C2 43".

F5. [MAJOR] s3_faults.png and s3_misses.png show rows the short paper never introduces: K1 (report), K1.3 (report), K2.1 (report). K2.1 is not mentioned anywhere in the short paper, and "report" is not explained. Also the one thing the figure must show, C1 at 7.2% against a base band of about 2 to 6% (a 1.3-point miss), is hard to see at the printed size. s3_misses.png uses shares of all recall questions (C1 red is about 53%), while the text gives 661 of 878 wrong answers (75%), a different denominator with no bridge.
    Evidence: figures/s3_faults.png, figures/s3_misses.png; HF_ARTICLE.md lines 181, 192-195.
    Fix: drop the report rows from the short paper's copies or add one caption line explaining them. Annotate the C1 point on the right panel "7.2% against 5.9%". Add "of all recall questions" to the s3_misses caption.

F6. [MAJOR] HF_ARTICLE.md:192-193: "the query, the fault left untrained, is now the largest loss." The data show that the search returned text without the fact (661 of 878 wrong answers). It does not show that the model's query was the cause. Retrieval can fail with a good query, because the tool is keyword search over top 5 passages and the fact may be worded differently. The paper presents a cause as established and makes it the next-work item.
    Evidence: HF_ARTICLE.md lines 192-193, 215; s3_misses.png.
    Fix: write "searches that never found the fact are the largest loss; whether the query or the keyword tool is the cause was not tested".

F7. [MINOR] Line 34-35: "Confirmatory claims rest on a sealed test opened once (the first sealed test, S3)." The opening paragraph calls S3 the second sealed test. The parenthesis reads as S3 being the first one.
    Fix: "(the first sealed test and S3)".

F8. [MINOR] Undefined terms for an outside reader: N-hit false answers (used in the rule, the metrics list and the text, never defined; the S3 table row is its only gloss), `hard_dev`, `probe`, `heldout`, `independent`, OP, C1, C2, R2c, K1 to K4.9, Demo2 to Demo5, "taught turns", "decoys" (defined once, in passing). Section 5 reads as a list of codes. Clause (b) "copy at most half as often as 6.37 and 10 points less" is ambiguous.
    Fix: one-line glossary after the claim labels, and one sentence in section 5 saying what OP's "corrections of its own errors" are.

F9. [MINOR] Section 1 is dense. The "Settings" run-on (line 50) and the "Data, splits and leak checks" paragraph (lines 60-68) are walls of identifiers, and leakage counts sit beside licence details. Lines 25-26 (the make_article.py provenance note) and 54-58 (AuditKIT bootstrap detail) interrupt the story.
    Fix: move settings to a small table and the provenance note to section 8.

F10. [MINOR] Lines 225-226: "the plan (R-001) and the my chat engine LLE" is garbled. The claim "faster" (line 105) has no number in the short paper; the long paper's section 10 has them (ARTICLE.md line 693). "Compute cost is $0" ignores electricity; "no cost to me beyond owned hardware" is more exact.
    Fix: repair the sentence, add "1.7 to 2.1 s against 1.0 to 1.5 s" or drop "faster".

F11. [MINOR] recall_out_of_view.png: reads at a glance (large gap on the four sealed rows), but its outside-writer rows show 40% and 43% (eight seeds pooled) while the table shows seed 82 at 39 and 53 of 120 (32% and 44%). The figure is correctly labelled, but the table and figure use different seed sets without saying so in the text.
    Fix: add "(table: seed 82; figure: eight seeds pooled)" under the figure.

## What holds up
The story order (task, build, first sealed test, faults, reopening, S3, limits) is clear, and the ten-minute reader can tell what was built, that C1 failed by 1.3 points (7.2 minus 5.9, S3 table) and that 6.37 stayed shipped. The short paper stands without the long one for claims, with the table at the end routing each item. demo_contamination.png reads at a glance (6, 4, 0, 0 of 8). I did not re-run any number against results files except the figure-to-script check in F3 and the 661 of 878 string in ARTICLE.md.
