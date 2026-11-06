"""Training labels that put the loss only on the replies a row demonstrates.

A row is the system prompt, the exchanges in view, the friend's message, then what the model should
do: a search call, the tool's result and a reply, or a reply alone. TRL's default trains on every
token of that, so the model also learns to write the friend's lines, the tool's passages and the
scripted small talk in view. Here only the assistant turns after the friend's message carry loss.
``decision_labels`` goes further for plain-chat rows (17m, R-088): only a reply's first token,
which decides between a search and a reply, and its end-of-turn marker carry loss, so the words of
the reply stay the model's own.
"""

from __future__ import annotations

IGNORE = -100


def _ids(tokenizer, messages: list[dict], generation: bool = False) -> list[int]:
    return tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=generation, return_dict=True
    )["input_ids"]


def _assistant_spans(tokenizer, messages: list[dict], ids: list[int]):
    """Yield each assistant turn's index and token span.

    A turn's tokens are those its message adds to the conversation before it, with the generation
    prompt counted as context, so a span is the reply and its end-of-turn marker.
    """
    for index, message in enumerate(messages):
        if message["role"] != "assistant":
            continue
        before = _ids(tokenizer, messages[:index], generation=True)
        through = _ids(tokenizer, messages[: index + 1])
        if ids[: len(before)] != before or ids[: len(through)] != through:
            raise ValueError(f"turn {index} does not render as a prefix of the row")
        yield index, len(before), len(through)


def demonstrated_labels(tokenizer, messages: list[dict], first: int) -> tuple[list[int], list[int]]:
    """Return the row's token ids and labels, with loss only on assistant turns from ``first`` on.

    Raises:
        ValueError: If the chat template does not render a conversation as a prefix of a longer one,
            so a span could not be placed.
    """
    ids = _ids(tokenizer, messages)
    labels = [IGNORE] * len(ids)
    for index, start, end in _assistant_spans(tokenizer, messages, ids):
        if index >= first:
            labels[start:end] = ids[start:end]
    return ids, labels


def without_history_replies(
    tokenizer, messages: list[dict], first: int
) -> tuple[list[int], list[int]]:
    """Return the row's token ids and labels, with loss on every token but the assistant turns
    before ``first``: the scripted small-talk replies in view.

    Raises:
        ValueError: As ``demonstrated_labels``.
    """
    ids = _ids(tokenizer, messages)
    labels = list(ids)
    for index, start, end in _assistant_spans(tokenizer, messages, ids):
        if index < first:
            labels[start:end] = [IGNORE] * (end - start)
    return ids, labels


def decision_labels(tokenizer, messages: list[dict], first: int) -> tuple[list[int], list[int]]:
    """Return the row's token ids and labels, with loss only on the first token and the end-of-turn
    marker of each assistant turn from ``first`` on.

    Raises:
        ValueError: As ``demonstrated_labels``.
    """
    ids = _ids(tokenizer, messages)
    labels = [IGNORE] * len(ids)
    for index, start, end in _assistant_spans(tokenizer, messages, ids):
        if index < first:
            continue
        empty = [*messages[:index], {**messages[index], "content": ""}]
        marker = next(
            e - s
            for i, s, e in _assistant_spans(tokenizer, empty, _ids(tokenizer, empty))
            if i == index
        )
        labels[start] = ids[start]
        labels[end - marker : end] = ids[end - marker : end]
    return ids, labels


def answer_decision_labels(
    tokenizer, messages: list[dict], first: int
) -> tuple[list[int], list[int]]:
    """Return the row's token ids and labels, with the demonstrated turns' loss, except that the
    last turn, the reply to the search result, keeps loss only on its first token and its
    end-of-turn marker (fix B, R-095): the search is taught in full and the reply's words stay the
    model's own.

    Raises:
        ValueError: As ``demonstrated_labels``.
    """
    ids, labels = demonstrated_labels(tokenizer, messages, first)
    _, decided = decision_labels(tokenizer, messages, first)
    spans = list(_assistant_spans(tokenizer, messages, ids))
    _, start, end = spans[-1]
    labels[start:end] = decided[start:end]
    return ids, labels
