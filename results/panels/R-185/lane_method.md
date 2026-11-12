# R-185 method lane (claude-opus-5-5; read only the brief's allowed files; pools.py not opened, TRAIN imported for its people and relations; read-only Python over committed files)

**1. The single-passage explanation is not supported as the main cause.**
- In 24 of K1's 61 found-but-wrong hard_dev rows, K1 sent the same query as 6.37 and 6.37 answered right. Same chat
  and same query mean the same search output and passage count, yet K1 gave a wrong reply. Source:
  hd_k1_r178_{82,83} against hd_fix17cs37_{82,83}.
- Of the 61, 43 decline and 18 give a passage line.
- A better explanation: 6.37's training separated the two cases perfectly. If a returned passage names the asked
  person or relation, the target answers (562 of 562 search rows); if none does, it declines (138 of 138). K1 breaks
  this: 53 of its 160 never_told rows (the same_person share) have a passage about the asked person and a decline
  target. Source: data/screens/fix17cs37.jsonl and k1_r178.jsonl.
- So K1 learned to decline when a passage is about the right person but its wording does not match the asked type.
  By answer type (both seeds, found rows): hometown ("grew up in Cork", searched with the training birth query) 6.37
  24 of 24, K1 7 of 25; interview day 21 of 28 against 13 of 28; pets in indirect wording 17 of 24 against 13 of 25;
  other types 87 of 89 against 76 of 85.
- This also explains the 5-or-more bin: 12 of K1's 23 wrong there are hometown items.
- T2 points the same way: 6.37's 53 false answers are 52 same_person, 1 same_type, 0 shared_word
  (st_of_{probe,hd}_*_{82,83}). The share K2 needs for T2 is the same share that breaks the separation.

**2. F3 is not a plausible cause.** K1 has 139 rows with a declined reply in view (116 answer targets, 23
never_told). hard_dev runs with asked_before False, so it has no earlier questions in view. On outside-writer chats K1
declines 37 found facts against 6.37's 8 (blind_ and blind2_ files); those fit the found-but-declined pattern, not
F3. Not settled: whether in-view replies carry loss under chat_decision.

**3. Neither A nor B as written.** A keeps all 53 decline rows about the asked person, and the same-query evidence
argues against passage count. B halves F3, which has no evidence against it and drives T3 (68 against a gate of 184),
and halves F2 found rows, which T2 recall needs.

Candidate K2 = K1 with only the same_person never_told rows halved.
- Rule: in `f2_shares`, for never_told only, the rows K1 gave `same_person` alternate in row order; odd ones keep
  `same_person`, even ones are rebuilt with `same_type`. They keep their decline target; the existing fallback
  replaces any row whose search returns no passages. All other rows, F3, the 50 re-asks and found-row shares stay as
  in K1.
- Check before training (no model): never_told rows with a passage naming a relation or person from the final
  message 24 to 30 (K1 53, 6.37 0); rows that differ from K1 at most 27, all never_told; never_told rows with passages
  160 of 160; found and never_told mean passage gap no larger than 6.37's 0.37 (K1 2.98 against 2.74). Fail any line
  and nothing trains.
- Expected effect (direction only; dose response unmeasured; seed noise about 20): hard_dev recall (+29 needed),
  outside-writer recall (+7) and T2 recall (+22) should rise; T2 false answers rise from 3 with room up to 26; T3
  unchanged. Risk: 27 rows still teach the same type check.

Recommendation: K2 = K1 with every other same_person never_told row rebuilt as same_type (24 to 30 rows about the
asked person left), F3 and found rows unchanged; not A, not B.
