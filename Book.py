from datetime import datetime, timedelta


class Book:
    def __init__(self, isbn, title, authors, publisher=None, language=None, publicationYear=None, available=0):
        """
        Initializes a new instance of the Book class.

        Parameters
        ----------
        isbn : str
            The International Standard Book Number (ISBN) of the book.
        title : str
            The title of the book.
        authors : str
            The authors of the book, separated by a slash (/).
        publisher : str, optional
            The publisher of the book (default is None).
        language : str, optional
            The language of the book (default is None).
        publicationYear : int, optional
            The publication year of the book (default is None).
        available : int, optional
            The availability numbers of the book (default is 0).
        """
        self.isbn = isbn
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.language = language
        self.publicationYear = publicationYear
        self.available = available

    def __repr__(self):
        """
        Returns a string representation of the book, including title, authors, and ISBN.

        Returns
        -------
        str
            A string representation of the book, including title, authors, and ISBN.
        """
        return f"{self.title}\n~ {self.authors.split('/').join(', ')}\n~ {self.isbn}"

    def set_borrow_date(self):
        """
        Sets the borrow date and due date for the book when borrowed.
        """
        self.borrow_date = datetime.now()
        self.due_date = self.borrow_date + timedelta(days=7)

    def set_available_status(self, status):
        """
        Sets the availability number of the books.

        Parameters
        ----------
        status : int
            The availability number of the books.
        """
        self.available = status

    def showDueDate(self, borrow_date):
        """
        Returns the due date of the book.

        Parameters
        ----------
        borrow_date : datetime
            The date the book was borrowed.

        Returns
        -------
        due_date : datetime
            The due date of the book.
        """
        return self.borrow_date + timedelta(days=7)

    def reservationStatus(self):
        """
        Returns the availability number of the books.

        Returns
        -------
        available : int
            The availability number of the books.
        """
        return self.available
