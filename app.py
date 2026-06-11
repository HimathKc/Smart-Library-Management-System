import os
import sys
from functools import wraps

try:
    from flask import Flask, render_template, request, redirect, url_for, flash, session
    from dotenv import load_dotenv
    import mysql.connector
except ImportError:
    sys.exit("Required packages missing. Install with: pip install -r requirements.txt")

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "smart_library_dev_secret_key")


def get_db_connection():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "library_system_db"),
    )


# -------------------------
# Access Control
# -------------------------

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))

        if session.get("role") != "admin":
            flash("Admin access only.", "error")
            return redirect(url_for("user_dashboard"))

        return f(*args, **kwargs)
    return decorated


# -------------------------
# Auth
# -------------------------

@app.route("/")
def index():
    if "user_id" in session:
        if session.get("role") == "admin":
            return redirect(url_for("dashboard"))
        return redirect(url_for("user_dashboard"))

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        if session.get("role") == "admin":
            return redirect(url_for("dashboard"))
        return redirect(url_for("user_dashboard"))

    if request.method == "POST":
        username_or_email = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT * FROM users
            WHERE (username = %s OR email = %s)
            AND password = %s
            AND status = 'Active'
            """,
            (username_or_email, username_or_email, password),
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:
            session["user_id"] = user["user_id"]
            session["username"] = user["username"]
            session["role"] = user["role"]

            flash("Login successful.", "success")

            if user["role"] == "admin":
                return redirect(url_for("dashboard"))
            return redirect(url_for("user_dashboard"))

        flash("Invalid username/email or password.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# -------------------------
# Admin Dashboard
# -------------------------

@app.route("/dashboard")
@admin_required
def dashboard():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS cnt FROM books")
    total_books = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) AS cnt FROM books WHERE status = 'Available'")
    available_books = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) AS cnt FROM books WHERE status = 'Borrowed'")
    borrowed_books = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) AS cnt FROM members")
    total_members = cursor.fetchone()["cnt"]

    cursor.execute(
        """
        SELECT b.book_id, b.title, c.category_name, b.publication_year, b.status
        FROM books b
        JOIN categories c ON b.category_id = c.category_id
        ORDER BY b.book_id DESC
        LIMIT 5
        """
    )
    recent_books = cursor.fetchall()

    cursor.execute(
        """
        SELECT member_id, member_name, email, status
        FROM members
        ORDER BY member_id DESC
        LIMIT 5
        """
    )
    recent_members = cursor.fetchall()

    cursor.close()
    connection.close()

    stats = {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books,
        "total_members": total_members,
    }

    return render_template(
        "dashboard.html",
        stats=stats,
        recent_books=recent_books,
        recent_members=recent_members,
    )


# -------------------------
# User Dashboard
# -------------------------

@app.route("/user-dashboard")
@login_required
def user_dashboard():
    return render_template("user_dashboard.html")


# -------------------------
# Books
# -------------------------

@app.route("/books")
@login_required
def books():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            b.book_id,
            b.title,
            b.isbn,
            c.category_name,
            p.publisher_name,
            b.publication_year,
            b.status
        FROM books b
        JOIN categories c ON b.category_id = c.category_id
        JOIN publishers p ON b.publisher_id = p.publisher_id
        ORDER BY b.book_id
        """
    )

    books_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("books.html", books=books_data)


@app.route("/add-book", methods=["GET", "POST"])
@admin_required
def add_book():
    if request.method == "POST":
        title = request.form["title"].strip()
        isbn = request.form["isbn"].strip()
        author_name = request.form["author"].strip()
        category_name = request.form["category"].strip()
        publisher_name = request.form.get("publisher", "Unknown Publisher").strip() or "Unknown Publisher"
        publication_year = request.form.get("publication_year") or None

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT IGNORE INTO categories (category_name) VALUES (%s)",
            (category_name,),
        )
        cursor.execute(
            "SELECT category_id FROM categories WHERE category_name = %s",
            (category_name,),
        )
        category_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT IGNORE INTO publishers (publisher_name) VALUES (%s)",
            (publisher_name,),
        )
        cursor.execute(
            "SELECT publisher_id FROM publishers WHERE publisher_name = %s",
            (publisher_name,),
        )
        publisher_id = cursor.fetchone()[0]

        cursor.execute(
            "INSERT INTO authors (author_name) VALUES (%s)",
            (author_name,),
        )
        author_id = cursor.lastrowid

        cursor.execute(
            """
            INSERT INTO books (title, isbn, category_id, publisher_id, publication_year)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (title, isbn, category_id, publisher_id, publication_year),
        )
        book_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO book_authors (book_id, author_id) VALUES (%s, %s)",
            (book_id, author_id),
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Book added successfully!", "success")
        return redirect(url_for("books"))

    return render_template("add_book.html")


# -------------------------
# Members
# -------------------------

@app.route("/members")
@admin_required
def members():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM members ORDER BY member_id")
    members_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("members.html", members=members_data)


@app.route("/add-member", methods=["GET", "POST"])
@admin_required
def add_member():
    if request.method == "POST":
        member_name = request.form["name"].strip()
        email = request.form["email"].strip()
        phone = request.form["phone"].strip()
        address = request.form.get("address", "").strip()

        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO members (member_name, email, phone, address)
            VALUES (%s, %s, %s, %s)
            """,
            (member_name, email, phone, address),
        )

        connection.commit()

        cursor.close()
        connection.close()

        flash("Member added successfully!", "success")
        return redirect(url_for("members"))

    return render_template("add_member.html")


if __name__ == "__main__":
    app.run(debug=True)
