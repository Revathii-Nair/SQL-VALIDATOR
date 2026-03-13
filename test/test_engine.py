import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cli import CLIEngine


def test_get_user_choice_valid(monkeypatch):
    cli = CLIEngine()
    monkeypatch.setattr(cli.console, "input", lambda prompt: "1")
    choice = cli.get_user_choice()
    assert choice == "1"

def test_display_result_text(monkeypatch):
    cli = CLIEngine()
    result = {"success": True, "errors": [], "warnings": []}
    query = "SELECT * FROM users;"
    # Just call display_result; it should not crash
    cli.display_result(query, result)

def test_validate_query_basic(monkeypatch):
    cli = CLIEngine()
    query = "SELECT * FROM users;"
    result = cli.validate_query(query)
    # Result should contain 'success' key
    assert "success" in result