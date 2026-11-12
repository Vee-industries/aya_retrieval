# Writing brief: test conversations for a chat assistant's memory

You are writing test material. Do not read any file other than this brief and do not search for anything: write
from your own head. The only tool you may use is Write, to save your conversations to the files named at the end.

## What is being tested

A chat assistant sees only the last 3 exchanges of a long conversation (an exchange is one user message and the
assistant's reply). Everything earlier is hidden, but the assistant can search it. A good assistant:
- searches when the user asks about something they said earlier that is no longer visible, and answers with the
  exact detail, about the right person;
- answers from what is visible when the fact is in the last 3 exchanges;
- says plainly it was not told, when the user asks about something they never said;
- just chats, without searching, when the user is chatting.

Your conversations and questions will test this. Make them like real chats, and hard in the ways real chats are hard.

## Each conversation

- A user chatting with an assistant over one long sitting. **20 to 30 exchanges.**
- The user types the way real people type in chat. Vary it between conversations: mostly lower case, short
  messages, some typos, some long rambling messages, some with no punctuation, a few tidy ones. The assistant
  replies naturally in one to three sentences, and does not repeat the user's facts back word for word.
- Facts come up in passing, inside ordinary talk, the way people mention things: not announced, not listed.
- Each conversation involves **at least five people** besides the user.
- **At least a third of the facts are about the user themself** ("i just got the job at the pharmacy"), not only
  about other people.
- Each fact is of one of the categories below. Each conversation has **at least 2 facts from list A and at least 2
  facts from list B**. Use many different categories across your conversations; do not reuse the same few.
- Each conversation must include **look-alike people**: two different people who share a first name (for example a
  coworker and a cousin with the same name), or two near relations (for example a sister and a sister-in-law, an
  uncle and a great-uncle). Both have a fact of the same category with different values.
- Each conversation must include **one correction**: the user states a fact, and later in the conversation says it
  was wrong and gives the right value.
- Facts may appear anywhere: early, in the middle, just before the end. Do not put them in the same places in every
  conversation.
- In at least a third of your conversations, state one of the facts the questions ask about indirectly: with only a
  pronoun for the person ("she just started at the bakery"), or in a roundabout way. The value must still appear in
  one exchange.

## Fact categories

Every fact you record is of one of these categories. Refer to a category by its id.

### List A

- C15: where someone is going on a trip
- C18: someone's favourite food
- C19: food someone is allergic to or cannot eat
- C20: someone's favourite sports team
- C27: when someone's wedding is
- C28: where someone's wedding or party is held
- C31: someone's medical appointment time
- C33: how many siblings someone has
- C36: language someone speaks or is learning
- C37: someone's nationality or heritage
- C38: gym, class, or workout schedule day

### List B

- C01: where someone is moving to
- C02: where someone works (employer)
- C03: what someone's job title or role is
- C04: where someone lives now
- C05: where someone grew up or is from
- C06: someone's birthday date
- C07: someone's age
- C08: name of someone's partner
- C09: name of someone's pet
- C10: kind or breed of someone's pet
- C11: name of someone's child
- C12: how many children someone has
- C13: what someone is studying
- C14: which school someone attends or attended
- C16: when someone's trip or event is
- C17: what car someone drives
- C21: sport or hobby someone does
- C22: instrument someone plays
- C23: someone's favourite band or musician
- C24: show or series someone is watching
- C25: book someone is reading
- C26: someone's favourite restaurant or cafe
- C29: someone's baby due date
- C30: illness or injury someone has
- C32: name of someone's sibling
- C34: name of someone's friend or coworker
- C35: someone's phone or device brand
- C39: someone's daily commute method
- C40: what someone bought recently

Some categories have values that are numbers, dates or times. A fact's value must be a word or a proper name of at
least 4 letters (see the rules below), so record a fact of such a category only when its value can be said that way
(a clinic's name, a weekday spelled out, the name of a month), or use other categories.

## The earlier question, near the end

In each conversation, one of the last 3 exchanges is the user asking about a fact told earlier, before the last 3
exchanges ("wait whats my sisters dog called again"). Write two versions of the assistant's reply to it:

- `right_reply`: gives the right value.
- `wrong_reply`: gives a wrong value instead: another value of the same category from the same conversation (for
  example the look-alike's value, or another person's value of that category). That wrong value must not be the
  answer to any of your nine questions.

Leave the assistant half of that exchange empty (`""`) in `exchanges`; the two replies go in `earlier_question`. The
conversation is tested once with each reply in that place.

## Nine questions for each conversation

After the conversation, write nine questions. Each is a user message that would be sent **right after the last
exchange**, on its own: the nine are alternatives, not a sequence. Write each in the user's own typing style.

1. **older**, a fact from **list B**, told *before* the last 3 exchanges.
2. **older**, a fact from **list A**, told before the last 3 exchanges.
3. **older**, another fact from **list A**, told before the last 3 exchanges.
4. **confirm**: the user checks an earlier fact, told before the last 3 exchanges, in their own words. In five of
   your ten conversations the user names the true value ("it was X wasn't it"); in the other five the user names a
   wrong value, the old value before the correction or another value of the same category from the conversation
   ("she's still going to X right?"), and the right reply gives the true value. The answer is always the true value.
5. **in_view**: a fact told inside the last 3 exchanges, in an exchange other than the earlier question's.
6. **statement**: an ordinary chat message that carries on the conversation and asks nothing about an earlier fact.
   It must not mention any person or fact from before the last 3 exchanges.
7. **never_told**, plain: about something the user never said, of a category that does appear for other people in
   the conversation (for example asking a person's employer when other people's employers came up but this person's
   never did). The person asked about must be one of the conversation's people.
8. **never_told**, sharing a word: like 7, never told, and the message shares a word that carries meaning (a name, a
   noun, a verb; not "the", "my", "what" and the like) with an earlier exchange, before the last 3, that is about
   something else: a fact of a different category. Give that exchange's number as `overlap_exchange` and list its
   fact's value under `wrong`.
9. **re_ask**: the user asks again about the fact the earlier question was about, the one the wrong reply got wrong.

A question must not reuse the words of the sentence that stated the fact, other than the person's name or relation:
ask the way a person asks, not by quoting.

## What to record

The file for each conversation holds:

- `id`: `{writer}_01` to `{writer}_10`.
- `people`: everyone in the conversation besides the user, each written once the same way every time you refer to
  them below, for example `"Farah (my sister)"`. At least five.
- `exchanges`: `[["user message", "assistant reply"], ...]`, counting the first exchange as 0.
- `facts`: every fact any question, the earlier question or a look-alike depends on, and every value of the categories
  your questions ask about. Each fact is:
  - `exchange`: the number of the exchange that states it;
  - `person`: `"me"` for the user, otherwise exactly one entry of `people`;
  - `category`: a category id;
  - `value`: the value, **copied exactly as it appears in that exchange**;
  - `corrects`: `null`, or for the correction, the position (counting from 0) in `facts` of the fact it replaces. The
    replaced fact comes earlier in `facts` and in the conversation, with the same person and category.
- `lookalikes`: the two look-alike people, as written in `people`.
- `earlier_question`: `exchange` (its number, one of the last 3), `category`, `person`, `fact_exchange` (the number of
  the exchange that states the fact), `answer` (the right value), `wrong_value` (the value the wrong reply gives),
  `right_reply` and `wrong_reply`.
- `questions`: the nine questions, each with:
  - `kind`: one of `older`, `confirm`, `in_view`, `statement`, `never_told`, `re_ask`;
  - `message`: exactly what the user types;
  - `category` and `person`: the category id and the person the question asks about (`null` for `statement`);
  - `answer`: the value any correct reply must contain, copied exactly from the conversation. Empty string for
    `never_told` and `statement`;
  - `wrong`: the values a wrong reply might give, each copied exactly from the conversation: the look-alike's value,
    the old value before a correction, other values of the same category. For `never_told`, every value of the asked
    category in `facts`, plus, for question 8, the value of its `overlap_exchange`. For `re_ask`, it includes the
    wrong reply's value. Empty list for `statement`;
  - `fact_exchange`: the number of the exchange that holds the right answer (for a corrected fact, the exchange with
    the correction). `null` for `never_told` and `statement`;
  - `confirm` only: `claim`, `"true"` or `"false"`, and `claimed_value`, the value the user names in the message.
    When the claim is false, leave the claimed value out of `wrong`, because a right reply may mention it while
    correcting it;
  - `never_told` only: `overlap_exchange`, `null` for question 7, the exchange's number for question 8.

## Rules the material must meet

It is checked mechanically. A conversation that breaks a conversation rule is dropped whole; a question that breaks a
question rule is dropped.

- Every fact value, answer and wrong value appears, exactly as written, in the conversation, and is at least 4 letters
  long: one word, or a proper name. Do not use numbers, dates or common words that a reply could say in other ways.
- Values are spelled correctly wherever they appear, even inside a message that has other typos, so that a reply that
  spells them correctly is matched.
- For `older`, `confirm` and `re_ask`, the fact exchange is before the last 3 exchanges, and the answer appears nowhere
  in the last 3 exchanges with the wrong reply in place. For `older` and `confirm`, it also appears nowhere in the last
  3 exchanges with the right reply in place.
- For `in_view`, the fact exchange is one of the last 3.
- The answer is not in the question's own message, except in `confirm`, where naming the value is the point.
- No wrong value contains the answer, and the answer contains no wrong value.
- Every answer is a fact in `facts` with that person, category and exchange, and not one a later correction replaced.
- `never_told` asks about a person and category that no fact in `facts` has together.
- The earlier question's message names neither its answer nor the wrong value; `right_reply` names the answer and not
  the wrong value; `wrong_reply` names the wrong value and not the answer.

## Example

This example shows the format only. It is shorter than most of yours should be, and its setting, people and values are
made up for this page: do not reuse any of them.

```json
{
 "id": "w0_01",
 "people": ["Farah (my sister)", "Farah (my coworker)", "Bogdan (my neighbour)", "Kenji (my cousin)", "Lucia (my manager)"],
 "exchanges": [
  ["ugh train delayed again, stuck on the platform", "Sorry to hear it. How long is the delay?"],
  ["like 40 min. at least i can do my portuguese lessons on the app", "Good use of the wait. How is it going?"],
  ["slowly lol. my sister farah got a rescue dog btw, she named him Pistachio", "That is a great name for a rescue."],
  ["and farah from work ALSO got a dog, his name is Waffles. two farahs two dogs", "Busy month for people named Farah."],
  ["found out last week im allergic to sesame so no more of the bakery bagels for me", "That is a hard one to give up. Have you found anything to replace them?"],
  ["not yet. oh bogdan next door got hired at the brewery on king street", "Nice, he must be pleased."],
  ["he is. my cousin kenji is flying to Lisbon next month", "Exciting. Is it a holiday or for work?"],
  ["holiday i think, he never tells me much", "Some people like to keep plans quiet."],
  ["wait no i got that wrong, kenji said Porto not lisbon", "Thanks for fixing that."],
  ["anyway im starving, i could eat dumplings every day of my life", "Hard to argue with that. Any place near the station?"],
  ["my manager lucia keeps telling me to watch this show Driftwood", "Have you started it?"],
  ["not yet, too busy. oh i didnt tell you, i got the job at the pharmacy!!", "Congratulations, that is big news."],
  ["thanks!! start in two weeks", "Two weeks gives you time to get ready."],
  ["the guy next to me is on a loud phone call", "Long waits bring out the phone calls."],
  ["so true", "Is there a quieter spot on the platform?"],
  ["not really its packed", "Hopefully the train comes soon."],
  ["they just said ten more minutes", "That is close now."],
  ["bogdan texted, his daughter Ilse lost her first tooth lol", "A big day for her."],
  ["wait whats my sisters dog called again", ""],
  ["ok the train is here finally", "Good, enjoy the ride."]
 ],
 "facts": [
  {"exchange": 1, "person": "me", "category": "C36", "value": "portuguese", "corrects": null},
  {"exchange": 2, "person": "Farah (my sister)", "category": "C09", "value": "Pistachio", "corrects": null},
  {"exchange": 3, "person": "Farah (my coworker)", "category": "C09", "value": "Waffles", "corrects": null},
  {"exchange": 4, "person": "me", "category": "C19", "value": "sesame", "corrects": null},
  {"exchange": 5, "person": "Bogdan (my neighbour)", "category": "C02", "value": "brewery", "corrects": null},
  {"exchange": 6, "person": "Kenji (my cousin)", "category": "C15", "value": "Lisbon", "corrects": null},
  {"exchange": 8, "person": "Kenji (my cousin)", "category": "C15", "value": "Porto", "corrects": 5},
  {"exchange": 9, "person": "me", "category": "C18", "value": "dumplings", "corrects": null},
  {"exchange": 10, "person": "Lucia (my manager)", "category": "C24", "value": "Driftwood", "corrects": null},
  {"exchange": 11, "person": "me", "category": "C02", "value": "pharmacy", "corrects": null},
  {"exchange": 17, "person": "Bogdan (my neighbour)", "category": "C11", "value": "Ilse", "corrects": null}
 ],
 "lookalikes": ["Farah (my sister)", "Farah (my coworker)"],
 "earlier_question": {"exchange": 18, "category": "C09", "person": "Farah (my sister)", "fact_exchange": 2, "answer": "Pistachio", "wrong_value": "Waffles", "right_reply": "Your sister's dog is called Pistachio.", "wrong_reply": "Your sister's dog is called Waffles."},
 "questions": [
  {"kind": "older", "category": "C02", "person": "Bogdan (my neighbour)", "message": "where does bogdan work now", "answer": "brewery", "wrong": ["pharmacy"], "fact_exchange": 5},
  {"kind": "older", "category": "C15", "person": "Kenji (my cousin)", "message": "where's my cousin off to next month", "answer": "Porto", "wrong": ["Lisbon"], "fact_exchange": 8},
  {"kind": "older", "category": "C19", "person": "me", "message": "what was the thing i cant eat anymore", "answer": "sesame", "wrong": [], "fact_exchange": 4},
  {"kind": "confirm", "category": "C02", "person": "me", "message": "i got the job at the brewery right?", "answer": "pharmacy", "wrong": [], "fact_exchange": 11, "claim": "false", "claimed_value": "brewery"},
  {"kind": "in_view", "category": "C11", "person": "Bogdan (my neighbour)", "message": "what did bogdan name his kid", "answer": "Ilse", "wrong": [], "fact_exchange": 17},
  {"kind": "statement", "category": null, "person": null, "message": "ok gonna grab a coffee before i get on", "answer": "", "wrong": [], "fact_exchange": null},
  {"kind": "never_told", "category": "C02", "person": "Kenji (my cousin)", "message": "what does kenji do for work", "answer": "", "wrong": ["brewery", "pharmacy"], "fact_exchange": null, "overlap_exchange": null},
  {"kind": "never_told", "category": "C24", "person": "Bogdan (my neighbour)", "message": "what show is bogdan into lately", "answer": "", "wrong": ["Driftwood", "brewery"], "fact_exchange": null, "overlap_exchange": 5},
  {"kind": "re_ask", "category": "C09", "person": "Farah (my sister)", "message": "sorry which name did farah give her dog", "answer": "Pistachio", "wrong": ["Waffles"], "fact_exchange": 2}
 ]
}
```

## Output

Save each conversation to its own file, `{folder}/{id}.json`, where `{id}` is `{writer}_01`, `{writer}_02`, and so on.
Each file holds exactly one JSON object in the format above.

Write **10 conversations.** Their setting: **{setting}**. Use varied names from many cultures. When you are done,
reply with one line: how many files you wrote.

## Filled in per writer

The orchestrator gives each of six fresh writers this brief with `{writer}` (`w1` to `w6`), `{folder}` and `{setting}`
(one of six settings, one per writer) filled in, and cuts this section.
