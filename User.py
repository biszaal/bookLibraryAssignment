from datetime import datetime, timedelta
from Account import Account
from Book import Book

class User:
    def __init__(self, uid, name, password, uType):
        """
        Initialize the User object with user ID, name, password, and user type.

        Parameters
        ----------
        uid : int
            The unique user ID.
        name : str
            The user's name.
        password : str
            The user's password.
        uType : str
            The user's type (admin or user).
        """
        self.uid = uid
        self.name = name
        self.password = password
        self.uType = uType

    def __repr__(self):
        """
        String representation of the User object.

        Returns
        -------
        str
            The string representation of the User object containing the user's name and type.
        """
        return f"{self.name}, {self.uType}"

    @classmethod
    def load_user(cls, db, uid):
        """
        Load a user from the database by user ID.

        Parameters
        ----------
        db : object
            The database object.
        uid : int
            The unique user ID.

        Returns
        -------
        User object
            The User object if found in the database, otherwise None.
        """
        user_data = db.get_user(uid)
        if user_data:
            return cls(user_data[0], user_data[1], user_data[2], user_data[3])
        return None

    def borrow_book(self, db, isbn):
        """
        Borrow a book from the library.

        Parameters
        ----------
        db : object
            The database object.
        isbn : str
            The unique ISBN of the book to borrow.

        Returns
        -------
        None
        """
        book = db.get_book(isbn)
        book = Book(book[0], book[1], book[2],
                    book[3], book[4], book[5], book[6])

        if not book:
            print("Incorrect ISBN.")
            return

        isAvailable = book.available > 0
        no_borrowed_books = db.get_account(self.uid)[3]
        isReserved = not not db.get_reserved_book(isbn, self.uid)
        
        if no_borrowed_books >= 5:
            print("You have already borrowed 5 books.")
            return

        if not(isAvailable or isReserved):
            print("Sorry, the book is unavailable at the moment!")
            return
        
        if book:
            borrow_date = datetime.now().strftime("%Y-%m-%d")
            db.borrow_book(isbn, self.uid, borrow_date, isReserved)
            print(f"You have successfully borrowed {book.title}")

        else:
            print("Error, Cannot borrow book")


    def return_book(self, db, isbn):
        """
        Return a borrowed book to the library.

        Parameters
        ----------
        db : object
            The database object.
        isbn : str
            The unique ISBN of the book to return.

        Returns
        -------
        None
        """
        book = db.get_book(isbn)
        if book:
            print(book)

            # Check if the book was borrowed by the user
            borrowed_book_data = db.get_borrowed_book(isbn, self.uid)

            if borrowed_book_data:
                borrow_date = datetime.strptime(borrowed_book_data[3], "%Y-%m-%d")
                today = datetime.now().strftime("%Y-%m-%d")
                days = (datetime.now() - borrow_date).days

                if days > 7:
                    account_obj = Account(db.get_account(self.uid))
                    fine = days-7
                    total_fine = account_obj.calculate_fine(fine)
                    db.update_fine(self.uid, total_fine)
                    print(
                        f"You have been charged {fine} pounds fine for overdue of {days} days")
                    print("Fine has been added to your account and can be paid later.")

                db.return_book(isbn, self.uid, today)
                print(f"You have successfully returned {book[1]}")
            else:
                print("This book was not borrowed by you. Cannot return the book.")

        else:
            print("Cannot return the book. Invalid ISBN.")

    def reserve_book(self, db, isbn):
        """
        Reserve a book that is currently unavailable in the library.

        Parameters
        ----------
        db : object
            The database object.
        isbn : str
            The unique ISBN of the book to reserve.

        Returns
        -------
        None
        """
        book = db.get_book(isbn)
        isAvailable = book[6] > 0

        if isAvailable:
            print("The book is available please select 1. to borrow the book.")
            return

        if book:
            print(book)
            reserve_date = datetime.now().strftime("%Y-%m-%d")
            db.reserve_book(isbn, self.uid, reserve_date)
            print(f"You have successfully reserved {book[1]}")

        else:
            print("Error, Cannot reserve book")

    def renew_book(self, db, isbn):
        """
        Renew a borrowed book, extending the due date.

        Parameters
        ----------
        db : object
            The database object.
        isbn : str
            The unique ISBN of the book to renew.

        Returns
        -------
        None
        """
        book = db.get_book(isbn)
        if book:
            print(book)

            # Check if the book was borrowed by the user
            borrowed_book_data = db.get_borrowed_book(isbn, self.uid)

            if borrowed_book_data:
                borrow_date = datetime.strptime(
                    borrowed_book_data[3], "%Y-%m-%d")
                days = (datetime.now() - borrow_date).days

                if days > 7:
                    account_obj = Account(db.get_account(self.uid))
                    fine = days-7
                    total_fine = account_obj.calculate_fine(fine)
                    db.update_fine(self.uid, total_fine)
                    print(
                        f"You have been charged {fine} pounds fine for overdue of {days} days")
                    print("Fine has been added to your account and can be paid later.")
                
                newDate = datetime.now().strftime("%Y-%m-%d")
                newDueDate = (datetime.now() + timedelta(days=7)
                              ).strftime("%Y-%m-%d")
                db.renew_book(isbn, self.uid, newDate)
                print(f"You have successfully renewed {book[1]}, the new due date is {newDueDate}")
            else:
                print("This book was not borrowed by you. Cannot renew the book.")

        else:
            print("Cannot renew the book. Invalid ISBN.")


    def search_books(self, db, keyword):
        """
        Search for books in the library using a keyword.

        Parameters
        ----------
        db : object
            The database object.
        keyword : str
            The keyword to search for books.

        Returns
        -------
        None
        """
        results = db.search_books(keyword)

        if results:
            print("Search results:")
            print(
                "ISBN | Title | Author | Publisher | Language | Publication Year | Available")
            for book in results:
                print(
                    f"{book[0]} | {book[1]} | {book[2]} | {book[3]} | {book[4]} | {book[5]} | {book[6]}")
        else:
            print("No results found.")

    def get_user_details(self, db):
        """
        Display the user's account details.

        Parameters
        ----------
        db : object
            The database object.

        Returns
        -------
        None
        """
        account_obj = db.get_account(self.uid)
        account = Account(
            self.uid, account_obj[3], account_obj[2], account_obj[1], account_obj[4], account_obj[5])
        print(f"Account details for {self.name}:")
        print(f"User ID: {self.uid}")
        print(f"User Type: {self.uType}")
        print(f"No. of Borrowed Books: {account.no_borrowed_books}")
        print(f"No. of Reserved Books: {account.no_reserved_books}")
        print(f"No. of Returned Books: {account.no_returned_books}")
        print(f"No. of Lost Books: {account.no_lost_books}")
        print(f"Fine Amount: ${account.fine_amount}")

    def menu(self, db):
        """
        Display the user menu and handle user input for performing various actions.

        Parameters
        ----------
        db : object
            The database object.

        Returns
        -------
        None
        """
        account_obj = db.get_account(self.uid)
        account = Account(self.uid, account_obj[3], account_obj[2], account_obj[1], account_obj[4], account_obj[5])
        while True:
            print("""
                    1. Borrow a book
                    2. Return a book
                    3. Search book
                    4. Reserve a book
                    5. Renew a book
                    6. Pay fines
                    7. View account details
                    q. Quit
                    """)

            choice = input("Select your choice: ")

            if choice == 'q':
                break
            elif choice == '1':
                isbn = input("Enter the ISBN of the book to borrow: ")
                self.borrow_book(db, isbn)
            elif choice == '2':
                isbn = input("Enter the ISBN of the book to return: ")
                self.return_book(db, isbn)
            elif choice == '3':
                keyword = input("Enter the keyword to search a book: ")
                self.search_books(db, keyword)
            elif choice == '4':
                isbn = input("Enter the ISBN of the book to reserve: ")
                self.reserve_book(db, isbn)
            elif choice == '5':
                isbn = input("Enter the ISBN of the book to renew: ")
                self.renew_book(db, isbn)
            elif choice == '6':
                print(f"Your fine is {account.fine_amount} pounds.")
                if account.fine_amount > 0:
                    amount = float(input("Enter the amount to pay: "))
                    account.pay_fine(db,amount)
            elif choice == '7':
                self.get_user_details(db)
            else:
                print("Invalid choice. Please try again.")
