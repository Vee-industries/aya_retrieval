"""The tool loop must run real searches and give the model the result."""

from aya_retrieval.harness import MAX_CALLS, run_turn, search_query

CALL = '[{"tool_name": "search_corpus", "parameters": {"query": "sister dog"}}]'


def scripted(*replies):
    remaining = list(replies)
    seen = []

    def generate(messages):
        seen.append(messages)
        return remaining.pop(0)

    generate.seen = seen
    return generate


def test_a_plain_reply_ends_the_turn_with_no_search():
    result = run_turn(scripted("Nice."), lambda q: "unused", "S", (("a", "b"),), "hello")
    assert result.reply == "Nice."
    assert result.queries == []
    assert not result.ran_out_of_calls


def test_a_call_runs_the_tool_and_the_model_sees_its_result():
    generate = scripted(CALL, "Her dog is Pepper.")
    result = run_turn(generate, lambda q: f"found for {q}", "S", (), "who")
    assert result.reply == "Her dog is Pepper."
    assert result.queries == ["sister dog"]
    final_prompt = generate.seen[1]
    assert final_prompt[-2] == {"role": "assistant", "content": CALL}
    assert "found for sister dog" in final_prompt[-1]["content"]
    assert final_prompt[-1]["role"] == "user"


def test_a_model_that_keeps_calling_is_stopped_and_flagged():
    generate = scripted(*[CALL] * (MAX_CALLS + 1))
    result = run_turn(generate, lambda q: "x", "S", (), "who")
    assert result.ran_out_of_calls
    assert len(result.queries) == MAX_CALLS + 1


def test_invented_text_after_a_call_is_still_a_call():
    assert search_query(f"{CALL}\nTool result: invented") == "sister dog"


def test_text_that_only_mentions_the_tool_is_no_call():
    assert search_query("I could use search_corpus for that.") is None
