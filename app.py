from flask import Flask, render_template, request
import sqlite3
from pipeline import run_full_pipeline

app = Flask(__name__)

def run_query(sql):
    conn = sqlite3.connect("demo.db")
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    conn.close()
    return cols, rows

@app.route("/", methods=["GET", "POST"])
def index():
    columns = rows = None
    response = None
    question = ""

    if request.method == "POST":
        question = request.form["question"]

        # TEMP: hardcoded SQL (we will replace this)
        sql = "SELECT * FROM users WHERE country = 'Vietnam';"

        columns, rows = run_query(sql)

        response = run_full_pipeline(question)

    return render_template("index.html", question=question, response=response)

if __name__ == "__main__":
    app.run(debug=True)
