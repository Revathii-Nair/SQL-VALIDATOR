"""
Lexer Module - Breaks SQL text into tokens (pieces)
Think of this like breaking a sentence into words
"""

import re

class Token:
    """Represents one piece of SQL (like a word in a sentence)"""
    
    def __init__(self, token_type, value, line, column):
        self.type = token_type      # What kind of token (KEYWORD, IDENTIFIER, etc.)
        self.value = value          # The actual text
        self.line = line            # Which line it's on
        self.column = column        # Position in that line
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', Line:{self.line}, Col:{self.column})"


class Lexer:
    """Converts SQL text into a list of tokens"""
    
    def __init__(self):
        # Define SQL keywords (reserved words)
        self.keywords = {
            'SELECT', 'FROM', 'WHERE', 'INSERT', 'INTO', 'VALUES',
            'UPDATE', 'SET', 'DELETE', 'CREATE', 'TABLE', 'DROP',
            'ALTER', 'ADD', 'COLUMN', 'MODIFY', 'AND', 'OR', 'NOT', 'EXISTS',
            'IN', 'LIKE', 'BETWEEN', 'IS', 'NULL', 'AS', 'ORDER',
            'BY', 'GROUP', 'HAVING', 'LIMIT', 'JOIN', 'ON', 'INNER',
            'LEFT', 'RIGHT', 'OUTER', 'DISTINCT', 'ASC', 'DESC'
        }
        
        # Define token patterns (how to recognize different parts)
        self.token_patterns = [
            ('NUMBER', r'\d+(\.\d+)?'),           # Numbers like 123 or 12.34
            ('STRING', r"'[^']*'"),               # Strings like 'hello'
            ('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Names like table1, col_name
            ('OPERATOR', r'(>=|<=|!=|<>|=|>|<)'), # Comparison operators
            ('WILDCARD', r'\*'),                  # The * symbol
            ('COMMA', r','),                      # Comma
            ('SEMICOLON', r';'),                  # Semicolon
            ('LPAREN', r'\('),                    # Left parenthesis
            ('RPAREN', r'\)'),                    # Right parenthesis
            ('WHITESPACE', r'\s+'),               # Spaces, tabs, newlines
            ('COMMENT', r'--[^\n]*'),             # Comments starting with --
        ]
        
        # Combine all patterns into one big pattern
        self.combined_pattern = '|'.join(f'(?P<{name}>{pattern})' 
                                         for name, pattern in self.token_patterns)
        self.regex = re.compile(self.combined_pattern, re.IGNORECASE)
    
    def tokenize(self, sql_text):
        """
        Convert SQL text into tokens
        
        Args:
            sql_text: The SQL query as a string
            
        Returns:
            List of Token objects
        """
        tokens = []
        line_num = 1
        line_start = 0
        
        # Find all matches in the SQL text
        for match in self.regex.finditer(sql_text):
            token_type = match.lastgroup
            token_value = match.group()
            column = match.start() - line_start + 1
            
            # Skip whitespace and comments
            if token_type in ('WHITESPACE', 'COMMENT'):
                # Count newlines to track line numbers
                if '\n' in token_value:
                    line_num += token_value.count('\n')
                    line_start = match.end()
                continue
            
            # Check if identifier is actually a keyword
            if token_type == 'IDENTIFIER':
                if token_value.upper() in self.keywords:
                    token_type = 'KEYWORD'
            
            # Create and add the token
            tokens.append(Token(token_type, token_value, line_num, column))
        
        # Add EOF (End Of File) token
        tokens.append(Token('EOF', '', line_num, len(sql_text) - line_start + 1))
        
        return tokens


# Example usage (for testing)
if __name__ == "__main__":
    lexer = Lexer()
    
    # Test with a simple query
    test_query = "SELECT name, age FROM users WHERE age > 18;"
    
    tokens = lexer.tokenize(test_query)
    
    print("Tokens generated:")
    for token in tokens:
        print(token)
        
# Token(KEYWORD, 'SELECT', Line:1, Col:1)
# Token(IDENTIFIER, 'name', Line:1, Col:8)
# Token(COMMA, ',', Line:1, Col:12)
# Token(IDENTIFIER, 'age', Line:1, Col:14)
# Token(KEYWORD, 'FROM', Line:1, Col:18)
# Token(IDENTIFIER, 'users', Line:1, Col:23)
# Token(KEYWORD, 'WHERE', Line:1, Col:29)
# Token(IDENTIFIER, 'age', Line:1, Col:35)
# Token(OPERATOR, '>', Line:1, Col:39)
# Token(NUMBER, '18', Line:1, Col:41)
# Token(SEMICOLON, ';', Line:1, Col:43)
# Token(EOF, '', Line:1, Col:44)