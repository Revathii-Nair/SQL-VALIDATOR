import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lexer import Lexer

def test_tokenize_select_query():
    lexer = Lexer()
    query = "SELECT name, age FROM users WHERE age > 18;"
    tokens = lexer.tokenize(query)

    # Check first token
    assert tokens[0].type == "KEYWORD"
    assert tokens[0].value.upper() == "SELECT"

    # Check identifiers
    identifiers = [t.value for t in tokens if t.type == "IDENTIFIER"]
    assert "name" in identifiers
    assert "age" in identifiers
    assert "users" in identifiers

    # Check operators
    operators = [t.value for t in tokens if t.type == "OPERATOR"]
    assert ">" in operators

    # EOF token
    assert tokens[-1].type == "EOF"

def test_tokenize_with_comments_and_whitespace():
    lexer = Lexer()
    query = "SELECT * FROM users; -- This is a comment"
    tokens = lexer.tokenize(query)
    token_values = [t.value for t in tokens if t.type != "EOF"]
    assert "*" in token_values
    assert "users" in token_values
    # Comments should be skipped
    assert "-- This is a comment" not in token_values