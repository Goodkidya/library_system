from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 5432)
    )
    return conn

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/books", methods=["GET", "POST"])
def books():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        cur.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        conn.commit()

    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("books.html", books=books)

@app.route("/readers", methods=["GET", "POST"])
def readers():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        cur.execute("INSERT INTO readers (name, email) VALUES (%s, %s)", (name, email))
        conn.commit()

    cur.execute("SELECT * FROM readers")
    readers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("readers.html", readers=readers)

@app.route("/borrow", methods=["GET", "POST"])
def borrow_book():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        reader_id = request.form["reader_id"]
        book_id = request.form["book_id"]
        cur.execute("INSERT INTO records (reader_id, book_id) VALUES (%s, %s)", (reader_id, book_id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for("borrow_book"))

    cur.execute("SELECT id, name FROM readers")
    readers = cur.fetchall()
    cur.execute("SELECT id, title FROM books")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("borrow.html", readers=readers, books=books)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
