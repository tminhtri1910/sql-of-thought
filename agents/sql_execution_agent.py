# agents/sql_execution_agent.py

import sqlite3

def execute_sql(sql: str, db_path: str = "demo.db") -> dict:
    """
     Executes SQL and returns a tuple:
        (success: bool, result_or_error: Any)

    On success:
        return True, results (list[dict])

    On error:
        return False, "error message"
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        success=True
        
        # extract column names safely
        columns = [col[0] for col in cursor.description] if cursor.description else []
        results = [dict(zip(columns, row)) for row in rows]

        return success, results

    except Exception as e:
        # Return the raw DB error so the LLM can classify it
        success = False
        error = str(e)

        return success, error

    finally:
        conn.close()

