
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT")
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/borrow", methods=["GET", "POST"])
def borrow():
    conn = get_db_connection()
    cur = conn.cursor()
    if request.method == "POST":
        reader_id = request.form["reader_id"]
        book_id = request.form["book_id"]
        borrow_date = datetime.now().date()
        return_date = None
        cur.execute("INSERT INTO borrow_records (reader_id, book_id, borrow_date, return_date) VALUES (%s, %s, %s, %s)",
                    (reader_id, book_id, borrow_date, return_date))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("borrow"))
    else:
        cur.execute("SELECT id, name FROM readers")
        readers = cur.fetchall()
        cur.execute("SELECT id, title FROM books")
        books = cur.fetchall()
        cur.close()
        conn.close()
        return render_template("borrow.html", readers=readers, books=books)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
