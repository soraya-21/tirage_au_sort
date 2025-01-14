from flask import Flask, request, render_template, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Make sure to use a secure key in production

# Database configuration
DATABASE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    # Return rows as dictionaries
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create users table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
        print("Initialized the database.")

# Initialize the database when the application starts
init_db()

# Context processor to inject current_year into all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

# Home Route
@app.route("/")
def home():
    return render_template("index.html")

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username").strip()
        password = request.form.get("password")
        email = request.form.get("email").strip().lower()

        # Validate form data
        if not (username and password and email):
            return render_template("register.html", message="All fields are required.")

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert user into the database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, hashed_password)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            # Handle unique constraint failures
            if "UNIQUE constraint failed: users.username" in str(e):
                message = "Username already exists."
            elif "UNIQUE constraint failed: users.email" in str(e):
                message = "Email already registered."
            else:
                message = "Registration failed. Please try again."
            return render_template("register.html", message=message)

    return render_template("register.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get form data
        username = request.form.get("username").strip()
        password = request.form.get("password")

        # Validate form data
        if not (username and password):
            return render_template("login.html", message="Both fields are required.")

        # Retrieve user from the database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        # Check if user exists and password is correct
        if user and check_password_hash(user['password'], password):
            session["user_id"] = user['id']
            session["username"] = user['username']
            return redirect(url_for('userhome'))
        else:
            return render_template("login.html", message="Invalid username or password.")

    return render_template("login.html")

# User Home route
@app.route("/userhome")
def userhome():
    if "user_id" not in session:
        return redirect(url_for('login'))
    return render_template("userhome.html", username=session.get("username"))

# Logout route
@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('home'))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)