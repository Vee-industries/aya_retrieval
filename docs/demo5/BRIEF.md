# Writing brief: one demo chat and twelve questions for a chat assistant's memory

You are writing test material. Do not read any file other than this brief and do not search for anything: write
from your own head. The only tool you may use is Write, to save the two files named at the end.

## What is being tested

A chat assistant sees only the last 3 exchanges of a long conversation (an exchange is one user message and the
assistant's reply). Everything earlier is hidden, but the assistant can search it. A good assistant searches when the
user asks about something said earlier that is no longer visible and answers with the exact detail, answers from
what is visible when the fact is in the last 3 exchanges, and says plainly it was not told when the user asks about
something they never said.

The assistant's replies are not yours to write: you write only the user's messages. The assistant answers each one
live when the demo runs.

## The chat

- **24 user messages**, one per line, in one sitting. The user types the way real people type in chat: mostly lower
  case, short, some typos, no list of facts. Facts come up in passing, inside ordinary talk.
- **At least six people** besides the user, each named at least once.
- **One pair of look-alike people**: two different people who share a first name, or two near relations (a sister
  and a sister-in-law). Both have a fact of the same category, with different values.
- **At least a third of the facts are about the user themself** ("i just started at the pharmacy").
- Use the categories below. Use at least 4 categories from list O (categories the assistant was not trained on).
- Facts go anywhere: early, middle, late. Not in a pattern.

### List I (inside training)
C01 where someone is moving to; C02 where someone works; C03 job title; C04 where someone lives; C05 where someone
grew up; C08 name of someone's partner; C09 name of someone's pet; C10 kind or breed of pet; C11 name of someone's
child; C13 what someone is studying; C14 which school; C17 what car someone drives; C21 sport or hobby; C22
instrument; C23 favourite band or musician; C24 show being watched; C25 book being read; C26 favourite restaurant
or cafe; C30 illness or injury; C32 name of a sibling; C34 name of a friend or coworker; C35 phone or device brand;
C39 daily commute; C40 something bought recently.

### List O (outside training)
C15 where someone is going on a trip; C18 favourite food; C19 food someone cannot eat; C20 favourite sports team;
C28 where a wedding or party is held; C36 language someone speaks or is learning; C37 nationality or heritage; C38
day of a class or workout.

## Twelve questions

Each question is a user message sent **right after message 24**, on its own: the twelve are alternatives, not a
sequence. Write each in the user's typing style, without reusing the words of the sentence that stated the fact
(other than the person's name or relation).

1 to 3. **older**, list I facts told in messages 1 to 21. At least one about the user.
4 to 6. **older**, list O facts told in messages 1 to 21. At least one about the user.
7 to 8. **in_view**, facts told in messages 22 to 24.
9 to 10. **never_told, plain**: a category that comes up for other people, asked about one of the chat's people
   whose value of it was never said. The question shares no word with any message except the person's name or
   relation.
11 to 12. **never_told, sharing a word**: like 9, but the question shares a noun or verb, besides the person's name
   or relation, with one message in 1 to 21 that states a different fact about the same person.

Question 1 or question 4 asks the fact of one person of the look-alike pair.

## Rules

- Every answer value is one word or a proper name of at least 4 letters, spelled correctly, and appears exactly as
  written in its message. No numbers or dates.
- An older question's answer appears nowhere in messages 22 to 24.
- The answer is not in the question's own message.
- A never_told question asks about a person and category that no message states together, and its value is not
  hinted at: a reader of all 24 messages could not name it.
- Each key appears in exactly one of the 24 messages, in no other message, and in no question.
- Pick values that are not the most common choice for their category, and that no other message hints at (no
  heritage that follows from a language, no subject that follows from a job).

## Files

1. `C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/demo5/chat.txt`: the 24 user messages, one per line, nothing else.
2. `C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/demo5/questions.json`: `{"questions": [...]}`, twelve entries in the order above, each with `kind` (`older`,
   `in_view` or `never_told`), `question` (exactly what the user types), `source_message` (the number, 1 to 24, of
   the message that states the fact; `null` for never_told), `key` (the answer copied exactly from that message;
   `"never told"` for never_told), `same_meaning` (other words a right reply might use; for never_told: `["you never
   said", "not mentioned", "you didn't tell me", "no idea"]`), `category` (the category id), `person` (`"me"` or the
   person as named in the chat), for 11 and 12 `overlap_message` (the number of the message it shares a word with),
   and for the look-alike question `other_value` (the other look-alike's value of that category).

Write the two files to those paths, and nothing else.
