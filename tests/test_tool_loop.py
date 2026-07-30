from pocket_agent.core.tool_loop import parse_tool_call, unknown_tool_in_response


def test_unknown_tool_not_parsed_as_valid():
    text = '{"tool": "general", "arguments": {"query": "author"}}'
    assert parse_tool_call(text) is None
    assert unknown_tool_in_response(text) == "general"


def test_valid_tool_parsed():
    text = '{"tool": "current_weather", "arguments": {"location": "Amsterdam"}}'
    assert parse_tool_call(text) == ("current_weather", {"location": "Amsterdam"})
    assert unknown_tool_in_response(text) is None
