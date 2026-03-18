print("SERVER STARTING...")
from flask import Flask, request, redirect, render_template, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Use a writable database location for production (Render, etc.).
# On Windows (local dev), we keep the database in the project folder.
if os.name == 'nt':
    DB_PATH = "doubts.db"
else:
    DB_PATH = os.environ.get("DB_PATH", "/tmp/doubts.db")


def get_db_connection():
    return sqlite3.connect(DB_PATH)

# ---------------- DATABASE ----------------
def init_db():
    conn = get_db_connection()
    conn = get_db_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # Questions table
    c.execute("""
    CREATE TABLE IF NOT EXISTS doubts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        question TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Answers table
    c.execute("""
    CREATE TABLE IF NOT EXISTS answers(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        doubt_id INTEGER,
        username TEXT,
        answer TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

# Initialize database on app startup
init_db()

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users(email,password) VALUES(?,?)",
                      (email,password))
            conn.commit()
        except:
            return render_template('register.html', error="Email already exists!")
        conn.close()
        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?",
                  (email,password))
        user = c.fetchone()
        conn.close()

        if user:
            session['email'] = email
            return redirect('/')
        else:
            return render_template('login.html', error="Invalid email or password")

    return render_template('login.html')

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

# ---------------- HOME ----------------
@app.route('/')
def home():
    if 'email' not in session:
        return redirect('/login')

    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM doubts ORDER BY created_at DESC")
    doubts = c.fetchall()
    conn.close()

    return render_template('index.html', doubts=doubts, user=session['email'])

# ---------------- POST QUESTION ----------------
@app.route('/post', methods=['GET','POST'])
def post():
    if 'email' not in session:
        return redirect('/login')

    if request.method == 'POST':
        question = request.form['question']

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO doubts(username,question) VALUES(?,?)",
                  (session['email'],question))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('post.html', user=session['email'])

# ---------------- VIEW DOUBT ----------------
@app.route('/doubt/<int:doubt_id>', methods=['GET','POST'])
def view_doubt(doubt_id):
    if 'email' not in session:
        return redirect('/login')

    conn = get_db_connection()
    c = conn.cursor()

    if request.method == 'POST':
        answer = request.form['answer']
        c.execute("INSERT INTO answers(doubt_id,username,answer) VALUES(?,?,?)",
                  (doubt_id,session['email'],answer))
        conn.commit()

    c.execute("SELECT * FROM doubts WHERE id=?", (doubt_id,))
    doubt = c.fetchone()

    c.execute("SELECT * FROM answers WHERE doubt_id=?",
              (doubt_id,))
    answers = c.fetchall()

    conn.close()

    return render_template('doubt.html', doubt=doubt, answers=answers, user=session['email'])

# ---------------- RUN ----------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)