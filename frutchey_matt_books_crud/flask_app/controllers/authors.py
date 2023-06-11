from flask_app import app
from flask import render_template, session, redirect, request

from flask_app.models.author import Author
from flask_app.models.book import Book

# Home screen / Displays all authors
@app.route("/")
def home():
    authors = Author.get_all_authors()
    return render_template("/authors.html", authors = authors)

# Create a new author
@app.route("/create/author", methods = ["POST"])
def create_author():
    data = {
        "name": request.form["new_author_name"]
    }
    Author.create_author(data)
    return redirect("/")

# Create a new favorite book
@app.route("/create/book/favorite", methods = ["POST"])
def create_favorite_book():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.author_favorite_book(data)
    return redirect(f"/author/{request.form['author_id']}")

# Reading and redirecting by ID
@app.route("/author/<int:author_id>")
def get_author_by_id(author_id):
    author_info = Author.get_one_author(author_id)
    author_favorites = Author.get_author_favorites({"id": author_id})
    books = Book.get_all_books()
    return render_template("author_info.html", author = author_info, books = books, author_favorites = author_favorites)
