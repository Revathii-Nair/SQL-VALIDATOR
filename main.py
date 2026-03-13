"""
ANSI SQL Query Validator - Main Entry Point
This is where the program starts running
"""

from cli import CLIEngine

def main():
    """Start the application"""
    print("=" * 60)
    print("ANSI SQL Query Validator")
    print("=" * 60)
    print()
    
    # Create and run the CLI
    cli = CLIEngine()
    cli.run()

if __name__ == "__main__":
    main()