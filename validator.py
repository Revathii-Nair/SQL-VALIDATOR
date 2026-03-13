"""
Validator Module - Final validation checks on the parsed query
Applies ANSI SQL rules
"""

class ValidationError:
    """Represents a validation error"""
    
    def __init__(self, error_id, error_type, message, line=0, column=0):
        self.id = error_id
        self.type = error_type
        self.message = message
        self.line = line
        self.column = column
    
    def __repr__(self):
        return (f"ValidationError(ID: {self.id}, Type: {self.type}, "
                f"Message: {self.message}, Line: {self.line}, Col: {self.column})")


class Validator:
    """Validates parsed SQL queries against ANSI SQL rules"""
    
    def __init__(self, config=None):
        self.config = config
        self.errors = []
    
    def validate(self, ast):
        """
        Validate the Abstract Syntax Tree
        
        Args:
            ast: The AST from the parser
            
        Returns:
            Dictionary with validation results
        """
        self.errors = []
        
        try:
            # Route to appropriate validation method
            if ast.type == 'SELECT':
                self.validate_select(ast)
            elif ast.type == 'INSERT':
                self.validate_insert(ast)
            elif ast.type == 'UPDATE':
                self.validate_update(ast)
            elif ast.type == 'DELETE':
                self.validate_delete(ast)
            elif ast.type == 'CREATE_TABLE':
                self.validate_create_table(ast)
            elif ast.type == 'DROP_TABLE':
                self.validate_drop_table(ast)
            elif ast.type == 'ALTER_TABLE':
                self.validate_alter_table(ast)
            
            # If no errors, validation passed
            if not self.errors:
                return {
                    'success': True,
                    'errors': [],
                    'warnings': []
                }
            else:
                return {
                    'success': False,
                    'errors': self.errors,
                    'warnings': []
                }
        
        except Exception as e:
            # Catch any unexpected errors
            self.errors.append(ValidationError(
                'VAL_000',
                'Validation',
                f"Validation error: {str(e)}",
                0, 0
            ))
            return {
                'success': False,
                'errors': self.errors,
                'warnings': []
            }
    
    def validate_select(self, ast):
        """Validate SELECT statement"""
        # Get children nodes
        columns_node = None
        table_node = None
        where_node = None
        
        for child in ast.children:
            if child is None:
                continue
            if child.type == 'COLUMNS':
                columns_node = child
            elif child.type == 'TABLE':
                table_node = child
            elif child.type == 'WHERE':
                where_node = child
        
        # Check if table exists
        if not table_node or not table_node.value:
            self.errors.append(ValidationError(
                'VAL_001',
                'Validation',
                'SELECT statement must have a table name',
                0, 0
            ))
        
        # Check if columns exist
        if not columns_node or not columns_node.value:
            self.errors.append(ValidationError(
                'VAL_002',
                'Validation',
                'SELECT statement must have column list',
                0, 0
            ))
            
        if where_node and isinstance(where_node.value, tuple):
            if where_node.value[0] == 'IN':
                subquery_ast = where_node.value[2]

                # Ensure it's an AST node before validating
                if hasattr(subquery_ast, "type"):
                    self.validate(subquery_ast)
                    
            if where_node.value[0] == 'EXISTS':
                subquery_ast = where_node.value[1]

                # Ensure it's an AST node before validating
                if hasattr(subquery_ast, "type"):
                    self.validate(subquery_ast)

        
        # Additional ANSI SQL rules can be added here
    
    def validate_insert(self, ast):
        """Validate INSERT statement"""
        table_node = None
        values_node = None
        columns_node = None
        
        for child in ast.children:
            if child is None:
                continue
            if child.type == 'TABLE':
                table_node = child
            elif child.type == 'VALUES':
                values_node = child
            elif child.type == 'COLUMNS':
                columns_node = child
        
        # Check table
        if not table_node or not table_node.value:
            self.errors.append(ValidationError(
                'VAL_003',
                'Validation',
                'INSERT statement must have a table name',
                0, 0
            ))
        
        # Check values
        if not values_node or not values_node.value:
            self.errors.append(ValidationError(
                'VAL_004',
                'Validation',
                'INSERT statement must have values',
                0, 0
            ))
        
        # If both columns and values exist, check if counts match
        if columns_node and columns_node.value and values_node and values_node.value:
            if len(columns_node.value) != len(values_node.value):
                self.errors.append(ValidationError(
                    'VAL_005',
                    'Validation',
                    f'Column count ({len(columns_node.value)}) does not match value count ({len(values_node.value)})',
                    0, 0
                ))
    
    def validate_update(self, ast):
        """Validate UPDATE statement"""
        table_node = None
        assignments_node = None
        
        for child in ast.children:
            if child is None:
                continue
            if child.type == 'TABLE':
                table_node = child
            elif child.type == 'ASSIGNMENTS':
                assignments_node = child
        
        # Check table
        if not table_node or not table_node.value:
            self.errors.append(ValidationError(
                'VAL_006',
                'Validation',
                'UPDATE statement must have a table name',
                0, 0
            ))
        
        # Check assignments
        if not assignments_node or not assignments_node.value:
            self.errors.append(ValidationError(
                'VAL_007',
                'Validation',
                'UPDATE statement must have at least one assignment',
                0, 0
            ))
    
    def validate_delete(self, ast):
        """Validate DELETE statement"""
        table_node = None
        
        for child in ast.children:
            if child is None:
                continue
            if child.type == 'TABLE':
                table_node = child
        
        # Check table
        if not table_node or not table_node.value:
            self.errors.append(ValidationError(
                'VAL_008',
                'Validation',
                'DELETE statement must have a table name',
                0, 0
            ))
    
    def validate_create_table(self, ast):
        """Validate CREATE TABLE statement"""
        table_node = None
        columns_node = None
        
        for child in ast.children:
            if child is None:
                continue
            if child.type == 'TABLE':
                table_node = child
            elif child.type == 'COLUMNS':
                columns_node = child
        
        # Check table name
        if not table_node or not table_node.value:
            self.errors.append(ValidationError(
                'VAL_009',
                'Validation',
                'CREATE TABLE statement must have a table name',
                0, 0
            ))
        
        # Check columns
        if not columns_node or not columns_node.value:
            self.errors.append(ValidationError(
                'VAL_010',
                'Validation',
                'CREATE TABLE statement must have at least one column',
                0, 0
            ))
    
    def validate_drop_table(self, ast):
        """Validate DROP TABLE statement"""
        table_node = None
        
        for child in ast.children:
            if child is None:
                continue
            if child.type == 'TABLE':
                table_node = child
        
        # Check table name
        if not table_node or not table_node.value:
            self.errors.append(ValidationError(
                'VAL_011',
                'Validation',
                'DROP TABLE statement must have a table name',
                0, 0
            ))
    
    def validate_alter_table(self, ast):
        """Validate ALTER TABLE statement"""
        table_node = None
        action_node = None
        column_node = None
        
        for child in ast.children:
            if child is None:
                continue
            if child.type == 'TABLE':
                table_node = child
            elif child.type == 'ACTION':
                action_node = child
            elif child.type == 'COLUMN':
                column_node = child
        
        # Check table name
        if not table_node or not table_node.value:
            self.errors.append(ValidationError(
                'VAL_012',
                'Validation',
                'ALTER TABLE statement must have a table name',
                0, 0
            ))
        
        # Check action
        if not action_node or not action_node.value:
            self.errors.append(ValidationError(
                'VAL_013',
                'Validation',
                'ALTER TABLE statement must have an action (ADD/DROP/MODIFY)',
                0, 0
            ))
        
        # Check column
        if not column_node or not column_node.value:
            self.errors.append(ValidationError(
                'VAL_014',
                'Validation',
                'ALTER TABLE statement must specify a column',
                0, 0
            ))


# Example usage
if __name__ == "__main__":
    from lexer import Lexer
    from parser import Parser
    
    lexer = Lexer()
    test_query = "SELECT name, age FROM users WHERE age > 18;"
    
    tokens = lexer.tokenize(test_query)
    parser = Parser(tokens)
    ast = parser.parse()
    
    validator = Validator()
    result = validator.validate(ast)
    
    print("Validation result:", result)