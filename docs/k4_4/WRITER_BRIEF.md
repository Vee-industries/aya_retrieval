# Writing brief: wrong-person questions for existing practice chats

You are writing training material for a chat assistant's memory. Read only the files this brief names and do not
search for anything else. The only tool you may use besides Read is Write, to save the one file named at the end.

## What the assistant does

A chat assistant sees only the last 3 exchanges of a long conversation. Everything earlier is hidden, but it can
search it with a keyword search, which returns the earlier exchanges that share words with the search. A good
assistant answers with the exact stored detail when it was told, and says plainly it was not told when it was not,
even when the search brings back the same kind of fact about a different person.

## Your input

Read these files (each holds 8 chats; a chat has 24 messages, each with `user`, `assistant` and `fact`, which is
null or `{"category", "person", "value"}`):

INPUT_FILES

## What to write

For **every chat** in your files, three new questions, each a user message sent right after message 24, in the
user's typing style (mostly lower case, short, some typos). Use only facts stated in messages 1 to 21.

1 and 2. **other_person**: pick a fact of some category X stated in messages 1 to 21 for one person Q (or for the
   user, "me"). Ask about the same category X for a different person P: someone else named or mentioned in the chat,
   or the user, for whom the chat never states a category X fact. A reader of all 24 messages could not name the
   answer for P. Name P in the question the way the chat does (by name or by relation, as the chat writes it). X
   must be a category that has a fact annotation in the chat. Use a different X, or a different P, for the two.
3. **contrast**: for the same Q and X as question 1, ask for Q's stored X fact itself, in words close to question
   1's.

Do not reuse the wording of the message that states the fact, other than the name or relation, and do not start two
of your questions in a chat the same way.

For each question write:
- `query`: the keywords a good assistant would type first, using only words that appear in the question itself
  (names and relations as the question writes them), 1 to 4 words, never a filler word (say, tell, told, mention,
  remember, again, know, think, what, where, which, who, does, did, is).
- `second_query`: 1 to 3 other words a person would likely use when telling that kind of fact, never a value.
- `stored_person`: Q, as the fact annotation names them.
- For contrast only: `source_message` (1 to 21), `value` (copied exactly from that message) and `reply` (one short
  sentence that states the value).

## File

Write `OUTPUT_FILE`:

```
{"questions": [
  {"file": "w1.json", "chat": 0, "kind": "other_person", "question": "...", "person": "...",
   "stored_person": "...", "category": "C13", "query": "...", "second_query": "..."},
  {"file": "w1.json", "chat": 0, "kind": "contrast", "question": "...", "person": "...", "category": "C13",
   "source_message": 9, "value": "...", "query": "...", "second_query": "...", "reply": "..."},
  ...
]}
```

`chat` is the chat's position in its file, counting from 0. For contrast, `person` is Q. Write that one file and
nothing else.
