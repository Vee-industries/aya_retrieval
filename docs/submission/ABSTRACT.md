# Teaching a 3B model to search a long chat it can no longer see

Tiny Aya Global (3.35B) answers only from what it can read. I trained a LoRA adapter, 6.37, with Lexsi Labs'
AgentTune to search the earlier conversation when an answer is out of view, read what the search returns, and
answer in the model's own voice. The harness shows the last three exchanges; everything older is reachable
only through a full-text search tool. The 1,094 training rows come from a generated pool, with targets taken
from the untrained model's own replies where they pass the scorer. AuditKIT checks the scorer and CuratorKIT the
training answers. Every decision, run and result is in a dated log; each test was registered before it ran.

On the registered sealed test (300 unseen generated chats in each of four conditions, run once), recall rises
from 8 to 28% for the untrained model to 85 to 90% pooled over eight training seeds. Every right answer came from
a search that found the fact, no adapter made more false retrievals than the untrained model, and three judges
rated every adapter coherent more often than the untrained model. The shipped seed answers 91 to 107 of 120
recall questions against 13 to 32. Per 60 recall questions at one chat length, the untrained model reading the whole
chat answers 21 to 33, and code that searches on every turn 14 to 32, against the shipped seed's 44 to 55.

On two sets of chats by Claude Opus writers who never saw the generator (averaging 1,400 tokens), the
untrained model given the whole chat answers 58 and 52 of 80 earlier-fact questions, against
28 and 34 for 6.37 with the tool; given the whole chat, 6.37 and the untrained model show no measured difference.
Code that searches on every turn recalls as well as 6.37 (42 and 47 of 120 against 39 and 53; p = 0.76 and
0.45), against the untrained model's 26 and 27. What training adds there is deciding when not to search: answers
in view, 35 and 37 of 40 against code's 13 and 16; facts never told, 37 and 36 against 31 and 24; plain
statements answered without a search, 37 and 35 against 0.

On LongMemEval-S (500 questions, each over a user-to-assistant history, median 244 exchanges), judged
with LongMemEval's prompts by Claude judges rather than the official GPT-4o judge, 6.37 is right on 53 of 248
judged questions, the untrained model with the tool on 34 (p = 0.014), and code that searches every question on
40 (p = 0.12). On the 233 answerable questions 6.37 and code tie at 40. 6.37 declines 13 of the 15 unanswerable
questions, where code declines none, and declines 233 of all 470 answerable questions. Code is
faster than 6.37 on every set.

Short outside-writer chats shown whole need no tool. For longer chats the adapter matches code that searches
every turn (outside-writer recall, LongMemEval judged answers), adds the decision not to search, and recalls more
than either reference on the generated pools.
