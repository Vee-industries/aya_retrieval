# Against lane: blend and T4 + never-told rows

**Recommendation:** Neither lever is more likely than not to pass. If one is run, run lever 2 once after T5. Run the blend at most once, at w = 0.5 registered before any result. Check hard_dev before spending an 18th Demo2 read where the registry allows it. K1.3 stays the pick unless a candidate matches it on hard_dev (46 / 2).

All probabilities and predictions below are my judgment from the five rows in the brief. They are unsourced and not measured.

## 1. More likely than not?

**Blend: no (about 20%).** T4 was staged on K1.3, so the blend equals K1.3 + w x (T4's stage change). At w = 0.5 that is a half-size T4 stage.
- Strongest for: the merge is exact and costs no training, so it tests the midpoint of the trade cheaply.
- Strongest against: it can only move along the line between two points already measured, and the brief says every measured point sits on one trade. T4 reaches Demo2 3 / 3, exactly at both thresholds. Any shrink of the stage is likely to drop one older item and one never-told item first. T1 was a smaller step (1e-4) on different data and landed at 2 older. Half of 46 to 38 is 42, which is under 44.

**Lever 2: no (about 35%), but it is the better of the two.**
- Strongest for: it is the only lever that changes the cause. T4's hard_dev failure is in never_told and false retrieval, and the dropped 160 rows include the ones built for hard_dev's same-type trap.
- Strongest against: K1.3 already held those rows, and T4 at 3e-4 still wore hard_dev down from 46 to 38. At 160 of 1,553 rows (10%) for one epoch, they may be too few to hold it. There is also a format shortcut. The 160 rows are scripted and the 1,393 are natural, so the model can learn "decline on scripted-looking input, retrieve on natural input". If hard_dev reads like natural rows, the restored rows do not help it. If they do help, they pull Demo2 older back toward K1.3's 0.

## 2. Blend w

0.5 is not more honest than any other w; no data picks it. It is acceptable only as a single try registered before the result. Trying 0.5, then 0.67 after a Demo2 miss, is a search along the curve tuned on a gate already read 17 times. If more than one w is run, register a fixed grid now: three points (0.33, 0.5, 0.67). Register the rule now too: pick the highest w that passes hard_dev on seed 82, and read Demo2 once, for that w only. Leave Demo3 untouched until the end.

Disclose:
- every w run and its full numbers
- that w was not chosen from data
- that Demo2 has n = 6 older items, read 17+ times, so 3 of 6 against 2 of 6 is one item
- the count of all candidates tried on seed 82

## 3. Order

1. Let T5 finish.
2. Run lever 2.
3. Run T6 and round 2's four as registered.
4. Run the blend last, or drop it.

Both levers are unregistered additions. Register them before their results and say which registered tries they delay. Each lever also needs per-seed training for seeds 83 and 94 (about 25 minutes each); that fits the time left before Saturday 16:00 ET. Note that the brief's gate names seeds 82 and 83 for screening, but it names 94 for the T4 stage. Confirm which seeds are registered.

## 4. Predictions, seed 82

| Lever | Demo2 older | Demo2 never-told | hard_dev never_told | hard_dev false retrieval |
|---|---|---|---|---|
| Blend w = 0.5 | 2 (range 1 to 3) | 4 | 43 (41 to 45) | 5 (3 to 8) |
| Lever 2 | 2 (1 to 3) | 4 | 43 (40 to 46) | 5 (3 to 8) |

Not checked: hard_dev's format against the 160 rows, the composition of K4.6, and whether the registry fixes the gate order.
