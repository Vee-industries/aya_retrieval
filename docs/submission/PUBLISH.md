# Submission plan: Lexsi hackathon, due 15 November 2026, 11:59 PM AoE

Requirements read from hackathon.lexsi.ai on 10 November (R-171). A later submission replaces an earlier one.

## What goes where

| Item | Source in this repository | Destination |
|---|---|---|
| Abstract (496 words, limit 500) | `docs/submission/ABSTRACT.md` | the form |
| Adapter | `../adapters/screens/fix17cs37_82`: `adapter_model.safetensors` and `adapter_config.json` only | Hugging Face model repo, card `docs/MODEL_CARD.md` as its README |
| Training and test chats | `data/screens/`, `data/recall_train.jsonl`, `data/blind_dev/`, `data/blind_dev2/` | Hugging Face dataset repo, card `docs/submission/hf_data_card.md` |
| Evaluation logs | `results/` without `results/longmemeval/` (which git already ignores) | Hugging Face dataset repo, card `docs/submission/hf_eval_logs_card.md` |
| Model collection and dataset collection | the three repos above | Hugging Face, both public and not gated |
| Write-up | `README.md` and `docs/ARTICLE.md` | the GitHub repository (an HF article is optional) |
| Code | this repository | github.com/Vee-industries/aya_retrieval, made public |

## Form fields

- Models used: `CohereLabs/tiny-aya-global`, revision `af89d219`.
- Toolkits used: Lexsi Labs' AgentTune, AuditKIT and CuratorKIT, at the commits in RECORDS R-003.
- Track: 3, Agentic Fine-tuning. Problem statement: retrieval, in its wording "decides when and what to retrieve,
  grounds its answers in the retrieved text and ignores distracting documents" (ARTICLE section 1 maps each phrase to
  a measure).
- Before-and-after metrics: recall, false retrievals, coherence, declining never-told facts, searches on plain
  statements, judged accuracy on LongMemEval-S.

## Order

1. Privacy and secrets sweep of the whole repository before it goes public (Claude): family words, names, email
   addresses and keys, with full output.
2. Kevin's go to publish. Every step from here is public and his call.
3. Hugging Face: create the three repos and two collections, and upload (Kevin, or Claude through the logged-in
   `hf` command on Kevin's word).
4. GitHub: make the repository public (Kevin, in its settings).
5. The form (Kevin): his registered email, the abstract, the links.
6. Shortlisted teams are told by 16 November and submit a video presentation or slides by 22 November.

## Done, 10 November (R-172)

- Model: https://huggingface.co/KevinVaillancourt/aya-retrieval-6.37 (weights SHA-256 matches the sealed manifest)
- Datasets: https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-chats and
  https://huggingface.co/datasets/KevinVaillancourt/aya-retrieval-eval-logs
- Collections: https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-models-6af35d3c521e8481db061df5 and
  https://huggingface.co/collections/KevinVaillancourt/aya-retrieval-datasets-6af35d3cf9a91556f52af373
- Code: https://github.com/Vee-industries/aya_retrieval (public)
- Left for Kevin: the form.
