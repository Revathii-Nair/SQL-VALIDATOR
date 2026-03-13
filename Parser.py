"""
Parser Module - Checks if tokens are in the correct order
Think of this like checking grammar in a sentence
"""

class ASTNode:
    """Represents a node in the Abstract Syntax Tree"""
    
    def __init__(self, node_type, value=None, children=None):
        self.type = node_type
        self.value = value
        self.children = children if children else []
    
    def __repr__(self):
        return f"ASTNode({self.type}, {self.value})"


class Parser:
    """Parses tokens into an Abstract Syntax Tree (AST)"""
    
    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0  # Current position in token list
    
    def current_token(self):
        """Get the current token we're looking at"""
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def peek_token(self):
        """Look at the next token without moving forward"""
        if self.current + 1 < len(self.tokens):
            return self.tokens[self.current + 1]
        return None
    
    def consume(self, expected_type=None):
        """
        Move to the next token
        If expected_type is given, check if current token matches
        """
        token = self.current_token()
        
        if expected_type and token.type != expected_type:
            raise SyntaxError(
                f"Expected {expected_type} but got {token.type} "
                f"at line {token.line}, column {token.column}"
            )
        
        self.current += 1
        return token
    
    def parse(self):
        """
        Main parsing method - determines what type of SQL statement this is
        Returns an AST (Abstract Syntax Tree)
        """
        token = self.current_token()
        
        if token.type != 'KEYWORD':
            raise SyntaxError(
                f"Expected SQL keyword at line {token.line}, column {token.column}"
            )
        
        keyword = token.value.upper()
        
        # Route to appropriate parser based on SQL command
        if keyword == 'SELECT':
            return self.parse_select()
        elif keyword == 'INSERT':
            return self.parse_insert()
        elif keyword == 'UPDATE':
            return self.parse_update()
        elif keyword == 'DELETE':
            return self.parse_delete()
        elif keyword == 'CREATE':
            return self.parse_create()
        elif keyword == 'DROP':
            return self.parse_drop()
        elif keyword == 'ALTER':
            return self.parse_alter()
        else:
            raise SyntaxError(
                f"Unsupported SQL command: {keyword} at line {token.line}"
            )
    
    def parse_select(self):
        """Parse SELECT statement"""
        self.consume('KEYWORD')  # Consume 'SELECT'
        
        # Parse column list (what to select)
        columns = self.parse_column_list()
        
        # Expect FROM keyword
        if self.current_token().value.upper() != 'FROM':
            raise SyntaxError(
                f"Expected FROM after column list at line {self.current_token().line}"
            )
        self.consume('KEYWORD')  # Consume 'FROM'
        
        # Parse table name
        table = self.consume('IDENTIFIER')
        
        # Optional WHERE clause
        where_clause = None
        if (self.current_token().type == 'KEYWORD' and 
            self.current_token().value.upper() == 'WHERE'):
            self.consume('KEYWORD')  # Consume 'WHERE'
            where_clause = self.parse_condition()
        
        # Expect semicolon at the end
        if self.current_token().type == 'SEMICOLON':
            self.consume('SEMICOLON')

        
        # Build AST
        return ASTNode('SELECT', value=None, children=[
            ASTNode('COLUMNS', value=columns),
            ASTNode('TABLE', value=table.value),
            ASTNode('WHERE', value=where_clause) if where_clause else None
        ])
    
    def parse_insert(self):
        """Parse INSERT statement"""
        self.consume('KEYWORD')  # Consume 'INSERT'
        
        # Expect INTO
        if self.current_token().value.upper() != 'INTO':
            raise SyntaxError(
                f"Expected INTO after INSERT at line {self.current_token().line}"
            )
        self.consume('KEYWORD')
        
        # Table name
        table = self.consume('IDENTIFIER')
        
        # Optional column list
        columns = None
        if self.current_token().type == 'LPAREN':
            self.consume('LPAREN')
            columns = self.parse_column_list()
            self.consume('RPAREN')
        
        # Expect VALUES
        if self.current_token().value.upper() != 'VALUES':
            raise SyntaxError(
                f"Expected VALUES at line {self.current_token().line}"
            )
        self.consume('KEYWORD')
        
        # Parse values
        self.consume('LPAREN')
        values = self.parse_value_list()
        self.consume('RPAREN')
        
        # Expect semicolon
        self.consume('SEMICOLON')
        
        return ASTNode('INSERT', children=[
            ASTNode('TABLE', value=table.value),
            ASTNode('COLUMNS', value=columns) if columns else None,
            ASTNode('VALUES', value=values)
        ])
    
    def parse_update(self):
        """Parse UPDATE statement"""
        self.consume('KEYWORD')  # Consume 'UPDATE'
        
        # Table name
        table = self.consume('IDENTIFIER')
        
        # Expect SET
        if self.current_token().value.upper() != 'SET':
            raise SyntaxError(
                f"Expected SET after table name at line {self.current_token().line}"
            )
        self.consume('KEYWORD')
        
        # Parse assignments (column = value)
        assignments = self.parse_assignment_list()
        
        # Optional WHERE clause
        where_clause = None
        if (self.current_token().type == 'KEYWORD' and 
            self.current_token().value.upper() == 'WHERE'):
            self.consume('KEYWORD')
            where_clause = self.parse_condition()
        
        # Expect semicolon
        self.consume('SEMICOLON')
        
        return ASTNode('UPDATE', children=[
            ASTNode('TABLE', value=table.value),
            ASTNode('ASSIGNMENTS', value=assignments),
            ASTNode('WHERE', value=where_clause) if where_clause else None
        ])
    
    def parse_delete(self):
        """Parse DELETE statement"""
        self.consume('KEYWORD')  # Consume 'DELETE'
        
        # Expect FROM
        if self.current_token().value.upper() != 'FROM':
            raise SyntaxError(
                f"Expected FROM after DELETE at line {self.current_token().line}"
            )
        self.consume('KEYWORD')
        
        # Table name
        table = self.consume('IDENTIFIER')
        
        # Optional WHERE clause
        where_clause = None
        if (self.current_token().type == 'KEYWORD' and 
            self.current_token().value.upper() == 'WHERE'):
            self.consume('KEYWORD')
            where_clause = self.parse_condition()
        
        # Expect semicolon
        self.consume('SEMICOLON')
        
        return ASTNode('DELETE', children=[
            ASTNode('TABLE', value=table.value),
            ASTNode('WHERE', value=where_clause) if where_clause else None
        ])
    
    def parse_create(self):
        """Parse CREATE TABLE statement"""
        self.consume('KEYWORD')  # Consume 'CREATE'
        
        # Expect TABLE
        if self.current_token().value.upper() != 'TABLE':
            raise SyntaxError(
                f"Expected TABLE after CREATE at line {self.current_token().line}"
            )
        self.consume('KEYWORD')
        
        # Table name i.e. it saves the token.value 
        table = self.consume('IDENTIFIER')
        
        # Column definitions
        self.consume('LPAREN')
        columns = self.parse_column_definitions()
        self.consume('RPAREN')
        
        # Expect semicolon
        self.consume('SEMICOLON')
        
        return ASTNode('CREATE_TABLE', children=[
            ASTNode('TABLE', value=table.value),
            ASTNode('COLUMNS', value=columns)
        ])
    
    def parse_drop(self):
        """Parse DROP TABLE statement"""
        self.consume('KEYWORD')  # Consume 'DROP'
        
        # Expect TABLE
        if self.current_token().value.upper() != 'TABLE':
            raise SyntaxError(
                f"Expected TABLE after DROP at line {self.current_token().line}"
            )
        self.consume('KEYWORD')
        
        # Table name
        table = self.consume('IDENTIFIER')
        
        # Expect semicolon
        self.consume('SEMICOLON')
        
        return ASTNode('DROP_TABLE', children=[
            ASTNode('TABLE', value=table.value)
        ])
    
    def parse_alter(self):
        """Parse ALTER TABLE statement (simplified)"""
        self.consume('KEYWORD')  # Consume 'ALTER'
        
        # Expect TABLE
        if self.current_token().value.upper() != 'TABLE':
            raise SyntaxError(
                f"Expected TABLE after ALTER at line {self.current_token().line}"
            )
        self.consume('KEYWORD')
        
        # Table name
        table = self.consume('IDENTIFIER')
        
        # Expect ADD or DROP or MODIFY
        action = self.current_token()
        if action.value.upper() not in ('ADD', 'DROP', 'MODIFY'):
            raise SyntaxError(
                f"Expected ADD, DROP, or MODIFY at line {action.line}"
            )
        self.consume('KEYWORD')
        
        # Optional COLUMN keyword
        if (
            self.current_token().type == 'KEYWORD'
            and self.current_token().value.upper() == 'COLUMN'
        ):
            self.consume('KEYWORD')
        
        # Parse column name
        column = self.consume('IDENTIFIER')
        
        # Optional data type (for ADD and MODIFY)
        data_type = None

        if action.value.upper() in ('ADD', 'MODIFY'):
            if self.current_token().type != 'IDENTIFIER':
                raise SyntaxError(
                    f"Expected data type after column name at line {self.current_token().line}"
                )
            data_type = self.consume('IDENTIFIER').value

        
        # Expect semicolon
        self.consume('SEMICOLON')
        
        return ASTNode('ALTER_TABLE', children=[
            ASTNode('TABLE', value=table.value),
            ASTNode('ACTION', value=action.value.upper()),
            ASTNode('COLUMN', value=column.value),
            ASTNode('DATATYPE', value=data_type) if data_type else None
        ])
    
    def parse_column_list(self):
        """Parse list of columns (e.g., col1, col2, *, 1)"""
        columns = []

        token = self.current_token()

        if token.type in ('STAR', 'WILDCARD'):
            self.consume()
            return ['*']

        while True:
            token = self.current_token()

            if token.type in ('IDENTIFIER', 'NUMBER'):
                columns.append(self.consume().value)
            else:
                raise SyntaxError(
                    f"Expected column name, number, or * at line {token.line}"
                )

            if self.current_token().type == 'COMMA':
                self.consume('COMMA')
                continue
            break

        return columns
    
    def parse_value_list(self):
        """Parse list of values"""
        values = []
        
        # Parse first value
        token = self.current_token()
        if token.type in ('STRING', 'NUMBER'):
            values.append(self.consume().value)
        else:
            raise SyntaxError(f"Expected value at line {token.line}")
        
        # Parse remaining values
        while self.current_token().type == 'COMMA':
            self.consume('COMMA')
            token = self.current_token()
            if token.type in ('STRING', 'NUMBER'):
                values.append(self.consume().value)
            else:
                raise SyntaxError(f"Expected value at line {token.line}")
        
        return values
    
    def parse_assignment_list(self):
        """Parse assignments (column = value, column2 = value2)"""
        assignments = []
        
        # Parse first assignment
        column = self.consume('IDENTIFIER').value
        self.consume('OPERATOR')  # Should be '='
        value = self.current_token()
        if value.type in ('STRING', 'NUMBER', 'IDENTIFIER'):
            assignments.append((column, self.consume().value))
        
        # Parse remaining assignments
        while self.current_token().type == 'COMMA':
            self.consume('COMMA')
            column = self.consume('IDENTIFIER').value
            self.consume('OPERATOR')
            value = self.current_token()
            if value.type in ('STRING', 'NUMBER', 'IDENTIFIER'):
                assignments.append((column, self.consume().value))
        
        return assignments
    
    def parse_condition(self):
        """Parse WHERE condition with nested SELECT support"""

        token = self.current_token()

        # EXISTS (subquery)
        if token.type == 'KEYWORD' and token.value.upper() == 'EXISTS':
            self.consume('KEYWORD')  # EXISTS
            self.consume('LPAREN')

            subquery = self.parse()  # nested SELECT

            self.consume('RPAREN')

            return ('EXISTS', subquery)

        # Left side (supports table.column)
        left = self.parse_identifier()

        operator_token = self.current_token()

        # IN (subquery)
        if operator_token.type == 'KEYWORD' and operator_token.value.upper() == 'IN':
            self.consume('KEYWORD')  # IN
            self.consume('LPAREN')

            subquery = self.parse()

            self.consume('RPAREN')

            return ('IN', left, subquery)

        # Normal operator
        operator = self.consume('OPERATOR').value

        # Right side (supports table.column)
        if self.current_token().type == 'IDENTIFIER':
            right = self.parse_identifier()
        elif self.current_token().type in ('STRING', 'NUMBER'):
            right = self.consume().value
        else:
            token = self.current_token()
            raise SyntaxError(
                f"Expected value in condition at line {token.line}"
            )

        return (left, operator, right)


    
    #---Helper----
    def parse_identifier(self):
        """Parse identifiers like: col, table.col, schema.table.col"""

        parts = [self.consume('IDENTIFIER').value]

        while self.current_token() and self.current_token().type == 'DOT':
            self.consume('DOT')
            parts.append(self.consume('IDENTIFIER').value)

        return ".".join(parts)

    
    def parse_column_definitions(self):
        """Parse column definitions in CREATE TABLE"""
        columns = []
        
        # Parse first column
        col_name = self.consume('IDENTIFIER').value
        col_type = self.consume('IDENTIFIER').value
        columns.append((col_name, col_type))
        
        # Parse remaining columns
        while self.current_token().type == 'COMMA':
            self.consume('COMMA')
            col_name = self.consume('IDENTIFIER').value
            col_type = self.consume('IDENTIFIER').value
            columns.append((col_name, col_type))
        
        return columns


# Example usage
if __name__ == "__main__":
    from lexer import Lexer
    
    lexer = Lexer()
    test_query = "SELECT name, age FROM users WHERE age > 18;"
    
    tokens = lexer.tokenize(test_query)
    parser = Parser(tokens)
    
    try:
        ast = parser.parse()
        print("Parsing successful!")
        print("AST:", ast)
    except SyntaxError as e:
        print("Parsing failed:", e)

