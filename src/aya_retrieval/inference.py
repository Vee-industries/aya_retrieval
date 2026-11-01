"""Generating one reply, the same way for the base model and for a trained adapter."""

from __future__ import annotations

import torch

SAMPLING = {"do_sample": True, "temperature": 0.7, "top_p": 0.95}
GREEDY = {"do_sample": False}

# The model's generation config stops only on <EOS_TOKEN>, but its chat template ends a turn with
# the other two, so without all three a finished reply runs on past its end.
STOP_TOKENS = ("<EOS_TOKEN>", "<|END_RESPONSE|>", "<|END_OF_TURN_TOKEN|>")


def stop_token_ids(tokenizer) -> list[int]:
    """Return the ids that end a reply.

    Raises:
        ValueError: If the tokenizer does not know one of the tokens, so a stop would be missed.
    """
    ids = tokenizer.convert_tokens_to_ids(list(STOP_TOKENS))
    unknown_id = tokenizer.unk_token_id
    if any(token_id is None or token_id == unknown_id for token_id in ids):
        known = dict(zip(STOP_TOKENS, ids, strict=True))
        raise ValueError(f"tokenizer does not know every stop token: {known}")
    return ids


def generate_from_messages(
    model, tokenizer, messages: list[dict], options: dict, max_tokens: int
) -> str:
    """Return the model's next turn after ``messages``."""
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt", return_dict=True
    ).to(model.device)
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            eos_token_id=stop_token_ids(tokenizer),
            pad_token_id=tokenizer.pad_token_id,
            **options,
        )
    reply_tokens = output[0][inputs["input_ids"].shape[1] :]
    return tokenizer.decode(reply_tokens, skip_special_tokens=True).strip()


def generate_reply(model, tokenizer, system: str, user: str, options: dict, max_tokens: int) -> str:
    """Return the model's reply to one user message."""
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    return generate_from_messages(model, tokenizer, messages, options, max_tokens)
