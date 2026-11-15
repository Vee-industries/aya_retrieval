# Teaching a 3B model to search a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

**Result first.** 6.37, a LoRA adapter trained with Lexsi's AgentTune, lets Tiny Aya Global (3.35B) search the part
of a chat it can no longer see. On a sealed test of chats from the generator that made its training chats, the shipped
seed recalls {{sealed_ship_range}} of {{sealed_recall_n}} facts, against {{sealed_shipbase_range}} for the untrained
model with the same tool. On two sets of chats from outside writers it recalls {{ow_82_recall_1}} and
{{ow_82_recall_2}} of {{as_recall_n}}; the whole chat recalls more and code that searches every turn shows no measured
difference. On S3, a second sealed test from outside writers, code recalls more, and 6.37 repeats its own wrong
answers and names values on never-told questions more often than the untrained model. C1 cut both faults and missed
one clause of a rule fixed before S3 opened, by {{s3_gap_points}} points, a gap S3 cannot resolve. **6.37 stays
shipped** because no replacement passed the rule, not because it passed S3. C1 is published beside it, labelled.

**Use this when.** If the chat was written outside the generator and fits the context, show it whole, with no
adapter; on S3 the whole chat names a listed value on {{s3_nhit_wc}} never-told N-hit questions, against base with the
tool's {{s3_nhit_base}}, and names no listed value on {{s3_ntp_wc}} plain never-told questions, against
{{s3_ntp_base}}. If the chat is longer than the model's {{model_max_tokens}}-token window, 6.37 and code show no
measured difference on LongMemEval-S answers, code's first search finds the evidence more often ({{lme_h2_code}};
registered H2, R-170), and code needs no training. If both faults matter: 6.37 is shipped by the registered rule; for
the two faults, C1 measured lower rates ({{s3_rel_copy}} on copies, {{s3_rel_nhit}} on N-hit false answers).

Adapters: [aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37) (shipped) and
[aya-retrieval-c1](https://huggingface.co/KevinVaillancourt/aya-retrieval-c1). Datasets:
[aya-retrieval-chats](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-chats) and
[aya-retrieval-eval-logs](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-eval-logs), in the
[models](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-models-6af35d3c521e8481db061df5) and
[datasets](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-datasets-6af35d3cf9a91556f52af373)
collections. The full write-up,
[docs/ARTICLE.md](https://github.com/Vee-industries/aya_retrieval/blob/main/docs/ARTICLE.md), holds every table and
limit; code, results files and `RECORDS.md`, the dated record, are in
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval). **Author:** I am Kevin
Vaillancourt; every research decision here is mine. **Labels:** *confirmatory* claims rest on a sealed test opened
once (the first sealed test and S3); *exploratory* ones on sets read many times or after the decision they inform.

**Terms.** *Base*: the untrained model. *Code*: base handed the passages of a search on every turn, the newest
message as the query. *Whole chat*: base with every message in view, no tool. *Recall*: right answers on facts told
long ago and "did I tell you...?" questions; "of {{sealed_recall_n}}" counts those questions in a run. *Never told*:
the chat never held the fact; right when the reply names no listed value. *Copy* (S3): naming its own earlier wrong
value, in view, when answering another question. *N-hit* (S3): a never-told question whose fixed keyword search
returns passages; an N-hit false answer names a value listed for the chat. *K1, K1.3, OP, C1*: reopened candidates,
each built on the last (K1.3 restates K1's facts in other wordings; OP trains on corrections of its own errors; C1
repeats OP's stage). *Demo2 to Demo5*: one-chat screening demos. *No measured difference*: the 95% interval of the
difference includes zero.

## 1. The task and what was built

Track 3, problem statement 4: "Fine-tuning for retrieval-augmented generation: Train a model that decides when and
what to retrieve, grounds its answers in the retrieved text and ignores distracting documents." The use: a chat
assistant on a small model that must recall what a user said long ago. Tiny Aya Global takes at most
{{model_max_tokens}} tokens, and {{model_full_layers}} of its {{model_layers}} layers attend to all of them.

The model sees the system prompt, the last three exchanges and the newest message. Everything older is reachable
only through `search_corpus`, AgentTune's SQLite full-text search (top {{top_k}} passages, up to {{max_calls}} calls a
turn). The newest message asks for a fact told long ago (`older`), asks "did I tell you...?" (`confirm`), or is a
fact in view, a fact never told or plain chat. Each chat holds decoys: the same kind of fact about other people.
**Threat model:** the adversary is the chat's own content (decoys, a false claim in a "..., right?" question, the
model's own wrong answer in view, a fact never told).

The statement's four clauses, for 6.37:

- **When** to retrieve: met for answers in view and plain statements; not for "did I tell you...?" (S3: searched on
  {{s3_conf_637}} by seed).
- **What** to retrieve: met on generated chats; on S3 its queries found the fact on {{s3_found_637}} recall questions,
  code's raw message on {{s3_found_as}}.
- **Grounds**: met on the first sealed test; on S3 it answered {{s3_ground_637}} of the questions its search found
  right, as often as base on code's passages, {{s3_ground_as}}.
- **Ignores distracting documents**: met for decoys in generated chats; not on S3 (sections 4 and 6).

6.37 is a rank-32 LoRA on all attention and MLP projections, trained on {{training_rows}} rows from the generator's
`train` pool (R-075) whose targets are the untrained model's own passing replies. AgentTune trains it and supplies the
search; CuratorKIT's grounding gate audited an ancestor set ({{curator_v6}} rejected); AuditKIT was a development
scorer. S3 shares {{s3_runs_shared}} four-word runs with 6.37's training lines (R-179).

## 2. What happened, in order

| Dates (Eastern) | Stage | Records |
|---|---|---|
| 1 to 9 Nov | Test registered before any adapter; {{ledger_total}} candidate sets; 6.37 frozen | R-016 to R-160 |
| 9 to 10 Nov | First sealed test passes; baselines run late; LongMemEval-S; published | R-162 to R-172 |
| 12 Nov | Demo shows two faults; deadline extended; reopened; S3 written and sealed | R-173 to R-179 |
| 12 to 14 Nov | {{reopened_n}} candidates listed for screening; K1.3 the pick, then C1 | R-180 to R-279 |
| 14 Nov | S3 opened once; C1 misses one clause; 6.37 stays shipped | R-280 to R-293 |
| 15 Nov | Review panels; C1 published beside 6.37; audit; appendices; a third review round | R-294 to R-301 |

## 3. 6.37's results

**First sealed test (confirmatory).** {{sealed_conversations}} unseen chats from the generator in each of four
conditions, run once on base and all eight seeds. Every registered rule passes: pooled recall
{{sealed_adapters_range}}% against base's {{sealed_base_range}}%; every right answer came from a search that found
the fact; no adapter made more decoy retrievals than base; three judges rated every adapter coherent more often.

![Recall out of view](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/recall_out_of_view.png)

*Figure 1. Recall with three exchanges in view, base against 6.37's eight seeds pooled (small dots: each seed); the
table below gives the shipped seed alone.*

**The strongest baselines (exploratory, registered and run late).** On the generator's chats seed 82 is above both
code and the whole chat: at 58 messages, {{r168_ship58}} of {{r168_recall_n}} against the whole chat's {{r168_wc}};
at {{long_size}} messages (inside the window, too long to show whole on the 10 GB card, R-166), {{long_ship}} against
code's {{long_code}}. On two sets of chats by outside writers (a mean of {{ow_tokens_mean}} tokens), the reading
reverses:

| Outside-writer sets (set 1 / set 2) | Base, tool | Code | Base, whole chat | 6.37 seed 82, tool |
|---|---|---|---|---|
| Recall, of {{as_recall_n}} | {{ow_base_recall_1}} / {{ow_base_recall_2}} | {{as_recall_1}} / {{as_recall_2}} | {{wc_recall_1}} / {{wc_recall_2}} | {{ow_82_recall_1}} / {{ow_82_recall_2}} |
| Answer in view, of {{as_kind_n}} | {{ow_base_in_view_1}} / {{ow_base_in_view_2}} | {{as_in_view_1}} / {{as_in_view_2}} | {{ow_wc_in_view_1}} / {{ow_wc_in_view_2}} | {{ship_in_view_1}} / {{ship_in_view_2}} |

Code shows no measured difference from 6.37 on recall here; 6.37 leaves answers in view alone, where code searches
every turn.

**LongMemEval-S (exploratory)**, histories past the window: judged right (Claude judges, not the official GPT-4o
judge), 6.37 {{lme_j_ship}}, base with the tool {{lme_j_base}}, code {{lme_j_code}} of a stratified {{lme_judged_n}}.
Registered H2 (R-170): no measured difference from code on answers; code's first search finds the evidence more
often, {{lme_h2_code}}. 6.37 declines {{lme_refuse_ship}} of {{lme_answerable_n}} answerable questions.

## 4. The faults, and S3

The scripted demo, run for 6.37 on 12 November (R-175, R-176), showed two faults: asked something it was never told,
it answered with an unrelated stored fact; and it repeated its own wrong answer while that answer was in view. The
deadline was then extended, and I reopened the project to fix the faults (R-177).

**The test came before the training.** S3 was written by {{s3_writers}} fresh Claude Opus writers given only a brief:
{{s3_chats}} chats, {{s3_items}} items, hashed before any new training row (R-179). **The ship rule, fixed before S3
opened** (R-178, R-191). The pick must:

- (a) beat base on recall, lose no more than 5 points against base on in-view, statement and plain never-told
  questions, and keep coherence at least base's times 0.95;
- (b) copy both at most half as often as 6.37 and at least 10 points less;
- (c) give at least 10 points fewer N-hit false answers than 6.37, and no more than base.

Its scorer was written after S3 started and before any S3 file was read (R-281).

## 5. The push to replace 6.37

Each candidate was registered before it was built; the pick had the highest pooled development recall among those
passing 20 lines against base (R-191, R-192). K1.3 was the pick from R-203. Demo2's and Demo3's answers were training
values, so both were replaced by Demo4 and Demo5 (R-254; Figure 2).

**How C1 became the pick.** C1 failed Demo5's fixed older line. I first ruled that a candidate must beat K1.3 on each
demo, and C1 failed (R-276, R-277); six minutes later I changed the test to the totals over both demos (R-278), on
which C1 led ({{demos_c1_older}} against {{demos_k13_older}} older; {{demos_c1_never_told}} against
{{demos_k13_never_told}} never-told). My reason (R-283): one demo's six older questions are too few to rank these
models. Both changes came after both models' readings existed. C1 then led K1.3 on development recall,
{{pick_recall_c1}} against {{pick_recall_k13}} (R-279), a lead inside the seed-to-seed spread.

![Demo contamination](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/demo_contamination.png)

*Figure 2. Demo answer keys that are fact values in the training data, by demo (8 keyed questions each; R-254).*

## 6. S3: C1 misses one clause, and 6.37 stays shipped (confirmatory)

{{s3_chats}} chats, 6.37 and C1 pooled over three seeds:

| Measure | Base, tool | 6.37 | 6.37 seed 82 (shipped) | C1 | C1's line |
|---|---|---|---|---|---|
| Recall | {{s3_recall_base}} | {{s3_recall_637}} | {{s3_ship82_recall}} | {{s3_recall_c1}} | (a) pass |
| Copy: names its in-view wrong value | {{s3_copy_base}} | {{s3_copy_637}} | {{s3_ship82_copy}} | {{s3_copy_c1}} | (b) pass |
| N-hit: names a listed value of the asked category | {{s3_nhit_base}} | {{s3_nhit_637}} | {{s3_ship82_nhit}} | {{s3_nhit_c1}} | (c) **fail**: above base |
| Never told, plain: names no listed value | {{s3_ntp_base}} | {{s3_ntp_637}} | {{s3_ship82_ntp}} | {{s3_ntp_c1}} | (a) pass |

![S3 faults](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/s3_faults.png)

*Figure 3. The two faults on S3 by arm, lower is better, with 95% intervals over chats; grey band: base with the tool.
6.37 and C1 pool three seeds; report arms pool seeds 82 and 83.*

C1 missed (c) by {{s3_gap_points}} points; the chat-resampled 95% interval of C1 minus base is {{c1_gap_interval}},
and the lines C1 passed are as unresolved (statements {{s3_a_int_st}}). The rule requires every clause, so 6.37 stays
shipped; R-294 records my position that the aggregate should have decided. The published C1, seed 82, is under base
on (c) but fails (a)'s statement line: it left {{c1s82_st}} plain statements unsearched, {{c1s82_st_gap}} against
base.

On S3, the whole chat recalls {{s3_recall_wc}} and code {{s3_recall_as}}: code recalls more than 6.37
({{s3_code_vs_637}}) and C1 ({{s3_code_vs_c1}}), and is worse than base and C1 on both faults. Query writing is a
measured cause (exploratory): code's raw message found the fact where seed 82's queries did not on
{{s3_qw_code_only_637}} recall questions, the reverse on {{s3_qw_own_only_637}} (C1 seed 82: {{s3_qw_code_only_c1}}
and {{s3_qw_own_only_c1}}). Report arms K1 and K2.1 (two seeds, no coherence judging) meet every measured line,
naming a listed value on {{s3_nhit_k1}} and {{s3_nhit_k21}}; K1.3, the pick before C1, fails (c) on
{{s3_nhit_k13}}. Exploratory; no arm is swapped in.

## 7. Limits and disclosures

- **What S3's flags count.** Only values of the asked category listed for the chat; an invented value or another
  category's stored fact passes, so the plain never-told rates of base, 6.37 and C1 are ceilings. Counting other
  stored facts too, N-hit questions answered with a value (exploratory, R-298): base {{s3_off_base}}, 6.37
  {{s3_off_637}}, C1 {{s3_off_c1}}. S3 was scored on the never-told rubric's model-free part only (deviation 20).
- **Rules set after readings** (the long paper's deviations table): base replaced 6.37 as the standard of (a) after
  K1's development results (R-191); the demo test changed twice (R-276 to R-278); Demo5 was read twice, partly
  through a judge's marks (R-277); judges' quotes showed parts of S3 replies after the marks were final (R-286).
- **Who judged.** Every judge, writer and panel lane is a Claude model, the same family as the assistant that did the
  work. Two people marked 50 development scorer lines: me, not blind to the hypotheses, and one independent marker
  (R-144, R-145); no person checked S3's flags or the coherence judges.
- **Not tested: instructions hidden in retrieved passages.** A value given as something the user said, when the user
  never said it, is a false memory the user may act on.
- Development numbers overstate the chosen candidates. One model, one size, English only, one 10 GB card, no chat from
  a real person, no second team. Not run: a general-capability benchmark, LoCoMo, a question-shaped router, a
  contamination probe (LongMemEval-S predates the model).

## 8. With more credits, reproduce, and who did what

**With more credits.** A sealed test of K1 on a new set of outside chats under S3's rule; query writing trained on its
own and judged the same way; LoCoMo and chats past the window against code; a judge applying the full never-told
rubric; the whole chat at {{long_size}} messages on a larger card.

**The expectation in hand** (exploratory). K1's S3 report arm (two seeds) reads recall {{s3_recall_k1}}, copies
{{s3_copy_k1}} and a listed value named on {{s3_nhit_k1}} never-told questions, against base's {{s3_nhit_base}}; a
sealed test of K1 passes or fails on S3's rule as registered.

**Reproduce.** The README gives every command; `scripts/make_article.py` fills the write-ups from results files,
except the items the long paper's section 15 lists. Training takes {{train_minutes}} minutes a seed on an RTX 3080;
the run files hold {{gpu_total}} GPU hours, on my own card. Tiny Aya Global, the adapters and the data are
CC-BY-NC-4.0; the code is Apache-2.0.

**Who did what.** I directed the work and made every decision in `RECORDS.md`. Claude (Anthropic) wrote the code,
data, tests and these write-ups and ran the experiments, as an executive-function accommodation; other Claude agents
wrote the outside-writer chats, S3 and the demos, and judged. Teammates: none. Before 1 November: only the plan
(R-001) and my chat engine LLE, none of it here. Thanks to Lexsi Labs and Cohere Labs.
