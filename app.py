from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "24962496",
    database = "library_db"
)

print("Connected to library_db")

@app.route("/")
def index():
    cursor = conn.cursor(dictionary=True) # dictionary=True -> returns rows as dicts
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    # print(books)

    cursor.close()
    return render_template("index.html", books=books) 


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    author = request.form.get("author")
    status = request.form.get("status")

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO books (title, author, status) VALUES (%s, %s, %s)", 
        (title, author, status)
    )
    
    conn.commit() #Save changes
    cursor.close()
    return redirect("/")


@app.route("/delete/<int:book_id>", methods=["POST"])
def delete(book_id):

    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = %s", (book_id,))

    conn.commit()
    cursor.close()
    return redirect("/")

