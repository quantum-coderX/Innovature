class Book:
    def __init__(self, book_id, title, author, isbn, available=True):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.available = available

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'available': self.available
        }

    def __str__(self):
        return f"Book({self.book_id}, {self.title}, {self.author}, {self.isbn}, {self.available})"