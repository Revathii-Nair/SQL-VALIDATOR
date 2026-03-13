import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from cli import CLIEngine


def test_missing_from_clause():
    engine = CLIEngine()
    result = engine.validate_query("SELECT id;")

    assert result["success"] is False
    assert any("FROM" in err.message.upper() for err in result["errors"])

