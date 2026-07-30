from pocket_agent.core.tool_loop import parse_tool_call


def test_parse_tool_call_web_search():
    text = '{"tool": "web_search", "arguments": {"query": "time Amsterdam"}}'
    parsed = parse_tool_call(text)
    assert parsed == ("web_search", {"query": "time Amsterdam"})


def test_parse_tool_call_fenced():
    text = 'Here is the call:\n```json\n{"tool": "web_search", "arguments": {"query": "weather"}}\n```'
    parsed = parse_tool_call(text)
    assert parsed == ("web_search", {"query": "weather"})


def test_parse_tool_call_unknown_tool():
    parsed = parse_tool_call('{"tool": "delete_everything", "arguments": {}}')
    assert parsed is None
