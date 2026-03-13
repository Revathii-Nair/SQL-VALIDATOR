# ANSI SQL Query Validator

A simple command-line tool to validate SQL queries without executing them.

## What This Project Does

This tool checks if your SQL queries are written correctly. It's like a spell-checker for SQL code. It doesn't run the queries or connect to any database - it just checks if they follow proper SQL rules.

## Requirements

- Python 3.6 or higher
- No external libraries needed (uses only built-in Python modules)

## Project Structure

```
sql_validator/
├── main.py              # Start the program here
├── cli.py               # User interface
├── lexer.py             # Breaks SQL into pieces (tokens)
├── parser.py            # Checks if pieces are in correct order
├── validator.py         # Final validation checks
├── error_handler.py     # Manages errors
├── output_formatter.py  # Formats results
├── config.py            # Settings
├── app.py            # UI based app
├── test_queries.sql     # Sample queries to test
├── queries.sql     # Sample queries to test
├── implementation_guide.txt
├── test/
    ├── test_engine.py
    ├── test_lexer.py
    ├── conftest.py
    ├── test_parser.py
    ├── test_validator.py
└── README.md            # This file
```

## How to Run the Program

### Step 1: Open Command Prompt/Terminal

**On Windows:**

- Press `Windows Key + R`
- Type `cmd` and press Enter

**On Mac/Linux:**

- Open Terminal application

### Step 2: Navigate to Project Folder

```bash
cd path/to/sql_validator
```

Example:

```bash
cd C:\Users\YourName\Desktop\sql_validator
```

### Step 3: Run the Program

```bash
python main.py
```

## How to Use the Validator

Once you run the program, you'll see a menu with 5 options:

### Option 1: Validate Inline Query

This lets you type a SQL query directly.

**Example:**

```
Enter your choice: 1
Enter your SQL query:
SELECT name FROM users;
```

The program will tell you if it's valid or show errors.

### Option 2: Validate from File

This validates all queries in a file.

**Example:**

```
Enter your choice: 2
Enter the path to SQL file: test_queries.sql
```

The program will check each query in the file.

### Option 3: Configure Settings

Change how the validator works:

- **SQL Dialect**: Choose ANSI (default) or MSSQL
- **Output Format**: Choose text, json, or custom
- **Strict Mode**: Enable/disable extra checks

### Option 4: Display Help

Shows information about supported SQL commands and usage tips.

### Option 5: Exit

Quit the program.

## Supported SQL Commands

The validator supports these SQL commands:

### DML (Data Manipulation)

- **SELECT**: Get data from tables
- **INSERT**: Add new data
- **UPDATE**: Change existing data
- **DELETE**: Remove data

### DDL (Data Definition)

- **CREATE TABLE**: Make new tables
- **DROP TABLE**: Delete tables
- **ALTER TABLE**: Change table structure

## Example Queries

### Valid Queries:

```sql
-- Simple SELECT
SELECT * FROM users;

-- SELECT with WHERE clause
SELECT name, age FROM users WHERE age > 18;

-- INSERT with all columns
INSERT INTO users (name, age) VALUES ('John', 25);

-- UPDATE with condition
UPDATE users SET age = 26 WHERE name = 'John';

-- DELETE with condition
DELETE FROM users WHERE age < 18;

-- CREATE TABLE
CREATE TABLE students (id INT, name VARCHAR);

-- DROP TABLE
DROP TABLE students;

-- ALTER TABLE
ALTER TABLE users ADD email VARCHAR;
```

### Invalid Queries (These will show errors):

```sql
-- Missing semicolon
SELECT * FROM users

-- Missing FROM keyword
SELECT name WHERE age > 18;

-- Missing table name
SELECT * FROM;

-- Wrong column count in INSERT
INSERT INTO users (name) VALUES ('John', 25);
```

## Understanding the Output

### Success Example:

```
============================================================
SQL QUERY VALIDATION RESULT
============================================================

Query: SELECT * FROM users;

Result: SUCCESS

Message: Query validated successfully
============================================================
```

### Error Example:

```
============================================================
SQL QUERY VALIDATION RESULT
============================================================

Query: SELECT * FROM

Result: FAILED

--- ERRORS ---

Error ID: SYNTAX_001
Type: Syntax
Message: Expected IDENTIFIER but got KEYWORD at line 1, column 15
Line: 1, Column: 15
============================================================
```

## Output Formats

### Text Format (Default)

Easy to read, good for viewing on screen.

### JSON Format

Structured format, good for processing by other programs.

Example:

```json
{
  "query": "SELECT * FROM users;",
  "success": true,
  "errors": [],
  "warnings": []
}
```

### Custom Format

Special format for integration with other tools.

## Saving Results

After validation, the program asks:

```
Save output to file? (yes/no):
```

Type `yes` and enter a filename to save results.

## Testing the Validator

A test file `test_queries.sql` is included with sample queries.

**To test:**

1. Run the program: `python main.py`
2. Choose option 2 (Validate from file)
3. Enter: `test_queries.sql`
4. See results for all queries

## Troubleshooting

### Problem: "python is not recognized"

**Solution:**

- Make sure Python is installed
- Try `python3` instead of `python`

### Problem: "No module named 'lexer'"

**Solution:**

- Make sure you're in the correct folder
- All files should be in the same folder

### Problem: "File not found"

**Solution:**

- Check the file path is correct
- Use full path if needed: `C:\Users\Name\file.sql`

## How It Works (Simple Explanation)

1. **Lexer** - Breaks your SQL into small pieces (like words in a sentence)
2. **Parser** - Checks if pieces are in the right order (like grammar check)
3. **Validator** - Applies SQL rules to make sure everything makes sense

Think of it like checking an essay:

- Lexer = Breaking into words
- Parser = Checking grammar
- Validator = Making sure it makes sense

## Project Limitations

- Does NOT execute queries
- Does NOT connect to databases
- Does NOT check if tables/columns actually exist
- Only validates syntax and structure

## Need Help?

If you get stuck:

1. Check the error message carefully
2. Look at the example queries
3. Make sure your query ends with a semicolon (;)
4. Check spelling of SQL keywords (SELECT, FROM, WHERE, etc.)

## Quick Reference Card

```
VALID QUERY CHECKLIST:
☑ Starts with SQL keyword (SELECT, INSERT, etc.)
☑ Has table name after FROM (for SELECT/DELETE)
☑ Has table name after INTO (for INSERT)
☑ Has table name before SET (for UPDATE)
☑ Ends with semicolon (;)
☑ Parentheses are balanced ( )
☑ String values in single quotes 'like this'
```

# UML DIAGRAMS

![WhatsApp Image 2026-02-03 at 9 54 57 PM](https://github.com/user-attachments/assets/57197b9a-8314-4d89-91b9-c1da83657f51 'Sequence Diagram')
![WhatsApp Image 2026-02-03 at 9 59 22 PM](https://github.com/user-attachments/assets/6973c6b1-b204-4c27-9f27-5d54b3a1a6f1 'Flow chart')

![WhatsApp Image 2026-02-03 at 10 04 41 PM](https://github.com/user-attachments/assets/7d95e5b1-aeb0-4e8c-8760-cb67a31ab7af 'Class Diagram')
![WhatsApp Image 2026-02-03 at 10 50 13 PM](https://github.com/user-attachments/assets/135f74ec-1e42-48bd-bb3d-5cd87abf7202 'Componenet Diagram')
