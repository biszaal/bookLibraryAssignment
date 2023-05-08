from User import User
from Account import Account
from Book import Book

class Librarian(User):
    def __init__(self, uid, name, password):
        """
        init

        Parameters

        uid : str
            The user ID of the librarian.
        name : str
            The name of the librarian.
        password : str
            The password for the librarian account.

        """
        user = super().__init__(uid, name, password, "librarian")

    def add_book(self, db, isbn, title, author, publisher, language, publication_year, available):
        """
        add_book

        Parameters

        db : Database object
            An instance of the database object to interact with the database.
        isbn : str
            The International Standard Book Number (ISBN) of the book.
        title : str
            The title of the book.
        author : str
            The author of the book.
        publisher : str
            The publisher of the book.
        language : str
            The language of the book.
        publication_year : int
            The publication year of the book.
        available : int
            The availability numbers of books.

        """
        book = Book(isbn, title, authors, publisher,
                    language, publication_year, available)
        db.insert_book(book)

    def delete_book(self, db, isbn):
        """
        delete_book

        Parameters

        db : Database object
            An instance of the database object to interact with the database.
        isbn : str
            The International Standard Book Number (ISBN) of the book.

        """
        db.delete_book(isbn)
        print(f"Book with isbn: {isbn} has been deleted.")

    def display_book(self, db, isbn):
        """
        display_book

        Parameters

        db : Database object
            An instance of the database object to interact with the database.
        isbn : str
            The International Standard Book Number (ISBN) of the book.

        """
        book = db.get_book(isbn)
        if book:
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Publisher: {book[3]}")
            print(f"Language: {book[4]}")
            print(f"Publication Year: {book[5]}")
            print(f"Available: {book[6]}")
        else:
            print("Book not found")

    def view_user_record(self, db, uid):
        """
        view_user_record

        Parameters

        db : Database object
            An instance of the database object to interact with the database.
        uid : str
            The user ID of the user whose records need to be viewed.

        """
        borrowed_books = db.get_borrowed_books_by_uid(uid)
        reserved_books = db.get_reserved_books_by_uid(uid)
        returned_books = db.get_returned_books_by_uid(uid)

        print(f"\nUser ID: {uid}")
        print("Borrowed Books:")
        for book in borrowed_books:
            print(f"ISBN: {book[1]}, Title: {book[2]}, Borrow Date: {book[3]}")

        print("\nReserved Books:")
        for book in reserved_books:
            print(
                f"ISBN: {book[1]}, Title: {book[2]}, Reserve Date: {book[3]}")

        print("\nReturned Books:")
        for book in returned_books:
            print(
                f"ISBN: {book[1]}, Title: {book[2]}, Return Date: {book[3]}")
        print()

    def view_user_details(self, db, uid):
        """
        view_user_details

        Parameters

        db : Database object
            An instance of the database object to interact with the database.
        uid : str
            The user ID of the user whose details need to be viewed.

        """
        user_data = db.get_user(uid)
        user_data = User(user_data[0], user_data[1], user_data[2], user_data[3])
        if user_data:
            print(f"User ID: {user_data.uid}")
            print(f"Name: {user_data.name}")
            print(f"User Type: {user_data.uType}")
        else:
            print("User not found")

    def update_account(self, db, uid, num_returnedBooks=None, num_reservedBooks=None, num_borrowedBooks=None, num_lostBooks=None, fineAmount=None):
        """
        update_account

        Parameters

        db : Database object
            An instance of the database object to interact with the database.
        uid : str
            The user ID of the user whose account needs to be updated.
        num_returnedBooks : int, optional
            The number of returned books for the user (default is None).
        num_reservedBooks : int, optional
            The number of reserved books for the user (default is None).
        num_borrowedBooks : int, optional
            The number of borrowed books for the user (default is None).
        num_lostBooks : int, optional
            The number of lost books for the user (default is None).
        fineAmount : float, optional
            The fine amount for the user (default is None).

        """
        db.update_account(uid, num_returnedBooks, num_reservedBooks, num_borrowedBooks, num_lostBooks, fineAmount)
        print(f"Account with User ID: {uid} has been updated.")

    def update_book_availability(self, db, isbn, available):
        """
        update_book_availability

        Parameters

        db : Database object
            An instance of the database object to interact with the database.
        isbn : str
            The International Standard Book Number (ISBN) of the book.
        available : int
            The availability status of the book (0 or 1).

        """
        book = db.get_book(isbn)
        if book:
            db.update_book_availability(isbn, available)
        else:
            print("The book does not exists.")

    def view_all_borrowed_books(self, db):
        """
        view_all_borrowed_books

        Parameters

        db : Database object
            An instance of the database object to interact with the database.

        """
        borrowed_books = db.get_all_borrowed_books()
        if borrowed_books:
            for book in borrowed_books:
                print(
                    f"ISBN: {book[0]}, Borrowed User ID: {book[1]}, Borrow Date: {book[2]}")
        else:
            print("No borrowed books found")

    def view_all_reserved_books(self, db):
        """
        view_all_reserved_books

        Parameters

        db : Database object
            An instance of the database object to interact with the database.

        """
        reserved_books = db.get_all_reserved_books()
        if reserved_books:
            for book in reserved_books:
                print(
                    f"ISBN: {book[0]}, Reserved User ID: {book[1]}, Borrow Date: {book[2]}")
        else:
            print("No reserved books found")
    
    def view_all_returned_books(self,db):
        """
        view_all_returned_books

        Parameters

        db : Database object
            An instance of the database object to interact with the database.

        """
        returned_books = db.get_all_returned_books()
        if returned_books:
            for book in returned_books:
                print(
                    f"ISBN: {book[0]}, User ID: {book[1]}, Borrow Date: {book[2]}, Return Date: {book[3]}")
        else:
            print("No returned books found")
    
    def verify_user(self, db, uid):
        """
        verify_user

        Parameters

        db : Database object
            An instance of the database object to interact with the database.
        uid : str
            The user ID of the user to be verified.

        Returns

        bool
            True if the user exists, False otherwise.

        """
        user_data = db.get_user(uid)
        return not not user_data

    def lib_menu(self, db):
        """
        lib_menu

        Parameters

        db : Database object
            An instance of the database object to interact with the database.

        Displays a menu for librarian actions and handles the selected action.

        """
        account_obj = db.get_account(self.uid)
        account = Account(
            self.uid, account_obj[3], account_obj[2], account_obj[1], account_obj[4], account_obj[5])
        while True:
            print("""
                1. Borrow books
                2. Return books
                3. Search books
                4. Reserve books
                5. Renew a book
                6. View user records
                7. View account details
                8. Add a book
                9. Delete a book
               10. Update a book
               11. Display a book
               12. View user details
               13. View all borrowed books
               14. View all reserved books
               15. Update user's account
               16. View book report
                q. Quit
                """)
            choice = input("Select your choice: ")
            
            if choice == 'q':
                break
            elif choice == '1':
                isbn = input("Enter the ISBN of the book to borrow: ")
                super().borrow_book(db, isbn)
            elif choice == '2':
                isbn = input("Enter the ISBN of the book to return: ")
                super().return_book(db, isbn)
            elif choice == '3':
                keyword = input("Enter the keyword to search a book: ")
                super().search_books(db, keyword)
            elif choice == '4':
                isbn = input("Enter the ISBN of the book to reserve: ")
                super().reserve_book(db, isbn)
            elif choice == '5':
                isbn = input("Enter the ISBN of the book to renew: ")
                super().renew_book(db, isbn)
            elif choice == '6':
                uid = input("Enter the uid of the user: ")
                self.view_user_record(db, uid)
            elif choice == '7':
                print(f"Account details for {self.name}:")
                print(f"User ID: {self.uid}")
                print(f"User Type: {self.uType}")
                print(f"No. of Borrowed Books: {account.no_borrowed_books}")
                print(f"No. of Reserved Books: {account.no_reserved_books}")
                print(f"No. of Returned Books: {account.no_returned_books}")
                print(f"No. of Lost Books: {account.no_lost_books}")
                print(f"Fine Amount: ${account.fine_amount}")
            elif choice == '8':
                isbn = input("Enter the book isbn: ")
                title = input("Enter the book title: ")
                author = input("Enter the book author: ")
                publisher = input("Enter the book publisher: ")
                language = input("Enter the book language: ")
                publication_year = input("Enter the book publication year: ")
                available = int(input("Enter the number of available books: "))
                self.add_book(db, title, author, publisher, language,
                              publication_year, available)
            elif choice == '9':
                isbn = input("Enter the ISBN of the book to delete: ")
                self.delete_book(db, isbn)
            elif choice == '10':
                isbn = input("Enter the ISBN of the book to update: ")
                available = int(input("Enter the new number of available books: "))
                self.update_book_availability(db, isbn, available)
            elif choice == '11':
                isbn = input("Enter the ISBN of the book to display: ")
                self.display_book(db, isbn)
            elif choice == '12':
                uid = input("Enter the user ID to view their details: ")
                self.view_user_details(db, uid)
            elif choice == '13':
                self.view_all_borrowed_books(db)
            elif choice == '14':
                self.view_all_reserved_books(db)
            elif choice == '15':
                print("\nUpdate Account")
                uid = input("Enter the User ID: ")
                if not self.verify_user(db, uid):
                    print("User does not exists with that uid.")
                else:
                    num_returnedBooks = input(
                        "Enter the number of returned books (press enter to skip): ")
                    num_reservedBooks = input(
                        "Enter the number of reserved books (press enter to skip): ")
                    num_borrowedBooks = input(
                        "Enter the number of borrowed books (press enter to skip): ")
                    num_lostBooks = input(
                        "Enter the number of lost books (press enter to skip): ")
                    fineAmount = input("Enter the fine amount (press enter to skip): ")

                    # Convert inputs to appropriate types or set to None if not provided
                    num_returnedBooks = int(
                        num_returnedBooks) if num_returnedBooks else None
                    num_reservedBooks = int(
                        num_reservedBooks) if num_reservedBooks else None
                    num_borrowedBooks = int(
                        num_borrowedBooks) if num_borrowedBooks else None
                    num_lostBooks = int(num_lostBooks) if num_lostBooks else None
                    fineAmount = float(fineAmount) if fineAmount else None

                    self.update_account(db, uid, num_returnedBooks, num_reservedBooks,
                                            num_borrowedBooks, num_lostBooks, fineAmount)
            elif choice == '16':
                print("\nView List of Borrowed, Returned, and Reserved Books")
                print("\nBorrowed Books:")
                self.view_all_borrowed_books(db)
                print("\Reserved Books:")
                self.view_all_reserved_books(db)
                print("\Returned Books:")
                self.view_all_returned_books(db)
            else:
                print("Invalid choice. Please try again.")
