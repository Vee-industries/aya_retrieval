**Chair's design: 6.38 (`fix17cs38`)**

I checked the disputed facts in the repo myself. I wrote nothing and opened no sealed file, token file or seed 97 to 99 file.

**Which rows truly deflect.** I read all 150 `in_view` targets in `data/screens/fix17cs37.jsonl` (SHA-256 `04df294a…`).
- **All 28 of the data expert's rows deflect.** None answers as a known fact about the right person. About 22 of them name the value, but inside one of these:
  - a request for a hint (0036, 0058);
  - a puzzle (0098);
  - a reading of the message as a feeling (0086, 0122, 0134);
  - "lost" read as losing a thing (0094, 0145);
  - a referral elsewhere (0103, 0120, 0139);
  - a denial (0015, 0085).
- **0124 and 0143 are bad targets too.** 0124 gives the coworker's job to the speaker; 0143 is a denial. But their wording ("That's not true", "I don't know much about") is in none of the 66 in-view misses, or any in-view reply, over hd and probe at seeds 82, 83 and 94 to 96. The 28 rows' phrases are in those misses (10, 9 and 14 times for three of them).
- **The 12 "It sounds like your…" rows outside the 28 state the value:** 0001, 0012, 0018, 0033, 0049, 0056, 0065, 0082, 0096, 0109, 0125, 0127.
- **0110 and 0105 hedge but give the value.**

0124, 0143, 0110 and 0105 stay unchanged, and this is disclosed.

**1. Name and rows.** `fix17cs38`, version 6.38, built by a new `scripts/records/build_r134.py` modelled on `build_r122.py`. It changes the final assistant turn of these 28 rows:
`in_view_` 0000 0015 0027 0036 0057 0058 0059 0060 0064 0077 0079 0085 0086 0088 0094 0098 0099 0103 0120 0121 0122 0130 0132 0134 0136 0139 0145 0146.

**2. How targets are made.** Targets are hand-written by the main session, in a dictionary in the script (row id to value and target). No base resampling: it would need the GPU while 6.37's control runs must have the card to themselves. Disclosed: the writer has read the `hard_dev` and battery misses, and those items are scored again. The build stops on any row that fails a rule:
- the dictionary's value appears, ignoring case, in the row's fact turn and in the first sentence, along with the person's name and every detail on the chat line ("Priya won a telescope in a raffle.");
- the target opens with the name or the value, never "Your" or "My";
- no "?";
- none of: hint, remember, recall, feeling, lost, confused, "ask ", "tell me more", "something else", "it sounds like", "it seems like", "tough one", "i don't", "didn't", "you can";
- at most one more sentence, and it must appear word for word in another `in_view` target;
- `slip_shape` is False;
- no four-word run shared with `TEST_GRAMS` (`build_r110`);
- the row stays at or under 1,024 tokens.

**3. Vetting.**
- One fresh blind Sonnet judge marks the 28 new targets under `results/vet/R-118/rubric.txt`. The 28 old targets are shuffled in as hidden controls; their marks are reported, not gated.
- A rejected target is rewritten once and marked by a second fresh judge. If it fails again, the old target stays.
- The number changed is reported. The set is frozen (SHA recorded, committed) before training, and judge transcripts are audited.

**4. Recipe and build checks.** 6.37's recipe exactly, from scratch, clean tree:
`run_recall_train.py --seed S --data data/screens/fix17cs38.jsonl --lora-r 32 --lora-targets q_proj k_proj v_proj o_proj gate_proj up_proj down_proj --learning-rate 3e-4 --max-vram-fraction 0.85 --save-epochs 2 --loss-on chat_decision`
Defaults stay: 3 epochs, batch size 2.

The build checks:
- 1,094 rows, same order, ids and kinds, 150 `in_view`;
- only `turns[-1]` differs, in at most 28 rows;
- the SHA-256 of the 1,066 or more unchanged lines matches the same lines in 6.37's set.

The train report must show 1,094 rows, `decision_rows` 222, `loss_on` `chat_decision`, and no collision error.

**5. Registered comparison** (written into RECORDS as R-134 before any row is built)
- **At 82 and 83:** the reference is 6.37's 192 (probe) and 163 (`hard_dev`). This is stricter than v6's 192 and 157.
- **At 97 to 99:**
  - 6.37 is retrained from its byte-identical set and command, already queued first and alone on the card.
  - Pooled three-seed sums on probe and `hard_dev` recall; ties pass.
  - 6.37's 97 to 99 files are scored by script and not opened until 6.38's are done.
  - If 6.37's runs there do not finish by Monday 12:00, 6.38 fails. Those runs do not re-decide whether 6.37 ships.
- **Stop rule:** any failed line stops the try (this covers recipe's below-157 stop). There is no 6.39.

**6. Gates and queue**

At 82 and 83:
- **R-086, unjudged:** probe 51203 recall at least 94 and `statement` at least 47 at seed 82; `hard_dev` `never_told` at least 44 and false retrieval at most 6 at seed 82; probe recall pooled at least 189; `hard_dev` recall pooled at least 145.
- **R-086, judged:** probe and `hard_dev` Sheet B `statement` and `in_view`, and the check set at both seeds, each at or above base. Three fresh judges, judge 1 decides.
- **R-094:** probe slips at most 5 a seed; `hard_dev` slips at most 3 a seed; recall not below the item 5 reference.
- **R-097:** probe `in_view` at least 41 at each seed.
- **R-102:** held-out corrections at least v6 + 48 (probe) and v6 + 32 (`hard_dev`), above v6 at each seed; phone typing not below v6 by more than 8 (probe) or 16 (`hard_dev`).

At 97 to 99:
- R-076's rule (`rule_r076.py`), with Sheets A, B and h and three fresh judges;
- R-094's slips, including probe pooled over 82, 83 and 97 to 99 at most 8;
- recall against 6.37 retrained, as in item 5;
- R-102's fresh-seed items (`fresh_report.py fix17cs38 97 98 99`).

Timeline from 16:30:

| Time | Work |
|---|---|
| 16:30–17:00 | vote; register R-134 |
| 17:00–18:45 | write, build, vet, freeze (CPU only) |
| until about 19:05 | 6.37 trains at 97, 98, 99 (GPU) |
| 19:05 | 6.38 at 82 trains |
| 19:57 | 6.38 at 83 trains (both start before 22:00; the latest safe start for 82 is 21:08) |
| 20:49 | 6.37's six evals at 97 to 99 |
| 21:40 | 6.38's five count evals; read them and stop on a fail |
| 22:20 | eight R-102 stress runs; judges on the CPU, with a stop file |
| 23:25, 00:17, 01:09 | 6.38 trains at 97, 98, 99 (all before 04:00) |
| 02:01–04:30 | 18 evals at 97 to 99 |
| about 05:00 | four lower-case (`st_style`) runs at 82 and 83, reported only |
| about 07:00 | judging done; verdict before Monday 12:00 |

**7. Write-up discloses:**
- that this is candidate 17 since R-093;
- that the targets were hand-written by the main session after reading misses on items that 82, 83 and 97 to 99 score again, so in-view gains are not independent evidence (only the sealed pool after the freeze is);
- the copied-phrase evidence;
- the four rows left unchanged;
- the measured in-view and lower-case results whatever they show, with no gain claimed below +3 a seed;
- on a fail, that 6.37 ships and the deflecting targets are the probable cause.

**8. Each expert's yes conditions**
- **Data:** met except two. It is 28 rows, not 50, because the 12 rows dialogue withdrew state the value (6.34's risk). It is hand-written, not resampled, because resampling needs the card. Data's round-1 design was exactly this.
- **Retrieval:** not met on "swap only." That swap is fitted to three `hard_dev` fact types that 97 to 99 score again, and it edits found-fact rows. Its other conditions are met: 6.37 retrained, a `hard_dev` floor of 163, fitting disclosed, a first-fail stop. Found-but-wrong counts are reported.
- **Recipe:** met in full: 28 ids, frozen dictionary, no "Your" frame, no rows added or removed, recipe byte for byte, stats' protocol, a stop rule.
- **Dialogue:** met: data's 28, SHA check, no "Your" opener, no question or feeling, the judge's pass needed or the old target stays, the protocol registered first, the disclosure.
- **Stats:** met: 6.37 queued first and alone, pooled sums with ties passing, a fail if 6.37's runs do not finish, a reference of 192 and 163, the four-word filter, the judge, the noise caveat, the disclosure.
- **Against:** met: exactly 28 ids, one blind judge with one rewrite, 6.37's 192 and 163 as floors, 97 to 99 as specified, any fail stops with no 6.39, the "candidate 17" disclosure.

**Recommendation.** No design meets all six item-4 lists as written. Data's 50 rows conflict with recipe, stats and against, and retrieval's swap conflicts with everyone else. This design meets four in full and the rest of data's and retrieval's conditions. Put it to one vote. If data or retrieval votes no, I recommend no 7 rather than a revision, because moving toward either of their versions loses three other votes.

### Critical Files for Implementation
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/data/screens/fix17cs37.jsonl
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/records/build_r122.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/records/build_r110.py (`four_grams`, `TEST_GRAMS`)
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/scripts/run_recall_train.py
- C:/Users/Gaming/Desktop/hackathons/Lexsi Sprint/aya_retrieval/results/vet/R-118/rubric.txt