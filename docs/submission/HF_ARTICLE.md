# Teaching a 3B model to search a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

**Claim.** On a sealed test of chats from its training generator, 6.37 makes Tiny Aya Global recall
91 to 107 of 120 out-of-view facts, against the untrained model's
13 to 32. On chats from outside writers (Claude agents) it does not beat the strongest simple baselines,
and on S3 it repeats its own wrong answers and names listed values on never-told questions more often than the
untrained model.

**Result first.** 6.37, a LoRA adapter trained with Lexsi's AgentTune, lets Tiny Aya Global (3.35B) search the part
of a chat it can no longer see. On two sets of chats from outside writers it recalls 39 and
53 of 120; the whole chat recalls more than 6.37, and code shows no measured difference
from it. On S3, a second sealed test
from outside writers, code recalls more, and 6.37 repeats its own wrong answers and names listed values on never-told
questions more often than the untrained model. C1 cut both faults. It missed one clause of a rule fixed before S3
opened, by 1.3 points, a gap S3 cannot resolve. **6.37 stays shipped** because no replacement passed the
rule, not because it passed S3. C1 is published beside it, labelled.

**Terms.**

- *Base*: the untrained model. *Code*: base handed a search's passages every turn, the newest message as the query.
  *Whole chat*: base with every message in view, no tool.
- *Recall*: right `older` and `confirm` answers (section 1), "of 120" in a run. *Never told*: the chat
  never held the fact; right when the reply names no listed value. *N-hit* (S3): a never-told question whose fixed
  keyword search returns passages; an N-hit false answer names a value listed for the chat (of the asked category, or a writer's listed wrong value). *Copy* (S3): naming its
  own in-view wrong value when answering another question.
- *K1, K1.3, C1*: reopened candidates, each built on the last; C1 trains on corrections of its own errors. *Demo2 to
  Demo5*: one-chat screening demos.
- *No measured difference*: the 95% interval of the difference includes zero, or a sign test gives p of 0.05 or more.

**Use this when.** For an outside chat that fits the context, show base the whole chat; on S3 it names a listed value on 57 of 236 (24.2%) N-hit questions, more than base with the tool's
14 of 236 (5.9%), and no listed value on 89 of 120 (74.2%) plain never-told ones, against base's 111 of 120 (92.5%). Past
the 8,192-token window, code needs no training, shows no measured difference from 6.37 on LongMemEval-S
answers and finds the evidence more often (372 against 333 of 476; registered H2), but on S3 copies on 65 of 298 (21.8%) and
gives 121 of 236 (51.3%) N-hit false answers, against base's 11 of 298 (3.7%) and 14 of 236 (5.9%); neither fault was
measured past the window. If both faults matter, do not use 6.37: on S3 it is worse than base on both. C1 is
lower than 6.37 (-97% copies, -82% N-hit false answers) but is not below base on N-hit
(51 of 708 (7.2%)).

Adapters: [aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37) (shipped) and
[aya-retrieval-c1](https://huggingface.co/KevinVaillancourt/aya-retrieval-c1). Datasets:
[aya-retrieval-chats](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-chats) and
[aya-retrieval-eval-logs](https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-eval-logs), in the
[models](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-models-6af35d3c521e8481db061df5) and
[datasets](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-datasets-6af35d3cf9a91556f52af373)
collections. The full write-up,
[docs/ARTICLE.md](https://github.com/Vee-industries/aya_retrieval/blob/main/docs/ARTICLE.md), holds every table and
limit (metrics: section 5; data, splits and trajectories: section 3); code, results
files and `RECORDS.md`, the dated record, are in
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval). **Author:** I am Kevin
Vaillancourt; every research decision here is mine. **Labels:** *confirmatory* claims rest on the two sealed tests,
each opened once; *exploratory* ones on sets read many times or after the decision they inform.

## 1. The task and what was built

Track 3, problem statement 4: "Fine-tuning for retrieval-augmented generation: Train a model that decides when and
what to retrieve, grounds its answers in the retrieved text and ignores distracting documents." The use: a small-model chat
assistant recalling what a user said long ago. The base model is
`CohereLabs/tiny-aya-global`, revision `af89d219b53ed9b13b8a4645f9c8028973510324`.

The model sees the system prompt, the last three exchanges and the newest message. Everything older is reachable
only through `search_corpus`, AgentTune's SQLite full-text search (top 5 passages, up to 3 calls a
turn). The newest message asks for a fact told long ago (`older`), asks "did I tell you...?" (`confirm`; on S3 "..., right?",
30 of 58 a true claim holding the answer), or is a fact in view, a fact never
told or plain chat. Each chat holds decoys: the same kind of fact about others. **Threat model:** the
adversary is the chat's own content (decoys, a false claim in a "..., right?" question, the model's own wrong answer
in view, a fact never told). A value the user never said, given as the user's, is a false memory.

The statement's four clauses, for 6.37:

- **When** to retrieve: met for answers in view and plain statements; not for "did I tell you...?" (S3: searched on
  7, 0 and 5 of 58 by seed). On S3 code makes more right search decisions (714 of 834) than
  any 6.37 seed (682, 666 and 670 of 834).
- **What** to retrieve: met on generated chats; on S3 its queries found the fact on 480 of 1,242 (38.6%) recall questions,
  code's raw message on 260 of 414 (62.8%).
- **Grounds** (answers from found text): met on the first sealed test; on S3, of 119 recall
  questions both seed 82's and code's searches found, seed 82 answered 65 right, base on code's
  passages 84 (p = 0.0026, exploratory).
- **Ignores distracting documents**: met for decoys in generated chats; not on S3 (sections 4 and 6).

6.37 is a rank-32 LoRA on all attention and MLP projections, trained on 1,094 rows from the generator's
`train` pool (R-075) whose targets are the untrained model's own passing replies. **How the kits connect:** AgentTune
trains it and supplies the search; CuratorKIT's grounding gate audited an ancestor set (22 of 350 rejected);
AuditKIT was a development scorer. S3 shares 140 of 42,561 four-word runs with 6.37's training lines (R-179).

## 2. What happened, in order

| Dates (Eastern) | Stage | Records |
|---|---|---|
| 1 to 9 Nov | Test registered before any adapter; 40 candidate sets; 6.37 frozen | R-016 to R-160 |
| 9 to 10 Nov | First sealed test passes; late baselines; LongMemEval-S; published | R-162 to R-172 |
| 12 Nov | Demo shows two faults; reopened; S3 written and sealed | R-173 to R-179 |
| 12 to 14 Nov | 24 candidates listed; K1.3 the pick, then C1 | R-180 to R-279 |
| 14 Nov | S3 opened once; C1 misses one clause; 6.37 stays shipped | R-280 to R-293 |
| 15 Nov | Review panels and audits; C1 published beside 6.37 | R-294 to R-313 |

R-304: two private names that a sweep record had named were removed from the whole history; every commit from 10
November on has a new id (map in `results/scrub/`).

## 3. 6.37's results

**First sealed test (confirmatory).** 300 unseen chats from the generator in each of four
conditions (Figure 1), run once on base and all eight seeds. Every registered rule passes: pooled recall
85.2 to 90.4% against base's 8.3 to 28.3%; every right answer came from a search that found
the fact; no adapter made more decoy retrievals than base; three judges rated every adapter coherent more often.

![6.37 above base on every row](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/recall_out_of_view.png)

*Figure 1. Recall, three exchanges in view: base against 6.37's eight seeds pooled (small dots: each seed); point
counts, no interval.*

**The strongest baselines (exploratory, registered and run late).** On the generator's chats seed 82 is above both
code and the whole chat: at 58 messages, 46 to 55 of 60 against the whole chat's 21 to 33;
at 419 messages (too long for the 10 GB card, R-166), 52, 52, 46 and 44 against
code's 32, 30, 17 and 14. On two sets of chats by outside writers (a mean of 1,400 tokens), the reading
reverses:

| Outside-writer sets (set 1 / set 2) | Base, tool | Code | Base, whole chat | 6.37 seed 82, tool |
|---|---|---|---|---|
| Recall, of 120 | 26 / 27 | 42 / 47 | 71 / 65 | 39 / 53 |
| Answer in view, of 40 | 36 / 34 | 13 / 16 | 35 / 32 | 35 / 37 |

**LongMemEval-S (exploratory)**, histories past the window: judged right (Claude judges, not the official GPT-4o), 6.37 53, base with the tool 34, code 40 of a stratified 248.
Registered H2 (R-170): code's first search finds more evidence, 372 against 333 of 476, with no measured difference on
answers. Split after reading that result: on the 233 answerable questions of the
248, 6.37 and code have the same count (40 against 40; 23 right only for 6.37 and 23 only for code that always searches, p = 1.0); its higher count than code comes only from the 15
unanswerable ones. Of all 470 answerable questions, 6.37 declines 233.

## 4. The faults, and S3

The scripted demo, run for 6.37 on 12 November (R-175, R-176), showed two faults: asked something it was never told,
it gave an unrelated stored fact; and it repeated its own wrong answer while in view. With
the deadline reported extended (R-173), I saw results I had missed and judged the extra time enough to train further,
so I reopened the project to fix the faults (R-177).

**The test came before the training.** S3 was written by six fresh Claude Opus writers given only a brief:
60 chats, 834 items, hashed before any new training row (R-179). **The ship rule, fixed before S3
opened** (R-178, R-191). The pick must:

- (a) beat base on recall, lose no more than 5 points against base on in-view, statement and plain never-told
  questions, and keep coherence at least base's times 0.95;
- (b) copy at most half as often as 6.37 and at least 10 points less than it;
- (c) give at least 10 points fewer N-hit false answers than 6.37, and no more than base.

Its scorer was written after S3 started, before any S3 file was read (R-281).

## 5. The push to replace 6.37

Each candidate was registered before it was built; the pick had the highest pooled development recall among those
passing 20 lines against base (R-191, R-192). K1.3 was the pick from R-203, ahead of K1, 742 to
720, inside the seed spread. Demo2's and Demo3's answers were training values,
so both were replaced by Demo4 and Demo5 (R-254; Figure 2).

**How C1 became the pick.** C1 failed Demo5's fixed older line. I first ruled that a candidate must beat K1.3 on each
demo, and C1 failed (R-276, R-277); six minutes later I changed the test to the totals over both demos (R-278), on
which C1 led (5 of 12 against 4 of 12 older; 6 of 8 against
5 of 8 never-told). My reason (R-283): one demo's six older questions are too few to rank these
models. The first change came after both of C1's demo readings and K1.3's Demo4 reading, and ordered K1.3's Demo5
reading knowing C1's; the second came after all four. C1 then led K1.3 on development recall, 775
against 742 of 1,296 (R-279), inside the seed spread.

![Demo2 and Demo3 keys were training values](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/demo_contamination.png)

*Figure 2. Demo answer keys that are fact values in the training data, by demo (8 keyed questions each; R-254).*

## 6. S3: C1 misses one clause, and 6.37 stays shipped (confirmatory)

60 chats, 6.37 and C1 pooled over three seeds:

| Measure | Base, tool | 6.37 | 6.37 seed 82 (shipped) | C1 | C1's line |
|---|---|---|---|---|---|
| Recall | 59 of 414 (14.3%) | 347 of 1,242 (27.9%) | 99 of 414 (23.9%) | 364 of 1,242 (29.3%) | (a) pass |
| Copy: names its in-view wrong value | 11 of 298 (3.7%) | 195 of 894 (21.8%) | 62 of 298 (20.8%) | 5 of 894 (0.6%) | (b) pass |
| N-hit: names a listed value of the asked category | 14 of 236 (5.9%) | 286 of 708 (40.4%) | 100 of 236 (42.4%) | 51 of 708 (7.2%) | (c) **fail**: above base |
| Never told, plain: names no listed value | 111 of 120 (92.5%) | 238 of 360 (66.1%) | 76 of 120 (63.3%) | 344 of 360 (95.6%) | (a) pass |
| False claim in a tag question: corrected | 1 of 28 | 0 of 84 | 0 of 28 | 32 of 84 | none |

`older` alone, with no answer cue in the question (exploratory; 6.37 and C1 three seeds pooled): base
30 of 356 (8.4%), 6.37 285 of 1,068 (26.7%), C1 292 of 1,068 (27.3%).

![6.37 above base on both faults](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/s3_faults.png)

*Figure 3. The two faults on S3 by arm, lower is better; 95% intervals resample chats; grey band: base's interval;
thin line (right): base's rate, clause (c)'s line. Report arms: seeds 82 and 83.*

C1 missed (c) by 1.3 points (Figure 3); the chat-resampled 95% interval of C1 minus base is -3.1 to +5.7 points.
Counting every stored value the chat holds, not only listed values of the asked category, N-hit questions answered
with a value (exploratory, R-298): base 17 of 236 (7.2%), 6.37 402 of 708 (56.8%), C1 99 of 708 (14.0%).
The rule requires every clause, so 6.37 stays
shipped; R-294 records my position that the aggregate should have decided. The published C1, seed 82, is under base
on (c) but fails (a)'s statement line: it left 50 of 60 (83.3%) plain statements unsearched, -13.3 points, 95% interval -23.3 to -3.3 against
base.

On S3 (exploratory, beside the rule, not part of it), the whole chat recalls 274 of 414 (66.2%) and code 161 of 414 (38.9%): code recalls more than 6.37
(+11.0 points, 95% interval +3.5 to +18.6) and C1 (+9.6 points, 95% interval +2.4 to +16.6). Query writing is the likeliest cause (exploratory; seed 82 ran
at most one search an item, so its comparison is one search against one; C1 seed 82 ran more than one on
89 of 834, so its counts do not isolate the query): where both searched, code's raw message found
the fact where seed 82's queries did not on 88 recall questions, the reverse on
22; of the 67 seed 82 did not search, code's search found it on
53 (C1 seed 82: 100, 29, and 6 of
11). Report
arms K1 and K2.1 (two seeds, no coherence judging) meet every measured line,
naming a listed value on 12 of 472 (2.5%) and 14 of 472 (3.0%); K1.3, the pick before C1, fails (c) on
37 of 472 (7.8%). Exploratory; none swapped in. I picked on development recall, under a development false-answer gate
that compared with 6.37, not with base (R-191); the development screen and the demos did not predict S3 on that line.

## 7. Limits and disclosures

- **What S3's flags count.** Only values listed for the chat (of the asked category, or a writer's listed wrong
  value); any other invented value or another
  category's stored fact passes, so the plain never-told rates of base, 6.37 and C1 are ceilings: replies with no
  value at all can be fewer (section 6 counts the other stored facts). S3 was scored on the never-told rubric's model-free part only (deviation 20).
- **Rules set after readings** (deviations table, long paper): base replaced 6.37 as the standard of (a) after
  K1's development results (R-191); the demo test, twice (section 5); Demo5 was read twice, partly through a judge's
  marks (R-277); judges' quotes showed parts of S3 replies after the marks were final (R-286).
- **Who judged.** Every judge, writer and panel lane is a Claude model, the same family as the assistant that did the
  work. Two people marked 50 development scorer lines: me, not blind to the hypotheses, and one independent marker
  (R-144, R-145); no person checked S3's flags or the coherence judges.
- **Not tested: instructions hidden in retrieved passages.**
- Development numbers overstate the chosen candidates; each baseline ran in one setting, 6.37 came from
  40 trained candidate sets. One model, one size, English only, one 10 GB card, no chat from
  a real person, no second team. Not run: a general-capability benchmark, LoCoMo, a question-shaped router, a
  contamination probe (LongMemEval-S predates the model).

## 8. With more credits, reproduce, and who did what

**With more credits.** A sealed test of K1 on a new set of outside chats under S3's rule; query writing trained on its
own and judged the same way; LoCoMo and chats past the window against code; a judge applying the full never-told
rubric; the whole chat at 419 messages on a larger card.

**Reproduce.** The README gives 6.37's commands; every other run's command is in its run file's provenance.
`scripts/make_article.py` fills the write-ups from results files, except what the long paper's section 15 lists. Training takes 33 to 35 minutes a seed on an RTX 3080;
the run files hold 217 GPU hours, on my own card. Tiny Aya Global, the adapters and the data are
CC-BY-NC-4.0; the code is Apache-2.0.

**Who did what.** I directed the work and made every decision in `RECORDS.md`. Claude (Anthropic) wrote the code,
data, tests and these write-ups and ran the experiments, as an executive-function accommodation; other Claude agents
wrote the outside-writer chats, S3 and the demos, and judged. Teammates: none. Before 1 November: only the plan
(R-001) and my chat engine LLE, none of it here. Thanks to Lexsi Labs and Cohere Labs.
