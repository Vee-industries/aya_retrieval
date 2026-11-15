# Audit of 9556c2f (R-311 and R-313, diff b08ec7f to 9556c2f)

Date 2026-11-15, 12:22 Eastern. Repo and Hugging Face unchanged by me. Read: `git diff b08ec7f 9556c2f` (11 files), RECORDS.md
R-311 to R-313, `results/panels/R-313/findings.md`, `src/aya_retrieval/heldout3.py` (`false_answer`, lines 536 to 556, plus
the item builder around 425 to 480 and the copy checks near 392). Never-open list kept.

Result: **0 HIGH, 0 MEDIUM, 6 LOW.** No wrong number. Every fix says what its finding asked, at or below its evidence.

## Checks run

1. **Rebuild.** `git archive 9556c2f`, `make_article.py` with the venv python and `HF_HUB_OFFLINE=1`: exit 0. ARTICLE, HF_ARTICLE,
   ABSTRACT, MODEL_CARD, MODEL_CARD_C1 are byte for byte identical to the committed files. `git diff b08ec7f 9556c2f` shows no change to
   ABSTRACT.md, MODEL_CARD_C1.md or the long paper's Abstract section (Kevin's choice holds). MODEL_CARD.md changed in R-311 only
   (template `model_card_template.md`, 4 lines).
2. **R-311 fixes against my audit of b08ec7f.**
   - M1 fixed: MODEL_CARD.md 150 to 153 now reads "above code on recall ... at each of 58 and 419 messages against code's 14 to 32
     ...; it is above the whole chat at 58 messages, the only size the whole chat ran at (table above)". The table row (line 83)
     gives the whole chat 21 to 33 (58 messages only), 6.37 44 to 55 (46 to 55 at 58). Right.
   - L1 fixed: section 9 says "higher on statements and, by one item, in view" and "no measured difference in recall".
   - L2 fixed: HF_ARTICLE 126 to 128 "6.37 and code have the same count (40 against 40; ...); its higher count than code comes only
     from the 15 unanswerable ones. Of all 470 answerable questions, 6.37 declines 233." The 53 against 40 and 233 + 15 = 248 hold (as
     in my last audit); the two 233s are now separated.
   - L3 fixed: the N-hit term now reads "a value listed for the chat: a value of the asked category in that chat, or one of the
     writers' listed wrong values for the question" (ARTICLE 138; HF_ARTICLE 26). Against `false_answer`: the scorer's value set is
     `item.forbidden`, built as `tuple(question["wrong"])` (the question's writers' wrong values), plus `category_values`, "every chat
     value of the asked category", minus the item's answer and a confirm's claimed value, and `None` for a statement. The wording is
     exact. The copy flag names the earlier question's `wrong_value`, which the builder requires to be in that question's `wrong` list
     (line 392), so "Both flags count only values listed for the chat" holds.
   - L4 fixed: "(sections 6.2, 6.3 and this one)". L5 informational; the short paper is 2,961 words now (R-311 says 2,942 at its
     commit, R-313 2,961; the file is 2,961). L6 fixed: "6.37 and C1 three seeds pooled".
3. **R-313 fixes against the reviewer's findings (`results/panels/R-313/findings.md`).**
   - M1: HF_ARTICLE 195 now "On S3 (exploratory, beside the rule, not part of it), ..."; matches the long paper's label. Right.
   - M2: both flag sets named in HF_ARTICLE 26 and 210, ARTICLE 138 and 783; "an invented value on neither list passes unseen"
     is right. The row label (HF 175) was left, with a stated reason (the Terms line defines it); see L2 below.
   - L1: changelogs (ARTICLE 917 to 922, README 587 to 592) name R-311 and R-313; both stage tables read R-313 (ARTICLE 208, HF 96). See L5.
   - L2: "so I do not count the statement line as a gain over code" (ARTICLE one-minute summary item 2): clear, and true by
     construction (code searches every statement).
   - L3: "a third seed would have needed 5 or fewer of 236 to pass (c)". Recomputed earlier: K1.3's two seeds 9 and 28 of 236, base 14 of
     236 is 42.0 of 708, so 5 or fewer puts the pooled rate at or under base's. The other parts of (c) (10 points under 6.37's 40.4%,
     bound above 0) are met by any rate near base's, so "to pass (c)" is not too strong.
   - L4: "no measured difference in recall" in section 9 (ARTICLE 629). L6: "same count" in ARTICLE 451 and HF_ARTICLE 127.
   - L5: Future work now points to Appendix C (ARTICLE 786 to 787) and the "likeliest cause" sentence stays once at line 790. Right.
4. **Numbers in changed sentences.** The changed sentences hold few numbers: "5 or fewer of 236" (above), "58 messages" and
   "419" (R-166, R-168), "40 against 40", "15", "470", "233", "R-309 to R-313". Everything else in the diff is wording or a generated
   key already audited in b08ec7f. Short paper 2,961 words, long paper unchanged in the Abstract.
5. **Voice (kv_voice_v2).** The added lines hold 0 em or en dashes and 0 we/our/us; the only hits from my hedge list are "only" in
   "only at 58 messages", "the only size", "comes only from" (restrictive, not a hedge). Whole files: ARTICLE, HF_ARTICLE, README
   0 dashes and 0 we/our/us (rechecked on the built files).
6. **Conflicts with the rest of either paper or the 6.37 card.** See L1 to L6; nothing contradicts a number.

## LOW

### L1. "Ties code" is still in README and the 6.37 card

R-313 L6 changed "ties" to "have the same count" in both papers. The same phrase stays in `README.md` 373 ("On the 233 answerable
ones it ties code (40 and 40)") and `docs/MODEL_CARD.md` 194 ("on the 233 answerable questions it ties code"; template
`model_card_template.md`), the live 6.37 Hugging Face README. The reviewer's reason (a post-result split reads as shown equal)
applies equally. Fix: "has the same count as code" in both.

### L2. The old "asked category only" wording survives in four places

The N-hit term now names two sets. Still naming one: `docs/submission/HF_ARTICLE.md` 175 (row label "names a listed value of the asked
category"; R-313 left it on purpose; the reviewer asked for it), HF_ARTICLE 188 ("not only listed values of the asked category":
the wider count adds other categories' stored values, and a "listed value" now includes the writers' wrong values), `README.md` 417
("flags see only listed values of the asked category"), and `docs/MODEL_CARD_C1.md` 53 ("counting the asked category only"; line
59 of the same card names both sets). Fix: HF 175 "names a value listed for the chat"; HF 188 "not only values listed for the chat";
README 417 "only values listed for the chat"; C1 card 53 is a measure name, leave or say "counting listed values". The C1 card is
live and Kevin kept the abstract, so say whether it is in scope.

### L3. README still says "no measured change in recall"

R-313 L4 used the defined term "no measured difference" and left the Abstract's "no measured change" (Kevin's choice).
`README.md` 44 ("with no measured change in recall") is not the abstract and holds the same phrase. Fix: "no measured
difference in recall". ARTICLE 38 is the long paper's Abstract and stays.

### L4. S3's "code recalls more" is labelled exploratory in one place only

R-313 M1 labelled `docs/submission/HF_ARTICLE.md` 195. The same claim is unlabelled in the short paper's "Result first" (HF 14 to 15,
"On S3 ... code recalls more"), `README.md` 9 and 84. The long paper labels it where it states the numbers (ARTICLE 649). STANDARD
rule 38 applies to every claim, so an unlabelled repeat is the same finding. Fix: "(exploratory)" after "code recalls more" in each,
two words.

### L5. The changelog phrase is still unclear about who beat whom

`docs/ARTICLE.md` 918 and `README.md` 588: "the whole chat named as beaten only at 58 messages, the one size it ran at". The reviewer's
L1 called the earlier wording unclear; this one leaves it open what beats the whole chat. Fix: "the adapter named as above the whole
chat only at 58 messages, the one size the whole chat ran at".

### L6. The 6.37 card's heading and its "Which to use" paragraph read in opposite directions

`docs/MODEL_CARD.md` 124: "First: when an outside chat fits, give it the whole chat; and plain code shows no measured
difference" (the next paragraph says the adapter and base show no measured difference with the whole chat), against 202: "show base
the whole chat and leave this adapter out". "It" in the heading can read as the adapter. Not in this diff (the heading is
older), but the card is the Hugging Face front page and the conflict is one word. Fix: "give base the whole chat".

## Not checked

The reviewer's report beyond its findings list; the LongMemEval files (never-open); privacy of the diff text (no names in the added
lines that I read); tests (the diff holds no code; unchanged since a39473f where 1,790 passed); the Hugging Face copies (not yet
uploaded, per HANDOFF).
