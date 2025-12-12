import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("demo.db")
cursor = conn.cursor()

# --- Sample users ---
countries = ["USA", "Vietnam", "Japan", "Germany", "Brazil"]
names = ["Alice", "Bob", "Charlie", "Daisy", "Ethan", "Fiona", "Gabe", "Hana"]

# Insert users
for i in range(1, 21):
    name = random.choice(names)
    country = random.choice(countries)

    signup_date = (
        datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))
    ).strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO users (id, name, country, signup_date) VALUES (?, ?, ?, ?)",
        (i, name, country, signup_date),
    )

# --- Sample orders ---
for i in range(1, 51):
    user_id = random.randint(1, 20)
    amount = round(random.uniform(10, 500), 2)
    created_at = (
        datetime(2023, 1, 1) + timedelta(days=random.randint(0, 700))
    ).strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO orders (id, user_id, amount, created_at) VALUES (?, ?, ?, ?)",
        (i, user_id, amount, created_at),
    )

conn.commit()
conn.close()

print("Sample data inserted into demo.db")
