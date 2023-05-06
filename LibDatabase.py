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

    def create_books_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS books(
            isbn TEXT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            publisher TEXT,
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

    def insert_book(self, b):
        try:
            self.cursor.execute("INSERT INTO books (isbn, title, authors, publisher, available) VALUES (?, ?, ?, ?, ?)", (
                b.isbn, b.title, b.authors, b.publisher, b.available))
            self.conn.commit()
        except sqlite3.IntegrityError:
            print("Book already exists in the database.")

    def search(self, opt, s):
        s = '%' + s + '%'
        if opt in ['title', 'authors']:
            cmd = f'SELECT * FROM books WHERE {opt} LIKE ?'
            self.cursor.execute(cmd, (s,))
        return self.cursor.fetchall()
    
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

    def return_book(self, isbn, uid):
        self.conn = sqlite3.connect('main.sqlite')
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            "UPDATE books SET available=available+1 WHERE isbn=?", (isbn,))
        self.cursor.execute(
            "UPDATE accounts SET num_borrowedBooks=num_borrowedBooks-1 WHERE uid=?", (
                uid,))
        self.cursor.execute(
            "DELETE FROM borrowedBooks WHERE borrowID = (SELECT MIN(borrowID) FROM borrowedBooks WHERE uid=? AND isbn=?)", (uid, isbn,))
        self.conn.commit()

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

    def remove_book(self, b):
        self.cursor.execute("DELETE from books WHERE isbn=?", (b.isbn,))
        self.conn.commit()

    def get_users(self):
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
        try:
            if user.uType == "staff":
                self.cursor.execute("INSERT INTO users (uid, password, name, uType, department) VALUES (?, ?, ?, ?, ?)", (
                    user.uid, user.password, user.name, user.uType, user.department))
            elif user.uType == "student":
                self.cursor.execute("INSERT INTO users (uid, password, name, uType, studentClass) VALUES (?, ?, ?, ?, ?)", (
                    user.uid, user.password, user.name, user.uType, user.studentClass))
            self.conn.commit()
            self.insert_account(user.uid)
            print(f"User {user.uid} inserted successfully.")
        except sqlite3.IntegrityError:
            print(f"User {user.uid} already exists in the database.")

    def get_user(self, uid):
        self.cursor.execute(f'SELECT * FROM users WHERE uid=?', (uid,))
        return self.cursor.fetchone()

    def close(self):
        if self.conn:
            self.conn.close()
