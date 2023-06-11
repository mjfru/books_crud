from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.somethingElseThisClassMightContain = []
            # I.E. Dojos and Ninjas example, dojos has an empty list of ninjas
        self.favorite_books = []

# CREATE
    # Make sure to indent when making a class method
    @classmethod
    def create_author(cls, data):
        query = "INSERT INTO authors (name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());"
        return connectToMySQL('books').query_db(query, data)

    # 'Favorite a book', incorporate the middle table, can only use ids provided
    # Method found in Books query from old assignment!
    @classmethod
    def author_favorite_book(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s)"
        return connectToMySQL('books').query_db(query, data)
# READ
    # Show all authors - intended for the home page
    @classmethod
    def get_all_authors(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books').query_db(query)
        authors = []
        for author in results:
            authors.append(cls(author))
        return authors

    @classmethod
    def get_one_author(cls, author_id):
        query = "SELECT * FROM authors WHERE id = %(author_id)s"
        data = {
            "author_id": author_id
        }
        results = connectToMySQL('books').query_db(query, data)
        author = results[0]
        return author

# Notes for remembering later (sorry Aaron or the TA looking at this mess):
# The first LEFT JOIN matches the authors table with the favorites table, matching the ID in the authors table to the authod_id in the favorites table.
# The second LEFT JOIN matches the books and the favorites table together, then matches those with an id the same as the author ID.     

    @classmethod
    def get_author_favorites(cls, data):
        query = """
        SELECT * FROM authors 
        LEFT JOIN favorites ON authors.id = favorites.author_id
        LEFT JOIN books ON books.id = favorites.book_id
        WHERE authors.id = %(id)s;
        """
        # data = {...} Was here, is now in the class Book (line 6-11) as an if/else statement
        results = connectToMySQL('books').query_db(query, data)
        author_favorite = cls(results[0])
        print('$$$$$$$$$$$$', results)
        for result in results:
            if result['books.id'] is None:      # New info from 'old' Python material to handle a case where an author hasn't favorited anything yet, e.g. a new author just added.
                break
            author_favorite.favorite_books.append(book.Book(result))
            # print(author_favorite)
            # print(author_favorite.favorite_books)
        return author_favorite
    
# UPDATE

# DELETE