# Teaching a 3B model to search a long chat it can no longer see

*Kevin Vaillancourt · Lexsi AI Safety and Alignment Hackathon, Track 3 (Agentic Fine-tuning) · November 2026*

A short version of the full write-up,
[docs/ARTICLE.md](https://github.com/Vee-industries/aya_retrieval/blob/main/docs/ARTICLE.md). Code, the dated
record of every decision and run, and every results file:
[github.com/Vee-industries/aya_retrieval](https://github.com/Vee-industries/aya_retrieval). Adapter:
[KevinVaillancourt/aya-retrieval-6.37](https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37). Data and logs:
[aya_retrieval datasets](https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-datasets). Record numbers
(R-164 and so on) point into `RECORDS.md` in the repository.

## What was built

Tiny Aya Global (3.35B) answers only from what it can read. 6.37 is a LoRA adapter (rank 32, all attention and MLP
projections) trained with Lexsi Labs' AgentTune to search the earlier conversation when an answer is out of view,
read what the search returns, and answer in the model's own voice. The harness shows the last three exchanges;
everything older is reachable only through a `search_corpus` tool (SQLite full-text search, top 5 passages, up to
three calls a turn). The same harness and decoding (greedy, 60 new tokens) serve every arm below.

The 1,094 training rows come from a generated pool: chats of small talk with facts told along the way, ending in a
message the model must answer. There are five kinds of message:
- `older`: a question about a fact now out of view.
- `confirm`: "..., right?" about such a fact.
- `in_view`: the answer is still on screen.
- `never_told`: the fact was never given, so the right reply declines.
- `statement`: plain chat, where the right move is not to search.

Targets are the untrained model's own replies where they pass the scorer, vetted plain-chat replies, and scripted
answers where needed. AuditKIT re-scores recorded replies as a check on the scorer; CuratorKIT's grounding gate
checks the training answers.

Every test was registered before it ran, with its pass rule, and the model, scorer and judge were frozen by digest
before the sealed run (R-154, R-160).

## 1. When the chat fits, give it the whole chat

On two sets of chats written by fresh Claude Opus agents who never saw the generator (40 chats a set, averaging
1,400 tokens), questions about earlier facts (`older`, 80 a set; R-164, R-165):

| Set | Base, last three exchanges and the tool | 6.37, last three exchanges and the tool | Base, whole chat | 6.37, whole chat and the tool |
|---|---|---|---|---|
| 1 | 11 | 28 | 58 | 57 |
| 2 | 12 | 34 | 52 | 54 |

![Whole chat or search](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/whole_chat_or_search.png)

Base with every message in view beats 6.37 working from the last three exchanges on both sets (p = 2.8 × 10⁻⁶ and
0.0051). Given the whole chat, 6.37 and base show no measured difference on any kind of message, with or without
the tool. This test is one seed and 40 chats a set, so gaps under 15 points on a kind of 40 questions are below what
it resolves (R-142).

This holds on the outside-writer chats only. On the project's generated chats of the same length (58 messages, 1,105
to 1,332 tokens), base with the whole chat answers 21 to 33 of 60 recall questions against 6.37's 46 to 55 with the
tool (R-168).

## 2. Plain code that searches every turn recalls as well, on outside-writer chats

R-016 registered a reference that was left out of the sealed run and run late (R-167, R-169). Code makes the first
search on every turn with the newest message as the query, and hands base the passages. Nothing is trained. Before
it ran, the record fixed what each outcome would mean: if code is at or above 6.37 on recall, training adds nothing
to recall on these chats.

| Kind (questions a set) | Set 1: code | 6.37 | Set 2: code | 6.37 |
|---|---|---|---|---|
| recall, `older` and `confirm` (120) | 42 | 39 (p = 0.76) | 47 | 53 (p = 0.45) |
| `in_view` (40) | 13 | 35 (p = 3.0 × 10⁻⁶) | 16 | 37 (p = 9.5 × 10⁻⁷) |
| `never_told` (40) | 31 | 37 (p = 0.11) | 24 | 36 (p = 0.0042) |
| `statement`, answered without a search (40) | 0 | 37 | 0 | 35 |

Base with the tool gets 26 and 27 on recall. On recall, code and 6.37 show no measured difference; set 1 meets the
registered outcome. What training adds on these chats is deciding when not to search: code searches even when the
answer is on screen, and it searches on every plain statement.

## 3. The sealed run, on generated chats

Run once on 300 unseen generated chats in each of four conditions, on the untrained model and all eight training
seeds. The pools are `heldout` (written by Claude) and `independent` (written by a fresh agent from a brief), with
one or four decoy facts a chat. Every registered rule passes in every condition (R-163):
- recall up 20 points or more;
- every right answer from a search that found the fact;
- no adapter with more false retrievals than base;
- every adapter judged coherent at least as often as base, by all three judges.

Recall (`older` and `confirm`, at 58 and 419 messages):

| Condition | Base, 58 | Eight adapters pooled, 58 | Base, 419 | Eight adapters pooled, 419 |
|---|---|---|---|---|
| A, `heldout`, 1 decoy | 17 of 60 | 426 of 480 | 15 of 60 | 409 of 480 |
| B, `heldout`, 4 decoys | 15 of 60 | 434 of 480 | 14 of 60 | 409 of 480 |
| C, `independent`, 1 decoy | 10 of 60 | 434 of 480 | 11 of 60 | 429 of 480 |
| D, `independent`, 4 decoys | 5 of 60 | 434 of 480 | 8 of 60 | 424 of 480 |

![Recall out of view](https://raw.githubusercontent.com/Vee-industries/aya_retrieval/main/figures/recall_out_of_view.png)

The shipped seed, 82, answers 91 to 107 of 120 recall questions against base's 13 to 32. It is the lowest of the
eight seeds on the `independent` pool. On the same chats, code that searches every turn gets 14 to 32 of 60 against
seed 82's 44 to 55 (sign test p at most 3.2 × 10⁻⁴; R-168).

## 4. LongMemEval-S, an outside check

A third kind of chat: user-to-assistant histories, partly real logs and partly model-simulated, 500 questions, each
over its own history (244 exchanges at the median). Every arm sees the last three exchanges, with the same tool over
everything earlier. 6.37's system prompt, "You are chatting with a friend", does not match these chats. The official
score uses a GPT-4o judge, which was not available. The numbers here are not the official score, and no ranking
against published systems is made (R-170).

Judged with LongMemEval's own per-type prompts by three fresh Claude Sonnet judges, blind to the arm. Judge 1
decides. Kevin marked 50 lines blind before any judged number was read.

| Judged right | 6.37, tool | base, tool | code always searches | base, three exchanges, no tool |
|---|---|---|---|---|
| all 248 judged questions | 53 | 34 | 40 | 13 |
| of those, the 233 answerable | 40 | 32 | 40 | 8 |
| of those, the 15 unanswerable | 13 | 2 | 0 | 5 |

- 6.37 against base with the tool: 53 against 34 (p = 0.014). 11 of the 19-question lead come from the unanswerable
  questions. On the answerable ones, 40 against 32 is no measured difference (p = 0.29).
- 6.37 against code: 53 against 40 (p = 0.12), and a tie at 40 on the answerable questions. The answerable and
  unanswerable split was read after the registered result.
- Code's first search finds the evidence on 372 of 476 questions, against 6.37's 333 (p = 0.0004).
- 6.37 declines 233 of all 470 answerable questions, against base's 22.
- The judges agree with each other on 1,027 to 1,030 of 1,035 lines. Kevin agrees with each judge on 46 of his 50.
  Two of the four lines where he differs are replies that cannot answer "because I am a language model"; he counts
  them as failures and the judge prompt counts them right.
- Every arm answers few questions. Base reading only the sessions that hold the evidence is right on 47 of its 71
  lines.

## 5. Cost

Code that searches every turn is faster than 6.37 on every set:
- generated sealed chats: 1.01 to 1.23 s a conversation against 1.67 to 2.08;
- outside-writer sets: 1.45 to 1.48 s a question against 1.70 to 1.96;
- LongMemEval-S: 3.09 s a question against 3.81.

6.37 reads 35 to 37% of the whole chat's tokens a turn on the sealed chats. Training took 33 to 35 minutes a seed on
one RTX 3080 (10 GB); peak card memory in the sealed run was 7.02 GiB.

## 6. Limits

- Short outside-writer chats are better shown whole.
- On outside-writer chats, plain code recalls as well as 6.37; the recall gain over code is shown on generated chats
  only.
- On LongMemEval-S, code finds more evidence than 6.37, and 6.37 declines half the answerable questions.
- 6.37 goes along with most false claims in "..., right?" questions: it corrects 1 and 3 of 20 on the outside-writer
  sets.
- One model, one size, English only, greedy decoding, one machine. No hostile text in retrieved passages is tested.
- The generated pools and outside-writer sets hold no chat from a real person.
- The coherence judges are Claude Sonnet agents and were never checked against a person.
- The whole-chat reading at 419 messages is not measured: those runs did not fit the 10 GB card.

## Reproduce

The repository's README gives the setup, the commands for every run, and the training command for the shipped seed
(33 to 35 minutes on an RTX 3080). The full write-up covers the method, the evaluation protocol, the candidate
ledger, toolkit findings, threats to validity, and every error found and corrected.

Tiny Aya Global is released by Cohere Labs under CC-BY-NC-4.0, and the adapter and data carry that licence. The code
is Apache-2.0. LongMemEval's judge prompts are used under its MIT licence.
