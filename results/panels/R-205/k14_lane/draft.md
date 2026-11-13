# K1.4 draft (for the against lane; not registered)

**Evidence** (R-203, `results/panels/R-203/`; K1.3, outside-writer sets 1 and 2, seeds 82, 83 and 94):
- Older facts: 170 of 480 right; 210 searches did not find the fact; in 152 of the 210 the query held a word found in
  neither the question nor the chat in view (examples: "brother law car auction", "aunt keeps animals yard", "mother
  team bass", "great uncle weekend hobby").
- Confirm questions: 104 of 240 right; 120 had no search. Outside writers' confirm questions state a value and ask
  for a check ("anya's in winnipeg right", "Leyla's still studying medicine, isn't she?", the value right or wrong).
  The model replies with a pleasantry and does not search.

**Cause, in the training rows** (`src/aya_retrieval/conversations.py`):
- `_query` writes every query from `template.query`, made of the statement's own words ("{who} car auction",
  "{who} weekend hobby", "{who} moving city"). In training the search therefore always finds; the model learned to
  write the template's words, which other writers' chats do not contain.
- The confirm form is "did i tell you about my {relation}'s car". No training question states a value and asks to
  check it.

**K1.4 = K1.3 with two changes.**
1. Queries from the question. Every training query becomes the name or relation the message gives (as `_query`
   chooses now) plus the content words of the user's own question (R-176's content-word rule, the name and relation
   removed), in the question's order. No word appears in a query unless it is in that question.
2. Check questions. A share of confirm rows (proposed: half) ask in a check form that states a value: the true value
   (reply confirms with it) or another value of the same type (reply corrects with the stored value). Forms written
   per fact type from the question's category word, in Kevin's style (lower case, no punctuation, "right", "yeah",
   "isn't it"). The never_told side gets the same forms (a value stated for a fact never told: the reply says it was
   not told and does not confirm), so a check form does not mean "found".
3. Search outputs recomputed: each searching row's search is run again with its new query over the row's
   template-wording chat (as K1 decided retrieval), then K1.3's rewording and quotas are applied unchanged. Which
   lines return, and the passage counts, can change; replies follow the new outputs (found or not found).

**Check before training**: R-199's lines, rerun (`check_r199.py` needs a K1.4 base set in place of K1 for line 1);
plus: (a) training queries with a word outside their question: 0; (b) found share of searching rows within 5 points
of K1.3's; (c) never_told rows with passages: all, gap at most 0.37; (d) four-word runs shared with hard_dev forms and
with the check forms: 0; (e) check-form rows: confirmed true value, corrected other value and never_told each about a
third, found and never_told sides alike.

**Open questions for the lane**
- Does a question-word query still find the fact in the training chats often enough? (Compute on K1's set: for each
  searching row, the new query's top 5 over the template chat, found or not.)
- Does it create a new cue between found and never_told (passage counts, query length)?
- Do the check forms put words of the dev sets' questions into training (hard_dev, probe, outside-writer questions)?
- Anything in this that a model could use as a shortcut that would not hold on S3.
