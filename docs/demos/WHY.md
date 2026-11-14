# Why Demo2 and Demo3 were replaced (R-253, R-254)

## What a demo is for

A demo chat checks one thing: when a fact was told long ago and is out of view, does the model search for it and
answer with it, and when a fact was never told, does it say so. For that to measure retrieval, the answers must be
reachable only through the chat. If the model met an answer as a training answer, it can name it without searching,
and a right answer then says nothing about retrieval.

## What was found

Demo2 and Demo3 were written by fresh writer agents, as were the training chats. Writers of the same kind choose the
same "uncommon" values and the same turns of phrase. Checked against all training data (every training set's rows,
every writer chat, and K1.3's template values), on Saturday 14 November:

| Demo | Keys that are a training fact value | Keys inside a six-word run shared with a training chat |
|---|---|---|
| Demo2 | 6 of 8 (questions 1, 2, 3, 4, 7, 8) | 2 (7, 8) |
| Demo3 | 4 of 8 (questions 2, 3, 7, 8) | 1 (8) |

Two of Demo2's shared runs, quoted because Demo2 has been read many times: "has been blasting khruangbin all week"
and "caved and bought a kayak its". Both sentences, with the answer word, also stand in a training chat. Demo3's text
is not printed.

## What it means for the results so far

Every candidate trained on the writer chats (every one since K3, all but K1.3) had seen some Demo2 and Demo3 answers
as training answers. Their Demo2 and Demo3 scores, T4's and R2c's Demo3 passes among them, may be higher than their
retrieval alone would give. K1.3 trained only on template rows, which also hold some of these values. Screening
(hard_dev, probe, the outside-writer sets, the stresses) is unaffected by this finding; the pick is decided there.

## The fix

Two new demo chats, Demo4 (the screening demo) and Demo5 (held out), written by fresh writers to Demo2's brief, then
checked by `scripts/records/demo_contamination.py` before anyone reads them. A demo fails if any key is a training fact
value, or if any key sits inside a six-word run shared with the training text. On a failure the writer gets the
question numbers and the list of training fact values (`docs/demo4/forbidden_values.txt`), never the test, and
rewrites once; a second failure means a fresh writer. The check was run on Demo2 and Demo3 first, and fails both.
