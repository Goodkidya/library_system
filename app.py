from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret")

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/readers')
def readers():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM readers")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('readers.html', readers=rows, edit_reader=None)

@app.route('/add_reader', methods=['POST'])
def add_reader():
    name = request.form['name']
    email = request.form['email']
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO readers (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('readers'))

@app.route('/edit_reader/<int:reader_id>')
def edit_reader(reader_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM readers WHERE id = %s", (reader_id,))
    reader = cur.fetchone()
    cur.execute("SELECT * FROM readers")
    readers = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('readers.html', readers=readers, edit_reader=reader)

@app.route('/update_reader/<int:reader_id>', methods=['POST'])
def update_reader(reader_id):
    name = request.form['name']
    email = request.form['email']
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE readers SET name = %s, email = %s WHERE id = %s", (name, email, reader_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('readers'))

@app.route('/delete_reader/<int:reader_id>', methods=['POST'])
def delete_reader(reader_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM readers WHERE id = %s", (reader_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('readers'))


# --- Books ---
@app.route('/books')
def books():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    books = cur.fetchall()
                                        
                            
    cur.close()
    conn.close()
    return render_template('books.html', books=books)

@app.route("/add_book", methods=["POST"])
def add_book():
    title = request.form["title"]
    author = request.form["author"]

    conn = get_conn()
    cur = conn.cursor()
    # 加入 available=True
    cur.execute("INSERT INTO books (title, author, available) VALUES (%s, %s, TRUE)", (title, author))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for("books"))


@app.route('/delete_book/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id = %s", (book_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('books'))

# --- Borrow ---
from datetime import datetime

@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    conn = get_conn()
    cur = conn.cursor()
    if request.method == 'POST':
        reader_id = request.form['reader_id']
        book_id = request.form['book_id']
        borrow_date = datetime.now()

        # 新增借閱紀錄
        cur.execute(
            "INSERT INTO borrow_records (reader_id, book_id, borrow_date) VALUES (%s, %s, %s)",
            (reader_id, book_id, borrow_date)
        )
        # 設定書籍為不可借
        cur.execute("UPDATE books SET available = FALSE WHERE id = %s", (book_id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('borrow'))

    cur.execute("SELECT * FROM readers")
    readers = cur.fetchall()
    cur.execute("SELECT * FROM books WHERE available = TRUE")
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('borrow.html', readers=readers, books=books)

# --- Return ---
@app.route('/return', methods=['GET', 'POST'])
def return_book():
    conn = get_conn()
    cur = conn.cursor()
    if request.method == 'POST':
        record_id = request.form['record_id']
        cur.execute("UPDATE borrow_records SET return_date = NOW() WHERE id = %s", (record_id,))
        cur.execute("SELECT book_id FROM borrow_records WHERE id = %s", (record_id,))
        book_id = cur.fetchone()[0]
        cur.execute("UPDATE books SET available = TRUE WHERE id = %s", (book_id,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('return_book'))
    cur.execute("""
        SELECT br.id, r.name, b.title, br.borrow_date
        FROM borrow_records br
        JOIN readers r ON br.reader_id = r.id
        JOIN books b ON br.book_id = b.id
        WHERE br.return_date IS NULL
    """)
    records = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('return.html', records=records)

# --- Records ---
@app.route('/records')
def records():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT br.id, r.name, b.title, br.borrow_date, br.return_date
        FROM borrow_records br
        JOIN readers r ON br.reader_id = r.id
        JOIN books b ON br.book_id = b.id
        ORDER BY br.id DESC
    """)
    records = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('records.html', records=records)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
