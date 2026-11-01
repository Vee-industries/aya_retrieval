"""Generation must stop on every token that can end a Tiny Aya turn."""

import pytest
from huggingface_hub import snapshot_download
from transformers import AutoTokenizer

from aya_retrieval.inference import STOP_TOKENS, stop_token_ids
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


class _TokenizerMissingOneStop:
    unk_token_id = 1

    def convert_tokens_to_ids(self, tokens):
        return [3, 6, 1][: len(tokens)]


def test_an_unknown_stop_token_is_an_error():
    with pytest.raises(ValueError, match="stop token"):
        stop_token_ids(_TokenizerMissingOneStop())
