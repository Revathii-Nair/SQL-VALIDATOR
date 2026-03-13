"""
CLI Engine - Custom Command Line Interface with Rich Animations
"""

import sys
from time import sleep
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.text import Text
from lexer import Lexer
from parser import Parser
from validator import Validator
from error_handler import ErrorHandler
from output_formatter import OutputFormatter
from config import ConfigManager


class CLIEngine:
    """Custom CLI for SQL Query Validator with Rich Animations"""

    def __init__(self):
        self.lexer = Lexer()
        self.error_handler = ErrorHandler()
        self.output_formatter = OutputFormatter()
        self.config_manager = ConfigManager()
        self.running = True
        self.console = Console()

    def display_menu(self):
        """Display the main menu"""
        self.console.print("\n" + "=" * 60, style="bold green")
        self.console.print("[bold cyan]ANSI SQL QUERY VALIDATOR - MAIN MENU[/bold cyan]")
        self.console.print("=" * 60)
        self.console.print("[bold]1.[/bold] Validate inline SQL query")
        self.console.print("[bold]2.[/bold] Validate SQL from file")
        self.console.print("[bold]3.[/bold] Configure settings")
        self.console.print("[bold]4.[/bold] Display help")
        self.console.print("[bold]5.[/bold] Exit")
        self.console.print("=" * 60)

    def get_user_choice(self):
        """Get user's menu choice"""
        while True:
            choice = self.console.input("\nEnter your choice (1-5): ").strip()
            if choice in ['1', '2', '3', '4', '5']:
                return choice
            self.console.print("[red]Invalid choice. Enter 1-5.[/red]")

    def validate_query(self, query):
        """Validate a single SQL query with Rich animations"""
        self.console.print("\n[bold yellow]Validating query...[/bold yellow]\n")
        self.console.print(Panel(Text(query, style="bold white"), title="Query"))

        try:
            with Progress(
                SpinnerColumn(spinner_name="dots", style="cyan"),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                transient=True,
            ) as progress:
                # Lexical Analysis
                lex_task = progress.add_task("[cyan]Lexical analysis...", total=100)
                for _ in range(5):
                    sleep(0.15)
                    progress.update(lex_task, advance=20)
                tokens = self.lexer.tokenize(query)
                progress.update(lex_task, description=f"Tokens generated: {len(tokens)}")

                # Syntax Analysis
                parse_task = progress.add_task("[cyan]Syntax analysis...", total=100)
                parser = Parser(tokens)
                ast = parser.parse()
                for _ in range(4):
                    sleep(0.15)
                    progress.update(parse_task, advance=25)
                progress.update(parse_task, description="[green]Parse successful![/green]")

                # Validation
                validate_task = progress.add_task("[cyan]Validation...", total=100)
                validator = Validator(self.config_manager.get_config())
                result = validator.validate(ast)
                for _ in range(4):
                    sleep(0.15)
                    progress.update(validate_task, advance=25)
                progress.update(validate_task, description="[green]Validation complete![/green]")

            return result

        except SyntaxError as e:
            return {
                'success': False,
                'errors': [type('Error', (), {
                    'id': 'SYNTAX_001',
                    'type': 'Syntax',
                    'message': str(e),
                    'line': 0,
                    'column': 0
                })()],
                'warnings': []
            }
        except Exception as e:
            return {
                'success': False,
                'errors': [type('Error', (), {
                    'id': 'ERR_001',
                    'type': 'General',
                    'message': str(e),
                    'line': 0,
                    'column': 0
                })()],
                'warnings': []
            }

    def handle_inline_query(self):
        """Handle inline query validation"""
        self.console.print("\n" + "-" * 60, style="bold green")
        self.console.print("INLINE QUERY VALIDATION", style="bold cyan")
        self.console.print("-" * 60)
        self.console.print("Enter your SQL query (end with semicolon). Type 'cancel' to go back.\n")

        lines = []
        while True:
            line = self.console.input()
            if line.strip().lower() == 'cancel':
                self.console.print("[yellow]Cancelled.[/yellow]")
                return
            lines.append(line)
            if ';' in line:
                break

        query = '\n'.join(lines)
        result = self.validate_query(query)
        self.display_result(query, result)
        self.ask_save_output(query, result)

    def handle_file_query(self):
        """Handle file-based query validation"""
        self.console.print("\n" + "-" * 60, style="bold green")
        self.console.print("FILE QUERY VALIDATION", style="bold cyan")
        self.console.print("-" * 60)

        filepath = self.console.input("Enter the path to SQL file: ").strip()

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            queries = [q.strip() + ';' for q in content.split(';') if q.strip()]
            self.console.print(f"\nFound {len(queries)} queries in file")

            with Progress(
                SpinnerColumn(),
                TextColumn("{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                transient=True
            ) as progress:
                file_task = progress.add_task("[cyan]Processing queries...", total=len(queries))
                for i, query in enumerate(queries, 1):
                    progress.update(file_task, description=f"Query {i}/{len(queries)}")
                    result = self.validate_query(query)
                    self.display_result(query, result)
                    progress.advance(file_task)
                    sleep(0.1)

            save = self.console.input("\nSave all results to file? (yes/no): ").strip().lower()
            if save == 'yes':
                output_file = self.console.input("Enter output filename: ").strip()
                self.save_batch_results(queries, output_file)

        except FileNotFoundError:
            self.console.print(f"[red]Error: File '{filepath}' not found[/red]")
        except Exception as e:
            self.console.print(f"[red]Error reading file: {e}[/red]")

    def display_result(self, query, result):
        """Display validation result with Rich Panel"""
        config = self.config_manager.get_config()
        if config.output_format == 'json':
            output = self.output_formatter.format_json(query, result)
        elif config.output_format == 'custom':
            output = self.output_formatter.format_custom(query, result)
        else:
            output = self.output_formatter.format_text(query, result)

        panel = Panel(output, title="[bold green]Validation Result[/bold green]", border_style="green")
        self.console.print(panel)

    def ask_save_output(self, query, result):
        """Ask user if they want to save the output"""
        save = self.console.input("\nSave output to file? (yes/no): ").strip().lower()
        if save == 'yes':
            filename = self.console.input("Enter output filename (e.g., result.txt): ").strip()
            config = self.config_manager.get_config()
            if config.output_format == 'json':
                content = self.output_formatter.format_json(query, result)
            elif config.output_format == 'custom':
                content = self.output_formatter.format_custom(query, result)
            else:
                content = self.output_formatter.format_text(query, result)
            if self.output_formatter.write_output(content, filename):
                self.console.print(f"[green]Output saved to {filename}[/green]")
            else:
                self.console.print("[red]Failed to save output[/red]")

    def save_batch_results(self, queries, output_file):
        """Save results from multiple queries"""
        all_results = []
        for query in queries:
            result = self.validate_query(query)
            config = self.config_manager.get_config()
            if config.output_format == 'json':
                content = self.output_formatter.format_json(query, result)
            elif config.output_format == 'custom':
                content = self.output_formatter.format_custom(query, result)
            else:
                content = self.output_formatter.format_text(query, result)
            all_results.append(content)
        final_content = "\n\n".join(all_results)
        if self.output_formatter.write_output(final_content, output_file):
            self.console.print(f"[green]All results saved to {output_file}[/green]")
        else:
            self.console.print("[red]Failed to save results[/red]")

    def configure_settings(self):
        """Configure application settings"""
        self.console.print("\n" + "-" * 60, style="bold green")
        self.console.print("CONFIGURATION", style="bold cyan")
        self.console.print("-" * 60)

        config = self.config_manager.get_config()
        self.console.print(f"\nCurrent settings:")
        self.console.print(f"1. SQL Dialect: {config.dialect}")
        self.console.print(f"2. Output Format: {config.output_format}")
        self.console.print(f"3. Strict Mode: {config.strict_mode}")
        self.console.print(f"4. Back to main menu")

        choice = self.console.input("\nWhat would you like to change? (1-4): ").strip()
        if choice == '1':
            self.console.print("\nAvailable dialects: ANSI, MSSQL")
            dialect = self.console.input("Enter dialect: ").strip()
            config.load_dialect(dialect)
            self.console.print(f"[green]Dialect set to {config.dialect}[/green]")
        elif choice == '2':
            self.console.print("\nAvailable formats: text, json, custom")
            format_type = self.console.input("Enter format: ").strip()
            config.set_output_format(format_type)
            self.console.print(f"[green]Output format set to {config.output_format}[/green]")
        elif choice == '3':
            strict = self.console.input("Enable strict mode? (yes/no): ").strip().lower()
            config.strict_mode = (strict == 'yes')
            self.console.print(f"[green]Strict mode: {config.strict_mode}[/green]")
        elif choice == '4':
            return

    def display_help(self):
        """Display help information"""
        self.console.print("\n" + "=" * 60, style="bold green")
        self.console.print("HELP - SQL QUERY VALIDATOR", style="bold cyan")
        self.console.print("=" * 60)

        help_text = """
This tool validates SQL queries without executing them.

SUPPORTED SQL COMMANDS:
- SELECT: Query data from tables
- INSERT: Add new data to tables
- UPDATE: Modify existing data
- DELETE: Remove data from tables
- CREATE TABLE: Create new tables
- DROP TABLE: Delete tables
- ALTER TABLE: Modify table structure

FEATURES:
1. Inline validation: Type queries directly
2. File validation: Validate queries from .sql files
3. Multiple output formats: text, JSON, custom
4. Batch processing: Validate multiple queries at once

USAGE TIPS:
- Always end queries with a semicolon (;)
- Use valid SQL syntax
- Check error messages for specific issues

EXAMPLE QUERIES:
  SELECT * FROM users;
  INSERT INTO users (name, age) VALUES ('John', 25);
  UPDATE users SET age = 26 WHERE name = 'John';
  DELETE FROM users WHERE age < 18;
  CREATE TABLE students (id INT, name VARCHAR);
  DROP TABLE students;
        """
        self.console.print(Panel(help_text, title="[bold green]Help[/bold green]"))
        self.console.input("\nPress Enter to continue...")

    def run(self):
        """Main CLI loop"""
        self.console.print("[bold magenta]Welcome to ANSI SQL Query Validator![/bold magenta]\n")
        while self.running:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == '1':
                self.handle_inline_query()
            elif choice == '2':
                self.handle_file_query()
            elif choice == '3':
                self.configure_settings()
            elif choice == '4':
                self.display_help()
            elif choice == '5':
                self.console.print("\n[bold green]Thank you for using SQL Query Validator![/bold green]")
                self.running = False


if __name__ == "__main__":
    cli = CLIEngine()
    cli.run()
