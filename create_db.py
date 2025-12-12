import sqlite3

conn = sqlite3.connect("demo.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    signup_date TEXT
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    created_at TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
""")

conn.commit()
conn.close()

print("demo.db created with tables.")

