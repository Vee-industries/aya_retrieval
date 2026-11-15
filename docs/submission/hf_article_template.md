# Teaching a 3B model to search a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

**Result first.** 6.37, a LoRA adapter trained with Lexsi's AgentTune, lets Tiny Aya Global (3.35B) search the part
of a chat it can no longer see. It is strong on chats from the generator that made its training chats and weak on
chats from outside it. On the generator's chats it recalls {{sealed_ship_range}} of {{sealed_recall_n}} facts on a
sealed test, against {{sealed_shipbase_range}} for the untrained model with the same tool. On chats from outside
writers, the untrained model shown the whole chat recalls more, and code that searches every turn recalls as much or
more. On S3, a second sealed test from outside writers, 6.37 also repeats its own wrong answers and names values on
questions it was never told more often than the untrained model. C1, built to fix those two faults, cut both and
missed one clause of a rule fixed before S3 opened by {{s3_gap_points}} points, a gap S3 cannot resolve. **6.37
stays shipped** because no replacement passed the rule, not because it passed S3. C1 is published beside it, labelled.

**Use this when.** The chat was written outside the generator and fits the context: show it whole, no adapter. It is
longer than the model's {{model_max_tokens}}-token window: 6.37 and code that searches every turn show no measured
difference on LongMemEval-S; code is simpler and trains nothing. Both faults matter: C1 measured far lower rates of
both on S3, but missed one registered clause and is not the shipped model.

Adapters: [aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37) (shipped) and
[aya-retrieval-c1](https://huggingface.co/KevinVaillancourt/aya-retrieval-c1). The full write-up,
[docs/ARTICLE.md](https://github.com/Vee-industries/aya_retrieval/blob/main/docs/ARTICLE.md), holds every table, the
candidate ledger, the hypotheses, deviations, leakage and flow tables and the limits; code, results files and
`RECORDS.md`, the dated record (R-001 on), are in
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval). **Author:** I am Kevin
Vaillancourt; every research decision here is mine. **Labels:** *confirmatory* claims rest on a sealed test opened
once (the first sealed test and S3); *exploratory* ones on sets read many times or after the decision they inform.

## 1. The task and what was built

Track 3, problem statement 4: "Fine-tuning for retrieval-augmented generation: Train a model that decides when and
what to retrieve, grounds its answers in the retrieved text and ignores distracting documents." The use: a chat
assistant on a small model that must recall what a user said long ago. Tiny Aya Global takes at most
{{model_max_tokens}} tokens, and {{model_full_layers}} of its {{model_layers}} layers attend to all of them.

The model sees the system prompt, the last three exchanges and the newest message. Everything older is reachable
only through `search_corpus`, AgentTune's SQLite full-text search (top {{top_k}} passages, up to {{max_calls}} calls a
turn). The newest message is a fact told long ago (`older`), "did I tell you...?" (`confirm`), a fact in view
(`in_view`), a fact never told (`never_told`) or plain chat (`statement`). **Recall** is `older` plus `confirm`. Each
chat holds decoys: the same kind of fact about other people. **Threat model:** the adversary is the chat's own
content (decoys, a false claim in a "..., right?" question, the model's own wrong answer in view, a fact never told);
instructions hidden in retrieved passages are not tested.

6.37 is a rank-32 LoRA on all attention and MLP projections, trained on {{training_rows}} rows whose targets are the
untrained model's own passing replies (no teacher model); settings in the long paper's section 4. AgentTune trains it
and supplies the search; CuratorKIT's grounding gate audited an ancestor set ({{curator_v6}} rejected); AuditKIT was a
second scorer in development. Training rows come only from the generator's `train` and `wide` pools; every training
step stops on a four-word run shared with a development set, and S3 shares {{s3_runs_shared}} four-word runs with
6.37's training lines (R-179). No embedding check and no probe of the pretrained model's contamination were run.

## 2. What happened, in order

| Dates (Eastern) | Stage | Records |
|---|---|---|
| 1 to 9 Nov | Test registered before any adapter; {{ledger_total}} candidate sets; 6.37 frozen | R-016 to R-160 |
| 9 to 10 Nov | First sealed test passes; baselines run late; LongMemEval-S; published | R-162 to R-172 |
| 12 Nov | Demo shows two faults; deadline extended; reopened; S3 written and sealed | R-173 to R-179 |
| 12 to 14 Nov | {{reopened_n}} candidates listed for screening; K1.3 the pick, then C1 | R-180 to R-279 |
| 14 Nov | S3 opened once; C1 misses one clause; 6.37 stays shipped | R-280 to R-292 |
| 15 Nov | Two review panels; C1 published beside 6.37 | R-294 to R-298 |

## 3. 6.37's results

**First sealed test (confirmatory).** {{sealed_conversations}} unseen chats from the generator in each of four
conditions, run once on base and all eight seeds. Every registered rule passes: pooled recall
{{sealed_adapters_range}}% against base's {{sealed_base_range}}%; every right answer came from a search that found
the fact; no adapter made more decoy retrievals than base; three judges rated every adapter coherent more often.

![Recall out of view](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/recall_out_of_view.png)

**The strongest baselines (exploratory, registered and run late).** On the generator's chats seed 82 is above both
code that searches every turn and the whole chat: at 58 messages, {{r168_ship58}} of {{r168_recall_n}} against the
whole chat's {{r168_wc}}; at {{long_size}} messages, which fit the window but could not be shown whole under this
project's 10 GB memory cap (R-166), {{long_ship}} against code's {{long_code}}. On two sets of chats by outside writers
(a mean of {{ow_tokens_mean}} tokens), the reading reverses:

| Outside-writer sets (set 1 / set 2) | Base, tool | Code | Base, whole chat | 6.37, tool |
|---|---|---|---|---|
| Recall, of {{as_recall_n}} | {{ow_base_recall_1}} / {{ow_base_recall_2}} | {{as_recall_1}} / {{as_recall_2}} | {{wc_recall_1}} / {{wc_recall_2}} | {{ow_82_recall_1}} / {{ow_82_recall_2}} |
| Answer in view, of {{as_kind_n}} | {{ow_base_in_view_1}} / {{ow_base_in_view_2}} | {{as_in_view_1}} / {{as_in_view_2}} | {{ow_wc_in_view_1}} / {{ow_wc_in_view_2}} | {{ship_in_view_1}} / {{ship_in_view_2}} |

Code shows no measured difference from 6.37 on recall here. 6.37 leaves answers in view alone, where code searches
every turn. Asked "..., right?" with a false claim, it corrects {{claims_82_corrected_1}} and
{{claims_82_corrected_2}} of {{claims_false_n}}, base {{claims_base_corrected_1}} and {{claims_base_corrected_2}}.

**LongMemEval-S (exploratory)**, outside histories far past the window: 6.37 {{lme_j_ship}}, base with the tool
{{lme_j_base}}, code {{lme_j_code}} of a stratified {{lme_judged_n}} of {{lme_questions}}; against code, no measured
difference. 6.37 declines {{lme_refuse_ship}} of {{lme_answerable_n}} answerable questions. Claude judges, not the
official GPT-4o judge.

## 4. The faults, and S3

The scripted demo, run for 6.37 on 12 November (R-175, R-176), showed two faults: asked something it was never told,
it answered with an unrelated stored fact; and it repeated its own wrong answer while that answer was in view. A hand
read of 8 never-told replies on outside set 1 that the scorer counted right found none that declined; each named
another stored fact (R-298). The deadline was then extended, and I reopened the project to fix the faults (R-177).

**The test came before the training.** S3 was written by {{s3_writers}} fresh Claude Opus writers given only a brief:
{{s3_chats}} chats, {{s3_items}} items, hashed before any new training row (R-179). It measures the copy (the model's
earlier wrong value, in view, named when answering another question) and, for the first fault, a value of the asked
category listed for the chat, named on a never-told question whose fixed keyword search returns passages (N-hit).
**The ship rule, fixed before S3 opened** (R-178, R-191): the pick must (a) beat base on recall, lose no more than 5
points on in-view, statement and plain never-told questions, and keep coherence at least base's times 0.95; (b) copy
at most half as often as 6.37 and 10 points less; (c) give at least 10 points fewer N-hit false answers than 6.37, and
no more than base. Its scorer was written after S3 started and before any S3 file was read (R-281).

## 5. The push to replace 6.37

Each candidate was registered before it was built and checked before it trained; the pick had the highest pooled
development recall among those passing 20 lines against base (R-191, R-192). Rows written ahead of time gave K1.3
(R-203). Small stages on K1.3 sat inside run-to-run variation (R-249). Demo2's and Demo3's answers were training
values, so both were retired and replaced (R-254). Training K1.3 on corrections of its own errors gave OP, and the
same stage twice gave C1.

![Demo contamination](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/demo_contamination.png)

**How C1 became the pick.** C1 failed Demo5's fixed older line. I first ruled that a candidate must beat K1.3 on each
demo, and under that ruling C1 failed (R-276, R-277); six minutes later I changed the test to the totals over both
demos (R-278), on which C1 led ({{demos_c1_older}} against {{demos_k13_older}} older; {{demos_c1_never_told}} against
{{demos_k13_never_told}} never-told). My reason (R-283): one demo's six older questions are too few to rank these
models. Both changes came after both models' readings existed. C1 then led K1.3 on development recall,
{{pick_recall_c1}} against {{pick_recall_k13}} (R-279), a lead inside the seed-to-seed spread.

## 6. S3: C1 misses one clause, and 6.37 stays shipped (confirmatory)

{{s3_chats}} chats, 6.37 and C1 pooled over three seeds:

| Measure | Base, tool | 6.37 | 6.37 seed 82 (shipped) | C1 | C1's line |
|---|---|---|---|---|---|
| Recall | {{s3_recall_base}} | {{s3_recall_637}} | {{s3_ship82_recall}} | {{s3_recall_c1}} | (a) pass |
| Copy: names its in-view wrong value | {{s3_copy_base}} | {{s3_copy_637}} | {{s3_ship82_copy}} | {{s3_copy_c1}} | (b) pass |
| N-hit: names a listed value of the asked category | {{s3_nhit_base}} | {{s3_nhit_637}} | {{s3_ship82_nhit}} | {{s3_nhit_c1}} | (c) **fail**: above base |
| Never told, plain: names no listed value | {{s3_ntp_base}} | {{s3_ntp_637}} | {{s3_ship82_ntp}} | {{s3_ntp_c1}} | (a) pass |

![S3 faults](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/s3_faults.png)

C1 missed (c) by {{s3_gap_points}} points; the chat-resampled 95% interval of C1 minus base is {{c1_gap_interval}},
and the lines C1 passed are as unresolved (statements {{s3_a_int_st}}). The registered rule requires every clause, so
6.37 stays shipped. R-294 records my position that the aggregate should have decided; the registered rule was
applied. The published C1, seed 82, is under base on (c) alone but left only {{c1s82_st}} plain statements
unsearched, below (a)'s line: {{c1s82_st_gap}} against base.

On S3, the whole chat recalls {{s3_recall_wc}} and code {{s3_recall_as}}: code recalls more than 6.37
({{s3_code_vs_637}}) and C1 ({{s3_code_vs_c1}}), and is worse than base and C1 on both faults. Report arms K1 and
K2.1 (two seeds, no coherence judging) meet every measured line ({{s3_nhit_k1}} and {{s3_nhit_k21}} on (c));
exploratory, and no arm is swapped in.

## 7. Limits and disclosures

- **What S3's flags count.** The N-hit flag sees only values of the asked category listed for the chat; an invented
  value or another category's stored fact passes. Counting the chat's other stored facts too (exploratory, R-298):
  base {{s3_off_base}}, 6.37 {{s3_off_637}}, C1 {{s3_off_c1}}, C1 seed 82 {{s3_off_c182}}. The registered never-told
  rubric asks for a decline; S3 was scored on its model-free part only, and no judge read those replies (deviation
  20).
- **Rules set after readings**, each in the long paper's deviations table: base replaced 6.37 as the standard of
  (a) after K1's development results (R-191); the demo test changed twice after both models' readings (R-276 to
  R-278); Demo5 was read twice and partly seen through a judge's marks (R-277); S3 replies were partly seen through
  the coherence judges' quotes after the marks were final (R-286).
- **Who judged.** Every judge, writer and panel lane is a Claude model, the same family as the assistant that did the
  work; the only human marker is me, not blind to the hypotheses; the coherence judges were never checked against a
  person, and no person checked S3's flags.
- Development sets were read at every candidate, so development numbers overstate the chosen candidates. One model,
  one size, English only, one 10 GB card, no chat from a real person, no second team. Not run: a general-capability
  benchmark, LoCoMo, a question-shaped router or gated code, a contamination probe (LongMemEval-S predates the model).

## 8. With more credits, reproduce, and who did what

**With more credits.** A sealed test of K1 on a new set of outside chats, under S3's rule, the result expected being
that rule's pass or fail, not a forecast; query writing trained on its own and judged the same way; LoCoMo and chats
past the window against code; a judge applying the full never-told rubric; the whole chat at {{long_size}} messages
on a larger card. The records hold no forecast of recall.

**Reproduce.** The README gives setup and every command; `scripts/make_article.py` fills both write-ups from results
files, except the items section 15 of the long paper lists. Training takes {{train_minutes}} minutes a seed on an RTX
3080; the run files hold {{gpu_total}} GPU hours, on my own card. Tiny Aya Global, the adapters and the data are
CC-BY-NC-4.0; the code is Apache-2.0.

**Who did what.** I directed the work and made every decision in `RECORDS.md`. Claude (Anthropic) wrote the code,
pools, training sets, tests and these write-ups and ran the experiments, as an executive-function accommodation;
other Claude agents wrote the outside-writer chats, S3, the natural training chats and the demos, and judged.
Teammates: none. Before 1 November: only the plan (R-001) and my chat engine LLE, none of it here. Thanks to Lexsi
Labs for AgentTune, AuditKIT, CuratorKIT and the hackathon, and to Cohere Labs for Tiny Aya Global. Changelog: the
long paper's.
