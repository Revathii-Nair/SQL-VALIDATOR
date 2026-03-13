"""
Error Handler Module - Collects and formats errors
"""

class ErrorHandler:
    """Handles error collection and formatting"""
    
    def __init__(self):
        self.error_stack = []
    
    def collect(self, error):
        """
        Add an error to the stack
        
        Args:
            error: Error object (from lexer, parser, or validator)
        """
        self.error_stack.append(error)
    
    def get_errors(self):
        """Return all collected errors"""
        return self.error_stack
    
    def clear(self):
        """Clear all errors"""
        self.error_stack = []
    
    def format_error(self, error):
        """
        Format a single error for display
        
        Args:
            error: Error object
            
        Returns:
            Formatted error string
        """
        if hasattr(error, 'id'):
            # Validation error
            return (
                f"Error ID: {error.id}\n"
                f"Type: {error.type}\n"
                f"Message: {error.message}\n"
                f"Line: {error.line}, Column: {error.column}\n"
            )
        else:
            # Standard Python exception
            return f"Error: {str(error)}\n"
    
    def format_all_errors(self):
        """
        Format all errors for display
        
        Returns:
            String with all formatted errors
        """
        if not self.error_stack:
            return "No errors"
        
        output = []
        output.append("=" * 60)
        output.append("ERRORS DETECTED")
        output.append("=" * 60)
        
        for i, error in enumerate(self.error_stack, 1):
            output.append(f"\n--- Error {i} ---")
            output.append(self.format_error(error))
        
        return "\n".join(output)


# Example usage
if __name__ == "__main__":
    from validator import ValidationError
    
    handler = ErrorHandler()
    
    # Add some sample errors
    handler.collect(ValidationError(
        'VAL_001',
        'Validation',
        'Table name is missing',
        1, 20
    ))
    
    handler.collect(ValidationError(
        'SYNTAX_002',
        'Syntax',
        'Expected semicolon',
        1, 30
    ))
    
    # Display all errors
    print(handler.format_all_errors())