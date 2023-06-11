from flask_app import app
from flask import render_template, redirect, request

from flask_app.models.book import Book
from flask_app.models.author import Author


# Create 
@app.route("/create/book", methods = ["POST"])
def create_book():
    data = {
        "name": request.form["new_book_name"],
        "num_of_pages": request.form["new_book_pages"]
    }
    Book.create_book(data)
    return redirect("/books")

@app.route("/create/author/favorite", methods = ["POST"])
def liked_by_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.author_favorite_book(data)
    return redirect(f"/book/{request.form['book_id']}")
# Read
# View all books
@app.route("/books")
def read_all_books():
    books = Book.get_all_books()
    authors = Author.get_all_authors()
    return render_template("/books.html", books = books, authors=authors)
                                    # Left of equal = Bucket, # Right of equal = Data
@app.route("/book/<int:book_id>")
def get_book_by_id(book_id):
    book_info = Book.get_one_book(book_id)
    authors = Author.get_all_authors()
    favorited_by = Book.get_book_favorites({"id": book_id})
    return render_template("book_info.html", book = book_info, authors = authors, favorited_by = favorited_by) 

# Update

# Delete