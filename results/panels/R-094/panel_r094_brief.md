# Panel brief: the who-is-who slip in fact answers (2026-11-06 04:15)

Kevin: "don't love that weak spot" / "panel a fix". The panel comes up with the fix, then a second round
agrees one plan.

## The failure

v6 = 17m seed 82 passed R-076's rule at seeds 85 to 87 (R-093). Its fact answers are right but sometimes
pin the relation on the wrong person or on the speaker:
- "i'm blanking on what my barber is scared of" -> "Hana's barber is scared of clowns." (should be "Your
  barber Hana is scared of clowns.")
- "which club did Chidi join" -> "Chidi, who is my daughter, joined a water polo club this month."
- "what can my godfather speak besides english" -> "My godfather, Lucia, speaks fluent Turkish."
Judge 1 marked 15 of 48 such answers down at seed 87 (2 and 6 at seeds 85, 86).

## Measured (a mechanical pattern: "<Name>'s <relation>", "who is my", or a sentence opening "My <relation>")

Answers to `older` and `confirm` items, probe 73157, of 96 per seed:
- base 3; v5 3, 4, 4 (seeds 82-84)
- 17b 4, 1, 12, 5, 1, 10 (82-87); 17m 3, 4, 2, 1, 3, 14 (82-87); 19a 3, 7 (82, 83)
- hard_dev, same pattern: 17b 1-3 a seed; 17m 0-7 a seed

Training targets: 39 of the 350 `older` and `confirm` answers in 17b's / 17m's set (`strict_chat.jsonl`)
carry the pattern. They are base's own replies to the real search result, kept when they named the value
(only `confirm` rows get the scripted answer, "Your {relation} {person} ..."). Examples:
"My roommate, Omar, writes western novels at night."; "My cousin Omar is moving to Oslo in the spring.";
"Fun to know! Dana's coworker is happy with their new kitten, Tofu."; "It seems like Omar's aunt broke her
forearm while skiing."

History: scripted confirm answers alone failed coherence once (fix 5b, R-033); train answer templates
"Your {relation} {person} ..." passed (fix 5c, v4, R-035/R-036).

## Compute and rules

About 65 min a candidate-seed; R-088's reserve (about 25 candidate-seeds plus a buffer) is uncommitted;
the freeze is Tuesday Nov 10. Any fix must pass R-086's gate at seeds 82 and 83, then R-076's rule at
fresh seeds; 85-87 are used, so a new confirmation would be at 88-90. The ship rule: fewest changes from 17b unless pooled hard_dev recall is
higher by more than 15. The evaluation and its rules stay fixed.
