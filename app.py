
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['DB_HOST'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        port=os.environ.get('DB_PORT', 5432)
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        reader_id = request.form['reader_id']
        book_id = request.form['book_id']
        cur.execute("INSERT INTO records (reader_id, book_id, status) VALUES (%s, %s, %s)", (reader_id, book_id, 'borrowed'))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    cur.execute("SELECT id, name FROM readers")
    readers = cur.fetchall()

    cur.execute("SELECT id, title FROM books")
    books = cur.fetchall()

    cur.close()
    conn.close()

    return render_template('borrow.html', readers=readers, books=books)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
