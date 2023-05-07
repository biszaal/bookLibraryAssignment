class Book:
    def __init__(self, isbn, title, authors, publisher=None, publicationYear=None, available=0):
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.publicationYear = publicationYear
        self.available = available

    def __repr__(self):
        return f"{self.title}\n~ {self.authors.split('/').join(', ')}\n~ {self.isbn}"

    def set_borrow_date(self):
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + datetime.timedelta(days=7)

    def set_reservation_status(self, status):
        self.reserved = status

    def showDueDate(self):
        return self.due_date

    def reservationStatus(self):
        return self.reserved

    def feedback(self):
        self.feedback_list.append(feedback_text)

    def bookRequest(self):
        pass

    def renewInfo(self):
        self.set_borrow_date()
