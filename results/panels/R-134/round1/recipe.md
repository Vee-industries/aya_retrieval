**Field: LoRA training dynamics and recipe**

**Disclosure first.** One of my globs, `results/recall_eval/probe*base*73157.json`, matched `probe2_base_tokens_seed_73157.json`, a file the brief forbids because its name contains "token". All I printed from it was four in-view counts, which were identical to `probe2_base`. I did not use them. I wrote no files. I opened nothing sealed and read no seed 97 to 99 file.

**What the recipe is.** From `results/recall_train/fix17cs37_82.json`: rank 32 with alpha 64, attention plus MLP modules, learning rate 3e-4, batch size 2. Training runs for **3 epochs** and also saves an epoch-2 checkpoint. The 6.37 that ships is the 3-epoch final, not a 2-epoch model. `--loss-on` is given twice and argparse keeps only the last one, so the setting is `chat_decision`. In `scripts/run_recall_train.py` and `src/aya_retrieval/loss_masks.py`:
- `demonstrated` puts loss on every token of the assistant turns after the friend's message.
- `chat_decision` is the same, except the 222 `statement` rows get `decision_labels`: loss only on the reply's first token and its end-of-turn marker.
- So the 150 in-view rows carry full loss on every word of their reply, and those replies are base's own words.

**1. The weakness.** The in-view misses repeat the in-view training replies almost word for word. At `hd_fix17cs37_82/83`, 11 of the 14 misses open "It sounds like" and none searched. For example:
- 419_in_view_23 says "dealing with a bit of a situation", as does training row in_view_0088.
- Several misses say "trying to remember ... Can you give me a hint?", as do in_view_0000 and 0036.
- Several say "feeling a bit lost or confused", as does in_view_0122.

A phrase search over the 150 in-view targets finds 18 that ask the user, deny, or send the user elsewhere instead of answering plainly (0000, 0015, 0036, 0057, 0059, 0079, 0085, 0086, 0088, 0094, 0103, 0120, 0122, 0130, 0134, 0136, 0139, 0146). 9 of these open "It sounds like". in_view_0103 ("You can ask your cousin Ivan...") has the same shape as the lower-case deflection ("You can ask your godfather"). So the deflection comes from these targets, trained at full loss.

**2. Can a recipe change fix it? I checked each option against existing runs:**
- **Decision-only loss on in-view rows** (a new `LOSS_ON` entry with `kind in ("statement","in_view")`; 372 masked rows; the existing collision check covers it). The reply words would go back to base's. When base answers without searching, it gets 32 of 41 right on `hard_dev` (78%) and 30 of 35 on the probe (86%). 6.37 gets 200 of 240 (83%) and 88 of 96 (92%). So the expected effect is a loss, not a gain. The first token stays trained too, and 22 of the 150 first tokens are "It".
- **Masking only the answer words on `older` rows** (fix B, `fix17mb`): `hard_dev` in-view 36 and 30, worse.
- **Fewer epochs**: `fix17e2` (17b trained to the end of 2 epochs) gives `hard_dev` in-view 37 and 37 with 10 and 13 "It sounds like" openers. 17b itself gives 38 and 36 with 11 and 14. No change. The epoch-2 checkpoint is worse: `fix17m_e2` gives 32 and 40, with recall 38 and 63.
- **Lower learning rate**: `fix17e2lr2` keeps in-view the same (36, 39) and loses recall (54, 66).
- **Rank and modules**: R-044, R-048 and R-053 show these act on recall only.

**Seed spread is larger than any of these effects.** 6.37's `hard_dev` in-view is 42, 40, 43, 36, 39 (standard deviation about 2.7 of 48). 6.33 gives 44 and 34. 6.34's drop from 78 to 69 is about 1.6 standard deviations of a two-seed difference, so it is weak evidence that the 22 rows are needed. It is not proof.

**Proposal: none from the recipe.** The fault is in the targets, so no loss setting can teach the right words: masking returns base's words, which are worse. The fix would have to replace the 18 targets above with base replies that state the value. That is a data edit like R-118, outside my field, and R-120 and R-121 show the risk.

**3. Line and risk.** If the decision-only mask were run anyway, the line it aims at is `hard_dev` in-view (now 40 a seed). Base's own words predict about 37.5, so it would likely fall. The gate line most at risk is `hard_dev` recall pooled at 82 and 83: the floor is v6's 157 and 6.37 has 163. R-121 shows the in-view reply words affect how much detail found-fact answers give.

**4. Confidence a recipe-only change replaces 6.37 under the full gate: about 0.05.** A change with no effect already passes only about 0.3 at 82 and 83 and holds about 0.4 at fresh seeds (R-127), roughly 0.12 together. It must then also match 6.37's recall at unread seeds 97 to 99, and the measured comparisons point down for in-view.

### Critical files
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/run_recall_train.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/src/aya_retrieval/loss_masks.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/data/screens/fix17cs37.jsonl
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/results/recall_train/fix17cs37_82.json
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/results/recall_eval/hd_fix17cs37_83_seed_73157.json