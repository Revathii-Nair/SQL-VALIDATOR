"""
Configuration Module - Manages application settings
"""

class Config:
    """Stores configuration settings for the validator"""
    
    def __init__(self):
        # Default settings
        self.dialect = 'ANSI'  # SQL dialect (ANSI, MSSQL, etc.)
        self.max_query_length = 2000  # Maximum query length in characters
        self.output_format = 'text'  # Default output format (text, json, custom)
        self.strict_mode = False  # Enable strict validation
        self.show_warnings = True  # Show warnings along with errors
    
    def load_dialect(self, dialect_name):
        """
        Load a specific SQL dialect configuration
        
        Args:
            dialect_name: Name of the dialect ('ANSI', 'MSSQL', etc.)
        """
        self.dialect = dialect_name.upper()
        
        # You can extend this to load dialect-specific rules
        if self.dialect == 'MSSQL':
            # Load MSSQL-specific configurations
            self.dialect_keywords = ['TOP', 'NOLOCK']
        else:
            # Default ANSI
            self.dialect_keywords = []
    
    def set_output_format(self, format_type):
        """
        Set the output format
        
        Args:
            format_type: 'text', 'json', or 'custom'
        """
        if format_type.lower() in ['text', 'json', 'custom']:
            self.output_format = format_type.lower()
        else:
            print(f"Warning: Unknown format '{format_type}', using 'text'")
            self.output_format = 'text'
    
    def get_config_summary(self):
        """Return a summary of current configuration"""
        return {
            'dialect': self.dialect,
            'max_query_length': self.max_query_length,
            'output_format': self.output_format,
            'strict_mode': self.strict_mode,
            'show_warnings': self.show_warnings
        }


class ConfigManager:
    """Manages configuration loading and saving"""
    
    def __init__(self):
        self.config = Config()
    
    def load_options(self, options_dict):
        """
        Load options from a dictionary
        
        Args:
            options_dict: Dictionary with configuration options
        """
        if 'dialect' in options_dict:
            self.config.load_dialect(options_dict['dialect'])
        
        if 'format' in options_dict:
            self.config.set_output_format(options_dict['format'])
        
        if 'strict' in options_dict:
            self.config.strict_mode = options_dict['strict']
    
    def get_config(self):
        """Return the current configuration object"""
        return self.config


# Example usage
if __name__ == "__main__":
    manager = ConfigManager()
    
    # Load some options
    options = {
        'dialect': 'ANSI',
        'format': 'json',
        'strict': False
    }
    
    manager.load_options(options)
    
    # Get config summary
    config = manager.get_config()
    print("Current configuration:")
    print(config.get_config_summary())