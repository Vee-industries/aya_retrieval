# Writing brief: test conversations for a chat assistant's memory

You are writing test material. Do not read any file and do not search for anything: write from your own head. The
only tool you may use is Write, to save your conversations to the files named at the end.

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
- Facts about people come up in passing, inside ordinary talk, the way people mention things: not announced, not
  listed. Each conversation involves at least five people.
- Each conversation must include **look-alike people**: two different people who share a first name (for example a
  coworker and a cousin with the same name), or two near relations (for example a sister and a sister-in-law, an
  uncle and a great-uncle). Both have a fact of the same type with different values (both have a job, both have a
  pet, both moved somewhere).
- Each conversation must include **one correction**: the user states a fact, and later in the conversation says it
  was wrong and gives the right value.
- Facts may appear anywhere: early, in the middle, just before the end. Do not put them in the same places in every
  conversation.
- Spread the facts over at least six different types across your conversations (for example jobs, places, pets,
  foods, hobbies, illnesses, vehicles, schools, and anything else people mention). Do not reuse the same few types
  in every conversation.
- In at least a third of your conversations, state one of the facts the questions ask about indirectly: with only a
  pronoun for the person ("she just started at the bakery"), or in a roundabout way. The answer word must still
  appear in one exchange.

## Six questions for each conversation

After the conversation, write six questions. Each is a user message that would be sent **right after the last
exchange**, on its own: the six are alternatives, not a sequence. Write each in the user's own typing style.

1. **older**, about a look-alike: a fact told *before* the last 3 exchanges, about one of the look-alike people, so a
   careless answer would give the other person's value. Name the person by their relation or role (my cousin, my
   coworker), not by a shared first name alone, so the question has one right answer.
2. **older**, any other fact told before the last 3 exchanges.
3. **confirm**: the user checks an earlier fact, told before the last 3 exchanges, in their own words. In about half
   of your conversations the user names the true value ("it was X wasn't it"); in the other half the user names a
   wrong value, the old value before the correction or the look-alike's value ("she's still in X right?"), and the
   right reply gives the true value. The answer is always the true value. When the user names a wrong value, leave
   that value out of `wrong`, because a right reply may mention it while correcting it.
4. **in_view**: a fact told inside the last 3 exchanges.
5. **never_told**: about something the user never said, of a type that does appear for other people in the
   conversation (for example asking a person's job when other people's jobs came up but this person's never did).
   The person asked about must appear in the conversation.
6. **statement**: an ordinary chat message that carries on the conversation and asks nothing about an earlier fact.
   It must not mention any person or fact from before the last 3 exchanges.

In each conversation, one of questions 1 to 3 must be about the corrected fact.

A question must not reuse the words of the sentence that stated the fact, other than the person's name or relation:
ask the way a person asks, not by quoting.

For each question give:
- `kind`: one of `older`, `confirm`, `in_view`, `never_told`, `statement`.
- `message`: exactly what the user types.
- `answer`: the word any correct reply must contain, **copied exactly as it appears in the conversation**: one word,
  or a proper name, at least 4 letters long. Do not use numbers, dates or common words that a reply could say in
  other ways. Empty string for `never_told` and `statement`.
- `wrong`: the values a wrong reply might give, each **copied exactly from the conversation**: the look-alike's value,
  the old value before a correction, other values of the same type. For `never_told`, every value of the asked type
  that appears in the conversation. Empty list for `statement`.
- `fact_exchange`: the number of the exchange that holds the right answer, counting the first exchange as 0 (for a
  corrected fact, the exchange with the correction). `null` for `never_told` and `statement`.

Rules the material must meet (it is checked mechanically, and items that break a rule are dropped):
- For `older` and `confirm`, the answer must not appear anywhere in the last 3 exchanges, and the fact exchange must
  be before them.
- For `in_view`, the fact exchange must be one of the last 3.
- The answer must not appear in the question's own message, except in `confirm`, where naming the value is the point.
- No wrong value may contain the answer, and the answer may not contain a wrong value.
- Every answer and wrong value must appear, exactly as written, in the conversation, and be at least 4 letters long.
- Answer words and wrong values must be spelled correctly wherever they appear, even inside a message that has
  other typos, so that a reply that spells them correctly is matched.

## Output

Save each conversation to its own file, `{folder}/{id}.json`, where `{id}` is `{writer}_01`, `{writer}_02`, and so on.
Each file holds exactly one JSON object:

```
{"id": "...", "exchanges": [["user message", "assistant reply"], ...], "questions": [{"kind": "...", "message": "...", "answer": "...", "wrong": ["..."], "fact_exchange": 0}, ...]}
```

Write **{count} conversations.** Their setting: **{setting}**. Use varied names from many cultures. When you are done,
reply with one line: how many files you wrote.

## The four settings (R-151)

The second independent set used R-142's writer spec unchanged (the text above). Each of four fresh Opus writers got it
with {folder}, {writer} (x1 to x4), {count} (10) and {setting} filled in, and "Do not read any file" changed to "Do not
read any file other than this brief":

- x1: a parent talking with the assistant about their children, the school, teachers, coaches and other parents
- x2: a user planning a big family event, talking about guests, relatives, friends and the people they hire
- x3: a user in a shared house in a busy neighbourhood, talking about housemates, the landlord, neighbours and local
  shops
- x4: a member of a community group (a choir, a club, a volunteer crew), talking about the people in it
