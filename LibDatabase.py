import sqlite3


class LibDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()
        self.create_books_table()
        self.create_users_table()
        self.create_accounts_table()
        self.create_borrowed_books_table()
        self.create_reserved_books_table()
        self.create_returned_books_table()

    def create_books_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS books(
            isbn TEXT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            publisher TEXT,
            language TEXT,
            publicationYear TEXT,
            available INTEGER
            )""")
        self.conn.commit()

    def create_accounts_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts(
            uid VARCHAR(255) PRIMARY KEY,
            num_returnedBooks INTEGER,
            num_reservedBooks INTEGER,
            num_borrowedBooks INTEGER,
            num_lostBooks INTEGER,
            fineAmount FLOAT
            )""")
        self.conn.commit()

    def create_users_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            uid TEXT PRIMARY KEY,
            name TEXT,
            password TEXT,
            uType TEXT,
            department TEXT,
            studentClass TEXT
        )""")
        self.conn.commit()


    def create_borrowed_books_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS borrowedBooks(
            borrowID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            uid TEXT,
            isbn TEXT,
            dateBorrowed TEXT
        )""")
        self.conn.commit()

    def create_reserved_books_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS reservedBooks(
            reserveID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            uid TEXT,
            isbn TEXT,
            dateReserved TEXT
        )""")
        self.conn.commit()

    def create_returned_books_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS returnedBooks(
            returnID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            uid TEXT,
            isbn TEXT,
            dateBorrowed TEXT,
            dateReturned TEXT
        )""")
        self.conn.commit()

    def get_all_returned_books(self):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = """SELECT * FROM returnedBooks"""
        self.cursor.execute(query)
        returned_books = self.cursor.fetchall()

        self.conn.close()
        return returned_books


    def get_account(self, uid):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = "SELECT * FROM accounts WHERE uid = ?"
        self.cursor.execute(query, (uid,))
        account_data = self.cursor.fetchone()

        self.conn.close()

        if account_data:
            return account_data
        return None

    def update_account(self, uid, num_returnedBooks=None, num_reservedBooks=None, num_borrowedBooks=None, num_lostBooks=None, fineAmount=None):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        if num_returnedBooks is not None:
            self.cursor.execute(
                "UPDATE accounts SET num_returnedBooks=? WHERE uid=?", (num_returnedBooks, uid))

        if num_reservedBooks is not None:
            self.cursor.execute(
                "UPDATE accounts SET num_reservedBooks=? WHERE uid=?", (num_reservedBooks, uid))

        if num_borrowedBooks is not None:
            self.cursor.execute(
                "UPDATE accounts SET num_borrowedBooks=? WHERE uid=?", (num_borrowedBooks, uid))

        if num_lostBooks is not None:
            self.cursor.execute(
                "UPDATE accounts SET num_lostBooks=? WHERE uid=?", (num_lostBooks, uid))

        if fineAmount is not None:
            self.cursor.execute(
                "UPDATE accounts SET fineAmount=? WHERE uid=?", (fineAmount, uid))

        self.conn.commit()
        self.conn.close()


    def insert_book(self, book):
        try:
            self.cursor.execute("INSERT INTO books (isbn, title, authors, publisher, language, publicationYear, available) VALUES (?, ?, ?, ?, ?, ?, ?)", (
                book.isbn, book.title, book.authors, book.publisher, book.language, book.publicationYear, book.available))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Book already exists in the database.")

    def delete_book(self, isbn):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = "DELETE FROM books WHERE isbn = ?"
        self.cursor.execute(query, (isbn,))

        self.conn.commit()
        self.conn.close()

    def update_book_availability(self, isbn, new_availability):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = "UPDATE books SET available = ? WHERE isbn = ?"
        self.cursor.execute(query, (new_availability, isbn))

        self.conn.commit()
        self.conn.close()
    
    def get_borrowed_book(self, isbn, uid):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = "SELECT * FROM borrowedBooks WHERE uid = ? AND isbn = ?"
        self.cursor.execute(query, (uid, isbn))
        borrowed_book_data = self.cursor.fetchone()

        self.conn.close()

        if borrowed_book_data:
            return borrowed_book_data
        return None
    
    def get_borrowed_books_by_uid(self, uid):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = """SELECT b.*, bb.dateBorrowed
                FROM borrowedBooks AS bb
                JOIN books AS b ON bb.isbn = b.isbn
                WHERE bb.uid = ?"""
        self.cursor.execute(query, (uid,))
        borrowed_books = self.cursor.fetchall()

        self.conn.close()
        return borrowed_books


    def get_reserved_books_by_uid(self, uid):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = """
            SELECT b.isbn, b.title, rb.dateReserved
            FROM reservedBooks as rb
            INNER JOIN books as b ON rb.isbn = b.isbn
            WHERE rb.uid = ?
        """
        self.cursor.execute(query, (uid,))
        results = self.cursor.fetchall()

        self.conn.close()
        return results

    def get_returned_books_by_uid(self, uid):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = """
            SELECT b.isbn, b.title, r.dateBorrowed, r.dateReturned
            FROM returnedBooks as r
            INNER JOIN books as b ON r.isbn = b.isbn
            WHERE r.uid = ?
        """
        self.cursor.execute(query, (uid,))
        results = self.cursor.fetchall()

        self.conn.close()
        return results

    def get_all_borrowed_books(self):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = """SELECT b.*, bb.dateBorrowed, bb.uid
                FROM borrowedBooks AS bb
                JOIN books AS b ON bb.isbn = b.isbn"""
        self.cursor.execute(query)
        borrowed_books = self.cursor.fetchall()

        self.conn.close()
        return borrowed_books


    def get_all_reserved_books(self):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = """SELECT b.*, rb.dateReserved, rb.uid
                FROM reservedBooks AS rb
                JOIN books AS b ON rb.isbn = b.isbn"""
        self.cursor.execute(query)
        reserved_books = self.cursor.fetchall()

        self.conn.close()
        return reserved_books


    def get_reserved_book(self, isbn, uid):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            "SELECT * FROM reservedBooks WHERE isbn=? AND uid=?", (isbn, uid,))
        reserved_book = self.cursor.fetchone()
        self.conn.close()

        return reserved_book

    def get_books(self):
        self.cursor.execute('SELECT * FROM books')
        return self.cursor.fetchall()

    def get_book(self, isbn):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = "SELECT * FROM books WHERE isbn = ?"
        self.cursor.execute(query, (isbn,))
        book_data = self.cursor.fetchone()

        self.conn.close()

        if book_data:
            return book_data
        return None

    def search_books(self, keyword):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = """
        SELECT * FROM books
        WHERE title LIKE ? OR authors LIKE ? OR publisher LIKE ? OR language LIKE ? OR publicationYear LIKE ?
        """
        wildcard_keyword = f"%{keyword}%"
        self.cursor.execute(
            query, (wildcard_keyword, wildcard_keyword, wildcard_keyword, wildcard_keyword, wildcard_keyword))

        results = self.cursor.fetchall()

        self.conn.close()
        return results

    def borrow_book(self, isbn, uid, date, isReserved):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        if isReserved:
            self.cursor.execute(
                "DELETE FROM reservedBooks WHERE reserveID = (SELECT MIN(reserveID) FROM reservedBooks WHERE uid=? AND isbn=?)", (uid, isbn,))
            self.cursor.execute(
                "UPDATE accounts SET num_reservedBooks=num_reservedBooks-1 WHERE uid=?", (uid,))
        self.cursor.execute(
            "UPDATE books SET available=available-1 WHERE isbn=? AND available > 0", (isbn,))
        self.cursor.execute(
            "UPDATE accounts SET num_borrowedBooks=num_borrowedBooks+1 WHERE uid=?", (uid,))
        self.cursor.execute(
            "INSERT INTO borrowedBooks (uid, isbn, dateBorrowed) VALUES (?, ?, ?)", (uid, isbn, date,))
        self.conn.commit()

    def return_book(self, isbn, uid, date_returned):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        # Fetch the dateBorrowed from the borrowedBooks table
        self.cursor.execute(
            "SELECT dateBorrowed FROM borrowedBooks WHERE uid=? AND isbn=?", (uid, isbn,))
        date_borrowed = self.cursor.fetchone()[0]

        self.cursor.execute(
            "UPDATE books SET available=available+1 WHERE isbn=?", (isbn,))
        self.cursor.execute(
            "UPDATE accounts SET num_borrowedBooks=num_borrowedBooks-1 WHERE uid=?", (
                uid,))
        self.cursor.execute(
            "UPDATE accounts SET num_returnedBooks=num_returnedBooks+1 WHERE uid=?", (
                uid,))
        self.cursor.execute(
            "DELETE FROM borrowedBooks WHERE borrowID = (SELECT MIN(borrowID) FROM borrowedBooks WHERE uid=? AND isbn=?)", (uid, isbn,))

        # Insert the returned book record into the returnedBooks table
        self.cursor.execute(
            "INSERT INTO returnedBooks (uid, isbn, dateBorrowed, dateReturned) VALUES (?, ?, ?, ?)", (uid, isbn, date_borrowed, date_returned,))

        self.conn.commit()
        self.conn.close()

    def renew_book(self, isbn, uid, new_borrow_date):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            "UPDATE borrowedBooks SET dateBorrowed=? WHERE borrowID = (SELECT MIN(borrowID) FROM borrowedBooks WHERE uid=? AND isbn=?)", (new_borrow_date, uid, isbn,))
        self.conn.commit()

    def reserve_book(self, isbn, uid, reserve_date):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            "INSERT INTO reservedBooks (uid, isbn, dateReserved) VALUES (?, ?, ?)", (uid, isbn, reserve_date,))
        self.cursor.execute(
            "UPDATE accounts SET num_reservedBooks=num_reservedBooks+1 WHERE uid=?", (uid,))
        self.conn.commit()

    def get_users(self):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()
        
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def insert_account(self, uid):
        try:
            self.cursor.execute("INSERT INTO accounts(uid, num_returnedBooks,num_reservedBooks,num_borrowedBooks,num_lostBooks,fineAmount) VALUES(?, ?, ?, ?, ?, ?)",
                                (uid, 0, 0, 0, 0, 0))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("User already exists in the database.")

    def update_fine(self, uid, fine_amount):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        query = "UPDATE accounts SET fineAmount = ? WHERE uid = ?"
        self.cursor.execute(query, (fine_amount, uid))

        self.conn.commit()
        self.conn.close()

    def insert_user(self, user):

        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        try:
            if user.uType == "staff":
                self.cursor.execute("INSERT INTO users (uid, password, name, uType, department) VALUES (?, ?, ?, ?, ?)", (
                    user.uid, user.password, user.name, user.uType, user.department))
            elif user.uType == "student":
                self.cursor.execute("INSERT INTO users (uid, password, name, uType, studentClass) VALUES (?, ?, ?, ?, ?)", (
                    user.uid, user.password, user.name, user.uType, user.studentClass))
            elif user.uType == "librarian":
                self.cursor.execute("INSERT INTO users (uid, password, name, uType) VALUES (?, ?, ?, ?)", (
                    user.uid, user.password, user.name, user.uType))
            self.conn.commit()
            self.insert_account(user.uid)
            print(f"User {user.uid} inserted successfully.")
        except sqlite3.IntegrityError:
            print(f"User {user.uid} already exists in the database.")

        self.conn.close()

    def get_user(self, uid):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        self.cursor.execute(f'SELECT * FROM users WHERE uid=?', (uid,))
        user = self.cursor.fetchone()

        self.conn.commit()
        self.conn.close()

        return user

    def close(self):
        if self.conn:
            self.conn.close()
