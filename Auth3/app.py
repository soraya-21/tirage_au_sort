from flask import Flask, request, render_template, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key in production

# Database configuration
DATABASE = 'users1.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    # Return rows as dictionaries
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db_connection()
        cursor = conn.cursor()
        # Create users table with is_admin field
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0
            )
        ''')
        # Insert default admin user
        default_admin_username = 'admin'
        default_admin_email = 'admin@example.com'
        default_admin_password = generate_password_hash('adminpassword')  # Change the password after setup

        try:
            cursor.execute(
                "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
                (default_admin_username, default_admin_email, default_admin_password, 1)
            )
            print("Created default admin user.")
        except sqlite3.IntegrityError:
            print("Admin user already exists.")
        
        conn.commit()
        conn.close()
        print("Initialized the database.")

# Initialize the database when the application starts
init_db()

# Context processor to inject current_year into all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.utcnow().year}

# Helper function to check if the current user is admin
def is_admin():
    return session.get('is_admin', False)

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
            flash("All fields are required.", "danger")
            return render_template("register.html")

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
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError as e:
            # Handle unique constraint failures
            if "UNIQUE constraint failed: users.username" in str(e):
                message = "Username already exists."
            elif "UNIQUE constraint failed: users.email" in str(e):
                message = "Email already registered."
            else:
                message = "Registration failed. Please try again."
            flash(message, "danger")
            return render_template("register.html")

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
            flash("Both fields are required.", "danger")
            return render_template("login.html")

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
            session["is_admin"] = bool(user['is_admin'])
            flash(f"Welcome, {user['username']}!", "success")
            if session["is_admin"]:
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('userhome'))
        else:
            flash("Invalid username or password.", "danger")
            return render_template("login.html")

    return render_template("login.html")

# User Home route
@app.route("/userhome")
def userhome():
    if "user_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('login'))
    return render_template("userhome.html", username=session.get("username"))

# Admin Dashboard route
@app.route("/admin")
def admin_dashboard():
    if not is_admin():
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, is_admin FROM users")
    users = cursor.fetchall()
    conn.close()
    return render_template("admin_dashboard.html", users=users)

# Create User route (Admin)
@app.route("/admin/create", methods=["GET", "POST"])
def create_user():
    if not is_admin():
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('home'))
    
    if request.method == "POST":
        # Get form data
        username = request.form.get("username").strip()
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")
        is_admin_flag = request.form.get("is_admin") == 'on'

        # Validate form data
        if not (username and email and password):
            flash("All fields except 'Is Admin' are required.", "danger")
            return render_template("create_user.html")
        
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert new user into the database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password, is_admin) VALUES (?, ?, ?, ?)",
                (username, email, hashed_password, int(is_admin_flag))
            )
            conn.commit()
            conn.close()
            flash("User created successfully.", "success")
            return redirect(url_for('admin_dashboard'))
        except sqlite3.IntegrityError as e:
            # Handle unique constraint failures
            if "UNIQUE constraint failed: users.username" in str(e):
                message = "Username already exists."
            elif "UNIQUE constraint failed: users.email" in str(e):
                message = "Email already registered."
            else:
                message = "User creation failed. Please try again."
            flash(message, "danger")
            return render_template("create_user.html")

    return render_template("create_user.html")

# Edit User route (Admin)
@app.route("/admin/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if not is_admin():
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('home'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        flash("User not found.", "warning")
        return redirect(url_for('admin_dashboard'))
    
    if request.method == "POST":
        # Get form data
        username = request.form.get("username").strip()
        email = request.form.get("email").strip().lower()
        password = request.form.get("password")  # Optional
        is_admin_flag = request.form.get("is_admin") == 'on'

        # Validate form data
        if not (username and email):
            flash("Username and Email are required.", "danger")
            return render_template("edit_user.html", user=user)
        
        # Prepare update statement
        if password:
            hashed_password = generate_password_hash(password)
            query = "UPDATE users SET username = ?, email = ?, password = ?, is_admin = ? WHERE id = ?"
            params = (username, email, hashed_password, int(is_admin_flag), user_id)
        else:
            query = "UPDATE users SET username = ?, email = ?, is_admin = ? WHERE id = ?"
            params = (username, email, int(is_admin_flag), user_id)
        
        try:
            cursor.execute(query, params)
            conn.commit()
            conn.close()
            flash("User updated successfully.", "success")
            return redirect(url_for('admin_dashboard'))
        except sqlite3.IntegrityError as e:
            # Handle unique constraint failures
            if "UNIQUE constraint failed: users.username" in str(e):
                message = "Username already exists."
            elif "UNIQUE constraint failed: users.email" in str(e):
                message = "Email already registered."
            else:
                message = "User update failed. Please try again."
            flash(message, "danger")
            return render_template("edit_user.html", user=user)

    conn.close()
    return render_template("edit_user.html", user=user)

# Delete User route (Admin)
@app.route("/admin/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if not is_admin():
        flash("Access denied: Admins only.", "danger")
        return redirect(url_for('home'))
    
    # Prevent admin from deleting themselves
    if session.get('user_id') == user_id:
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for('admin_dashboard'))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully.", "success")
    return redirect(url_for('admin_dashboard'))

# Logout route
@app.route("/logout")
def logout():
    # Clear the session
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

# Run the application
if __name__ == "__main__":
    app.run(debug=True)