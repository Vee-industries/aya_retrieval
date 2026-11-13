# Demo2 brief, against lane (claude-opus-5-5; read the brief, the named RECORDS entries, both judge briefs, run_demo_branches.py and demo_judges_r176.py; edited nothing, ran nothing)

1. Never-told 9-10 and 11-12 are not different as written: both name a chat person, and a name is a meaning-carrying
   word. Fix: 9-10 share no word with any message except the person's name or relation; 11-12 share a noun or verb,
   besides the name, with one message in 1 to 21 that states a different fact about the same person. That is the
   K1/K2 same_person case (R-185) and the disclosure must say so.
2. The look-alike pair is never asked about. Fix: question 1 or 4 asks the fact of one look-alike; add `other_value`.
3. Keys that appear twice break `found_source`. Fix: each key appears in exactly one message and in no question.
4. Guessable values (labrador, pizza, iphone, spanish). Fix: not the most common choice for the category, not hinted
   at by another message; a never_told value is neither stated nor hinted at.
5. The model's replies to messages 22-24 can contain an older key. The runner should flag `key_in_view_reply` per arm
   and the report should print the replies to 22-24 beside each arm.
6. 4 of 12 are never_told; a model that declines everything scores 4. Report per kind, never one total, with the
   decline-everything baseline (0 of 8 facts, 4 of 4 never_told).
7. Zero word overlap tests query writing, which no model was trained on. Count shared words by script before the
   run, as R-176 did, and publish the counts.
8. The S3 judge brief has a gap: a never_told reply that neither declines nor names a value for the asked fact (an
   unrelated stored fact) is not covered. Add: such a reply is WRONG. Fix before the run and record it.
9. The harness does not fit: `run_demo_branches.py` hard-codes PREFIX = 14 and `questions_r176.json` and wraps one
   PeftModel onto base (three in a row would stack); `demo_judges_r176.py` hard-codes 4 arms and tallies in_view as
   facts. Register new scripts: each adapter on a fresh base or unloaded between arms, all adapter hashes saved, base
   arms first, 96 items, a new shuffle seed, a tally by kind.
10. Give the writer absolute paths.
11. All 12 branches share one history, so they are not 12 independent tests. State: counts only, one chat, items not
    independent; no ranking of models.

Leakage: the list labels do not tell the writer how to favour a model, but the design follows the known failures
(look-alikes, shared-word never_told, 4 of 12 never_told). The record should say it is blind to the models, not blind
to the failure types; "blind for K1" (R-182) needs that qualifier.

Verdict: ready with the listed changes.
