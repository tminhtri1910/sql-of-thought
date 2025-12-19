import sqlite3

def execute_sql(sql: str, db_path: str = "demo.db") -> dict:
    """
     Executes SQL and returns a tuple:
        (success: bool, result_or_error: Any)

    On success:
        return True, result (list[dict])

    On error:
        return False, "error message"
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        success = True
        
        # extract column names safely
        columns = [col[0] for col in cursor.description]
        result = [dict(zip(columns, row)) for row in rows]
        error_message = ""
        # return success, result

    except Exception as e:
        # Return the raw DB error so the LLM can classify it
        success = False
        columns = None
        rows = None
        result = ""
        error_message = str(e)

    finally:
        conn.close()

        return {
            'success': success, 
            'columns': columns,
            'rows': rows,
            'result': result,
            'error': error_message,
        }
