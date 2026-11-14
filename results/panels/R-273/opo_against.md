Recommendation: do not run OPO; report K1.3 as the pick. If Kevin gives a fresh go for this lever by name, run it changed (new tag and file names, an answer-row floor of 18, a stop when no row has the source not first), and record any Demo5 result as its second read.

# Against lane: OPO, 2026-11-14

Sources: the brief, `R-271/c2_against.md`, `build_onpolicy_template.py`, RECORDS R-263 to R-272. "Estimate" marks arithmetic on those counts.

## 1. A registered stop rule already covers this

R-271, registered before C2 ran: "C2 fails hard_dev: no C3, no smaller retry, no OPT; K1.3 stays the pick." C2 failed (43, R-272). OPO is OPT at a smaller dose, so the rule names it twice. Earlier today Kevin lifted R-267's stop with his own word (R-271). Nothing in the files I read shows a new word from him after 09:45. Not checked whether one exists. Without it, OPO breaks a rule set before the result was known.

## 2. Dose and floor (point 1)

- 48 older and confirm items at OP's hard_dev reading-error rate (27 of 96) give about 13 answer rows before drops (estimate). The pool's templates were trained on, and rows are dropped when the value is not in the last output, by K3.1's runs, and by the token cut, so fewer is likely. Not checked.
- OP's 18 answer rows cut reading errors 32 to 27; a plain epoch with no rows cut them 27 to 23 (R-271). Rows have not yet beaten a plain epoch. A floor of 10 allows a dose about half of OP's, so OPO minus C1 is expected to be inside one-item noise on hard_dev (estimate). The only measured dose to cite is OP's 18; 10 is the OP4 lane's number, not a measurement.

## 3. never_told (point 2)

- OP never-told 48 of 48, all with one search (R-268). The 24 never-told items will then give almost no decline rows and about 24 correct declines (estimate). The decline side is rows the model already gets right; the new pressure is all toward answering.
- The plain epoch alone took 48 to 46 (C1). OPO is C1 plus that pressure, so its expected never_told is at or below 46, with 2 items to the line (estimate, direction only). C2 shows the slope: a third answering push gave 43.
- Check before training: `built_by_type` (decline vs correct_decline), `kept_each_side`, `new_answer_rows` after the token cut, and every `dropped` count.

## 4. Does it reach the demo misses? (point 3)

- The deciding gate is Demo5, where C1 had 2 of 6 and needs 3. The misses there and in Demo4 are natural chats with a passage about someone else ranked above the source.
- The code's own note says template items name no person (line 121), so no row can hold "someone else's passage first". `source_first` (line 54) only asks whether the answer string is in the first chunk; it does not test who the passages are about. `source_not_first` counts rank, not the demo class.
- The answer check is a substring of the last output (line 87). The R-271 lane asked for "in a passage about the right person". That is not in the code. With decoys in the pool (line 66), a value found in a decoy passage is possible. Not checked.
- hard_dev is the training template family (c2_against). A hard_dev gain from template rows is the expected fit and says little about the demos.

## 5. Demo5 (point 4)

C1, OPO's exact control, bombed Demo5. OPO would be the second read, chosen knowing the first, and would aim at C1's Demo5 misses. Each step so far moved a demo's older line by one item of 6. A pass at the line on a second read cannot be told apart from a draw.

## 6. If Kevin says go: changes

1. The script is fixed to C1: `eval_label` is `opt_c1_SEED`, TAG "R-271", out `k13opt_SEED_r271`. Running it on OP's eval writes OP's rows under C1's name and the R-271 hash. Give it a new tag, label and stem, then rebuild OP's seed 82 set and confirm SHA-256 479c9379... is unchanged.
2. Floor: at least 18 answer rows after every cut (OP's dose, the only cited one), or no training.
3. `source_not_first` of 0: stop, the rows do not touch the demo miss shape at all.
4. C1 is the control on hard_dev and Demo4. Record Demo5 as read 2. OPO fails any gate: the day ends, no further retry.

## 7. The simple alternative (point 5)

Stopping is the better call. Four tries today (OP4, C1, C2, and OP2 and OP3, which built nothing) found no lever past Demo5. OPO's control already fails it, its rows cannot hold the demo miss shape, and a registered rule says stop. K1.3 (pick recall 742) stays the pick. This page did not check the clock, the card, or the seed 83 and 94 timings.
