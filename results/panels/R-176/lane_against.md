Verdict: approve with fixes. The fixes for blindness, the new-question layout and the grading rule must go in before the writer runs.

**1. Ways the protocol can still be steered, and the fix for each**
- **Writer blindness leaks.** A fork, or any agent with file tools, gets the global CLAUDE.md and MEMORY.md. Those name 6.37, the Lexsi repo and "read the SOP first", which leads to project files. Fix: start a fresh agent, not a fork. Paste the script into the brief, allow no tools, and scan its transcript for any tool call before using its output.
- **The writer can be re-run until the result looks good.** Fix: one writer run. Keep its output word for word and commit the brief and the transcript. Any check that fails gets one logged repair pass, quoting only the failed check.
- **The wording sets how easy a question is to find** (shared words with the statement). Fix: the writer stays free, but a script computes the shared content words per question before the run. That number is registered and printed beside every result.
- **The answer can leak into the question,** through yes/no or "was it three?" forms. Fix: open questions only, with no word of the key inside the question.
- **Some messages hold more than one fact** (msg 4: three trips, hardware store; msg 6: eleven years, big change). Asked facts left out: Marisol's name, "next month", "kitchen". Fix: the writer names one fact per message in the key. The report says the 8 do not cover every fact.
- **The never-told question varies in difficulty.** "did i ever tell you..." invites a "no". A question that assumes the fact ("what's my dad's job again") does not. Fix: copy message 12's form. The topic must name no person, place or thing that appears in the chat.
- **Some answers are guessable** ("who should i call" → mum; weather → grey). This also covers Kevin's strongest-baseline-first rule. Fix: add two runs, base and 6.37, with search turned off (empty index), and report each model's guess rate first.
- **Judges:** "judge 1 decides" is an arbitrary tie-break, and the orchestrator writes the judge prompt. Fix:
  - Commit the judge prompt and the pinned model in R-176.
  - Each judge sees only the question, the key and one reply. Replies are graded one at a time, shuffled across models.
  - A disagreement counts as not right, and both grades are shown.
  - Scan the judges' transcripts too.
  - Add a measure the judges cannot touch: a script checks whether the search output contained the source message (found / not found).
- **The run:**
  - The index path must not exist before each arm; assert it. A file left by a crash would carry old passages into the run.
  - Record the commit, the adapter hash and the exact command.
  - A run that crashes before finishing may be restarted from scratch. A run that finishes is final.
  - If the GPU makes turns 1-14 differ from the first run, the run still counts. The difference is reported.
- **Reporting:**
  - Headline = per model, right of 7 facts and right of 1 never-told, for the 8 new questions only. They are the only blind items.
  - The first demo's 4 are reported apart, because the author had seen them.
  - Show every reply, every search query and found / not found.
  - Counts only; no significance claim at this size.
  - Any cause given (such as "fact type not in training") is labelled as an explanation written after the run.

**2. Is a writer that saw only the script blind enough?**
Only with the fixes above (no tools, transcript checked, one attempt).
- **The brief must contain:** the script, the target message numbers in order, the style, the format rules and the never-told rule.
- **The brief must not contain:** search, memory, retrieval, model, adapter, training, view, three exchanges, demo, results, hackathon, any word about easy or hard, or any advice to paraphrase or avoid the script's words.

Draft brief (about 180 words):

"Use no tools and read nothing; all you need is here. [Messages 1-15 of the script, numbered.] Later the person asks a friend about things they said. Write one question for each of these messages, in this order: 2, 4, 6, 7, 8, 9, 13. Each question asks for one fact stated in that message, the way this person would ask a friend: casual, lower case, like messages 10, 11 and 14. Rules: no yes/no questions; no word of the answer in the question; the fact must come from that message. Then write one question in the same form as message 12 about something the person never mentioned; its topic must not be any person, place or thing named in the chat. For each question give: the message number, the question, the key (the shortest phrase from the message that answers it), and other words that mean the same. The last key is 'never told'. Output a table only. One attempt; no notes."

**3. Is the grading rule complete?**
No. It leaves out partial answers, extra facts, hedges, questions back, cut-off replies and "I don't know". Register this rule:
- **Fact question, right:** the reply contains the key, or a listed equal, and offers no second, conflicting answer.
- **Fact question, wrong:**
  - A partial answer that misses the key (for example "the teacher is strict" when the key is "centring the clay").
  - The right fact plus a wrong candidate ("Halifax or Toronto").
  - A question back with no answer.
  - "I don't know". This is labelled "abstained", apart from "wrong fact", but scores as not right.
- **Fact question, extra facts and hedges:**
  - A hedge ("i think it was three") is right.
  - A made-up extra detail that does not conflict with the chat leaves the reply right, but it is flagged "invented" and counted.
- **Never-told question:** right only if the reply says it was not told or does not know, and states no value. A bare question back counts as not right.
- **Cut-off replies:** replies stop at 60 tokens and are graded as cut.

**4. What appending after message 14 changes**
- **Every fact is out of view.** All 7 facts are asked at positions 15-21. The nearest one, msg 13, is 8 exchanges back, so every in-view label is "out of view" and there is no in-view control.
- **The index fills with test answers.** It now holds the model's own earlier answers (exchanges 10-14 and each new Q&A). For example, a search for "Tobias" can return exchange 11 instead of exchange 6, and a wrong earlier answer can be found and repeated.
- **The view holds only questions and answers.** That primes searching, and one wrong answer stays in view for the next three questions.
- **The never-told question comes last,** after 7 quiz turns.

This differs from the first demo and from a normal chat. Fix: run each new question as its own branch (messages 1-14 plus that one question), 8 branches per model. Then every question has the same history. Msg 13 becomes one real in-view item, and the labels mean something. If the appended design is kept, register it and report these effects.

**5. Verdict**
Approve with the fixes above.
