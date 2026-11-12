# Demo extension protocol (draft for the against lane), 2026-11-12

Kevin: "can we add 8 more questions to the test without fudging shit".

## The problem with fudging
The orchestrator has seen the first demo's result and its cause: 6.37 fails on fact types absent from its training
set and copies training queries. Anyone who knows this and then picks or words the questions can steer the result
either way. So no question may be chosen or worded by the orchestrator.

## Rule that fixes WHICH questions (no choice left)
`demo/chat.txt` has 15 messages. The person states something in messages 1 to 9 and 13. The first demo already
asks about messages 1 (pottery day), 3 (the sink) and 5 (Tobias's city), and asks one never-told question
(the brother). The 8 new questions are:
- one question for each statement not yet asked about, in the order told: message 2 (the teacher is strict about
  centring the clay), 4 (three trips to the hardware store), 6 (Tobias has lived there eleven years), 7 (reading
  old detective novels), 8 (grey weather all week), 9 (making soup tonight), 13 (should call mum this weekend);
- one more never-told question, last.
That is 7 + 1 = 8.

## Who writes the wording
A fresh writer agent that has seen nothing but `demo/chat.txt` and this rule: not the results, not the training
data, not this conversation. It writes each question as the person in the chat would ask a friend later, casual
lower case, and writes the expected answer (the fact as stated) for each, and for the never-told question the
expected answer "never told". It picks the never-told topic itself.

## The new script
`demo/chat_extended.txt` = messages 1 to 14 of `demo/chat.txt` unchanged, then the 8 questions in the order above,
then message 15 ("thanks, that's all for now"). `demo/chat.txt` is not changed. Greedy decoding makes turns 1 to
14 of the extended run identical to the first run; the run checks this and reports any difference.

## Grading, fixed before the run
- The writer's answer key is committed before the run.
- A question about a fact is right if the reply states that fact; a never-told question is right if the reply says
  it was not told and states no other fact as the answer.
- Each question is also labelled before the run as in view or out of view (out of view = the statement is older
  than the last three exchanges when the question is asked), computed by script from the positions.
- Two Sonnet judges grade blind (model names hidden, order shuffled by a committed seed) against the key; the
  orchestrator does not grade. Disagreements are reported, judge 1 decides.

## Registration
Record R-176, committed before the run: this protocol, the writer's questions and key, the in-view labels, the
command lines, and that the whole result is published whatever it shows, with no rerun and no wording change.

## Run
Base and 6.37 seed 82, `scripts/run_chat.py --script demo/chat_extended.txt`, greedy, clean tree, card lock,
HF offline. Outputs `results/demo/fix17cs37_82_extended.json` and `results/demo/base_extended.json`.
