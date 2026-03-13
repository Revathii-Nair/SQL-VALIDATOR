import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lexer import Lexer
from parser import Parser, ASTNode

@pytest.fixture
def lexer():
    return Lexer()

def test_parse_select_simple(lexer):
    query = "SELECT name FROM users;"
    tokens = lexer.tokenize(query)
    parser = Parser(tokens)
    ast = parser.parse()

    assert isinstance(ast, ASTNode)
    assert ast.type == "SELECT"
    table_node = next((c for c in ast.children if c and c.type == "TABLE"), None)
    assert table_node.value == "users"

def test_parse_insert_with_values(lexer):
    query = "INSERT INTO users (name, age) VALUES ('John', 25);"
    tokens = lexer.tokenize(query)
    parser = Parser(tokens)
    ast = parser.parse()

    assert ast.type == "INSERT"
    table_node = next((c for c in ast.children if c and c.type == "TABLE"), None)
    values_node = next((c for c in ast.children if c and c.type == "VALUES"), None)
    assert table_node.value == "users"
    assert values_node.value == ["'John'", "25"]

def test_parse_delete(lexer):
    query = "DELETE FROM users WHERE age < 18;"
    tokens = lexer.tokenize(query)
    parser = Parser(tokens)
    ast = parser.parse()

    assert ast.type == "DELETE"
    where_node = next((c for c in ast.children if c and c.type == "WHERE"), None)
    assert where_node.value[0] == "age"  # left side
    assert where_node.value[1] == "<"
    assert where_node.value[2] == "18"