# SQL-of-Thought

An intelligent SQL query generation and error correction system that leverages LLMs (OpenAI) to translate natural language questions into executable SQL queries with automated error detection and correction.

This project is inspired by the [**SQL-of-Thought**](https://www.arxiv.org/pdf/2509.00581) paper, which proposes a chain-of-thought approach for improving SQL generation accuracy through multi-step reasoning and iterative refinement.

## Overview

SQL-of-Thought implements a multi-agent pipeline that:

1. **Schema Linking** - Identifies relevant tables and columns from the database schema
2. **Intent Classification** - Classifies the user's query intent (SELECT, INSERT, UPDATE, DELETE, etc.)
3. **Query Planning** - Generates a logical query plan from the natural language question
4. **SQL Generation** - Converts the logical plan into executable SQL
5. **SQL Execution** - Runs the query against the database
6. **Error Correction** - Automatically detects and corrects SQL errors using a taxonomy-based approach

## Model Configuration

This project uses **GPT-4.1-mini** as the default LLM:

- Fast inference
- Cost-effective for high-volume query generation
- Sufficient accuracy for SQL generation and error correction
- Can be swapped for GPT-4 or later versions by updating model names in agent files

To use a different model, update the `model` parameter in agent function calls:

```python
correction_plan_from_runtime(question, schema, sql, error, model="gpt-4")
```

## Project Structure

```
sql-of-thought/
├── agents/                          # AI agent modules
│   ├── schema_linking_agent.py      # Links NL to schema
│   ├── intent_classifier_agent.py   # Classifies query intent
│   ├── query_planning_agent.py      # Generates logical plans
│   ├── sql_generator_agent.py       # Converts plans to SQL
│   ├── sql_execution_agent.py       # Executes SQL queries
│   └── error_correction_agent.py    # Error detection & correction
├── config/                          # Configuration files
│   ├── schema.json                  # Database schema
│   ├── error_taxonomy.json          # Error classification taxonomy
│   └── error_priority.json          # Error priority levels
├── utils/                           # Utility modules
│   └── openai_client.py             # OpenAI API client
├── pipeline.py                      # Main execution pipeline
├── create_db.py                     # Database initialization
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

## Installation

### Prerequisites

- Python 3.8+
- OpenAI API key

### Setup

1. **Clone/Download the project**

   ```bash
   cd sql-of-thought
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   Create a `.env` file in the project root:

   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Initialize database** (if needed)
   ```bash
   python create_db.py
   ```

## Usage

### Running the Full Pipeline

```python
from pipeline import run_full_pipeline

result = run_full_pipeline("What are the top 10 users by order amount?", max_iterations=5)

print(f"SQL: {result['final_sql']}")
print(f"Result: {result['result']}")
print(f"Success: {result['success']}")
print(f"Iterations: {result['iterations']}")
```

### Pipeline Response Format

```json
{
    "final_sql": "SELECT * FROM users WHERE id IN (...)",
    "result": [{"id": 1, "name": "John", ...}, ...],
    "success": true,
    "iterations": 2
}
```

## Error Correction System

The error correction agent uses a comprehensive taxonomy to identify and fix SQL errors:

### Error Categories

- **Syntax Errors** - Malformed SQL syntax, invalid aliases
- **Schema Linking** - Missing tables/columns, ambiguous references
- **Join Issues** - Missing or incorrectly typed joins
- **Filter Problems** - Missing WHERE clauses, wrong conditions
- **Aggregation Errors** - Incorrect GROUP BY, HAVING usage
- **Ordering Issues** - Invalid ORDER BY specifications

### How It Works

1. Detects runtime errors during execution
2. Classifies error against the taxonomy
3. Generates a high-level correction plan
4. Applies the fix to the SQL query
5. Re-executes and validates

## Configuration

### Database Schema (`config/schema.json`)

Define your tables and columns:

```json
{
  "users": {
    "id": "INTEGER",
    "name": "TEXT",
    "country": "TEXT",
    "signup_date": "TEXT"
  },
  "orders": {
    "id": "INTEGER",
    "user_id": "INTEGER",
    "amount": "REAL",
    "created_at": "TEXT"
  }
}
```

### Error Taxonomy (`config/error_taxonomy.json`)

Customize error categories and error codes for your domain.

## Key Modules

### `pipeline.py`

Main orchestration logic that runs all agents in sequence with error correction loop.

### `agents/error_correction_agent.py`

- `correction_plan_from_runtime()` - Analyzes runtime errors and generates fix plans
- `apply_correction_to_sql()` - Applies correction plans to SQL queries

### `utils/openai_client.py`

Singleton OpenAI client instance for all agents to use.

## Environment Variables

- `OPENAI_API_KEY` - Your OpenAI API key (required)

## Dependencies

- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `sqlite3` - Database (built-in)

## Troubleshooting

### ModuleNotFoundError: No module named 'utils'

Ensure the project root is in your Python path or run scripts from the project root directory.

### OpenAI API Errors

- Verify `OPENAI_API_KEY` is set in `.env`
- Check your OpenAI account has available credits
- Ensure you have permission to use GPT-4 or specified model

### Database Errors

- Run `create_db.py` to initialize the database
- Verify `schema.json` matches your database structure

## Example: Full Pipeline Execution

### Example demo database (demo.db)

The repository includes a small example SQLite database (demo.db) used by the demos and tests. Location: project root (demo.db).

Schema

- users
  - id INTEGER PRIMARY KEY
  - name TEXT
  - country TEXT
  - signup_date TEXT
- orders
  - id INTEGER PRIMARY KEY
  - user_id INTEGER -- FK -> users.id
  - amount REAL
  - created_at TEXT

Relationships

- orders.user_id references users.id (one-to-many: one user can have many orders)

Sample rows

- users
  - (4, "Hana", "USA", "2023-09-27")
  - (11, "Charlie", "USA", "2024-09-12")
  - (19, "Bob", "USA", "2024-05-16")
- orders
  - (1, 4, 120.50, "2024-01-05")
  - (2, 11, 45.00, "2024-02-13")
  - (3, 19, 75.25, "2024-03-20")

Quick commands

- Create / populate (if you have create_db.py):

```bash
python create_db.py
```

- Print all tables as pandas DataFrames:

```powershell
python print_db_df.py demo.db
```

Notes

- The example DB is intentionally small to make pipeline debugging and error-correction demonstrations deterministic.

### Input

**Question:** "Show me the users in the USA."

**Detected Schema:**

```json
{
  "tables": {
    "users": ["id", "name", "country"]
  },
  "reasoning": "The users table contains the country column needed to filter users by location."
}
```

**Intent Classification:** `filter`

**Query Plan:**

```json
{
  "select": ["id", "name", "country"],
  "from": "users",
  "where": { "country": "USA" }
}
```

### Pipeline Execution with Error Correction

**Initial SQL:** `SELECT FROM WHERE;`

#### Iteration 1

- **Detected Error:** `syntax.sql_syntax_error`
- **Reason:** Missing SELECT columns and FROM table name
- **Fix Plan:** Add columns after SELECT and table name after FROM
- **Corrected SQL:** `SELECT * FROM table_name WHERE;`

#### Iteration 2

- **Detected Error:** `syntax.sql_syntax_error`
- **Reason:** WHERE clause has no condition specified
- **Fix Plan:** Add valid condition to filter by country = 'USA'
- **Corrected SQL:** `SELECT * FROM table_name WHERE country = 'USA';`

#### Iteration 3

- **Detected Error:** `schema_link.table_missing`
- **Reason:** Table 'table_name' does not exist in schema
- **Fix Plan:** Replace 'table_name' with correct table 'users'
- **Corrected SQL:** `SELECT * FROM users WHERE country = 'USA';`

### Final Result

**Success:** ✅ True (Iterations: 4)

**Final SQL:**

```sql
SELECT * FROM users WHERE country = 'USA';
```

**Query Results:**

```json
[
  {
    "id": 4,
    "name": "Hana",
    "country": "USA",
    "signup_date": "2023-09-27"
  },
  {
    "id": 11,
    "name": "Charlie",
    "country": "USA",
    "signup_date": "2024-09-12"
  },
  {
    "id": 19,
    "name": "Bob",
    "country": "USA",
    "signup_date": "2024-05-16"
  }
]
```

## Development

To extend the system:

1. Add new agents in `agents/` directory
2. Update error taxonomy in `config/error_taxonomy.json`
3. Modify pipeline in `pipeline.py` to include new agents

## License

Proprietary - SQL-of-Thought Project

## Notes

- The pipeline includes a maximum iteration limit (default: 5) to prevent infinite correction loops
- All LLM calls use temperature=0 for deterministic outputs
- The system currently supports SQLite databases
