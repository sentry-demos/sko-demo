import pytest
from unittest.mock import Mock, patch
from llm_adventure import AdventureEngine

def test_parse_response_with_two_options():
    engine = AdventureEngine()
    test_response = """You notice increased latency in the application.

1. Check application logs for errors
2. Monitor system metrics"""

    narrative, options = engine.parse_response(test_response)
    assert len(options) == 2
    assert all(isinstance(opt, str) for opt in options)
    assert options[0].startswith(("Check", "Monitor", "Debug", "Deploy", "Run", "Analyze", "Restart", "Test"))
    assert options[1].startswith(("Check", "Monitor", "Debug", "Deploy", "Run", "Analyze", "Restart", "Test"))

def test_parse_response_with_three_options():
    engine = AdventureEngine()
    test_response = """Database connections are timing out.

1. Check connection pool settings
2. Monitor query performance
3. Deploy configuration update"""

    narrative, options = engine.parse_response(test_response)
    assert len(options) == 3
    assert all(isinstance(opt, str) for opt in options)
    assert all(opt.startswith(("Check", "Monitor", "Debug", "Deploy", "Run", "Analyze", "Restart", "Test")) for opt in options)

def test_parse_response_with_invalid_input():
    engine = AdventureEngine()
    test_response = """Invalid response with no options"""

    narrative, options = engine.parse_response(test_response)
    assert len(options) >= 2  # Should provide fallback options
    assert all(isinstance(opt, str) for opt in options)
    assert all(opt.startswith(("Check", "Monitor", "Debug", "Deploy", "Run", "Analyze", "Restart", "Test")) for opt in options)

def test_parse_response_with_non_action_verbs():
    engine = AdventureEngine()
    test_response = """System is experiencing issues.

1. Look at the logs
2. Search through metrics"""

    narrative, options = engine.parse_response(test_response)
    assert len(options) == 2
    assert all(opt.startswith(("Check", "Monitor", "Debug", "Deploy", "Run", "Analyze", "Restart", "Test")) for opt in options)