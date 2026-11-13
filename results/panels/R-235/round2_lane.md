# Design lane, round 2 (against-minded)

Prior: 11 seed-82 tries, both fresh adapters and stages, all score 2 of 6 older at the end, except K4.6 at epoch 2, which then failed hard_dev. More of the same data, more epochs or a higher rate has not moved that 2. A lever has real odds only if it changes what the model does on the failure seen in the record, not how much it trains. The odds below are all low. They are ranked against each other and are not predictions.

## 1. Ranked levers

1. **Merged first query.** Build natural rows whose one search is the question's `query` words plus its `second_query` words in a single OR call. Then stage K1.3's adapter at 1e-4 x 1 on the whole set (K1.3's 1,094 template rows plus the rebuilt natural rows). Cost: about 15 min of code and build (a flag in build_k3.py at line 129; rerun the balance step and check_k3.py), then about 30 min to a Demo2 result. Need: no new writing, only the existing writer fields. Why it ranks first: the main failure is a query that does not reach the fact, followed by a stop (65 of 108 outside-writer misses; 3 of 4 Demo2 misses). One merged OR call gets the category words' reach without the model having to learn a second call. 1e-4 x 1 on the whole set is T1's setting, the only stage that kept never-told at 4 of 4. Main risk: category words bring the other person's same-type fact into the top 5 more often, which threatens hard_dev never_told 44 of 48 and false retrieval at most 4.
2. **Order swap.** Use the writer's `second_query` first, then `query`, same stage settings. Cost: about 45 min. Need: a code flag. It ranks below 1 because category words alone lose the person anchor. That makes the wrong-person risk worse, and it can lose the 2 items the question-word query answers now.
3. **Stage from K4.6's epoch-3 adapter** at 1e-4 x 1 on K1.3's whole set. Cost: about 30 min. Need: none. K4.6 e3 already passes hard_dev and has learned second searches, but its own Demo2 is 2 of 6, and no training on similar data has moved a 2. Its seed-83 screening has to be checked before it can be the pick.
4. **K5 third-search build as stage data** (K1.3 adapter, 1e-4 x 1). Cost: about 30 min. Need: the existing build. It adds a third call after two misses, but the main failure is stopping after one (65 searched once, 8 twice), so it targets the smaller mode.
5. **K4.9 miss-then-hit rows as stage data** (K1.3 adapter, 1e-4 x 1). Cost: about 30 min. Its 27 rows were already in a fresh 3-epoch try that scored 2 of 6. That is too few rows, and the effect has already been measured as none.
6. **More found-and-named rows** (less decline-side balance cut). Cost: about 40 min. It targets the 1 Demo2 item that is found and declined on every try (35 of 108 outside). That item has been declined on all 11 tries, which points to the wrong-person rejection that screening rewards. Pushing toward answering puts never_told and false retrieval at direct risk. This is the lowest chance of passing all gates.

Run 1, then 3, while T4 to T6 finish. Take 2 only if 1 fails screening on false retrieval.

## 2. Must not be done

- Choose, word or filter queries, rows or chats by looking at Demo2's or Demo3's items, including the 4 missed items' words or the writer's style.
- Read Demo3 for any try that has not passed Demo2. Rerun Demo2 on other seeds until one passes.
- Pick an epoch or checkpoint because it passed Demo2 (the K4.6 epoch-2 case). Use any rate or epoch count other than 1e-4 or 3e-4 and 1 or 3.
- Change hard_dev, its 44 and 4 cutoffs, the outside-writer sets, the tool, the prompt, the eval or the judges. Hand-edit rebuilt rows. Report the outside-writer sets as held-out once they have steered a lever (they steered the ranking above, and that must be stated).

## 3. If rounds 1 and 2 both fail, tell Kevin

The result first, as raw counts: K1.3 stays the pick and passes screening, but scores 0 of 6 older on Demo2, so it fails the Demo2 gate. No try that passes screening passes Demo2. Every try scores 2 of 6, and the one 3 of 6 (K4.6 epoch 2) failed hard_dev at never_told 39 and false retrieval 10. The measured cause: the model's own keyword queries do not reach 3 of the 4 missed facts, and it stops after one search. The tool can reach all four (K4.1's searches once returned them). The fourth is found and declined on every try. State it plainly, with no softening and no "close". The decision for him: submit K1.3 with the Demo2 failure disclosed, or rule on whether the fixed tool, prompt or eval may change. That ruling is his, and no change is made without it.
