# Submission plan: Lexsi hackathon, due 15 November 2026, 11:59 PM AoE

Requirements read from hackathon.lexsi.ai on 10 November (R-171); the judges' checklist on 13 November (R-217). A
later submission replaces an earlier one. The abstract limit is under 500 words; `scripts/make_article.py` refuses
to write an `ABSTRACT.md` over 500.

## What goes where

| Item | Source in this repository | Destination |
|---|---|---|
| Abstract | `docs/submission/ABSTRACT.md` | the form |
| 6.37, the shipped adapter | `../adapters/screens/fix17cs37_82`: `adapter_model.safetensors` and `adapter_config.json` only | Hugging Face model repo `aya-retrieval-6.37`, card `docs/MODEL_CARD.md` as its README |
| The short paper | `docs/submission/HF_ARTICLE.md` | the 6.37 model repo, as `ARTICLE.md` (the Hugging Face article) |
| C1, published beside 6.37, labelled as failing one clause | `../adapters/screens/k13opc1_r263_82` (R-296) | Hugging Face model repo `aya-retrieval-c1`, card `docs/MODEL_CARD_C1.md` as its README |
| Training and test chats | `data/screens/`, `data/recall_train.jsonl`, `data/blind_dev/`, `data/blind_dev2/` | Hugging Face dataset repo `aya-retrieval-chats`, card `docs/submission/hf_data_card.md` |
| Evaluation logs | `results/` without `results/longmemeval/` (which git already ignores), including `results/s3/` | Hugging Face dataset repo `aya-retrieval-eval-logs`, card `docs/submission/hf_eval_logs_card.md` |
| Model collection and dataset collection | the four repos above | Hugging Face, all public and not gated |
| Write-up | `docs/ARTICLE.md` (long), `docs/submission/HF_ARTICLE.md` (short), `README.md` | the GitHub repository and the 6.37 model repo |
| Code | this repository | github.com/Vee-industries/aya_retrieval, public |

## Form fields

- Models used: `CohereLabs/tiny-aya-global`, revision `af89d219`.
- Toolkits used: Lexsi Labs' AgentTune, AuditKIT and CuratorKIT, at the commits in RECORDS R-003.
- Track: 3, Agentic Fine-tuning. Problem statement: retrieval, in its wording "decides when and what to retrieve,
  grounds its answers in the retrieved text and ignores distracting documents" (ARTICLE section 1 maps each phrase to
  a measure).
- Before-and-after metrics: recall, false retrievals, coherence, declining never-told facts, searches on plain
  statements, judged accuracy on LongMemEval-S, and on S3 copies of the model's own wrong answer and N-hit false
  answers.
- Model put forward: 6.37 seed 82 (R-294); C1 is published beside it, labelled.

## Order

Every step from 2 on is public and Kevin's call.

1. Privacy and secrets sweep (Claude) of every commit not yet on GitHub (R-172 swept only to 10 November): family
   words, names, email addresses and keys, with full output.
2. Push to GitHub, so that `main` holds this write-up: every GitHub link in the documents (figures, `docs/demo.md`,
   the Colab notebook) points at `main`.
3. Hugging Face uploads (Kevin, or Claude through the logged-in `hf` command on Kevin's word):
   - 6.37's model card (`docs/MODEL_CARD.md` as README) and the short paper (`docs/submission/HF_ARTICLE.md` as
     `ARTICLE.md`) to `aya-retrieval-6.37`;
   - C1's model card (`docs/MODEL_CARD_C1.md` as README) to `aya-retrieval-c1`;
   - `aya-retrieval-eval-logs` from every source its row in the table above names: all of `results/` except
     `results/longmemeval/`, so every folder written since 10 November goes up, `results/s3/` among them, with its
     card naming the S3 folder;
   - `aya-retrieval-chats` from every source its row names, so the reopened candidates' training sets added to
     `data/screens/` since 10 November go up;
   - both collections checked to list all four repos.
4. Recheck every link in README, ARTICLE, HF_ARTICLE, both model cards and both dataset cards, from outside the
   clone, logged out: each must open, and each figure must load.
5. The form (Kevin): his registered email, `ABSTRACT.md`, the links.
6. Shortlisted teams are told by 16 November and submit a video presentation or slides by 22 November.

## Done

- 10 November (R-172): https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37 (weights SHA-256 matches the
  sealed manifest); https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-chats and
  https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-eval-logs; the collections
  https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-models-6af35d3c521e8481db061df5 and
  https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-datasets-6af35d3cf9a91556f52af373; the code at
  https://github.com/Vee-industries/aya_retrieval (public).
- 12 November (R-181): S3's chats and seal pushed to the GitHub repository's `reopened` branch.
- 15 November (R-296): https://huggingface.co/KevinVaillancourt/aya-retrieval-c1, public and not gated, added to the
  models collection.
- Not yet done: steps 1 to 5 above for the reopened work (R-173 to R-303).
