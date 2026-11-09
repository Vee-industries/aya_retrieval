# Sample data: Tiny Aya recall LoRA (Track 3)

> Made on 2026-11-07 for Lexsi's feedback. "The adapter" here is v6, the adapter shipped that day, and
> its training set; 6.37 (`fix17cs37` seed 82) replaced v6 on 2026-11-08 (RECORDS R-131).

Every name and fact below is synthetic, generated from a fixed pool of people, relations and facts.
The model sees only the last few exchanges of a long chat. Older facts must be found with a
`search_corpus` tool over the earlier chat. The adapter teaches when to search, when not to, and
how to answer from what comes back.

## Part 1: training rows (one of each kind, from the adapter's training set)

### Fact said long ago, now out of view: search, then answer (`older_0000`)

```
USER: i'm actually pretty happy with the laundry lately
ASSISTANT: Good to hear the laundry is behaving.
USER: ugh, my knee is driving me up the wall
ASSISTANT: Sorry, my knee sounds like a real hassle.
USER: the fridge let me down this morning
ASSISTANT: That's frustrating. Is the fridge usually like that?
USER: the creatures in my neighbour's yard escape me
ASSISTANT: [{"tool_name": "search_corpus", "parameters": {"query": "neighbour keeps animals yard"}}]
USER: Tool result for search_corpus: [chunk_id=exchange_0023::0 doc_id=exchange_0023 score=6.708]
User: so Omar (my neighbour) keeps tortoises in the yard
Assistant: Thanks for telling me.

[chunk_id=exchange_0014::0 doc_id=exchange_0014 score=3.633]
User: so Yusuf (my brother) keeps rabbits in the yard
Assistant: How are they finding it?

[chunk_id=exchange_0002::0 doc_id=exchange_0002 score=3.557]
User: so Marc (my sister) keeps chickens in the yard
Assistant: Oh, that's nice to hear.

[chunk_id=exchange_0024::0 doc_id=exchange_0024 score=1.629]
User: funny how the mail keeps coming up
Assistant: It does seem to come up a lot.
Use this result to answer the original question.
ASSISTANT: It sounds like your neighbour, Omar, keeps tortoises in the yard.
```

### Asking whether something was said: search, then confirm (`confirm_0000`)

```
USER: my coffee let me down this morning
ASSISTANT: I'd be fed up with my coffee too.
USER: no complaints about the elevator this week
ASSISTANT: Good to hear the elevator is behaving.
USER: my phone is getting on my nerves
ASSISTANT: I'd be fed up with my phone too.
USER: have i said anything about my cousin's baby
ASSISTANT: [{"tool_name": "search_corpus", "parameters": {"query": "cousin baby name"}}]
USER: Tool result for search_corpus: [chunk_id=exchange_0025::0 doc_id=exchange_0025 score=4.851]
User: my cousin, Dana, had a baby and named them Hugo
Assistant: That sounds exciting for them.

[chunk_id=exchange_0013::0 doc_id=exchange_0013 score=1.950]
User: my roommate, Greta, had a baby and named them Nora
Assistant: That sounds exciting for them.

[chunk_id=exchange_0000::0 doc_id=exchange_0000 score=1.910]
User: my coworker, Yusuf, had a baby and named them Mila
Assistant: Oh, that's nice to hear.
Use this result to answer the original question.
ASSISTANT: Your cousin Dana named the baby Hugo.
```

### Never said: search, find nothing, say so (`never_told_0000`)

```
USER: so my back has been a pain all week
ASSISTANT: Oof. An hour lost to my back is no fun.
USER: i'm actually pretty happy with my laptop lately
ASSISTANT: Love that for you.
USER: anyway, enough about my bike
ASSISTANT: It does seem to come up a lot.
USER: the floor my cousin rents on escapes me
ASSISTANT: [{"tool_name": "search_corpus", "parameters": {"query": "cousin floor flat rent"}}]
USER: Tool result for search_corpus: [chunk_id=exchange_0006::0 doc_id=exchange_0006 score=4.569]
User: Greta is my sister, and they rent on the third floor
Assistant: That's a change.

[chunk_id=exchange_0024::0 doc_id=exchange_0024 score=4.472]
User: Marc is my neighbour, and they rent on the ninth floor
Assistant: That sounds exciting for them.
Use this result to answer the original question.
ASSISTANT: Nothing on that here. Did you mean someone else?
```

### Fact still in the visible chat: answer without searching (`in_view_0000`)

```
USER: apparently my aunt Marc finished a 5k on sunday
ASSISTANT: Good to know.
USER: good news, my bike sorted itself out
ASSISTANT: Glad my bike worked out.
USER: no complaints about the mail this week
ASSISTANT: That's a small win. the mail sounds good.
USER: my aunt ran something on sunday and i've lost which
ASSISTANT: It sounds like you're trying to remember what your aunt ran. Was it a 5k? A marathon? Or something else?
```

### Plain chat, no question: just reply (`statement_0000`)

```
USER: so that show has been a pain all week
ASSISTANT: I'd be fed up with that show too.
USER: i lost an hour to my phone today
ASSISTANT: I'd be fed up with my phone too.
USER: i was thinking about the bakery on the way home
ASSISTANT: Fair enough, one thing at a time.
USER: Lena cancelled our plans at the last minute
ASSISTANT: That sounds frustrating. Maybe you can reschedule or just enjoy the day with friends instead.
```

## Part 2: evaluation items, base model against the adapter (development pool)

Same conversation, same last message. `correct` is the automatic scorer's mark.

### `58_older_00` (older)

- **Friend's message:** drawing a blank on my daughter's tattoo
- **Right answer:** koi
- **Base:** searched ["daughter's tattoo"]; reply: "Ayaan, your godfather got a thistle tattoo last week."; correct: False
- **Adapter:** searched ['daughter tattoo']; reply: "Your daughter Gustav got a koi tattoo."; correct: True

### `58_confirm_00` (confirm)

- **Friend's message:** did i say anything about my godfather's tattoo
- **Right answer:** lighthouse
- **Base:** searched no; reply: "No, you didn't."; correct: False
- **Adapter:** searched ['godfather tattoo']; reply: "Your godfather Hana got a lighthouse tattoo."; correct: True

### `58_never_told_01` (never_told)

- **Friend's message:** it's on the tip of my tongue which club my mentor joined
- **Right answer:** (never said: the reply should say it does not know)
- **Base:** searched ['which club did my mentor join']; reply: "Dmitri, your mentor joined an archery club this month."; correct: False
- **Adapter:** searched ['mentor club joined']; reply: "I don't have that from you. What is it?"; correct: True

### `58_in_view_06` (in_view)

- **Friend's message:** it's on the tip of my tongue which club my godfather joined
- **Right answer:** water polo
- **Base:** searched ["Esme's godfather water polo club", "Farah's tutor handball club", "Farah's tutor handball club", "Farah's tutor handball club"]; reply: "Tool result: [{"tool_name": "search_corpus", "parameters": {"query": "Farah's tutor handball club"}}]"; correct: False
- **Adapter:** searched no; reply: "That's a fun way to remember the water polo club your godfather joined.  Chimney is a great way to recall information.  Do you have any other fun facts or memories about Esme or the water polo club?"; correct: True

### `58_statement_02` (statement)

- **Friend's message:** Dmitri forgot my birthday again
- **Right answer:** (no question: the reply should just chat, no search)
- **Base:** searched ['how to deal with a forgetful friend']; reply: "That's lovely to hear."; correct: False
- **Adapter:** searched no; reply: "That sounds like a bit of a bummer."; correct: True

### `58_in_view_04` (in_view)

- **Friend's message:** drawing a blank on my classmate's tattoo
- **Right answer:** swallow
- **Base:** searched no; reply: "That's a clever way to respond. Drawing a blank on someone's tattoo is a playful way to acknowledge the change."; correct: False
- **Adapter:** searched no; reply: "That's a bit of a problem. If you don't know the details of Esme's tattoo, it's hard to draw a blank. Can you tell me more about it?"; correct: False
