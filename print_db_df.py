import sqlite3
import pandas as pd
import sys

def db_to_dfs(db_path: str = "demo.db"):
    conn = sqlite3.connect(db_path)
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn)
    dfs = {}
    for table in tables['name']:
        dfs[table] = pd.read_sql(f"SELECT * FROM '{table}';", conn)
    conn.close()
    return dfs

if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else "demo.db"
    dfs = db_to_dfs(db)
    for name, df in dfs.items():
        print(f"\n--- Table: {name} ({len(df)} rows) ---")
        print(df)