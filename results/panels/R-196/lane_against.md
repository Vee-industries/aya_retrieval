# R-196 against lane (claude-opus-5-5; read only what brief.md allows; ran no model)

Counts are mine, read-only Python over committed files (scripts in my scratchpad, not in the repo).

**1. The gap is real; the found-and-declined count is fair, its seed 83 column inflated.**
- 6.37 hard_dev older + confirm, eight seeds (`hd_fix17cs37_{82,83,94..99}_seed_73157.json`): 73, 90, 77, 87, 83, 79,
  80, 76; mean 80.6, sd 5.4, range 17. fix17m, 12 seeds: sd 3.8; fix17b, 6 seeds: sd 6.2. K1: 57, 65, its best 8
  below 6.37's worst. A gap of about 20 is 3 to 4 per-seed sd. The brief's "about 20 points" is a two-seed range.
- 6.37 finds the fact and then declines on 0 items at all 8 seeds. The habit is K1's.
- Seed 83 is 6.37's best seed. Of K1's 28 items lost there, 15 are items 6.37 misses at another seed; of the 19
  found-and-declined, 9. On items 6.37 gets right at all 8 seeds, K1 finds and declines 13 (seed 82) and 10 (seed 83).

**2. The brief's cause does not match the data.**
- By ask form (tagged against `pool_hard_dev.py`; 6.37 8 seeds, K1 2): same_words 73/104 (70%) against 4/26 (15%);
  confirm 87% against 70%; indirect 85% against 71%; new_words 85% against 75%. K1 loses most where the question's
  words match the statement, the reverse of the brief's reading.
- By type: hometown 98/104 against 7/26 (confirm hometown 64/64 against 2/16, 13 declines); bake 100% against 86%,
  tea 90% against 88%. Both brief examples are hometown. hard_dev shares no fact type with training
  (`pool_hard_dev.py` docstring); training cannot cover hometown without taking a type from hard_dev.
- K2.1 already tested the dose: decline rows whose passage names the asked person, K1 53, K2.1 27 (`check_r185.py`'s
  rule); hard_dev pooled 122 against 119 (R-195); found-and-declined 17/19 against 14/18. No recall gained; T2 false
  answers 3 to 20.

**3. Direction A adds what K1 already has.** `k1_r178.jsonl`, same_person share: 93 older rows (31 indirect, 39
new_words, 23 same_words, tagged against `TRAIN` and `MORE_INDIRECT`) and 77 confirm. Rows whose passage names the
asked person: 562 answer, 53 decline. 294 of the 562 share no content word (4+ letters, names and relations removed)
with that passage, as do all 53 declines. Fifty more rows move 562 to 612 against 53; K2.1 moved the balance further
with no effect.
- Leakage: training user lines share 6 three-word and 1 four-word runs with hard_dev's forms (6.37 and K1 alike);
  "came of age" and "ever come up" appear in no training file. The larger leak is the design: picking rows for few
  shared words copies how hard_dev was written, so hard_dev stops testing K1.1 fairly.
- Never-told harm: each added answer row naming the asked person pushes toward answering; T2 is the line that moved
  when K2.1 shifted this balance (gate 26).

**4. Direction B's premise fails.** The 124 spliced rows: 52 older (`indirect/`) and 72 statement (`facts/` 57,
`contrast/` 15), which ask nothing. Of K1's 137 indirect-form older rows, 85 are rebuilt with F2, 31 in same_person.

**5. Cost.** Per candidate about 3 x 33 min training plus up to 3 x 75 min screening, about 5.4 h of card; 17:30 today
to Saturday 16:00 is 46.5 h. Time is not the limit; optimism is. K1.1 would be the seventh candidate on these pools
since 6.37 (6.38, 6.39, 7, 7.1, K1, K2.1). 6.37's per-seed dev total (probe + hard_dev + blind + blind2) has sd 7.7
over 8 seeds; assuming independent seeds, two candidates' 3-seed sums differ with sd about 19 (my estimate). K1
against K2.1 was 481 against 485. A K1 against K1.1 pick would be mostly noise, and the winner could carry K2.1's T2
rise.

**6. K1 alone.** If base's rerun puts K1 above base on every recall line, K1 is the only eligible arm; seed 94 trains
today. It enters S3 where its dev margins are widest: T3 68 against 368 (gate 184), T2 3 against 53 (gate 26). Its
recall gap to 6.37 (hard_dev 122 against 163, outside-writer 171 against 188) is reported as the cost, and S3 measures
it on unread chats (119 of 178 older items outside training's categories, R-179). If base beats K1 on any line, no
arm is eligible and 6.37 stays shipped; only then is a candidate worth its cost, and not A or B. Untested causes: F3's
117 declined replies in view (a K1-without-F3 removal test), or never_told rows with empty searches (6.37 22, K1 0).

**If Kevin wants K1.1 anyway** (R-194 allows it):
- Design: added rows only, no never_told row changed; types and wording from `TRAIN` and `MORE_INDIRECT` only.
- Check before training: decline rows naming the asked person exactly 53; runs shared with hard_dev forms at most 6
  (three-word) and 1 (four-word), any new row sharing one removed; found against never_told passage gap at most 0.37;
  zero-overlap answer rows reported against K1's 294.
- Predictions first: hard_dev pooled, same_words and hometown right counts, T2 false answers.
- Disclose: designed from hard_dev items after K1's and K2.1's results; seventh candidate; pick-noise sd about 19.
  Kevin rules before the build whether a K1.1 ahead of K1 by less than that replaces it.

**Verdict:** against K1.1 by A or B. Carry K1 alone to the pick; build a candidate only if base's rerun leaves no
eligible arm, and then from a cause the data have not ruled out.
