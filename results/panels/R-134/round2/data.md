**Round 2: data curation**

**Checks on the other reports** (`fix17cs37.jsonl` and 6.37's results at seeds 82, 83, 94 to 96)
- **Confirmed:**
  - stats: `hard_dev` in-view 42, 40, 43, 36, 39.
  - against: 57 correct replies open "It sounds like", 6 targets open "You can", and the 6.34 group ids.
  - dialogue: no training row says "my head has lost".
- **against, "rewriting has been tried four times": wrong.** Fix 13 changed the questions, not the answers. 6.311 and 6.32 added 72 rows and left every deflecting target in place. Fix 12 is the only true precedent: it replaced all 150 targets with *brief* base replies, on one seed.
- **against, "the opener comes before right answers more often": misleading.** In `hard_dev` it opens 57 of 200 right answers (29%) and 32 of 40 misses (80%).
- **recipe: two small errors.** 12 of the 14 misses at 82 and 83 open "It sounds like", not 11. 27 in-view targets start with "It", not 22.
- **dialogue's 44 rows miss 6 clear deflections:** 0027, 0058 ("Can you try to recall..."), 0060, 0064, 0099, 0132.

**1. Final position: a merged fix, 6.38**
- Keep all 1,094 rows and every user turn. Replace only the final assistant turn of 50 `in_view` rows: my 28 plus dialogue's 44, with 22 ids in both.
- New target: base's own reply, resampled on the same three exchanges with no tool and not shortened, up to N candidates. N is fixed before the build. Keep the first candidate that passes all three checks:
  - it names the value (the existing scorer);
  - it has none of my deflection phrases anywhere in the reply, not only in the opener ("hint", "trying to remember", "feeling a bit", "ask your", "tell me more", "something else", "a bit lost", "It sounds like you", "It seems like you", "tough one", denials);
  - it has no four-word run in common with the probe or `hard_dev`.
- If no candidate passes, use `hinted_reply`, then my hand-written rule (value first, no question, never opens "Your").
- One fresh blind judge vets every new target. The build reports how many rows changed and from which source.
- Same recipe, trained from scratch.

**2. Strongest objection (stats and against)**
The in-view lines barely gate. Seed noise is larger than any likely gain, and in-view edits cost found-fact recall before (R-063 and R-064).

My answer: R-097 (probe in-view at least 41 at both seeds) is a real gate line, and 6.37 itself scored 39 at seed 95. The deflection comes from these targets at full loss, as recipe and against agree. Fix 12's cost came with brief replies on all 150 rows. This fix uses unshortened base replies on a third of the rows and changes no search decision. That narrows the risk; it does not remove it.

**3. Probability: down from 20% to about 7%**
Stats' per-line pass rates for an exact clone of 6.37 (about 3% for the full gate) are better grounded than my figure. The fix helps one line and leaves the rest to chance.

**4. What I need in the chair's design to vote yes**
- The 50 ids, N, the phrase list and the fallback order, all recorded before the build.
- The comparison at 82 and 83 fixed now: 6.37's 192 and 163, or v6's 192 and 157.
- 6.37 retrained at 97 to 99 from the byte-identical set, queued first. It can start at 15:05, since it does not depend on 6.38, which keeps the 04:00 clock. Pooled sums, ties pass. If 6.37's runs do not finish, 6.38 fails.
- No rows added in the "my head has lost" or lower-case shapes, because that would be fitting to `hard_dev`.
- A fail ships 6.37 unchanged, and the write-up says the deflecting targets are the probable cause.