"""Loss masks put the loss exactly on the turns they name, on Tiny Aya's own chat template."""

import pytest

from aya_retrieval.loss_masks import IGNORE, demonstrated_labels, without_history_replies


@pytest.fixture(scope="module")
def tokenizer():
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer

    from aya_retrieval.models import MODEL_ID, MODEL_REVISION

    try:
        path = snapshot_download(MODEL_ID, revision=MODEL_REVISION, local_files_only=True)
    except Exception:
        pytest.skip("Tiny Aya is not in the local cache")
    return AutoTokenizer.from_pretrained(path)


CALL = '[{"tool_name": "search_corpus", "parameters": {"query": "cousin cello"}}]'
MESSAGES = [
    {"role": "system", "content": "You are chatting with a friend."},
    {"role": "user", "content": "the weather is grim"},
    {"role": "assistant", "content": "Love that for you."},
    {"role": "user", "content": "what instrument does my cousin play"},
    {"role": "assistant", "content": CALL},
    {"role": "user", "content": "Tool result: my cousin Ines plays the cello"},
    {"role": "assistant", "content": "Ines plays the cello."},
]
FIRST = 4


def labelled_text(tokenizer, ids, labels):
    return tokenizer.decode([i for i, label in zip(ids, labels, strict=True) if label != IGNORE])


def test_only_the_demonstrated_turns_carry_loss(tokenizer):
    ids, labels = demonstrated_labels(tokenizer, MESSAGES, FIRST)
    text = labelled_text(tokenizer, ids, labels)
    assert CALL in text and "Ines plays the cello." in text
    for unseen in ("Love that for you.", "Tool result", "the weather is grim", "chatting"):
        assert unseen not in text
    assert text.count("<|END_OF_TURN_TOKEN|>") == 2


def test_without_history_replies_masks_only_the_replies_in_view(tokenizer):
    ids, labels = without_history_replies(tokenizer, MESSAGES, FIRST)
    text = labelled_text(tokenizer, ids, labels)
    assert "Love that for you." not in text
    for kept in (CALL, "Ines plays the cello.", "Tool result", "the weather is grim", "chatting"):
        assert kept in text
    masked = sum(label == IGNORE for label in labels)
    assert 0 < masked < len(ids) // 4


def test_two_searches_both_carry_loss(tokenizer):
    second = CALL.replace("cousin cello", "Ines instrument")
    messages = [*MESSAGES[:6], {"role": "assistant", "content": second}, *MESSAGES[5:]]
    ids, labels = demonstrated_labels(tokenizer, messages, FIRST)
    text = labelled_text(tokenizer, ids, labels)
    assert CALL in text and second in text and "Ines plays the cello." in text
