"""
Output Formatter Module - Formats validation results in different formats
"""

import json

class OutputFormatter:
    """Formats validation results for output"""
    
    def __init__(self):
        pass
    
    def format_text(self, query, result):
        """
        Format result as plain text
        
        Args:
            query: The SQL query string
            result: Validation result dictionary
            
        Returns:
            Formatted text string
        """
        output = []
        output.append("=" * 60)
        output.append("SQL QUERY VALIDATION RESULT")
        output.append("=" * 60)
        output.append(f"\nQuery: {query}")
        output.append(f"\nResult: {'SUCCESS' if result['success'] else 'FAILED'}")
        
        if result['success']:
            output.append("\nMessage: Query validated successfully")
        else:
            output.append("\n--- ERRORS ---")
            for error in result['errors']:
                output.append(f"\nError ID: {error.id}")
                output.append(f"Type: {error.type}")
                output.append(f"Message: {error.message}")
                output.append(f"Line: {error.line}, Column: {error.column}")
        
        if result.get('warnings'):
            output.append("\n--- WARNINGS ---")
            for warning in result['warnings']:
                output.append(f"\n{warning}")
        
        output.append("\n" + "=" * 60)
        
        return "\n".join(output)
    
    def format_json(self, query, result):
        """
        Format result as JSON
        
        Args:
            query: The SQL query string
            result: Validation result dictionary
            
        Returns:
            JSON string
        """
        output = {
            'query': query,
            'success': result['success'],
            'errors': [],
            'warnings': result.get('warnings', [])
        }
        
        # Convert error objects to dictionaries
        for error in result.get('errors', []):
            output['errors'].append({
                'id': error.id,
                'type': error.type,
                'message': error.message,
                'line': error.line,
                'column': error.column
            })
        
        return json.dumps(output, indent=2)
    
    def format_custom(self, query, result):
        """
        Format result in custom CSP format
        
        Args:
            query: The SQL query string
            result: Validation result dictionary
            
        Returns:
            Custom formatted string
        """
        output = []
        output.append("VALIDATION_REPORT")
        output.append(f"QUERY:{query}")
        output.append(f"STATUS:{'PASS' if result['success'] else 'FAIL'}")
        
        if not result['success']:
            output.append("ERRORS_START")
            for error in result['errors']:
                output.append(f"  ID={error.id}")
                output.append(f"  TYPE={error.type}")
                output.append(f"  MESSAGE={error.message}")
                output.append(f"  LOCATION=Line:{error.line},Col:{error.column}")
                output.append("  ---")
            output.append("ERRORS_END")
        
        output.append("END_REPORT")
        
        return "\n".join(output)
    
    def write_output(self, content, filepath):
        """
        Write formatted content to a file
        
        Args:
            content: The formatted content
            filepath: Path to output file
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"Error writing to file: {e}")
            return False


# Example usage
if __name__ == "__main__":
    from validator import ValidationError
    
    formatter = OutputFormatter()
    
    # Sample successful result
    test_query = "SELECT * FROM users;"
    success_result = {
        'success': True,
        'errors': [],
        'warnings': []
    }
    
    print("TEXT FORMAT:")
    print(formatter.format_text(test_query, success_result))
    print("\n" + "=" * 60 + "\n")
    
    # Sample failed result
    fail_result = {
        'success': False,
        'errors': [
            ValidationError('VAL_001', 'Validation', 'Table name missing', 1, 15)
        ],
        'warnings': []
    }
    
    print("JSON FORMAT:")
    print(formatter.format_json(test_query, fail_result))