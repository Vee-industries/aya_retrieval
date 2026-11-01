"""Generating one reply, the same way for the base model and for a trained adapter."""

from __future__ import annotations

import torch

SAMPLING = {"do_sample": True, "temperature": 0.7, "top_p": 0.95}
GREEDY = {"do_sample": False}


def generate_reply(model, tokenizer, system: str, user: str, options: dict, max_tokens: int) -> str:
    """Return the model's reply to one user message."""
    messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt", return_dict=True
    ).to(model.device)
    with torch.no_grad():
        output = model.generate(
            **inputs, max_new_tokens=max_tokens, pad_token_id=tokenizer.eos_token_id, **options
        )
    reply_tokens = output[0][inputs["input_ids"].shape[1] :]
    return tokenizer.decode(reply_tokens, skip_special_tokens=True).strip()
