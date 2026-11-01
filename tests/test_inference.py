"""Generation must stop on every token that can end a Tiny Aya turn."""

import pytest
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer

from aya_retrieval.inference import STOP_TOKENS, prompt_tokens, stop_token_ids
from aya_retrieval.models import MODEL_ID, MODEL_REVISION


@pytest.fixture(scope="module")
def tokenizer():
    path = snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True)
    return AutoTokenizer.from_pretrained(path)


def test_the_tokens_that_close_a_rendered_turn_are_all_stops(tokenizer):
    messages = [{"role": "user", "content": "U"}, {"role": "assistant", "content": "A"}]
    rendered = tokenizer.apply_chat_template(messages, tokenize=True, return_dict=True)
    closing_ids = rendered["input_ids"][-2:]
    assert set(closing_ids) <= set(stop_token_ids(tokenizer))


def test_the_three_stops_are_distinct(tokenizer):
    assert len(set(stop_token_ids(tokenizer))) == len(STOP_TOKENS)


def test_prompt_tokens_counts_what_generation_feeds_the_model(tokenizer):
    messages = [{"role": "user", "content": "how is the weather"}]
    inputs = tokenizer.apply_chat_template(
        messages, add_generation_prompt=True, return_tensors="pt", return_dict=True
    )
    assert prompt_tokens(tokenizer, messages) == inputs["input_ids"].shape[1]


def test_prompt_tokens_grow_with_the_conversation(tokenizer):
    short = [{"role": "user", "content": "hello"}]
    longer = [*short, {"role": "assistant", "content": "hi"}, {"role": "user", "content": "hello"}]
    assert prompt_tokens(tokenizer, longer) > prompt_tokens(tokenizer, short)


class _TokenizerMissingOneStop:
    unk_token_id = 1

    def convert_tokens_to_ids(self, tokens):
        return [3, 6, 1][: len(tokens)]


def test_an_unknown_stop_token_is_an_error():
    with pytest.raises(ValueError, match="stop token"):
        stop_token_ids(_TokenizerMissingOneStop())
