# Writing brief: first searches that miss, for existing practice chats

You are writing training material for a chat assistant's memory. Read only the files this brief names and do not
search for anything else. The only tool you may use besides Read is Write, to save the one file named at the end.

## What the assistant does

A chat assistant sees only the last 3 exchanges of a long conversation. Everything earlier is hidden, but it can
search it with a keyword search, which returns up to 5 earlier exchanges that share words with the search. Its
first search often brings back other messages and not the one it needs; a good assistant then searches again with
different words instead of giving up.

## Your input

Read these files (each holds 8 chats; a chat has 24 messages and a list of `questions`):

INPUT_FILES

## What to write

For **every question** whose `kind` is `older` or `check_true`, write one `miss_query`: a first search a person might
type for that question that would bring back some earlier messages but **not** the message the question is about
(the message numbered `source_message`). Use 1 to 4 words, every one taken from the question itself (names and
relations as the question writes them), never a filler word (say, tell, told, mention, remember, again, know, think,
what, where, which, who, does, did, is), never the question's own `query` unchanged, and never a word of the
`value`. Read the chat's messages 1 to 21 to pick words that appear in other messages but not in the source message.
If no such words exist in the question, skip that question.

## File

Write `OUTPUT_FILE`:

```
{"miss_queries": [
  {"file": "w9.json", "chat": 0, "question": 0, "miss_query": "..."},
  ...
]}
```

`chat` is the chat's position in its file and `question` the question's position in that chat's `questions`, both
counting from 0. Write that one file and nothing else.
