# Writing brief: eight practice chats for a chat assistant's memory

You are writing training material. Do not read any file other than this brief and do not search for anything: write
from your own head. The only tool you may use is Write, to save the one file named at the end.

## What the assistant does

A chat assistant sees only the last 3 exchanges of a long conversation (an exchange is one user message and the
assistant's reply). Everything earlier is hidden, but it can search it with a keyword search, which returns the
earlier exchanges that share words with the search. A good assistant searches when the user asks about something
said earlier that is no longer visible, and answers with the exact detail; answers from what is visible when the
fact is in the last 3 exchanges; and says plainly it was not told when the user asks about something they never
said.

## Each chat

- **24 user messages**, in one sitting, each with a short assistant reply (one sentence, friendly, rarely a question
  back, and never repeating the fact's detail word for word). The user types the way real people type in chat:
  mostly lower case, short, some typos, no list of facts. Facts come up in passing, inside ordinary talk, worded any
  way a person would say them.
- **At least five people** besides the user. About half the fact messages name the person only by name or only by
  relation ("my glazier", "dara"), not both. Some categories get two kinds of detail about one person (a dog's name
  in one message, its breed in another).
- **One pair of look-alike people**: two people who share a first name, or two near relations (a sister and a
  sister-in-law), each with a fact of the same category, different values.
- **At least a third of the facts are about the user themself** ("finally got the job at the vet clinic").
- About 12 facts per chat, from the categories below only. Every chat uses at least 8 different categories, and
  across your eight chats use every category at least twice.
- Messages that state no fact are ordinary chat (plans, moods, small news) and make up about half the chat.
- Every fact's value is one word or a proper name of at least 4 letters, spelled correctly, appearing exactly as
  written in its message, in no other message. No numbers or dates. Pick values that are not the most common choice
  for their category, and invent your own names and places rather than the first ones that come to mind.
- At least one of messages 22 to 24 states a fact.

### Categories
C01 where someone is moving to; C02 where someone works; C03 job title; C04 where someone lives; C05 where someone
grew up; C08 name of someone's partner; C09 name of someone's pet; C10 kind or breed of pet; C11 name of someone's
child; C13 what someone is studying; C14 which school; C17 what car someone drives; C21 sport or hobby; C22
instrument; C23 favourite band or musician; C24 show being watched; C25 book being read; C26 favourite restaurant
or cafe; C30 illness or injury; C32 name of a sibling; C34 name of a friend or coworker; C35 phone or device brand;
C39 daily commute; C40 something bought recently.

## Eleven questions per chat

Each question is a user message sent right after message 24, on its own: the eleven are alternatives, not a
sequence. Write each in the user's typing style. Vary the wording: do not reuse the words of the sentence that
stated the fact, other than the person's name or relation, and do not start two questions in a chat the same way.

1 to 4. **older**: a fact told in messages 1 to 21. At least two about the user.
5 to 6. **check_true**: states the right value of a fact told in messages 1 to 21 and asks to check it, the way people
   do ("so the quads are in thornbury now yeah", "my car's still that old tercel right").
7 to 8. **check_false**: states a wrong value, of the same category, for a fact told in messages 1 to 21. When another
   person in the chat has a value of that category (the look-alike pair), use that other person's value as the
   wrong one at least once.
9 to 10. **never_told**: a category that comes up for other people, asked about one of the chat's people (or the
   user) whose value of it was never said. A reader of all 24 messages could not name it. One of the two is a check
   form that states a value.
11. **in_view**: a fact told in messages 22 to 24.

For every question except in_view, write two searches:
- `query`: the keywords a good assistant would type first, using only words that appear in the question itself
  (names and relations as the question writes them), 1 to 4 words, never a filler word (say, tell, told, mention,
  remember, again, know, think, what, where, which, who, does, did, is).
- `second_query`: what it would try next if the first found nothing: 1 to 3 other words a person would likely use
  when telling that kind of fact ("job work employer", "dog pet breed"), never the value itself.

For older, check_true, check_false and in_view, write `reply`: what a good assistant says, one short sentence that
states the stored value (for check_false, says it is not that and gives the stored value). For never_told, no reply.

## File

Write `C:/Users/Gaming/scratch/claude/C--Users-Gaming--claude-spares-spare-wcSF8M/3f7d989b-d009-44ac-9f86-64e88058f022/scratchpad/k3_writers/WRITER.json`:

```
{"chats": [
  {"messages": [{"user": "...", "assistant": "...", "fact": {"category": "C02", "person": "me", "value": "..."}},
                {"user": "...", "assistant": "...", "fact": null}, ... 24 of them],
   "questions": [{"kind": "older", "question": "...", "source_message": 7, "value": "...", "category": "C02",
                  "person": "me", "query": "...", "second_query": "...", "reply": "..."}, ... 11 of them]},
  ... 8 chats
]}
```

`fact` is null for a message that states no fact. `source_message` is the number (1 to 24) of the message that
states the fact, `null` for never_told; `value` is the answer copied exactly from that message (for never_told,
`null`; for check forms, the stored value, not the one the question states); `person` is `"me"` or the person as
named in the chat.

Write that one file and nothing else.
