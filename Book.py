class Book:
    def __init__(self, isbn, title, authors, publisher=None, language=None, publicationYear=None, available=0):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.language = language
        self.publicationYear = publicationYear
        self.available = available

    def __repr__(self):
        return f"{self.title}\n~ {self.authors.split('/').join(', ')}\n~ {self.isbn}"

    def set_borrow_date(self):
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + datetime.timedelta(days=7)

    def set_available_status(self, status):
        self.available = status

    def showDueDate(self, borrow_date):
        return self.borrow_date + datetime.timedelta(days=7)

    def reservationStatus(self):
        return self.available
