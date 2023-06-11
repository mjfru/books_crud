from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self, data):
        if "books.id" in data:
            self.id = data['books.id'] 
            self.name = data['books.name']
            self.num_of_pages = data['num_of_pages']
            self.created_at = data['books.created_at']
            self.updated_at = data['books.updated_at']
            self.favorited_authors = []
        else:
            self.id = data['id']
            self.name = data['name']
            self.num_of_pages = data['num_of_pages']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
            self.favorited_authors = []
            # self.somethingElseThisClassMightContain = []
            # I.E. Dojos and Ninjas example, dojos has an empty list of ninjas

# CREATE
    # Make sure to indent when making a class method
    @classmethod
    def create_book(cls, data):
        query = "INSERT INTO books (name, num_of_pages, created_at, updated_at) VALUES (%(name)s, %(num_of_pages)s, NOW(), NOW());"
        return connectToMySQL('books').query_db(query, data)

# READ
    # Getting all books
    @classmethod
    def get_all_books(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL('books').query_db(query)
        books = []
        for book in results:
            books.append(cls(book))
        return books
    
    # Getting a book by id
    @classmethod
    def get_one_book(cls, book_id):
        query = "SELECT * FROM books WHERE id = %(book_id)s"
        data = {
            "book_id": book_id
        }
        results = connectToMySQL('books').query_db(query, data)
        book = results[0]
        return book
    
    @classmethod
    def get_book_favorites(cls, data):
        query = """
        SELECT * FROM books 
        LEFT JOIN favorites ON books.id = favorites.book_id
        LEFT JOIN authors ON authors.id = favorites.author_id
        WHERE books.id = %(id)s;
        """
        results = connectToMySQL('books').query_db(query, data)
        book_favorite = cls(results[0])
        # print('$$$$$$$$$$$$', results)
        for result in results:
            if result['authors.id'] is None:
                break
            data = {
                "id": result['authors.id'],
                "name": result['authors.name'],
                "created_at": result['authors.created_at'],
                "updated_at": result['authors.updated_at']
            }
            book_favorite.favorited_authors.append(author.Author(data))
        # print(results)
        return book_favorite
# UPDATE

# DELETE