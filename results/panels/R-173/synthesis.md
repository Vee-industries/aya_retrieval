# Panel R-173 synthesis (orchestrator, 2026-11-12 05:05)

Lanes: method (lane_method.md), against (lane_against.md), both claude-opus-5-5, read only the review folder.
Orchestrator checks against the repo: HF_ARTICLE line 29 present-tense AuditKIT (confirmed); CuratorKIT gated
v6's found-fact answers only, ARTICLE lines 250 and 904 (confirmed); outside-writer statement 37 vs 38, 35 vs 39,
ARTICLE line 602 (confirmed); base whole chat recall 71 and 65 of 120, ARTICLE section 6 table (confirmed); seed 82
sealed 91 to 107 of 120 (memory record of R-163, to be confirmed by the sources lane).

## Verdict on the target
Both lanes: 90/100 and 9/10 usefulness are not reachable honestly by presentation. Clarity 8 to 9 is. Usefulness
caps at about 6 to 7 and overall at about 72 to 80, because on outside-writer chats base with the whole chat is
best, code that always searches matches recall and is faster, and on LongMemEval-S 6.37 declines 233 of 470
answerable. Against lane: a reader giving usefulness 9 after these edits signals overstatement. Carried to Kevin.

## Edit spec (method lane's plan, with every against-lane safe version taking precedence)

### Overstatements to fix in every file where they appear
1. AuditKIT: past tense; a second scorer in development (959 of 960 on v3); not run on 6.37. (ABSTRACT line 7,
   HF_ARTICLE line 29, any other.)
2. CuratorKIT: its grounding gate audited v6's 350 found-fact answers (22 rejected); accepted replacements went
   into 6.37's set; the rest of 6.37's 1,094 rows were not gated by it.
3. "85 to 90%" is the eight-seed pool. Where the shipped seed is meant, use seed 82's counts (91 to 107 of 120).
4. "what training adds is deciding when not to search" becomes the against lane's safe sentence: base searches
   too little and code searches every turn; training adds searching when the answer is out of view (against base)
   and not searching when it is in view (against code). Keep the outside-writer statement result (37 vs 38,
   35 vs 39) beside any right-decisions claim.
5. ABSTRACT "For longer chats the adapter matches code": the outside-writer chats are about 1,400 tokens with a
   three-exchange view; say that, and say only LongMemEval-S is long.
6. ABSTRACT LongMemEval sentence: condition first; include answerable 40 vs 32 (p = 0.29) and 40 vs 40 vs code.
7. "declines 13 of the 15": "judged right on 13 of the 15 judged unanswerable; declines 21 of all 30".
8. hf_data_card: blind_dev is not a test set; set 1 became development when 7 was designed from its failures.
9. "One-line fix" for AuditKIT: the project's proposed fix, not adopted upstream.
10. Seed-82 ranges: 46 to 55 at 58 messages (against whole chat); 44 to 55 at both lengths (against code).

### Leave as they are (against lane)
- Coherence rule vs result wording (round 1 item 8): both true.
- Label, do not reconcile: "18 judges' marks" = 6 sheets x 3 judges (checked: results/analysis/R-170/judge has
  brief_L1..L6 x j1..j3); memory 7.81 to 7.84 GiB = 6.37 training peak, 7.12 = v3 under the lean loss, 7.02 =
  sealed-run inference peak. "47 of 71" = judged; "63 of 114" = gold in reply.

### Short write-up (HF_ARTICLE) and README top
1. Lead claim (method lane section 2), amended with points 3 and 4 above.
2. One summary table near the top. Cells: seed 82 where code and whole-chat arms ran against seed 82; "not
   measured (does not fit 10 GB)" where an arm did not run; by-construction cells marked; LongMemEval-S gets
   judged-right, answerable-only and declines-on-answerable rows. Outside-writer recall row first, with base
   whole chat (71, 65 of 120) shown as the strongest arm.
3. "Which to use when" in three lines (model card's rule).
4. Track table with a result column.
5. Tool calls paragraph: definition of a clean call, both denominators, and whether unclean calls still ran.
6. Prompted baseline: "for these two prompts".
7. Toolkit chain paragraph: AgentTune trains; CuratorKIT on v6's answers; AuditKIT in development, not on 6.37,
   bootstrap defect with the project's proposed fix; TRL loss fix (v3 figures, labelled).
8. "Kevin" becomes "I" (voice spec first person singular). On the human checks: "I (the author, not an
   independent marker)".
9. Record ids: keep inline on every registration, deviation, post-hoc and limitation sentence; move the rest to a
   "Records:" line per section. Define base, code, recall, judge 1, clean call, seed 82 at first use.
10. LongMemEval-S: denominators once; refusal first; gold-answer row 63 vs 51 of 411.
11. Cost: three-row table; closed-model line per Kevin's decision (default: "No comparison with closed models was
    made."); models collection link.
12. Access line: adapter and datasets public and un-gated (verify on the Hub from outside first); the base model
    is gated, so users accept Tiny Aya's licence.

### Long write-up (article_template.md via make_article.py)
1. Abstract slot: the form abstract's text, then a short limits paragraph keeping all four of: seed 82 set 1
   p = 0.047 above the registered 0.01; seed 82 lowest of the eight seeds; tag questions corrected 1 and 3 of 20;
   coherence judges never checked against a person.
2. The summary table and both figures right after; a glossary of up to 12 terms after the table.
3. Ids: out of the abstract, section 1 and each section's first paragraph, except registration, deviation,
   post-hoc and limitation sentences; kept in tables and sections 11 to 14.
4. Split wide tables by set, not by arm.
5. Section 11 opens with the noise sentence and the 40 candidates screened on reused development pools.
6. Section 14 one opening sentence; section 4 toolkit table ("AuditKIT: no; CuratorKIT: on an ancestor set only");
   section 5 summary: "Ten deviations; three found by the write-up's reviewer and first disclosed in R-167; none
   changes a pass rule." (sources lane to confirm the counts).
7. Memory labels as above.

### Model card template, dataset cards
- Model card: summary table, dataset and collection links, gated-base line, scorer caveat restated in Limitations,
  "Kevin" -> "I". No untested snippet.
- Dataset cards: field list, one sample row (never from sealed pools or LongMemEval text), a loading line tested
  from outside, a number-to-file table, whether heldout and independent are published and how to rebuild them
  (item seed 90311), both human checkers named with their records, the 18-judge-run label.

## Next scoring round (against lane design, adopted)
At least 4 fresh readers, Opus and Sonnet (only Claude models are available here; disclosed). Each scores the old
and the new version blind to which is which. They get the hackathon's published criteria, the repository for code
quality, a skim budget for the short write-up, an overstatement list and a fixed factual quiz. Rule registered
before reading: clarity rises; the overstatement count does not rise; quiz right answers do not fall. Scores
reported as they come.

## Amendments from the sources lane (lane_sources.md, claude-sonnet-5-5), 2026-11-12 05:20
Every number in the edit spec is CONFIRMED in lane_sources.md section 1 except these, which override the spec:
- Deviations first disclosed in R-167: FOUR (items 7 to 10), not three. Summary line: "Ten deviations; four first
  disclosed in R-167 after the write-up's review; none changes a pass rule."
- Base tokens read a turn: 1,122 to 1,154 (the method lane wrote 1,148 to 1,154).
- The 9.81 to 7.12 GiB pair is an early development run (R-029), not 6.37 and not v3. Label it so. 6.37 trained
  at 7.81 to 7.84 GiB, already under the lean loss.
- Clean call = the reply parses whole as one search_corpus call with nothing before or after it. Denominator =
  replies that searched (so 180 vs 136 are different populations). Unclean calls still ran their search. It is a
  format measure; say so wherever the count appears.
- Human checks: R-144 the author (47 of 50 with the scorer); R-145 a second marker, unnamed, the only independent
  human (48 of 50 with the scorer, 49 of 50 with the author). The 50 lines are from development pools (probe,
  hard_dev), not sealed or outside-writer chats; say so.
- Sealed pools: not a HF dataset, but public as source in the repo (pools.py, pool_independent.py,
  docs/independent_pool/); rebuilt by scripts/run_recall_eval.py --pool heldout|independent --final
  --items-per-kind 30 --decoys 1|4, item seed 90311 (flag name unverified: the builder checks --help).
  The sealed runs' replies are published in the eval-logs dataset (results/recall_eval/final_*).
- Gate status checked by the orchestrator 2026-11-12 with no login via the HF API: adapter and both datasets
  gated=False private=False; CohereLabs/tiny-aya-global gated=auto.
- make_article.py never keys on record ids, but hard-codes ids and "Kevin" in generated strings (human_check,
  status line, ledger rows, captions): edit those strings too, or the rebuild puts them back.
- Present-tense AuditKIT: ABSTRACT 7, HF_ARTICLE 30, README 241-242. CuratorKIT "the training answers" without
  scope: ABSTRACT 7, HF_ARTICLE 31, README 243, hf_data_card 85.
- RECORDS R-170 itself prints p = 0.015 and "all of the lead from unanswerable"; R-171 already corrected both.
  Records stay as written (append-only); no edit.
